# -*- coding: utf-8 -*-
"""film_portraits_1002.py -- Film portraits with no copy of 1000px or more replaced by a different, larger portrait.

film_hr_1002.py upgrades a picture only to the same photograph. For 52 director and actor portraits TMDB's original
is itself about 500px (the w500 fetch was the whole file), and no larger copy exists. Portraits appear only on card
backs and, except two, carry no caption, so another photograph of the person does as well. Each pick was chosen by
eye from a contact sheet of TMDB profiles of 1000px or more, Wikipedia's lead image, and Commons (category and
search): a clear face, preferably from the person's working years, never colourized. Where the new photograph needs
one, a caption says who is who. Kieślowski, Vertov, and Ophüls have no photograph of 1000px or more anywhere
(TMDB, Commons, Wikidata, six Wikipedias: 700px at most), so their portraits are removed.

    py -3.9 film_portraits_1002.py [--apply]
"""
import json, os, re, sys, time
from PIL import Image
import concept_add as C
import film_hr_1002 as F
import img_upgrade_1002 as U

# person: index into portrait_cands.json (the contact sheet), or ("commons", sheet, index), or None to remove
PICKS = {
    "Andrei Tarkovsky": 1, "F. W. Murnau": 0, "Howard Hawks": 0, "Michael Haneke": 0, "David Lean": 0, "Robert Altman": 1,
    "Paul Thomas Anderson": 2, "Jean-Luc Godard": 1, "Satyajit Ray": 0, "Ingrid Bergman": 1, "Rita Hayworth": 1,
    "Jack Nicholson": 2, "Max von Sydow": 2, "Peter Lorre": 0, "Robert Bresson": 1, "Carl Theodor Dreyer": 0,
    "Wong Kar-wai": 2, "Abbas Kiarostami": 2, "Sergio Leone": 0, "Rainer Werner Fassbinder": 1, "Terrence Malick": 0,
    "D. W. Griffith": 0, "Miloš Forman": 0, "Jane Campion": 1, "Elia Kazan": 1, "Jean-Pierre Melville": 1,
    "Ousmane Sembène": 0, "Wes Anderson": 1, "Sofia Coppola": 1, "Derek Jarman": 1, "Barbara Stanwyck": 4,
    "Lynne Ramsay": 0, "Miranda July": 0, "Marcello Mastroianni": 1, "Kenji Mizoguchi": 0, "Chris Marker": 2,
    "Hou Hsiao-hsien": 1, "Claire Denis": 1, "Sam Peckinpah": 0, "Preston Sturges": 0, "Sidney Lumet": 0,
    "Mike Nichols": 0, "Kelly Reichardt": 3,
    "Joel and Ethan Coen": ("commons", "portrait_search", 3), "Yasujirō Ozu": ("commons", "portrait_cat", 0),
    "Mae West": ("commons", "portrait_cat", 10), "Roberto Rossellini": ("commons", "portrait_search", 2),
    "Erich von Stroheim": ("commons", "portrait_search", 0), "Douglas Sirk": ("commons", "portrait_cat", 2),
    "Krzysztof Kieślowski": None, "Dziga Vertov": None, "Max Ophüls": None,
}
# new Caption values ("" clears one that described the old picture)
CAPTIONS = {
    "Andrei Tarkovsky": "",
    "Chris Marker": "Marker hidden behind his camera: he rarely let himself be photographed, and often sent a picture of a cat instead",
    "Joel and Ethan Coen": "Ethan (left) and Joel Coen at the Castro Theatre, San Francisco, 2016",
    "Yasujirō Ozu": "Ozu (right, in his white hat) with Setsuko Hara on the set of <i>Tokyo Story</i>",
    "Douglas Sirk": "Sirk (left) with Jeff Chandler on the set of <i>Sign of the Pagan</i>, 1954",
    "Krzysztof Kieślowski": "", "Dziga Vertov": "", "Max Ophüls": "",
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", C.fold(s).lower()).strip("-")


def fetch(name, pick, cands):
    """The chosen portrait saved as a JPEG of 1000-2400px; returns its path."""
    if isinstance(pick, tuple):
        c = json.load(open(os.path.join(F.WORK, pick[1] + ".json"), encoding="utf-8"))[name][pick[2]]
        c = dict(c, url=c["url"].split("?")[0])
        return U.download(c)
    c = cands[name][pick]
    if c["src"] == "wp":
        return U.download({"title": "File:" + c["name"], "url": c["url"], "w": c["w"], "h": c["h"], "host": "en.wikipedia.org",
                           "mime": "image/tiff" if c["url"].lower().endswith((".tif", ".tiff")) else "image/jpeg"})
    src = F.get(F.IMG + "original" + c["path"], os.path.join(F.WORK, "o_" + c["path"].strip("/")))
    im = Image.open(src).convert("RGB")
    if max(im.size) > 2400:
        im.thumbnail((2400, 2400))
    out = os.path.join(F.WORK, "filmperson-hr-%s-1002.jpg" % slug(name))
    im.save(out, quality=90)
    return out


def main(really):
    rows = json.load(open(os.path.join(F.WORK, "portraits_none.json"), encoding="utf-8"))
    cands = json.load(open(os.path.join(F.WORK, "portrait_cands.json"), encoding="utf-8"))
    assert {r["title"] for r in rows} == set(PICKS), set(PICKS) ^ {r["title"] for r in rows}
    bk = {}
    for r in rows:
        name, pick = r["title"], PICKS[r["title"]]
        n = C.anki("notesInfo", notes=[r["nid"]])[0]
        pic, cap = n["fields"]["Picture"]["value"], n["fields"]["Caption"]["value"]
        if 'src="%s"' % r["file"] not in pic:
            print("skip (changed):", name)
            continue
        upd = {}
        if pick is None:
            upd["Picture"] = ""
        else:
            path = fetch(name, pick, cands)
            w, h = Image.open(path).size
            assert max(w, h) >= U.MIN, (name, w, h)
            new = os.path.basename(path)
            print("%-26s %4dx%-4d %s" % (name, w, h, new))
            if really:
                C.anki("storeMediaFile", filename=new, path=path)
            upd["Picture"] = pic.replace('src="%s"' % r["file"], 'src="%s"' % new)
        if name in CAPTIONS:
            upd["Caption"] = CAPTIONS[name]
        if really:
            bk[str(r["nid"])] = {"Picture": pic, "Caption": cap}
            C.anki("updateNoteFields", note={"id": r["nid"], "fields": upd})
    if really:
        json.dump(bk, open("backups/film_portraits_1002_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        print("updated", len(bk), "notes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
