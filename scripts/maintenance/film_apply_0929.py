# -*- coding: utf-8 -*-
"""film_apply_0929.py -- write film_text_0929.T (clues, details, movements) into the Film notes.

The Film tier tags follow Movement where they carry one (Film::movement::...); none do today, so only
the fields change. Backs up every field it touches.

    py -3.9 film_apply_0929.py [--apply]
"""
import json, sys, time
import concept_add as C
from film_text_0929 import T

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(T))}
    ch = {}
    for nid, f in T.items():
        d = {k: v for k, v in f.items() if ns[nid]["fields"][k]["value"] != v}
        if d:
            ch[nid] = d
    from collections import Counter
    print(len(ch), "notes;", dict(Counter(k for d in ch.values() for k in d)))
    if "--apply" in sys.argv:
        json.dump({str(nid): {k: ns[nid]["fields"][k]["value"] for k in d} for nid, d in ch.items()},
                  open("backups/film_apply_0929_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for nid, d in ch.items():
            C.anki("updateNoteFields", note={"id": nid, "fields": d})
        print("applied")
