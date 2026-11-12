# -*- coding: utf-8 -*-
"""cm_layout_0928.py -- two Classical Music layout fixes (Carter, 2026-09-28).

  DESCRIPTION to WORK back: "Not enough space between description and audio clip" -- the clip sat
  directly under the clue. It now has the same gap as the other blocks.
  DEFINITION to NAME back: the clip is the "Heard in" example, but it sat under the Detail line. It
  now sits directly under "Heard in", and the Detail follows.

    py -3.9 cm_layout_0928.py [--apply]
"""
import json, sys, time
import concept_add as C

M = "Classical Music"
OLD_DEF = ('<div class="cm2-facts">{{#Composer}}<div class="cm2-fact"><div class="cm2-fact-label">Heard in</div>'
           '<div class="cm2-fact-value">{{Composer}}</div></div>{{/Composer}}</div>\n'
           '{{#Nickname}}<div class="cm2-detail"><div class="cm2-fact-label">Detail</div>'
           '<div class="cm2-detail-body">{{Nickname}}</div></div>{{/Nickname}}\n'
           '{{#Audio}}<div class="cm2-audio">{{Audio}}</div>{{/Audio}}')
NEW_DEF = ('<div class="cm2-facts">{{#Composer}}<div class="cm2-fact"><div class="cm2-fact-label">Heard in</div>'
           '<div class="cm2-fact-value">{{Composer}}</div></div>{{/Composer}}</div>\n'
           '{{#Audio}}<div class="cm2-audio cm2-heard-audio">{{Audio}}</div>{{/Audio}}\n'
           '{{#Nickname}}<div class="cm2-detail"><div class="cm2-fact-label">Detail</div>'
           '<div class="cm2-detail-body">{{Nickname}}</div></div>{{/Nickname}}')
CSS = """
/* 2026-09-28: breathing room around the clip under a clue or a "Heard in" example */
.cm2 .cm2-def + .cm2-audio { margin-top: 20px; }
.cm2 .cm2-heard-audio { margin: 10px 0 18px; }
"""

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t = C.anki("modelTemplates", modelName=M)
    css = C.anki("modelStyling", modelName=M)["css"]
    back = t["DEFINITION to NAME"]["Back"]
    print("definition block found:", back.count(OLD_DEF), "| css present:", "breathing room around the clip" in css)
    if "--apply" in sys.argv:
        json.dump({"templates": t, "css": css}, open("templates_backup/cm_layout_0928_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        if back.count(OLD_DEF) == 1:
            C.anki("updateModelTemplates", model={"name": M, "templates": {"DEFINITION to NAME": {
                "Front": t["DEFINITION to NAME"]["Front"], "Back": back.replace(OLD_DEF, NEW_DEF)}}})
        if "breathing room around the clip" not in css:
            C.anki("updateModelStyling", model={"name": M, "css": css + CSS})
        print("applied")
