# -*- coding: utf-8 -*-
"""cm_text_1001.py -- Classical Music text, Carter's notes of 2026-10-01.

- "Prelude menuet etc should be italicized on suite bergamesque card": instrumental pieces and movements are italic
  (*Mars*, *Clair de lune*); only sung numbers take quotes. Titled instrumental movements had been quoted all over
  the deck ("Shepherd's Song", "The Sea and Sinbad's Ship", Ives's "Putnam's Camp", Debussy's "Golliwogg's
  Cakewalk"), and many Movement fields left their tempo markings roman.
- "A lot of times when a work is preceded by the artist eg 'mozart's leoporello' ... the work isn't italicized":
  every "Name's Title" in the deck was read by hand. Leporello is a character, not a work: the Diabelli card now
  names his aria. Brahms's *Hungarian Dances*, Bach's *Orgelbüchlein*, Brahms's *Alto Rhapsody*, Reich's
  *Piano Phase* and *Come Out*; Gounod's "Jewel Song" and "Dido's Lament" are sung, so quoted.
- Movement fields in one form: "mvt. III · <i>Title</i> · <i>Tempo</i>", "Act III · “Aria”", "Act III · <i>Orchestral
  piece</i>" ("Act 3 - Ride of the Valkyries" and "Aria (Mimi)" were left from the original import).

    py -3.9 cm_text_1001.py [--apply]
"""
import json
import os
import re
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_FIELDS = ("Description", "Clue", "Listen", "Nickname", "Notes", "Composer", "Movement")

# quoted instrumental titles: italic wherever they appear
INSTR = ["Harold aux montagnes", "Marche des pèlerins", "Orgie de brigands", "Sérénade d’un montagnard des Abruzzes",
         "Putnam's Camp", "The Housatonic at Stockbridge", "The Queen’s Monastery", "Turandot", "Doctor Gradus ad Parnassum",
         "Golliwogg's Cakewalk", "Désordre", "L'escalier du diable", "Träumerei", "Rondo alla turca", "Emerson", "Hawthorne",
         "The Alcotts", "Thoreau", "Festival at Baghdad – The Sea – The Ship Breaks against a Cliff", "The Kalendar Prince",
         "The Sea and Sinbad’s Ship", "The Young Prince and the Young Princess",
         "Awakening of Cheerful Feelings on Arrival in the Country", "Merry Gathering of Country Folk", "Shepherd’s Song",
         "Thunderstorm", "Engelkonzert", "Waltz of the Flowers", "The Elephant", "The Swan", "The Old Castle", "Hoedown",
         "Sabre Dance", "A Cosmic Landscape", "The Poem of Fire", "Flight of the Bumblebee", "Infernal Galop", "Méditation",
         "The Representation of Chaos"]

# plain replacements, any note: (old, new)
REPL = [
    ("including a parody of Mozart's Leporello.",
     "including a parody of Leporello's “Notte e giorno faticar” from Mozart's <i>Don Giovanni</i>."),
    ("after the success of Brahms's Hungarian Dances;", "after the success of Brahms's <i>Hungarian Dances</i>;"),
    ("parodying Gounod's Jewel Song,", "parodying Gounod's “Jewel Song”,"),
    ("Dido's Lament and Purcell's laments generally", "“Dido's Lament” and Purcell's laments generally"),
    ("Bach's Orgelbüchlein is the great collection.", "Bach's <i>Orgelbüchlein</i> is the great collection."),
    ("Brahms's Alto Rhapsody,", "Brahms's <i>Alto Rhapsody</i>,"),
    ("Reich's Piano Phase and Come Out are", "Reich's <i>Piano Phase</i> and <i>Come Out</i> are"),
    ("<i>Starting</i> two identical repeating patterns", "Starting two identical repeating patterns"),
    ("Four pieces, Prélude, Menuet, Clair de lune, and Passepied;",
     "Four pieces, <i>Prélude</i>, <i>Menuet</i>, <i>Clair de lune</i>, and <i>Passepied</i>;"),
    ("Contains <i>Nessun dorma</i>.", "Contains “Nessun dorma”."),
]
WORK = {1787711405050: "<i>Suite bergamasque</i>"}   # Debussy's title, French capitals as for the deck's other French titles

