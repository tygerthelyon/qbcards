# -*- coding: utf-8 -*-
"""cm_nick_1002.py -- Carter, 2026-10-02, on Music nicknames (cards showed “Moonlight” in quotes, the text *Moonlight*
in italics): "do what is conventional and apply it everywhere".

Convention (Chicago 8.193; Grove): a nickname that others gave a work is roman in quotation marks (the “Eroica”, Haydn's
“Farewell” Symphony); a real title, including a translation of the title and a composer's own subtitle, is italic
(*From the New World*, *Prelude to the Afternoon of a Faun*, *Fingal's Cave*).
- The Nickname field mixed both and the card wrapped every one in quotes ("Die Zauberflöte “The Magic Flute”"). The
  field now carries its own form, “Moonlight” or (<i>The Magic Flute</i>), and the card shows it as written.
- In running text, nicknames set in italics become quoted (about 60 mentions); titles stay italic.

    py -3.9 cm_nick_1002.py [--apply]
"""
import json
import os
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
OLD_T = '<span class="cm2-nick">“{{Nickname}}”</span>'
NEW_T = '<span class="cm2-nick">{{Nickname}}</span>'
# titles, translations of titles, and composers' own subtitles: italic, in brackets after the work
TITLES = {"Sleepers, Wake!", "Prelude to the Afternoon of a Faun", "From the New World", "Fingal's Cave", "Songs Without Words",
          "The Magic Flute", "Rondo alla turca", "A German Requiem", "Grande Messe des morts", "Mephisto Waltz No. 1", "Nocturne",
          "La campanella", "Nuages gris", "Vallée d'Obermann", "The Seasons", "The Creation", "A Musical Joke",
          "The Abduction from the Seraglio", "Death and Transfiguration", "Vespers", "Transfigured Night", "The Age of Anxiety",
          "Symphony of Sorrowful Songs", "The Girl of the Golden West", "Pique Dame", "Pope Marcellus Mass", "Song of the Youths",
          "Musique de table", "Le matin", "Le midi", "Nimrod"}
SPECIAL = {"From the Notebook for Anna Magdalena Bach": "(from the <i>Notebook for Anna Magdalena Bach</i>)",
           "Fantasy Overture": "(fantasy overture)", "Turandot Scherzo": "(<i>Turandot</i> Scherzo)"}
# running text: nicknames in italics become quoted; titles are left alone
TEXT = [("<i>Moonlight</i>", "“Moonlight”"), ("<i>Pathétique</i>", "“Pathétique”"), ("<i>Military</i>", "“Military”"),
        ("<i>Heroic</i>", "“Heroic”"), ("The <i>Organ Symphony</i>", "The “Organ” Symphony"), ("<i>Eroica</i>", "“Eroica”"),
        ("<i>Pastoral</i>", "“Pastoral”"), ("The <i>Spring</i>,", "The “Spring”,"), ("<i>Rhenish</i>", "“Rhenish”"),
        ("<i>American</i>", "“American”"), ("<i>Death and the Maiden</i>", "“Death and the Maiden”"),
        ("<i>Revolutionary</i>", "“Revolutionary”"), ("<i>Farewell</i> waltz", "“Farewell” waltz"), ("<i>Scottish</i>", "“Scottish”"),
        ("<i>Italian</i>", "“Italian”"), ("<i>Appassionata</i>", "“Appassionata”"), ("<i>Paukenmesse</i>", "“Paukenmesse”"),
        ("<i>Hornsignal</i>", "“Hornsignal”"), ("<i>Oxford</i>", "“Oxford”"), ("<i>Surprise</i>", "“Surprise”"),
        ("<i>Linz</i>", "“Linz”"), ("The <i>Classical</i>", "The “Classical”"), ("quoting the <i>Jupiter</i>", "quoting the “Jupiter”"),
        ("Shostakovich's <i>Leningrad Symphony</i>", "Shostakovich's “Leningrad” Symphony")]
TEXT_FIELDS = ("Description", "Clue", "Listen", "Notes", "Composer")


def form(v):
    p = C.plain(v).strip().replace("  ", " ")
    if p in SPECIAL:
        return SPECIAL[p]
    if p in TITLES:
        return "(<i>%s</i>)" % p
    return "“%s”" % p.strip("“”\"")


def main(apply):
    ids = C.anki("findNotes", query='note:"Classical Music"')
    notes = []
    for i in range(0, len(ids), 400):
        notes += C.anki("notesInfo", notes=ids[i:i + 400])
    changes, backup, used = {}, {}, set()
    for n in notes:
        f = {k: v["value"] for k, v in n["fields"].items()}
        new = {}
        concept = bool(C.plain(f["Kind"]).strip())
        if f["Nickname"].strip() and not concept:
            v = form(f["Nickname"])
            if v != f["Nickname"]:
                new["Nickname"] = v
        for k in TEXT_FIELDS + (("Nickname",) if concept else ()):
            s = new.get(k, f.get(k, ""))
            for old, rep in TEXT:
                if old in s:
                    s = s.replace(old, rep)
                    used.add(old)
            if s != f.get(k, ""):
                new[k] = s
        if new:
            changes[n["noteId"]] = new
            backup[n["noteId"]] = {k: f[k] for k in new}
    for old, _ in TEXT:
        if old not in used:
            print("UNUSED", old)
    shown = set()
    for nid, new in changes.items():
        for k, v in new.items():
            key = (k, backup[nid][k][:60])
            if key in shown:
                continue
            shown.add(key)
            print("%s %-9s %s\n   -> %s" % (nid, k, backup[nid][k][:90], v[:90]))
    print(len(changes), "notes")
    t = C.anki("modelTemplates", modelName="Classical Music")
    nt, cnt = {}, 0
    for name, sides in t.items():
        nt[name] = {}
        for side in ("Front", "Back"):
            cnt += sides[side].count(OLD_T)
            nt[name][side] = sides[side].replace(OLD_T, NEW_T)
    print("template spots:", cnt)
    if not apply:
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump(backup, open(os.path.join(HERE, "backups", "cm_nick_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(t, open(os.path.join(HERE, "templates_backup", "cm_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    C.anki("updateModelTemplates", model={"name": "Classical Music", "templates": nt})
    for nid, new in changes.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": new})
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
