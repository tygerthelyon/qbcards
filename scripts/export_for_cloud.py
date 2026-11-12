"""Export an Anki collection's note fields and models as JSON, without media.

Run with Anki and AnkiConnect open: python scripts/export_for_cloud.py
Output goes to scripts/export/. Review the contents before sharing: notes,
tags, and review metadata may be personal.
"""
import json
from pathlib import Path


OUT = Path(__file__).resolve().parent / "export"
LIMIT = 24 * 1024 * 1024


def chunks(values, size):
    for i in range(0, len(values), size):
        yield values[i:i + size]


def safe(name):
    return "".join(char if char.isalnum() else "_" for char in name).strip("_")


def write(path, obj):
    """Write JSON, splitting large note lists into numbered parts."""
    path = Path(path)
    rendered = json.dumps(obj, ensure_ascii=False, indent=0)
    if len(rendered.encode("utf-8")) <= LIMIT:
        path.write_text(rendered, encoding="utf-8")
        return [path]

    parts, current, size = [], [], 0
    for note in obj["notes"]:
        note_size = len(json.dumps(note, ensure_ascii=False).encode("utf-8"))
        if current and size + note_size > LIMIT - 4096:
            parts.append(current)
            current, size = [], 0
        current.append(note)
        size += note_size
    parts.append(current)

    paths = []
    for i, notes in enumerate(parts, 1):
        part_path = path.with_name("%s_part%d%s" % (path.stem, i, path.suffix))
        payload = dict(obj, notes=notes, part=i, parts=len(parts))
        part_path.write_text(json.dumps(payload, ensure_ascii=False, indent=0), encoding="utf-8")
        paths.append(part_path)
    return paths


def main():
    import concept_add as anki

    OUT.mkdir(parents=True, exist_ok=True)
    models = {}
    for model in anki.anki("modelNames"):
        models[model] = {
            "fields": anki.anki("modelFieldNames", modelName=model),
            "templates": anki.anki("modelTemplates", modelName=model),
            "css": anki.anki("modelStyling", modelName=model).get("css", ""),
        }
    write(OUT / "models.json", models)
    print("models:", len(models))

    for model in models:
        note_ids = anki.anki("findNotes", query='"note:%s"' % model)
        if not note_ids:
            continue
        notes = []
        for group in chunks(note_ids, 500):
            notes.extend(anki.anki("notesInfo", notes=group))
        card_ids = [card for note in notes for card in note["cards"]]
        cards = {}
        for group in chunks(card_ids, 500):
            for card in anki.anki("cardsInfo", cards=group):
                cards[card["cardId"]] = {
                    "id": card["cardId"], "ord": card.get("ord"), "deck": card["deckName"],
                    "queue": card["queue"], "ivl": card["interval"],
                    "reps": card["reps"], "lapses": card["lapses"],
                }
        rows = [
            {"id": note["noteId"], "tags": note["tags"],
             "fields": {key: value["value"] for key, value in note["fields"].items()},
             "cards": [cards[card] for card in note["cards"] if card in cards]}
            for note in notes
        ]
        paths = write(OUT / ("notes_%s.json" % safe(model)), {"model": model, "notes": rows})
        print("%-28s %6d notes %6d cards -> %s" %
              (model, len(rows), len(card_ids), ", ".join(path.name for path in paths)))
    print("done:", OUT)


if __name__ == "__main__":
    main()
