# -*- coding: utf-8 -*-
"""fix_0927_pa_captions.py -- Performing Arts gallery captions scraped from file names, and
two gallery pictures that were wrong (each viewed on a contact sheet first).

  Art Tatum         the only gallery picture was Fats Waller ("Fats Waller edit"): removed
  Nina Simone       two near-identical crops of one 1965 photo: the "restoration1" copy removed
  captions          "Sylphide -Marie Taglioni -1832 -2", "ABT Swan Lake Curtain Call 2022 2",
                    Cyrillic "Майя Плисецкая, 1953 г 2", trailing " 2", "From left to right -",
                    and titles not in italics

    py -3.9 fix_0927_pa_captions.py [--apply]
"""
import json, re, sys, time
import concept_add as C

# title -> {gallery index: new caption}; None removes the picture and its caption
EDITS = {
    "Art Tatum": {0: None},
    "Nina Simone": {0: None, 1: "Nina Simone in 1965"},
    "A Love Supreme": {0: "The album cover", 1: "Elvin Jones, the quartet's drummer, in 1976"},
    "Dave Brubeck": {0: "The quartet in 1959, during the <i>Time Out</i> sessions: Joe Morello, Paul Desmond, Dave Brubeck, and Eugene Wright",
                     1: "The quartet in 1967: Joe Morello, Eugene Wright, Dave Brubeck, and Paul Desmond"},
    "La Sylphide": {0: "Marie Taglioni as the Sylph, 1832", 1: "August Bournonville, 1841"},
    "Maya Plisetskaya": {0: "Plisetskaya in 1953", 1: "Plisetskaya in <i>Carmen Suite</i>, 1974",
                         2: "In <i>Swan Lake</i> with the Bolshoi Ballet, 1966"},
    "American Ballet Theatre": {1: "Curtain call after <i>Swan Lake</i>, 2022"},
    "Serenade": {0: "Kaleena Burks and Kelsey Hellebuyck of Kansas City Ballet in <i>Serenade</i>",
                 1: "Kansas City Ballet dancers in <i>Serenade</i>"},
    "Company": {1: "Beth Howland, the original Amy, 1970",
                2: "Jonathan Bailey, Jamie in the 2018 London revival"},
    "Frederick Ashton": {0: "Léonide Massine, who taught the young Ashton, in 1914",
                         1: "Ninette de Valois, with whom Ashton worked from 1931"},
    "Paris Opera Ballet": {0: "Louis XIV as Apollo in the <i>Ballet royal de la nuit</i>, 1653"},
    "Tango": {0: "Pedro Figari, <i>El Tango</i>", 1: "Tango postcard, c. 1919"},
}


def plan():
    ch = []
    for title, ed in EDITS.items():
        ns = [n for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"deck:Performing Arts" "Title:*%s*"' % title))
              if C.plain(n["fields"]["Title"]["value"]) == title]
        assert len(ns) == 1, (title, len(ns))
        n = ns[0]
        g = re.findall(r"<img[^>]*>", n["fields"]["Gallery"]["value"])
        caps = n["fields"]["Gallery captions"]["value"].split(" | ")
        assert len(g) == len(caps), (title, len(g), len(caps))
        keep_g, keep_c = [], []
        for i, (im, cp) in enumerate(zip(g, caps)):
            if i in ed and ed[i] is None:
                continue
            keep_g.append(im)
            keep_c.append(ed.get(i, cp))
        ch.append((n, {"Gallery": "".join(keep_g), "Gallery captions": " | ".join(keep_c)}))
    return ch


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    for n, new in ch:
        print("==", C.plain(n["fields"]["Title"]["value"]), "|", new["Gallery captions"][:200])
    if "--apply" in sys.argv:
        json.dump([{"nid": n["noteId"], "fields": {k: n["fields"][k]["value"] for k in new}} for n, new in ch],
                  open("backups/fix_0927_pa_captions_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, new in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": new})
        print("applied", len(ch))
