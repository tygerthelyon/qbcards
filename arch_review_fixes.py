# -*- coding: utf-8 -*-
"""arch_review_fixes.py -- Carter's phone review, 2026-09-27 (Architecture and Art).

- Alternate names in one format: each alternate is a name, foreign names italic; an English meaning follows in
  brackets, with no quotes, no "lit." and no leading "The". Entries that are not other names for the building
  (Faisal Mosque -> "Islamabad", Petra -> "Al-Khazneh", street addresses) are removed.
- Location: the middle region is dropped when it only repeats the city ("London, Greater London, England").
- Descriptions no longer name or describe the architect (Casa Batlló: "designed by Catalan architect").
- Captions: a stray Wikipedia "[fr]" link and sentence-length captions on Reinforced concrete.
- Functionalism: the first two pictures were two low-resolution crops of one photo; now the Van Nelle Factory
  and the Bauhaus at Dessau.
- A list inside a centred block is aligned left (Gothic's old bullet notes sat ragged under a centred text).
- Art: s and t with comma below (Brâncuși) are missing from Optima, the Art title face on iOS, so the phone drew
  them in another font; written with the cedilla forms, which Optima has.

    py -3.9 arch_review_fixes.py [--apply]
"""
import base64
import json
import os
import re
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
I = lambda s: "<i>%s</i>" % s

ALT = {
    "Alcázar of Seville": I("Real Alcázar de Sevilla") + " (Royal Alcázar of Seville)",
    "Altes Museum": "Old Museum",
    "Angkor Wat": I("Nokor Wat") + " (Temple City)",
    "Baroque": "",
    "Basilica of Saint Denis": "",
    "Bublik Apartments": I("Dom-bublik") + " (Bagel House)",
    "Burj Khalifa": "Khalifa Tower",
    "Casa Luis Barragán": "Luis Barragán House",
    "Casa Milà": I("La Pedrera") + " (the Stone Quarry)",
    "Casa del Fascio": "House of the Fascio, " + I("Casa del Popolo") + " (House of the People)",
    "Chartres Cathedral": I("Notre-Dame de Chartres") + " (Our Lady of Chartres)",
    "Chrysler Building": "",
    "Citadel of Aleppo": I("Qalʿat Ḥalab"),
    "Empire State Building": "",
    "Faisal Mosque": "",
    "Flatiron Building": "Fuller Building",
    "Göbekli Tepe": "Potbelly Hill",
    "Hearst Castle": I("La Cuesta Encantada") + " (the Enchanted Hill)",
    "Hôtel Tassel": "Tassel House",
    "Il Gesù": I("Chiesa del Santissimo Nome di Gesù") + " (Church of the Most Holy Name of Jesus)",
    "Itaipu Dam": I("Central Hidroeléctrica Itaipu") + " (Itaipu Power Plant)",
    "Kaaba": I("al-Kaʿbah") + " (the Cube)",
    "Karlskirche": "Church of Saint Charles",
    "Lakshmana Temple": "Laxmana Temple, Chaturbhuja Temple of Khajuraho, Ramachandra Temple of Khajuraho",
    "Leça Swimming Pools": I("Piscina das Marés") + " (Tidal Pools)",
    "Liverpool Cathedral": "Cathedral Church of Christ in Liverpool, Liverpool Anglican Cathedral",
    "Lloyd's building": "Inside-Out Building, One Lime Street",
    "Metéora monasteries": I("Metéora") + " (suspended in the air)",
    "Mosteiro da Batalha": "Batalha Monastery, " + I("Mosteiro de Santa Maria da Vitória") + " (Monastery of Saint Mary of the Victory)",
    "Palazzo Medici Riccardi": "Medici Riccardi Palace",
    "Palazzo Pubblico": "Public Palace",
    "Palazzo Rucellai": "Rucellai Palace",
    "Palácio da Alvorada": "Palace of the Dawn",
    "Panama Canal locks": "",
    "Pantheon": I("Santa Maria ad Martyres") + " (Saint Mary and the Martyrs)",
    "Park Güell": "Güell Park",
    "Parkroyal Collection Pickering": "Parkroyal on Pickering",
    "Petra": "",
    "Piazza d'Italia": "Square of Italy",
    "Rockefeller Center": "Radio City",
    "Saint John the Divine Cathedral": "Saint John the Unfinished",
    "Saint Mary's Church": I("St. Marien zu Lübeck"),
    "Saint Peter's Basilica": I("San Pietro in Vaticano") + " (Papal Basilica of Saint Peter in the Vatican)",
    "Sanjusangen-do": "Hall of Thirty-Three Bays",
    "Santuário Dom Bosco": "Dom Bosco Sanctuary",
    "Schönbrunn Palace": I("Schloss Schönbrunn") + " (Beautiful Spring Palace)",
    "Seville Cathedral": I("Catedral de Santa María de la Sede") + " (Cathedral of Saint Mary of the See)",
    "Shah-i-Zinda": I("Shohizinda") + " (the Living King)",
    "St.-Marien-Kirche": "Saint Mary's Church of Stralsund",
    "Stephansdom": I("Steffl") + ", Saint Stephen's Cathedral",
    "Teotihuacan": "",
    "Torres de Satélite": "Satellite Towers",
    "Whitney Museum of American Art (Breuer Building)": "Breuer Building",
    "30 St Mary Axe": "Gherkin",
    "Al-Masjid an-Nabawi": "Prophet's Mosque",
    "Sydney Harbour Bridge": "Coathanger",
    "World Trade Center": "Twin Towers",
    "Basilica di San Marco": "Saint Mark's Basilica, " + I("Chiesa d'Oro") + " (Church of Gold)",
}

