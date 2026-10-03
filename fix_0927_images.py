# -*- coding: utf-8 -*-
"""fix_0927_images.py -- pictures Carter flagged on 2026-09-27, plus duplicate pictures.

Flagged (each replacement viewed on a contact sheet first):
  Installation art   The Dinner Party was 600px, dark and seen from far above; now Sappho's place
                     setting. La Menesunda read as a snapshot of a couple in bed; now Kadishman's
                     Shalechet at the Jewish Museum Berlin.
  Table of Silence   the photo showed park benches, not the table; now the table and its stools.
  Saint Peter's Sq.  picture 2 was an engraving of the square before Bernini's colonnade; now the
                     colonnade's four rows of columns. Both pictures captioned.
  Step Pyramid       one 500px picture with scaffolding; now three, captioned.

Duplicates: eight Art concept notes carried the same picture twice (artcon2-X and termg-X-1, from
two sourcing passes), and Rock-cut architecture carried Abu Simbel twice. The copy is removed with
its caption.

    py -3.9 fix_0927_images.py [--apply]
"""
import json, os, re, sys, time
from PIL import Image
import concept_add as C

SRC = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/4c6fe2ff-c3a6-47fb-8b54-226f916ad6af/scratchpad/img/"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
FILES = {
    "dp_04.jpg": "artcon-installation-dinner-party-sappho.jpg",
    "inst_en_20.jpg": "artcon-installation-kadishman-shalechet.jpg",
    "tos_01.jpg": "qba-table-of-silence-brancusi.jpg",
    "spq_03.jpg": "arch-st-peters-square-colonnade.jpg",
    "djo_05.jpg": "arch-djoser-pyramid.jpg",
    "djo_06.jpg": "arch-djoser-complex.jpg",
    "djo_15.jpg": "arch-djoser-masonry.jpg",
}
DUP_ART = [1790236437405, 1790236437930, 1790236438904, 1790236439217, 1790236439351,
           1790236439487, 1790236439538, 1790236439731]


def one(q):
    ids = C.anki("findNotes", query=q)
    assert len(ids) == 1, (q, ids)
    return C.anki("notesInfo", notes=ids)[0]


def plan():
    ch = []   # (nid, {field: new}, {field: old})
    n = one('"deck:Art" "Title:Installation art"')
    imgs = re.findall(r'<img[^>]*>', n["fields"]["Artwork"]["value"])
    caps = n["fields"]["Captions"]["value"].split(" | ")
    assert "dinner-party" in imgs[2] and len(caps) == len(imgs) == 4
    imgs[2] = '<img src="artcon-installation-dinner-party-sappho.jpg">'
    imgs[3] = '<img src="artcon-installation-kadishman-shalechet.jpg">'
    caps[2] = "Judy Chicago, <i>The Dinner Party</i>, 1974–1979: Sappho's place setting"
    caps[3] = "Menashe Kadishman, <i>Shalechet</i> (<i>Fallen Leaves</i>), Jewish Museum Berlin"
    ch.append((n, {"Artwork": "".join(imgs), "Captions": " | ".join(caps)}))
    n = one('"deck:Art" "Title:*Table of Silence*"')
    ch.append((n, {"Artwork": '<img src="qba-table-of-silence-brancusi.jpg">'}))
    n = one('"deck:Architecture" "Name:Saint Peter*Square*"')
    ch.append((n, {"Picture 2": '<img src="arch-st-peters-square-colonnade.jpg">',
                   "Caption 1": "The piazza from the dome: Bernini's two colonnades enclose an oval around the obelisk",
                   "Caption 2": "Inside the colonnade: four rows of Tuscan columns"}))
    n = one('"deck:Architecture" "Name:*Djoser*"')
    ch.append((n, {"Picture 1": '<img src="arch-djoser-pyramid.jpg">',
                   "Picture 2": '<img src="arch-djoser-complex.jpg">',
                   "Picture 3": '<img src="arch-djoser-masonry.jpg">',
                   "Caption 1": "The six-stepped pyramid, designed by Imhotep",
                   "Caption 2": "Restored buildings of Djoser's funerary complex",
                   "Caption 3": "The stepped courses of limestone blocks"}))
    for nid in DUP_ART:
        n = C.anki("notesInfo", notes=[nid])[0]
        imgs = re.findall(r'<img[^>]*>', n["fields"]["Artwork"]["value"])
        caps = n["fields"]["Captions"]["value"].split(" | ") if n["fields"]["Captions"]["value"].strip() else []
        k = next(i for i, x in enumerate(imgs) if re.search(r'termg-[^"]*-1\.', x))
        imgs.pop(k)
        if len(caps) == len(imgs) + 1:
            caps.pop(k)
        ch.append((n, {"Artwork": "".join(imgs), "Captions": " | ".join(caps)}))
    n = C.anki("notesInfo", notes=[1790240144093])[0]
    f = {k: n["fields"][k]["value"] for k in n["fields"]}
    assert "termg-rock-cut-architecture-1" in f["Picture 2"]
    ch.append((n, {"Picture 2": f["Picture 3"], "Caption 2": f["Caption 3"],
                   "Picture 3": f["Picture 4"], "Caption 3": f["Caption 4"],
                   "Picture 4": "", "Caption 4": ""}))
    return ch


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    for n, new in ch:
        print("==", C.plain(list(n["fields"].values())[0]["value"])[:40])
        for k, v in new.items():
            print("   %-9s %s" % (k, v[:150]))
    if "--apply" in sys.argv:
        for s, d in FILES.items():
            im = Image.open(SRC + s).convert("RGB")
            im.thumbnail((1600, 1600))
            im.save(os.path.join(MED, d), quality=88)
        bk = [{"nid": n["noteId"], "fields": {k: n["fields"][k]["value"] for k in new}} for n, new in ch]
        json.dump(bk, open("backups/fix_0927_images_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, new in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": new})
        print("applied", len(ch))
