# -*- coding: utf-8 -*-
"""fix_0928_art.py -- Art cards Carter flagged on 2026-09-28, and what reading them turned up.

  "can you try to improve some of the art cards that say "mixed media", eg. all the performance
   art cards say it and idk if thats really appropriate"
      119 notes gave their medium as "Mixed media". Each now names what the work is made of, as
      a museum label would, or, for a performance, says what happened ("Performance: the audience
      cut away her clothing with scissors"). Eight whose materials I could not state with
      confidence are left as they are (the eight in UNSURE). Three style labels in the same set were
      wrong: Manzoni is not Arte Povera (named in 1967, four years after his death), and Nam June
      Paik is video art and Fluxus, not Neo-Dada; "New Realism" is made "Nouveau Réalisme", the
      form the deck already uses once and quizbowl uses.
  "linear perspective images are bad"
      three textbook diagrams, replaced by the Urbino Ideal City, Uccello's chalice study, and
      Dürer's Man Drawing a Lute, with captions; Alberti gets his full name.
  "girl with a balloon should be italicized in the description of the love is in the bin card"
      done; the canvas was renamed by Banksy, not Sotheby's; its medium was "Aerosol and acrylic on
      cardboard" (it is spray paint and acrylic on canvas, mounted on board); the picture's alt
      text was a Sotheby's headline.
  Found while reading: Angel Bust (Banksy) carried the Winged Victory of Samothrace's notes, and
  Liber Veritatis was called "[195 paintings]" (it is 195 drawings recording Claude's paintings).

  After applying: the fourteen performance media were reworded by hand without the "Performance:"
  prefix, which repeated the style ("Performance Art; Performance: ..."); see
  backups/fix_0928_art_perf_*.json.

    py -3.9 fix_0928_art.py [--apply]
"""
import json, os, re, shutil, sys, time
import concept_add as C

SRC = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/4c6fe2ff-c3a6-47fb-8b54-226f916ad6af/scratchpad/img/"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
FILES = {"lp_1.jpg": "artcon-linear-perspective-ideal-city.jpg",
         "lp_2.jpg": "artcon-linear-perspective-uccello-chalice.jpg",
         "lp_3.jpg": "artcon-linear-perspective-durer-lute.jpg"}

