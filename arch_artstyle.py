# -*- coding: utf-8 -*-
"""arch_artstyle.py -- Architecture building cards laid out like the Art deck.

Carter (2026-09-25): "would it make more sense to have it be exactly like the art
deck in terms of style/layout?" ... "yes do it."

What changes on the four building cards (PICTURE to NAME, PICTURE and NAME to
LOCATION / STYLE, WORK to ARCHITECT):
  * one centred column in Art's order: name large, then architect, "- date -",
    style, location, description, Detail -- no labelled four-column grid
  * the field the card asks for keeps its place in that order but is set large
    and dark (as Art sets the artist), so every card reads the same way
  * the "Show details" fold is gone: Art shows its text directly
  * pictures: Art's natural-proportion figures, no grey matte tiles
  * palette and type from Art (#f7f3ea paper, Optima / Century Gothic)
Kept: the class names the scroll-to-answer script looks for (.arch-name,
.arch-focus-box), the tier tag and every script. DEFINITION to NAME is left to
its own concept layout, which Art also has.

    py -3.9 arch_artstyle.py --dry | --apply
"""
import json
import re
import sys
import time

import concept_add as C

M = "Architecture"
START = '{{^Kind}}<div class="arch-card"><div class="arch-panel">'
TIER = '<div id="allowed-tags-container" class="arch-tier"></div>'
NAME = ('<div class="arch-name">\n<div>{{#Foreign}}<i>{{Name}}</i>{{/Foreign}}{{^Foreign}}{{Name}}'
        '{{/Foreign}}</div>\n{{#Alternate}}<div class="arch-synonym">{{Alternate}}</div>{{/Alternate}}\n</div>\n')
LINES = [("Architect", "arch2-architect", "{{Architect}}"),
         ("Date", "arch2-date", "&mdash; {{Date}} &mdash;"),
         ("Main style", "arch2-sub", "{{Main style}}"),
         ("Location", "arch2-sub", "{{Location}}")]
TEXT = ('{{#Description}}<div class="arch2-desc">{{Description}}</div>{{/Description}}\n'
        '{{#Notes}}<div class="arch2-label">Detail</div><div class="arch2-desc">{{Notes}}</div>{{/Notes}}\n')
ASKS = {"PICTURE to NAME": None, "PICTURE and NAME to LOCATION": "Location",
        "PICTURE and NAME to STYLE": "Main style", "WORK to ARCHITECT": "Architect"}
# what each back reveals, as the Art deck does (Carter: "the art deck doesnt reveal
# all info for every card type, try to only output the information relevant to
# what is being asked"): identifying the building shows everything, like Art's
# ARTWORK to TITLE; the other cards show the name, the answer, and only the text
# that bears on it
SHOW = {"PICTURE to NAME": ("Architect", "Date", "Main style", "Location", "Description", "Notes"),
        "PICTURE and NAME to LOCATION": ("Location",),
        "PICTURE and NAME to STYLE": ("Main style", "Architect", "Description"),
        "WORK to ARCHITECT": ("Architect", "Notes")}

CSS = r"""
/* ---- Art-deck layout (arch_artstyle.py, 2026-09-25) ---- */
:root, :root.night_mode, :root.nightMode, .night_mode, .nightMode, .card,
.night_mode .card, .nightMode .card, .night_mode html, .night_mode body,
.nightMode html, .nightMode body {
  --bg: #f7f3ea; --panel: #f7f3ea; --border: #d8d0c0; --ink: #2b2b2b;
  --muted: #706a61; --accent: #6b4c3b; --accent-soft: transparent;
}
html, body, .card { background-color: #f7f3ea !important; }
.card { font-family: Optima, "Century Gothic", sans-serif; color: #2b2b2b; }
.arch-card { max-width: 700px; padding: 10px 20px; }
.arch-panel { text-align: center; padding: 0 0 12px; }
.arch2-rule { border: none; border-top: 1px solid #d8d0c0; width: 60%; margin: 20px auto; }
.arch-name { margin-top: 0; }
.arch-name > div:first-child { font-family: Optima, "Century Gothic", sans-serif;
  font-size: 27px; font-weight: 600; color: #2b2b2b; line-height: 1.3; }
.arch-synonym { font-family: Optima, "Century Gothic", sans-serif; font-size: 17px;
  color: #706a61; margin-top: 4px; letter-spacing: 0; }
.arch2-architect { font-size: 22px; color: #2b2b2b; margin-top: 10px; }
.arch2-date { font-size: 19px; color: #2b2b2b; letter-spacing: 1px; }
.arch2-sub { font-size: 18px; color: #706a61; }
.arch-focus-box, .arch-focus-box.arch2-sub, .arch-focus-box.arch2-date {
  background: none !important; border: 0 !important; border-radius: 0 !important;
  padding: 0 !important; margin: 6px 0 0 !important;
  font-size: 24px !important; font-weight: 600; color: #6b4c3b !important; letter-spacing: 0; }
.arch2-desc { font-size: 17px; line-height: 1.5; color: #2b2b2b; max-width: 620px;
  margin: 18px auto 0; text-align: center; }
.arch2-label { font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  color: #706a61; margin: 18px auto -12px; }
.arch-figs, .arch-concept-figs { display: flex !important; flex-wrap: wrap; justify-content: center;
  align-items: flex-start; gap: 6px 10px; margin: 6px 0 16px; grid-template-columns: none !important; }
.arch-fig, .arch-figs figure.arch-fig { background: none !important; aspect-ratio: auto !important;
  width: auto !important; height: auto !important; padding: 0 !important; border: 0 !important; }
.arch-fig figcaption { color: #6e675c; font-size: 13.5px; }
.arch-tier { text-align: center; }
"""