DESC = {
    "Casa Batlló": "Residence remodelled in 1904–1906 with an organic, skeletal façade of bone-like columns and almost no "
                   "straight lines, clad in a colourful mosaic of broken ceramic tiles.",
    "Il Gesù": "The mother church of the Jesuits in Rome. Its wide single nave and two-storey façade became the model for "
               "Counter-Reformation churches.",
    "United Nations Secretariat Building": "A green glass slab with blank marble end walls, designed by an international "
                                           "board of architects.",
}

FIELDS = {
    ("Reinforced concrete", "Caption 2"): "The Philips Pavilion, Brussels, Expo 58",
    ("Reinforced concrete", "Caption 3"): "François Coignet's house, Saint-Denis (1853)",
    ("Reinforced concrete", "Caption 4"): "Houses Coignet built for his factory workers, Saint-Denis",
    ("Functionalism", "Caption 1"): "The Van Nelle Factory, Rotterdam (1925–1931)",
    ("Functionalism", "Caption 2"): "The Bauhaus building, Dessau (1925–1926)",
    ("Functionalism", "Caption 3"): "The tower of the Helsinki Olympic Stadium (1934–1938)",
    ("Functionalism", "Caption 4"): "Houses in Södra Ängby, Stockholm (1938)",
}
PICS = {("Functionalism", "Picture 1"): ("vn0.jpg", "arch-functionalism-van-nelle.jpg"),
        ("Functionalism", "Picture 2"): ("arch-bauhaus-dessau-4.jpg", None)}
SCRATCH = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\1d6bde35-08b4-4391-958b-52d033191c05\scratchpad\vn"

CSS_ADD = """
/* a list inside a centred block reads left-aligned, the block itself still centred (Carter: Gothic's bullets) */
.arch-concept-note ul, .arch-concept-note ol, .arch-concept-def ul, .arch-concept-def ol,
.arch2-desc ul, .arch2-desc ol { display: inline-block; text-align: left; margin: 4px auto; padding-left: 1.2em; }
"""
CSS_MARK = "Carter: Gothic's bullets"

REDUNDANT_REGION = re.compile(r"^(?:greater\s+)?(?P<c>.+?)(?:\s+(?:prefecture|province|governorate|region|district|division|city))?$", re.I)


def location_fix(loc):
    parts = [p.strip() for p in loc.split(",")]
    if len(parts) != 3:
        return loc
    city, reg, country = parts
    if reg == "Greater London":
        return "%s, %s" % (city, country) if city == "London" else "%s, London, %s" % (city, country)
    m = REDUNDANT_REGION.match(reg)
    core = m.group("c").lower() if m else reg.lower()
    c = city.lower()
    if core == c or c.startswith(core + " ") or reg in ("Capital Region",):
        return "%s, %s" % (city, country)
    return loc


