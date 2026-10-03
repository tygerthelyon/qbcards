# -*- coding: utf-8 -*-
"""art_title_notes_space.py -- TITLE to ARTIST: the W109 context note sat flush
under the title, in parentheses, with no top margin (Carter, 2026-09-25: "verify
the spacing on the front side"). Parentheses were for the old one-phrase notes;
Notes now holds full sentences. Given a margin, line height and a measure, on
front and back.

    py -3.9 art_title_notes_space.py --dry | --apply
"""
import json, sys, time
import concept_add as C

FRONT_OLD = ("<div style=\n'color: #6b4c3b;\nfont-size: 18px;\ntext-align: center'>\n({{Notes}})\n</div>")
FRONT_NEW = ("<div style=\n'color: #6b4c3b;\nfont-size: 17px;\nline-height: 1.5;\nmax-width: 620px;\n"
             "margin: 14px auto 0;\ntext-align: center'>\n{{Notes}}\n</div>")
BACK_OLD = ("<div style='color: #6b4c3b; font-size: 18px; text-align: center;\nmargin-top: 10px'>({{Notes}})</div>")
BACK_NEW = ("<div style='color: #6b4c3b; font-size: 17px; line-height: 1.5; max-width: 620px; text-align: center;\n"
            "margin: 14px auto 0'>{{Notes}}</div>")
t = C.anki("modelTemplates", modelName="Art")
v = t["TITLE to ARTIST"]
print("front:", v["Front"].count(FRONT_OLD), "back:", v["Back"].count(BACK_OLD))
assert v["Front"].count(FRONT_OLD) == 1 and v["Back"].count(BACK_OLD) == 1
if "--apply" in sys.argv:
    json.dump(t, open("templates_backup/art_before_title_notes_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
    C.anki("updateModelTemplates", model={"name": "Art", "templates": {"TITLE to ARTIST": {
        "Front": v["Front"].replace(FRONT_OLD, FRONT_NEW), "Back": v["Back"].replace(BACK_OLD, BACK_NEW)}}})
    print("applied")
