# -*- coding: utf-8 -*-
"""fix_0927_templates.py -- two layout faults from the 2026-09-27 recheck.

  Art, ARTWORK to TITLE back: a hard-coded "Title" heading sat above the picture on every
  answer. It is hidden, not removed, so it keeps its line and the picture does not jump when
  the answer is revealed (the front has "Title?" in the same place).
  Film: pictures had rounded corners and no border, unlike every other deck (checklist N1,
  "restore image borders on every deck"). Square corners and the same 1px black border.

    py -3.9 fix_0927_templates.py [--apply]
"""
import json, sys, time
import concept_add as C

OLD = "font-weight: 500;\nletter-spacing: 0.5px'>\nTitle\n</div>"
NEW = "font-weight: 500;\nletter-spacing: 0.5px;\nvisibility: hidden' aria-hidden=\"true\">\nTitle\n</div>"
FILM_CSS = """
/* 2026-09-27: same framing as the other decks -- square corners, 1px black border */
.film-figs img, .film-fig img { border-radius: 0 !important; border: 1px solid #000 !important; box-sizing: border-box; }
"""

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    art = C.anki("modelTemplates", modelName="Art")
    back = art["ARTWORK to TITLE"]["Back"]
    print("Art heading occurrences:", back.count(OLD))
    film_css = C.anki("modelStyling", modelName="Film")["css"]
    print("Film rule present:", "same framing as the other decks" in film_css)
    if "--apply" in sys.argv:
        stamp = time.strftime("%Y%m%d_%H%M")
        json.dump({"Art": art, "Film_css": film_css}, open("templates_backup/fix_0927_templates_%s.json" % stamp, "w", encoding="utf-8"), ensure_ascii=False)
        if back.count(OLD) == 1:
            C.anki("updateModelTemplates", model={"name": "Art", "templates": {"ARTWORK to TITLE": {
                "Front": art["ARTWORK to TITLE"]["Front"], "Back": back.replace(OLD, NEW)}}})
        if "same framing as the other decks" not in film_css:
            C.anki("updateModelStyling", model={"name": "Film", "css": film_css + FILM_CSS})
        print("applied")
