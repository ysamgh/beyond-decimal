"""Human-gated research workflow and release-package checks."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any

from .client import ARXIV_ID_RE
from .store import ResearchStore

REQUIRED_RELEASE_FILES = (
    "research/paper/manuscript/main.tex",
    "research/paper/README.md",
)


def literature_review(store: ResearchStore) -> dict[str, Any]:
    """Return a structured evidence inventory; it does not invent synthesis."""
    papers = store.list_papers(limit=500)
    notes = store.list_notes()
    notes_by_id: dict[str, list[str]] = {}
    for item in notes:
        notes_by_id.setdefault(item["arxiv_id"], []).append(item["note"])
    entries = []
    for paper in papers:
        entries.append({
            "arxiv_id": paper["arxiv_id"], "title": paper["title"],
            "authors": paper["authors"], "published": paper["published"],
            "categories": paper["categories"], "abstract_url": paper["abstract_url"],
            "summary": paper["summary"], "research_notes": notes_by_id.get(paper["arxiv_id"], []),
            "review_status": "needs_human_synthesis",
        })
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "paper_count": len(entries), "papers": entries,
            "instruction": "Verify each source and write a human-checked synthesis. Metadata and abstracts are not full-paper peer review."}


def prepare_release(root: str | Path, *, author_name: str, category: str, license_id: str) -> dict[str, Any]:
    """Create a preflight report only. This function never submits to arXiv."""
    root = Path(root).resolve()
    checks = []
    for relative in REQUIRED_RELEASE_FILES:
        candidate = (root / relative).resolve()
        checks.append({"check": f"file:{relative}", "ok": candidate.is_relative_to(root) and candidate.is_file()})
    checks.extend([
        {"check": "author_name_confirmed", "ok": bool(author_name.strip()) and len(author_name) <= 200},
        {"check": "category_present", "ok": bool(re.fullmatch(r"[a-z-]+\.[A-Z]{2}", category))},
        {"check": "license_present", "ok": license_id in {"arxiv", "CC BY 4.0", "CC BY-SA 4.0", "CC BY-NC-SA 4.0", "CC BY-NC-ND 4.0", "CC0 1.0"}},
        {"check": "human_submission_required", "ok": True},
    ])
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(root),
        "checks": checks,
        "ready_for_human_review": all(item["ok"] for item in checks),
        "submission_performed": False,
        "approval_required": ["author identity", "author order", "affiliation", "category", "license", "final compiled source/PDF", "endorsement status"],
        "warning": "This is a local preflight checklist, not an arXiv validator or submission. The author must inspect and submit through arXiv's official interface.",
    }


def validate_arxiv_id(value: str) -> str:
    if not ARXIV_ID_RE.fullmatch(value):
        raise ValueError("invalid arXiv identifier")
    return value


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
