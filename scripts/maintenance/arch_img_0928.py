# -*- coding: utf-8 -*-
"""arch_img_0928.py -- replacement pictures for Architecture, chosen from Commons contact sheets.

Follows arch_fix_0928.py, which removed pictures that were not the building or the idea. Here:
  * cards that removal left thin get a relevant picture: Angkor Wat (the Churning of the Sea of
    Milk relief, the central towers), the Kimbell (a vaulted gallery), Brutalism (the Barbican,
    Boston City Hall, both named in its notes), Rock-cut architecture (Lalibela, Petra), Flying
    buttress (the chevet of Notre-Dame);
  * style cards whose pictures were not architecture: Minimalism (Tony Smith and Donald Judd
    sculptures -> Zumthor's Therme Vals), Rococo (a Chelsea porcelain group and Fragonard's The
    Swing -> the Amalienburg and the Wieskirche, both named in its notes), Art Deco (a fair poster
    and a Lalique car mascot -> Ocean Drive, the Eastern Columbia Building), Art Nouveau (a Jugend
    cover and a Tiffany lamp -> Otto Wagner's Majolikahaus);
  * figure cards that showed the architect's childhood haunts or family rather than his buildings:
    I. M. Pei (a Suzhou garden and the Bund -> the National Gallery's East Building, the Bank of
    China Tower), Walter Gropius (a family photograph -> the Fagus Factory), Sinan (the Ferhat Pasha
    Mosque, by his school, and an unnamed view -> the Süleymaniye and the Selimiye), Philip Johnson
    ("Mobiliario principal" -> the AT&T Building).
Every file is a Commons image, resized to at most 1280 px.

    py -3.9 arch_img_0928.py [--apply]
"""
import json, os, sys, time
from PIL import Image
import concept_add as C

SRC = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/4c6fe2ff-c3a6-47fb-8b54-226f916ad6af/scratchpad/img/"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")

# nid -> {slot: (scratch file or None to clear the slot, media name, caption)}
PICS = {
 1596400691402: {2: ("ar_angkor_relief_1.jpg", "arch-angkor-wat-relief.jpg", "The Churning of the Sea of Milk, in the bas-relief gallery"),
                 3: ("ar_angkor_towers_1.jpg", "arch-angkor-wat-towers.jpg", "The central towers, standing for the five peaks of Mount Meru")},
 1788200166517: {3: ("ar_kimbell_vault_0.jpg", "arch-kimbell-gallery.jpg", "A gallery under the cycloid vaults, lit from the slit at each crown")},
 1788585240715: {3: ("ar_barbican_3.jpg", "arch-brutalism-barbican.jpg", "The Barbican Estate, London (1965–1976), by Chamberlin, Powell and Bon"),
                 4: ("ar_bostoncityhall_1.jpg", "arch-brutalism-boston-city-hall.jpg", "Boston City Hall (1968), by Kallmann McKinnell & Knowles")},
 1790240144093: {3: ("ar_lalibela_1.jpg", "arch-rockcut-lalibela.jpg", "The Church of Saint George, Lalibela, Ethiopia, cut down into the rock"),
                 4: ("ar_petra_0.jpg", "arch-rockcut-petra.jpg", "The Treasury (Al-Khazneh), Petra, Jordan")},
 1788585237929: {3: ("ar_nd_buttress_0.jpg", "arch-flying-buttress-notre-dame.jpg", "Flying buttresses around the apse of Notre-Dame de Paris")},
 1790240144433: {2: ("ar_vals_0.jpg", "arch-minimalism-vals.jpg", "Peter Zumthor, Therme Vals, Switzerland, 1996"),
                 3: (None, "", "")},
 1788585240621: {2: ("ar_amalienburg_1.jpg", "arch-rococo-amalienburg.jpg", "François de Cuvilliés, the Hall of Mirrors in the Amalienburg, Munich, 1734–1739"),
                 3: ("ar_wies_2.jpg", "arch-rococo-wieskirche.jpg", "Dominikus Zimmermann, the Wieskirche, Bavaria, 1745–1754")},
 1788585240681: {2: ("ar_miamideco_3.jpg", "arch-artdeco-ocean-drive.jpg", "Art Deco hotels on Ocean Drive, Miami Beach"),
                 3: ("ar_eastcolumbia_2.jpg", "arch-artdeco-eastern-columbia.jpg", "The Eastern Columbia Building, Los Angeles (1930), in turquoise terracotta")},
 1788585240657: {1: ("ar_majolika_3.jpg", "arch-artnouveau-majolikahaus.jpg", "Otto Wagner's Majolikahaus, Vienna (1898–1899)"),
                 2: ("KEEP3", "", ""),       # Guimard's Métro entrance moves up
                 3: (None, "", "")},
 1788620917728: {2: ("ar_ngaeast_0.jpg", "arch-pei-nga-east.jpg", "The East Building of the National Gallery of Art, Washington D.C. (1978)"),
                 3: ("ar_bankofchina_0.jpg", "arch-pei-bank-of-china.jpg", "The Bank of China Tower, Hong Kong (1990)")},
 1788620819847: {2: ("ar_fagus_0.jpg", "arch-gropius-fagus.jpg", "The Fagus Factory, Alfeld (1911–1913), designed with Adolf Meyer")},
 1788621011600: {1: ("ar_suleymaniye_3.jpg", "arch-sinan-suleymaniye.jpg", "The Süleymaniye Mosque, Istanbul (1550–1557), from its courtyard"),
                 2: ("ar_selimiye_2.jpg", "arch-sinan-selimiye.jpg", "The Selimiye Mosque, Edirne (1568–1575), his masterpiece")},
 1788620841629: {3: ("ar_madison550_0.jpg", "arch-johnson-att-building.jpg", "The AT&amp;T Building (now 550 Madison Avenue), New York City (1984), with its broken pediment")},
}


def plan():
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(PICS))}
    ch = []
    for nid, slots in PICS.items():
        F = {k: v["value"] for k, v in ns[nid]["fields"].items()}
        f = {}
        for s, (src, name, cap) in slots.items():
            if src == "KEEP3":
                f["Picture %d" % s], f["Caption %d" % s] = F["Picture 3"], F["Caption 3"]
            elif src is None:
                f["Picture %d" % s], f["Caption %d" % s] = "", ""
            else:
                f["Picture %d" % s], f["Caption %d" % s] = '<img src="%s">' % name, cap
        ch.append((ns[nid], f))
    return ch


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    for n, f in ch:
        print("##", C.plain(n["fields"]["Name"]["value"]))
        for k in sorted(f):
            if k.startswith("Caption"):
                print("   %s: %s -> %s" % (k, C.plain(n["fields"][k]["value"])[:50], C.plain(f[k])[:70]))
    if "--apply" in sys.argv:
        for slots in PICS.values():
            for src, name, cap in slots.values():
                if src and src != "KEEP3":
                    im = Image.open(SRC + src).convert("RGB")
                    if max(im.size) > 1280:
                        im.thumbnail((1280, 1280))
                    im.save(os.path.join(MED, name), quality=88)
        json.dump([{"nid": n["noteId"], **{k: n["fields"][k]["value"] for k in f}} for n, f in ch],
                  open("backups/arch_img_0928_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, f in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": f})
        print("applied", len(ch))
