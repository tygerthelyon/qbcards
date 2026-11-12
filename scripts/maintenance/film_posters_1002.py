# -*- coding: utf-8 -*-
"""film_posters_1002.py -- the ten posters film_hr_1002.py matched to the wrong copy, matched again against all of TMDB's posters.

film_hr_1002.py stopped at the first good match among a film's 25 most-voted posters, which for these ten was a
redesign or a foreign-language reprint (rejected on the contact sheet). Scoring every poster TMDB holds found the
same design at 1000px or more for each: the same language, or for Lagaan the Hindi release of the same artwork.
Picked by eye from data in poster_rematch.json; captions stay as they are.

    py -3.9 film_posters_1002.py [--apply]
"""
import json, os, sys, time
from PIL import Image
import concept_add as C
import film_hr_1002 as F
import img_upgrade_1002 as U

PICK = {"A Trip to the Moon": 0, "Casablanca": 3, "Das Boot": 0, "Women on the Verge of a Nervous Breakdown": 0, "Amélie": 3,
        "Lagaan": 1, "The White Ribbon": 0, "Gravity": 0, "Jules and Jim": 0, "Cléo from 5 to 7": 0}


def main(really):
    d = json.load(open(os.path.join(F.WORK, "poster_rematch.json"), encoding="utf-8"))
    bk = {}
    for f, r in d.items():
        if r["title"] not in PICK:
            continue
        s = r["scores"][PICK[r["title"]]]
        src = F.get(F.IMG + "original" + s[4], os.path.join(F.WORK, "o_" + s[4].strip("/")))
        im = Image.open(src).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400))
        assert max(im.size) >= U.MIN
        fn = "film-hr-" + os.path.basename(s[4]).rsplit(".", 1)[0] + ".jpg"
        print("%-42s %s %dx%d" % (r["title"], s[1], im.size[0], im.size[1]))
        if not really:
            continue
        out = os.path.join(F.WORK, fn)
        im.save(out, quality=90)
        C.anki("storeMediaFile", filename=fn, path=out)
        v = C.anki("notesInfo", notes=[r["nid"]])[0]["fields"]["Poster"]["value"]
        if 'src="%s"' % f in v:
            bk[str(r["nid"])] = {"Poster": v}
            C.anki("updateNoteFields", note={"id": r["nid"], "fields": {"Poster": v.replace('src="%s"' % f, 'src="%s"' % fn)}})
    if really:
        json.dump(bk, open("backups/film_posters_1002_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        print("updated", len(bk))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