# nid -> the medium (the part of Style after ";")
MEDIUM = {
    1787890517173: "Oil, varnish, lead foil, lead wire, and dust on glass panels",
    1787890517174: "Assemblage: an old wooden door, bricks, velvet, leather over a metal armature, twigs, glass, electric lights, and a motor",
    1787890517176: "Painted wood window frame with eight panes of black leather",
    1787890517196: "Motor-driven mobile: painted iron pipe, steel wire, motor, and wood with string",
    1787890517197: "Wire, wood, metal, cloth, yarn, paper, leather, string, cork, and bottle caps",
    1787890517198: "Iron, wood, cord, and found objects",
    1787890517348: "Temporary theme park in a derelict lido, with works by 58 artists",
    1787890517367: "Tiger shark, glass, steel, silicone, and formaldehyde solution",
    1787890517368: "Platinum, diamonds, and human teeth",
    1787890517399: "Cow, calf, glass, steel, silicone, and formaldehyde solution, in four tanks",
    1787890517403: "Appliquéd tent, mattress, and light",
    1787890517404: "Mattress, linens, pillows, and objects",
    1787890517439: "Wood from a dismantled red barn, on a steel frame",
    1787890517718: "Pigment and synthetic resin, sponges, and pebbles on board",
    1787890517719: "Pigment and synthetic resin, sponges, and pebbles on board",
    1787890517884: "Pen and brown ink and wash on paper, bound as a book",
    1787890517897: "Combine: oil, paper, fabric, and found objects on canvas, with a stuffed Angora goat and a rubber tire on a platform",
    1787890517898: "Combine: oil, paper, fabric, photographs, metal, and wood on canvas, with a stuffed bald eagle and a hanging pillow",
    1787890518062: "Steel, plaster, rubber, resin, and paper",
    1787890518261: "Oil, acrylic, emulsion, and straw on canvas",
    1787890518484: "Casein paint, gold leaf, and inlaid glass, mother-of-pearl, and semi-precious stones on plaster",
    1787890518575: "Steel, wire mesh, concrete, bronze, and ceramic tile",
    1787890518750: "Plaster, latex, wood, fabric, and red light",
    1787890518754: "Marble, mirrors, steel, and glass",
    1787890518812: "Scrap: bicycle wheels, motors, a piano, a bathtub, and other junk, built to destroy itself",
    1787890518813: "Iron, wood, rubber belts, and an electric motor (a drawing machine)",
    1787890518818: "Ten scrap-metal machines with electric motors, in a water basin",
    1787890520204: "Calf with 18-carat gold horns and hooves, glass, gold-plated steel, silicone, and formaldehyde solution",
    1787890520205: "Tiger shark, glass, stainless steel, and formaldehyde solution",
    1787890520206: "Zebra, glass, steel, silicone, and formaldehyde solution",
    1787890520210: "Installation: an examination couch under a monitor playing a Margaret Thatcher broadcast",
    1787890520271: "The stolen contents of another gallery's exhibition",
    1787890520274: "Wax figure of Pope John Paul II, with polyester resin, human hair, fabric, stone, carpet, and glass",
    1787890520275: "Taxidermied horse, leather harness, rope, and pulley",
    1787890520277: "Taxidermied squirrel, ceramic, Formica, wood, paint, and metal",
    1787890520278: "Banana and duct tape",
    1787890520279: "Performance: the dealer duct-taped to the gallery wall for a day",
    1787890520280: "Wax figure of the artist, with human hair and clothing, set into the museum floor",
    1787890520311: "Assemblage: stuffed parrot on a perch, silk stocking with garter and doll's shoe, bowler hat, cork ball, celluloid fish, and map",
    1787890520421: "Oil, acrylic, emulsion, clay, porcelain, lead, copper wire, and circuit board on canvas",
    1787890520630: "Casein paint, gold leaf, and inlaid glass, mother-of-pearl, and semi-precious stones on plaster",
    1787890520648: "Oil, aluminum paint, and enamel with sand, pebbles, string, and broken sticks on canvas",
    1787890520656: "Oil, aluminum paint, and gravel on canvas",
    1787890520662: "Copper metallic paint and urine on canvas",
    1787890520665: "Acrylic paint on a BMW M1 racing car",
    1787890520683: "Concrete clad in ceramic tile",
    1787890520687: "Painted concrete and steel, with a living palm tree",
    1787890520818: "Vacuum cleaners, Plexiglas, and fluorescent lights",
    1787890520819: "Deep fryer mounted on fluorescent lights",
    1787890520825: "Stainless steel, soil, irrigation system, and live flowering plants",
    1787890520826: "Glass, steel, distilled water, and three basketballs",
    1787890520842: "Sheet metal, rod, wire, pitch, and mercury",
    1787890520848: "Paint on a Braniff Douglas DC-8 jet",
    1787890520881: "Mirror-lined rooms with lights, some with water",
    1787890520883: "Furnished white room and thousands of coloured dot stickers",
    1787890520915: "Shoes, string, and paper frills on a metal platter",
    1787890520917: "Fur-covered cup, saucer, and spoon",
    1787890520945: "Combine: oil, pencil, paper, fabric, newspaper, and printed reproductions on canvas",
    1787890520946: "Combine: oil, paper, fabric, wood, and metal on canvas",
    1787890520948: "Combine: oil, paper, fabric, and found objects on two canvases joined by a wooden ladder",
    1787890520949: "Combine: oil, paper, fabric, wood, and metal on canvas",
    1787890520951: "Combine: a painted, collaged box with a stuffed rooster, on a post set in a pillow",
    1787890520952: "Screenprint on Plexiglas and mirror, with sound-activated lights",
    1787890520953: "Found metal (a car door, a window frame, an air duct, a bathtub), with radios and water",
    1787890520955: "Acrylic, screenprint, fabric, and found objects on 190 panels",
    1787890520980: "Plywood tracks and an inflatable vinyl lipstick (remade in steel and aluminum, 1974)",
    1787890521105: "Video installation: 336 television monitors, neon, steel, and wood",
    1787890521106: "Buddha statue, closed-circuit video camera, and television monitor",
    1787890521107: "Three television monitors in Plexiglas boxes, with cello strings",
    1787890521112: "A cannon firing red wax and Vaseline into a gallery corner",
    1787890521121: "Powdered pigment over sculpted forms",
    1787890521197: "Ceramic, porcelain, and textile",
    1787890521199: "Installation: a white bathroom with a bin of used sanitary products",
    1787890521222: "Performance: three days in a gallery with a live coyote, felt, a staff, and copies of <i>The Wall Street Journal</i>",
    1787890521223: "Performance: the artist, his head covered in honey and gold leaf, explains pictures to a dead hare",
    1787890521224: "Grand piano covered in grey felt, with a red cross",
    1787890521225: "Volkswagen bus and 24 sleds, each carrying felt, fat, and a flashlight",
    1787890521226: "Chalk on blackboard, with felt, fat, a dead hare, and painted poles",
    1787890521231: "Ship model with Dutch wax-print cotton sails, in a giant acrylic bottle",
    1787890521232: "Two headless mannequins in Dutch wax-print cotton, bench, and dog",
    1787890521233: "Headless mannequin in a Dutch wax-print cotton dress, swing, and artificial foliage",
    1787890521244: "Seven installations on Alcatraz, including LEGO portraits of political prisoners",
    1787890521246: "Steel wire-mesh fences and cages installed across New York City",
    1787890521270: "Aluminum, steel, nickel-plated brass, glass, wood, plastic, and electric motor",
    1787890521304: "Acrylic, oil, polyester resin, paper collage, glitter, map pins, and elephant dung on linen",
    1787890521305: "Acrylic, oil, polyester resin, paper collage, glitter, map pins, and elephant dung on canvas",
    1787890521306: "Thirteen paintings in oil, acrylic, glitter, and elephant dung on canvas, in a walnut-panelled room",
    1787890521373: "Pigment and synthetic resin on paper, printed by painted models' bodies",
    1787890521374: "The artist's silhouette in mud, sand, grass, flowers, fire, and blood, recorded in photographs and film",
    1787890521375: "Performance: she read a text from a paper scroll drawn from her body",
    1787890521376: "Performance, recorded in photographs, time cards, and film",
    1787890521377: "Performance: the artists, faces painted metallic, move stiffly to “Underneath the Arches”",
    1787890521378: "Performance: the audience cut away her clothing with scissors",
    1787890521379: "Performance: an assistant shot the artist in the arm with a .22 rifle",
    1787890521380: "Performance: the artist nailed to the back of a Volkswagen Beetle",
    1787890521381: "Performance: near-naked dancers with raw fish, chickens, sausages, paint, and paper",
    1787890521382: "Happening: three rooms of plastic sheeting, with scripted instructions for the audience",
    1787890521383: "Performance: the artist hidden under a gallery ramp, his voice relayed by loudspeaker",
    1787890521384: "Tin cans with printed paper labels",
    1787890521386: "Performance on the streets of New York, recorded in photographs",
    1787890521387: "Performance with animal carcasses, blood, and entrails",
    1787890521388: "Monofrequency lights, projection foil, haze machines, mirror foil, aluminum, and scaffolding",
    1787890521402: "A crack cut into the concrete floor of the Turbine Hall",
    1787890521414: "Assemblage: a wooden box with a mammy figurine holding a broom, a pistol, and a rifle",
    1787890521417: "Iron, copper, wood, and rope",
    1787890521421: "Oil, varnish, crayon, coloured papers, sandpaper, foil, and metallic paint on plywood",
    1787890521431: "Painted wood figures with clothing and found objects",
    1787890521446: "Layered paper, paint, and string on canvas",
    1787890521458: "Acrylic, charcoal, coloured pencil, collage, and transfers on paper",
    1787890521539: "Fibreglass, resin, silicone, and synthetic hair",
    1787890521572: "Plaster, cloth, metal, vinyl, and wood",
}
UNSURE = [1787890518263, 1787890518528, 1787890520198, 1787890520261, 1787890520420,
          1787890520954, 1787890521128, 1787890521242]   # Zim Zum, Jonah, Angel Bust, Christ of the
