# -*- coding: utf-8 -*-
"""arch_front_0928.py -- take the hidden answer off the Architecture DEFINITION to NAME front.

Audit: "Architecture DEFINITION fronts carry the answer in a hidden div. It is invisible, but
fragile." Carter, 2026-09-28: "ok, correct this." The div (#qb-front-caps, holding the captions
and <b id="qb-front-name">{{Name}}</b>) fed one script, qb-front-caps-js, which labelled front
pictures by work name unless the label contained part of the answer. That script already did
nothing: it exits unless the page has an .arch-concept-eyebrow element, and the template no longer
has one. Both the hidden div and the dead script are removed, so the answer is not on the front at
all and nothing visible changes.

    py -3.9 arch_front_0928.py [--apply]
"""
import json, re, sys, time
import concept_add as C

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t = C.anki("modelTemplates", modelName="Architecture")
    f = t["DEFINITION to NAME"]["Front"]
    assert "arch-concept-eyebrow\"" not in f.replace('querySelector(".arch-concept-eyebrow")', "")
    nf, a = re.subn(r'\n<div id="qb-front-caps" style="display:none">.*?</b></div>', "", f, flags=re.S)
    nf, b = re.subn(r'\n<script id="qb-front-caps-js">.*?</script>\n', "\n", nf, flags=re.S)
    print("hidden div removed:", a, "| script removed:", b, "| {{Name}} left on front:", "{{Name}}" in nf)
    if "--apply" in sys.argv and a == b == 1:
        json.dump(t, open("templates_backup/arch_front_0928_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        C.anki("updateModelTemplates", model={"name": "Architecture", "templates": {"DEFINITION to NAME": {"Front": nf, "Back": t["DEFINITION to NAME"]["Back"]}}})
        print("applied")
