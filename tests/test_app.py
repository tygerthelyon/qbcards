"""Offline coverage for the standalone app's API and local request boundary."""
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

from qbr.app import Application, AppServer


class AppQueryTests(unittest.TestCase):
    def test_profile_preserves_filters_and_options(self):
        data = {"query": "Damien Hirst", "category": "fa", "difficulty": "8", "year": "2018-",
                "ranking": "n", "limit": 30, "exact": True, "anki": False, "exclude": "example, another"}
        with patch("qbr.app.qbr.profile", return_value={"found": True}) as profile:
            self.assertEqual(Application().query("profile", data), {"found": True})
        self.assertEqual(profile.call_args.args, ("Damien Hirst",))
        self.assertEqual(profile.call_args.kwargs, {"cat": "fa", "diff": "8", "year": "2018-",
                                                  "sort": "n", "top": 30, "exact": True, "anki": False,
                                                  "exclude": ["example", "another"]})

    def test_invalid_filters_never_reach_the_engine(self):
        for changes in ({"difficulty": "banana"}, {"difficulty": "9-6"}, {"year": ","},
                        {"limit": 101}, {"anki": "true"}, {"query": []}, {"ranking": "invalid"}):
            with self.subTest(changes=changes), patch("qbr.app.qbr.profile") as profile:
                with self.assertRaises(ValueError):
                    Application().query("profile", dict({"query": "Example"}, **changes))
                profile.assert_not_called()

    def test_search_is_not_an_app_action(self):
        # passage search lives in the CLI (python -m qbr search); the app only profiles answers
        with self.assertRaises(ValueError):
            Application().query("search", {"query": "butterflies"})


class AppHttpTests(unittest.TestCase):
    def setUp(self):
        self.server = AppServer(0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join(timeout=5)
        self.server.server_close()

    def request(self, path, data=None, token=True, headers=None):
        request_headers = {"X-StockFisher-Token": self.server.token} if token else {}
        if data is not None:
            request_headers["Content-Type"] = "application/json"
        request_headers.update(headers or {})
        payload = json.dumps(data).encode() if data is not None else None
        return urlopen(Request(self.server.origin + path, data=payload, headers=request_headers), timeout=5)

    def test_page_is_standalone_and_assets_are_restricted(self):
        with self.request("/", token=False) as response:
            html = response.read().decode()
            self.assertIn('id="search-form"', html)
            self.assertIn(self.server.token, html)
            self.assertNotIn("__SESSION_TOKEN__", html)
            self.assertIn("frame-ancestors 'none'", response.headers["Content-Security-Policy"])
        for asset in ("/app.js", "/app.css", "/favicon.svg"):
            with self.request(asset, token=False) as response:
                self.assertEqual(response.status, 200)
        with self.assertRaises(HTTPError) as error:
            self.request("/../store.py", token=False)
        error.exception.close()
        self.assertEqual(error.exception.code, 404)

    def test_api_rejects_missing_tokens_foreign_origins_and_hosts(self):
        for options in ({"token": False}, {"headers": {"Origin": "https://example.com"}},
                        {"headers": {"Host": "example.com"}}):
            with self.subTest(options=options), self.assertRaises(HTTPError) as error:
                self.request("/api/status", **options)
            error.exception.close()
            self.assertEqual(error.exception.code, 403)

    def test_json_errors_are_actionable(self):
        with self.assertRaises(HTTPError) as error:
            self.request("/api/profile", {"query": "Hirst", "difficulty": "banana"})
        with error.exception:
            self.assertEqual(error.exception.code, 400)
            self.assertIn("Difficulty: use", json.load(error.exception)["error"])
        with self.assertRaises(HTTPError) as error:
            self.request("/api/profile", ["not an object"])
        error.exception.close()
        self.assertEqual(error.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
