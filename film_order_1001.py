# -*- coding: utf-8 -*-
"""film_order_1001.py -- every Film note is introduced by its own card before its clue cards.

Carter, 2026-10-01: "fix the insertion so that the first card for a note that gets studied is the film / actor
itself, so that im not starting with random facts/details before i know what the film even is".

Why it happened: all decks share the Default options preset, which gathers new cards as random individual
cards (newGatherPriority 4) and then sorts them by card type (newSortOrder 0). CLUE to TITLE is card type 1,
so a day's new cards opened on clues from films never seen, and a film's siblings arrived in any order.

Now:
  * Film gets its own preset, "Film -- intro first", cloned from Default: new cards gathered in position order
    and shown in the order gathered, with new siblings buried, so a note's next card comes on a later day.
    The other decks keep Default unchanged.
  * Every new Film card is re-positioned. Notes keep a random order (the variety random gathering gave),
    and within a note: the intro card first -- TITLE to DIRECTOR, which names the film (or, for actors and
    directors, NAME to KEY FILMS, which names the person) -- then the still, then the clue.
  * The intro cards film_tmpl_1001.py created for actor and director notes start suspended where the note's
    other cards are (tier 2 and below).
Re-run after adding Film notes; new notes are otherwise placed at the end with their clue card first.

    py -3.9 film_order_1001.py [--apply]
"""
import json, random, sys, time
import concept_add as C

PRESET = "Film -- intro first"
RANK = {2: 0, 1: 1, 0: 2, 3: 3}          # TITLE to DIRECTOR / NAME to KEY FILMS, STILL, CLUE, FIGURE to NAME
START = 1                                # below Anki's counter, so Film notes added later queue after these


def preset():
    cfg = C.anki("getDeckConfig", deck="Film")
    if cfg["name"] == PRESET:
        return cfg, False
    new_id = C.anki("cloneDeckConfigId", name=PRESET, cloneFrom=cfg["id"])
    C.anki("setDeckConfigId", decks=["Film"], configId=new_id)
    return C.anki("getDeckConfig", deck="Film"), True


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cards = C.anki("cardsInfo", cards=C.anki("findCards", query='"note:Film"'))
    by = {}
    for c in cards:
        by.setdefault(c["note"], []).append(c)
    # 1. intro cards of suspended actor and director notes start suspended
    sus = [c["cardId"] for cs in by.values() for c in cs
           if c["ord"] == 2 and c["queue"] == 0 and c["type"] == 0
           and any(s["ord"] == 3 for s in cs) and all(s["queue"] == -1 for s in cs if s["ord"] == 3)]
    # 2. positions: notes in a fixed random order, the intro card first within each
    notes = sorted(by)
    random.Random(20261001).shuffle(notes)
    pos, plan = START, []
    for nid in notes:
        new = sorted((c for c in by[nid] if c["type"] == 0), key=lambda c: RANK[c["ord"]])
        for c in new:
            if c["due"] != pos:
                plan.append((c["cardId"], c["due"], pos))
            pos += 1
    print("intro cards to suspend:", len(sus), "| new cards to re-position:", len(plan), "of", sum(1 for c in cards if c["type"] == 0))
    cfg = C.anki("getDeckConfig", deck="Film")
    print("Film preset now:", cfg["name"], {k: cfg.get(k) for k in ("newGatherPriority", "newSortOrder")}, "bury new:", cfg["new"]["bury"])
    if "--apply" in sys.argv:
        json.dump({"cfg": cfg, "due": {str(c): d for c, d, _ in plan}, "suspended": sus},
                  open("backups/film_order_1001_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        if sus:
            C.anki("suspend", cards=sus)
        for cid, _, p in plan:
            C.anki("setSpecificValueOfCard", card=cid, keys=["due"], newValues=[p])
        cfg, made = preset()
        cfg["newGatherPriority"] = 1      # lowest position first
        cfg["newSortOrder"] = 1           # in the order gathered
        cfg["new"]["bury"] = True         # bury new siblings: a note's next card comes another day
        C.anki("saveDeckConfig", config=cfg)
        cfg = C.anki("getDeckConfig", deck="Film")
        print("applied; preset", cfg["name"], "(new)" if made else "", {k: cfg.get(k) for k in ("newGatherPriority", "newSortOrder")},
              "bury new:", cfg["new"]["bury"])
