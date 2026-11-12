# -*- coding: utf-8 -*-
"""film_lowres2_1001.py -- every Film picture under 500px: the same picture, larger, wherever TMDB has it.

Carter, 2026-10-01: "also, fix the low quality images". After film_lowres_1001.py fixed the eleven on tier-1
front pictures, 175 more Film pictures were under 500px: 134 posters and 41 gallery stills, mostly 220-330px
Wikipedia thumbnails, most of them on tier-2 cards (suspended until promoted).

Every still has a caption describing its frame ("Here's Johnny!", "The dance of death along the hilltop"), and
posters are captioned "Release poster", so a different picture would make the caption wrong. So:
  * each small picture is matched against TMDB's images of the film (the 20 most-voted backdrops or 12 posters, compared as 342px previews) with ORB
    feature matching, which survives crops and colour shifts; a match needs 25+ consistent keypoints under a
    RANSAC homography, i.e. the same frame or the same poster design;
  * a match replaces the picture and keeps its caption;
  * a poster with no match takes TMDB's most-voted poster, and its caption changes from "Release poster" to
    "Poster", since it may be a later design;
  * a still with no match stays as it is (publicity and on-set photographs TMDB does not carry).
Matches are checked by eye on contact sheets (old beside new) before --apply.

    py -3.9 film_lowres2_1001.py find
    py -3.9 film_lowres2_1001.py [--apply]     (data/film_lowres2_reject_1001.json lists any rejected)
"""
import json, os, re, sys, time, urllib.request
import cv2
import numpy as np
import concept_add as C

WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_lowres2_1001")
ITEMS = "data/film_lowres_all_1001.json"
REJECT = "data/film_lowres2_reject_1001.json"
MEDIA = os.path.expandvars(r"%APPDATA%\Anki2\User 1\collection.media")
SP = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\4c6fe2ff-c3a6-47fb-8b54-226f916ad6af\scratchpad"


def load_gray(path, long=600):
    data = np.fromfile(path, dtype=np.uint8) if os.path.exists(path) else np.zeros(0, np.uint8)
    if not data.size:
        return None
    im = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    if im is None:
        return None
    s = long / max(im.shape)
    return cv2.resize(im, (max(1, int(im.shape[1] * s)), max(1, int(im.shape[0] * s))))


ORB = cv2.ORB_create(2000)
BF = cv2.BFMatcher(cv2.NORM_HAMMING)


def inliers(a, b):
    ka, da = ORB.detectAndCompute(a, None)
    kb, db = ORB.detectAndCompute(b, None)
    if da is None or db is None or len(ka) < 10 or len(kb) < 10:
        return 0
    good = []
    for m in BF.knnMatch(da, db, k=2):
        if len(m) == 2 and m[0].distance < 0.75 * m[1].distance:
            good.append(m[0])
    if len(good) < 10:
        return 0
    pa = np.float32([ka[m.queryIdx].pt for m in good])
    pb = np.float32([kb[m.trainIdx].pt for m in good])
    H, mask = cv2.findHomography(pa, pb, cv2.RANSAC, 6.0)
    return int(mask.sum()) if mask is not None else 0


def tmdb_movie(it):
    import film_stills as S
    dirs = [S.surname(d) for d in re.split(r",| and |;|&", it["director"]) if S.surname(d)]
    year = (re.findall(r"\d{4}", it["year"]) or [""])[0]
    for q in [it["title"], it["orig"]]:
        if not q:
            continue
        for yr in ([year] if year else []) + [None]:
            for r in S.tmdb("/search/movie", query=q, **({"year": yr} if yr else {}))["results"][:5]:
                crew = S.tmdb("/movie/%d/credits" % r["id"])["crew"]
                names = " ".join(C.fold(c["name"]) for c in crew if c.get("job") == "Director")
                if not dirs or any(d in names for d in dirs):
                    return r["id"]
    return None


def get(url, path):
    if not os.path.exists(path) or not os.path.getsize(path):     # an interrupted download leaves an empty file
        open(path, "wb").write(urllib.request.urlopen(url, timeout=60).read())
        time.sleep(0.15)
    return path


