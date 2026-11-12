# -*- coding: utf-8 -*-
"""cm_trim_movements.py -- at most two active AUDIO and WORK cards per work.

Audit 2026-09-26, 1.2: "297 active audio cards cover only 163 works. The
Nutcracker and Peer Gynt are each asked 9 times with the title on the front."
Every movement note of a work asks the same question (the title is on the front,
the answer is the composer), so nine of them is one fact reviewed nine times.

Keeps the two best-known movements active (PREFER, else the first two in movement
order) and suspends the AUDIO and WORK card on the rest. Nothing is deleted; the
notes keep their audio and are tagged Music::trimmed so this can be reversed.

    py -3.9 cm_trim_movements.py --dry | --apply
"""
import collections
import json
import re
import sys
import time

import concept_add as C

CARD = "AUDIO and WORK to COMPOSER"
PREFER = {
    "Peer Gynt": ["Morning Mood", "Hall of the Mountain King"],
    "The Nutcracker": ["Sugar Plum", "Waltz of the Flowers"],
    "Requiem|Mozart": ["Lacrimosa", "Dies Irae"],
    "Swan Lake": ["Scene", "Little Swans"],
    "Die Zauberflöte": ["Hölle Rache", "Overture"],
    "Symphonie fantastique": ["mvt. IV", "mvt. V"],
    "Turandot": ["Nessun dorma", "Act I"],
    "Carnival of the Animals": ["The Swan", "Aquarium"],
    "Requiem|Berlioz": ["Dies Irae", "Lacrimosa"],
    "Requiem|Verdi": ["Requiem aeternam", "Dies Irae - Lacrymosa"],
    "La bohème": ["Aria (Mimi)", "Aria"],
    "Piano Sonata No. 14": ["mvt. I ", "mvt. III"],
    "Symphony No. 5|Beethoven": ["mvt. I ", "mvt. IV"],
    "Symphony No. 9|Beethoven": ["mvt. IV", "mvt. II "],
    "Symphony No. 6|Beethoven": ["mvt. I ", "mvt. IV"],
    "Symphony No. 9|Dvořák": ["mvt. II ", "mvt. IV"],
    "Eine kleine Nachtmusik": ["mvt. I ", "mvt. II "],
    "Pictures at an Exhibition": ["Promenade", "Great Gate"],
    "Aida": ["Triumphal March", "Fuggiam"],
    "La traviata": ["Libiamo", "Prelude"],
    "Symphony No. 3|Beethoven": ["mvt. I ", "mvt. II "],
    "Symphony No. 3|Brahms": ["mvt. III", "mvt. I "],
    "Piano Quintet in A major": ["mvt. I ", "mvt. V"],
    "Symphony No. 5|Tchaikovsky": ["mvt. I ", "mvt. II "],
    "Symphony No. 6|Tchaikovsky": ["mvt. I ", "mvt. III"],
    "The Sleeping Beauty": ["Garland Waltz", "Introduction"],
    "Rigoletto": ["donna è mobile", "Zitti"],
    "The Four Seasons": ["Spring", "Winter"],
    "Madama Butterfly": ["Act II - Aria", "Finale"],
    "Tosca": ["Vissi d'arte", "lucevan"],
    "Don Giovanni": ["Champagne", "Overture"],
    "Le nozze di Figaro": ["Overture", "Non più andrai"],
}


def roman_order(m):
    r = re.search(r"mvt\. ([IVX]+)", m)
    if not r:
        return 99
    v = {"I": 1, "V": 5, "X": 10}
    s = r.group(1)
    return sum(v[c] if i + 1 == len(s) or v[c] >= v[s[i + 1]] else -v[c] for i, c in enumerate(s))


def main(apply):
    cs = C.anki("cardsInfo", cards=C.anki("findCards", query='note:"Classical Music" card:"%s" -is:suspended' % CARD))
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=list({c["note"] for c in cs}))}
    g = collections.defaultdict(list)
    for c in cs:
        n = ns[c["note"]]
        w, comp = C.plain(n["fields"]["Work"]["value"]), C.plain(n["fields"]["Composer"]["value"])
        g[(w, comp)].append((c["cardId"], n["noteId"], C.plain(n["fields"]["Movement"]["value"]) + " "))
    off, notes = [], []
    for (w, comp), v in g.items():
        if len(v) <= 2:
            continue
        pref = PREFER.get("%s|%s" % (w, comp.split()[-1])) or PREFER.get(w) or []
        def rank(x):
            for i, p in enumerate(pref):
                if p.lower() in x[2].lower():
                    return (i, 0)
            return (len(pref), roman_order(x[2]))
        v.sort(key=rank)
        keep, drop = v[:2], v[2:]
        print("%-28s keep %s | off %d" % (w[:28], " / ".join(k[2].strip()[:28] for k in keep), len(drop)))
        off += [d[0] for d in drop]
        notes += [d[1] for d in drop]
    print(len(off), "cards to suspend")
    if apply and off:
        json.dump({"cards": off, "notes": notes}, open("backups/cm_trim_%s.json" % time.strftime("%Y%m%d_%H%M"), "w"))
        C.anki("suspend", cards=off)
        C.anki("addTags", notes=notes, tags="Music::trimmed")
        print("suspended", len(off))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
