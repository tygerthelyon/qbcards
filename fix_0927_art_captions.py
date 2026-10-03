# -*- coding: utf-8 -*-
"""fix_0927_art_captions.py -- captions on active Art concept cards that were Wikipedia text.

Dimensions and credit lines ("oil on canvas, 65.1 x 80.6 cm, Minneapolis Institute..."), whole
sentences ending in full stops, titles not in italics, and vague labels ("A Dutch kitchen interior")
rewritten as "Artist, <i>Title</i>, date". Pictures identified by eye on a contact sheet, attributions
checked against Wikipedia (Alechinsky, Appel, Utamaro).

Two factual fixes: Oath of the Horatii was dated 1786 (1784). Synthetic Cubism showed Picasso's
Girl with a Mandolin (1910), an Analytic work that is also on the Analytic Cubism card: removed.
Analytic Cubism showed Braque's Viaduct at L'Estaque (1907-08), which is proto-Cubist: replaced
by Picasso's Portrait of Daniel-Henry Kahnweiler (1910).

    py -3.9 fix_0927_art_captions.py [--apply]
"""
import json, os, re, sys, time
from PIL import Image
import concept_add as C

SRC = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/4c6fe2ff-c3a6-47fb-8b54-226f916ad6af/scratchpad/img/cub_00.jpg"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
KAHN = "artcon-analytic-cubism-kahnweiler.jpg"

# title -> [(old caption prefix, new caption | None to drop the picture | (new img, new caption))]
EDITS = {
    "Expressionism": [("Einstein Tower in Potsdam", "Erich Mendelsohn, Einstein Tower, Potsdam, 1919–22"),
                      ("Goetheanum, Dornach", "Rudolf Steiner, the second Goetheanum, Dornach, 1924–28"),
                      ("Het Schip, Amsterdam", "Michel de Klerk, Het Schip, Amsterdam, 1917–20")],
    "Neoclassicism": [("Cupid driving a griffin chariot", "Michelangelo Maestri, Cupid driving a chariot of griffins, c. 1800")],
    "Ukiyo-e": [("A woodcut titled Kushi", "Kitagawa Utamaro, <i>Kushi</i> (<i>Comb</i>), c. 1785")],
    "Lithography": [("A lithograph of Charles Marion Russell", "Charles Marion Russell, <i>The Custer Fight</i>, lithograph, 1903")],
    "Academic art": [("Giorgio Vasari helped found", "Giorgio Vasari, a founder of the Accademia delle Arti del Disegno, Florence"),
                     ("Carlo Maratti, The Academy of Drawing", "Carlo Maratti, <i>The Academy of Drawing</i>, c. 1704–09"),
                     ("Charles Le Brun, Apotheosis of Louis XIV", "Charles Le Brun, <i>The Apotheosis of Louis XIV</i>, 1677")],
    "Analytic Cubism": [("Georges Braque, 1907", ('<img src="%s">' % KAHN, "Pablo Picasso, <i>Portrait of Daniel-Henry Kahnweiler</i>, 1910")),
                        ("Fernand Léger, Nudes in the forest", "Fernand Léger, <i>Nudes in the Forest</i>, 1909–11")],
    "Synthetic Cubism": [("Juan Gris, September 1916", "Juan Gris, <i>Woman with a Mandolin, after Corot</i>, 1916"),
                         ("Pablo Picasso, 1910, Girl with a Mandolin", None),
                         ("Pablo Picasso, Head", "Pablo Picasso, <i>Head</i>, 1913–14, papier collé")],
    "Ashcan School": [("John French Sloan, Self-portrait", "John French Sloan, <i>Self-Portrait</i>, 1890"),
                      ("Ashcan School artists and friends", "Ashcan School artists and friends at John French Sloan's Philadelphia studio, 1898")],
    "CoBrA": [("Le Bruit de la Chute", "Pierre Alechinsky, <i>Le Bruit de la chute</i>, 1974–75"),
              ("Frog with umbrella", "Karel Appel, <i>Frog with Umbrella</i>, 2001, the Spui, The Hague"),
              ("The Elephant, now located", "Karel Appel, <i>The Elephant</i>, University of Maryland")],
    "Dutch Golden Age": [("Frans Hals' tronie", "Frans Hals, <i>Gypsy Girl</i>, 1628–30"),
                         ("The Blinding of Samson", "Rembrandt, <i>The Blinding of Samson</i>, 1636")],
    "Graffiti": [("Ancient Pompeii graffito", "A graffito caricature of a politician, Villa of the Mysteries, Pompeii")],
    "Hellenistic": [("The Ludovisi Gaul", "<i>Ludovisi Gaul</i>, Roman copy of a Hellenistic original, Museo Nazionale Romano, Rome")],
    "Performance art": [("Conceptual work by Yves Klein", "Yves Klein, <i>Leap into the Void</i>, Fontenay-aux-Roses, 1960"),
                        ("Helen Moller dance performance", "Helen Moller dancing, photographed by Arnold Genthe, early 20th century")],
    "Romanesque": [("A round-arched Romanesque interior", "The painted vaults of the Pantheon of the Kings, San Isidoro, León, 12th century"),
                   ("The “Morgan Leaf”", "The Morgan Leaf, from the Winchester Bible, 1160–75")],
    "Young British Artists": [("Goldsmiths College, Millard Building", "Goldsmiths' Millard Building, Camberwell, where many of the YBAs studied in the late 1980s"),
                              ("View of East Country Yard Show", "Anya Gallaccio's installation at the <i>East Country Yard Show</i>, 1990")],
    "Genre painting": [("A Dutch kitchen interior", "Nicolaes Maes, <i>The Idle Servant</i>, 1655"),
                       ("Peasant Dance, c. 1568", "Pieter Bruegel the Elder, <i>The Peasant Dance</i>, c. 1567"),
                       ("Merry Company, by Dirck Hals", "Dirck Hals, <i>Merry Company</i>")],
    "History painting": [("A mythological subject", "Titian, <i>Diana and Actaeon</i>, 1556–59"),
                         ("Judas Returning the Thirty Silver Pieces", "Rembrandt, <i>Judas Returning the Thirty Pieces of Silver</i>, 1629"),
                         ("Jacques-Louis David's Oath of the Horatii", "Jacques-Louis David, <i>Oath of the Horatii</i>, 1784")],
    "Humanism": [("Original lyrics by Petrarch", "A manuscript of Petrarch's verse, found in Erfurt in 1985"),
                 ("Medieval and Renaissance Italian writers", "Giorgio Vasari, <i>Six Tuscan Poets</i>, 1544")],
    "Avant-garde": [("Political revolution has influenced", "<i>The Overthrow of the Autocracy</i>, a Soviet avant-garde painting, c. 1917")],
}


