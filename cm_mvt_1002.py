# -*- coding: utf-8 -*-
"""cm_mvt_1002.py -- Movement fields of sung works still in the import's form ("Act 2 - <i>Der Hölle Rache</i>"), found
while checking the nickname change on Die Zauberflöte. One convention, as cm_text_1001.py set it for instrumental works:
arias, songs, and choruses in quotation marks; Mass and Requiem sections roman (Kyrie, Dies irae); orchestral numbers
inside an opera or oratorio italic (*Flight of the Bumblebee*); generic labels roman (Prelude, Finale); "Act II · ".

    py -3.9 cm_mvt_1002.py [--apply]
"""
import json
import os
import re
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
SUNG = re.compile(r"opera|song|lied|choral|oratorio|operetta|requiem|mass|cantata|passion|musical|vocal|madrigal|anthem|hymn|sacred", re.I)
INSTR = {"Les Toréadors", "Polovtsian Dance: Dance of the Maidens", "Polovtsian Dance: Dance of the Men", "Arrival of the Queen of Sheba",
         "Wedding March", "Flight of the Bumblebee", "Dance of the Tumblers", "Entry of the Gods into Valhalla",
         "Dawn and Siegfried's Rhine Journey", "Act III Prelude and Wedding March", "Forest Murmurs", "Polovtsian Dances I",
         "Polovtsian Dances II", "Polovtsian Dances III", "Polovtsian Dances IV", "Polovtsian Dances V", "Representation of Chaos",
         "Four Sea Interludes", "Knee Play 5", "Dance of the Seven Veils", "Dance of the Hours", "Mysteries of the Macabre",
         "Shepherd's Dance"}
LITURGY = {"Kyrie", "Gloria", "Credo", "Sanctus", "Agnus Dei", "Benedictus", "Dona nobis pacem", "Dies Irae", "Dies irae", "Lacrimosa",
           "Rex tremendae", "Tuba mirum", "Requiem aeternam", "Agnus Dei (Dona nobis pacem)"}
GENERIC = {"Prelude", "Finale", "Arioso", "Intermezzo", "Passacaglia", "Galop", "Recognition Scene", "The Fifth Door",
           "Presentation of the Rose"}
SPECIAL = {"Ombra mai fu (Largo)": "“Ombra mai fu” (“Largo”)", "Gute Nacht (Good Night)": "“Gute Nacht” (“Good Night”)",
           "Aria der Anna": "Act I · “Se come voi piccina io fossi”", "Votre serviteur.": "“Votre serviteur”"}
ROMAN = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V"}


def fix(mv, genre):
    m = re.fullmatch(r"(?:(Act|mvt\.) (\d|[IVX]+) - |(\d+)\. |(No\. \d+), )?<i>([^<]+)</i>(.*)", mv.strip())
    if not m:
        return mv
    kind, num, numdot, no, title, rest = m.groups()
    title = title.strip()
    if rest.strip() and not rest.strip().startswith("("):
        return mv   # a work title followed by its excerpt ("<i>Die Walküre</i>, Act III · ...") is already in form
    if title in SPECIAL:
        return SPECIAL[title]
    if not SUNG.search(genre) or title in INSTR:
        body = "<i>%s</i>" % title
    elif title in LITURGY:
        body = title.replace("Dies Irae", "Dies irae")
    elif title in GENERIC:
        body = title
    else:
        body = "“%s”" % title
    pre = ""
    if kind:
        pre = "%s %s · " % ("Act" if kind == "Act" else "mvt.", ROMAN.get(num, num))
    elif numdot:
        pre = "No. %s, " % numdot
    elif no:
        pre = no + ", "
    return pre + body + rest


def main(apply):
    ids = C.anki("findNotes", query='note:"Classical Music"')
    changes, backup = {}, {}
    for i in range(0, len(ids), 400):
        for n in C.anki("notesInfo", notes=ids[i:i + 400]):
            f = n["fields"]
            mv = f["Movement"]["value"]
            if not mv.strip() or f["Kind"]["value"].strip():
                continue
            new = fix(mv, C.plain(f["Genre"]["value"]))
            if new != mv:
                changes[n["noteId"]] = new
                backup[n["noteId"]] = mv
    seen = set()
    for nid, v in changes.items():
        if (backup[nid], v) in seen:
            continue
        seen.add((backup[nid], v))
        print("%-55s -> %s" % (backup[nid][:55], v))
    print(len(changes), "notes")
    if not apply:
        return
    json.dump(backup, open(os.path.join(HERE, "backups", "cm_mvt_before_%s.json" % time.strftime("%Y%m%d_%H%M%S")), "w",
                           encoding="utf-8"), ensure_ascii=False)
    for nid, v in changes.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": {"Movement": v}})
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
