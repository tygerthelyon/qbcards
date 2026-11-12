# -*- coding: utf-8 -*-
"""geo_maps_apply.py -- put the v4 Geography maps (geo_maps_v4.py) into the deck.

Each rendered note gets three images:
    Map          the question map: the place in its surroundings, the answer not named
    Map Labeled  the answer map: the same view with the place named
    Map Wide     the locator: zoomed out (its country, sub-region or hemisphere), the place in red
The MAP to NAME card shows Map + Map Wide on the front and Map Labeled + Map Wide on the back.

Images are palette-quantised (flat map colours survive it; ~85 KB instead of ~300 KB) and named with a
content hash, so a re-rendered map never collides with a copy the phone has cached.

    py -3.9 geo_maps_apply.py --dirs renders/geo_v4/p1,renders/geo_v4/p2 [--names "A|B"] [--apply]
"""
import argparse
import hashlib
import io
import json
import os
import sys
import time

from PIL import Image

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = (("front", "Map", "g4front"), ("back", "Map Labeled", "g4lab"), ("locator", "Map Wide", "g4loc"))


def packed(path):
    im = Image.open(path).convert("RGB")
    q = im.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE)
    buf = io.BytesIO()
    q.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", required=True)
    ap.add_argument("--names", default="")
    ap.add_argument("--apply", action="store_true")
    # a long apply done in pieces: skip the first N rendered notes (in manifest order), which a piece already applied
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--count", type=int, default=0)   # 0: to the end
    a = ap.parse_args()
    want = {x.strip() for x in a.names.split("|") if x.strip()}
    todo = {}
    for d in a.dirs.split(","):
        man = json.load(open(os.path.join(HERE, d.strip(), "manifest.json"), encoding="utf-8"))
        for nid, r in man.items():
            if r.get("status") == "rendered" and (not want or r["name"] in want):
                if all(os.path.exists(r[k]) for k, _, _ in FIELDS):
                    todo[int(nid)] = r
    todo = dict(list(todo.items())[a.start:a.start + a.count if a.count else None])
    print("from note", a.start, ":", len(todo), "to check", flush=True)
    info = {}
    ids = list(todo)
    for i in range(0, len(ids), 400):
        for n in C.anki("notesInfo", notes=ids[i:i + 400]):
            info[n["noteId"]] = n
    backup, n_done = {}, 0
    # the backup is written as the run goes: a run cut off by a restart left notes updated with no record
    # (pieces run side by side: the start offset keeps their backups apart)
    bpath = os.path.join(HERE, "backups", "geo_maps_before_%s_%d.json" % (time.strftime("%Y%m%d_%H%M%S"), a.start))
    for nid, r in todo.items():
        if nid not in info:
            continue
        fields = {}
        for key, field, pre in FIELDS:
            data = packed(r[key])
            h = hashlib.md5(data).hexdigest()[:8]
            base = os.path.basename(r[key])[len(pre) + 1:-4].lower()
            fname = "%s-%s-%s.png" % (pre, base, h)
            if a.apply:
                # Anki refuses media writes while it syncs media, which a large apply itself sets off: wait it out
                for attempt in range(40):
                    try:
                        C.anki("storeMediaFile", filename=fname, data=__import__("base64").b64encode(data).decode())
                        break
                    except RuntimeError as e:
                        if "syncing" not in str(e) and "not available" not in str(e):
                            raise
                        print("  (Anki busy: %s; waiting)" % e, flush=True)
                        time.sleep(30)
            fields[field] = '<img src="%s">' % fname
        old = {f: info[nid]["fields"][f]["value"] for f in fields}
        if old == fields:
            continue
        backup[nid] = old
        n_done += 1
        if a.apply:
            if n_done % 25 == 1:
                json.dump(backup, open(bpath, "w", encoding="utf-8"), ensure_ascii=False)
            C.anki("updateNoteFields", note={"id": nid, "fields": fields})
            print("  updated", info[nid]["fields"]["Name"]["value"][:40], flush=True)
    if a.apply and backup:
        json.dump(backup, open(bpath, "w", encoding="utf-8"), ensure_ascii=False)
    print(("updated" if a.apply else "would update"), n_done, "notes of", len(todo), "rendered", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
