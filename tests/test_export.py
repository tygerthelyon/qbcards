"""Checks for the collection-export file format, without connecting to Anki."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "export_for_cloud.py"
SPEC = importlib.util.spec_from_file_location("collection_export", SCRIPT)
export = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(export)


class ExportTests(unittest.TestCase):
    def test_small_export_round_trips(self):
        with tempfile.TemporaryDirectory(prefix="anki-export-test-") as tmp:
            path = Path(tmp) / "notes.json"
            payload = {"model": "Art", "notes": [{"id": 1, "title": "École"}]}
            self.assertEqual(export.write(path, payload), [path])
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), payload)

    def test_large_note_list_is_split_without_losing_records(self):
        with tempfile.TemporaryDirectory(prefix="anki-export-test-") as tmp:
            path = Path(tmp) / "notes.json"
            notes = [{"id": i, "text": "x" * 2400} for i in range(3)]
            with mock.patch.object(export, "LIMIT", 4300):
                paths = export.write(path, {"model": "Art", "notes": notes})
            parts = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
            self.assertGreater(len(parts), 1)
            self.assertEqual([part["part"] for part in parts], list(range(1, len(parts) + 1)))
            self.assertTrue(all(part["parts"] == len(parts) for part in parts))
            self.assertEqual([note for part in parts for note in part["notes"]], notes)


if __name__ == "__main__":
    unittest.main()
