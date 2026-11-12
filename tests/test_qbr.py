"""Offline checks for answer parsing and the SQLite mirror."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from unittest import mock

from qbr import store
from qbr.anki import _note_fold
from qbr.selftest import ANSWER_LINE_REGRESSIONS, PARSER_REGRESSIONS, scratch_store_regressions
from qbr.text import fold, parse_answer


class AnswerParserTests(unittest.TestCase):
    def test_accepted_and_rejected_alternates(self):
        for line, required, forbidden in PARSER_REGRESSIONS:
            with self.subTest(answerline=line):
                accepts = set(parse_answer(line)["accepts"])
                self.assertTrue(set(required) <= accepts, (required, accepts))
                self.assertFalse(set(forbidden) & accepts, (forbidden, accepts))

    def test_formatted_answerlines(self):
        for label, plain, formatted, required, forbidden in ANSWER_LINE_REGRESSIONS:
            with self.subTest(case=label):
                accepts = set(parse_answer(plain, formatted)["accepts"])
                self.assertTrue(set(required) <= accepts, (required, accepts))
                self.assertFalse(set(forbidden) & accepts, (forbidden, accepts))

    def test_normalization_and_note_acronyms(self):
        self.assertEqual(fold("Antoni Gaudí i Cornet"), "antoni gaudi i cornet")
        self.assertEqual(fold("c·A·M·P"), "c a m p")
        self.assertIn("camp", _note_fold("c·A·M·P").split())


class MirrorTests(unittest.TestCase):
    def test_replacing_and_removing_a_set_updates_the_search_index(self):
        ok, detail = scratch_store_regressions()
        self.assertTrue(ok, detail)

    def test_missing_mirror_gives_setup_instruction(self):
        with tempfile.TemporaryDirectory(prefix="qbr-test-") as tmp:
            env = os.environ.copy()
            env["QBR_DB"] = str(Path(tmp) / "missing.sqlite")
            result = subprocess.run(
                [sys.executable, "-m", "qbr", "status"],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("python -m qbr sync", result.stderr)
            self.assertFalse(Path(env["QBR_DB"]).exists())

    def test_failed_sync_preserves_last_success_and_can_be_retried(self):
        with tempfile.TemporaryDirectory(prefix="qbr-test-") as tmp:
            path = str(Path(tmp) / "mirror.sqlite")
            with mock.patch.object(store, "PATH", path), \
                 mock.patch.object(store.api, "set_list", return_value=["Example Set"]), \
                 mock.patch.object(store.api, "counts", return_value=(0, 0)), \
                 mock.patch.object(store, "_fetch_set", side_effect=OSError("unavailable")):
                con = store.connect(write=True)
                con.execute("INSERT INTO meta VALUES ('synced', '12345')")
                con.commit()
                con.close()
                with self.assertRaisesRegex(RuntimeError, "sync incomplete"):
                    store.sync(full=True, log=lambda message: None)
                con = store.connect()
                try:
                    self.assertEqual(store.meta("synced", con=con), 12345)
                finally:
                    con.close()
                with mock.patch.object(store, "_fetch_set", return_value=("Example Set", [])):
                    self.assertEqual(store.sync(full=True, log=lambda message: None), 1)
                con = store.connect()
                try:
                    self.assertGreater(store.meta("synced", con=con), 12345)
                finally:
                    con.close()

    def test_status_after_first_sync_fails(self):
        with tempfile.TemporaryDirectory(prefix="qbr-test-") as tmp:
            path = str(Path(tmp) / "mirror.sqlite")
            with mock.patch.object(store, "PATH", path), \
                 mock.patch.object(store.api, "set_list", return_value=["Example Set"]), \
                 mock.patch.object(store.api, "counts", return_value=(0, 0)), \
                 mock.patch.object(store, "_fetch_set", side_effect=OSError("unavailable")):
                with self.assertRaisesRegex(RuntimeError, "sync incomplete"):
                    store.sync(log=lambda message: None)
            env = os.environ.copy()
            env["QBR_DB"] = path
            result = subprocess.run([sys.executable, "-m", "qbr", "status"],
                                    capture_output=True, text=True, env=env, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("never completed", result.stdout)

    def test_relative_database_path_with_uri_characters(self):
        with tempfile.TemporaryDirectory(prefix="qbr-test-") as tmp:
            old_cwd = os.getcwd()
            try:
                os.chdir(tmp)
                with mock.patch.object(store, "PATH", "mirror #1.sqlite"):
                    con = store.connect(write=True)
                    con.execute("INSERT INTO meta (k, v) VALUES (?, ?)", ("example", "1"))
                    con.commit()
                    con.close()
                    con = store.connect()
                    try:
                        self.assertEqual(con.execute("SELECT v FROM meta WHERE k='example'").fetchone()[0], "1")
                    finally:
                        con.close()
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
