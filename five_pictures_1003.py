"""five_pictures_1003.py -- Carter, 2026-10-03: "AEG turbine factory could use an image showcasing the whole thing";
"others that could use better images (just to showcase them in entirety): moscow kremlin, bauhaus dessau - first two
images are the same perspective, glass house, westminster abbey". Picks from contact sheets (Commons searches,
data/five_pictures_1003_cands.json). Bauhaus: no corner view, because the stair tower's BAUHAUS lettering would answer the
card; the curtain wall is cropped from candidate 3 without it. Glass House drops Da Monsta and Bauhaus drops Gropius's
Konsum building in Törten (other buildings than the card's).        py -3.9 five_pictures_1003.py [--apply]
"""
import base64, hashlib, io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image
import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "renders", "five_pictures_1003")
UA = {"User-Agent": "QB-anki-deck/1.0 (personal study deck; yottc@mcmaster.ca)"}
CANDS = json.load(open(os.path.join(HERE, "data", "five_pictures_1003_cands.json"), encoding="utf-8"))
KEEP = "keep"
PLAN = {  # name -> full new picture list [(source, caption)]; source: ("c", i[, crop fraction box]) or (KEEP, n)
    "AEG Turbine Factory": [(("c", 1), "The hall from the street corner: the gable end and the long glazed side"),
                            ((KEEP, 2), None)],
    "Moscow Kremlin": [(("c", 5), "The south wall and its towers above the Moskva River, with the Grand Kremlin Palace and the cathedrals behind"),
                       ((KEEP, 2), None)],
    "Bauhaus Dessau": [((KEEP, 1), None), (("c", 9), "The vocational-school wing, with its ribbon windows"),
                       (("c", 3, (0.0, 0.0, 0.68, 1.0)), "The glass curtain wall of the workshop wing")],
    "Glass House": [(("c", 0), "The house on its lawn: glass walls on a black steel frame"),
                    (("c", 10), "The single open room, divided only by a brick cylinder and free-standing furniture")],
    "Westminster Abbey": [(("c", 11), "The north side, with the north transept and the nave's flying buttresses"),
                          ((KEEP, 1), "The west front and its two towers, finished to Nicholas Hawksmoor's design in 1745"),
                          ((KEEP, 2), "The cloister")],
}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def fetch(title):
    p = os.path.join(DL, re.sub(r"[^\w.-]+", "_", title[5:]))
    if not os.path.exists(p):
        q = {"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 3000, "format": "json", "formatversion": 2}
        ii = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)))["query"]["pages"][0]["imageinfo"][0]
        time.sleep(2.0)
        open(p, "wb").write(get(ii.get("thumburl") or ii["url"])); time.sleep(2.0)
    return Image.open(p).convert("RGB")


def main(apply):
    os.makedirs(DL, exist_ok=True)
    byname = {C.plain(n["fields"]["Name"]["value"]).strip(): n for n in C.anki("notesInfo", notes=C.anki("findNotes", query="note:Architecture"))}
    backup = {}
    for nm, pics in PLAN.items():
        n = byname[nm]; f = n["fields"]; new = {}
        for k, (src, cap) in enumerate(pics, 1):
            if src[0] == KEEP:
                new["Picture %d" % k] = f["Picture %d" % src[1]]["value"]
                new["Caption %d" % k] = f["Caption %d" % src[1]]["value"] if cap is None else cap
                continue
            im = fetch(CANDS[nm][src[1]]["title"])
            if len(src) > 2:
                a, b, c, d = src[2]; im = im.crop((round(a * im.width), round(b * im.height), round(c * im.width), round(d * im.height)))
            if max(im.size) > 2200:
                s = 2200 / max(im.size); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            assert max(im.size) >= 1000
            buf = io.BytesIO(); im.save(buf, format="JPEG", quality=85, optimize=True); data = buf.getvalue()
            fn = "arch-%s-%d-%s.jpg" % (nm.lower().replace(" ", "-"), k, hashlib.md5(data).hexdigest()[:6])
            if apply:
                C.anki("storeMediaFile", filename=fn, data=base64.b64encode(data).decode())
            new["Picture %d" % k], new["Caption %d" % k] = '<img src="%s">' % fn, cap
        for k in range(len(pics) + 1, 5):
            new["Picture %d" % k], new["Caption %d" % k] = "", ""
        print(nm, " | ".join(C.plain(new["Caption %d" % k])[:40] for k in range(1, len(pics) + 1)))
        if apply:
            backup[n["noteId"]] = {k: f[k]["value"] for k in new}
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": new})
    if apply:
        json.dump(backup, open(os.path.join(HERE, "backups", "five_pictures_%s.json" % time.strftime("%Y%m%d_%H%M%S")), "w", encoding="utf-8"), ensure_ascii=False)
        print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
