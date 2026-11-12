# -*- coding: utf-8 -*-
"""film_lowres_1001.py -- Film pictures under 500px replaced with larger copies from TMDB.

Carter, 2026-10-01: "also, fix the low quality images". Eleven pictures on active (tier 1) Film cards were
under 500px on the long side -- Wikipedia thumbnails at 220-330px, mostly posters. For each, TMDB is searched
(the film by title and year, its director confirmed from the credits; the person by name), and the
candidates go on a contact sheet: stills are textless backdrops at 1280px, posters at 780px, portraits at
500px+. Picks are looked at before they go in, as with every picture in these decks.

    py -3.9 film_lowres_1001.py find               (candidates and a contact sheet; no Anki needed)
    py -3.9 film_lowres_1001.py [--apply]          (with data/film_lowres_picks_1001.json)
"""
import json, os, re, sys, time, urllib.request
import concept_add as C

WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_lowres_1001")
PICKS = "data/film_lowres_picks_1001.json"
SP = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\4c6fe2ff-c3a6-47fb-8b54-226f916ad6af\scratchpad"

# (title as in the Title field, field, year, director) -- from the 2026-10-01 check of tier-1 pictures
ITEMS = [("A Trip to the Moon", "Still", "1902", "Georges Méliès"), ("It's a Wonderful Life", "Still", "1946", "Frank Capra"),
         ("The Seventh Seal", "Still", "1957", "Ingmar Bergman"), ("The Godfather", "Poster", "1972", "Francis Ford Coppola"),
         ("Stalker", "Poster", "1979", "Andrei Tarkovsky"), ("Un Chien Andalou", "Poster", "1929", "Luis Buñuel"),
         ("Mulholland Drive", "Still", "2001", "David Lynch"), ("8½", "Poster", "1963", "Federico Fellini"),
         ("Andrei Rublev", "Poster", "1966", "Andrei Tarkovsky"), ("Mad Max: Fury Road", "Poster", "2015", "George Miller"),
         ("Michael Powell", "Picture", "", "")]


def get(url, path):
    if not os.path.exists(path):
        open(path, "wb").write(urllib.request.urlopen(url, timeout=60).read())
        time.sleep(0.2)
    return path


def find():
    import film_stills as S
    os.makedirs(WORK, exist_ok=True)
    plan, tiles = {}, []
    for i, (title, field, year, director) in enumerate(ITEMS):
        out = []
        if field == "Picture":
            r = S.tmdb("/search/person", query=title)["results"]
            profs = sorted(S.tmdb("/person/%d/images" % r[0]["id"])["profiles"], key=lambda p: -(p.get("vote_count") or 0))
            for k, p in enumerate(profs[:4]):
                out.append(get("https://image.tmdb.org/t/p/original" + p["file_path"], os.path.join(WORK, "%d_%d.jpg" % (i, k))))
        else:
            dirs = [S.surname(director)]
            hit = None
            for yr in (year, None):
                for r in S.tmdb("/search/movie", query=title, **({"year": yr} if yr else {}))["results"][:5]:
                    crew = S.tmdb("/movie/%d/credits" % r["id"])["crew"]
                    if any(d in " ".join(C.fold(c["name"]) for c in crew if c.get("job") == "Director") for d in dirs):
                        hit = r
                        break
                if hit:
                    break
            imgs = S.tmdb("/movie/%d/images" % hit["id"], include_image_language="en,null")
            if field == "Still":
                cand = [b for b in imgs["backdrops"] if not b.get("iso_639_1")]
                size = "w1280"
            else:
                cand = sorted(imgs["posters"], key=lambda p: (p.get("iso_639_1") not in ("en", None), -(p.get("vote_count") or 0)))
                size = "w780"
            cand.sort(key=lambda b: -(b.get("vote_count") or 0) * (b.get("vote_average") or 0)) if field == "Still" else None
            for k, b in enumerate(cand[:4]):
                out.append(get("https://image.tmdb.org/t/p/%s%s" % (size, b["file_path"]), os.path.join(WORK, "%d_%d.jpg" % (i, k))))
            plan[str(i)] = {"tmdb": hit["id"]}
        plan.setdefault(str(i), {})["cands"] = out
        tiles += [("%d.%d %s %s" % (i, k, title[:22], field), p) for k, p in enumerate(out)]
        print(i, title, field, len(out), flush=True)
    json.dump(plan, open(os.path.join(WORK, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    sys.path.insert(0, SP)
    import wm
    for s in range(0, len(tiles), 24):
        wm.sheet(tiles[s:s + 24], os.path.join(WORK, "sheet_%02d.jpg" % (s // 24)), cols=6, W=240)


def apply():
    plan = json.load(open(os.path.join(WORK, "plan.json"), encoding="utf-8"))
    picks = json.load(open(PICKS, encoding="utf-8"))
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Film"'))
    by = {C.plain(n["fields"]["Title"]["value"]): n for n in ns}
    ch = {}
    for i, (title, field, year, director) in enumerate(ITEMS):
        k = picks.get(str(i))
        if k is None:
            continue
        n = by[title]
        src = plan[str(i)]["cands"][k]
        fn = "film-%s-%s-1001.jpg" % (re.sub(r"[^a-z0-9]+", "-", C.fold(title).lower()).strip("-"), field.lower())
        C.anki("storeMediaFile", filename=fn, path=src)
        ch.setdefault(n["noteId"], {})[field] = '<img src="%s">' % fn
        print(title, field, "->", fn)
    json.dump({str(nid): {"fields": {f: next(x for x in ns if x["noteId"] == nid)["fields"][f]["value"] for f in d}} for nid, d in ch.items()},
              open("backups/film_lowres_1001_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
    for nid, d in ch.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": d})
    print("applied", len(ch), "notes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:2] == ["find"]:
        find()
    elif "--apply" in sys.argv:
        apply()
