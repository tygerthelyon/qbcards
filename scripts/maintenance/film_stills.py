# -*- coding: utf-8 -*-
"""film_stills.py -- stills from TMDB for the Film notes that have none.

122 Film notes had no Still (17 of them tier1), waiting on a TMDB key; Carter added
.tmdb_key on 2026-09-25. For each: search TMDB by title and year (original title as a
fallback), confirm the director from the film's credits, and take the most-voted
backdrop that carries no text (TMDB tags lettered images with a language), at 1280px.
Every still is looked at on a contact sheet before it goes in.

    py -3.9 film_stills.py find
    py -3.9 film_stills.py sheet
    py -3.9 film_stills.py apply 0 1 2 ...     (numbers from the sheet)

The key is read from .tmdb_key and never printed.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import concept_add as C

KEY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".tmdb_key"), encoding="utf-8-sig").read().strip()
WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_stills")
PLAN = "data/film_stills_plan.json"


def tmdb(path, **p):
    h = {"accept": "application/json"}
    if len(KEY) == 32:
        p["api_key"] = KEY
    else:
        h["Authorization"] = "Bearer " + KEY
    url = "https://api.themoviedb.org/3" + path + "?" + urllib.parse.urlencode(p)
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30).read())


def surname(s):
    t = [x for x in re.split(r"[^a-z]+", C.fold(C.plain(s))) if len(x) > 2]
    return t[-1] if t else ""


def find():
    os.makedirs(WORK, exist_ok=True)
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query="note:Film Kind: Still:"))
    plan = []
    for n in ns:
        f = n["fields"]
        title, orig = C.plain(f["Title"]["value"]), C.plain(f["Original title"]["value"])
        year = re.findall(r"\d{4}", C.plain(f["Year"]["value"]))
        directors = [surname(d) for d in re.split(r",| and |;|&", C.plain(f["Director"]["value"])) if surname(d)]
        tier = ([t.split("::")[-1] for t in n["tags"] if "tier::" in t] or ["none"])[0]
        rec = {"nid": n["noteId"], "title": title, "year": year[0] if year else "", "tier": tier, "status": "no match"}
        try:
            hit = None
            for q in [title, orig]:
                if not q or hit:
                    continue
                for yr in ([year[0]] if year else []) + [None]:
                    res = tmdb("/search/movie", query=q, **({"year": yr} if yr else {}))["results"][:5]
                    for r in res:
                        crew = tmdb("/movie/%d/credits" % r["id"])["crew"]
                        dirs = " ".join(C.fold(c["name"]) for c in crew if c.get("job") == "Director")
                        if not directors or any(d in dirs for d in directors):
                            hit = r
                            break
                    if hit:
                        break
            if hit:
                imgs = [b for b in tmdb("/movie/%d/images" % hit["id"])["backdrops"] if not b.get("iso_639_1")]
                imgs.sort(key=lambda b: (-(b.get("vote_count") or 0) * (b.get("vote_average") or 0), -b["width"]))
                if imgs:
                    b = imgs[0]
                    local = os.path.join(WORK, "%d.jpg" % n["noteId"])
                    if not os.path.exists(local):
                        data = urllib.request.urlopen("https://image.tmdb.org/t/p/w1280" + b["file_path"], timeout=60).read()
                        open(local, "wb").write(data)
                    rec.update(status="candidate", tmdb=hit["id"], tmdb_title=hit["title"], release=hit.get("release_date", ""),
                               local=local, px=[b["width"], b["height"]],
                               alts=[x["file_path"] for x in imgs[1:4]])
                else:
                    rec.update(status="no text-free still", tmdb=hit["id"])
        except Exception as e:
            rec["status"] = "error: %s" % str(e)[:60]
        plan.append(rec)
        print("%-10s %-40s %s" % (rec["status"][:10], title[:40], rec.get("tmdb_title", "")))
        time.sleep(0.25)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=0)


def sheet():
    from PIL import Image, ImageDraw
    plan = json.load(open(PLAN, encoding="utf-8"))
    cands = [p for p in plan if p["status"] == "candidate"]
    for i, p in enumerate(cands):
        p["n"] = i
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    cols, per = 4, 24
    for s in range(0, len(cands), per):
        tiles = []
        for p in cands[s:s + per]:
            im = Image.open(p["local"]).convert("RGB")
            im = im.resize((360, int(im.height * 360 / im.width)))
            t = Image.new("RGB", (360, im.height + 30), "white")
            t.paste(im, (0, 30))
            ImageDraw.Draw(t).text((3, 2), "#%d %s (%s)\nTMDB: %s %s" % (p["n"], p["title"][:34], p["year"],
                                                                        p["tmdb_title"][:30], p["release"][:4]), fill="black")
            tiles.append(t)
        H = max(t.height for t in tiles)
        rows = (len(tiles) + cols - 1) // cols
        sh = Image.new("RGB", (cols * 368, rows * (H + 8)), "white")
        for k, t in enumerate(tiles):
            sh.paste(t, ((k % cols) * 368, (k // cols) * (H + 8)))
        out = "renders/_stills_%02d.png" % (s // per)
        sh.save(out)
        print(out)


def apply(nums):
    plan = json.load(open(PLAN, encoding="utf-8"))
    pick = [p for p in plan if p.get("n") in nums and p["status"] == "candidate"]
    done = []
    for p in pick:
        n = C.anki("notesInfo", notes=[p["nid"]])[0]
        if n["fields"]["Still"]["value"].strip():
            continue
        fn = "film-tmdb-%d.jpg" % p["tmdb"]
        C.anki("storeMediaFile", filename=fn, path=p["local"])
        C.anki("updateNoteFields", note={"id": p["nid"], "fields": {"Still": '<img src="%s">' % fn}})
        p["status"] = "applied"
        done.append(p["nid"])
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    # tier gate: only tier1 cards in the queue
    if done:
        cards = C.anki("findCards", query="(" + " OR ".join("nid:%d" % i for i in done) + ") -tag:Film::tier::tier1-core -is:suspended")
        if cards:
            C.anki("suspend", cards=cards)
    print("applied %d" % len(done))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    a = sys.argv[1:]
    {"find": find, "sheet": sheet}.get(a[0], lambda: apply({int(x) for x in a[1:]}))()
