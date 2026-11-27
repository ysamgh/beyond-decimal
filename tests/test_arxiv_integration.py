from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from beyond_decimal.arxiv.client import ArxivClient, _safe_xml, _paper_from_entry, ATOM
from beyond_decimal.arxiv.store import ResearchStore
from beyond_decimal.arxiv.workflow import prepare_release

ATOM_SAMPLE = b'''<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom"><entry><id>https://arxiv.org/abs/2401.01234v2</id><title> Test Paper </title><summary>A summary.</summary><author><name>Example Author</name></author><published>2024-01-01T00:00:00Z</published><updated>2024-01-02T00:00:00Z</updated><category term="math.NT"/><arxiv:primary_category term="math.NT"/></entry></feed>'''


class ArxivClientTests(unittest.TestCase):
    def test_parse_atom_record(self):
        root = _safe_xml(ATOM_SAMPLE)
        paper = _paper_from_entry(root.find(ATOM + "entry"))
        self.assertEqual(paper.arxiv_id, "2401.01234v2")
        self.assertEqual(paper.primary_category, "math.NT")
        self.assertEqual(paper.authors, ("Example Author",))

    def test_reject_dtd(self):
        with self.assertRaises(ValueError):
            _safe_xml(b'<!DOCTYPE feed [<!ENTITY x "y">]><feed/>')

    def test_reject_invalid_query_and_interval(self):
        with self.assertRaises(ValueError):
            ArxivClient(min_interval=1.0)
        with self.assertRaises(ValueError):
            ArxivClient().search(" ")

    def test_search_builds_expected_atom_request(self):
        client = ArxivClient(min_interval=3.0)
        with patch.object(client, "_request", return_value=ATOM_SAMPLE) as request:
            papers = client.search("all:modular arithmetic", max_results=5)
        self.assertEqual(len(papers), 1)
        self.assertEqual(request.call_args.args[0]["max_results"], "5")


class ResearchStoreTests(unittest.TestCase):
    def test_save_search_and_notes(self):
        with tempfile.TemporaryDirectory() as temp:
            store = ResearchStore(Path(temp) / "research.sqlite3")
            paper = _paper_from_entry(_safe_xml(ATOM_SAMPLE).find(ATOM + "entry"))
            store.save_search("all:test", [paper], max_results=10)
            self.assertEqual(store.get_paper(paper.arxiv_id)["title"], "Test Paper")
            cached = store.get_cached_search("all:test", max_results=10)
            self.assertEqual(cached[0]["arxiv_id"], paper.arxiv_id)
            self.assertIsNone(store.get_cached_search("all:test", max_results=11))
            store.add_note(paper.arxiv_id, "Relevant to coding schemes.")
            self.assertEqual(len(store.list_notes(paper.arxiv_id)), 1)

    def test_release_gate_never_submits(self):
        with tempfile.TemporaryDirectory() as temp:
            report = prepare_release(temp, author_name="Researcher", category="math.NT", license_id="arxiv")
            self.assertFalse(report["submission_performed"])
            self.assertTrue(report["approval_required"])
            self.assertFalse(report["ready_for_human_review"])


if __name__ == "__main__":
    unittest.main()
