# -*- coding: utf-8 -*-
"""cm_desc_move.py -- Classical Music backs: Description above the tier tag, centred.

Carter (2026-09-25): "the note should be above the tag on the back and it should
be centered (on my phone it is on the left)". The Description div sat after the
tier-tag container, and .cm2-desc forced text-align:left.

    py -3.9 cm_desc_move.py --dry | --apply
"""
import json, sys, time
import concept_add as C

M = "Classical Music"
DESC = '{{^Kind}}{{#Description}}<div class="cm2-desc">{{Description}}</div>{{/Description}}{{/Kind}}'
TAG = '<div id="allowed-tags-container" class="qb-tier"></div>'
OLD_CSS = "max-width: 640px; margin: 16px auto 0; text-align: left; }"
NEW_CSS = "max-width: 640px; margin: 16px auto 0; text-align: center; }"

apply = "--apply" in sys.argv
t = C.anki("modelTemplates", modelName=M)
css = C.anki("modelStyling", modelName=M)["css"]
json.dump({"templates": t, "css": css},
          open("templates_backup/classical_before_descmove_%s.json" % time.strftime("%Y%m%d_%H%M"),
               "w", encoding="utf-8"), ensure_ascii=False, indent=1)
new = {}
for name in ("AUDIO to COMPOSER", "AUDIO and WORK to COMPOSER"):
    b = t[name]["Back"]
    assert b.count(DESC) == 1 and b.count(TAG) == 1, name
    b2 = b.replace("\n" + DESC, "").replace(DESC, "")
    b2 = b2.replace(TAG, DESC + "\n" + TAG)
    assert b2.index(DESC) < b2.index(TAG)
    new[name] = {"Back": b2}
    print(name, "Description moved above tier tag")
assert css.count(OLD_CSS) == 1
print(".cm2-desc text-align left -> center")
if apply:
    C.anki("updateModelTemplates", model={"name": M, "templates": new})
    C.anki("updateModelStyling", model={"name": M, "css": css.replace(OLD_CSS, NEW_CSS)})
    print("applied")
