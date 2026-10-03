# -*- coding: utf-8 -*-
"""film_still_dedupe.py -- STILL to TITLE back showed Still 1 and its caption twice:
once under the question, again as the first figure of the W93 gallery.
Same mechanism as the Art title-back duplicate Carter reported 2026-09-25.
The gallery on this card drops Still 1; the other Film cards keep it.

    py -3.9 film_still_dedupe.py --dry | --apply
"""
import json, sys, time
import concept_add as C

FIG = ('{{#Still}}<figure class="film-fig">{{Still}}{{#Still caption}}<figcaption>'
       '{{Still caption}}</figcaption>{{/Still caption}}</figure>{{/Still}}\n')
t = C.anki("modelTemplates", modelName="Film")
b = t["STILL to TITLE"]["Back"]
print("gallery Still-1 figure:", b.count(FIG))
assert b.count(FIG) == 1
if "--apply" in sys.argv:
    json.dump(t, open("templates_backup/film_before_still_dedupe_%s.json" % time.strftime("%Y%m%d_%H%M"),
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    C.anki("updateModelTemplates", model={"name": "Film", "templates": {
        "STILL to TITLE": {"Back": b.replace(FIG, "")}}})
    print("applied")
