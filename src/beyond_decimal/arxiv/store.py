"""Local metadata/notes store. Paper PDFs are deliberately not mirrored."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .client import ArxivPaper


class ResearchStore:
    def __init__(self, path: str | Path = "data/arxiv/research.sqlite3"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS papers (
                arxiv_id TEXT PRIMARY KEY, metadata_json TEXT NOT NULL,
                fetched_at TEXT NOT NULL)""")
            db.execute("""CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, arxiv_id TEXT NOT NULL,
                note TEXT NOT NULL, created_at TEXT NOT NULL,
                FOREIGN KEY(arxiv_id) REFERENCES papers(arxiv_id))""")
            db.execute("""CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT NOT NULL,
                result_ids_json TEXT NOT NULL, created_at TEXT NOT NULL)""")
            db.execute("""CREATE TABLE IF NOT EXISTS search_cache (
                cache_key TEXT PRIMARY KEY, result_ids_json TEXT NOT NULL,
                fetched_at TEXT NOT NULL)""")

    def save_paper(self, paper: ArxivPaper) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as db:
            db.execute("INSERT INTO papers(arxiv_id, metadata_json, fetched_at) VALUES(?,?,?) ON CONFLICT(arxiv_id) DO UPDATE SET metadata_json=excluded.metadata_json, fetched_at=excluded.fetched_at", (paper.arxiv_id, json.dumps(paper.to_dict(), ensure_ascii=False), now))

    @staticmethod
    def _cache_key(query: str, start: int, max_results: int) -> str:
        return json.dumps([query.strip(), start, max_results], ensure_ascii=False, separators=(",", ":"))

    def get_cached_search(self, query: str, *, start: int = 0, max_results: int = 20, ttl_seconds: int = 86400) -> list[dict[str, Any]] | None:
        key = self._cache_key(query, start, max_results)
        with self._connect() as db:
            row = db.execute("SELECT result_ids_json, fetched_at FROM search_cache WHERE cache_key=?", (key,)).fetchone()
            if not row:
                return None
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(row["fetched_at"])).total_seconds()
            if age < 0 or age >= ttl_seconds:
                return None
            ids = json.loads(row["result_ids_json"])
            rows = db.execute(
                f"SELECT metadata_json FROM papers WHERE arxiv_id IN ({','.join('?' for _ in ids)})",
                ids,
            ).fetchall() if ids else []
        by_id = {item["arxiv_id"]: item for item in (json.loads(row["metadata_json"]) for row in rows)}
        return [by_id[paper_id] for paper_id in ids if paper_id in by_id]

    def save_search(self, query: str, papers: list[ArxivPaper], *, start: int = 0, max_results: int = 20) -> None:
        now = datetime.now(timezone.utc).isoformat()
        ids = [p.arxiv_id for p in papers]
        with self._connect() as db:
            for paper in papers:
                db.execute("INSERT INTO papers(arxiv_id, metadata_json, fetched_at) VALUES(?,?,?) ON CONFLICT(arxiv_id) DO UPDATE SET metadata_json=excluded.metadata_json, fetched_at=excluded.fetched_at", (paper.arxiv_id, json.dumps(paper.to_dict(), ensure_ascii=False), now))
            db.execute("INSERT INTO searches(query,result_ids_json,created_at) VALUES(?,?,?)", (query, json.dumps(ids), now))
            db.execute("INSERT INTO search_cache(cache_key,result_ids_json,fetched_at) VALUES(?,?,?) ON CONFLICT(cache_key) DO UPDATE SET result_ids_json=excluded.result_ids_json, fetched_at=excluded.fetched_at", (self._cache_key(query, start, max_results), json.dumps(ids), now))

    def get_paper(self, arxiv_id: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute("SELECT metadata_json FROM papers WHERE arxiv_id=?", (arxiv_id,)).fetchone()
        return json.loads(row["metadata_json"]) if row else None

    def add_note(self, arxiv_id: str, note: str) -> int:
        if not note.strip() or len(note) > 12000:
            raise ValueError("note must contain 1–12000 characters")
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as db:
            if not db.execute("SELECT 1 FROM papers WHERE arxiv_id=?", (arxiv_id,)).fetchone():
                raise LookupError("save the paper metadata before adding a note")
            cur = db.execute("INSERT INTO notes(arxiv_id,note,created_at) VALUES(?,?,?)", (arxiv_id, note.strip(), now))
            return int(cur.lastrowid)

    def list_papers(self, limit: int = 100) -> list[dict[str, Any]]:
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        with self._connect() as db:
            rows = db.execute("SELECT metadata_json FROM papers ORDER BY fetched_at DESC LIMIT ?", (limit,)).fetchall()
        return [json.loads(row["metadata_json"]) for row in rows]

    def list_notes(self, arxiv_id: str | None = None) -> list[dict[str, Any]]:
        with self._connect() as db:
            if arxiv_id:
                rows = db.execute("SELECT arxiv_id,note,created_at FROM notes WHERE arxiv_id=? ORDER BY id", (arxiv_id,)).fetchall()
            else:
                rows = db.execute("SELECT arxiv_id,note,created_at FROM notes ORDER BY id").fetchall()
        return [dict(row) for row in rows]
