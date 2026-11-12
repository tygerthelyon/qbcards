# -*- coding: utf-8 -*-
"""cm_heard_in.py -- concept cards: "Heard in" as one phrase, and the Detail line cleaned.

Carter, 2026-09-28: "heard in field separates Beethoven and ninth symphony: does this mean it is
heard in Beethoven works, as well as some ninth symphony? It is unusual to separate the two. If
you say something is x language for y, then it is customary to put y in quotation marks."

"Beethoven · Symphony No. 9" -> "Beethoven's <i>Symphony No. 9</i>"; garbled ones repaired
("Mendelssohn · Violin, E minor, Op. 64" -> the Violin Concerto in E minor). Famous composers by
surname, others in full. Details: glosses quoted, repeats of the Heard-in example replaced, stray
italics fixed, bare surnames of lesser-known figures given in full.

    py -3.9 cm_heard_in.py [--apply]
"""
import json, sys, time
import concept_add as C


def I(t):
    return "<i>%s</i>" % t


HEARD = {
    1788585500470: "Mozart's " + I("Piano Sonata No. 16"),
    1790365377131: "Puccini's " + I("Gianni Schicchi"),
    1790365377723: "John Gay's " + I("The Beggar's Opera"),
    1790448082619: "Jacques Offenbach's " + I("The Tales of Hoffmann"),
    1790365379137: "Mozart's " + I("Requiem"),
    1790448081810: "the opening solo of Stravinsky's " + I("The Rite of Spring"),
    1788585499376: "Vincenzo Bellini's " + I("Norma"),
    1788585501096: "Mozart's " + I("Piano Concerto No. 21"),
    1788585498436: "Pachelbel's " + I("Canon in D"),
    1790365378285: "Tchaikovsky's " + I("The Nutcracker"),
    1790448081614: "Bach's cello suites",
    1788585498574: "Bach's " + I("Partita No. 2") + " for solo violin",
    1790365377931: "Schumann's " + I("Kinderszenen"),
    1790365379014: "Britten's " + I("Curlew River"),
    1790365379077: "Zoltán Kodály's " + I("Háry János"),
    1790448081490: "Mozart's Clarinet Concerto, K. 622",
    1788585501150: "Mozart's " + I("Die Zauberflöte"),
    1790448082025: "Mendelssohn's Violin Concerto in E minor",
    1788585498979: "Bach's " + I("Brandenburg Concerto No. 3"),
    1790365378258: "Dvořák's " + I("Symphony No. 9"),
    1790365378030: "Britten's " + I("A Midsummer Night's Dream"),
    1788585498637: "Handel's " + I("Giulio Cesare"),
    1790365377157: "Berlioz's " + I("Symphonie fantastique"),
    1790448081966: "“The Elephant” from Saint-Saëns's " + I("Carnival of the Animals"),
    1790448081465: "Debussy's " + I("Syrinx"),
    1790448081749: "Mozart's horn concertos, written for Joseph Leutgeb",
    1788585498398: "Bach's " + I("The Art of Fugue"),
    1790365378216: "Colin McPhee's " + I("Tabuh-Tabuhan"),
    1790365379108: "Donizetti's " + I("Lucia di Lammermoor"),
    1790365377629: "Giacomo Meyerbeer's " + I("Les Huguenots"),
    1788585498467: "Purcell's " + I("Dido and Aeneas"),
    1790448081873: "Joaquín Rodrigo's " + I("Concierto de Aranjuez"),
    1790448081841: "Debussy's " + I("Danses sacrée et profane"),
    1790448081902: "Bach's " + I("Goldberg Variations"),
    1788585501311: "Berlioz's " + I("Symphonie fantastique"),
    1788585500125: "Chopin's " + I("Fantaisie-Impromptu"),
    1790365377834: "Grieg's " + I("Peer Gynt"),
    1790365377803: "Giovanni Battista Pergolesi's " + I("La serva padrona"),
    1788585501251: "Wagner's " + I("Die Walküre"),
    1788585499404: "Schubert's " + I("Erlkönig"),
    1790365377963: "Donizetti's " + I("Lucia di Lammermoor"),
    1790365378093: "Mozart's " + I("Symphony No. 40"),
    1790448082178: "John Philip Sousa's " + I("The Stars and Stripes Forever"),
    1790365377684: "John Blow's " + I("Venus and Adonis"),
    1790448082089: "Bach's " + I("Mass in B minor"),
    1788585500157: "Chopin's Mazurka in D minor",
    1790365378780: "Carl Maria von Weber's " + I("Der Freischütz"),
    1790365378819: "Aribert Reimann's " + I("Lear"),
    1788585501590: "Philip Glass's " + I("Einstein on the Beach"),
    1788585498757: "Mozart's " + I("Symphony No. 40"),
    1788585499497: "Thomas Tallis's " + I("Spem in alium"),
    1788585499715: "Chopin's Nocturne in E-flat major, Op. 9 No. 2",
    1790448081717: "Mozart's Oboe Concerto, K. 314",
    1790365379042: "Olivier Messiaen's " + I("Turangalîla-Symphonie"),
    1788585499171: "Handel's " + I("Giulio Cesare"),
    1790365377774: "Franz Lehár's " + I("The Merry Widow"),
    1790365377597: "Bizet's " + I("Carmen"),
    1790365378736: "Jean-Philippe Rameau's " + I("Les Indes galantes"),
    1788585499075: "Handel's " + I("Messiah"),
    1790448081933: "Bach's " + I("Toccata and Fugue in D minor"),
    1788585500503: "Ravel's " + I("Boléro"),
    1788585500007: "Dvořák's " + I("Carnival Overture"),
    1790365378889: "Josquin des Prez's " + I("Missa Pange lingua"),
    1790448081583: "Chopin's nocturnes",
    1790448082588: "Beethoven's “Archduke” Trio, Op. 97",
    1788585500186: "Chopin's “Heroic” Polonaise",
    1788585499806: "Debussy's " + I("Prelude to the Afternoon of a Faun"),
    1788585501388: "Berlioz's " + I("Symphonie fantastique"),
    1790365378850: "Giovanni Battista Pergolesi's " + I("La serva padrona"),
    1790365378981: "Bach's " + I("Goldberg Variations"),
    1790448082210: "Scott Joplin's " + I("The Entertainer"),
    1790365377103: "Mozart's " + I("Don Giovanni"),
    1788585499466: "the “Dies irae” of Berlioz's " + I("Requiem"),
    1788585500038: "Gershwin's " + I("Rhapsody in Blue"),
    1788585498599: "Vivaldi's " + I("The Four Seasons"),
    1788585498250: "Mozart's “Rondo alla turca”",
    1790448081654: "“The Old Castle” in Ravel's orchestration of " + I("Pictures at an Exhibition"),
    1788585498816: "Beethoven's " + I("Symphony No. 9"),
    1790365378608: "Purcell's " + I("The Fairy-Queen"),
    1790365377897: "Mozart's " + I("Eine kleine Nachtmusik"),
    1788585499013: "the finale of Haydn's " + I("Sinfonia Concertante"),
    1788585499272: "Mozart's " + I("Die Zauberflöte"),
    1790365378951: "Guido of Arezzo's hymn " + I("Ut queant laxis"),
    1790448082148: "Beethoven's “Moonlight” Sonata",
    1788585498183: "Mozart's " + I("Symphony No. 40"),
    1788585499437: "Schubert's " + I("Winterreise"),
    1788585501217: "Schoenberg's " + I("Pierrot lunaire"),
    1790448081993: "Beethoven's String Quartet in C-sharp minor, Op. 131",
    1790365378122: "Haydn's “Farewell” Symphony",
    1790365377864: "Handel's " + I("Water Music"),
    1788585498953: "Richard Strauss's " + I("Also sprach Zarathustra"),
    1790448082118: "Beethoven's " + I("Symphony No. 5"),
    1788585498345: "Bach's " + I("Goldberg Variations"),
    1790448082525: "Haydn's “Drumroll” Symphony",
    1788585499840: "Bach's " + I("Toccata and Fugue in D minor"),
    1790365378148: "Henry Cowell's " + I("The Tides of Manaunaun"),
    1790365378685: "Jean-Baptiste Lully's " + I("Armide"),
    1790365377197: "Wagner's " + I("Tristan und Isolde"),
    1790448081779: "“Tuba mirum” from Mozart's " + I("Requiem"),
    1790365377998: "Richard Strauss's " + I("Der Rosenkavalier"),
    1790448081521: "Haydn's Trumpet Concerto",
    1788585499345: "Ruggero Leoncavallo's " + I("Pagliacci"),
    1790448081685: "Berlioz's " + I("Harold en Italie"),
    1790448081552: "Vivaldi's " + I("The Four Seasons"),
    1790448082056: "Johann Strauss II's " + I("The Blue Danube"),
    1788585500935: "Debussy's " + I("Prelude to the Afternoon of a Faun"),
    1788585499747: "Chopin's “Revolutionary” Étude, Op. 10 No. 12",
}
# Detail line (the Nickname field on concept notes): whole replacements
DETAIL = {
    1788585498816: "Italian for “joke”; Beethoven made it the standard replacement for the minuet.",
    1788585501557: "A medieval device, from the word for “hiccup”.",
    1788585501063: "Literally “robbed time”; associated above all with Frédéric Chopin.",
    1788585499840: "From the Italian for “touched”; Bach's D minor for organ is the famous one.",
    1788585498716: "<i>Durchkomponiert</i>; Franz Schubert's “Erlkönig” is the standard example.",
    1788585501525: "The rhythmic unit is the <i>talea</i>, the pitch unit the <i>color</i>; Guillaume de Machaut and Guillaume Du Fay use it.",
    1788585499272: "<i>The Magic Flute</i> and <i>The Abduction from the Seraglio</i> are Mozart's.",
    1788585501311: "Berlioz's own term; an ancestor of Wagner's <i>leitmotif</i>.",
    1788585499075: "Haydn's <i>The Creation</i> is the other standard example; a narrator often carries the plot.",
    1788585501217: "Half-sung, half-spoken: the voice touches the notated pitch and leaves it. Berg uses it in <i>Wozzeck</i>.",
    1790365378093: "A fast rising arpeggio, the signature of Johann Stamitz's Mannheim orchestra; Beethoven's first piano sonata opens with one.",
    1788585501590: "Terry Riley, Steve Reich, Philip Glass, and John Adams.",
    1788585500871: "Milton Babbitt, Pierre Boulez, and Karlheinz Stockhausen carried it beyond pitch after 1945.",
}
# Motet: a composer's name was italicised
FIXES = {1788585499497: [("<i>Giovanni Pierluigi da Palestrina</i>", "Giovanni Pierluigi da Palestrina")]}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ids = sorted(set(HEARD) | set(DETAIL) | set(FIXES))
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=ids)}
    assert len(ns) == len(ids), set(ids) - set(ns)
    ch = []
    for nid in ids:
        n = ns[nid]
        new = {}
        if nid in HEARD:
            new["Composer"] = HEARD[nid]
        if nid in DETAIL:
            new["Nickname"] = DETAIL[nid]
        for a, b in FIXES.get(nid, []):
            new["Nickname"] = new.get("Nickname", n["fields"]["Nickname"]["value"]).replace(a, b)
        ch.append((n, new))
        print(C.plain(n["fields"]["Work"]["value"])[:22].ljust(22), "|", " | ".join(C.plain(v)[:70] for v in new.values()))
    if "--apply" in sys.argv:
        json.dump([{"nid": n["noteId"], "fields": {k: n["fields"][k]["value"] for k in new}} for n, new in ch],
                  open("backups/cm_heard_in_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, new in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": new})
        print("applied", len(ch))
