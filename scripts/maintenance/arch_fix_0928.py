# -*- coding: utf-8 -*-
"""arch_fix_0928.py -- Architecture text and pictures, after reading all 181 active notes.

Carter, 2026-09-28: main decks first (Art, Classical Music, Architecture). Read the way the Music
deck was read (every active note, every field). Fixed here:

  * Descriptions carried over from the original deck that were one-line encyclopaedia stubs
    ("Roman Catholic basilica. Seat of the Patriarch of Venice."; "Iconic triangular building,
    landmark of New York City."; the Milwaukee Art Museum described by its collection size, not its
    Calatrava pavilion) are rewritten to say what the building is and looks like.
  * Wrong: the Tempietto is not "a tomb inside" San Pietro in Montorio; it is a martyrium in the
    church's courtyard. Sinan's works led with the Ferhat Pasha Mosque in Banja Luka, which is by
    his school, and left out the Selimiye.
  * Pictures that are not the building or the idea, and which the PICTURE to NAME front shows as
    clues: a Vishnu statue and Khmer Rouge bullet holes on Angkor Wat, a Michelangelo painting on
    the Kimbell, a Neolithic bowl on Knossos, a bronze actor on Theatre, the Brussels KANAL offshoot
    on the Centre Pompidou, a 2006 memorial on the Tower of London, the pre-1950 chapel on Ronchamp,
    a Louis IX statue on Sacré-Cœur, a Russian suburb on Brutalism, a colossal statue on Rock-cut
    architecture, the Rotunda of Galerius on Flying buttress, a brick building on Timber framing.
    Each is removed and the rest move up. (Replacements for cards left thin, and for figure and
    style cards whose pictures are not architecture at all, are in arch_img_0928.py.)
  * Captions copied whole from Wikipedia ("...remarkably carved out of one single rock was built
    by...") are trimmed to what the picture shows, without full stops; "--" becomes a dash.

    py -3.9 arch_fix_0928.py [--apply]
"""
import json, re, sys, time
import concept_add as C

DESC = {
 1596562390534: "The Nasrid palace-fortress on a hill above Granada, the last seat of Muslim rule in Spain, famed for the stucco, tile, and <i>muqarnas</i> of its courts; Charles V later built a Renaissance palace inside it.",
 1593009867773: "Venice's cathedral, a Greek cross of five domes modelled on Constantinople's Church of the Holy Apostles, its interior sheathed in gold-ground mosaics.",
 1593547961220: "The papal chapel in the Vatican, built for Sixtus IV and named after him, where the conclave meets; Michelangelo painted its ceiling (1508–1512) and the <i>Last Judgment</i> on the altar wall.",
 1593009380026: "Gaudí's basilica, begun in 1882 and still unfinished, with tree-like columns that branch toward the vault and a skyline of spires; Gaudí is buried in its crypt.",
 1593009314115: "Nine chapels grouped around a central tower on Red Square, each crowned by a brightly patterned onion dome.",
 1593551586528: "A performing-arts centre on Bennelong Point whose roof is a cluster of white shell vaults, all cut from the surface of a single sphere and clad in over a million tiles.",
 1593550505904: "A wedge-shaped, steel-framed skyscraper filling the triangular block where Broadway crosses Fifth Avenue at Madison Square, clad in limestone and terracotta.",
 1596737242097: "Santiago Calatrava's Quadracci Pavilion on Lake Michigan, whose Burke Brise Soleil, a pair of steel wings, opens and closes over the glass hall like a bird's.",
 1593549264185: "Hadrian's temple to all the gods: a porticoed rotunda under an unreinforced concrete dome with an open oculus, consecrated as a church in 609, which saved it.",
 1593547415798: "Bramante's small circular martyrium in the courtyard of San Pietro in Montorio, marking the traditional site of Saint Peter's crucifixion; the first building of the High Renaissance.",
 1593547614907: "Florence's great Dominican church: a Gothic nave behind a marble façade that Alberti completed by setting a classical temple front, joined by scrolled volutes, on the Gothic lower storey.",
 1594917446718: "An octagonal shrine under a gilded dome on the Temple Mount, built over the Foundation Stone, which is sacred to Jews, Christians, and Muslims.",
 1788620819847: "German founder and first director of the Bauhaus, whose Fagus Factory and Dessau school building made the glass curtain wall a modernist signature; he later taught at Harvard.",
 1596036791632: "The medieval style of pointed arches, rib vaults, and flying buttresses, which let churches rise higher and turn their walls into stained glass; it began in Abbot Suger's choir at Saint-Denis around 1140.",
 1788620599062: "Rome's largest fountain, an 18th-century Baroque work: Oceanus rides a shell chariot drawn by two sea horses, one calm and one wild.",
}

