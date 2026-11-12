# -*- coding: utf-8 -*-
"""cm_qb_apply.py -- Carter, 2026-10-02: "can we verify we are cluing the best things for quizbowl in the music deck --
sometimes it just names an opera that is famous when the card itself is testing an aria that is less famous"; "try to
clue passages that are often clued in quizbowl ... note progressions"; "make sure the way you present the listen for in
general aligns with quizbowl writing"; "The detail I don't mind as referring to the whole work but the listen for should
be just the passage clipped."

Each batch file (data/cm_qb/batch_NN.json) gives, per live Music note, a new Listen line written in tossup voice about
the clip only (what plays, who plays it, the motif's notes, key, meter, as tossups cite them), and for an aria or
movement a Clue that points to the work through that excerpt, as tossups use it. Written against the tossups that
mention each work (scratchpad qb_dossier.py: 10,414 qbreader questions) and what each clip holds (clip_analyze.py:
key estimate, loudness shape, opening notes, sung words). The Description (Detail) stays about the whole work.

    py -3.9 cm_qb_apply.py data/cm_qb/batch_00.json [--apply]
"""
import json
import os
import re
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
STOP = {"symphony", "concerto", "sonata", "quartet", "piano", "major", "minor", "the", "and", "for", "with", "from", "no.", "of",
        "in", "mass", "suite", "opera", "variations", "string", "violin", "cello", "prelude", "fugue", "overture"}


def main(path, apply):
    batch = json.load(open(os.path.join(HERE, path), encoding="utf-8"))
    notes = {n["noteId"]: n for n in C.anki("notesInfo", notes=[int(k) for k in batch])}
    backup, warn = {}, []
    for k, new in batch.items():
        n = notes[int(k)]
        f = {x: v["value"] for x, v in n["fields"].items()}
        work = C.plain(f["Work"]).strip()
        words = {w for w in re.findall(r"[A-Za-zÀ-ÿ']{5,}", work.lower()) if w not in STOP}
        clue = C.plain(new.get("Clue", "")).lower()
        leak = [w for w in words if w in clue]
        if leak:
            warn.append("%s %s: clue contains %s" % (k, work, leak))
        for x in [x for x in new if "<img" in f[x]]:
            warn.append("%s %s: %s holds an image, skipped" % (k, work, x))
            del new[x]
        backup[k] = {x: f[x] for x in new}
        print("#%s %s | %s" % (k, work, C.plain(f["Movement"])))
        for x, v in new.items():
            print("   %s: %s" % (x, C.plain(v)))
    for w in warn:
        print("WARN", w)
    if not apply:
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump(backup, open(os.path.join(HERE, "backups", "cm_qb_%s_before_%s.json" % (os.path.basename(path)[:-5], stamp)), "w",
                           encoding="utf-8"), ensure_ascii=False)
    for k, new in batch.items():
        C.anki("updateNoteFields", note={"id": int(k), "fields": new})
    print("applied", len(batch))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main(sys.argv[1], "--apply" in sys.argv)
