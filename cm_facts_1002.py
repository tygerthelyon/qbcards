# -*- coding: utf-8 -*-
"""cm_facts_1002.py -- Carter, 2026-10-02: Music facts, "yes please verify they are all correct".

Every work note's Period, Date, Composer Dates, Nationality, Genre, Hint, and period/genre tags cross-checked
(scratchpad period_check.py, facts_check2.py):
- Period on the card was consistent per composer except Debussy, filed Romantic while Ravel and Satie were Modern.
  Debussy goes with them, as the usual start of 20th-century music (Impressionism is taught as early modern).
- The hidden period tags disagreed with the field on 150 notes (Schubert tagged classical, Mahler/Strauss/Puccini/
  Rachmaninoff modern, postwar operas contemporary): every tag now matches the field.
- Seven operas carried their premiere year, after the composer's death (Prince Igor 1890, Borodin d. 1887), under a
  hint that says "Composed": now their composition years.
- Four works had no date; Peer Gynt suite hints said 1875 (the incidental music) on cards for the 1888/1891 suites.
- Genre tags plainly wrong for the work (Lohengrin, Swan Lake, Prélude à l'après-midi d'un faune as "piano-miniature";
  the Hungarian and Slavonic Dances, Danse macabre, Jeux d'eau as "ballet"; Lieder ohne Worte as "song") replaced by the
  Genre field's tag. Tags that name the excerpt ("overture" on an opera whose clip is its overture) stay.
Composer dates and nationality were already the same on every note of a composer.

    py -3.9 cm_facts_1002.py [--apply]
"""
import json
import os
import re
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
DATES = {   # composition, not premiere
    "Prince Igor": "1869–1887", "Khovanshchina": "1872–1880", "Moses und Aron": "1930–1932",
    "From the House of the Dead": "1927–1928", "Ariane": "1958", "The Greek Passion": "1954–1959", "Le roi Arthus": "1886–1895",
}
UNDATED = {1787711405560: "1830", 1787711405568: "1838", 1787711405572: "1832", 1787711405964: "1790"}
DEBUSSY = "Claude Debussy"
# (Genre field, wrong genre tag) -> right tag
GENRE_FIX = {("Opera", "piano-miniature"): "opera", ("Ballet", "piano-miniature"): "ballet",
             ("Orchestral", "piano-miniature"): "orchestral", ("Suite", "piano-miniature"): "suite", ("Orchestral", "ballet"): "orchestral",
             ("Tone poem", "ballet"): "tone-poem", ("Solo piano", "ballet"): "piano-miniature", ("Solo piano", "song"): "piano-miniature",
             ("Orchestral", "keyboard"): "orchestral", ("Keyboard", "chamber"): "keyboard", ("Suite", "ballet"): "suite",
             ("Chamber", "orchestral"): "chamber", ("Incidental music", "ballet"): "suite"}


def set_hint(h, key, val):
    if re.search(r"%s=[^|]*" % key, h):
        return re.sub(r"%s=[^|]*" % key, "%s=%s" % (key, val), h)
    return h + ("|" if h else "") + "%s=%s" % (key, val)


def main(apply):
    ids = C.anki("findNotes", query='note:"Classical Music"')
    notes = []
    for i in range(0, len(ids), 400):
        notes += C.anki("notesInfo", notes=ids[i:i + 400])
    fields, add, rem, backup = {}, {}, {}, {}
    for n in notes:
        f = {k: v["value"] for k, v in n["fields"].items()}
        if C.plain(f["Kind"]).strip():
            continue
        nid, work, comp = n["noteId"], C.plain(f["Work"]).strip(), C.plain(f["Composer"]).strip()
        new = {}
        period = C.plain(f["Period"]).strip()
        if comp == DEBUSSY and period == "Romantic":
            period = new["Period"] = "Modern"
        date = C.plain(f["Date"]).strip()
        if work in DATES and date != DATES[work]:
            date = new["Date"] = DATES[work]
        if nid in UNDATED and not date:
            date = new["Date"] = UNDATED[nid]
        h = f["Hint"]
        # a hint key is corrected where the hint has it, never added (a date field with a note in brackets would leak)
        h2 = set_hint(h, "Period", period) if period and "Period=" in h else h
        if date and ("Composed=" in h or nid in UNDATED):
            h2 = set_hint(h2, "Composed", date)
        genre = C.plain(f["Genre"]).strip()
        if genre and "Genre=" in h:
            h2 = set_hint(h2, "Genre", genre)
        if h2 != h:
            new["Hint"] = h2
        tags = n["tags"]
        want_p = "Music::period::%s" % period.lower()
        old_p = [t for t in tags if "::period::" in t]
        if period and old_p != [want_p]:
            rem.setdefault(nid, []).extend(t for t in old_p if t != want_p)
            if want_p not in old_p:
                add.setdefault(nid, []).append(want_p)
        for t in [t for t in tags if "::genre::" in t]:
            fix = GENRE_FIX.get((genre, t.split("::")[-1]))
            if fix:
                rem.setdefault(nid, []).append(t)
                if "Music::genre::%s" % fix not in tags:
                    add.setdefault(nid, []).append("Music::genre::%s" % fix)
        if new:
            fields[nid] = new
            backup[nid] = {k: f[k] for k in new}
    for nid, new in list(fields.items())[:40]:
        print(nid, {k: (backup[nid][k][:50], v[:50]) for k, v in new.items()})
    print(len(fields), "notes with field changes;", len(add), "notes gaining tags;", len(rem), "losing tags")
    tagchg = collections_count(add, rem)
    print("tag changes:", tagchg)
    if not apply:
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump({"fields": backup, "tags": {str(n["noteId"]): n["tags"] for n in notes if n["noteId"] in add or n["noteId"] in rem}},
              open(os.path.join(HERE, "backups", "cm_facts_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    for nid, new in fields.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": new})
    for nid, ts in rem.items():
        C.anki("removeTags", notes=[nid], tags=" ".join(sorted(set(ts))))
    for nid, ts in add.items():
        C.anki("addTags", notes=[nid], tags=" ".join(sorted(set(ts))))
    print("applied")


def collections_count(add, rem):
    import collections
    c = collections.Counter()
    for nid in set(add) | set(rem):
        c[(tuple(sorted(set(rem.get(nid, [])))), tuple(sorted(set(add.get(nid, [])))))] += 1
    return {"%s -> %s" % ("+".join(t.split("::")[-1] for t in r) or "-", "+".join(t.split("::")[-1] for t in a) or "-"): k
            for (r, a), k in c.most_common(25)}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
