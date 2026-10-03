# -*- coding: utf-8 -*-
"""dot_fix.py -- even spacing around the middle dot in proponent lists.

Audit 2026-09-26: "Middle-dot spacing is broken in proponent lists, rendering
'Donald Judd ·Carl Andre'." The proponents script joined names with "  ·  " in
the deck's body font, which draws the dot off-centre; everywhere else the deck
uses a .qb-dot span in Georgia with equal margins. The script now builds the
same span.

    py -3.9 dot_fix.py --dry | --apply
"""
import json
import sys
import time

import concept_add as C

U = chr(92) + "u00b7"      # the JS escape, kept literal: an editor pass turned it into the character once
OLD = r'e.textContent = artists.split(/\s*;\s*/).join("  ' + U + r'  ");'
NEW = (r'e.textContent = ""; artists.split(/\s*;\s*/).forEach(function (p, i) { if (i) { '
       r'var d = document.createElement("span"); d.className = "qb-dot"; d.textContent = "' + U + r'"; '
       r'e.appendChild(d); } e.appendChild(document.createTextNode(p)); });')
DOT_CSS = '\n.qb-dot { display: inline-block; margin: 0 0.42em; font-family: Georgia, "Times New Roman", serif; }\n'


def main(apply):
    bk, n = {}, 0
    for m in C.anki("modelNames"):
        t = C.anki("modelTemplates", modelName=m)
        ch = {}
        for k, v in t.items():
            f, b = v["Front"].replace(OLD, NEW), v["Back"].replace(OLD, NEW)
            if (f, b) != (v["Front"], v["Back"]):
                ch[k] = {"Front": f, "Back": b}
        if not ch:
            continue
        bk[m] = t
        n += len(ch)
        print(m, sorted(ch))
        if apply:
            C.anki("updateModelTemplates", model={"name": m, "templates": ch})
            css = C.anki("modelStyling", modelName=m)["css"]
            if ".qb-dot" not in css:
                C.anki("updateModelStyling", model={"name": m, "css": css + DOT_CSS})
    if apply:
        json.dump(bk, open("templates_backup/dot_fix_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w",
                           encoding="utf-8"), ensure_ascii=False)
    print(("updated" if apply else "would update"), n, "templates")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
