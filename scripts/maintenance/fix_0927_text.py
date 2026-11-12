# -*- coding: utf-8 -*-
"""fix_0927_text.py -- audit recheck 2026-09-27, highest-priority text fixes (non-Geography).

1. Performing Arts musicals: Creator named only the composer on most notes ("Richard Rodgers"
   for Oklahoma!) but the songwriting team on others (Dear Evan Hansen, Camelot). Questions ask
   for the team, so every musical with a separate lyricist now names composer and lyricist.
2. Table of Silence dated 1907; the Targu Jiu ensemble is 1937-38.
3. Tango's Venue held a region ("Rio de la Plata, Argentina, and Uruguay"); the origin is
   already in its clue, so the Venue is cleared.
4. Classical Music Composer fields holding a raw "&middot;" entity use the character.

    py -3.9 fix_0927_text.py [--apply]
"""
import json, sys, time
import concept_add as C

TEAMS = {
    "West Side Story": "Leonard Bernstein and Stephen Sondheim",
    "Oklahoma!": "Richard Rodgers and Oscar Hammerstein II",
    "The Phantom of the Opera": "Andrew Lloyd Webber and Charles Hart",
    "The Sound of Music": "Richard Rodgers and Oscar Hammerstein II",
    "The King and I": "Richard Rodgers and Oscar Hammerstein II",
    "South Pacific": "Richard Rodgers and Oscar Hammerstein II",
    "Carousel": "Richard Rodgers and Oscar Hammerstein II",
    "Les Misérables": "Claude-Michel Schönberg and Alain Boublil",
    "Evita": "Andrew Lloyd Webber and Tim Rice",
    "Cabaret": "John Kander and Fred Ebb",
    "Chicago": "John Kander and Fred Ebb",
    "A Chorus Line": "Marvin Hamlisch and Edward Kleban",
    "Annie": "Charles Strouse and Martin Charnin",
    "Fiddler on the Roof": "Jerry Bock and Sheldon Harnick",
    "Show Boat": "Jerome Kern and Oscar Hammerstein II",
    "My Fair Lady": "Frederick Loewe and Alan Jay Lerner",
    "Camelot": "Frederick Loewe and Alan Jay Lerner",
    "Gypsy": "Jule Styne and Stephen Sondheim",
    "Man of La Mancha": "Mitch Leigh and Joe Darion",
    "The Threepenny Opera": "Kurt Weill and Bertolt Brecht",
    "Hair": "Galt MacDermot, Gerome Ragni, and James Rado",
    "Miss Saigon": "Claude-Michel Schönberg and Alain Boublil",
    "The Lion King": "Elton John and Tim Rice",
    "Spring Awakening": "Duncan Sheik and Steven Sater",
    "Funny Girl": "Jule Styne and Bob Merrill",
    "Bye Bye Birdie": "Charles Strouse and Lee Adams",
    "42nd Street": "Harry Warren and Al Dubin",
    "Damn Yankees": "Richard Adler and Jerry Ross",
    "The Pajama Game": "Richard Adler and Jerry Ross",
}


def plan():
    ch = []   # (nid, field, old, new)
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"deck:Performing Arts" Kind:Work')):
        t = C.plain(n["fields"]["Title"]["value"])
        if t in TEAMS and C.plain(n["fields"]["Creator"]["value"]) != TEAMS[t]:
            ch.append((n["noteId"], "Creator", n["fields"]["Creator"]["value"], TEAMS[t]))
        if t == "Tango" and n["fields"]["Venue"]["value"].strip():
            ch.append((n["noteId"], "Venue", n["fields"]["Venue"]["value"], ""))
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"deck:Performing Arts" Title:Tango')):
        if n["fields"]["Venue"]["value"].strip() and not any(c[0] == n["noteId"] and c[1] == "Venue" for c in ch):
            ch.append((n["noteId"], "Venue", n["fields"]["Venue"]["value"], ""))
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='deck:Art "Title:*Table of Silence*"')):
        if C.plain(n["fields"]["Date"]["value"]) == "1907":
            ch.append((n["noteId"], "Date", n["fields"]["Date"]["value"], "1937–1938"))
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"deck:Classical Music" Composer:*middot*')):
        v = n["fields"]["Composer"]["value"]
        ch.append((n["noteId"], "Composer", v, v.replace("&middot;", "·")))
    return ch


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    for nid, f, o, v in ch:
        print("%d %-8s %s  ->  %s" % (nid, f, C.plain(o)[:45], C.plain(v)[:50]))
    print(len(ch), "changes")
    if "--apply" in sys.argv and ch:
        json.dump(ch, open("backups/fix_0927_text_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for nid, f, o, v in ch:
            C.anki("updateNoteFields", note={"id": nid, "fields": {f: v}})
        print("applied")
