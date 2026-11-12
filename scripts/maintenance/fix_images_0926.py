# -*- coding: utf-8 -*-
"""fix_images_0926.py -- the wrong or weak pictures listed in AUDIT_2026-09-26, section 3.

Each replacement was viewed on a contact sheet first (scratchpad fx_sheet.jpg).

  Farnsworth House      picture 2 was the "Barnsworth Gallery" visitor centre
  San Giorgio Maggiore  picture 3 was St Mark's Basin seen from the campanile
  Sant'Ivo              picture 3 was an engraving of a window
  Casa Milà             caption "The Pedrera" sat on the painted entrance hall
  Frank Gehry           no Bilbao, no Disney Concert Hall (Chiat/Day replaced; Disney added)
  Art Nouveau           four Guimard pictures; now Guimard, Mucha, Tiffany, Horta
  Minimalism            two near-identical Judd concrete boxes; the second removed
  Zone System           a 13:1 strip that the picture layout crops to its middle three
                        zones; padded to the layout's widest ratio so all eleven show
  Rub' al-Khali         generic dunes, unanswerable; now the peninsula from orbit
  Bight of Biafra       the map printed its alternate name, "Bight of Bonny"; label removed
  Escarpment            picture 1 was a road seen through a window

    py -3.9 fix_images_0926.py [--apply]
"""
import json
import os
import sys
import time

from PIL import Image

import concept_add as C

S = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/1d6bde35-08b4-4391-958b-52d033191c05/scratchpad/"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")

# (source in scratchpad, media name)
FILES = {
    "fx_farnsworth_b.jpg": "arch-farnsworth-house-glass.jpg",
    "fx_sangiorgio_b.jpg": "arch-san-giorgio-maggiore-facade.jpg",
    "fx_santivo_a.jpg": "arch-sant-ivo-dome-interior.jpg",
    "fx_bilbao.jpg": "arch-gehry-guggenheim-bilbao.jpg",
    "fx_disney.jpg": "arch-gehry-disney-concert-hall.jpg",
    "fx_mucha.jpg": "artcon-art-nouveau-mucha-job.jpg",
    "fx_tiffany.jpg": "artcon-art-nouveau-tiffany-wisteria.jpg",
    "fx_horta.jpg": "artcon-art-nouveau-horta-tassel.jpg",
    "fx_rub_b.jpg": "geo-rub-al-khali-modis.jpg",
    "biafra_clean.jpg": "naqtimg-bight-of-biafra-unlabelled.jpg",
    "fx_escarp_a.jpg": "geoel-escarpment-bruce-peninsula.jpg",
}

EDITS = [
    ("Architecture", '"Name:Farnsworth House"', {
        "Picture 2": '<img src="arch-farnsworth-house-glass.jpg">',
        "Caption 2": "The glass walls, raised above the Fox River's floodplain"}),
    ("Architecture", '"Name:San Giorgio Maggiore*"', {
        "Picture 3": '<img src="arch-san-giorgio-maggiore-facade.jpg">',
        "Caption 3": "The Istrian stone façade"}),
    ("Architecture", '"Name:Sant\'Ivo*"', {
        "Picture 3": '<img src="arch-sant-ivo-dome-interior.jpg">',
        "Caption 3": "The dome from below, its plan a six-pointed star"}),
    ("Architecture", '"Name:Casa Mil*"', {
        "Caption 2": "The painted entrance hall"}),
    ("Architecture", '"Name:Frank Gehry"', {
        "Picture 3": '<img src="arch-gehry-guggenheim-bilbao.jpg">',
        "Caption 3": "Guggenheim Museum Bilbao (1997)",
        "Picture 4": '<img src="arch-gehry-disney-concert-hall.jpg">',
        "Caption 4": "Walt Disney Concert Hall, Los Angeles (2003)"}),
    ("Art", '"Title:Art Nouveau"', {
        "Artwork": '<img src="artcon2-art-nouveau.jpg"><img src="artcon-art-nouveau-mucha-job.jpg">'
                   '<img src="artcon-art-nouveau-tiffany-wisteria.jpg"><img src="artcon-art-nouveau-horta-tassel.jpg">',
        "Captions": "Hector Guimard, a Paris Métro entrance | Alphonse Mucha, poster for <i>Job</i> cigarette papers, 1896"
                    " | Tiffany Studios, <i>Wisteria</i> table lamp, c. 1901 | Victor Horta, the stair hall of the"
                    " Hôtel Tassel, Brussels, 1893"}),
    ("Art", '"Title:Minimalism"', {
        "Artwork": '<img src="qbam-minimalism.jpg"><img src="named3-Minimalism-3.jpg">',
        "Captions": "Donald Judd, <i>Untitled</i>, 1988–91, concrete | Dan Flavin, <i>untitled (to Don Judd, colorist)</i>"}),
    ("Photography", '"Title:Zone System"', {
        "Photograph": '<img src="photocon-zone-system-padded.png"><img src="pick-Zone_System-40.jpg">'}),
    ("Geography", '"Name:Rub* al-Khali"', {
        "Image": '<img src="geo-rub-al-khali-modis.jpg">',
        "Photo caption": "The Arabian Peninsula from orbit; the sand sea fills its southern third"}),
    ("Geography", '"Name:Bight of Biafra"', {
        "Image": '<img src="naqtimg-bight-of-biafra-unlabelled.jpg">'}),
    ("Geology", '"Name:Escarpment"', {
        "Picture 1": '<img src="geoel-escarpment-bruce-peninsula.jpg">',
        "Caption 1": "Cliffs of the Niagara Escarpment on Georgian Bay, Bruce Peninsula"}),
]


def pad_zone_strip():
    """Centre the 13:1 zone strip on a white canvas at the layout's widest ratio (2.4:1)."""
    im = Image.open(os.path.join(MED, "photocon-Zone_System.png")).convert("RGB")
    w, h = im.size
    H = int(round(w / 2.4))
    out = Image.new("RGB", (w, H), "white")
    out.paste(im, (0, (H - h) // 2))
    p = S + "photocon-zone-system-padded.png"
    out.save(p)
    return p


def main(apply):
    bk = []
    for m, q, f in EDITS:
        ids = C.anki("findNotes", query='note:"%s" %s' % (m, q))
        assert len(ids) == 1, (m, q, ids)
        n = C.anki("notesInfo", notes=ids)[0]
        missing = [k for k in f if k not in n["fields"]]
        assert not missing, (m, q, missing)
        bk.append({"nid": ids[0], "old": {k: n["fields"][k]["value"] for k in f}})
        print(m, q, "->", sorted(f))
    if not apply:
        return
    for src, dst in FILES.items():
        im = Image.open(S + src).convert("RGB")
        im.thumbnail((1600, 1600))
        p = S + "store_" + dst
        im.save(p, quality=88)
        C.anki("storeMediaFile", filename=dst, path=p)
    C.anki("storeMediaFile", filename="photocon-zone-system-padded.png", path=pad_zone_strip())
    json.dump(bk, open("backups/fix_images_0926_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"),
              ensure_ascii=False)
    for (m, q, f), b in zip(EDITS, bk):
        C.anki("updateNoteFields", note={"id": b["nid"], "fields": f})
    print("applied", len(bk))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