# Movement fields set whole
MOVEMENT = {
    1787711405019: "mvt. IV · <i>Presto – Allegro assai</i> (“Ode to Joy”)",
    1787711405192: "Act II · <i>Triumphal March</i>",
    1787711405202: "Act III · <i>Ride of the Valkyries</i>",
    1787711405422: "Act III · <i>Ride of the Valkyries</i>",
    1787711405409: "Act III · <i>Dance of the Apprentices</i>",
    1787711405415: "Act III · <i>Siegfried's Funeral March</i>",
    1787711405762: "Act II · <i>Dance of the Little Moorish Slaves</i>",
    1787711405763: "Act I · <i>Sacred Dance of the Priestesses</i>",
    1787711405889: "Act III · <i>Bacchanale</i>",
    1787711405430: "Act III · Finale",
    1787711405775: "Dies irae · Ingemisco",
    1787711405776: "Dies irae · Lacrymosa",
    1787711405679: "“O mio babbino caro”",
    1787792906306: "Act III · “When I am laid in earth” (“Dido's Lament”)",
    1788489953224: "Act I · “Glück, das mir verblieb” (“Marietta's Lute Song”)",
    1788489953153: "Act III · “When Other Lips” (Thaddeus)",
    # clips named "Aria (Mimi)" and "Act III - Aria" in the original import, identified by speech recognition
    1787711405684: "Act I · “Sì, mi chiamano Mimì”",
    1787711405698: "Act II · “In questa reggia”",
    1787711405700: "Act III · “Tu che di gel sei cinta”",
    1787711405868: "Prologue, Scene 1",
    1787711405316: "mvt. III · “Herr, lehre doch mich” · <i>Andante moderato</i>",
    1787711405317: "mvt. III · “Herr, lehre doch mich” · <i>Andante moderato</i>",
    1787711405319: "mvt. III · “Herr, lehre doch mich” · <i>Andante moderato</i>",
    1787711405320: "mvt. III · “Herr, lehre doch mich” · <i>Andante moderato</i>",
}
# Brahms's Requiem: a sung title, then a tempo
for nid in (1787711405306, 1787711405307, 1787711405308):
    MOVEMENT[nid] = "mvt. I · “Selig sind, die da Leid tragen” · <i>Ziemlich langsam und mit Ausdruck</i>"
for nid in (1787711405310, 1787711405311, 1787711405313):
    MOVEMENT[nid] = "mvt. II · “Denn alles Fleisch es ist wie Gras” · <i>Langsam, marschmäßig</i>"
MOVEMENT[1787711405322] = "mvt. IV · “Wie lieblich sind deine Wohnungen” · <i>Mäßig bewegt</i>"
MOVEMENT[1787711405323] = "mvt. V · “Ihr habt nun Traurigkeit” · <i>Langsam</i>"
MOVEMENT[1787711405324] = "mvt. VI · “Denn wir haben hie keine bleibende Statt” · <i>Andante</i> – <i>Allegro</i>"
LEAVE = re.compile(r"^(no tempo indication)$")
SUNG = re.compile(r"opera|song|lied|choral|oratorio|operetta|requiem|mass|cantata|passion|musical|vocal|madrigal|anthem|hymn", re.I)


def mvt_italic(mv):
    """'mvt. II · Romanze. Andante' -> 'mvt. II · <i>Romanze. Andante</i>': the parts after the number of an
    instrumental movement are titles or tempo markings, italic either way"""
    m = re.match(r"^(mvt\. [IVXL]+)( · .*)$", mv)
    if not m:
        return mv
    parts = m.group(2).split(" · ")[1:]
    out = []
    for p in parts:
        if "<i>" in p or "“" in p or LEAVE.match(p.strip()):
            out.append(p)
        else:
            out.append("<i>%s</i>" % p.strip())
    return m.group(1) + "".join(" · " + p for p in out)


def main(apply):
    ids = C.anki("findNotes", query='note:"Classical Music"')
    notes = []
    for i in range(0, len(ids), 400):
        notes += C.anki("notesInfo", notes=ids[i:i + 400])
    changes, backup = {}, {}
    used = set()
    for n in notes:
        f = {k: v["value"] for k, v in n["fields"].items()}
        new = {}
        for k in TEXT_FIELDS:
            if k not in f:
                continue
            v = new.get(k, f[k])
            for t in INSTR:
                if "“%s”" % t in v:
                    v = v.replace("“%s”" % t, "<i>%s</i>" % t)
                    used.add(t)
            for old, rep in REPL:
                if old in v:
                    v = v.replace(old, rep)
                    used.add(old)
            if v != f[k]:
                new[k] = v
        nid = n["noteId"]
        if nid in MOVEMENT:
            new["Movement"] = MOVEMENT[nid]
        elif "Movement" in f and not SUNG.search(C.plain(f.get("Genre", ""))):
            mv = mvt_italic(new.get("Movement", f["Movement"]))
            if mv != f["Movement"]:
                new["Movement"] = mv
        if nid in WORK:
            new["Work"] = WORK[nid]
        new = {k: v for k, v in new.items() if v != f[k]}
        if new:
            changes[nid] = new
            backup[nid] = {k: f[k] for k in new}
    for t in INSTR + [o for o, _ in REPL]:
        if t not in used:
            print("UNUSED:", t)
    for nid, new in changes.items():
        for k, v in new.items():
            print(nid, k, "|", backup[nid][k][:120], "\n     ->", v[:120])
    print(len(changes), "notes")
    if not apply:
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump(backup, open(os.path.join(HERE, "backups", "cm_text_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    for nid, new in changes.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": new})
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
