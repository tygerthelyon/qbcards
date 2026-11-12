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
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = BASE + path + ("?" + q if q else "")
    for k in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
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


def rows(**params):
    """Every row of a query of any size: split by difficulty, then by category, wherever the ceiling would bite."""
    try:
        yield from pages(**params)
        return
    except OverflowError:
        pass
    seen = set()
    for d in ([params["difficulties"]] if "difficulties" in params else range(0, 11)):
        try:
            part = list(pages(**dict(params, difficulties=d)))
        except OverflowError:
            part = []
            for c in CATEGORIES:
                part += list(pages(**dict(params, difficulties=d, categories=c)))
        for q in part:
            if q["_id"] not in seen:
                seen.add(q["_id"])
                yield q


CATEGORIES = ["Literature", "History", "Science", "Fine Arts", "Religion", "Mythology", "Philosophy", "Social Science",
              "Current Events", "Geography", "Other Academic", "Pop Culture"]
