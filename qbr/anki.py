# -*- coding: utf-8 -*-
"""qbr.anki -- what the Anki collection already holds, so a search can mark it. Read-only: this never writes to Anki.

    idx = index()
    have(idx, "black square")   -> "studied"    a note is named this and has an unsuspended card that has been reviewed
                                   "card"       a note is named this and has an unsuspended card, none reviewed yet
                                   "suspended"  a note is named this, every card suspended
                                   "on-note"    the answer's own note holds it (back information, not a card of its own);
                                   "on-note-suspended"  the same, but that note's cards are all suspended
                                   "text"       only some other note's text holds it: not coverage
                                   ""           nowhere in the collection

A note's name is its first field when that is short (a title or a term, not a cloze sentence), its Title/Name-type
fields, plus anything in a field called Alternate. Reading goes through AnkiConnect, so Anki must be open; the
result is cached in qbr/data/anki_index.json for twelve hours, and a stale cache is used (and said to be stale) when
Anki is closed.
"""
import json
import os
import re
import time
import urllib.request

from .store import PATH
from .text import _key, fold, plain

CACHE = os.path.join(os.path.dirname(PATH), "anki_index.json")
_CLOZE = re.compile(r"\{\{c\d+::(.*?)(?:::[^}]*)?\}\}", re.S)
_MIDDOT = re.compile(r"(?<=[A-Za-z0-9])[\u00b7\u2022\u22c5](?=[A-Za-z0-9])")
_ALT = {"alternate", "alternates", "alt", "aliases", "also"}
_NAME_FIELDS = {"title", "work", "name", "answerline", "term"}
VERSION = 2                     # index layout: 2 added studied cards and the answer notes' suspension
_RANK = {"studied": 6, "card": 5, "suspended": 4, "on-note": 3, "on-note-suspended": 2, "text": 1, "": 0}
_CREATOR_FIELDS = {"composer", "artist", "creator", "author", "poet", "architect", "librettist",
                   "choreographer", "conductor", "painter", "designer"}


def _note_fold(s):
    """Fold Anki note text, joining middle-dot acronyms (c·A·M·P -> camp) while keeping standard folded tokens."""
    s = s or ""
    joined = _MIDDOT.sub("", s)
    return (fold(joined) + " " + fold(s)).strip() if joined != s else fold(s)


def _creator_leak(thing, creators):
    """Does a named candidate merely repeat a creator already printed on the note?"""
    candidate = _key(thing)
    if not candidate:
        return False
    words = set(candidate.split())
    return any(words <= set(_key(creator).split()) for creator in creators if _key(creator))


