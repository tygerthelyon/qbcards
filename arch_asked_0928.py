# -*- coding: utf-8 -*-
"""arch_asked_0928.py -- buildings quizbowl asks about: add the missing, wake the suspended.

Carter, 2026-09-28: "check which asked-about buildings are missing (one appearance on qbreader does
not classify as being "asked about")." Every Architecture tossup on qbreader (1,250, fetched into
_qb_pool_other_fine_arts_architecture.json) was searched for building names; a building counts as
asked about when three or more different tossups name it. Buildings are seldom the answer line --
they are the clues in questions on their architects -- which is why tiering by answer lines had
suspended the Gateway Arch (57 tossups), the Imperial Hotel (27), the World Trade Center (22),
Chartres, and Westminster Abbey.

  WAKE: 24 suspended notes named in 3+ tossups become tier 1 (One World Trade Center and Pisa
        Cathedral stay suspended; the questions are about the Twin Towers and the Leaning Tower).
        Their faults are fixed first: the Imperial Hotel's only picture was the 1890 hotel Wright's
        replaced; the Crystal Palace showed its empty Sydenham site; Chartres showed an organ and an
        altar group; Petronas, the Gateway Arch, and Westminster Abbey carried a fountain, a visitor
        centre door, and a postcard; Villa Tugendhat's captions were "Exteriér Vila Tugendhat".
  ADD:  33 buildings named in 4+ tossups (and 7 canonical ones named in 3) that the deck lacked,
        from the Rock and Roll Hall of Fame (30) and the Palace of Westminster to Penn Station.
        Pictures from Commons, chosen on contact sheets.

    py -3.9 arch_asked_0928.py [--apply]
"""
import json, os, sys, time
from PIL import Image
import concept_add as C

SRC = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/4c6fe2ff-c3a6-47fb-8b54-226f916ad6af/scratchpad/img/"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
T1 = "Architecture::tier::tier1-core"

WAKE = [1788200170777, 1790355287070, 1787878329517, 1790355291509, 1788200212434, 1787878329521,
        1790355287730, 1790355289415, 1788200199758, 1788200208301, 1788620628235, 1788200221116,
        1788200016970, 1788200047211, 1788200159507, 1790355287512, 1593546551904, 1594919963375,
        1787878329481, 1788200140825, 1788620672572, 1788620630336, 1788620670320, 1788200189815,
        1787878329524, 1788200040759, 1593545681195]

# (scratch image, media name, caption) per picture slot; None clears the slot
FIX = {
 1790355287070: {"pics": [("ar_imperial2_0.jpg", "arch-imperial-hotel-elevations.jpg", "Wright's elevations and sections for the hotel"),
                          ("ar_imperial_1.jpg", "arch-imperial-hotel-lobby.jpg", "Oya stone and Wright's chairs in the lobby, re-erected at Meiji Mura")]},
 1788200221116: {"pics": [("ar_crystalpal2_0.jpg", "arch-crystal-palace-1851.jpg", "The Crystal Palace in Hyde Park, 1851"),
                          ("ar_crystalpal2_3.jpg", "arch-crystal-palace-transept.jpg", "The transept, built high enough to enclose the park's elms")]},
 1593546551904: {"slots": {2: ("ar_chartres_glass_0.jpg", "arch-chartres-north-rose.jpg", "The north rose window"),
                           3: ("ar_chartres_portal_0.jpg", "arch-chartres-royal-portal.jpg", "The Royal Portal of the west front, in a 19th-century photograph")},
                 "Description": "The best-preserved High Gothic cathedral, rebuilt in about thirty years after a fire of 1194; it keeps most of its 12th- and 13th-century stained glass and the Royal Portal of its earlier west front."},
 1594919963375: {"slots": {3: None},
                 "Description": "Twin 88-storey towers in Kuala Lumpur joined by a skybridge, their plan an eight-pointed Islamic star; the tallest buildings in the world from 1998 to 2004."},
 1788200170777: {"slots": {2: None}},
 1788200016970: {"slots": {2: "MOVE3"}},
 1788620670320: {"captions": {1: "The garden front", 2: "The terrace under the upper floor"}},
}

