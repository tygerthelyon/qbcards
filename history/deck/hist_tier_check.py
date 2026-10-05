# -*- coding: utf-8 -*-
"""hist_tier_check.py -- check History v2 tiers against qbreader. Report only; changes nothing.

    py -3.9 hist_tier_check.py --include qinhan          (any of prehistory,shang,zhou,qinhan; comma list)

For each entity it counts qbreader tossups and bonuses whose ANSWER line matches the underlined key word, suggests a tier, and lists
the cards whose tier is off by one or more. Fix the tier numbers in the cards_*.py file by hand, then run
hist_qb_apply.py. Thresholds (tossups + bonuses): 40+ tier 1, 15+ tier 2, 5+ tier 3, fewer tier 4.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

import hist_qb_apply as app


def count(name):
    url = "https://www.qbreader.org/api/query?" + urllib.parse.urlencode(
        {"queryString": name, "searchType": "answer", "questionType": "all", "maxReturnLength": 1})
    req = urllib.request.Request(url, headers={"User-Agent": "qbcards tier check"})
    r = json.loads(urllib.request.urlopen(req, timeout=60).read())
    return r["tossups"]["count"] + r["bonuses"]["count"]


def suggest(n):
    return 1 if n >= 40 else 2 if n >= 15 else 3 if n >= 5 else 4


def main():
    if "--include" not in sys.argv:
        sys.exit(__doc__)
    notes = app.load_notes()
    base = {id(n) for n in __import__("cards_china_myth_lit").NOTES}
    notes = [n for n in notes if id(n) not in base]
    seen, off = {}, []
    for n in notes:
        e = n["entity"]
        if e not in seen:
            m = re.search(r"<u>(.*?)</u>", n["fields"].get("Answer", ""))
            key = re.sub(r"<.*?>", "", m.group(1)) if m else e
            seen[e] = count(key if len(key) > 3 else e)   # 'Li', 'Yu', 'Xian' alone match too much
            time.sleep(1)
        s = suggest(seen[e])
        print("%4d  tier %d (suggest %d)  %s" % (seen[e], n["tier"], s, e))
        if abs(s - n["tier"]) >= 1 and n["model"] == "QB Clue" and n["pos"] != "lead":
            off.append((e, n["tier"], s, seen[e]))
    print("\nOff by a tier or more (clue cards that aren't lead-ins; lead-ins are meant to be harder than the entity):")
    for e, t, s, c in sorted(set(off)):
        print("  %-40s now %d, qbreader suggests %d (%d questions)" % (e, t, s, c))


if __name__ == "__main__":
    main()