# Rubbish, Fertile Crescent, Cat Paws, Léger UN murals, Man in a Cube: left as "Mixed media"
STYLE = {  # nid -> new style (the part before ";")
    1787890521384: "Conceptual Art",
    1787890521105: "Video Art", 1787890521106: "Video Art", 1787890521107: "Fluxus, Video Art",
}


def one(q):
    ids = C.anki("findNotes", query=q)
    assert len(ids) == 1, (q, ids)
    return C.anki("notesInfo", notes=ids)[0]


def plan():
    ch = []   # (note, {field: new})
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(set(MEDIUM) | set(STYLE)))}
    for nid, n in ns.items():
        style, _, med = n["fields"]["Style"]["value"].partition(";")
        if nid in MEDIUM:
            assert "mixed media" in med.lower(), (nid, med)
            med = " " + MEDIUM[nid]
        ch.append((n, {"Style": STYLE.get(nid, style) + ";" + med}))
    # Manzoni's Achrome, and "New Realism" -> "Nouveau Réalisme"
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='note:Art "Style:*Arte Povera*" Artist:*Manzoni*')):
        if n["noteId"] not in ns:
            ch.append((n, {"Style": n["fields"]["Style"]["value"].replace("Arte Povera", "Conceptual Art")}))
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='note:Art "Style:*New Realism*"')):
        f = [x for x in ch if x[0]["noteId"] == n["noteId"]]
        cur = f[0][1]["Style"] if f else n["fields"]["Style"]["value"]
        new = cur.replace("New Realism", "Nouveau Réalisme")
        if f: f[0][1]["Style"] = new
        else: ch.append((n, {"Style": new}))

    n = one('note:Art "Title:Linear perspective"')
    assert "multi-Linear_perspective" in n["fields"]["Artwork"]["value"]
    ch.append((n, {
        "Artwork": "".join('<img src="%s">' % f for f in FILES.values()),
        "Captions": " | ".join([
            "<i>The Ideal City</i>, c. 1480–1490, Galleria Nazionale delle Marche, Urbino: a piazza laid out in one-point perspective",
            "Paolo Uccello, <i>Perspective Study of a Chalice</i>, c. 1450, Uffizi, Florence",
            "Albrecht Dürer, <i>Man Drawing a Lute</i>, 1525, from his treatise <i>Underweysung der Messung</i>: a thread stands in for the line of sight"]),
        "Notes": "Demonstrated by Filippo Brunelleschi and codified by Leon Battista Alberti in <i>De pictura</i> (1435); Masaccio's <i>Holy Trinity</i> is the first great painted use."}))

    n = one('note:Art "Title:*Love is in the Bin*"')
    ch.append((n, {
        "Notes": "<i>Girl with Balloon</i> shredded itself through a mechanism hidden in the frame the moment it sold at Sotheby's in 2018. Banksy renamed the half-shredded canvas; it resold in 2021 for about eighteen times the original price.",
        "Style": "Conceptual Art; Spray paint and acrylic on canvas, mounted on board",
        "Artwork": re.sub(r'<img [^>]*src="([^"]+)"[^>]*>', r'<img src="\1">', n["fields"]["Artwork"]["value"])}))

    n = C.anki("notesInfo", notes=[1787890520198])[0]
    assert "Samothrace" in n["fields"]["Notes"]["value"] and "Banksy" in n["fields"]["Artist"]["value"]
    ch.append((n, {"Notes": ""}))
    n = C.anki("notesInfo", notes=[1787890517884])[0]
    assert "[195 paintings]" in n["fields"]["Title"]["value"]
    ch.append((n, {"Title": n["fields"]["Title"]["value"].replace("[195 paintings]", "[195 drawings]")}))
    return ch


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    for n, f in ch:
        for k, v in f.items():
            old = n["fields"][k]["value"]
            if k != "Artwork":
                print("%s  %-8s %s\n%s  %-8s -> %s" % (n["noteId"], k, C.plain(old)[:150], " " * 13, "", C.plain(v)[:150]))
    print(len(ch), "notes;", len(MEDIUM), "media rewritten,", len(UNSURE), "left as mixed media")
    if "--apply" in sys.argv:
        for s, d in FILES.items():
            shutil.copy(SRC + s, os.path.join(MED, d))
        json.dump([{"nid": n["noteId"], **{k: n["fields"][k]["value"] for k in f}} for n, f in ch],
                  open("backups/fix_0928_art_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, f in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": f})
        print("applied")
