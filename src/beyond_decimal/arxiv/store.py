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

    def save_paper(self, paper: ArxivPaper) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as db:
            db.execute("INSERT INTO papers(arxiv_id, metadata_json, fetched_at) VALUES(?,?,?) ON CONFLICT(arxiv_id) DO UPDATE SET metadata_json=excluded.metadata_json, fetched_at=excluded.fetched_at", (paper.arxiv_id, json.dumps(paper.to_dict(), ensure_ascii=False), now))

    def save_search(self, query: str, papers: list[ArxivPaper]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as db:
            for paper in papers:
                db.execute("INSERT INTO papers(arxiv_id, metadata_json, fetched_at) VALUES(?,?,?) ON CONFLICT(arxiv_id) DO UPDATE SET metadata_json=excluded.metadata_json, fetched_at=excluded.fetched_at", (paper.arxiv_id, json.dumps(paper.to_dict(), ensure_ascii=False), now))
            db.execute("INSERT INTO searches(query,result_ids_json,created_at) VALUES(?,?,?)", (query, json.dumps([p.arxiv_id for p in papers]), now))

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