B = []   # (Name, Alternate, Location, Date, Style, Main style, Architect, Description, Notes, flags, tags, pics)
def add(name, alt, loc, date, style, main, arch, desc, notes, pics, tags, nametells=False, foreign=False):
    B.append(dict(Name=name, Alternate=alt, Location=loc, Date=date, Style=style, **{"Main style": main}, Architect=arch,
                  Description=desc, Notes=notes, pics=pics, tags=tags, NameTells="1" if nametells else "",
                  Foreign="1" if foreign else ""))

NA, EU, AS, OC = "north-america", "europe", "asia", "oceania"
add("Rock and Roll Hall of Fame", "", "Cleveland, Ohio, United States", "1993–1995", "Modernism", "Modernism", "I. M. Pei",
    "A glass tent-pyramid on the shore of Lake Erie, from which a tower and cantilevered geometric volumes project over the water.",
    "Pei, who knew little about rock, toured music venues with the museum's founders before designing it; the pyramid recalls his Louvre entrance.",
    [("ar_rrhof_0.jpg", "The glass pyramid facing the plaza"), ("ar_rrhof_2.jpg", "The cantilevered volumes at night")], [NA, "contemporary", "cultural", "modernist"])
add("Jay Pritzker Pavilion", "", "Chicago, Illinois, United States", "1999–2004", "Deconstructivism", "Deconstructivism", "Frank Gehry",
    "An outdoor concert stage framed by curling ribbons of brushed stainless steel, with a trellis of crisscrossing steel pipes carrying the sound system over the lawn.",
    "The centrepiece of Millennium Park, beside Anish Kapoor's <i>Cloud Gate</i>; because building heights were limited in Grant Park, the city classed it as a work of art.",
    [("ar_pritzker_0.jpg", "The stage and the steel trellis over the Great Lawn")], [NA, "contemporary", "cultural", "deconstructivist"])
add("John F. Kennedy Presidential Library", "", "Boston, Massachusetts, United States", "1977–1979", "Modernism", "Modernism", "I. M. Pei",
    "A white concrete triangular tower beside a black glass pavilion ten storeys high and almost empty inside, on a point overlooking Boston Harbor.",
    "Jacqueline Kennedy chose Pei in 1964; the library was meant for Harvard's campus, but local opposition moved it to Columbia Point.",
    [("ar_jfklib2_0.jpg", "The concrete block and the glass pavilion")], [NA, "contemporary", "cultural", "modernist"])
add("John Hancock Tower", "200 Clarendon Street", "Boston, Massachusetts, United States", "1972–1976", "Modernism", "Modernism", "Henry N. Cobb (I. M. Pei & Partners)",
    "A sixty-storey rhomboid slab sheathed entirely in reflective blue glass beside Trinity Church, which appears in its façade.",
    "Soon after completion its windows began to fall out, and all 10,344 panes were replaced; Boston's tallest building.",
    [("ar_hancock_2.jpg", "The tower above Copley Square")], [NA, "contemporary", "skyscraper", "modernist"])
add("Central Park", "", "New York City, United States", "1857–1876", "Picturesque landscape", "Landscape architecture", "Frederick Law Olmsted; Calvert Vaux",
    "An 843-acre landscaped park in the middle of Manhattan, laid out as meadows, woods, and lakes, with sunken transverse roads carrying cross-town traffic out of sight.",
    "Olmsted and Vaux's Greensward Plan won the 1858 competition; Vaux designed Bethesda Terrace and its fountain.",
    [("ar_centralpark_0.jpg", "The park from the top of Rockefeller Center"), ("ar_centralpark2_1.jpg", "Bethesda Terrace and Fountain")], [NA, "industrial", "garden"])
