# -*- coding: utf-8 -*-
"""film_tmpl_1001.py -- Film's card style brought into line with the other decks, and an intro card for every note.

Carter, 2026-10-01: "also improve the film card style please", and "fix the insertion so that the first card
for a note that gets studied is the film / actor itself, so that im not starting with random facts/details
before i know what the film even is".

Style, against Performing Arts and Photography (rendered side by side at phone width, light and night):
  * the answer was plain black, barely heavier than the muted prompt; it is now the accent colour, as the
    other decks' answers are;
  * director, year, country, and movement ran together as a line of text ("Akira Kurosawa, 1950 / Japan ·
    Jidaigeki"); they are now the labelled facts grid the other decks use, with the movement (often a genre:
    "Horror", "Film noir") as an unlabelled chip, since "Movement: Horror" would be wrong;
  * Cast and Detail were left-aligned under a centred card; they are centred, as in the other decks;
  * the poster filled the phone screen below a full-width still; it is capped smaller;
  * actor and director backs said "DIRECTOR" or "ACTOR" where the front said "FILM"; both say "Film".
Intro card: TITLE to DIRECTOR (the film named, director asked) is the card that says what the film is, so its
back now carries the whole film -- stills, poster, cast, detail -- and film_order_1001.py schedules it first.
For actor and director notes the same template gets a second branch, NAME to KEY FILMS: the person named,
"Known for?" asked, portrait and films on the back. Adding a branch to an existing template creates the
cards without adding a card type, so no full sync is needed.

    py -3.9 film_tmpl_1001.py [--apply]
"""
import json, re, sys, time
import concept_add as C
from film_tmpl_0929 import shared_scripts, TIER, RELABEL, MODEL

OPEN = '<div class="qb-card"><div class="qb-panel">\n<div class="qb-eyebrow">Film</div>\n'
CLOSE = "</div></div>"


def fact(field, label):
    return ('{{#%s}}<div class="film-fact"><div class="film-fact-label">%s</div>'
            '<div class="film-fact-value">{{%s}}</div></div>{{/%s}}' % (field, label, field, field))


TITLE_ANS = ('<div class="film-title film-hit"><i>{{Title}}</i></div>\n'
             '{{#Original title}}<div class="film-orig">{{Original title}}</div>{{/Original title}}')
FACTS = '<div class="film-facts">' + fact("Director", "Director") + fact("Year", "Year") + fact("Country", "Country") + "</div>"
FACTS_NO_DIR = '<div class="film-facts">' + fact("Year", "Year") + fact("Country", "Country") + "</div>"
CHIP = '{{#Movement}}<div class="film-chip">{{Movement}}</div>{{/Movement}}'
FIG = '{{#%s}}<figure class="film-fig%s">{{%s}}{{#%s caption}}<figcaption>{{%s caption}}</figcaption>{{/%s caption}}</figure>{{/%s}}'


def fig(f, extra=""):
    return FIG % (f, extra, f, f, f, f, f)


def gallery(*fields):
    return '<div class="film-gallery">' + "".join(fig(f, " film-fig-poster" if f == "Poster" else "") for f in fields) + "</div>"


def section(field, label):
    return ('{{#%s}}<div class="film-section"><div class="film-label">%s</div><div class="film-note">{{%s}}</div></div>{{/%s}}'
            % (field, label, field, field))


SECTIONS = section("Cast", "Cast") + "\n" + section("Notes", "Detail")
DIVIDER = '<hr class="film-divider">\n'
PORTRAIT = '{{#Picture}}<div class="film-figs film-portrait">{{Picture}}</div>{{#Caption}}<div class="film-cap">{{Caption}}</div>{{/Caption}}{{/Picture}}'
PERSON_FACTS = ('<div class="film-facts">' + fact("Year", "Dates") + fact("Country", "Country") + "</div>")


