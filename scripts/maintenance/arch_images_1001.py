# -*- coding: utf-8 -*-
"""arch_images_1001.py -- Architecture, Carter's notes of 2026-10-01.

- "Each architecture work should have at least two images (eg biltmore estate, jfk library do not)": the 30 live works
  with one picture get one or two more, chosen on contact sheets from the building's Wikipedia article and Commons.
- "Bad image: Museum of pop culture, Hill house, British museum": MoPOP showed an abstract close-up of metal panels;
  Hill House and the British Museum showed old prints with the building's name printed under them, which answered
  the card. The Transportation Building's only picture had the same fault ("THE GOLDEN DOOR, TRANSPORTATION
  BUILDING"): it is cropped, as is the guidebook engraving added beside it.
- Captions for the seven works that had none.
- "Sant Andrea mantua card asks for location": a name that contains the city answers PICTURE and NAME to LOCATION.
  NameTells is set (the card renders empty) and the card suspended, for Sant'Andrea, Mantua and Imperial Hotel, Tokyo,
  the only two such names among live cards (the card shows Name only, not Alternate).
- "Trencadis not italicized in park guell card": *trencadís*, with its accent.

    py -3.9 arch_images_1001.py [--apply]
"""
import base64
import json
import os
import re
import sys
import time

from PIL import Image

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
SP = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\1d6bde35-08b4-4391-958b-52d033191c05\scratchpad\arch2"
OLD = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\4c6fe2ff-c3a6-47fb-8b54-226f916ad6af\scratchpad\img"
KEEP = "keep"   # (KEEP, n): the note's current Picture n, caption as given (None: as it is)