def note(title):
    ns = [n for n in C.anki("notesInfo", notes=C.anki("findNotes", query='note:Art "Title:*%s*" Kind:_*' % title))
          if C.plain(n["fields"]["Title"]["value"]) == title]
    assert len(ns) == 1, (title, len(ns))
    return ns[0]


def plan():
    ch = []
    for title, eds in EDITS.items():
        n = note(title)
        imgs = re.findall(r"<img[^>]*>", n["fields"]["Artwork"]["value"])
        caps = n["fields"]["Captions"]["value"].split(" | ")
        assert len(imgs) == len(caps), (title, len(imgs), len(caps))
        for old, new in eds:
            k = [i for i, c in enumerate(caps) if C.plain(c).startswith(old)]
            assert len(k) == 1, (title, old, [C.plain(c)[:40] for c in caps])
            k = k[0]
            if new is None:
                imgs[k] = caps[k] = None
            elif isinstance(new, tuple):
                imgs[k], caps[k] = new
            else:
                caps[k] = new
        keep = [(i, c) for i, c in zip(imgs, caps) if i is not None]
        ch.append((n, {"Artwork": "".join(i for i, c in keep), "Captions": " | ".join(c for i, c in keep)}))
    return ch


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    for n, new in ch:
        print("==", C.plain(n["fields"]["Title"]["value"]), "|", new["Captions"][:230])
    if "--apply" in sys.argv:
        im = Image.open(SRC).convert("RGB"); im.save(os.path.join(MED, KAHN), quality=90)
        json.dump([{"nid": n["noteId"], "fields": {k: n["fields"][k]["value"] for k in new}} for n, new in ch],
                  open("backups/fix_0927_art_captions_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, new in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": new})
        print("applied", len(ch))
