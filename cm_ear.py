# -*- coding: utf-8 -*-
"""cm_ear.py [--dry|--apply] -- make the audio load-bearing, and interleave composers.

Carter: "i am essentially just associating the names of pieces with artists, which
is effective, but i dont learn anything about the era, style, or most importantly
the actual *piece*. they all sound the same to me. is this just a matter of time
on task?"

No. Two measured reasons, neither of which more drilling fixes.

1. THE DECK NEVER ASKS HIM TO LISTEN. `AUDIO to COMPOSER` -- audio alone on the
   front -- has 1428 cards and **0 active**. The only active work card is
   `AUDIO and WORK to COMPOSER`, which prints the title next to the player. The
   title alone answers it, so the audio is decoration. Every correct answer he
   has ever given on this deck was given by reading, not by hearing. A cue that
   is never required is a cue that is never learned (cue overshadowing: when one
   cue is sufficient, the others are not encoded).

2. THE QUEUE MASSES COMPOSERS. Measured on his live new-card queue: mean run of
   2.1 consecutive cards by the same composer, **longest run 20** -- twenty
   Beethovens in a row, then four Chopins. Massing is what makes everything
   "sound the same": hearing twenty Beethovens back to back teaches the sound of
   "orchestra", not the sound of Beethoven. Interleaving excerpts by different
   composers is the manipulation that produces the ability to classify *unheard*
   pieces by those composers (Wong, Roark et al. 2020); massing does not.

So: unsuspend the ear card for tier1, and reposition the new queue so no two
adjacent cards share a composer.
"""
import collections
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import concept_add as C

Q = 'note:"Classical Music"'


def interleave(seq, key):
    """Greedy: repeatedly take from the largest remaining group whose key differs
    from the one just placed. Guarantees no adjacent repeat when feasible."""
    groups = collections.defaultdict(list)
    for x in seq:
        groups[key(x)].append(x)
    out, last = [], None
    while groups:
        cands = [k for k in groups if k != last] or list(groups)
        k = max(cands, key=lambda k: len(groups[k]))
        out.append(groups[k].pop())
        if not groups[k]:
            del groups[k]
        last = k
    return out


def main():
    dry = "--apply" not in sys.argv
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query=Q))
    by_id = {n["noteId"]: n for n in ns}

    # ---- 1. the ear card, for tier1 works that actually have audio ----
    ear = set(C.anki("findCards", query=Q + ' card:"AUDIO to COMPOSER"'))
    live = set(C.anki("findCards", query="deck:\"Classical Music\" -is:suspended"))
    want = []
    for n in ns:
        if "Music::tier::tier1-core" not in n["tags"]:
            continue
        if C.plain(n["fields"]["Kind"]["value"]).strip():
            continue                      # composer/concept notes, not pieces
        if not C.plain(n["fields"]["Audio"]["value"]).strip():
            continue                      # nothing to hear
        want += [c for c in n["cards"] if c in ear and c not in live]
    print("tier1 pieces with audio, ear card currently suspended: %d" % len(want))

    # ---- 2. interleave the new queue by composer ----
    newc = C.anki("findCards", query='deck:"Classical Music" is:new -is:suspended')
    info = []
    for i in range(0, len(newc), 500):
        info += C.anki("cardsInfo", cards=newc[i:i + 500])
    if not dry:
        # the ear cards we are about to unsuspend join the queue too
        info += C.anki("cardsInfo", cards=want)
    dues = sorted(c.get("due", 0) for c in info)

    def comp(c):
        n = by_id.get(c["note"])
        return C.plain(n["fields"]["Composer"]["value"]) if n else "?"

    order = interleave(info, comp)
    runs, cur = [], 1
    cs = [comp(c) for c in order]
    for a, b in zip(cs, cs[1:]):
        cur = cur + 1 if a == b else (runs.append(cur) or 1)
    runs.append(cur)
    print("new queue: %d cards" % len(order))
    print("   longest same-composer run after interleave: %d (was 20)" % max(runs))
    print("   first 12: %s" % ", ".join(c[:18] for c in cs[:12]))

    if dry:
        print("\n-- dry run --")
        return

    if want:
        for i in range(0, len(want), 500):
            C.anki("unsuspend", cards=want[i:i + 500])
        print("\nunsuspended %d ear cards" % len(want))

    # rewrite due positions in interleaved order, reusing the existing slots
    for i in range(0, len(order), 200):
        chunk = order[i:i + 200]
        C.anki("setDueOrder" if False else "setSpecificValueOfCard",
               card=chunk[0]["cardId"], keys=[], newValues=[]) if False else None
    # AnkiConnect exposes repositioning via the scheduler action:
    C.anki("setDueOrder") if False else None
    ids = [c["cardId"] for c in order]
    for i in range(0, len(ids), 500):
        C.anki("setDueOrder", cards=ids[i:i + 500]) if False else None
    try:
        C.anki("setSpecificValueOfCard", card=ids[0], keys=["due"],
               newValues=[str(dues[0])])
        ok = True
    except Exception as e:
        ok = False
        print("   setSpecificValueOfCard unavailable: %s" % e)
    if ok:
        for cid, due in zip(ids, dues):
            C.anki("setSpecificValueOfCard", card=cid, keys=["due"],
                   newValues=[str(due)], warning_check=True)
        print("repositioned %d new cards into interleaved order" % len(ids))

    print("\nactive Classical Music cards: %d"
          % len(C.anki("findCards", query='deck:"Classical Music" -is:suspended')))


if __name__ == "__main__":
    main()
