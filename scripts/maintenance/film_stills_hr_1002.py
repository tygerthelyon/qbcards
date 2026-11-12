# -*- coding: utf-8 -*-
"""film_stills_hr_1002.py -- Film stills under 1000px with no larger copy, replaced by a TMDB frame of the same film.

film_hr_1002.py found no TMDB backdrop matching 120 stills (most are publicity or on-set photographs, or frames
TMDB does not carry), and img_upgrade_1002.py looks for the same still on Wikimedia. For the active cards' stills
that neither upgraded, a frame was chosen by eye from the film's TMDB backdrops (true frames only, no fan art or
posters), preferring one that shows what the old caption describes so the caption can stay; otherwise the caption
is rewritten for the new frame. Picks: data/replace/film_still_picks.json, {"nid|field": [index, caption or null]},
indexes into still_cands.json.

    py -3.9 film_stills_hr_1002.py [--apply]
"""
import json, os, sys, time
from PIL import Image
import concept_add as C
import film_hr_1002 as F
import img_upgrade_1002 as U


def main(really):
    picks = json.load(open("data/replace/film_still_picks.json", encoding="utf-8"))
    cands = json.load(open(os.path.join(F.WORK, "still_cands.json"), encoding="utf-8"))
    rows = U.plan_rows()
    rej = set(json.load(open(U.REJECT, encoding="utf-8")))
    bk, n = {}, 0
    for key, (idx, cap) in picks.items():
        nid, field = key.split("|")
        f = C.anki("notesInfo", notes=[int(nid)])[0]["fields"]
        v = f[field]["value"]
        old = [fn for _, fn, _ in [s for s in cands[nid]["slots"] if s[0] == field]]
        if not old or 'src="%s"' % old[0] not in v:
            print("%-40s already changed, skipped" % key)
            continue
        r = rows.get(old[0])
        if r and r["status"] == "match" and old[0] not in rej:
            print("%-40s Wikimedia has the same still larger, skipped" % key)
            continue
        c = cands[nid]["cands"][idx]
        src = F.get(F.IMG + "original" + c["path"], os.path.join(F.WORK, "o_" + c["path"].strip("/")))
        im = Image.open(src).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400))
        assert max(im.size) >= U.MIN, (key, im.size)
        fn = "film-hr-%s" % os.path.basename(c["path"]).rsplit(".", 1)[0] + ".jpg"
        upd = {field: v.replace('src="%s"' % old[0], 'src="%s"' % fn)}
        if cap is not None:
            upd[field + " caption"] = cap
        print("%-40s %s %dx%d | %s" % (key, fn, im.size[0], im.size[1], cap if cap is not None else "(caption kept) " + C.plain(f[field + " caption"]["value"])[:50]))
        if really:
            out = os.path.join(F.WORK, fn)
            im.save(out, quality=90)
            C.anki("storeMediaFile", filename=fn, path=out)
            bk[nid] = dict(bk.get(nid, {}), **{k: f[k]["value"] for k in upd})
            C.anki("updateNoteFields", note={"id": int(nid), "fields": upd})
            json.dump(bk, open("backups/film_stills_hr_1002_%s.json" % stamp, "w", encoding="utf-8"), ensure_ascii=False)
        n += 1
    print(n, "stills", "replaced" if really else "to replace")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    stamp = time.strftime("%Y%m%d_%H%M")
    main("--apply" in sys.argv)