add("Dulles Airport Main Terminal", "Washington Dulles International Airport", "Chantilly, Virginia, United States", "1958–1962", "Neo-futurism", "Neo-futurism", "Eero Saarinen",
    "An airport terminal whose concrete roof hangs in a catenary curve between two rows of outward-leaning piers.",
    "Completed after Saarinen's death; its mobile lounges carried passengers out to the planes.",
    [("ar_dulles_0.jpg", "The terminal's leaning piers and hanging roof")], [NA, "modern", "infrastructure", "modernist"])
add("Miller House", "", "Columbus, Indiana, United States", "1953–1957", "Modernism", "Modernism", "Eero Saarinen",
    "A flat-roofed, glass-walled house on a grid of cruciform columns, with a sunken conversation pit at its centre and skylights running along the roof.",
    "Built for the industrialist J. Irwin Miller, whose foundation brought modernist architecture to Columbus; interiors by Alexander Girard and gardens by Dan Kiley.",
    [("ar_miller2_1.jpg", "The house from the garden"), ("ar_miller_1.jpg", "Dan Kiley's honey-locust allée")], [NA, "modern", "residential", "modernist"])
add("Ennis House", "", "Los Angeles, California, United States", "1924", "Maya Revival", "Maya Revival", "Frank Lloyd Wright",
    "A temple-like house on a hillside, built of interlocking concrete blocks cast with a patterned relief, the largest of Wright's four textile-block houses.",
    "Its Maya look has made it a film set, most famously in <i>Blade Runner</i>.",
    [("ar_ennis_0.jpg", "The house on its hillside"), ("ar_ennis_3.jpg", "The gate and the patterned textile blocks")], [NA, "modern", "residential", "maya-revival"])
add("Stata Center", "Ray and Maria Stata Center", "Cambridge, Massachusetts, United States", "2000–2004", "Deconstructivism", "Deconstructivism", "Frank Gehry",
    "A cluster of tilting, colliding volumes in brick, brushed metal, and bright paint, built for MIT's computer-science laboratories.",
    "Built on the site of Building 20, the wartime radar laboratory; MIT sued Gehry's firm in 2007 over leaks and cracks.",
    [("ar_stata_3.jpg", "The tilting metal volumes")], [NA, "contemporary", "cultural", "deconstructivist"])
add("Transportation Building", "", "Chicago, Illinois, United States [demolished]", "1893", "Chicago School", "Chicago School", "Louis Sullivan; Dankmar Adler",
    "The only coloured building in the White City of the 1893 World's Columbian Exposition, entered through the Golden Door, a gilded arch of concentric ornamented bands.",
    "Demolished after the fair; the Golden Door won Sullivan medals from the Union centrale des arts décoratifs in Paris.",
    [("ar_transport_1.jpg", "The Golden Door, in the official views of the fair")], [NA, "industrial", "civic", "chicago-school"])
add("Kansai International Airport Terminal", "", "Osaka, Japan", "1988–1994", "High-tech", "High-tech", "Renzo Piano",
    "A terminal 1.7 kilometres long under a single curved roof whose profile follows the flow of air from its ducts, on an artificial island in Osaka Bay.",
    "The island has been sinking since construction; the terminal came through the 1995 Kobe earthquake without a broken pane.",
    [("ar_kansai_1.jpg", "The terminal's canyon of escalators and bridges")], [AS, "contemporary", "infrastructure", "high-tech"], nametells=True)
add("British Museum", "", "London, England", "1823–1852; Great Court 2000", "Greek Revival", "Neoclassical", "Robert Smirke; Norman Foster (Great Court)",
    "A Greek Revival museum fronted by a colonnade of forty-four Ionic columns; its courtyard, around the round Reading Room, was roofed in 2000 with a glass-and-steel lattice as the Great Court.",
    "The Reading Room (1857) was designed by Robert Smirke's brother Sydney; Karl Marx wrote much of <i>Das Kapital</i> there.",
    [("ar_britmus2_0.jpg", "The south front, in a 19th-century print"), ("ar_britmus_0.jpg", "The Great Court under Norman Foster's roof")], [EU, "industrial", "cultural", "neoclassical"])
