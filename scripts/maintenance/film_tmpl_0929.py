# -*- coding: utf-8 -*-
"""film_tmpl_0929.py -- Film's four card templates rebuilt on the house card anatomy.

Carter, 2026-09-28, on Film: "poorly designed, horrifically inconsistent." Against the other decks:
  * no tier pill at all: the templates relabelled a pill but nothing built one (PA, Photography,
    Music, Art, and Architecture all build theirs from {{Tags}});
  * no zoom: the pictures had a zoom cursor but no zoom script;
  * no scroll-to-answer, which the other decks use to bring a long back's answer into view;
  * the back of CLUE to TITLE repeated the clue at full size and ran straight into the title with no
    divider, so prompt and answer read as one block; TITLE to DIRECTOR drew its divider inline.
Now every back reads: prompt (muted) / divider / answer / credit and meta / pictures / Cast and Detail
sections / tier pill, as the Music and History backs do. The shared scripts are copied from the live
Performing Arts template, so there is one source for them. Film keeps its own accent colour, as each
deck does.

    py -3.9 film_tmpl_0929.py [--apply]
"""
import json, re, sys, time
import concept_add as C

MODEL = "Film"


def shared_scripts():
    t = C.anki("modelTemplates", modelName="Performing Arts")
    back = t["CLUE to WORK"]["Back"] + t["CLUE to WORK"]["Front"]
    out = {}
    for sid in ("qb-zoom", "qb-scroll-answer"):
        m = re.search(r'<script id="%s">.*?</script>' % sid, back, re.S)
        assert m, sid
        out[sid] = m.group(0)
    return out


TIER = """<div id="allowed-tags-container" class="film-tier"></div>
<div id="raw-tags" style="display:none">{{Tags}}</div>
<script id="qb-tier-build">
(function () {
  var pre = "film::tier::", raw = (document.getElementById("raw-tags").innerText || "").trim();
  var box = document.getElementById("allowed-tags-container");
  if (!raw || !box) { return; }
  box.innerHTML = "";
  raw.split(/\\s+/).forEach(function (t) {
    if (t.toLowerCase().indexOf(pre) !== 0) { return; }
    var s = document.createElement("span");
    s.className = "custom-tag";
    s.textContent = t.substring(pre.length);
    box.appendChild(s);
  });
})();
</script>"""

RELABEL = """<script id="qb-tier-label">
(function () {
  var names = {"1": "TIER 1 · CORE", "2": "TIER 2 · SOLID", "3": "TIER 3 · DEEP CUT", "4": "TIER 4 · RARE"};
  Array.prototype.forEach.call(document.querySelectorAll(".custom-tag"), function (e) {
    var m = /tier\\s*([1-4])/i.exec(e.textContent || "");
    if (m) { e.textContent = names[m[1]]; }
  });
})();
</script>"""

FIG = '{{#%s}}<figure class="film-fig">{{%s}}{{#%s caption}}<figcaption>{{%s caption}}</figcaption>{{/%s caption}}</figure>{{/%s}}'
POSTER = '{{#Poster}}<figure class="film-fig film-fig-poster">{{Poster}}{{#Poster caption}}<figcaption>{{Poster caption}}</figcaption>{{/Poster caption}}</figure>{{/Poster}}'


def fig(f):
    return FIG % (f, f, f, f, f, f)


ANSWER = """<div class="film-title"><i>{{Title}}</i></div>
{{#Original title}}<div class="film-orig">{{Original title}}</div>{{/Original title}}
<div class="film-credit">{{#Director}}<b>{{Director}}</b>{{/Director}}{{#Year}}, {{Year}}{{/Year}}</div>
{{#Country}}<div class="film-meta">{{Country}}{{#Movement}} &middot; {{Movement}}{{/Movement}}</div>{{/Country}}"""
SECTIONS = """{{#Cast}}<div class="film-section"><div class="film-label">Cast</div><div class="film-note">{{Cast}}</div></div>{{/Cast}}
{{#Notes}}<div class="film-section"><div class="film-label">Detail</div><div class="film-note">{{Notes}}</div></div>{{/Notes}}"""


