# -*- coding: utf-8 -*-
"""cm_gaps_add.py -- add the Classical Music gap notes in audit/cm_gaps.json (Anki must be open).

    py -3.9 audit\\cm_gaps_add.py           dry run: what would be added, what is skipped
    py -3.9 audit\\cm_gaps_add.py --apply   add them

99 works that are often asked in quizbowl and had no note in the deck. Each note has the usual fields
(Work, Composer, dates, Date, Period, Genre, Hint, Clue, Description) but NO Audio or Listen yet, so:
  - the AUDIO to COMPOSER card (which would be blank) is suspended on every new note;
  - tier-1 notes keep their AUDIO and WORK to COMPOSER (shows the title) and DESCRIPTION to WORK cards active;
  - tier-2 and tier-3 notes are suspended entirely, as the house rule says.
Add a recording later and unsuspend the audio card by hand if you want it.

A note is skipped if the deck already has the same Work by the same Composer. Tags: the deck's usual
genre/period/tier tags plus Music::gap_2026-10-05, so `tag:Music::gap_2026-10-05` finds them all.
The ids of everything added go to backups/cm_gaps_add_<timestamp>.json.
"""
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODEL = DECK = "Classical Music"
STAMP = "Music::gap_2026-10-05"


def anki(action, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", data=json.dumps(
        {"action": action, "version": 6, "params": params}).encode(), headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    if r.get("error"):
        raise RuntimeError("%s: %s" % (action, r["error"]))
    return r["result"]


def key(work, composer):
    return (re.sub(r"<[^>]+>", "", work).strip().lower(), composer.strip().lower())


def main():
    apply = "--apply" in sys.argv
    notes = json.load(open(os.path.join(HERE, "cm_gaps.json"), encoding="utf-8"))["notes"]
    fields_ok = set(anki("modelFieldNames", modelName=MODEL))
    have = set()
    ids = anki("findNotes", query='note:"%s"' % MODEL)
    for i in range(0, len(ids), 500):
        for n in anki("notesInfo", notes=ids[i:i + 500]):
            have.add(key(n["fields"]["Work"]["value"], n["fields"]["Composer"]["value"]))

    todo, skip = [], []
    for n in notes:
        f = n["fields"]
        bad = set(f) - fields_ok
        if bad:
            raise SystemExit("unknown fields %s -- the note type has changed; stop." % bad)
        (skip if key(f["Work"], f["Composer"]) in have else todo).append(n)
    for n in todo:
        f = n["fields"]
        print("ADD  t%d  %s — %s" % (n["tier"], re.sub(r"<[^>]+>", "", f["Work"]), f["Composer"]))
    for n in skip:
        print("SKIP (already in deck)  %s — %s" % (re.sub(r"<[^>]+>", "", n["fields"]["Work"]), n["fields"]["Composer"]))
    print("\n%d to add, %d skipped." % (len(todo), len(skip)))
    if not apply:
        print("Dry run. Nothing written. Add --apply to add them.")
        return

    log = []
    for n in todo:
        nid = anki("addNote", note={"deckName": DECK, "modelName": MODEL, "fields": n["fields"],
                                    "tags": n["tags"] + [STAMP], "options": {"allowDuplicate": False}})
        cards = anki("cardsInfo", cards=anki("findCards", query="nid:%d" % nid))
        sus = [c["cardId"] for c in cards if n["tier"] != 1 or c["template"] == "AUDIO to COMPOSER"]
        if sus:
            anki("suspend", cards=sus)
        log.append({"note_id": nid, "work": n["fields"]["Work"], "composer": n["fields"]["Composer"],
                    "tier": n["tier"], "suspended_cards": sus})
    os.makedirs(os.path.join(ROOT, "backups"), exist_ok=True)
    bk = os.path.join(ROOT, "backups", "cm_gaps_add_%s.json" % time.strftime("%Y%m%d_%H%M%S"))
    json.dump(log, open(bk, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Added %d notes. Log: %s" % (len(log), bk))


if __name__ == "__main__":
    main()