def build(S):
    tail = "\n" + RELABEL + "\n" + S["qb-zoom"] + "\n" + S["qb-scroll-answer"]
    T = {}
    T["CLUE to TITLE"] = {
        "Front": "{{^Kind}}{{#Clue}}" + OPEN + '<div class="film-clue">{{Clue}}</div>\n<div class="film-ask">Title?</div>\n' + CLOSE + "{{/Clue}}{{/Kind}}",
        "Back": "{{^Kind}}{{#Clue}}" + OPEN + '<div class="film-clue film-prompt-back">{{Clue}}</div>\n' + DIVIDER
                + TITLE_ANS + "\n" + FACTS + "\n" + CHIP + "\n" + gallery("Still", "Still 2", "Still 3", "Poster") + "\n"
                + SECTIONS + "\n" + TIER + "\n" + CLOSE + "{{/Clue}}{{/Kind}}" + tail}
    T["STILL to TITLE"] = {
        "Front": "{{^Kind}}{{#Still}}" + OPEN + '<div class="film-figs">{{Still}}</div>\n<div class="film-ask">Title?</div>\n' + CLOSE
                 + "{{/Still}}{{/Kind}}\n" + S["qb-zoom"],
        "Back": "{{^Kind}}{{#Still}}" + OPEN + '<div class="film-figs">{{Still}}</div>\n{{#Still caption}}<div class="film-cap">{{Still caption}}</div>{{/Still caption}}\n'
                + DIVIDER + TITLE_ANS + "\n" + FACTS + "\n" + CHIP + "\n" + gallery("Still 2", "Still 3", "Poster") + "\n"
                + SECTIONS + "\n" + TIER + "\n" + CLOSE + "{{/Still}}{{/Kind}}" + tail}
    film_intro_front = ('{{^Kind}}{{^DirectorTells}}{{#Director}}' + OPEN
                        + '<div class="film-title"><i>{{Title}}</i></div>\n{{#Original title}}<div class="film-orig">{{Original title}}</div>{{/Original title}}\n'
                        + '{{#Year}}<div class="film-meta">{{Year}}{{#Country}} &middot; {{Country}}{{/Country}}</div>{{/Year}}\n<div class="film-ask">Director?</div>\n'
                        + CLOSE + "{{/Director}}{{/DirectorTells}}{{/Kind}}")
    person_intro_front = ('{{#Kind}}{{#Works}}' + OPEN + '<div class="film-name">{{Title}}</div>\n'
                          + '{{#Year}}<div class="film-meta">{{Year}}{{#Country}} &middot; {{Country}}{{/Country}}</div>{{/Year}}\n'
                          + '<div class="film-ask">Known for?</div>\n' + CLOSE + "{{/Works}}{{/Kind}}")
    film_intro_back = ('{{^Kind}}{{^DirectorTells}}{{#Director}}' + OPEN
                       + '<div class="film-title film-prompt-back"><i>{{Title}}</i></div>\n{{#Original title}}<div class="film-orig">{{Original title}}</div>{{/Original title}}\n'
                       + '{{#Year}}<div class="film-meta">{{Year}}{{#Country}} &middot; {{Country}}{{/Country}}</div>{{/Year}}\n' + DIVIDER
                       + '<div class="film-answer film-hit">{{Director}}</div>\n' + CHIP + "\n" + gallery("Still", "Still 2", "Still 3", "Poster") + "\n"
                       + SECTIONS + "\n" + TIER + "\n" + CLOSE + "{{/Director}}{{/DirectorTells}}{{/Kind}}")
    person_intro_back = ('{{#Kind}}{{#Works}}' + OPEN + '<div class="film-name film-prompt-back">{{Title}}</div>\n'
                         + '{{#Year}}<div class="film-meta">{{Year}}{{#Country}} &middot; {{Country}}{{/Country}}</div>{{/Year}}\n' + DIVIDER
                         + '<div class="film-works film-hit">{{Works}}</div>\n' + PORTRAIT + "\n" + section("Notes", "Detail") + "\n"
                         + TIER + "\n" + CLOSE + "{{/Works}}{{/Kind}}")
    T["TITLE to DIRECTOR"] = {"Front": film_intro_front + person_intro_front,
                              "Back": film_intro_back + person_intro_back + tail}
    T["FIGURE to NAME"] = {
        "Front": "{{#Kind}}" + OPEN + '<div class="film-clue">{{Clue}}</div>\n<div class="film-ask">{{Kind}}?</div>\n' + CLOSE + "{{/Kind}}",
        "Back": "{{#Kind}}" + OPEN + '<div class="film-clue film-prompt-back">{{Clue}}</div>\n' + DIVIDER
                + '<div class="film-name film-hit">{{Title}}</div>\n' + PERSON_FACTS + "\n" + PORTRAIT + "\n"
                + section("Works", "Key films") + "\n" + section("Notes", "Detail") + "\n" + TIER + "\n" + CLOSE + "{{/Kind}}" + tail}
    return T


