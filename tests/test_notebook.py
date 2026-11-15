import csv
import importlib.util
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

HAS_WIDGETS = importlib.util.find_spec("ipywidgets") is not None
if HAS_WIDGETS:
    from qbr import anki, store
    from qbr.notebook import StockFisherNotebook


@unittest.skipUnless(HAS_WIDGETS, "install notebook requirements for widget tests")
class NotebookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "mirror.sqlite"
        with closing(sqlite3.connect(str(self.path))) as con:
            with con:
                for table in ("u", "q", "f", "sets", "meta"):
                    schema = "k TEXT PRIMARY KEY, v TEXT" if table == "meta" else "id INTEGER"
                    con.execute('CREATE TABLE "{}" ({})'.format(table, schema))
        self.old_path, self.old_con, self.old_cache = store.PATH, store._CON, anki.CACHE
        store.PATH, store._CON = str(self.path), None
        self.app = StockFisherNotebook()

    def tearDown(self):
        if store._CON is not None:
            store._CON.close()
        store.PATH, store._CON, anki.CACHE = self.old_path, self.old_con, self.old_cache
        self.temp.cleanup()

    def test_connection_is_read_only_and_rejects_missing_path(self):
        self.assertTrue(self.app.connected)
        missing = self.path.parent / "missing.sqlite"
        self.app.db_path.value = str(missing)
        self.assertFalse(self.app.connect())
        self.assertFalse(missing.exists())
        self.assertIn("Database not connected", self.app.db_status.value)

    def test_profile_filters_and_export(self):
        result = {"found": True, "name": "Example", "questions": 1, "tossups": 1,
                  "bonuses": 0, "sets": 1, "lines": [("Example", 1)], "foils": [],
                  "things": [{"thing": "clue", "n": 1, "tied": 1.0, "where": "lead-in"}]}
        self.app.difficulty.value = "6-9"
        self.app.tabs.selected_index = 3
        with patch("qbr.notebook.qbr.profile", return_value=result) as profile:
            self.assertEqual(self.app.run_profile(), result)
        self.assertEqual(self.app.tabs.selected_index, 0)
        self.assertEqual(profile.call_args.kwargs["diff"], "6-9")
        self.app._select_all()
        export = self.path.parent / "clues.csv"
        self.app.export_path.value = str(export)
        self.assertEqual(self.app.export(), export)
        with export.open(encoding="utf-8-sig", newline="") as f:
            self.assertEqual(next(csv.DictReader(f))["clue"], "clue")
        self.assertIsNone(self.app.export())
        self.assertIn("already exists", self.app.export_status.value)
        self.app.connect()
        self.assertIsNone(self.app.result)
        self.assertEqual(len(self.app.selection.options), 0)

    def test_missing_mirror_disables_queries(self):
        self.app.db_path.value = str(self.path.parent / "missing.sqlite")
        self.app.connect()
        with patch("qbr.notebook.qbr.profile") as profile:
            self.assertIsNone(self.app.run_profile())
            profile.assert_not_called()

    def test_changed_answer_cannot_export_previous_results(self):
        result = {"found": True, "name": "Original", "questions": 1, "tossups": 1,
                  "bonuses": 0, "sets": 1, "things": [{"thing": "clue"}]}
        with patch("qbr.notebook.qbr.profile", return_value=result):
            self.app.run_profile()
        self.app._select_all()
        self.app.answer.value = "Changed"
        target = self.path.parent / "stale.csv"
        self.app.export_path.value = str(target)
        self.assertTrue(self.app.export_button.disabled)
        self.assertIn("Original", self.app.context_status.value)
        self.assertIsNone(self.app.export())
        self.assertFalse(target.exists())

    def test_bad_ranges_report_actionable_errors_without_querying(self):
        for field, values, label in ((self.app.difficulty, ["banana", "9-6", "11", ",", "999999999-"], "Difficulty"),
                                     (self.app.year, ["recent", "2025-2019", ","], "Years")):
            for value in values:
                self.app.difficulty.value = ""
                self.app.year.value = ""
                field.value = value
                with patch("qbr.notebook.qbr.profile") as query:
                    self.assertIsNone(self.app.run_profile())
                    query.assert_not_called()
                self.assertIn(label + ": use", self.app.profile_status.value)

    def test_source_question_escapes_corpus_text_and_includes_bonus_parts(self):
        from qbr.notebook import _question_details
        result = {"question": {"set_name": "Sample <set>", "kind": "B", "packet": 2, "number": 4, "id": "source"},
                  "units": [{"part": 1, "lead": "Lead", "text": "<script>alert(1)</script>", "answer": "A"},
                            {"part": 2, "text": "Second part", "answer": "B"}]}
        with patch("qbr.notebook.qbr.show", return_value=result):
            rendered = _question_details(1)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertIn("Second part", rendered)
        self.assertIn("packet 2", rendered)


if __name__ == "__main__":
    unittest.main()
