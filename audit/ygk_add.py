# -*- coding: utf-8 -*-
"""ygk_add.py -- add the 10 NAQT "You Gotta Know" gap notes from audit/ygk_more.json (Anki must be open).

    py -3.9 audit\\ygk_add.py                        dry run: what would be added
    py -3.9 audit\\ygk_add.py --apply                add the notes
    py -3.9 audit\\ygk_add.py --apply --unsuspend-metaphysical
                                                     also unsuspend the Metaphysical art movement note

Adds 2 Performing Arts FIGURE notes (Buddy Rich, Pierre Beauchamp) and 8 Art FIGURE notes (Frans Hals,
Judith Leyster, Anthony van Dyck, Lorenzo Ghiberti, Gutzon Borglum, Phidias, Daniel Chester French,
Frédéric-Auguste Bartholdi). No pictures: add one by hand later if you want a picture on the back.

Each note gets the deck's usual tags plus a tier and `...::ygk_2026-10-05`. As the house rule says only
tier-1 cards are active, the new cards of non-tier-1 notes are suspended straight away. A note is
skipped if one with the same title already exists in that note type. The ids of everything added
go to backups/ygk_add_<timestamp>.json, so the notes can be found (tag:*ygk_2026-10-05) and deleted.
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STAMP = "ygk_2026-10-05"
METAPHYSICAL_NOTE = 1790236438367

# item -> (model, deck, tier, tags, extra fields)
PLAN = {
    "Buddy Rich": ("Performing Arts", "Performing Arts", "tier2-solid",
                   ["PA::discipline::jazz", "PA::era::1910s", "PA::kind::figure", "PA::role::drummer"], {"Kind": "Figure", "Discipline": "jazz"}),
    "Pierre Beauchamp": ("Performing Arts", "Performing Arts", "tier3-deepcut",
                         ["PA::discipline::dance", "PA::era::1630s", "PA::kind::figure", "PA::role::choreographer"], {"Kind": "Figure", "Discipline": "dance"}),
    "Frans Hals": ("Art", "Art", "tier1-core", ["Art::figure", "Art::nationality::dutch"], {}),
    "Judith Leyster": ("Art", "Art", "tier2-solid", ["Art::figure", "Art::nationality::dutch"], {}),
    "Anthony van Dyck": ("Art", "Art", "tier1-core", ["Art::figure", "Art::nationality::flemish"], {}),
    "Lorenzo Ghiberti": ("Art", "Art", "tier1-core", ["Art::figure", "Art::nationality::italian"], {}),
    "Gutzon Borglum": ("Art", "Art", "tier2-solid", ["Art::figure", "Art::nationality::american"], {}),
    "Phidias": ("Art", "Art", "tier1-core", ["Art::figure", "Art::nationality::greek"], {}),
    "Daniel Chester French": ("Art", "Art", "tier2-solid", ["Art::figure", "Art::nationality::american"], {}),
    "Frédéric-Auguste Bartholdi": ("Art", "Art", "tier2-solid", ["Art::figure", "Art::nationality::french"], {}),
}
PREFIX = {"Performing Arts": "PA", "Art": "Art"}


def anki(action, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", data=json.dumps(
        {"action": action, "version": 6, "params": params}).encode(), headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    if r.get("error"):
        raise RuntimeError("%s: %s" % (action, r["error"]))
    return r["result"]


def main():
    apply = "--apply" in sys.argv
    gaps = json.load(open(os.path.join(HERE, "ygk_more.json"), encoding="utf-8"))["gaps"]
    drafts = {g["item"]: g["draft"] for g in gaps if g.get("draft")}
    model_fields = {m: set(anki("modelFieldNames", modelName=m)) for m in set(p[0] for p in PLAN.values())}

    todo = []
    for item, (model, deck, tier, tags, extra) in PLAN.items():
        fields = dict(drafts[item])
        fields.update(extra)
        fields = {k: v for k, v in fields.items() if k in model_fields[model]}
        title_field = "Title"
        dup = anki("findNotes", query='"note:%s" "%s:%s"' % (model, title_field, fields[title_field].replace('"', '\\"')))
        tags = tags + ["%s::tier::%s" % (PREFIX[model], tier), "%s::%s" % (PREFIX[model], STAMP)]
        status = "exists (note %s), skipped" % dup[0] if dup else "add"
        print("%-28s %-16s %-13s %s" % (item, model, tier, status))
        if not dup:
            todo.append((item, model, deck, tier, tags, fields))

    if not apply:
        print("\nDry run. Nothing added. Add --apply to add the %d notes above marked 'add'." % len(todo))
        if "--unsuspend-metaphysical" in sys.argv:
            print("--unsuspend-metaphysical would unsuspend the cards of note %d (Metaphysical art)." % METAPHYSICAL_NOTE)
        return

    added = []
    for item, model, deck, tier, tags, fields in todo:
        nid = anki("addNote", note={"deckName": deck, "modelName": model, "fields": fields, "tags": tags,
                                    "options": {"allowDuplicate": False}})
        cards = anki("findCards", query="nid:%d" % nid)
        if tier != "tier1-core" and cards:
            anki("suspend", cards=cards)
        added.append({"item": item, "note_id": nid, "cards": cards, "suspended": tier != "tier1-core"})
        print("added %s: note %d, %d card(s)%s" % (item, nid, len(cards), ", suspended" if tier != "tier1-core" else ""))

    if "--unsuspend-metaphysical" in sys.argv:
        cards = anki("findCards", query="nid:%d" % METAPHYSICAL_NOTE)
        if cards:
            anki("unsuspend", cards=cards)
            print("unsuspended %d card(s) of note %d (Metaphysical art)" % (len(cards), METAPHYSICAL_NOTE))
        else:
            print("note %d not found; nothing unsuspended" % METAPHYSICAL_NOTE)

    os.makedirs(os.path.join(ROOT, "backups"), exist_ok=True)
    log = os.path.join(ROOT, "backups", "ygk_add_%s.json" % time.strftime("%Y%m%d_%H%M%S"))
    json.dump(added, open(log, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nAdded %d notes. Log: %s\nTo undo: search tag:*%s in the browser and delete them." % (len(added), log, STAMP))


if __name__ == "__main__":
    main()