add("North Christian Church", "", "Columbus, Indiana, United States", "1959–1964", "Modernism", "Modernism", "Eero Saarinen",
    "A hexagonal church whose low slate roof rises into a needle spire 192 feet high, with the sanctuary gathered around a central communion table.",
    "Saarinen's last building, completed after his death.",
    [("ar_northchristian2_1.jpg", "The hexagonal roof and its spire")], [NA, "modern", "religious", "modernist"])
add("Crystal Cathedral", "Christ Cathedral", "Garden Grove, California, United States", "1977–1980", "Late Modernism", "Modernism", "Philip Johnson; John Burgee",
    "A star-shaped megachurch walled in more than 10,000 panes of mirrored glass on a white steel space frame, built for the televangelist Robert H. Schuller.",
    "Its 90-foot doors open so that drive-in worshippers can follow the service; the Catholic Church bought it in 2012 and reconsecrated it as Christ Cathedral.",
    [("ar_crystalcath_0.jpg", "The mirrored-glass church and its bell tower"), ("ar_crystalcath_1.jpg", "The stainless-steel bell tower")], [NA, "contemporary", "religious", "modernist"])
add("Palace of Westminster", "Houses of Parliament", "London, England", "1840–1870", "Gothic Revival", "Gothic Revival", "Charles Barry; Augustus Pugin",
    "The seat of Parliament on the Thames, rebuilt after the fire of 1834: Barry planned it, Pugin designed its Perpendicular Gothic detail, and it ends in the Victoria Tower and the Elizabeth Tower (Big Ben).",
    "Westminster Hall, of 1097, survived the fire and was incorporated.",
    [("ar_westminster_1.jpg", "The river front")], [EU, "industrial", "civic", "gothic-revival"], nametells=True)
add("Green Building", "MIT Building 54", "Cambridge, Massachusetts, United States", "1962–1964", "Modernism", "Modernism", "I. M. Pei",
    "A 21-storey concrete tower for MIT's earth sciences, raised on two-storey legs, with a weather radome on its roof.",
    "Students have turned its grid of windows into a giant screen, playing <i>Tetris</i> on it in 2012.",
    [("ar_greenbldg_1.jpg", "The tower on its legs")], [NA, "modern", "cultural", "modernist"])
add("Dallas City Hall", "", "Dallas, Texas, United States", "1972–1978", "Brutalism", "Brutalism", "I. M. Pei",
    "An inverted pyramid of concrete, each floor projecting beyond the one below at 34 degrees, over a plaza with a pool.",
    "The overhang shades the offices from the Texas sun; the building played the headquarters of Omni Consumer Products in <i>RoboCop</i>.",
    [("ar_dallas_3.jpg", "The leaning west elevation")], [NA, "contemporary", "civic", "brutalist"], nametells=True)
add("Jacobs House", "Herbert and Katherine Jacobs First House", "Madison, Wisconsin, United States", "1936–1937", "Usonian", "Organic architecture", "Frank Lloyd Wright",
    "The first Usonian house: an L-shaped, single-storey house of brick and board-and-batten wood on a heated concrete slab, built for about $5,500 as a house the middle class could afford.",
    "Its radiant floor heating and carport became Usonian standards.",
    [("ar_jacobs2_3.jpg", "The garden side, its glass doors opening onto the lawn"), ("ar_jacobs_3.jpg", "The living room")], [NA, "modern", "residential", "organic-architecture"])
add("MIT Chapel", "", "Cambridge, Massachusetts, United States", "1955", "Modernism", "Modernism", "Eero Saarinen",
    "A windowless brick cylinder in a moat, lit by light reflected up through low arches and by an oculus over the altar, where Harry Bertoia's screen of metal leaves shimmers.",
    "", [("ar_mitchapel_3.jpg", "The altar under Harry Bertoia's screen"), ("ar_mitchapel_2.jpg", "The undulating brick wall")], [NA, "modern", "religious", "modernist"], nametells=True)
