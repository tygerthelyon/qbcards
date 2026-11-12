# -*- coding: utf-8 -*-
"""qbr.api -- the live qbreader API. The mirror answers nearly everything; this is what fills it, and what reaches a
set added an hour ago.

    api.get("num-packets", setName="2026 ACF Nationals")
    for row in api.rows(queryString="arkhitekton", questionType="tossup"): ...

qbreader allows 20 requests a second (qbreader.org/tools/api-docs). Everything here uses one connection at a time
unless the caller asks for more (sync uses four).
"""
import gzip
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.qbreader.org/api/"
UA = {"User-Agent": "qbr local mirror (personal study tool)", "Accept-Encoding": "gzip"}
PAGE = 5000        # the most rows one request returns
CEILING = 10000    # past this row a query repeats its last page (measured 2026-11-11), so big pulls are split


def get(path, tries=5, timeout=180, **params):
    """One GET, as parsed JSON. Retries rate limits, timeouts and server errors with a growing wait."""
    query = {key: ",".join(map(str, value)) if isinstance(value, (list, tuple, set)) else value
             for key, value in params.items() if value is not None}
    q = urllib.parse.urlencode(query)
    url = BASE + path + ("?" + q if q else "")
    for k in range(tries):
        try:
            request = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
                encoding = response.headers.get("Content-Encoding")
            if encoding == "gzip":
                raw = gzip.decompress(raw)
            return json.loads(raw.decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or k == tries - 1:
                raise
        except (urllib.error.URLError, socket.timeout, ConnectionError, ValueError):
            if k == tries - 1:
                raise
        time.sleep(1.5 * 2 ** k)


def set_list():
    return get("set-list")["setList"]


def counts(**params):
    """(tossups, bonuses) a query matches, without fetching them"""
    j = get("query", **dict({"queryString": "", "questionType": "all"}, **params, maxReturnLength=1))
    return j["tossups"]["count"], j["bonuses"]["count"]


def pages(**params):
    """Every row of one query, both kinds, each tagged _kind "T" or "B". Raises past the paging ceiling rather than
    return repeats -- rows() below splits such a query instead."""
    params = dict({"queryString": "", "questionType": "all"}, **params)
    got = {"tossups": 0, "bonuses": 0}
    page = 1
    while True:
        j = get("query", **dict(params, maxReturnLength=PAGE, tossupPagination=page, bonusPagination=page))
        more = False
        for key in got:
            if ((j.get(key) or {}).get("count") or 0) > CEILING:
                raise OverflowError("%d %s match; past %d qbreader repeats pages" % (j[key]["count"], key, CEILING))
        for key, kind in (("tossups", "T"), ("bonuses", "B")):
            block = j.get(key) or {}
            arr, total = block.get("questionArray") or [], block.get("count") or 0
            if got[key] < total:
                for q in arr:
                    q["_kind"] = kind
                    yield q
                got[key] += len(arr)
                more = more or (bool(arr) and got[key] < total)
        if not more:
            return
        page += 1


def _values(value, default):
    """Expand a comma-separated or sequence-valued API filter."""
    if value is None or value == "":
        return list(default)
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()] or list(default)
    if isinstance(value, (list, tuple, set)):
        return list(value) or list(default)
    return [value]


def rows(**params):
    """Fetch all rows, splitting oversized queries by difficulty and category.

    Raises OverflowError if a single partition still exceeds the API limit.
    """
    try:
        yield from pages(**params)
        return
    except OverflowError:
        pass
    seen = set()
    difficulties = _values(params.get("difficulties"), range(0, 11))
    categories = _values(params.get("categories"), CATEGORIES)
    for difficulty in difficulties:
        try:
            part = list(pages(**dict(params, difficulties=difficulty)))
        except OverflowError:
            part = []
            for category in categories:
                part.extend(pages(**dict(params, difficulties=difficulty, categories=category)))
        for question in part:
            if question["_id"] not in seen:
                seen.add(question["_id"])
                yield question


CATEGORIES = ["Literature", "History", "Science", "Fine Arts", "Religion", "Mythology", "Philosophy", "Social Science",
              "Current Events", "Geography", "Other Academic", "Pop Culture"]