def main(apply):
    ids = C.anki("findNotes", query="note:Architecture")
    notes = []
    for i in range(0, len(ids), 400):
        notes += C.anki("notesInfo", notes=ids[i:i + 400])
    by = {C.plain(n["fields"]["Name"]["value"]).strip(): n for n in notes}
    new = {}

    def put(n, f, v):
        if n["fields"][f]["value"] != v:
            new.setdefault(n["noteId"], {})[f] = v

    for nm, v in ALT.items():
        put(by[nm], "Alternate", v)
    for nm, v in DESC.items():
        put(by[nm], "Description", v)
    for (nm, f), v in FIELDS.items():
        put(by[nm], f, v)
    n_loc = 0
    for n in notes:
        loc = n["fields"]["Location"]["value"]
        fx = location_fix(loc)
        if fx != loc:
            put(n, "Location", fx)
            n_loc += 1
    media_ops = []
    for (nm, f), (src, dest) in PICS.items():
        if dest:
            media_ops.append((os.path.join(SCRATCH, src), dest))
            put(by[nm], f, '<img src="%s">' % dest)
        else:
            put(by[nm], f, '<img src="%s">' % src)

    name = {n["noteId"]: C.plain(n["fields"]["Name"]["value"]) for n in notes}
    old = {n["noteId"]: n for n in notes}
    for nid, fs in new.items():
        for f, v in fs.items():
            print("%s [%s]: %s  ->  %s" % (name[nid], f, C.plain(old[nid]["fields"][f]["value"])[:80], C.plain(v)[:100]))
    print(len(new), "Architecture notes;", n_loc, "locations")

    # Art: comma-below letters -> cedilla forms
    art_ids = C.anki("findNotes", query="note:Art (ș or ț or Ș or Ț)")
    art = C.anki("notesInfo", notes=art_ids) if art_ids else []
    tr = str.maketrans({"ș": "ş", "ț": "ţ", "Ș": "Ş", "Ț": "Ţ"})
    art_new = {}
    for n in art:
        for f, v in n["fields"].items():
            if v["value"] != v["value"].translate(tr):
                art_new.setdefault(n["noteId"], {})[f] = v["value"].translate(tr)
    print(len(art_new), "Art notes with comma-below letters")
    # Art Gothic's caption for the Toruń Magdalene
    g = C.anki("notesInfo", notes=C.anki("findNotes", query='note:Art "Title:Gothic"'))
    for n in g:
        cap = n["fields"]["Captions"]["value"]
        fx = cap.replace("14th Century International Gothic Mary Magdalene in St. Johns' Cathedral in Toruń, Poland",
                         "Mary Magdalene, International Gothic, 14th century, St. John's Cathedral, Toruń")
        if fx != cap:
            art_new.setdefault(n["noteId"], {})["Captions"] = fx
            print("Art Gothic caption fixed")

    css = C.anki("modelStyling", modelName="Architecture")["css"]
    if not apply:
        print("css rule present:", CSS_MARK in css)
        return
    stamp = time.strftime("%Y%m%d_%H%M")
    json.dump({"arch": {nid: {f: old[nid]["fields"][f]["value"] for f in fs} for nid, fs in new.items()},
               "art": {nid: {f: next(x for x in art if x["noteId"] == nid)["fields"][f]["value"] if any(x["noteId"] == nid for x in art) else None
                             for f in fs} for nid, fs in art_new.items()},
               "css": css}, open(os.path.join(HERE, "backups", "arch_review_before_%s.json" % stamp), "w", encoding="utf-8"),
              ensure_ascii=False)
    for src, dest in media_ops:
        from PIL import Image
        import io
        im = Image.open(src).convert("RGB")
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=88)
        C.anki("storeMediaFile", filename=dest, data=base64.b64encode(buf.getvalue()).decode())
    for nid, fs in new.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": fs})
    for nid, fs in art_new.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": fs})
    if CSS_MARK not in css:
        C.anki("updateModelStyling", model={"name": "Architecture", "css": css + CSS_ADD})
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
