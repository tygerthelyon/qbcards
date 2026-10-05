# -*- coding: utf-8 -*-
"""art_cleanup.py -- remove two duplicate Art notes and the Vitruvian Man picture (Anki must be open).

    py -3.9 audit\\art_cleanup.py           dry run
    py -3.9 audit\\art_cleanup.py --apply   do it

1. Deletes 1787890519171 (Raphael's Disputa, a duplicate of 1787890518304, which is kept; the deleted one
   wrongly said "Oil on panel").
2. Deletes 1790239802400 ("Surprised!", a duplicate of 1787890517675 "Tiger in a Tropical Storm (or
   Surprised!)", which is kept).
   Neither deleted note has ever been reviewed, so no history is lost.
3. Northern Renaissance movement card (1788586194873): removes the third picture and caption, Leonardo's
   Vitruvian Man, which is not Northern Renaissance.

Each step runs only if the note still matches the 2026-10-04 export; anything edited since is skipped.
Full notesInfo of every touched note is backed up to backups/art_cleanup_<timestamp>.json first.
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DELETE = {
    1787890519171: "<i>Disputation of the Sacrament (or La disputa)</i>",
    1790239802400: "<i>Surprised!</i>",
}
KEEP = {1787890519171: 1787890518304, 1790239802400: 1787890517675}
NR = 1788586194873
NR_OLD = {
    "Artwork": '<img src="artcon-Northern_Renaissance.jpg"><img src="multi-Northern_Renaissance-2.jpg">'
               '<img src="multi-Northern_Renaissance-4.jpg">',
    "Captions": "<i>The Adoration of the Magi</i> in the snow, Pieter Brueghel the Younger, 1584–1638 | "
                "Jan van Eyck, <i>The Arnolfini Portrait</i>, 1434, National Gallery, London | "
                "Leonardo da Vinci, <i>Vitruvian Man</i>, c. 1490",
}
NR_NEW = {
    "Artwork": '<img src="artcon-Northern_Renaissance.jpg"><img src="multi-Northern_Renaissance-2.jpg">',
    "Captions": "<i>The Adoration of the Magi</i> in the snow, Pieter Brueghel the Younger, 1584–1638 | "
                "Jan van Eyck, <i>The Arnolfini Portrait</i>, 1434, National Gallery, London",
}


def anki(action, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", data=json.dumps(
        {"action": action, "version": 6, "params": params}).encode(), headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    if r.get("error"):
        raise RuntimeError("%s: %s" % (action, r["error"]))
    return r["result"]


def main():
    apply = "--apply" in sys.argv
    ids = list(DELETE) + list(KEEP.values()) + [NR]
    info = {n["noteId"]: n for n in anki("notesInfo", notes=ids) if n}
    reps = {}
    cinfo = anki("cardsInfo", cards=anki("findCards", query=" OR ".join("nid:%d" % i for i in DELETE)))
    for c in cinfo:
        reps[c["note"]] = reps.get(c["note"], 0) + c.get("reps", 0)

    dele = []
    for nid, title in DELETE.items():
        n, keep = info.get(nid), info.get(KEEP[nid])
        if not n:
            print("SKIP %d: already gone" % nid)
        elif not keep:
            print("SKIP %d: the note to keep (%d) is missing, so not deleting" % (nid, KEEP[nid]))
        elif n["fields"]["Title"]["value"] != title:
            print("SKIP %d: title changed since the export" % nid)
        elif reps.get(nid):
            print("SKIP %d: it has %d reviews now; decide by hand" % (nid, reps[nid]))
        else:
            print("DELETE %d %s  (keeping %d %s)" % (nid, title, KEEP[nid], keep["fields"]["Title"]["value"]))
            dele.append(nid)

    nr = info.get(NR)
    upd = None
    if not nr:
        print("SKIP Northern Renaissance: note missing")
    elif any(nr["fields"][k]["value"] != v for k, v in NR_OLD.items()):
        print("SKIP Northern Renaissance: Artwork or Captions changed since the export")
    else:
        print("UPDATE %d Northern Renaissance: remove the Vitruvian Man picture and caption" % NR)
        upd = NR_NEW

    if not apply:
        print("\nDry run. Nothing written. Add --apply to do it.")
        return
    os.makedirs(os.path.join(ROOT, "backups"), exist_ok=True)
    bk = os.path.join(ROOT, "backups", "art_cleanup_%s.json" % time.strftime("%Y%m%d_%H%M%S"))
    json.dump([info[i] for i in ids if i in info], open(bk, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nBackup: %s" % bk)
    if dele:
        anki("deleteNotes", notes=dele)
        print("Deleted %d notes." % len(dele))
    if upd:
        anki("updateNoteFields", note={"id": NR, "fields": upd})
        print("Updated Northern Renaissance.")
    print("Done. The image file multi-Northern_Renaissance-4.jpg is now unused; Tools > Check Media can remove it.")


if __name__ == "__main__":
    main()
