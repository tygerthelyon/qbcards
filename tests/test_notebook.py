import csv
import importlib.util
import sqlite3
import tempfile
import unittest
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
        with sqlite3.connect(str(self.path)) as con:
            for table in ("u", "q", "f", "sets", "meta"):
                con.execute('CREATE TABLE "{}" (id INTEGER)'.format(table))
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
        with patch("qbr.notebook.qbr.profile", return_value=result) as profile:
            self.assertEqual(self.app.run_profile(), result)
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


if __name__ == "__main__":
    unittest.main()
