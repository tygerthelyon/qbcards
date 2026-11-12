# -*- coding: utf-8 -*-
"""cm_listen_model.py -- add a Listen field: what to actually hear.

The back already prints Period, Genre, Year and a historical Description. None of
it is aural. The ear card now runs (cm_ear.py) but when Carter gets it wrong the
back tells him *facts about the piece*, not *what he should have noticed*.

Listen is one short line of concrete audible features -- forces, texture, tempo,
the identifying gesture -- placed directly under the player on the back so it is
read while the sound is still in the ear. Written to be discriminative (what
separates this from its neighbours), not descriptive.
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import concept_add as C

M = "Classical Music"
BLOCK = ('{{#Listen}}<div class="cm2-listen">'
         '<div class="cm2-listen-label">Listen for</div>{{Listen}}</div>{{/Listen}}')
CSS = """
.cm2-listen{max-width:34em;margin:.55em auto .2em;padding:.5em .75em;
  border-left:3px solid #7a8b9c;background:rgba(122,139,156,0.10);
  border-radius:3px;text-align:left;font-size:.92em;line-height:1.45;color:#3d4650;}
.cm2-listen-label{font-size:.68em;letter-spacing:.11em;text-transform:uppercase;
  color:#7a8b9c;margin-bottom:.18em;}
.nightMode .cm2-listen{background:rgba(148,167,186,0.13);border-left-color:#94a7ba;color:#c9d3dd;}
.nightMode .cm2-listen-label{color:#94a7ba;}
"""


def main():
    if "Listen" not in C.anki("modelFieldNames", modelName=M):
        C.anki("modelFieldAdd", modelName=M, fieldName="Listen")
        print("added field Listen")
    else:
        print("field Listen already present")

    tpl = C.anki("modelTemplates", modelName=M)
    changed = {}
    for name in ("AUDIO to COMPOSER", "AUDIO and WORK to COMPOSER"):
        t = tpl.get(name)
        if not t or "cm2-listen" in t["Back"]:
            continue
        # insert immediately after the audio player div on the back
        b = t["Back"]
        anchor = '{{#Audio}}<div class="cm2-audio">{{Audio}}</div>{{/Audio}}'
        if anchor not in b:
            print("   anchor not found in %s -- skipped" % name)
            continue
        changed[name] = {"Front": t["Front"], "Back": b.replace(anchor, anchor + " " + BLOCK, 1)}
    if changed:
        C.anki("updateModelTemplates", model={"name": M, "templates": changed})
        print("wired Listen into: %s" % ", ".join(changed))
    else:
        print("templates already wired")

    css = C.anki("modelStyling", modelName=M)["css"]
    if ".cm2-listen{" not in css:
        C.anki("updateModelStyling", model={"name": M, "css": css.rstrip() + "\n" + CSS})
        print("added .cm2-listen CSS")
    else:
        print("CSS already present")


if __name__ == "__main__":
    main()