def find():
    import film_stills as S
    os.makedirs(WORK, exist_ok=True)
    items = json.load(open(ITEMS, encoding="utf-8"))
    part = os.path.join(WORK, "plan_partial.jsonl")          # resumable: one line per picture
    done = {json.loads(l)["i"]: json.loads(l) for l in open(part, encoding="utf-8")} if os.path.exists(part) else {}
    fh = open(part, "a", encoding="utf-8")
    plan = []
    movies = {}
    for i, it in enumerate(items):
        if i in done:
            plan.append(done[i])
            continue
        if it["kind"]:
            plan.append(dict(it, i=i, result="person picture: skipped"))
            continue
        if it["nid"] not in movies:
            movies[it["nid"]] = tmdb_movie(it)
        mid = movies[it["nid"]]
        if not mid:
            plan.append(dict(it, i=i, result="no TMDB match"))
            continue
        imgs = S.tmdb("/movie/%d/images" % mid)
        poster = it["field"] == "Poster"
        cands = imgs["posters"] if poster else imgs["backdrops"]
        cands = sorted(cands, key=lambda b: -(b.get("vote_count") or 0) * (b.get("vote_average") or 1))[:12 if poster else 20]
        old = load_gray(os.path.join(MEDIA, it["file"]))
        best, best_k, best_path = None, 0, None
        for k, b in enumerate(cands):
            # match on small previews; only the winner is fetched at full size
            p = get("https://image.tmdb.org/t/p/w342%s" % b["file_path"], os.path.join(WORK, "s_%d_%s_%d.jpg" % (mid, "p" if poster else "b", k)))
            new = load_gray(p)
            n = inliers(old, new) if old is not None and new is not None else 0
            if n > best_k:
                best, best_k = b, n
        if best_k >= 25:
            size = "w780" if poster else "w1280"
            best_path = get("https://image.tmdb.org/t/p/%s%s" % (size, best["file_path"]), os.path.join(WORK, "%d_%s.jpg" % (mid, best["file_path"].strip("/").split(".")[0])))
            plan.append(dict(it, i=i, result="match", inliers=best_k, new=best_path))
        elif poster:
            top = [b for b in cands if b.get("iso_639_1") in ("en", None)] or cands
            p = get("https://image.tmdb.org/t/p/w780" + top[0]["file_path"], os.path.join(WORK, "%d_p_top.jpg" % mid)) if top else None
            plan.append(dict(it, i=i, result="poster, no match" if p else "no poster", inliers=best_k, new=p))
        else:
            plan.append(dict(it, i=i, result="still, no match: kept", inliers=best_k))
        print(i, it["title"][:30], it["field"], plan[-1]["result"], plan[-1].get("inliers"), flush=True)
        fh.write(json.dumps(plan[-1], ensure_ascii=False) + "\n")
        fh.flush()
    json.dump(plan, open(os.path.join(WORK, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    # contact sheets: old (left) beside new (right)
    from PIL import Image, ImageDraw
    tiles = [p for p in plan if p.get("new")]
    per = 24
    for s in range(0, len(tiles), per):
        chunk = tiles[s:s + per]
        W, H = 250, 210
        sh = Image.new("RGB", (4 * W, ((len(chunk) + 1) // 2) * (H + 22)), "white")
        for j, p in enumerate(chunk):
            x0, y0 = (j % 2) * 2 * W, (j // 2) * (H + 22)
            for k, src in enumerate((os.path.join(MEDIA, p["file"]), p["new"])):
                try:
                    im = Image.open(src).convert("RGB")
                    im.thumbnail((W - 8, H - 8))
                    sh.paste(im, (x0 + k * W + 4, y0 + 4))
                except Exception:
                    pass
            ImageDraw.Draw(sh).text((x0 + 4, y0 + H), "%d %s %s %s" % (p["i"], p["title"][:26], p["field"], p["result"][:12]), fill="black")
        sh.save(os.path.join(WORK, "pairs_%02d.jpg" % (s // per)), quality=85)


def apply():
    plan = json.load(open(os.path.join(WORK, "plan.json"), encoding="utf-8"))
    reject = set(json.load(open(REJECT, encoding="utf-8"))) if os.path.exists(REJECT) else set()
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=sorted({p["nid"] for p in plan}))}
    ch, bk = {}, {}
    for p in plan:
        if not p.get("new") or p["i"] in reject:
            continue
        n = ns[p["nid"]]
        field = p["field"]
        fn = "film-%d-%s-1001.jpg" % (p["nid"], re.sub(r"[^a-z0-9]+", "", field.lower()))
        C.anki("storeMediaFile", filename=fn, path=p["new"])
        cur = ch.setdefault(p["nid"], {})
        cur[field] = n["fields"][field]["value"].replace(p["file"], fn)
        bk.setdefault(str(p["nid"]), {})[field] = n["fields"][field]["value"]
        if field == "Poster" and p["result"] == "poster, no match":
            cap = n["fields"]["Poster caption"]["value"]
            if cap.startswith("Release poster"):
                cur["Poster caption"] = "Poster" + cap[len("Release poster"):]
                bk[str(p["nid"])]["Poster caption"] = cap
    json.dump(bk, open("backups/film_lowres2_1001_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
    for nid, d in ch.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": d})
    print("applied:", sum(len([k for k in d if not k.endswith("caption")]) for d in ch.values()), "pictures in", len(ch), "notes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:2] == ["find"]:
        find()
    elif "--apply" in sys.argv:
        apply()
