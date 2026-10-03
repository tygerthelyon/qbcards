# -*- coding: utf-8 -*-
"""art_template_fixes.py -- three layout fixes from Carter's phone review (2026-09-26).

1. "Description too close to year below it on back of card for harmony in blue and
   gold": the Notes block on the ARTWORK backs had a top margin and none below, so
   "— 1877 —" sat directly under it. It gets the same 18px below as above.
2. "Image appears too close below the description on the back of the Washington
   crossing Delaware description -> name card": DESCRIPTION to TITLE back, the clue
   ran straight into the picture. 18px between them.
3. "Instead of title + description -> artist, make it title -> artist with a button
   to reveal the description as a hint": the TITLE to ARTIST front showed the
   disambiguating line (location · date) under the title. That line, and the note's
   Clue where it has one, now sit behind a Hint button; the button only appears on
   notes that have something to reveal.

    py -3.9 art_template_fixes.py --dry | --apply
"""
import json
import sys
import time

import concept_add as C

M = "Art"

SHARED_OLD = """{{#TitleShared}}
<div class="title-shared-clue" style=
'color: #6b4c3b;
font-size: 17px;
text-align: center;
margin-top: 10px;
letter-spacing: 0.3px'>
{{TitleShared}}
</div>
{{/TitleShared}}"""

HINT = """<div class="qb-hint-wrap">
<div class="qb-hint-btn" onclick="var h = this.nextElementSibling; h.style.display = 'block'; this.style.display = 'none';">Hint</div>
<div class="qb-hint" style="display: none">{{#TitleShared}}<div class="title-shared-clue">{{TitleShared}}</div>{{/TitleShared}}{{#Clue}}<div class="art-clue qb-hint-clue">{{Clue}}</div>{{/Clue}}</div>
</div>
<script id="qb-hint">
(function () {
  Array.prototype.forEach.call(document.querySelectorAll(".qb-hint-wrap"), function (w) {
    var h = w.querySelector(".qb-hint");
    if (!h || !h.textContent.replace(/\\s+/g, "")) { w.style.display = "none"; }
  });
})();
</script>"""

CSS = """
/* Hint button on TITLE to ARTIST (2026-09-26) */
.qb-hint-wrap { text-align: center; margin-top: 16px; }
.qb-hint-btn { display: inline-block; padding: 5px 16px; border: 1px solid #c9bca6; border-radius: 16px;
  font-size: 14px; letter-spacing: 0.12em; text-transform: uppercase; color: #6b4c3b; cursor: pointer; }
.qb-hint .title-shared-clue { color: #6b4c3b; font-size: 17px; letter-spacing: 0.3px; margin-top: 4px; }
.qb-hint-clue { margin-top: 10px; }
.night_mode .qb-hint-btn, .nightMode .qb-hint-btn { border-color: #555; color: #aaa; }
"""


def main(apply):
    t = C.anki("modelTemplates", modelName=M)
    css = C.anki("modelStyling", modelName=M)["css"]
    ch = {}
    for name in ("ARTWORK to ARTIST", "ARTWORK to TITLE"):
        b = t[name]["Back"]
        assert b.count("margin: 18px auto 0;") == 1, name
        ch[name] = {"Front": t[name]["Front"], "Back": b.replace("margin: 18px auto 0;", "margin: 18px auto 18px;")}
    b = t["DESCRIPTION to TITLE"]["Back"]
    assert b.count('<div class="art-clue">{{Clue}}</div>') == 1
    ch["DESCRIPTION to TITLE"] = {"Front": t["DESCRIPTION to TITLE"]["Front"],
                                  "Back": b.replace('<div class="art-clue">{{Clue}}</div>',
                                                    '<div class="art-clue" style="margin-bottom: 18px">{{Clue}}</div>')}
    f = t["TITLE to ARTIST"]["Front"]
    assert f.count(SHARED_OLD) == 1
    ch["TITLE to ARTIST"] = {"Front": f.replace(SHARED_OLD, HINT), "Back": t["TITLE to ARTIST"]["Back"]}
    print("templates:", sorted(ch))
    if apply:
        json.dump({"templates": t, "css": css},
                  open("templates_backup/art_fixes_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w",
                       encoding="utf-8"), ensure_ascii=False)
        C.anki("updateModelTemplates", model={"name": M, "templates": ch})
        if ".qb-hint-btn" not in css:
            C.anki("updateModelStyling", model={"name": M, "css": css + CSS})
        print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
