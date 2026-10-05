# -*- coding: utf-8 -*-
"""hist_qb_apply.py -- put History v2 into Anki (AnkiConnect, Anki open). Dry run by default.

    py -3.9 hist_qb_apply.py                 dry run: what would be created, added, updated, suspended
    py -3.9 hist_qb_apply.py --apply         create note types, upload pictures, add/update notes, order the new queue
    py -3.9 hist_qb_apply.py --apply --deck "History"      (default deck: History)
    py -3.9 hist_qb_apply.py --apply --include prehistory,shang,zhou   also these sections (comma list; any subset)
    py -3.9 hist_qb_apply.py --supersede     list the old History Clue notes on the same topics (dry)
    py -3.9 hist_qb_apply.py --supersede --apply   suspend them and tag History::v1_superseded (reversible)

Safe to re-run: every note carries a stable v2 id in its Sources field, so a second run updates notes in
place (review history kept) instead of adding duplicates. Templates/CSS are only rewritten with
--update-templates. Everything touched is backed up to backups/hist_v2_*.json first.

Activity rule (DESIGN.md section 7): cards from my notes are active; supplement (qbreader) cards are
active at tier 1-2 and suspended at tier 3-4.
"""
import base64, hashlib, json, os, re, sys, time, unicodedata, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hist_qb_models as M  # noqa: E402
import images as IMG  # noqa: E402

TIERS = {1: "tier1-core", 2: "tier2-solid", 3: "tier3-deepcut", 4: "tier4-rare"}
DECK_FILES = ["cards_china_myth_lit"]


def anki(action, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", data=json.dumps(
        {"action": action, "version": 6, "params": params}).encode(), headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    if r.get("error"):
        raise RuntimeError("%s: %s" % (action, r["error"]))
    return r["result"]


def fold(s):
    s = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", "", s or ""))
    return re.sub(r"[^a-z0-9]+", "-", "".join(c for c in s if not unicodedata.combining(c)).lower()).strip("-")


def v2id(note):
    f = note["fields"]
    key = "|".join([note["model"], note["entity"], f.get("Answer", f.get("Title", "")),
                    f.get("Prompt", f.get("Text", f.get("Clue1", "")))])
    return "%s-%s" % (fold(note["entity"])[:24], hashlib.sha1(key.encode()).hexdigest()[:10])


def img_tag(key, media_dir, preview):
    if not key:
        return "", ""
    fn, cap = IMG.IMAGES[key][0], IMG.IMAGES[key][1]
    src = os.path.join(media_dir, fn) if preview else fn
    if preview:
        src = "file://" + src
    return '<img src="%s">' % src, cap


def build_fields(note, media_dir=os.path.join(HERE, "media"), preview=False):
    f = dict(note["fields"])
    tag, cap = img_tag(note.get("img"), media_dir, preview)
    if "Image" in [x for m in M.MODELS if m["name"] == note["model"] for x in m["fields"]]:
        f["Image"], f["Caption"] = tag, cap
    if note.get("pic"):
        f["Picture"] = img_tag(note["pic"], media_dir, preview)[0]
        f["PictureQuestion"] = note.get("picq", "")
    f["Sources"] = "v2id:%s; %s" % (v2id(note), "my notes" if note["src"] == "notes" else "qbreader supplement")
    tags = ["History::v2", "History::country::china", "History::period::" + note["period"],
            "History::kind::" + note["kind"], "History::tier::" + TIERS[note["tier"]],
            "History::source::" + ("notes" if note["src"] == "notes" else "qbreader"), "History::pos::" + note["pos"],
            "History::entity::" + fold(note["entity"])[:40]]
    return f, tags


def load_notes():
    out, files = [], list(DECK_FILES)
    extra = {"prehistory": "cards_china_prehistory_xia", "shang": "cards_china_shang", "zhou": "cards_china_zhou"}
    if "--include" in sys.argv:
        for name in sys.argv[sys.argv.index("--include") + 1].split(","):
            files.append(extra[name.strip()])
    for mod in files:
        out += __import__(mod).NOTES
    return out


def active(note):
    return note["src"] == "notes" or note["tier"] <= 2


def ensure_models(apply, update):
    have = set(anki("modelNames"))
    for m in M.MODELS:
        if m["name"] not in have:
            print("create note type", m["name"])
            if apply:
                anki("createModel", modelName=m["name"], inOrderFields=m["fields"], css=M.CSS,
                     isCloze=bool(m.get("is_cloze")), cardTemplates=[dict(t) for t in m["templates"]])
        elif update:
            print("update templates/CSS of", m["name"])
            if apply:
                back = dict(templates=anki("modelTemplates", modelName=m["name"]),
                            css=anki("modelStyling", modelName=m["name"]))
                json.dump(back, open(backup_path("models_" + m["name"].replace(" ", "")), "w", encoding="utf-8"),
                          ensure_ascii=False)
                anki("updateModelTemplates", model={"name": m["name"], "templates": {
                    t["Name"]: {"Front": t["Front"], "Back": t["Back"]} for t in m["templates"]}})
                anki("updateModelStyling", model={"name": m["name"], "css": M.CSS})


def backup_path(what):
    d = os.path.join(HERE, "backups")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "hist_v2_%s_%s.json" % (what, time.strftime("%Y%m%d_%H%M%S")))