add("8 Spruce Street", "New York by Gehry; Beekman Tower", "New York City, United States", "2006–2011", "Deconstructivism", "Deconstructivism", "Frank Gehry",
    "A 76-storey apartment tower in Lower Manhattan whose stainless-steel skin ripples like draped cloth.",
    "", [("ar_spruce_1.jpg", "The rippling tower above the Potter Building")], [NA, "contemporary", "skyscraper", "deconstructivist"])
add("Carpenter Center for the Visual Arts", "", "Cambridge, Massachusetts, United States", "1961–1963", "Brutalism", "Brutalism", "Le Corbusier",
    "Le Corbusier's only building in North America, a concrete block for Harvard pierced by an S-shaped ramp that carries a path through the building.",
    "", [("ar_carpenter_1.jpg", "The concrete studios and their brise-soleil")], [NA, "modern", "cultural", "brutalist"])
add("Museum of Pop Culture", "Experience Music Project", "Seattle, Washington, United States", "1995–2000", "Deconstructivism", "Deconstructivism", "Frank Gehry",
    "Colliding masses of coloured stainless steel and aluminum, said to evoke smashed electric guitars, with the Seattle Center monorail running through them.",
    "Built for Microsoft's co-founder Paul Allen as a tribute to Jimi Hendrix; its main hall is the Sky Church.",
    [("ar_emp_0.jpg", "The coloured metal skins")], [NA, "contemporary", "cultural", "deconstructivist"])
add("General Motors Technical Center", "", "Warren, Michigan, United States", "1949–1956", "International Style", "International Style", "Eero Saarinen; Eliel Saarinen",
    "A research campus of long steel-and-glass buildings around a lake, with glazed-brick end walls in bright colours and a stainless-steel water tower.",
    "Called the \"Industrial Versailles\"; begun by Eliel Saarinen and completed by his son.",
    [("ar_gmtech_3.jpg", "A glazed-brick end wall and the blue stair towers")], [NA, "modern", "commercial", "international-style"])
add("Cardboard Cathedral", "Transitional Cathedral", "Christchurch, New Zealand", "2013", "Contemporary", "Contemporary", "Shigeru Ban",
    "A temporary A-frame cathedral of cardboard tubes coated in polyurethane, with a triangle of coloured glass at its front, built after the 2011 earthquake wrecked Christchurch Cathedral.",
    "", [("ar_cardboard_2.jpg", "The A-frame and its coloured-glass front")], [OC, "contemporary", "religious", "contemporary"])
add("Banqueting House", "", "London, England", "1619–1622", "Palladian", "Renaissance", "Inigo Jones",
    "The first building in England in the Renaissance classical manner, a double-cube hall that is the only surviving part of Whitehall Palace; Rubens painted its ceiling for Charles I.",
    "Charles I was executed on a scaffold outside it in 1649.",
    [("ar_banqueting_1.jpg", "The Whitehall front"), ("ar_banqueting2_2.jpg", "The hall under Rubens's ceiling")], [EU, "early-modern", "palace", "renaissance"])
add("Pennsylvania Station", "Penn Station", "New York City, United States [demolished]", "1905–1910", "Beaux-Arts", "Beaux-Arts", "McKim, Mead & White",
    "A Beaux-Arts railway terminal whose waiting room was modelled on the Baths of Caracalla; its demolition in 1963 launched the historic-preservation movement in New York.",
    "Vincent Scully: “One entered the city like a god; one scurries in now like a rat.”",
    [("ar_pennstation2_0.jpg", "The station from the air, before 1963")], [NA, "industrial", "infrastructure", "beaux-arts"])
