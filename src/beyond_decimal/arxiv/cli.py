"""Command-line interface for the arXiv research integration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .client import ArxivClient
from .store import ResearchStore
from .workflow import literature_review, prepare_release, write_json


def main() -> None:
    parser = argparse.ArgumentParser(prog="beyond-decimal-arxiv")
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=20)
    get = sub.add_parser("get")
    get.add_argument("arxiv_id")
    note = sub.add_parser("note")
    note.add_argument("arxiv_id")
    note.add_argument("text")
    sub.add_parser("library")
    review = sub.add_parser("review")
    review.add_argument("--output", default="research/literature-review/inventory.json")
    release = sub.add_parser("preflight")
    release.add_argument("--author", required=True)
    release.add_argument("--category", required=True)
    release.add_argument("--license", required=True)
    release.add_argument("--root", default=".")
    release.add_argument("--output", default="research/paper/release-preflight.json")
    args = parser.parse_args()
    store = ResearchStore()
    client = ArxivClient()
    if args.command == "search":
        cached = store.get_cached_search(args.query, max_results=args.limit)
        if cached is not None:
            print(json.dumps({"cached": True, "papers": cached}, ensure_ascii=False, indent=2))
        else:
            papers = client.search(args.query, max_results=args.limit)
            store.save_search(args.query, papers, max_results=args.limit)
            print(json.dumps({"cached": False, "papers": [p.to_dict() for p in papers]}, ensure_ascii=False, indent=2))
    elif args.command == "get":
        paper = client.get_paper(args.arxiv_id)
        store.save_paper(paper)
        print(json.dumps(paper.to_dict(), ensure_ascii=False, indent=2))
    elif args.command == "note":
        print(store.add_note(args.arxiv_id, args.text))
    elif args.command == "library":
        print(json.dumps(store.list_papers(), ensure_ascii=False, indent=2))
    elif args.command == "review":
        payload = literature_review(store)
        write_json(args.output, payload)
        print(args.output)
    elif args.command == "preflight":
        payload = prepare_release(args.root, author_name=args.author, category=args.category, license_id=args.license)
        write_json(args.output, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