# name -> the full picture list in order: (source, caption); a source is (KEEP, n), "c:key_i" (first search),
# "d:key_i" (second search), or a path; crops as ("crop", source, box)
PLAN = {
    "Leaning Tower of Pisa": [((KEEP, 1), "The tower from above, leaning to the south"), ("c:pisa_9", "The tower behind the cathedral on the Piazza dei Miracoli"),
                              ("c:pisa_8", "The blind arcades of its base")],
    "Whitney Museum of American Art (Breuer Building)": [((KEEP, 1), "The stepped granite block on Madison Avenue"),
                                                         ("c:whitney_3", "The lobby under its grid of round ceiling lights"),
                                                         ("c:whitney_8", "A cantilevered upper floor and one of the trapezoid windows")],
    "Gateway Arch": [((KEEP, 1), "The arch above the St. Louis skyline at night"), ("c:gateway_7", "From the air, framing the Old Courthouse"),
                     ("c:gateway_9", "One of the tram capsules that climb its legs")],
    "Hollyhock House": [((KEEP, 1), "The house on Olive Hill"), ("c:hollyhock_6", "The living-room hearth"),
                        ("c:hollyhock_2", "The colonnade around the garden court, 1921")],
    "Price Tower": [((KEEP, 1), "The tower and its copper louvres"), ("c:price_3", "The entrance court under a copper-panelled canopy"),
                    ("c:price_7", "The lobby ceiling")],
    "Auditorium Building": [((KEEP, 1), "The building and its tower"), ("d:auditorium_10", "The theatre's arches, from the balcony"),
                            ("d:auditorium_0", "Box seats in the theatre")],
    "East Building, National Gallery of Art": [((KEEP, 1), "The 19-degree corner"),
                                               (os.path.join(OLD, "ar_ngaeast_0.jpg"), "The west front, with the plaza's glass pyramids"),
                                               ("d:ngaeast_0", "The atrium under its space-frame skylight, with Alexander Calder's mobile")],
    "Jay Pritzker Pavilion": [((KEEP, 1), None), ("c:pritzker_0", "The trellis over the Great Lawn, from above"),
                              ("c:pritzker_3", "The lawn and trellis from the stage")],
    "John F. Kennedy Presidential Library": [((KEEP, 1), None), ("c:jfklib_7", "The glass pavilion and its hanging flag"),
                                             ("c:jfklib_5", "On Columbia Point at dusk")],
    "John Hancock Tower": [((KEEP, 1), None), ("c:hancock_1", "Trinity Church reflected in the tower")],
    "Dulles Airport Main Terminal": [((KEEP, 1), None), ("d:dulles_4", "The hall under its suspended concrete roof"),
                                     ("d:dulles_11", "The terminal and control tower from the landside")],
    "Stata Center": [((KEEP, 1), None), ("c:stata_7", "The brick and steel volumes along Vassar Street"),
                     ("c:stata_4", "The terraced steps of the courtyard")],
    "Transportation Building": [(("crop", (KEEP, 1), (16, 45, 1257, 925)), None),
                                (("crop", "c:transport_1", (0, 0, 1920, 866)), "The building across the lagoon, from an 1893 guidebook")],
    "Kansai International Airport Terminal": [((KEEP, 1), None), ("c:kansai_4", "The terminal's curved roof from the apron"),
                                              ("c:kansai_1", "The airport's island, flooded by Typhoon Jebi in 2018")],
    "North Christian Church": [((KEEP, 1), None), ("c:northchristian_8", "The sanctuary under its oculus"),
                               ("c:northchristian_3", "The spire above the approach steps")],
    "Palace of Westminster": [((KEEP, 1), None), ("c:westminster_11", "The Central Lobby"), ("c:westminster_5", "Elizabeth Tower at the north end")],
    "Green Building": [((KEEP, 1), None), ("c:greenbldg_3", "Above McDermott Court and Alexander Calder's <i>La Grande Voile</i>"),
                       ("c:greenbldg_6", "The weather-radar dome on its roof")],
    "Dallas City Hall": [((KEEP, 1), None), ("c:dallas_3", "The north front leaning out over the plaza"), ("c:dallas_5", "From Reunion Tower")],
    "8 Spruce Street": [((KEEP, 1), None), ("c:spruce_0", "The rippling stainless-steel skin")],
    "Carpenter Center for the Visual Arts": [((KEEP, 1), None), ("c:carpenter_2", "The ramp that runs through the building"),
                                             ("c:carpenter_0", "A curved studio wall")],
    "Museum of Pop Culture": [("c:emp_0", "From the air, beside the Space Needle"), ("c:emp_9", "The Seattle Center monorail running through it"),
                              ("c:emp_1", "The coloured metal skins")],
    "General Motors Technical Center": [((KEEP, 1), None), ("c:gmtech_2", "The stainless-steel Design Dome"),
                                        ("c:gmtech_6", "The campus and its lake from the air")],
    "Cardboard Cathedral": [((KEEP, 1), None), ("d:cardboard_0", "Inside: the cardboard-tube roof and the coloured-glass end wall")],
    "Pennsylvania Station": [((KEEP, 1), None), ("c:pennstation_7", "The Doric colonnade on Seventh Avenue"),
                             ("c:pennstation_6", "The steel-and-glass concourse")],
    "AEG Turbine Factory": [((KEEP, 1), None), ("c:aeg_2", "The glazed side wall between its steel piers")],
    "Nakagin Capsule Tower": [((KEEP, 1), None), ("c:nakagin_0", "Inside a capsule, with its built-in fittings"),
                              ("c:nakagin_1", "A single capsule, preserved after the 2022 demolition")],
    "Transamerica Pyramid": [((KEEP, 1), None), ("c:transamerica_4", "From above"), ("c:transamerica_7", "The angled columns of its base")],
    "Hill House": [("c:hillhouse_0", "The house above Helensburgh"), ("c:hillhouse_1", "The hall, with Mackintosh's lanterns and furniture"),
                   ("c:hillhouse_2", "Inside the steel-mesh box built over it in 2019")],
    "St. Vitus Cathedral": [((KEEP, 1), None), ("c:stvitus_2", "The west front"), ("c:stvitus_3", "The Golden Gate's Last Judgement mosaic")],
    "Biltmore Estate": [((KEEP, 1), None), ("c:biltmore_11", "The entrance front"), ("c:biltmore_1", "The Winter Garden")],
    "British Museum": [("d:britmus_3", "The south front's colonnade from the forecourt"), ((KEEP, 2), None),
                       ("d:britmus_4", "The portico's Ionic columns")],
}
NAMETELLS = {"Sant'Andrea, Mantua", "Imperial Hotel, Tokyo"}
TEXT = {"Park Güell": ("Notes", "faced in trencadis mosaic", "faced in <i>trencadís</i> mosaic")}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", C.fold(s)).strip("-")


CANDS = {"c": json.load(open(os.path.join(SP, "r", "cand_all.json"), encoding="utf-8")),
         "d": json.load(open(os.path.join(SP, "r", "cand2.json"), encoding="utf-8"))}