add("AEG Turbine Factory", "AEG-Turbinenfabrik", "Berlin, Germany", "1908–1909", "Industrial architecture", "Modernism", "Peter Behrens",
    "A factory hall of steel and glass under a massive gable, a temple of industry designed by the company's artistic adviser.",
    "Walter Gropius, Mies van der Rohe, and Le Corbusier all worked in Behrens's office at the time.",
    [("ar_aeg_3.jpg", "The hall's gable end")], [EU, "industrial", "commercial", "modernist"])
add("Nakagin Capsule Tower", "", "Tokyo, Japan [demolished 2022]", "1970–1972", "Metabolism", "Contemporary", "Kisho Kurokawa",
    "Two concrete cores carrying 140 prefabricated capsules, each a tiny apartment with a round window, meant to be replaced as they wore out: the icon of Japanese Metabolism.",
    "None was ever replaced; the tower was demolished in 2022 and some capsules preserved.",
    [("ar_nakagin_0.jpg", "The stacked capsules")], [AS, "contemporary", "residential", "contemporary"])
add("New York Public Library", "Stephen A. Schwarzman Building", "New York City, United States", "1902–1911", "Beaux-Arts", "Beaux-Arts", "Carrère and Hastings",
    "A Beaux-Arts marble library on Fifth Avenue, guarded by the stone lions Patience and Fortitude, whose Rose Main Reading Room runs almost two blocks.",
    "", [("ar_nypl_2.jpg", "The Fifth Avenue front"), ("ar_nypl_0.jpg", "The Rose Main Reading Room")], [NA, "industrial", "cultural", "beaux-arts"], nametells=True)
add("Transamerica Pyramid", "", "San Francisco, California, United States", "1969–1972", "Modernism", "Modernism", "William Pereira",
    "A 48-storey tapering white pyramid with two wings for the elevators and stairs, the emblem of San Francisco's skyline.",
    "", [("ar_transamerica_2.jpg", "The pyramid above the Financial District")], [NA, "contemporary", "skyscraper", "modernist"])
add("Hill House", "", "Helensburgh, Scotland", "1902–1904", "Art Nouveau", "Art Nouveau", "Charles Rennie Mackintosh",
    "Mackintosh's harled grey house for the publisher Walter Blackie, for which he designed everything from the furniture to the light fittings.",
    "Its porous render let in so much water that since 2019 it has stood inside a protective steel-mesh box.",
    [("ar_hillhouse_1.jpg", "The house in an early photograph")], [EU, "industrial", "residential", "art-nouveau"])
add("St. Vitus Cathedral", "", "Prague, Czech Republic", "1344–1929", "Gothic", "Gothic", "Matthias of Arras; Peter Parler",
    "The Gothic cathedral inside Prague Castle, begun for Charles IV in 1344 and finished only in 1929, with Peter Parler's net vaults over the choir.",
    "", [("ar_stvitus_2.jpg", "The nave, looking east")], [EU, "medieval", "religious", "gothic"])
add("Biltmore Estate", "", "Asheville, North Carolina, United States", "1889–1895", "Châteauesque", "Beaux-Arts", "Richard Morris Hunt",
    "The largest private house in the United States, a French Renaissance château built for George Washington Vanderbilt II, with grounds by Frederick Law Olmsted.",
    "", [("ar_biltmore_2.jpg", "The house above its lawn")], [NA, "industrial", "residential", "revivalist"])


