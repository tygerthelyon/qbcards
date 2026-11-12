# -*- coding: utf-8 -*-
"""qbr.anki -- what the Anki collection already holds, so a search can mark it. Read-only: this never writes to Anki.

    idx = index()
    have(idx, "black square")   -> "card"       a note is named this and has a card that is not suspended
                                   "suspended"  a note is named this, every card suspended
                                   "text"       no note is named this, but a note's text holds it
                                   ""           nowhere in the collection

A note's name is its first field when that is short (a title or a term, not a cloze sentence), plus anything in a
field called Alternate. Reading goes through AnkiConnect, so Anki must be open; the result is cached in
qbr/data/anki_index.json for twelve hours, and a stale cache is used (and said to be stale) when Anki is closed.
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


def build():
    """read every note from Anki and write the cache"""
    nids = _call("findNotes", query="deck:*")
    live = set(_call("findNotes", query="-is:suspended"))
    names, by_name, texts = {}, {}, []
    for i in range(0, len(nids), 500):
        for n in _call("notesInfo", notes=nids[i:i + 500]):
            fields = sorted(n["fields"].items(), key=lambda kv: kv[1]["order"])
            vals = [(k, plain(_CLOZE.sub(r"\1", v["value"]))) for k, v in fields]
            status = "card" if n["noteId"] in live else "suspended"
            own = [vals[0][1]] if vals and len(vals[0][1].split()) <= 8 else []
            for k, v in vals:
                if k.lower().strip() in _NAME_FIELDS and v and len(v.split()) <= 10:
                    own.append(v)
                if k.lower() in _ALT and v:
                    own += re.split(r"\s*(?:;|/|,|\bor\b)\s*", v)
            own = list(dict.fromkeys(x for x in own if x))
            ntext = _note_fold(" ".join(v for _, v in vals))
            for x in own:
                k = _key(x)
                if len(k) > 1:
                    if names.get(k, ("", ""))[0] != "card":
                        names[k] = (status, n["modelName"])
                    by_name[k] = (by_name.get(k, "") + " " + ntext).strip()
            texts.append(ntext)
    idx = {"built": time.time(), "notes": len(nids), "names": names, "by_name": by_name, "text": " | ".join(texts)}
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
        if not refresh and "by_name" in old and time.time() - old["built"] < max_age_h * 3600:
            return old
    try:
        return build()
    except Exception as e:
        if old:
            old["stale"] = "Anki not reachable (%s); using the index from %s" % (
                type(e).__name__, time.strftime("%Y-%m-%d %H:%M", time.localtime(old["built"])))
            return old
        raise RuntimeError("Anki is not reachable through AnkiConnect (localhost:8765) and there is no saved index. "
                           "Open Anki and run this again.") from e


_RANK = {"card": 4, "suspended": 3, "on-note": 2, "text": 1, "": 0}


def have(idx, key, also=(), target_names=()):
    """Is this folded name in the collection, and how?
        "card"       a note is named this and has an active card
        "suspended"  a note is named this, all cards suspended
        "on-note"    appears in the text of the target answer's own Anki note(s) (`target_names`)
        "text"       appears only in some other note's text across the collection
        ""           nowhere in the collection
    """
    best = ""
    by_name = idx.get("by_name") or {}
    own_blob = " " + " ".join(by_name.get(_key(n), "") for n in target_names if _key(n) in by_name) + " "
    for k in [_key(key)] + [_key(a) for a in also]:
        if not k:
            continue
        if k in idx["names"]:
            got = idx["names"][k][0]
        elif (" %s " % k) in own_blob:
            got = "on-note"
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
        # Work notes expose their composer/creator as part of the answer side. Require
        # an exact work answerline so an unrelated answer that merely accepts the title
        # as an alternate cannot flood the profile (e.g. Gluck's Orfeo ed Euridice for
        # Jacopo Peri's Euridice).
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
