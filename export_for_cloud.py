# -*- coding: utf-8 -*-
"""export_for_cloud.py -- dump the collection's text (no media) so a cloud session can work on it.

Writes export/ next to this script:
    export/models.json          every note type: fields, card templates, CSS
    export/notes_<model>.json   every note: id, fields, tags, and its cards
                                (template ord, deck, queue -1 = suspended, interval, reps, lapses)

Nothing in Anki is changed. Media files are not copied; fields keep their <img>/[sound:] tags.
Run with Anki open:

    py -3.9 export_for_cloud.py

Then upload the export/ folder to github.com/tygerthelyon/qbcards (Add file > Upload files,
drag the folder in). Files over 25 MB are split into parts so the web uploader accepts them.
"""
import json, os, sys
import concept_add as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export")
LIMIT = 24 * 1024 * 1024
os.makedirs(OUT, exist_ok=True)


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def safe(name):
    return "".join(c if c.isalnum() else "_" for c in name).strip("_")


def write(path, obj):
    s = json.dumps(obj, ensure_ascii=False, indent=0)
    if len(s.encode("utf-8")) <= LIMIT:
        open(path, "w", encoding="utf-8").write(s)
        return [path]
    # split the note list into parts that each fit
    notes, parts, cur, size = obj["notes"], [], [], 0
    for n in notes:
        b = len(json.dumps(n, ensure_ascii=False).encode("utf-8"))
        if cur and size + b > LIMIT - 4096:
            parts.append(cur); cur, size = [], 0
        cur.append(n); size += b
    parts.append(cur)
    out = []
    for i, p in enumerate(parts, 1):
        q = path.replace(".json", "_part%d.json" % i)
        open(q, "w", encoding="utf-8").write(
            json.dumps(dict(obj, notes=p, part=i, parts=len(parts)), ensure_ascii=False, indent=0))
        out.append(q)
    return out


models = {}
for m in C.anki("modelNames"):
    models[m] = dict(fields=C.anki("modelFieldNames", modelName=m),
                     templates=C.anki("modelTemplates", modelName=m),
                     css=C.anki("modelStyling", modelName=m).get("css", ""))
write(os.path.join(OUT, "models.json"), models)
print("models:", len(models))

for m in models:
    nids = C.anki("findNotes", query='"note:%s"' % m)
    if not nids:
        continue
    notes = []
    for ch in chunks(nids, 500):
        notes += C.anki("notesInfo", notes=ch)
    cids = [c for n in notes for c in n["cards"]]
    cards = {}
    for ch in chunks(cids, 500):
        for c in C.anki("cardsInfo", cards=ch):
            cards[c["cardId"]] = dict(id=c["cardId"], ord=c.get("ord"),
                                      deck=c["deckName"], queue=c["queue"], ivl=c["interval"],
                                      reps=c["reps"], lapses=c["lapses"])
    rows = [dict(id=n["noteId"], tags=n["tags"],
                 fields={k: v["value"] for k, v in n["fields"].items()},
                 cards=[cards[c] for c in n["cards"] if c in cards]) for n in notes]
    paths = write(os.path.join(OUT, "notes_%s.json" % safe(m)), dict(model=m, notes=rows))
    print("%-28s %6d notes %6d cards -> %s" % (m, len(rows), len(cids),
                                               ", ".join(os.path.basename(p) for p in paths)))
print("done:", OUT)