def slug(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", C.fold(s)).strip("-")


def save(src, name):
    im = Image.open(SRC + src).convert("RGB")
    if max(im.size) > 1280:
        im.thumbnail((1280, 1280))
    im.save(os.path.join(MED, name), quality=88)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    apply = "--apply" in sys.argv
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=WAKE)}
    for nid in WAKE:
        n = ns[nid]
        print("WAKE %-45s %s" % (C.plain(n["fields"]["Name"]["value"])[:45], [t.split("::")[-1] for t in n["tags"] if "::tier::" in t]))
    existing = {C.fold(C.plain(x["fields"]["Name"]["value"])) for x in C.anki("notesInfo", notes=C.anki("findNotes", query="note:Architecture"))}
    for b in B:
        assert "--resume" in sys.argv or C.fold(b["Name"]) not in existing, b["Name"]
        for src, cap in b["pics"]:
            assert os.path.exists(SRC + src), src
    print("ADD", len(B), [b["Name"] for b in B])
    if not apply:
        sys.exit()
    resume = "--resume" in sys.argv   # the first --apply died after the WAKE step; add only what is missing
    backup = {"wake": [{"nid": n["noteId"], "fields": {k: v["value"] for k, v in n["fields"].items()}, "tags": n["tags"]} for n in ns.values()]}
    # fixes on woken notes
    for nid, fx in ({} if resume else FIX).items():
        F = {k: v["value"] for k, v in ns[nid]["fields"].items()}
        f = {}
        if "pics" in fx:
            for i in range(1, 5):
                f["Picture %d" % i], f["Caption %d" % i] = "", ""
            for i, (src, name, cap) in enumerate(fx["pics"], 1):
                save(src, name); f["Picture %d" % i], f["Caption %d" % i] = '<img src="%s">' % name, cap
        for s, v in fx.get("slots", {}).items():
            if v is None:
                f["Picture %d" % s], f["Caption %d" % s] = "", ""
            elif v == "MOVE3":
                f["Picture %d" % s], f["Caption %d" % s] = F["Picture 3"], F["Caption 3"]
                f["Picture 3"], f["Caption 3"] = "", ""
            else:
                save(v[0], v[1]); f["Picture %d" % s], f["Caption %d" % s] = '<img src="%s">' % v[1], v[2]
        for s, c in fx.get("captions", {}).items():
            f["Caption %d" % s] = c
        if "Description" in fx:
            f["Description"] = fx["Description"]
        # close gaps left by a cleared slot
        pics = [(f.get("Picture %d" % i, F["Picture %d" % i]), f.get("Caption %d" % i, F["Caption %d" % i])) for i in range(1, 5)]
        pics = [p for p in pics if p[0]] + [("", "")] * 4
        for i in range(1, 5):
            f["Picture %d" % i], f["Caption %d" % i] = pics[i - 1]
        C.anki("updateNoteFields", note={"id": nid, "fields": f})
    for nid in ([] if resume else WAKE):
        n = ns[nid]
        old = [t for t in n["tags"] if "::tier::" in t and t != T1]
        if old:
            C.anki("removeTags", notes=[nid], tags=" ".join(old))
        C.anki("addTags", notes=[nid], tags=T1 + " Architecture::retier_2026-09-28")
        C.anki("unsuspend", cards=n["cards"])
    # new notes
    added = []
    for b in B:
        if resume and C.fold(b["Name"]) in existing:
            continue
        f = {k: b[k] for k in ("Name", "Alternate", "Location", "Date", "Style", "Main style", "Architect", "Description", "Notes", "NameTells", "Foreign")}
        f["StyleCard"] = "1"
        for i, (src, cap) in enumerate(b["pics"], 1):
            name = "arch-%s-%d.jpg" % (slug(b["Name"]), i)
            save(src, name)
            f["Picture %d" % i], f["Caption %d" % i] = '<img src="%s">' % name, cap
        region, period, typ = b["tags"][:3]
        tags = [T1, "Architecture::region::" + region, "Architecture::period::" + period, "Architecture::type::" + typ,
                "Architecture::added_2026-09-28"] + (["Architecture::style::" + b["tags"][3]] if len(b["tags"]) > 3 else [])
        nid = C.anki("addNote", note={"deckName": "Architecture", "modelName": "Architecture", "fields": f, "tags": tags,
                                      "options": {"allowDuplicate": False}})
        added.append(nid)
    backup["added"] = added
    json.dump(backup, open("backups/arch_asked_0928_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
    print("woke", len(WAKE), "| added", len(added))
