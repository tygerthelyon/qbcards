# -*- coding: utf-8 -*-
"""arch_detail_rewrite.py -- replace thin Architecture DETAIL notes.

Carter 2026-09-27: "DETAIL often adds very little information: selimiye mosque for eg."
All 533 Notes were read; the ones that only restated the description, were filler
("Enduring symbol of ...", "UNESCO World Heritage."), were run-on bullet lists, or had
spelling/naming slips are rewritten in data/arch_notes_rewrites.py.

    py -3.9 arch_detail_rewrite.py [--apply]
"""
import json
import re
import sys
import time

import concept_add as C

sys.path.insert(0, "data")
from arch_notes_rewrites import NEW  # noqa: E402

# Titles and foreign terms get italics (text style: italics for titles and foreign words).
ITALIC = [
    "Allegory of Good and Bad Government", "Holy Trinity", "Star Wars", "Puppy", "Isle of the Dead",
    "Indiana Jones and the Last Crusade", "The Bible of Amiens", "The Temple of the Golden Pavilion",
    "The Weather Project", "To-morrow: A Peaceful Path to Real Reform", "pilotis", "trompe-l'oeil",
    "clocháns", "ardha-mandapa", "maha-mandapa", "mandapa", "antarala", "garbhagriha",
]


def html(s):
    s = s.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
    for t in ITALIC:
        s = re.sub(r"(?<![\w>-])" + re.escape(t) + r"(?![\w<-])", "<i>" + t + "</i>", s)
    return s


def main(apply):
    rows = json.load(open("data/arch_notes_audit.json", encoding="utf-8"))
    by = {r["name"]: r["nid"] for r in rows}
    missing = [k for k in NEW if k not in by]
    if missing:
        sys.exit("not found: %s" % missing)
    nids = [by[k] for k in NEW]
    info = {i["noteId"]: i for i in C.anki("notesInfo", notes=nids)}
    backup, n = {}, 0
    for name, text in NEW.items():
        nid = by[name]
        old = info[nid]["fields"]["Notes"]["value"]
        new = html(text)
        if old == new:
            continue
        backup[nid] = old
        n += 1
        print("%s\n  - %s\n  + %s" % (name, C.plain(old)[:160], new[:220]))
        if apply:
            C.anki("updateNoteFields", note={"id": nid, "fields": {"Notes": new}})
    if apply:
        json.dump(backup, open("backups/arch_detail_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w",
                               encoding="utf-8"), ensure_ascii=False)
    print(("updated" if apply else "would update"), n, "notes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
