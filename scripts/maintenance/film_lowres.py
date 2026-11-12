# -*- coding: utf-8 -*-
"""film_lowres.py -- larger copies of the small pictures on active Film cards.

Audit 2026-09-26: 67 active Film pictures under 400px on the long side, most of them
220px Wikipedia poster thumbnails. For each film the TMDB match is confirmed by
director (film_stills.py's lookup), then:

  Poster   TMDB's most-voted poster in the film's own or English language, at 780px.
  Still N  replaced only when TMDB holds the SAME frame -- the old still is compared
           with every TMDB backdrop by perceptual hash -- so the caption stays true.
           A still with no same-frame match is left and reported.

    py -3.9 film_lowres.py find      -> data/film_lowres_plan.json + contact sheet
    py -3.9 film_lowres.py apply [--apply]
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

from PIL import Image, ImageDraw

import concept_add as C
import film_stills as F

MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_lowres")
PLAN = "data/film_lowres_plan.json"
SHEET = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/1d6bde35-08b4-4391-958b-52d033191c05/scratchpad/film_lowres_%d.jpg"


def dhash(im, n=8):
    g = im.convert("L").resize((n + 1, n))
    px = list(g.getdata())
    return sum(1 << i for i in range(n * n) if px[(i // n) * (n + 1) + i % n] > px[(i // n) * (n + 1) + i % n + 1])


def ham(a, b):
    return bin(a ^ b).count("1")


def fetch(url):
    return Image.open(io.BytesIO(urllib.request.urlopen(url, timeout=60).read())).convert("RGB")


def match_movie(f):
    title, orig = C.plain(f["Title"]["value"]), C.plain(f["Original title"]["value"])
    year = re.findall(r"\d{4}", C.plain(f["Year"]["value"]))
    directors = [F.surname(d) for d in re.split(r",| and |;|&", C.plain(f["Director"]["value"])) if F.surname(d)]
    for q in [title, orig]:
        if not q:
            continue
        for yr in ([year[0]] if year else []) + [None]:
            for r in F.tmdb("/search/movie", query=q, **({"year": yr} if yr else {}))["results"][:5]:
                crew = F.tmdb("/movie/%d/credits" % r["id"])["crew"]
                dirs = " ".join(C.fold(c["name"]) for c in crew if c.get("job") == "Director")
                if not directors or any(d in dirs for d in directors):
                    return r
    return None


def find():
    os.makedirs(WORK, exist_ok=True)
    low = json.load(open("data/lowres_active.json", encoding="utf-8"))["Film"]
    by = {}
    for nid, title, fld, src, size in low:
        by.setdefault(nid, []).append((fld, src))
    plan, tiles = [], []
    for nid, items in by.items():
        n = C.anki("notesInfo", notes=[nid])[0]
        f = n["fields"]
        try:
            mv = match_movie(f)
        except Exception as e:
            print("error", C.plain(f["Title"]["value"]), e)
            continue
        if not mv:
            print("no match", C.plain(f["Title"]["value"]))
            continue
        imgs = F.tmdb("/movie/%d/images" % mv["id"], include_image_language="en,null,%s,fr,it,de,ja,sv,es" % (mv.get("original_language") or "en"))
        for fld, src in items:
            old = Image.open(os.path.join(MED, src)).convert("RGB")
            if fld == "Poster":
                # the same design at a larger size, not TMDB's favourite (often a modern redesign,
                # which would make "Release poster" captions false)
                h0, best = dhash(old), None
                for b in imgs.get("posters", [])[:60]:
                    try:
                        th = fetch("https://image.tmdb.org/t/p/w185" + b["file_path"])
                    except Exception:
                        continue
                    d = ham(h0, dhash(th))
                    if best is None or d < best[0]:
                        best = (d, b)
                if not best or best[0] > 10:
                    print("   no same-design poster:", C.plain(f["Title"]["value"]), best and best[0])
                    continue
                url, dist = "https://image.tmdb.org/t/p/w780" + best[1]["file_path"], best[0]
            else:
                h0, best = dhash(old), None
                for b in imgs.get("backdrops", [])[:40]:
                    try:
                        th = fetch("https://image.tmdb.org/t/p/w300" + b["file_path"])
                    except Exception:
                        continue
                    d = ham(h0, dhash(th))
                    if best is None or d < best[0]:
                        best = (d, b)
                    time.sleep(0.05)
                if not best or best[0] > 10:
                    print("   no same-frame still:", C.plain(f["Title"]["value"]), fld, best and best[0])
                    continue
                url, dist = "https://image.tmdb.org/t/p/w1280" + best[1]["file_path"], best[0]
            new = fetch(url)
            local = os.path.join(WORK, "%d-%s.jpg" % (nid, re.sub(r"\W+", "", fld).lower()))
            new.save(local, quality=90)
            k = len(plan)
            plan.append({"k": k, "nid": nid, "title": C.plain(f["Title"]["value"]), "field": fld, "old": src,
                         "local": local, "size": new.size, "dist": dist})
            a, b = old.copy(), new.copy()
            a.thumbnail((160, 200)); b.thumbnail((160, 200))
            t = Image.new("RGB", (340, 222), "white")
            t.paste(a, (0, 20)); t.paste(b, (175, 20))
            ImageDraw.Draw(t).text((2, 2), "%d %s | %s" % (k, plan[-1]["title"][:24], fld), fill="black")
            tiles.append(t)
            print(k, plan[-1]["title"], fld, new.size, dist)
        time.sleep(0.2)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for s in range(0, len(tiles), 20):
        part = tiles[s:s + 20]
        sh = Image.new("RGB", (340 * 4, 222 * ((len(part) + 3) // 4)), "white")
        for i, t in enumerate(part):
            sh.paste(t, ((i % 4) * 340, (i // 4) * 222))
        sh.save(SHEET % (s // 20))
    print("planned", len(plan), "sheets", (len(tiles) + 19) // 20)


def apply(go, skip):
    plan = [p for p in json.load(open(PLAN, encoding="utf-8")) if p["k"] not in skip]
    bk = []
    for p in plan:
        name = "filmhi-%d-%s.jpg" % (p["nid"], re.sub(r"\W+", "", p["field"]).lower())
        cur = C.anki("notesInfo", notes=[p["nid"]])[0]["fields"][p["field"]]["value"]
        if p["old"] not in cur:
            continue
        bk.append({"nid": p["nid"], "field": p["field"], "old": cur})
        if go:
            C.anki("storeMediaFile", filename=name, path=p["local"])
            C.anki("updateNoteFields", note={"id": p["nid"], "fields": {p["field"]: cur.replace(p["old"], name)}})
    if go:
        json.dump(bk, open("backups/film_lowres_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"),
                  ensure_ascii=False)
    print(("replaced" if go else "would replace"), len(bk))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    a = sys.argv[1:]
    if a[0] == "find":
        find()
    else:
        sk = {int(x) for x in a[a.index("--skip") + 1].split(",")} if "--skip" in a else set()
        apply("--apply" in a, sk)
