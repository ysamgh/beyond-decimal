"""Optional MCP stdio server exposing read-only arXiv research tools."""
from __future__ import annotations

import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .client import ArxivClient
from .store import ResearchStore
from .workflow import literature_review, prepare_release

mcp = FastMCP("beyond-decimal-research")
client = ArxivClient()
store = ResearchStore(os.environ.get("BEYOND_DECIMAL_DB", "data/arxiv/research.sqlite3"))


@mcp.tool()
def search_papers(query: str, max_results: int = 20, start: int = 0) -> str:
    """Search arXiv's official Atom API and save descriptive metadata locally."""
    cached = store.get_cached_search(query, max_results=max_results, start=start)
    if cached is not None:
        return json.dumps({"cached": True, "papers": cached}, ensure_ascii=False, indent=2)
    papers = client.search(query, max_results=max_results, start=start)
    store.save_search(query, papers, max_results=max_results, start=start)
    return json.dumps({"cached": False, "papers": [p.to_dict() for p in papers]}, ensure_ascii=False, indent=2)


@mcp.tool()
def get_paper(arxiv_id: str) -> str:
    """Fetch one arXiv record by identifier and save its metadata."""
    paper = client.get_paper(arxiv_id)
    store.save_paper(paper)
    return json.dumps(paper.to_dict(), ensure_ascii=False, indent=2)


@mcp.tool()
def add_research_note(arxiv_id: str, note: str) -> str:
    """Attach a research note to a previously saved paper record."""
    store.add_note(arxiv_id, note)
    return "Research note saved."


@mcp.tool()
def list_library(limit: int = 100) -> str:
    """List locally saved arXiv metadata records (not paper PDFs)."""
    return json.dumps(store.list_papers(limit), ensure_ascii=False, indent=2)


@mcp.tool()
def build_literature_review() -> str:
    """Build a structured literature inventory from saved metadata and notes."""
    return json.dumps(literature_review(store), ensure_ascii=False, indent=2)


@mcp.tool()
def prepare_arxiv_release(author_name: str, category: str, license_id: str, repository_root: str = ".") -> str:
    """Run local preflight checks; never submits or uploads anything to arXiv."""
    report = prepare_release(Path(repository_root), author_name=author_name, category=category, license_id=license_id)
    return json.dumps(report, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
