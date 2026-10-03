# -*- coding: utf-8 -*-
"""render_previews.py -- render History v2 cards to HTML the way Anki would, for a visual check.

Writes previews/html/*.html (day and night). Screenshot them with shoot.js (Playwright, phone width).
A small Anki-template emulator: {{Field}}, {{#F}}..{{/F}}, {{^F}}..{{/F}}, {{cloze:Text}}, {{Tags}}.
    python3 render_previews.py [n_per_model]
"""
import html, os, re, sys
import hist_qb_models as M
import hist_qb_apply as A
import cards_china_myth_lit as CARDS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "previews", "html")


def render(tmpl, fields, tags, cloze_ord=None, side="front"):
    def sec(m):
        neg, name, body = m.group(1) == "^", m.group(2), m.group(3)
        has = bool(fields.get(name, "").strip())
        return body if has != neg else ""
    prev = None
    while prev != tmpl:
        prev = tmpl
        tmpl = re.sub(r"\{\{([#^])([^}]+)\}\}(.*?)\{\{/\2\}\}", sec, tmpl, flags=re.S)

    def cloze(text):
        def rep(m):
            n, body = int(m.group(1)), m.group(2)
            if n == cloze_ord:
                return '<span class="cloze">[...]</span>' if side == "front" else '<span class="cloze">%s</span>' % body
            return '<span class="cloze-inactive" data-ordinal="%d">%s</span>' % (n, body)
        return re.sub(r"\{\{c(\d+)::(.*?)\}\}", rep, text)
    tmpl = tmpl.replace("{{cloze:Text}}", cloze(fields.get("Text", "")))
    tmpl = tmpl.replace("{{Tags}}", " ".join(tags))
    return re.sub(r"\{\{([^}#^/]+)\}\}", lambda m: fields.get(m.group(1), ""), tmpl)


def page(body, night):
    cls = "card night_mode" if night else "card"
    return ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<style>%s</style></head><body class="%s"><div class="card">%s</div></body></html>'
            % (M.CSS, "night_mode" if night else "", body))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    os.makedirs(OUT, exist_ok=True)
    models = {m["name"]: m for m in M.MODELS}
    picks, seen = [], {}
    for note in CARDS.NOTES:
        k = note["model"] + ("+pic" if note.get("pic") else "")
        if seen.get(k, 0) < n:
            seen[k] = seen.get(k, 0) + 1
            picks.append(note)
    i = 0
    for note in picks:
        fields, tags = A.build_fields(note, media_dir=os.path.join(HERE, "media"), preview=True)
        m = models[note["model"]]
        for t_i, t in enumerate(m["templates"]):
            ords = [1, 2] if m.get("is_cloze") else [None]
            for o in ords:
                for side in ("front", "back"):
                    tmpl = t["Front"] if side == "front" else t["Back"]
                    body = render(tmpl, fields, tags, o, side)
                    if not re.sub(r"<[^>]+>|\s", "", body) and "<img" not in body:
                        continue
                    for night in (False, True):
                        i += 1
                        name = "%03d_%s_%s_%s%s.html" % (i, note["model"].replace(" ", ""), t["Name"].replace(" ", ""),
                                                         side, "_night" if night else "")
                        open(os.path.join(OUT, name), "w", encoding="utf-8").write(page(body, night))
    print("wrote", i, "pages to", OUT)


if __name__ == "__main__":
    main()