FIT = """
/* proportion-safe pictures (2026-09-25): a fixed 260px height made a wide photo
   on a phone shrink inside a white letterbox; cap the height instead */
.arch-figs img, .arch-concept-figs img, .arch-fig img {
  height: auto !important; max-height: 260px !important; width: auto !important; max-width: 100% !important; }
.arch-figs > figure:only-child img, .arch-concept-figs > figure:only-child img,
.arch-figs > img:only-child { max-height: 50vh !important; }
.arch-fig { max-width: 100%; }
"""


def rebuild(back, asks, figs_last, show):
    i, j = back.index(START) + len(START), back.index(TIER)
    body = back[i:j]
    m = re.search(r"\{\{#Picture 1\}\}<div class=\"arch-figs\">.*?</div>\{\{/Picture 1\}\}", body, re.S)
    figs = m.group(0)
    out = [] if figs_last else [figs + "\n", '<hr class="arch2-rule">\n']
    out.append(NAME)
    # fields in the card's own order; the answer gets a rule above it, as on
    # every back since the 2026-09-25 spacing pass
    lines = {f: (c, i) for f, c, i in LINES}
    for field in [f for f in show if f in lines]:
        cls, inner = lines[field]
        if field == asks:
            cls = "arch-focus-box " + cls
            out.append('<hr class="arch2-rule arch2-rule-answer">\n')
        out.append("{{#%s}}<div class=\"%s\">%s</div>{{/%s}}\n" % (field, cls, inner, field))
    if "Description" in show:
        out.append('{{#Description}}<div class="arch2-desc">{{Description}}</div>{{/Description}}\n')
    if "Notes" in show:
        out.append('{{#Notes}}<div class="arch2-label">Detail</div><div class="arch2-desc">{{Notes}}</div>{{/Notes}}\n')
    if figs_last:
        # no rule before pictures that close the card (Carter: "dont need a
        # separating line before images")
        out.append('<div class="arch2-figs-end">' + figs + "</div>\n")
    return back[:i] + "\n" + "".join(out) + "\n" + back[j:]


def main():
    t = C.anki("modelTemplates", modelName=M)
    css = C.anki("modelStyling", modelName=M)["css"]
    new = {}
    for name, asks in ASKS.items():
        b = t[name]["Back"]
        assert b.count(START) == 1 and b.count(TIER) == 1, name
        new[name] = {"Back": rebuild(b, asks, name == "WORK to ARCHITECT", SHOW[name])}
        print(name, "rebuilt; asks", asks)
    if "--apply" in sys.argv:
        json.dump({"templates": t, "css": css},
                  open("templates_backup/architecture_before_artstyle_apply_%s.json" % time.strftime("%Y%m%d_%H%M"),
                       "w", encoding="utf-8"), ensure_ascii=False)
        C.anki("updateModelTemplates", model={"name": M, "templates": new})
        if "arch_artstyle.py" not in css:
            C.anki("updateModelStyling", model={"name": M, "css": css + CSS})
            css = css + CSS
        if "proportion-safe" not in css:
            C.anki("updateModelStyling", model={"name": M, "css": css + FIT})
        print("applied")
    else:
        print(new["PICTURE and NAME to LOCATION"]["Back"][:1800])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
