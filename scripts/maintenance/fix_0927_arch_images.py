# -*- coding: utf-8 -*-
"""fix_0927_arch_images.py -- active Architecture cards with a single picture get a second view,
and two captions are fixed. Candidates viewed on a contact sheet next to each card's existing
picture, so nothing repeats it; the Guaranty terracotta close-up that spells "PRUDENTIAL" (its
other name) was passed over because it would give the answer away.

    py -3.9 fix_0927_arch_images.py [--apply]
"""
import json, os, sys, time
from PIL import Image
import concept_add as C

S = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/4c6fe2ff-c3a6-47fb-8b54-226f916ad6af/scratchpad/img/"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
FILES = {"s_tem_06.jpg": "arch-tempietto-rear.jpg",
         "s_bns_07.jpg": "arch-beijing-stadium-lattice.jpg",
         "s_wam_01.jpg": "arch-washington-monument-aerial.jpg",
         "s_wdc_05.jpg": "arch-disney-hall-steel-curves.jpg",
         "s_mil_01.jpg": "arch-milwaukee-brise-soleil.jpg",
         "s_mil_03.jpg": "arch-milwaukee-quadracci-interior.jpg",
         "s_gua_06.jpg": "arch-guaranty-cornice.jpg",
         "s_vanalen_00.jpg": "arch-chrysler-ornament.jpg"}
EDITS = {
    "Tempietto": {"Picture 2": "arch-tempietto-rear.jpg", "Caption 2": "The rear, with the ring of Doric columns and the balustrade"},
    "Beijing National Stadium": {"Picture 2": "arch-beijing-stadium-lattice.jpg", "Caption 2": "The interwoven steel members that gave it the name Bird's Nest"},
    "Washington Monument": {"Picture 2": "arch-washington-monument-aerial.jpg", "Caption 2": "The obelisk on the National Mall, from the air"},
    "Walt Disney Concert Hall": {"Picture 2": "arch-disney-hall-steel-curves.jpg", "Caption 2": "The curving stainless-steel panels"},
    "Milwaukee Art Museum": {"Picture 2": "arch-milwaukee-brise-soleil.jpg", "Caption 2": "The Burke Brise Soleil, its wings open above the Quadracci Pavilion",
                             "Picture 3": "arch-milwaukee-quadracci-interior.jpg", "Caption 3": "Inside the Quadracci Pavilion"},
    "Guaranty Building": {"Picture 2": "arch-guaranty-cornice.jpg", "Caption 2": "The top floors: arched windows, round oculi, and the cornice, all in ornamented terracotta"},
    "William Van Alen": {"Picture 2": "arch-chrysler-ornament.jpg", "Caption 2": "Automobile ornament on the Chrysler Building's setbacks"},
    "Santa Maria Novella": {"Caption 2": "The Gothic brick flank of the church"},
    "Guggenheim Museum Bilbao": {"Caption 2": "The museum at night on the Nervión"},
}


def note(name):
    ns = [n for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"deck:Architecture" "Name:*%s*"' % name))
          if C.plain(n["fields"]["Name"]["value"]) == name]
    assert len(ns) == 1, (name, len(ns))
    return ns[0]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = []
    for name, ed in EDITS.items():
        n = note(name)
        new = {k: ('<img src="%s">' % v if k.startswith("Picture") else v) for k, v in ed.items()}
        for k in new:
            if k.startswith("Picture"):
                assert not n["fields"][k]["value"].strip(), (name, k, "not empty")
        ch.append((n, new))
        print(name, new)
    if "--apply" in sys.argv:
        for s, d in FILES.items():
            im = Image.open(S + s).convert("RGB"); im.thumbnail((1600, 1600)); im.save(os.path.join(MED, d), quality=88)
        json.dump([{"nid": n["noteId"], "fields": {k: n["fields"][k]["value"] for k in new}} for n, new in ch],
                  open("backups/fix_0927_arch_images_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, new in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": new})
        print("applied", len(ch))
