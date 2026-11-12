# -*- coding: utf-8 -*-
"""film_hr_1002.py -- every Film picture under 1000px replaced by the same picture at TMDB's original resolution.

Carter, 2026-10-02: "Fix ALL of the low quality images ... stop adding low quality images." Film's pictures mostly
come from TMDB, but several passes fetched them below the bar: portraits at w500 (500x750, including the actor and
director cards added 2026-09-29 to 2026-10-01), posters at w780, stills from Wikipedia at 250-330px. For each Film
picture under 1000px on its long side: the film (title, year, director confirmed in the credits) or the person is
found on TMDB; its posters, backdrops, or profile photos are compared with the current picture (ORB/RANSAC on
w300 previews: the same image, so captions stay true); the match is fetched at "original" size and must be at least
1000px. A poster with no match takes TMDB's most-voted poster (caption "Poster", not "Release poster"); anything
else unmatched is left for img_upgrade_1002.py's Wikimedia pass.

    py -3.9 film_hr_1002.py find
    py -3.9 film_hr_1002.py sheet
    py -3.9 film_hr_1002.py apply [--apply]     (data/film_hr_reject_1002.json lists rejects)
"""
import json, os, re, sys, time, urllib.request
import concept_add as C
import film_stills as S
import img_upgrade_1002 as U

WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_hr_1002")
PLAN = os.path.join(WORK, "plan.jsonl")
REJECT = "data/film_hr_reject_1002.json"
IMG = "https://image.tmdb.org/t/p/"


def get(url, path):
    if not os.path.exists(path) or not os.path.getsize(path):
        open(path, "wb").write(urllib.request.urlopen(url, timeout=90).read())
        time.sleep(0.05)
    return path


def movie_id(f):
    dirs = [S.surname(d) for d in re.split(r",| and |;|&", f["Director"]) if S.surname(d)]
    year = (re.findall(r"\d{4}", f["Year"]) or [""])[0]
    for q in [f["Title"], f["Original title"]]:
        if not q:
            continue
        for yr in ([year] if year else []) + [None]:
            for r in S.tmdb("/search/movie", query=q, **({"year": yr} if yr else {}))["results"][:5]:
                names = " ".join(C.fold(c["name"]) for c in S.tmdb("/movie/%d/credits" % r["id"])["crew"] if c.get("job") == "Director")
                if not dirs or any(d in names for d in dirs):
                    return r["id"]
    return None


def person_id(name):
    r = S.tmdb("/search/person", query=name)["results"]
    return r[0]["id"] if r else None


def find():
    os.makedirs(WORK, exist_ok=True)
    audit = [a for a in json.load(open(U.AUDIT, encoding="utf-8")) if a["model"] == "Film" and 0 < max(a["w"], a["h"]) < U.MIN]
    done = {json.loads(l)["file"] for l in open(PLAN, encoding="utf-8")} if os.path.exists(PLAN) else set()
    notes = {n["noteId"]: {k: C.plain(v["value"]) for k, v in n["fields"].items()}
             for n in C.anki("notesInfo", notes=sorted({a["nid"] for a in audit}))}
    ids, fh, seen = {}, open(PLAN, "a", encoding="utf-8"), set()
    for a in sorted(audit, key=lambda a: not a["active"]):
        if a["file"] in done or a["file"] in seen:
            continue
        seen.add(a["file"])
        f = notes[a["nid"]]
        person = a["field"] == "Picture"
        key = ("p", f["Title"]) if person else ("m", a["nid"])
        if key not in ids:
            ids[key] = person_id(f["Title"]) if person else movie_id(f)
        tid = ids[key]
        r = {"file": a["file"], "nid": a["nid"], "field": a["field"], "title": f["Title"], "status": "none"}
        if tid:
            if person:
                cands = S.tmdb("/person/%d/images" % tid)["profiles"]
            else:
                im = S.tmdb("/movie/%d/images" % tid)
                cands = im["posters"] if a["field"] == "Poster" else im["backdrops"]
            cands = sorted(cands, key=lambda b: -(b.get("vote_count") or 0))[:25]
            old = U.gray(os.path.join(U.MEDIA, a["file"]))
            best, best_n = None, 0
            for k, b in enumerate(cands):
                p = get(IMG + "w300" + b["file_path"], os.path.join(WORK, "s_%s_%d_%s.jpg" % (key[0], tid, b["file_path"].strip("/").split(".")[0])))
                n = U.inliers(old, U.gray(p))
                if n > best_n:
                    best, best_n = b, n
                if best_n >= 40:
                    break
            if best and best_n >= 25 and max(best["width"], best["height"]) >= U.MIN:
                r.update(status="match", inliers=best_n, path=best["file_path"], w=best["width"], h=best["height"])
            elif a["field"] == "Poster" and cands:
                top = [c for c in cands if c.get("iso_639_1") in ("en", None)] or cands
                if max(top[0]["width"], top[0]["height"]) >= U.MIN:
                    r.update(status="poster, no match", inliers=best_n, path=top[0]["file_path"], w=top[0]["width"], h=top[0]["height"])
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        fh.flush()
        print(r["title"][:30], a["field"], r["status"], r.get("inliers"), flush=True)


