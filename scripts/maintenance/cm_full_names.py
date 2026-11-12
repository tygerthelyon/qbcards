# -*- coding: utf-8 -*-
"""cm_full_names.py -- full names for people who are not household names.

Carter (2026-09-25): "when a person ... is not extremely recognizable (i.e.
actually commonly known by their last name only) then write out their first and
last name. e.g. in the la boheme card, it just says 'murger', idk who that is".

Every bare capitalised surname in the Classical Music Description / Listen text
was listed and read; these are the ones a reader cannot be expected to place.
The first mention in each field becomes the full name; later mentions in the
same field stay short. Composers named on their own card, and the universally
known (Mozart, Tolstoy, Goya, Napoleon), are left alone.

    py -3.9 cm_full_names.py --dry | --apply
"""
import json
import re
import sys
import time

import concept_add as C

FULL = {
    "Murger": "Henri Murger", "Mallarmé": "Stéphane Mallarmé", "Nijinsky": "Vaslav Nijinsky",
    "Jaeger": "August Jaeger", "Grofé": "Ferde Grofé", "Kabalevsky": "Dmitry Kabalevsky",
    "Alma": "Alma Mahler", "Beaumarchais": "Pierre Beaumarchais", "Süssmayr": "Franz Xaver Süssmayr",
    "Toscanini": "Arturo Toscanini", "Paisiello": "Giovanni Paisiello", "Lyadov": "Anatoly Lyadov",
    "Hoffmann": "E. T. A. Hoffmann", "Bülow": "Hans von Bülow", "Balakirev": "Mily Balakirev",
    "Petipa": "Marius Petipa", "Ivanov": "Lev Ivanov", "Manzoni": "Alessandro Manzoni",
    "Meredith": "George Meredith", "Joachim": "Joseph Joachim", "Heine": "Heinrich Heine",
    "Clara": "Clara Schumann", "Müller": "Wilhelm Müller", "Guiraud": "Ernest Guiraud",
    "Salomon": "Johann Peter Salomon", "Esterházy": "Prince Nikolaus Esterházy",
    "Quinault": "Philippe Quinault", "Piccinni": "Niccolò Piccinni", "Diaghilev": "Sergei Diaghilev",
    "Chaliapin": "Feodor Chaliapin", "Koussevitzky": "Serge Koussevitzky", "Klopstock": "Friedrich Klopstock",
    "Schafer": "R. Murray Schafer", "Auden": "W. H. Auden", "Scott": "Walter Scott",
    "Čapek": "Karel Čapek", "Andersen": "Hans Christian Andersen", "Apollinaire": "Guillaume Apollinaire",
    "Cocteau": "Jean Cocteau", "Gesualdo": "Carlo Gesualdo", "Büchner": "Georg Büchner",
    "Artaud": "Antonin Artaud", "Atwood": "Margaret Atwood", "James": "Henry James",
    "Menotti": "Gian Carlo Menotti", "Tagore": "Rabindranath Tagore", "King": "Martin Luther King Jr.",
    "Ariosto": "Ludovico Ariosto", "Walpole": "Robert Walpole", "Furtwängler": "Wilhelm Furtwängler",
    "Massine": "Léonide Massine", "Ostrovsky": "Alexander Ostrovsky", "Prévost": "Abbé Prévost",
    "Corneille": "Pierre Corneille", "Oppenheimer": "J. Robert Oppenheimer", "Caruso": "Enrico Caruso",
    "Sheridan": "Richard Brinsley Sheridan", "Diabelli": "Anton Diabelli", "Boito": "Arrigo Boito",
    "Leoncavallo": "Ruggero Leoncavallo",
}
# only these uses are people; "King of the May", "James's" etc. are checked in context
CONTEXT = {
    "King": r"and King watching",
    "James": r"After James's",
    "Scott": r"(After Scott|Scott's|from Walter Scott)",
    "Alma": r"letter to Alma",
    "Clara": r"(written for Clara|Clara was)",
}


def expand(text, name, full):
    if full in text:
        return text
    if name in CONTEXT and not re.search(CONTEXT[name], text):
        return text
    # first bare use only: skip one already preceded by this person's first name
    given = full[:len(full) - len(name)] if full.endswith(name) else None
    for m in re.finditer(r"(?<![A-Za-zÀ-ž])%s(?![A-Za-zÀ-ž])" % re.escape(name), text):
        if given and text[:m.start()].endswith(given):
            continue
        return text[:m.start()] + full + text[m.end():]
    return text


def main():
    rows = C.anki("notesInfo", notes=C.anki("findNotes", query='note:"Classical Music"'))
    upd, backup, shown = [], {}, set()
    for n in rows:
        f = {}
        for fld in ("Description", "Listen"):
            v = n["fields"][fld]["value"]
            nv = v
            for name, full in FULL.items():
                if name in nv:
                    nv = expand(nv, name, full)
            if nv != v:
                f[fld] = nv
                if nv not in shown:
                    shown.add(nv)
                    print("-", C.plain(nv)[:170])
        if f:
            upd.append({"id": n["noteId"], "fields": f})
            backup[n["noteId"]] = {k: n["fields"][k]["value"] for k in f}
    print("\n%d notes, %d distinct texts" % (len(upd), len(shown)))
    if "--apply" in sys.argv:
        json.dump(backup, open("backups/cm_full_names_before_%s.json" % time.strftime("%Y%m%d_%H%M"),
                               "w", encoding="utf-8"), ensure_ascii=False)
        C.anki("multi", actions=[{"action": "updateNoteFields", "params": {"note": u}} for u in upd])
        print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