def source_file(src):
    """the local file for a source, re-fetched when a rate-limited download left it empty; and its Commons title"""
    if isinstance(src, str) and src[:2] in ("c:", "d:"):
        key, i = src[2:].rsplit("_", 1)
        t, w, h, url = CANDS[src[0]][key][int(i)]
        p = os.path.join(SP, "img", "%s%s_%s.jpg" % (key, "2" if src[0] == "d" else "", i))
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            sys.path.insert(0, SP)
            from wm import fetch
            if os.path.exists(p):
                os.remove(p)
            fetch(url, p)
        return p, t
    return src, "File:" + os.path.basename(src)


def main(apply):
    notes = C.anki("notesInfo", notes=C.anki("findNotes", query="note:Architecture"))
    by_name = {C.plain(n["fields"]["Name"]["value"]).strip(): n for n in notes}
    changes, backup, store, sources = {}, {}, [], {}
    for name, pics in PLAN.items():
        n = by_name[name]
        f = {k: v["value"] for k, v in n["fields"].items()}
        new, k = {}, 0
        used = set(re.findall(r'src="([^"]+)"', " ".join(f["Picture %d" % i] for i in range(1, 5))))
        for src, cap in pics:
            k += 1
            crop = None
            if isinstance(src, tuple) and src[0] == "crop":
                src, crop = src[1], src[2]
            if isinstance(src, tuple) and src[0] == KEEP:
                fn = re.search(r'src="([^"]+)"', f["Picture %d" % src[1]]).group(1)
                old_cap = f["Caption %d" % src[1]]
                if crop is None:
                    new["Picture %d" % k], new["Caption %d" % k] = '<img src="%s">' % fn, old_cap if cap is None else cap
                    continue
                path, title = os.path.join(MED, fn), "(cropped from %s)" % fn
                cap = old_cap if cap is None else cap
            else:
                path, title = source_file(src)
            im = Image.open(path).convert("RGB")
            if crop:
                im = im.crop(crop)
            if max(im.size) > 1280:
                im.thumbnail((1280, 1280))
            j = 1
            while True:
                fn = "arch-%s-%d%s.jpg" % (slug(name), j, "c" if crop else "")
                if fn not in used and not os.path.exists(os.path.join(MED, fn)):
                    break
                j += 1
            used.add(fn)
            store.append((fn, im))
            sources[fn] = title
            new["Picture %d" % k], new["Caption %d" % k] = '<img src="%s">' % fn, cap
        for i in range(k + 1, 5):
            new["Picture %d" % i], new["Caption %d" % i] = "", ""
        new = {x: v for x, v in new.items() if v != f[x]}
        changes[n["noteId"]] = new
        backup[n["noteId"]] = {x: f[x] for x in new}
        print("%-45s %s" % (name[:45], " | ".join(C.plain(new.get("Caption %d" % i, f["Caption %d" % i]))[:30] for i in range(1, k + 1))))
    for name, (fld, old, rep) in TEXT.items():
        n = by_name[name]
        v = n["fields"][fld]["value"]
        assert old in v, name
        changes.setdefault(n["noteId"], {})[fld] = v.replace(old, rep)
        backup.setdefault(n["noteId"], {})[fld] = v
    tells = [by_name[x]["noteId"] for x in NAMETELLS]
    for nid in tells:
        changes.setdefault(nid, {})["NameTells"] = "1"
        backup.setdefault(nid, {})["NameTells"] = next(x for x in notes if x["noteId"] == nid)["fields"]["NameTells"]["value"]
    print(len(store), "new pictures;", len(changes), "notes")
    if not apply:
        for fn, im in store:
            im.save(os.path.join(SP, "preview_" + fn), quality=85)
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump(backup, open(os.path.join(HERE, "backups", "arch_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(sources, open(os.path.join(HERE, "data", "arch_image_sources_1001.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for fn, im in store:
        import io
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=88)
        C.anki("storeMediaFile", filename=fn, data=base64.b64encode(buf.getvalue()).decode())
    for nid, f in changes.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": f})
    cards = C.anki("findCards", query="nid:%s card:1" % ",".join(str(x) for x in tells))
    live = [c["cardId"] for c in C.anki("cardsInfo", cards=cards) if c["queue"] != -1]
    if live:
        C.anki("suspend", cards=live)
    print("applied; suspended", len(live), "location cards")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