def rows():
    out = {}
    for l in open(PLAN, encoding="utf-8"):
        r = json.loads(l)
        out[r["file"]] = r
    return out


def full(r):
    p = get(IMG + "original" + r["path"], os.path.join(WORK, "o_" + r["path"].strip("/")))
    return p


def sheet():
    from PIL import Image, ImageDraw
    rs = [r for r in rows().values() if r.get("path")]
    W, H, per = 200, 170, 40
    for s in range(0, len(rs), per):
        chunk = rs[s:s + per]
        sh = Image.new("RGB", (8 * W, ((len(chunk) + 3) // 4) * (H + 20)), "white")
        for j, r in enumerate(chunk):
            x0, y0 = (j % 4) * 2 * W, (j // 4) * (H + 20)
            for k, src in enumerate((os.path.join(U.MEDIA, r["file"]), get(IMG + "w300" + r["path"], os.path.join(WORK, "v_" + r["path"].strip("/"))))):
                try:
                    im = Image.open(src).convert("RGB")
                    im.thumbnail((W - 6, H - 6))
                    sh.paste(im, (x0 + k * W + 3, y0 + 3))
                except Exception:
                    pass
            ImageDraw.Draw(sh).text((x0 + 3, y0 + H), "%d %s %s %s" % (s + j, r["title"][:22], r["field"], r["status"][:8]), fill="black")
        sh.save(os.path.join(WORK, "pairs_%02d.jpg" % (s // per)), quality=82)
    print(len(rs), "pairs")


def apply(really):
    from PIL import Image
    reject = set(json.load(open(REJECT, encoding="utf-8"))) if os.path.exists(REJECT) else set()
    rs = [r for i, r in enumerate([r for r in rows().values() if r.get("path")]) if i not in reject]
    print(len(rs), "Film pictures to replace")
    if not really:
        return
    bk = {}
    for r in rs:
        src = full(r)
        im = Image.open(src).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400))
        assert max(im.size) >= U.MIN, (r["title"], im.size)
        fn = "film-hr-%s" % os.path.basename(r["path"]).replace(".png", ".jpg")
        out = os.path.join(WORK, fn)
        im.save(out, quality=90)
        C.anki("storeMediaFile", filename=fn, path=out)
        n = C.anki("notesInfo", notes=[r["nid"]])[0]
        upd = {}
        v = n["fields"][r["field"]]["value"]
        if 'src="%s"' % r["file"] not in v:
            continue
        upd[r["field"]] = v.replace('src="%s"' % r["file"], 'src="%s"' % fn)
        bk.setdefault(str(r["nid"]), {})[r["field"]] = v
        if r["status"] == "poster, no match":
            cap = n["fields"]["Poster caption"]["value"]
            if cap.startswith("Release poster"):
                upd["Poster caption"] = "Poster" + cap[len("Release poster"):]
                bk[str(r["nid"])]["Poster caption"] = cap
        C.anki("updateNoteFields", note={"id": r["nid"], "fields": upd})
    json.dump(bk, open("backups/film_hr_1002_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
    print("applied", len(bk), "notes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    {"find": find, "sheet": sheet}.get(sys.argv[1], lambda: apply("--apply" in sys.argv))()
