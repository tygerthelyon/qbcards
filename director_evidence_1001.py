# -*- coding: utf-8 -*-
"""director_evidence_1001.py -- academic quizbowl evidence for the TSPDT Top 250 Directors (2026 edition).

Carter, 2026-10-01: "add the director cards ... do a search of a couple of well established lists and critic
reviews; i want to cover the real world canon of famous directors that could come up in quiz". The canon is
They Shoot Pictures, Don't They?'s Top 250 Directors (2026), an aggregate of critics' and filmmakers' lists,
checked against Sight & Sound's directors ranked by votes. Each is scored on qbreader, Fine Arts only:
strict answer lines (the name is the main answer; film_actors_strict_1001.py) and all mentions.
Pairs are searched by the name questions use ("Coen brothers").

    py -3.9 director_evidence_1001.py LISTFILE      (writes data/director_evidence_1001.json, resumable)
"""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
import retier2 as R
import film_actors_strict_1001 as S

OUT = "data/director_evidence_1001.json"
SEARCH = {"Coen brothers": "Coen", "Straub-Huillet": "Straub", "Wachowskis": "Wachowski", "Dardenne brothers": "Dardenne"}


def score(name):
    q = SEARCH.get(name, name)
    return {"name": name, "strict": S.strict(q), "all": len(R.ids_for(q, set(), "all", True))}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    names = [x.strip() for x in open(sys.argv[1], encoding="utf-8").read().split(";") if x.strip()]
    done = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    todo = [n for n in names if n not in done]
    print(len(todo), "to score", flush=True)
    with ThreadPoolExecutor(3) as ex:
        for r in ex.map(score, todo):
            done[r["name"]] = r
            json.dump(done, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
            print("%-28s strict %3d all %4d" % (r["name"], r["strict"], r["all"]), flush=True)