def _call(action, **params):
    req = urllib.request.Request("http://127.0.0.1:8765",
                                 data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
                                 headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    if r.get("error"):
        raise RuntimeError(r["error"])
    return r["result"]


def build(query="deck:*", *, persist=True):
    """read every note from Anki and write the cache"""
    nids = _call("findNotes", query=query)
    live = set(_call("findNotes", query=f"({query}) -is:suspended"))
    studied = set(_call("findNotes", query=f"({query}) -is:suspended -is:new"))
    names, by_name, by_status, texts = {}, {}, {}, []
    for i in range(0, len(nids), 500):
        for n in _call("notesInfo", notes=nids[i:i + 500]):
            fields = sorted(n["fields"].items(), key=lambda kv: kv[1]["order"])
            vals = [(k, plain(_CLOZE.sub(r"\1", v["value"]))) for k, v in fields]
            status = "studied" if n["noteId"] in studied else "card" if n["noteId"] in live else "suspended"
            own = [vals[0][1]] if vals and len(vals[0][1].split()) <= 8 else []
            for k, v in vals:
                if k.lower().strip() in _NAME_FIELDS and v and len(v.split()) <= 16:   # long titles are names too
                    own.append(v)
                if k.lower() in _ALT and v:
                    own += re.split(r"\s*(?:;|/|,|\bor\b)\s*", v)
            own = list(dict.fromkeys(x for x in own if x))
            ntext = _note_fold(" ".join(v for _, v in vals))
            for x in own:
                k = _key(x)
                if len(k) > 1:
                    if _RANK[status] > _RANK[names.get(k, ("", ""))[0]]:
                        names[k] = (status, n["modelName"])
                    by_name[k] = (by_name.get(k, "") + " " + ntext).strip()
                    if status != "suspended":
                        by_status[k] = "active"
                    else:
                        by_status.setdefault(k, "suspended")
            texts.append(ntext)
    idx = {"v": VERSION, "built": time.time(), "notes": len(nids), "names": names, "by_name": by_name,
           "by_status": by_status, "text": " | ".join(texts)}
    if persist:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump(idx, f, ensure_ascii=False)
    return idx


def index(max_age_h=12, refresh=False):
    """The index, from the cache when it is fresh enough, otherwise rebuilt from Anki. idx["stale"] is set when Anki
    could not be reached and an older cache was used instead."""
    old = None
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as f:
            old = json.load(f)
        if not refresh and old.get("v") == VERSION and time.time() - old["built"] < max_age_h * 3600:
            return old
    try:
        return build()
    except Exception as e:
        if old:
            old["stale"] = "Anki not reachable (%s); using the index from %s" % (
                type(e).__name__, time.strftime("%Y-%m-%d %H:%M", time.localtime(old["built"])))
            if old.get("v") != VERSION:
                old["stale"] += ", which cannot tell studied cards from new ones"
            return old
        raise RuntimeError("Anki is not reachable through AnkiConnect (localhost:8765) and there is no saved index. "
                           "Open Anki and run this again.") from e


def have(idx, key, also=(), target_names=()):
    """Is this folded name in the collection, and how? One of the labels in the module docstring; "on-note" looks
    in the target answer's own notes (`target_names`)."""
    best = ""
    by_name = idx.get("by_name") or {}
    by_status = idx.get("by_status") or {}
    own = [_key(n) for n in target_names if _key(n) in by_name]
    own_blob = " " + " ".join(by_name[k] for k in own) + " "
    own_live = any(by_status.get(k, "active") == "active" for k in own)
    for k in [_key(key)] + [_key(a) for a in also]:
        if not k:
            continue
        if k in idx["names"]:
            got = idx["names"][k][0]
        elif (" %s " % k) in own_blob:
            got = "on-note" if own_live else "on-note-suspended"
        elif (" %s " % k) in (" %s " % idx["text"]):
            got = "text"
        else:
            got = ""
        if _RANK[got] > _RANK[best]:
            best = got
    return best


def brief_notes(deck, tier=None, pattern=None, cat=None, top=12):
    """Compare a deck's fields with recurring clues, marking those already on the target note.

    This reads the collection through AnkiConnect and does not write to it.
    """
    from .clues import profile
    tiers = {1: "tier1-core", 2: "tier2-solid", 3: "tier3-deepcut", 4: "tier4-rare"}
    q = '"deck:%s"' % deck + (" tag:*::tier::%s" % tiers[int(tier)] if tier else "")
    nids = _call("findNotes", query=q)
    notes = []
    for i in range(0, len(nids), 400):
        notes += _call("notesInfo", notes=nids[i:i + 400])
    out = []
    rx = re.compile(pattern, re.I) if pattern else None
    for n in notes:
        if any("one_home" in t or "merged" in t or "dupe-suspended" in t for t in n.get("tags", [])):
            continue
        fields = sorted(n["fields"].items(), key=lambda kv: kv[1]["order"])
        vals = [(k, plain(_CLOZE.sub(r"\1", v["value"])).strip()) for k, v in fields]
        title = next((v for k, v in vals if k.lower() in ("title", "work", "name", "answerline") and v),
                     vals[0][1] if vals else "")
        if not title or (rx and not rx.search(title)):
            continue
        ntext = " " + _note_fold(" ".join(v for _, v in vals)) + " "
        creators = [v for k, v in vals if k.lower().strip() in _CREATOR_FIELDS and v]
        have_clues = {k: v for k, v in vals if v and (k.startswith("Clue") or k in ("Notes", "Description"))}
        # Require an exact work title to avoid matches to unrelated works with similar titles.
        p = profile(title, cat=cat, top=top + (max(8, 3 * len(creators)) if creators else 0),
                    exact=bool(creators))
        stock = []
        suppressed = []
        for t in p.get("things", []):
            if t["kind"] in ("name", "title") and _creator_leak(t["thing"], creators):
                suppressed.append({"thing": t["thing"], "reason": "creator already shown on note"})
                continue
            on = (" %s " % t["key"]) in ntext
            stock.append({"thing": t["thing"], "kind": t["kind"], "n": t["n"], "tied": round(t["tied"], 2),
                          "where": t["where"], "power": t.get("power", 0), "on_note": on, "example": t.get("example", "")})
        stock = stock[:top]
        out.append({"nid": n["noteId"], "title": title, "model": n["modelName"],
                    "questions": p.get("questions", 0), "tossups": p.get("tossups", 0),
                    "answerlines": p.get("lines", []),
                    "have": have_clues, "stock": stock, "suppressed": suppressed,
                    "missing": [s["thing"] for s in stock if not s["on_note"] and s["n"] >= 2]})
    return out