def build(S):
    tail = "\n" + RELABEL + "\n" + S["qb-zoom"] + "\n" + S["qb-scroll-answer"]
    open_ = '<div class="qb-card"><div class="qb-panel">\n<div class="qb-eyebrow">%s</div>\n'
    close = "</div></div>"
    T = {}
    T["CLUE to TITLE"] = {
        "Front": "{{^Kind}}{{#Clue}}" + open_ % "Film" + '<div class="film-clue">{{Clue}}</div>\n<div class="film-ask">Title?</div>\n' + close + "{{/Clue}}{{/Kind}}",
        "Back": "{{^Kind}}{{#Clue}}" + open_ % "Film" + '<div class="film-clue film-prompt-back">{{Clue}}</div>\n<hr class="film-divider">\n'
                + ANSWER + '\n<div class="film-gallery">\n' + fig("Still") + "\n" + fig("Still 2") + "\n" + fig("Still 3") + "\n" + POSTER
                + "\n</div>\n" + SECTIONS + "\n" + TIER + "\n" + close + "{{/Clue}}{{/Kind}}" + tail}
    T["STILL to TITLE"] = {
        "Front": "{{^Kind}}{{#Still}}" + open_ % "Film" + '<div class="film-figs">{{Still}}</div>\n<div class="film-ask">Title?</div>\n' + close
                 + "{{/Still}}{{/Kind}}\n" + S["qb-zoom"],
        "Back": "{{^Kind}}{{#Still}}" + open_ % "Film" + '<div class="film-figs">{{Still}}</div>\n{{#Still caption}}<div class="film-cap">{{Still caption}}</div>{{/Still caption}}\n'
                + '<hr class="film-divider">\n' + ANSWER + '\n<div class="film-gallery">\n' + fig("Still 2") + "\n" + fig("Still 3") + "\n" + POSTER
                + "\n</div>\n" + SECTIONS + "\n" + TIER + "\n" + close + "{{/Still}}{{/Kind}}" + tail}
    T["TITLE to DIRECTOR"] = {
        "Front": "{{^Kind}}{{^DirectorTells}}{{#Director}}" + open_ % "Film"
                 + '<div class="film-title"><i>{{Title}}</i></div>\n{{#Original title}}<div class="film-orig">{{Original title}}</div>{{/Original title}}\n'
                 + '{{#Year}}<div class="film-meta">{{Year}}{{#Country}} &middot; {{Country}}{{/Country}}</div>{{/Year}}\n<div class="film-ask">Director?</div>\n'
                 + close + "{{/Director}}{{/DirectorTells}}{{/Kind}}",
        "Back": "{{^Kind}}{{^DirectorTells}}{{#Director}}" + open_ % "Film"
                + '<div class="film-title film-prompt-back"><i>{{Title}}</i></div>\n{{#Original title}}<div class="film-orig">{{Original title}}</div>{{/Original title}}\n'
                + '{{#Year}}<div class="film-meta">{{Year}}{{#Country}} &middot; {{Country}}{{/Country}}</div>{{/Year}}\n<hr class="film-divider">\n'
                + '<div class="film-answer">{{Director}}</div>\n{{#Movement}}<div class="film-meta">{{Movement}}</div>{{/Movement}}\n'
                + '{{#Notes}}<div class="film-section"><div class="film-label">Detail</div><div class="film-note">{{Notes}}</div></div>{{/Notes}}\n'
                + TIER + "\n" + close + "{{/Director}}{{/DirectorTells}}{{/Kind}}" + "\n" + RELABEL + "\n" + S["qb-scroll-answer"]}
    T["FIGURE to NAME"] = {
        "Front": "{{#Kind}}" + open_ % "Film" + '<div class="film-clue">{{Clue}}</div>\n<div class="film-ask">{{Kind}}?</div>\n' + close + "{{/Kind}}",
        "Back": "{{#Kind}}" + open_ % "{{Kind}}" + '<div class="film-clue film-prompt-back">{{Clue}}</div>\n<hr class="film-divider">\n'
                + '<div class="film-answer">{{Title}}</div>\n{{#Year}}<div class="film-meta">{{Year}}{{#Country}} &middot; {{Country}}{{/Country}}</div>{{/Year}}\n'
                + '{{#Picture}}<div class="film-figs film-portrait">{{Picture}}</div>{{#Caption}}<div class="film-cap">{{Caption}}</div>{{/Caption}}{{/Picture}}\n'
                + '{{#Works}}<div class="film-section"><div class="film-label">Key films</div><div class="film-note">{{Works}}</div></div>{{/Works}}\n'
                + '{{#Notes}}<div class="film-section"><div class="film-label">Detail</div><div class="film-note">{{Notes}}</div></div>{{/Notes}}\n'
                + TIER + "\n" + close + "{{/Kind}}" + tail}
    return T


CSS_ADD = """
/* film_tmpl_0929: prompt, divider, answer, sections -- the anatomy the Music and History backs use */
.film-prompt-back { color: var(--muted) !important; font-size: 16.5px !important; line-height: 1.55 !important; }
.film-title.film-prompt-back { font-size: 22px !important; }
.film-divider { border: none; border-top: 1px solid var(--border); margin: 22px auto 20px; max-width: 580px; }
.film-answer {
  font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif;
  font-size: 29px; font-weight: 700; color: var(--ink); line-height: 1.35; }
.film-section { margin: 20px auto 0; max-width: 580px; padding-top: 14px; border-top: 1px solid var(--border); }
.film-section .film-label { margin: 0 0 4px; }
.film-portrait { margin-top: 20px; }
.film-portrait img { max-height: 320px !important; }
.film-gallery:empty { display: none; }
.film-figs img { border-radius: 0 !important; border: 1px solid #000 !important; }
.film-cap { font-style: normal !important; }  /* like the gallery captions, so an italic title inside shows */
@media (max-width: 480px) { .film-answer { font-size: 25px; } }
/* /film_tmpl_0929 */
"""

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    S = shared_scripts()
    T = build(S)
    cur = C.anki("modelTemplates", modelName=MODEL)
    css = C.anki("modelStyling", modelName=MODEL)["css"]
    assert set(T) == set(cur), (set(T), set(cur))
    for k in T:
        print(k, len(cur[k]["Front"]), "->", len(T[k]["Front"]), "|", len(cur[k]["Back"]), "->", len(T[k]["Back"]))
    if "--apply" in sys.argv:
        json.dump({"templates": cur, "css": css}, open("templates_backup/film_tmpl_0929_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w",
                                                    encoding="utf-8"), ensure_ascii=False)
        C.anki("updateModelTemplates", model={"name": MODEL, "templates": T})
        css = re.sub(r"\n/\* film_tmpl_0929:.*?/\* /film_tmpl_0929 \*/\n", "", css, flags=re.S)   # replace, never stack
        C.anki("updateModelStyling", model={"name": MODEL, "css": css + CSS_ADD})
        print("applied")
