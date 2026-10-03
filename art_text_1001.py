# -*- coding: utf-8 -*-
"""art_text_1001.py -- Art deck, Carter's notes of 2026-10-01.

- "Bad image: YBA card": the movement card showed an unreadable grid, a Goldsmiths doorway, and a 250-pixel scan. It
  now shows the movement's three signature works (Hirst's shark, Emin's bed, Ofili's Virgin), the deck's own images.
- "Luncheon on the grass should have déjeuner sur l'herbe listed as title too".
- Works named after an artist's possessive left roman (Blake's *Newton*, Whistler's *Nocturnes*), and the movement
  and technique captions imported from Commons on 2026-09-24: titles roman, artist and date in any order,
  dimensions and accession notes, a few cut off mid-sentence. Rewritten as "Artist, *Title*, date".

    py -3.9 art_text_1001.py [--apply]
"""
import json
import os
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))

FIELDS = {
    1790236439217: {   # Young British Artists
        "Artwork": '<img src="paste-54a1e5e799b15a359c63af46833d135e99271e60.jpg"><img src="2834.jpg">'
                   '<img src="Screen-Shot-2024-07-14-at-8.05.05-PM.png">',
        "Captions": "Damien Hirst, <i>The Physical Impossibility of Death in the Mind of Someone Living</i>, 1991 | "
                    "Tracey Emin, <i>My Bed</i>, 1998 | Chris Ofili, <i>The Holy Virgin Mary</i>, 1996",
    },
    1787890517565: {"Title": "<i>The Luncheon on the Grass (or Le Déjeuner sur l'herbe)</i>"},
}
# (note, field): [(old, new)]
REPL = {
    (1790236439025, "Notes"): [("Whistler's Nocturnes", "Whistler's <i>Nocturnes</i>")],
    (1790238648634, "Notes"): [("Blake's Newton rebuilt", "Blake's <i>Newton</i> rebuilt")],
    (1788489939767, "Captions"): [("(Tatlin's Tower)", "(<i>Tatlin's Tower</i>)")],
}
# caption entries, exact old text -> new, wherever they occur
CAPS = {
    "Werner Stürenburg, assemblage No. 5, 1968": "Werner Stürenburg, <i>Assemblage No. 5</i>, 1968",
    "Sabra (1956), Berardo Collection Museum": "<i>Sabra</i>, 1956, Berardo Collection, Lisbon",
    "Frank W. Benson, Eleanor Holding a Shell, North Haven, Maine, 1902, private collection":
        "Frank W. Benson, <i>Eleanor Holding a Shell, North Haven, Maine</i>, 1902",
    "Theodore Robinson, Low Tide Riverside Yacht Club, (1894), Collection of Margaret and Raymond Horowitz":
        "Theodore Robinson, <i>Low Tide, Riverside Yacht Club</i>, 1894",
    "Mary Cassatt, The Child's Bath (1893)": "Mary Cassatt, <i>The Child's Bath</i>, 1893",
    "Painting by Edvard Munch, “The Dance of Life”, 1899–1900.": "Edvard Munch, <i>The Dance of Life</i>, 1899–1900",
    "Deposition of Christ by Prospero Fontana, 1563": "Prospero Fontana, <i>Deposition of Christ</i>, 1563",
    "Domenichino, Saint Cecilia Distributing Alms, fresco, 1612–15, San Luigi dei Francesi, Rome":
        "Domenichino, <i>Saint Cecilia Distributing Alms</i>, 1612–15, San Luigi dei Francesi, Rome",
    "Mars Chastising Cupid (ca. 1605–1610) by Bartolomeo Manfredi": "Bartolomeo Manfredi, <i>Mars Chastising Cupid</i>, c. 1605–10",
    "Cain slaying Abel, Rubens, 1608–09": "Peter Paul Rubens, <i>Cain Slaying Abel</i>, 1608–09",
    "The Procuress by van Honthorst, 1625": "Gerard van Honthorst, <i>The Procuress</i>, 1625",
    "Bacchante with an Ape by ter Brugghen, 1627": "Hendrick ter Brugghen, <i>Bacchante with an Ape</i>, 1627",
    "Crowning with Thorns by Dirck van Baburen (1622)": "Dirck van Baburen, <i>The Crowning with Thorns</i>, 1622",
    "Paul Gauguin, The Yellow Christ (Le Christ jaune), 1889": "Paul Gauguin, <i>The Yellow Christ</i>, 1889",
    "Émile Bernard by Henri de Toulouse-Lautrec (1886)": "Henri de Toulouse-Lautrec, <i>Portrait of Émile Bernard</i>, 1886",
    "Autoportrait à la pipe, self-portrait, 1892": "<i>Autoportrait à la pipe</i>, 1892",
    "Natalia Goncharova, Cyclist (1913), oil on canvas, 78×105 cm, State Russian Museum":
        "Natalia Goncharova, <i>The Cyclist</i>, 1913, State Russian Museum",
    "Sergey Schukin by Dm. Melnikov (1915)": "Dmitry Melnikov, <i>Portrait of Sergei Shchukin</i>, 1915",
    "A View of Delft (1652) by Carel Fabritius": "Carel Fabritius, <i>A View of Delft</i>, 1652",
    "The Milkmaid (c. 1657–58) by Johannes Vermeer": "Johannes Vermeer, <i>The Milkmaid</i>, c. 1657–58",
    "The old “Academie of Düsseldorf”, Andreas Achenbach, 1831": "Andreas Achenbach, <i>The Old Academy in Düsseldorf</i>, 1831",
    "Clearing Up—Coast of Sicily, Andreas Achenbach, 1847, The Walters Art Museum":
        "Andreas Achenbach, <i>Clearing Up—Coast of Sicily</i>, 1847, Walters Art Museum",
    "Jolly Flatboatmen in Port, George Caleb Bingham, 1857": "George Caleb Bingham, <i>Jolly Flatboatmen in Port</i>, 1857",
    "Womanhouse, installation and performance space, 1972, organized by Judy Chicago and Miriam Schapiro, at the Feminist Art Program in Fresno, CA.":
        "<i>Womanhouse</i>, by Judy Chicago, Miriam Schapiro, and their students, Los Angeles, 1972",
    "Sheila de Bretteville, Pink, poster, 1973. Provided by the artist.": "Sheila de Bretteville, <i>Pink</i>, poster, 1973",
    "(l-r) Frederick Varley, A.": "The group at the Arts and Letters Club, Toronto, about 1920",
    "Gas Chamber at Seaford, 1918, by Frederick Varley, Canadian War Museum, Ottawa":
        "Frederick Varley, <i>Gas Chamber at Seaford</i>, 1918, Canadian War Museum, Ottawa",
    "The Jack Pine, 1916–17, by Tom Thomson, National Gallery of Canada, Ottawa":
        "Tom Thomson, <i>The Jack Pine</i>, 1916–17, National Gallery of Canada, Ottawa",
    "Shipwreck on a Rocky Coast (1828-39) by Wijnand Nuyen": "Wijnand Nuyen, <i>Shipwreck on a Rocky Coast</i>, 1828–39",
    "Forest View near Barbizon (1900) by Jan Hendrik Weissenbruch": "Jan Hendrik Weissenbruch, <i>Forest View near Barbizon</i>, 1900",
    "Cows at a Pond by Gerard Bilders": "Gerard Bilders, <i>Cows at a Pond</i>",
    "Charles Bell, Circus Act, Silkscreen on Paper, Smithsonian American Art Museum, 1995": "Charles Bell, <i>Circus Act</i>, screenprint, 1995",
    "La hora del té by Mexican painter Magda Torres Gurza [es] (oil on canvas, 90×140 cm)": "Magda Torres Gurza, <i>La hora del té</i>",
    "Aristarkh Lentulov, Woman with a Guitar, 1913": "Aristarkh Lentulov, <i>Woman with a Guitar</i>, 1913",
    "Saint Basil's Cathedral, 1913, Tretyakov Gallery, Moscow.": "Aristarkh Lentulov, <i>Saint Basil's Cathedral</i>, 1913, Tretyakov Gallery, Moscow",
    "Portrait of the artist's family (1911)": "<i>Portrait of the Artist's Family</i>, 1911",
    "Otto Eckmann by Lovis Corinth": "Lovis Corinth, <i>Portrait of Otto Eckmann</i>",
    "Krupp fountain (1912) by Obrist in Munich, Germany.": "Hermann Obrist, <i>Krupp Fountain</i>, 1912, Munich",
    "A simplified version of Cyclamen": "A simplified version of Hermann Obrist's <i>Cyclamen</i>",
    "La Manneporte à Étretat, Claude Monet (1886)": "Claude Monet, <i>La Manneporte, Étretat</i>, 1886",
    "Ensor in front of “Entry of Christ into Brussels” in his house in Ostend, 1940s, photo by Albert Lilar":
        "James Ensor in front of <i>Christ's Entry into Brussels in 1889</i> in his house in Ostend, 1940s",
    "Christ's Entry Into Brussels in 1889 (1888), oil on canvas, 256.8 × 378.4 cm, the Getty Museum":
        "James Ensor, <i>Christ's Entry into Brussels in 1889</i>, 1888, Getty Museum",
    "Singing Beach, Manchester, Massachusetts, 1862": "John Frederick Kensett, <i>Singing Beach, Manchester</i>, 1862",
    "The Artist Sketching at Mount Desert, Maine (1864-1865), National Gallery of Art":
        "Sanford Robinson Gifford, <i>The Artist Sketching at Mount Desert, Maine</i>, 1864–65, National Gallery of Art",
    "The Disquieting Muses by Giorgio de Chirico, 1947": "Giorgio de Chirico, <i>The Disquieting Muses</i>, 1947 version",
    "The Song of Love by Giorgio de Chirico, 1914": "Giorgio de Chirico, <i>The Song of Love</i>, 1914",
    "Carlo Carrà, 1918, L'Ovale delle Apparizioni (The Oval of Apparition), oil on canvas, 92 × 60 cm, Galleria Nazionale d'Arte Moderna, Rome":
        "Carlo Carrà, <i>L'ovale delle apparizioni</i>, 1918, Galleria Nazionale d'Arte Moderna, Rome",
    "Henri Rousseau's The Repast of the Lion (circa 1907, Metropolitan Museum of Art) is an example of naïve art.":
        "Henri Rousseau, <i>The Repast of the Lion</i>, c. 1907, Metropolitan Museum of Art",
    "Alfred Wallis, 1942, before Noah's Ark, Zander Collection": "Alfred Wallis, <i>Noah's Ark</i>, before 1942",
    "Niko Pirosmani, Deer, 1901": "Niko Pirosmani, <i>Deer</i>, 1901",
    "The Munitions Girls, 1918": "Stanhope Forbes, <i>The Munitions Girls</i>, 1918",
    "A Hopeless Dawn, 1888, oil on canvas": "Frank Bramley, <i>A Hopeless Dawn</i>, 1888",
    "Between the Tides, oil on canvas, 1901": "Walter Langley, <i>Between the Tides</i>, 1901",
    "Unknown Venetian artist, The Reception of the Ambassadors in Damascus, 1511, Louvre.":
        "Unknown Venetian artist, <i>The Reception of the Ambassadors in Damascus</i>, 1511, Louvre",
    "Eugène Delacroix, The Women of Algiers, 1834, the Louvre, Paris": "Eugène Delacroix, <i>The Women of Algiers</i>, 1834, Louvre",
    "Jean-Léon Gérôme, The Snake Charmer, c. 1879. Clark Art Institute.": "Jean-Léon Gérôme, <i>The Snake Charmer</i>, c. 1879, Clark Art Institute",
    "Ilya Repin, Barge Haulers on the Volga, 1870–1873": "Ilya Repin, <i>Barge Haulers on the Volga</i>, 1870–73",
    "Ivan Shishkin and Konstantin Savitsky, Morning in a Pine Forest, 1878": "Ivan Shishkin and Konstantin Savitsky, <i>Morning in a Pine Forest</i>, 1889",
    "Paul Gauguin, Watermill in Pont-Aven, 1894, Musée d'Orsay, Paris": "Paul Gauguin, <i>Watermill in Pont-Aven</i>, 1894, Musée d'Orsay",
    "Robert Wylie: La Sorcière bretonne (1872)": "Robert Wylie, <i>La Sorcière bretonne</i>, 1872",
    "Randolph Caldecott, Pont-Aven, 1881": "Randolph Caldecott, <i>Pont-Aven</i>, 1881",
    "In a Tropical Forest Combat of a Tiger and a Buffalo (1908–1909), by Henri Rousseau":
        "Henri Rousseau, <i>In a Tropical Forest: Combat of a Tiger and a Buffalo</i>, 1908–09",
    "The stylistic influences of the African mask of the Fang people are noticeable in the painting Les Demoiselles d'Avignon (1907), by Pablo Picasso.":
        "Pablo Picasso, <i>Les Demoiselles d'Avignon</i>, 1907",
    "Spirit of the Dead Watching (1892), by Paul Gauguin": "Paul Gauguin, <i>Spirit of the Dead Watching</i>, 1892",
    "Amédée Ozenfant, 1920–21, Nature morte (Still Life), oil on canvas, 81.28 cm x 100.65 cm, San Francisco Museum of Modern Art":
        "Amédée Ozenfant, <i>Nature morte</i>, 1920–21, San Francisco Museum of Modern Art",
    "Mikhail Larionov, Red Rayonism, 1913": "Mikhail Larionov, <i>Red Rayonism</i>, 1913",
    "Rayonist Lilies, 1913": "Natalia Goncharova, <i>Rayonist Lilies</i>, 1913",
    "The Talisman, by Paul Sérusier, one of the principal works of the Synthetist school": "Paul Sérusier, <i>The Talisman</i>, 1888",
    "Paul Sérusier, The Talisman (1888); oil on wood, 27 x 21.5 cm. Musée d'Orsay, Paris": "Paul Sérusier, <i>The Talisman</i>, 1888, Musée d'Orsay",
    "In the Berkshires, 1850": "George Inness, <i>In the Berkshires</i>, 1850",
    "The Lackawanna Valley, c. 1856, National Gallery of Art": "George Inness, <i>The Lackawanna Valley</i>, c. 1856, National Gallery of Art",
    "Lake Albano, 1869, Phillips Collection": "George Inness, <i>Lake Albano</i>, 1869, Phillips Collection",
    "James McNeill Whistler, a Nocturne": "James McNeill Whistler, a <i>Nocturne</i>",
    "The Delivery of the Keys fresco, 1481–1482, Sistine Chapel, Rome": "Pietro Perugino, <i>The Delivery of the Keys</i>, 1481–82, Sistine Chapel",
    "“Mandarin Ducks” by Hiroshige, digitally restored.": "Hiroshige, <i>Mandarin Ducks</i>",
    "Wind Blown Grass Across the Moon, by Hiroshige, probably around 1832": "Hiroshige, <i>Wind-Blown Grass across the Moon</i>, c. 1832",
    "Giovanni Bellini, San Zaccaria Altarpiece, 1505, a late work, San Zaccaria, Venice":
        "Giovanni Bellini, <i>San Zaccaria Altarpiece</i>, 1505, San Zaccaria, Venice",
    "Paolo Veneziano, polyptych altarpiece with Coronation of the Virgin, c. 1350":
        "Paolo Veneziano, polyptych with the <i>Coronation of the Virgin</i>, c. 1350",
    "Carlo Crivelli, The Annunciation, with St. Emidius, 1486": "Carlo Crivelli, <i>The Annunciation, with Saint Emidius</i>, 1486",
    "Pre-Bell-Man, Nam June Paik, 1989": "Nam June Paik, <i>Pre-Bell-Man</i>, 1989",
    "A still from Jonas' 1972 video": "A still from Joan Jonas's 1972 video",
    "Edward Wadsworth, Vorticist Study, 1914, Museo Thyssen-Bornemisza, Madrid":
        "Edward Wadsworth, <i>Vorticist Study</i>, 1914, Museo Thyssen-Bornemisza, Madrid",
    "Rock Drill in Jacob Epstein's studio c.1913": "Jacob Epstein's <i>Rock Drill</i> in his studio, c. 1913",
    "The Dancers Wyndham Lewis, 1912": "Wyndham Lewis, <i>The Dancers</i>, 1912",
    "Canaries by Albert Joseph Moore, ca. 1875–1880.": "Albert Joseph Moore, <i>Canaries</i>, c. 1875–80",
    "“Lady Lilith” by Dante Gabriel Rossetti": "Dante Gabriel Rossetti, <i>Lady Lilith</i>",
    "Adolf Wölfli's Irren-Anstalt Band-Hain, 1910": "Adolf Wölfli, <i>Irren-Anstalt Band-Hain</i>, 1910",
    "Anna Zemánková, No title, 1960s": "Anna Zemánková, <i>Untitled</i>, 1960s",
    "Score for Die Walküre; the Ring cycle was Wagner's most complete articulation of his idea of Gesamtkunstwerk.":
        "A page of the score of Richard Wagner's <i>Die Walküre</i>",
    "Portrait of West from 1770, now housed in the National Portrait Gallery in Washington, D.C.":
        "A portrait of Benjamin West, 1770, National Portrait Gallery, Washington",
    "John Talbot, later 1st Earl Talbot, 1773. J. Paul Getty Museum, Los Angeles":
        "Pompeo Batoni, <i>John Talbot, later 1st Earl Talbot</i>, 1773, Getty Museum",
    "Raphael, The Expulsion of Heliodorus from the Temple, from the Vatican, 1512. The original grand manner.":
        "Raphael, <i>The Expulsion of Heliodorus from the Temple</i>, 1512, Vatican",
    "The Agony in the Garden with the Donor Louis I, Duke of Orléans, Colart de Laon, c. 1405-1408, Prado Museum":
        "Colart de Laon, <i>The Agony in the Garden with the Donor Louis I, Duke of Orléans</i>, c. 1405–08, Prado",
    "Detail of the Annunciation (1333) by the Sienese Simone Martini, Uffizi": "Simone Martini, <i>The Annunciation</i> (detail), 1333, Uffizi",
    "Lorenzo Monaco, The Flight into Egypt (c. 1405, predella) Tempera on poplar, 21,2 x 35,5 cm":
        "Lorenzo Monaco, <i>The Flight into Egypt</i>, predella panel, c. 1405",
    "Naum Gabo, Kinetic Construction, also titled Standing Wave (1919–20)": "Naum Gabo, <i>Kinetic Construction</i> (<i>Standing Wave</i>), 1919–20",
    "Jean Tinguely, Eos (1965)": "Jean Tinguely, <i>Eos</i>, 1965",
    "George Rickey, Four Squares in Square Arrangement (1969), terrace of the New National Gallery, Berlin":
        "George Rickey, <i>Four Squares in Square Arrangement</i>, 1969, Neue Nationalgalerie, Berlin",
    "Eilif Peterssen, Summer Night (1886)": "Eilif Peterssen, <i>Summer Night</i>, 1886",
    "Francisco Goya, Charles IV of Spain and His Family, 1800–01": "Francisco Goya, <i>Charles IV of Spain and His Family</i>, 1800–01",
    "Henri Biva, Matin à Villeneuve, c. 1905–06": "Henri Biva, <i>Matin à Villeneuve</i>, c. 1905–06",
    "Alexander Kanoldt, Still Life with Jugs and Red Tea Caddy (1922)": "Alexander Kanoldt, <i>Still Life with Jugs and Red Tea Caddy</i>, 1922",
    "Hans Mertens, Card Players, 1929": "Hans Mertens, <i>Card Players</i>, 1929",
    "A Friend in Need, a 1903 Dogs Playing Poker painting by Cassius Marcellus Coolidge, is a common example of kitsch.":
        "Cassius Marcellus Coolidge, <i>A Friend in Need</i>, from the <i>Dogs Playing Poker</i> series, 1903",
    "Puppy by Jeff Koons (2010) is a self-aware display of kitsch, specifically as a combination of opulence and cuteness.":
        "Jeff Koons, <i>Puppy</i>",
    "Graham Sutherland, Devastation, 1941: East End, Wrecked Public House": "Graham Sutherland, <i>Devastation, 1941: East End, Wrecked Public House</i>",
    "Julian Opie, Shaida Walking , Broadwick Street, Soho, London": "Julian Opie, <i>Shaida Walking</i>, Broadwick Street, Soho, London",
    "Eduardo Paolozzi, Newton , after William Blake, British Library, London": "Eduardo Paolozzi, <i>Newton</i>, after William Blake, British Library, London",
    "Piero di Cosimo, Perseus Freeing Andromeda , c. 1510–15": "Piero di Cosimo, <i>Perseus Freeing Andromeda</i>, c. 1510–15",
    "Konrad Witz, Saint Christopher , Kunstmuseum Basel": "Konrad Witz, <i>Saint Christopher</i>, Kunstmuseum Basel",
    "A Painter Smoking a Pipe , thought to be Jan Davidsz. de Heem (follower of Adriaen Brouwer)":
        "<i>A Painter Smoking a Pipe</i>, thought to be Jan Davidsz. de Heem (follower of Adriaen Brouwer)",
    "Self-portrait with wide-open eyes III, 1912": "<i>Self-Portrait with Wide-Open Eyes III</i>, 1912",
    "Self-portrait as David with the head of Goliath": "<i>Self-Portrait as David with the Head of Goliath</i>",
    "Kroisos Kouros, c. 530 BCE": "The <i>Kroisos Kouros</i>, c. 530 BCE",
    "Kleobis and Biton c. 580 BCE (Delphi: Archaeological Museum)": "<i>Kleobis and Biton</i>, c. 580 BCE, Delphi Archaeological Museum",
    "The Barberini Faun, 2nd-century BCE Hellenistic or 2nd-century CE Roman copy of an earlier bronze":
        "The <i>Barberini Faun</i>, a Hellenistic marble of the 2nd century BCE or a Roman copy of an earlier bronze",
    "Barberini Ivory, Constantinople, 6th century, Louvre": "The <i>Barberini Ivory</i>, Constantinople, 6th century, Louvre",
    "Scene from the Alexander Sarcophagus": "A scene from the <i>Alexander Sarcophagus</i>",
    "The Hellenistic Pergamon Altar: l to r Nereus, Doris, a Giant, Oceanus": "The Hellenistic <i>Pergamon Altar</i>: Nereus, Doris, a Giant, and Oceanus",
    "Hiroshige studied under Toyohiro of the Utagawa school of artists.Returning Sails at Tsukuda by Toyohiro, from Eight Views of Edo, between 1802 and 1829":
        "Utagawa Toyohiro, Hiroshige's teacher, <i>Returning Sails at Tsukuda</i>, from <i>Eight Views of Edo</i>, 1802–29",
}


