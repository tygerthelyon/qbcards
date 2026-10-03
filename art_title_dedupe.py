# -*- coding: utf-8 -*-
"""art_title_dedupe.py -- ARTWORK to TITLE back printed artist and date twice.

Carter (2026-09-25): the Medusa back shows "[image], Medusa, artist name and
year, artist name, year". W102 added an "Artist, Date" line under the title on
the belief that the card never showed the artist; it already did, in the
Artist / "- Date -" block lower down. The added line is removed; the Notes block
W109 relies on stays.

    py -3.9 art_title_dedupe.py --dry | --apply
"""
import json, sys, time
import concept_add as C

LINE = ("<div style=\n'font-size: 19px;\ncolor: #6b4c3b;\nmargin-top: 8px'>\n"
        "{{#Artist}}{{Artist}}{{/Artist}}{{#Date}}, {{Date}}{{/Date}}\n</div>\n\n")
t = C.anki("modelTemplates", modelName="Art")
b = t["ARTWORK to TITLE"]["Back"]
print("added line present:", b.count(LINE), "| original artist block present:",
      b.count("{{Artist}}\n</div>"), "| date block:", b.count("— {{Date}} —"))
assert b.count(LINE) == 1 and b.count("— {{Date}} —") == 1
if "--apply" in sys.argv:
    json.dump(t, open("templates_backup/art_before_title_dedupe_%s.json" % time.strftime("%Y%m%d_%H%M"),
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    C.anki("updateModelTemplates", model={"name": "Art", "templates": {
        "ARTWORK to TITLE": {"Back": b.replace(LINE, "")}}})
    print("applied")
