"""Offline checks for QBReader API query handling."""
import json
import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

from qbr import api


class ApiTests(unittest.TestCase):
    def test_get_serializes_lists_and_closes_response(self):
        response = MagicMock()
        response.read.return_value = json.dumps({"ok": True}).encode("utf-8")
        response.headers.get.return_value = None
        response.__enter__.return_value = response
        with patch("qbr.api.urllib.request.urlopen", return_value=response) as open_url:
            self.assertEqual(api.get("query", categories=["Science", "Fine Arts"],
                                     difficulties=[6, 7]), {"ok": True})
        request = open_url.call_args.args[0]
        query = parse_qs(urlparse(request.full_url).query)
        self.assertEqual(query["categories"], ["Science,Fine Arts"])
        self.assertEqual(query["difficulties"], ["6,7"])
        response.__exit__.assert_called_once()

    def test_large_query_keeps_requested_filters(self):
        def pages(**params):
            difficulty = str(params.get("difficulties", ""))
            category = params.get("categories", "")
            if "," in difficulty or "," in category:
                raise OverflowError("partition too large")
            return iter([{"_id": "%s:%s" % (difficulty, category)}])

        with patch("qbr.api.pages", side_effect=pages) as search:
            results = list(api.rows(difficulties="6,7", categories="Science,History"))
        self.assertEqual({row["_id"] for row in results},
                         {"6:Science", "6:History", "7:Science", "7:History"})
        self.assertFalse(any(call.kwargs.get("categories") == "Literature"
                             for call in search.call_args_list))

    def test_single_large_category_does_not_expand_to_other_categories(self):
        def pages(**params):
            if params.get("categories") == "Science":
                raise OverflowError("partition too large")
            return iter([{"_id": "unrelated"}])

        with patch("qbr.api.pages", side_effect=pages) as search:
            with self.assertRaises(OverflowError):
                list(api.rows(difficulties=7, categories="Science"))
        self.assertTrue(all(call.kwargs.get("categories") == "Science"
                            for call in search.call_args_list))


if __name__ == "__main__":
    unittest.main()