def upload_media(notes, apply):
    keys = {n.get("img") for n in notes} | {n.get("pic") for n in notes}
    files = sorted({IMG.IMAGES[k][0] for k in keys if k})
    have = set(anki("getMediaFilesNames", pattern="hist2-*"))
    todo = [f for f in files if f not in have]
    missing = [f for f in todo if not os.path.exists(os.path.join(HERE, "media", f))]
    print("pictures: %d used, %d already in Anki, %d to upload, %d missing locally %s"
          % (len(files), len(files) - len(todo), len(todo), len(missing), missing[:5]))
    if apply:
        for f in todo:
            p = os.path.join(HERE, "media", f)
            if os.path.exists(p):
                anki("storeMediaFile", filename=f, data=base64.b64encode(open(p, "rb").read()).decode())


def existing_by_id():
    out = {}
    for m in M.MODELS:
        for ch in chunk(anki("findNotes", query='"note:%s" "Sources:*v2id:*"' % m["name"]), 400):
            for n in anki("notesInfo", notes=ch):
                mm = re.search(r"v2id:([\w-]+)", n["fields"]["Sources"]["value"])
                if mm:
                    out[mm.group(1)] = n
    return out


def chunk(seq, k):
    for i in range(0, len(seq), k):
        yield seq[i:i + k]


def order_new_queue(notes, ids, apply):
    """Giveaway clues first, then mid, then lead-ins; tier 1 before tier 2; entities interleaved round-robin."""
    rank = {"give": 0, "mid": 1, "lead": 2}
    by_entity = {}
    for n in sorted(notes, key=lambda n: (n["tier"], rank.get(n["pos"], 1))):
        by_entity.setdefault(n["entity"], []).append(n)
    order, queues = [], list(by_entity.values())
    while any(queues):
        for q in queues:
            if q:
                order.append(q.pop(0))
    cards = []
    for n in order:
        nid = ids.get(v2id(n))
        if nid:
            cards += anki("findCards", query="nid:%d is:new" % nid)
    print("new-card order: %d new cards interleaved over %d entities" % (len(cards), len(by_entity)))
    if apply and cards:
        start = min(c["due"] for c in anki("cardsInfo", cards=cards[:1])) if cards else 0
        for i, c in enumerate(cards):
            anki("setSpecificValueOfCard", card=c, keys=["due"], newValues=[str(start + i)], warning_check=True)


def supersede(apply):
    q = ('"note:History Clue" -tag:History::v2 (tag:History::period::*myth* OR tag:History::period::*legend* '
         'OR tag:History::period::*literat* OR tag:History::kind::*myth*)')
    nids = anki("findNotes", query=q)
    print("old History Clue notes on mythology/legend/literature: %d" % len(nids))
    info = anki("notesInfo", notes=nids[:15]) if nids else []
    for n in info:
        print("   ", re.sub(r"<[^>]+>", "", n["fields"].get("Prompt", {}).get("value", ""))[:90],
              "->", re.sub(r"<[^>]+>", "", n["fields"].get("Answer", {}).get("value", "")))
    if apply and nids:
        json.dump(anki("notesInfo", notes=nids), open(backup_path("superseded"), "w", encoding="utf-8"), ensure_ascii=False)
        cards = anki("findCards", query=q)
        anki("suspend", cards=cards)
        anki("addTags", notes=nids, tags="History::v1_superseded")
        print("suspended %d cards; undo with: search tag:History::v1_superseded, unsuspend, remove the tag" % len(cards))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    apply = "--apply" in sys.argv
    deck = sys.argv[sys.argv.index("--deck") + 1] if "--deck" in sys.argv else "History"
    if "--supersede" in sys.argv:
        return supersede(apply)
    notes = load_notes()
    print("History v2: %d notes (%s)" % (len(notes), ", ".join("%s %d" % (m["name"], sum(n["model"] == m["name"] for n in notes))
                                                           for m in M.MODELS)))
    ensure_models(apply, "--update-templates" in sys.argv)
    upload_media(notes, apply)
    have = existing_by_id() if set(anki("modelNames")) >= {m["name"] for m in M.MODELS} else {}
    add, upd = [], []
    for n in notes:
        f, tags = build_fields(n)
        (upd if v2id(n) in have else add).append((n, f, tags))
    print("add %d notes, update %d in place" % (len(add), len(upd)))
    if not apply:
        for n, f, t in add[:6]:
            print("   +", n["model"], "|", re.sub(r"<[^>]+>", "", f.get("Prompt", f.get("Title", f.get("Clue1", ""))))[:80],
                  "->", re.sub(r"<[^>]+>", "", f.get("Answer", "")))
        print("dry run only; add --apply to write")
        return
    if upd:
        json.dump([have[v2id(n)] for n, _, _ in upd], open(backup_path("updated"), "w", encoding="utf-8"), ensure_ascii=False)
    anki("createDeck", deck=deck)
    for n, f, tags in upd:
        nid = have[v2id(n)]["noteId"]
        anki("updateNoteFields", note={"id": nid, "fields": f})
        anki("addTags", notes=[nid], tags=" ".join(tags))
    for batch in chunk(add, 50):
        res = anki("addNotes", notes=[{"deckName": deck, "modelName": n["model"], "fields": f, "tags": tags,
                                        "options": {"allowDuplicate": True}} for n, f, tags in batch])
        bad = [b[0]["entity"] for b, r in zip(batch, res) if not r]
        if bad:
            print("   could not add:", bad)
    ids = {k: v["noteId"] for k, v in existing_by_id().items()}
    sus = [ids[v2id(n)] for n in notes if not active(n) and v2id(n) in ids]
    if sus:
        cards = [c for ch in chunk(sus, 200) for c in anki("findCards", query=" OR ".join("nid:%d" % x for x in ch))]
        anki("suspend", cards=cards)
        print("suspended %d cards (supplement tier 3-4)" % len(cards))
    order_new_queue([n for n in notes if active(n)], ids, True)
    print("done. Sync when convenient.")


if __name__ == "__main__":
    main()