CSS_ADD = """
/* film_tmpl_1001: answer in the accent colour, a labelled facts grid, centred sections, a smaller poster */
.film-prompt-back { color: var(--muted) !important; font-size: 16.5px !important; line-height: 1.55 !important; }
.film-title.film-prompt-back, .film-name.film-prompt-back { font-size: 22px !important; }
.film-divider { border: none; border-top: 1px solid var(--border); margin: 22px auto 20px; max-width: 580px; }
.film-name { font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif;
  font-size: 27px; font-weight: 700; color: var(--ink); line-height: 1.3; }
.film-answer { font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif;
  font-size: 27px; font-weight: 700; line-height: 1.3; }
.film-hit { color: var(--accent) !important; }
.film-works { font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif;
  font-size: 21px; font-weight: 600; line-height: 1.45; max-width: 30em; margin: 0 auto; }
.film-orig { font-size: 17px !important; margin-top: 4px !important; }
.film-facts { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px 32px; margin: 18px auto 0; max-width: 36em; }
.film-facts:not(:has(.film-fact)) { display: none; }
.film-fact { min-width: 84px; max-width: 240px; }
.film-fact-label { font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.film-fact-value { font-size: 15px; font-weight: 600; line-height: 1.4; color: var(--ink); margin-top: 3px; overflow-wrap: anywhere; }
.film-chip { display: inline-block; margin-top: 14px; padding: 3px 12px; border: 1px solid var(--border); border-radius: 999px;
  font-size: 13px; color: var(--muted); }
.film-section { margin: 20px auto 0; max-width: 34em; padding-top: 14px; border-top: 1px solid var(--border); text-align: center; }
.film-section .film-label { margin: 0 0 6px; text-align: center !important; }
.film-note { text-align: center !important; font-size: 16px !important; line-height: 1.6 !important; }
.film-gallery { margin-top: 20px !important; gap: 12px !important; }
.film-gallery:empty { display: none; }
.film-fig img { max-height: 300px !important; }
.film-fig-poster img { max-height: 230px !important; }
.film-fig figcaption { text-align: center !important; font-size: 12.5px !important; }
.film-portrait { margin-top: 20px; }
.film-portrait img { max-height: 300px !important; }
.film-figs img { border-radius: 0 !important; border: 1px solid #000 !important; }
.film-cap { font-style: normal !important; }
@media (max-width: 480px) { .film-answer, .film-name { font-size: 24px; } .film-works { font-size: 19px; } }
/* /film_tmpl_1001 */
"""

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    S = shared_scripts()
    T = build(S)
    cur = C.anki("modelTemplates", modelName=MODEL)
    css = C.anki("modelStyling", modelName=MODEL)["css"]
    assert set(T) == set(cur), (set(T), set(cur))
    before = len(C.anki("findCards", query='"note:Film"'))
    for k in T:
        print(k, len(cur[k]["Front"]), "->", len(T[k]["Front"]), "|", len(cur[k]["Back"]), "->", len(T[k]["Back"]))
    if "--apply" in sys.argv:
        json.dump({"templates": cur, "css": css}, open("templates_backup/film_tmpl_1001_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w",
                                                      encoding="utf-8"), ensure_ascii=False)
        C.anki("updateModelTemplates", model={"name": MODEL, "templates": T})
        css = re.sub(r"\n/\* film_tmpl_0929:.*?/\* /film_tmpl_0929 \*/\n", "", css, flags=re.S)   # superseded
        css = re.sub(r"\n/\* film_tmpl_1001:.*?/\* /film_tmpl_1001 \*/\n", "", css, flags=re.S)   # replace, never stack
        C.anki("updateModelStyling", model={"name": MODEL, "css": css + CSS_ADD})
        print("applied; Film cards", before, "->", len(C.anki("findCards", query='"note:Film"')))