def main(apply):
    ids = C.anki("findNotes", query="note:Art")
    notes = {}
    for i in range(0, len(ids), 400):
        for n in C.anki("notesInfo", notes=ids[i:i + 400]):
            notes[n["noteId"]] = n
    changes, used = {}, set()
    for nid, f in FIELDS.items():
        changes.setdefault(nid, {}).update(f)
    for (nid, k), reps in REPL.items():
        v = changes.get(nid, {}).get(k, notes[nid]["fields"][k]["value"])
        for old, new in reps:
            assert old in v, (nid, old)
            v = v.replace(old, new)
        changes.setdefault(nid, {})[k] = v
    for nid, n in notes.items():
        caps = changes.get(nid, {}).get("Captions", n["fields"]["Captions"]["value"])
        parts = caps.split(" | ")
        new = []
        for p in parts:
            key = p.strip()
            if key in CAPS:
                used.add(key)
                new.append(CAPS[key])
            else:
                new.append(p)
        if new != parts:
            changes.setdefault(nid, {})["Captions"] = " | ".join(new)
    for k in CAPS:
        if k not in used:
            print("UNUSED:", k[:90])
    backup = {}
    for nid, f in changes.items():
        backup[nid] = {k: notes[nid]["fields"][k]["value"] for k in f}
        for k, v in f.items():
            if v != backup[nid][k]:
                print(nid, k, "\n   ", backup[nid][k][:200], "\n -> ", v[:200])
    print(len(changes), "notes")
    if not apply:
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump(backup, open(os.path.join(HERE, "backups", "art_text_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    for nid, f in changes.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": f})
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