# nid -> {caption number (as the picture now stands): new caption}
CAP = {
 1790240143434: {2: "The White Tower, the keep of the Tower of London", 4: "Vidin Castle on the Danube, Bulgaria"},
 1790240143505: {3: "Oriel Chambers, Liverpool (1864), an early iron frame behind a glass curtain wall",
                 4: "Palacio Salvo, Montevideo (1928), once the tallest reinforced-concrete building"},
 1790240144024: {2: "Diagram of a Nagara-style Hindu temple", 3: "The temples at Pattadakal, 7th–8th century",
                 4: "The Kailasa temple at Ellora, carved from a single rock under the Rashtrakuta king Krishna I (r. 756–773)"},
 1790240143995: {2: "The Mosque of the Prophet, Medina, on the site of Muhammad's first mosque",
                 3: "The Umayyad Mshatta façade, from a palace near Amman, now in the Pergamon Museum, Berlin"},
 1790240143306: {2: "The theatre at Epidaurus, which Pausanias called the finest in Greece"},
 1790240143566: {2: "Nonsuch Palace, in a detail of Georg Hoefnagel's 1568 watercolour",
                 3: "Carved timber framing on a house in Strasbourg"},
 1788620884245: {2: "Vitra Fire Station, Weil am Rhein (1993)"},
 1788620599062: {2: "The fountain in an 18th-century painting by Giovanni Paolo Panini"},
 1788489927368: {1: "Vitruvius (c. 80–15 BCE)"},
}

# nid -> picture numbers to remove (pictures after them move up)
REMOVE = {
 1596400691402: [2, 3],   # Angkor Wat: Vishnu statue, bullet holes
 1788200166517: [2],      # Kimbell: Michelangelo painting
 1788620580153: [2],      # Knossos: Neolithic bowl
 1790240143306: [2],      # Theatre: bronze actor statue
 1788200177314: [3],      # Centre Pompidou: KANAL, Brussels
 1788200031786: [3],      # Tower of London: 2006 memorial
 1788200153918: [2],      # Ronchamp: the earlier chapel
 1593010082787: [3],      # Sacré-Cœur: statue of Louis IX
 1788585240715: [2],      # Brutalism: Talnakh suburb
 1790240144093: [3],      # Rock-cut: Gommateshwara statue
 1788585237929: [2],      # Flying buttress: Rotunda of Galerius
 1790240143566: [3],      # Timber framing: Rokumeikan (brick)
}

WORKS = {1788621011600: "<u>Süleymaniye Mosque</u>; Selimiye Mosque (Edirne); Şehzade Mosque; Mihrimah Sultan Mosque"}


def plan():
    ids = sorted(set(DESC) | set(CAP) | set(REMOVE) | set(WORKS))
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=ids)}
    ch = []
    for nid in ids:
        n = ns[nid]
        F = {k: v["value"] for k, v in n["fields"].items()}
        f = {}
        pics = [(F["Picture %d" % i], F["Caption %d" % i]) for i in range(1, 5)]
        if nid in REMOVE:
            keep = [p for i, p in enumerate(pics, 1) if i not in REMOVE[nid]]
            keep += [("", "")] * (4 - len(keep))
            for i, (p, c) in enumerate(keep, 1):
                f["Picture %d" % i], f["Caption %d" % i] = p, c
            pics = keep
        for i, c in CAP.get(nid, {}).items():
            f["Caption %d" % i] = c
        if nid in DESC:
            f["Description"] = DESC[nid]
        if nid in WORKS:
            f["Works"] = WORKS[nid]
        f = {k: v for k, v in f.items() if v != F[k]}
        if f:
            ch.append((n, f))
    # "--" used as a dash anywhere in Architecture prose
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='note:Architecture "Description:*--*" OR note:Architecture "Notes:*--*"')):
        f = next((x[1] for x in ch if x[0]["noteId"] == n["noteId"]), None)
        for k in ("Description", "Notes"):
            v = (f or {}).get(k, n["fields"][k]["value"])
            if " -- " in v:
                if f is None:
                    f = {}
                    ch.append((n, f))
                f[k] = v.replace(" -- ", " — ")
    return ch


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    for n, f in ch:
        print("##", C.plain(n["fields"]["Name"]["value"]), sorted(f))
    print(len(ch), "notes")
    if "--apply" in sys.argv:
        json.dump([{"nid": n["noteId"], **{k: n["fields"][k]["value"] for k in f}} for n, f in ch],
                  open("backups/arch_fix_0928_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, f in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": f})
        print("applied")
