"""Read-only client for arXiv's public Atom API.

The client intentionally supports metadata discovery only. It does not submit,
modify, or delete arXiv records. Requests are serialized and throttled in
accordance with arXiv's legacy API terms (one request every three seconds).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import re
import threading
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

API_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
OPENSEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
ARXIV_ID_RE = re.compile(r"^(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?$", re.I)


@dataclass(frozen=True)
class ArxivPaper:
    arxiv_id: str
    title: str
    summary: str
    authors: tuple[str, ...]
    published: str | None
    updated: str | None
    categories: tuple[str, ...]
    primary_category: str | None
    abstract_url: str
    pdf_url: str
    doi: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["authors"] = list(self.authors)
        data["categories"] = list(self.categories)
        return data


def _text(node: ET.Element | None) -> str | None:
    if node is None or node.text is None:
        return None
    return " ".join(node.text.split())


def _safe_xml(payload: bytes) -> ET.Element:
    if len(payload) > 8_000_000:
        raise ValueError("arXiv API response exceeds the 8 MB safety limit")
    upper = payload[:4096].upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        raise ValueError("DTD/entity declarations are not accepted")
    return ET.fromstring(payload)


def _paper_from_entry(entry: ET.Element) -> ArxivPaper:
    raw_id = _text(entry.find(ATOM + "id")) or ""
    arxiv_id = raw_id.rsplit("/", 1)[-1]
    if not ARXIV_ID_RE.fullmatch(arxiv_id):
        raise ValueError(f"Unexpected arXiv identifier in API response: {arxiv_id!r}")
    title = _text(entry.find(ATOM + "title")) or ""
    summary = _text(entry.find(ATOM + "summary")) or ""
    authors = tuple(filter(None, (_text(a.find(ATOM + "name")) for a in entry.findall(ATOM + "author"))))
    categories = tuple(sorted({c.attrib["term"] for c in entry.findall(ATOM + "category") if c.attrib.get("term")}))
    primary = entry.find(ARXIV + "primary_category")
    doi = _text(entry.find(ARXIV + "doi"))
    return ArxivPaper(
        arxiv_id=arxiv_id,
        title=title,
        summary=summary,
        authors=authors,
        published=_text(entry.find(ATOM + "published")),
        updated=_text(entry.find(ATOM + "updated")),
        categories=categories,
        primary_category=primary.attrib.get("term") if primary is not None else None,
        abstract_url=f"https://arxiv.org/abs/{arxiv_id}",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
        doi=doi,
    )


class ArxivClient:
    """Small, serialized, throttled client for the official arXiv Atom API."""

    def __init__(self, *, min_interval: float = 3.1, timeout: float = 25.0, user_agent: str = "BeyondDecimalResearch/0.1 (research use)"):
        if min_interval < 3.0:
            raise ValueError("min_interval must be at least 3 seconds")
        self.min_interval = min_interval
        self.timeout = timeout
        self.user_agent = user_agent
        self._lock = threading.Lock()
        self._last_request = 0.0

    def _request(self, params: dict[str, str]) -> bytes:
        with self._lock:
            wait = self.min_interval - (time.monotonic() - self._last_request)
            if wait > 0:
                time.sleep(wait)
            request = Request(f"{API_URL}?{urlencode(params)}", headers={"User-Agent": self.user_agent, "Accept": "application/atom+xml"})
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    payload = response.read(8_000_001)
            except (HTTPError, URLError, TimeoutError) as exc:
                raise RuntimeError(f"arXiv API request failed: {exc}") from exc
            finally:
                self._last_request = time.monotonic()
        return payload

    def search(self, query: str, *, start: int = 0, max_results: int = 20, sort_by: str = "relevance", sort_order: str = "descending") -> list[ArxivPaper]:
        query = query.strip()
        if not query or len(query) > 500 or any(ord(ch) < 32 for ch in query):
            raise ValueError("query must contain 1–500 printable characters")
        if start < 0 or not 1 <= max_results <= 100:
            raise ValueError("start must be >= 0 and max_results must be between 1 and 100")
        if sort_by not in {"relevance", "lastUpdatedDate", "submittedDate"}:
            raise ValueError("unsupported sort_by value")
        if sort_order not in {"ascending", "descending"}:
            raise ValueError("unsupported sort_order value")
        root = _safe_xml(self._request({"search_query": query, "start": str(start), "max_results": str(max_results), "sortBy": sort_by, "sortOrder": sort_order}))
        return [_paper_from_entry(entry) for entry in root.findall(ATOM + "entry")]

    def get_paper(self, arxiv_id: str) -> ArxivPaper:
        if not ARXIV_ID_RE.fullmatch(arxiv_id):
            raise ValueError("invalid arXiv identifier")
        root = _safe_xml(self._request({"id_list": arxiv_id, "max_results": "1"}))
        entries = root.findall(ATOM + "entry")
        if not entries:
            raise LookupError(f"No arXiv record found for {arxiv_id}")
        return _paper_from_entry(entries[0])
