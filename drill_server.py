# -*- coding: utf-8 -*-
"""drill_server.py -- Local Buzz Drill server with multi-set support and real-time buzz logging.

Serves the drill/ folder next to this file on http://127.0.0.1:8788. Everything it plays and records, one file per set:

    drill/tossups.json                 the studied collection (qb_drill_build.py)
    data/drill/sets/<id>.json          packs, tossups + bonuses (built by scripts, or uploaded in the page)
    data/drill/buzzes/<id>.jsonl       one line per tossup heard
    data/drill/bonuses/<id>.jsonl      one line per bonus heard
    data/drill/sessions/<id>.json      whole sessions as the page saved them at the end
    data/drill/buzzpoints/<id>.json    real tournaments' buzzpoints for "Against the field" (buzzpoints_build.py, or
                                       uploaded in the page); raw/ holds what they were built from

A set or buzzpoints file marked "private" (not on QBReader or public anywhere) never leaves this machine: the page
doesn't sync its records to the cloud.

Writes that replace a file go through a temp file, and appends skip a record already logged (same session, question,
and time), so the page can resend after a dropped connection without double counting.
"""
import argparse
import json
import mimetypes
import os
import re
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
DRILL_DIR = os.path.join(HERE, "drill")
STORE_DIR = os.path.join(HERE, "data", "drill")
SETS_DIR = os.path.join(STORE_DIR, "sets")
BP_DIR = os.path.join(STORE_DIR, "buzzpoints")
PROFILE_JSON = os.path.join(STORE_DIR, "profile.json")   # who the player is in real games: {"realNames": [...]}
# Tossups marked "Add to Anki" in the page: the clues to work into the decks (a missed clue onto a card's back, or a
# new card) by the deck rules, report first. {"items": [{key, set, id, q, answer, buzz, words, result, ...}]}
ANKI_QUEUE_JSON = os.path.join(STORE_DIR, "anki_queue.json")
STUDIED_JSON = os.path.join(DRILL_DIR, "tossups.json")

PORT = 8788
LOCK = threading.Lock()
_ANKI_CACHE = None
_PACK_CACHE = {}   # set file -> (mtime, the set as served, Anki-annotated; when, time.time())
_BP_INDEX = {}   # file -> (mtime, summary)


def _slug(s):
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", (s or "").strip()).strip("_").lower()
    return s[:64] or "custom_pack"


def _set_paths(set_id):
    """(pack, tossup log, session file) for a set."""
    sid = _slug(set_id)
    return (
        STUDIED_JSON if sid == "studied" else os.path.join(SETS_DIR, sid + ".json"),
        os.path.join(STORE_DIR, "buzzes", sid + ".jsonl"),
        os.path.join(STORE_DIR, "sessions", sid + ".json"),
    )


def _bonus_log_path(set_id):
    return os.path.join(STORE_DIR, "bonuses", _slug(set_id) + ".jsonl")


def _write_atomic(path, text):
    """Write through a temp file so a crash mid-write cannot truncate what was there."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def _row_key(row):
    return (row.get("sessionId") or "", row.get("id"), row.get("ts"))


def _read_jsonl(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def _read_json_list(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def _append_jsonl(path, row):
    """Append one record; returns False if the log already has it (a resend)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with LOCK:
        if any(_row_key(old) == _row_key(row) for old in _read_jsonl(path)):
            return False
        row["recordedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return True


def _remove_jsonl(path, target):
    """Remove the most recent matching JSONL line when the user clicks Undo."""
    if not os.path.exists(path):
        return False
    want_sid = target.get("sessionId")
    want_id = target.get("id")
    want_ts = target.get("ts")
    with LOCK:
        with open(path, encoding="utf-8") as f:
            lines = [ln.rstrip("\r\n") for ln in f if ln.strip()]
        drop_idx = None
        for i in range(len(lines) - 1, -1, -1):
            try:
                obj = json.loads(lines[i])
            except Exception:
                continue
            if obj.get("sessionId") == want_sid and obj.get("id") == want_id:
                if want_ts is None or obj.get("ts") == want_ts:
                    drop_idx = i
                    break
        if drop_idx is None:
            return False
        lines.pop(drop_idx)
        _write_atomic(path, "\n".join(lines) + ("\n" if lines else ""))
        return True


def _append_buzz(set_id, row):
    _, buzz_path, _ = _set_paths(set_id)
    return _append_jsonl(buzz_path, row)


def _remove_buzz(set_id, target):
    _, buzz_path, _ = _set_paths(set_id)
    return _remove_jsonl(buzz_path, target)


def _upsert_session(set_id, sess):
    _, _, sess_path = _set_paths(set_id)
    os.makedirs(os.path.dirname(sess_path), exist_ok=True)
    with LOCK:
        sessions = _read_json_list(sess_path)
        sid = sess.get("id")
        for i, old in enumerate(sessions):
            if old.get("id") == sid:
                sessions[i] = sess
                break
        else:
            sessions.append(sess)
        _write_atomic(sess_path, json.dumps(sessions, ensure_ascii=False, indent=2))


def _anki_index():
    global _ANKI_CACHE
    if _ANKI_CACHE is not None:
        return _ANKI_CACHE
    try:
        from qbr import anki
        _ANKI_CACHE = anki.index()
    except Exception:
        _ANKI_CACHE = {}
    return _ANKI_CACHE


def _answer_anki_meta(ans_text, names, text_blob, _key, parse_answer):
    pa = parse_answer(ans_text or "")
    main = pa.get("main") or ""
    accepts = pa.get("accepts") or []
    status = ""
    for cand in [main] + list(accepts):
        k = _key(cand)
        if k and k in names:
            got = names[k][0]
            if got == "studied":                          # qbr.anki splits active cards by review; here both are "card"
                got = "card"
            if got == "card":
                status = "card"
                break
            if not status:
                status = got
    if not status and main:
        k = _key(main)
        if len(k) >= 3 and (" %s " % k) in text_blob:
            status = "text"
    return main, accepts, status


# Match within the decks that study the question's subject: any deck with a part of its path ("QB::Fine Arts::Music")
# named after the category or one of its usual subjects. A category no deck is named for uses the whole collection, so
# any deck layout works.
_CATEGORY_DECK_NAMES = {
    "fine arts": {"art", "arts", "visual fine arts", "auditory fine arts", "other fine arts", "music", "classical music",
                  "opera", "architecture", "film", "photography", "dance", "jazz", "painting", "sculpture", "art history",
                  "vfa", "afa", "ovfa", "oafa"},
    "literature": {"lit", "poetry", "poems", "novels", "drama", "fiction"},
    "science": {"biology", "chemistry", "physics", "math", "mathematics", "astronomy", "earth science",
                "computer science"},
    "history": {"world history", "american history", "us history", "european history", "ancient history"},
    "mythology": {"myth", "myths"},
    "social science": {"economics", "psychology", "linguistics", "sociology", "anthropology"},
    "pop culture": {"trash"},
}
_ANSWER_CATEGORY_INDEXES = {}        # Anki search -> (time, index), shared by every category that ends up searching it
_ANSWER_CATEGORY_LOCK = threading.Lock()


def _category_query(anki, category):
    want = _CATEGORY_DECK_NAMES.get(category, set()) | {category}
    decks = [d for d in anki._call("deckNames") if any(part.strip().casefold() in want for part in d.split("::"))]
    escape = lambda d: d.replace("\\", "\\\\").replace('"', '\\"').replace("*", "\\*").replace("_", "\\_")
    return " OR ".join('deck:"%s"' % escape(d) for d in decks) or "deck:*"


def _answer_category_index(category):
    category = (category or "").strip().casefold()
    with _ANSWER_CATEGORY_LOCK:
        try:
            from qbr import anki
            query = _category_query(anki, category)
            cached = _ANSWER_CATEGORY_INDEXES.get(query)
            if cached and time.monotonic() - cached[0] < 300:
                return cached[1]
            index = anki.build(query, persist=False)
        except Exception:
            return {}
        _ANSWER_CATEGORY_INDEXES[query] = (time.monotonic(), index)
        return index


def _annotate_anki(items, bonuses=()):
    from qbr.text import _key, parse_answer

    indexes = {}
    def match(answer, category):
        if category not in indexes:
            idx = _answer_category_index(category)
            indexes[category] = idx.get("names") or {}, " " + (idx.get("text") or "") + " "
        names, text_blob = indexes[category]
        return _answer_anki_meta(answer, names, text_blob, _key, parse_answer)

    for it in items:
        main, _, status = match(it.get("a") or "", it.get("g"))
        if main and not it.get("main"):
            it["main"] = main
        it["anki"] = status
    for bo in bonuses:
        bo["part_meta"] = [
            {"main": main, "accepts": accepts, "anki": status}
            for main, accepts, status in (
                match(answer, bo.get("g")) for answer in bo.get("answers") or []
            )
        ]
    return items, bonuses


_DECK_ENT_CACHE = {}
_MUSIC_KEY_RE = re.compile(r"^[a-g](?:\s+(?:flat|sharp|major|minor|natural))+$")
_GENERIC_CLUE_TOKENS = frozenset(
    """
    instrument instruments piece pieces work works movement movements composer composers
    painting paintings painter novel novels author writer poet poem poems opera operas
    symphony symphonies concerto concertos sonata sonatas prelude preludes ballade ballades
    chaconne etude etudes waltz nocturne mass requiem aria overture fantasia serenade
    quartet quintet trio duo caprice caprices variation variations suite obsession
    country countries city cities river rivers mountain mountains element elements
    compound compounds molecule molecules protein proteins disease planet star monarch
    emperor king queen president battle treaty century centuries character characters
    protagonist protagonists narrator title book story short play plays film movie
    sculptor sculpture building architect scientist physicist chemist biologist mathematician philosopher
    """.split()
)


def _find_notes_for_phrase(fe, by_name, deck_blob, exclude_k="", scope=None):
    """Locate up to 2 Anki note names containing folded phrase `fe` anywhere in the collection."""
    if not fe or (" " + fe + " ") not in deck_blob:
        return []
    key = (scope, fe)
    cached = _DECK_ENT_CACHE.get(key)
    if cached is None:
        hits = []
        needle = " " + fe + " "
        for nk, nv in by_name.items():
            if needle in (" " + nv + " "):
                hits.append(nk)
                if len(hits) >= 4:
                    break
        _DECK_ENT_CACHE[key] = hits
        cached = hits
    return [k for k in cached if k != exclude_k][:2]


def _clue_match(payload):
    """Compare each tossup sentence against Anki notes in the question?s category."""
    category = (payload.get("category") or "").strip().casefold()
    idx = _answer_category_index(category)
    names = idx.get("names") or {}
    by_name = idx.get("by_name") or {}
    if not names:
        return {"status": "", "sentences": []}
    try:
        from qbr.text import _STOP, _key, fold, parse_answer, sentences, things, where
    except Exception:
        return {"status": "", "sentences": []}

    q_text = payload.get("q") or ""
    a_text = payload.get("a") or ""
    pa = parse_answer(a_text)
    main = payload.get("main") or pa.get("main") or ""
    accepts = pa.get("accepts") or []
    cands = []
    for raw in [main] + list(accepts):
        k = _key(raw)
        if k and k not in cands:
            cands.append(k)

    best_k, status, model = "", "", ""
    for k in cands:
        if k in names:
            got, got_model = names[k][0], names[k][1]
            if got == "studied":                          # qbr.anki splits active cards by review; here both are "card"
                got = "card"
            if got == "card":
                best_k, status, model = k, got, got_model
                break
            if not status:
                best_k, status, model = k, got, got_model

    deck_blob = " " + (idx.get("text") or "") + " "
    if not best_k and main and len(_key(main)) >= 3 and (" %s " % _key(main)) in deck_blob:
        status = "text"

    note_text = by_name.get(best_k) or ""
    note_blob = " " + note_text + " "
    ans_words = set()
    for c in cands:
        ans_words.update(c.split())

    sent_out = []
    w_cursor = 0
    for st in sentences(q_text):
        s_str = st["s"]
        w_len = len(s_str.split())
        w_start, w_end = w_cursor, w_cursor + w_len
        w_cursor = w_end

        phrase_hits = []
        sentence_words = fold(s_str).split()
        # Require a contiguous passage carrying at least three content words.
        # Prefer longer excerpts and skip fragments already shown.
        if best_k:
            for width in range(min(10, len(sentence_words)), 3, -1):
                for start in range(len(sentence_words) - width + 1):
                    words = sentence_words[start:start + width]
                    content = set(words) - _STOP - _GENERIC_CLUE_TOKENS - ans_words
                    if sum(len(word) >= 3 for word in content) < 3:
                        continue
                    phrase = " ".join(words)
                    if " " + phrase + " " in note_blob and not any(phrase in hit for hit in phrase_hits):
                        phrase_hits.append(phrase)
                        if len(phrase_hits) == 4:
                            break
                if len(phrase_hits) == 4:
                    break

        deck_hits = []
        if not phrase_hits:
            for _, entity in things(s_str):
                phrase = fold(entity)
                words = set(phrase.split()) - _STOP - _GENERIC_CLUE_TOKENS - ans_words
                if len(phrase.split()) < 4 or sum(len(word) >= 3 for word in words) < 3:
                    continue
                other_notes = _find_notes_for_phrase(phrase, by_name, deck_blob, exclude_k=best_k, scope=(category, idx.get("built")))
                if other_notes:
                    deck_hits.append({"clue": entity, "notes": other_notes})
                    if len(deck_hits) == 4:
                        break

        sent_out.append({
            "i": st["i"],
            "stage": where(st["pos"], st["give"]),
            "power": st["power"],
            "give": st["give"],
            "w0": w_start,
            "w1": w_end,
            "s": s_str,
            "covered": bool(phrase_hits),
            "matches": phrase_hits,
            "deckHits": deck_hits,
        })

    return {
        "status": status,
        "noteType": model,
        "matchedName": best_k,
        "sentences": sent_out,
    }


def _set_clue_audit(payload):
    """Batch clue-level comparison across played tossups for Set Analysis."""
    records = payload.get("records") or []
    out = []
    for r in records[:600]:
        q_text = r.get("q") or ""
        if not q_text:
            continue
        cm = _clue_match({"q": q_text, "a": r.get("a") or "", "main": r.get("main") or "",
                          "category": r.get("category") or ""})
        sents = cm.get("sentences") or []
        buzz = r.get("buzz")
        heard_sents = [s for s in sents if buzz is None or s["w0"] <= buzz]
        if not heard_sents and sents:
            heard_sents = [sents[0]]

        heard_card = any(s["covered"] for s in heard_sents)
        heard_deck = any(bool(s.get("deckHits")) for s in heard_sents)
        heard_kind = "card" if heard_card else ("deck" if heard_deck else "none")

        buzz_kind = "none"
        buzz_clues = []
        if buzz is not None:
            bs = None
            for s in sents:
                if s["w0"] <= buzz <= s["w1"]:
                    bs = s
                    break
            if bs is None and heard_sents:
                bs = heard_sents[-1]
            if bs:
                if bs["covered"]:
                    buzz_kind = "card"
                    buzz_clues = list(bs["matches"])
                elif bs.get("deckHits"):
                    buzz_kind = "deck"
                    buzz_clues = [d["clue"] + " (" + ", ".join(d["notes"]) + ")" for d in bs["deckHits"]]

        heard_clues = []
        for s in heard_sents:
            for m in s.get("matches") or []:
                if m not in heard_clues:
                    heard_clues.append(m)
            for d in s.get("deckHits") or []:
                lbl = d["clue"] + " -> " + d["notes"][0]
                if lbl not in heard_clues:
                    heard_clues.append(lbl)

        out.append({
            "id": r.get("id"),
            "totalClues": len(sents),
            "coveredClues": sum(1 for s in sents if s["covered"] or s.get("deckHits")),
            "heardKind": heard_kind,
            "buzzKind": buzz_kind,
            "noteName": cm.get("matchedName") or "",
            "noteType": cm.get("noteType") or "",
            "onCardSents": sum(1 for s in heard_sents if s["covered"]),
            "heardSents": len(heard_sents),
            "clues": (buzz_clues or heard_clues)[:5],
        })
    return {"items": out}


def _load_set_bonuses(sid):
    set_path, _, _ = _set_paths(sid)
    if not os.path.isfile(set_path):
        return []
    try:
        d = json.load(open(set_path, encoding="utf-8"))
        return d.get("bonuses") or []
    except Exception:
        return []


def _list_sets():
    out = []
    if os.path.exists(STUDIED_JSON):
        try:
            d = json.load(open(STUDIED_JSON, encoding="utf-8"))
            out.append({
                "id": "studied",
                "name": "Studied collection",
                "count": len(d.get("items") or []),
                "bonusCount": 0,
                "url": "/tossups.json",
                "hasPackets": False,
                "built": d.get("built") or "",
            })
        except Exception:
            pass
    if os.path.isdir(SETS_DIR):
        for fn in sorted(os.listdir(SETS_DIR)):
            if not fn.endswith(".json"):
                continue
            sid = fn[:-5]
            try:
                d = json.load(open(os.path.join(SETS_DIR, fn), encoding="utf-8"))
                items = d.get("items") or []
                bonuses = d.get("bonuses") or []
                out.append({
                    "id": sid,
                    "name": d.get("set") or sid,
                    "count": len(items),
                    "bonusCount": len(bonuses),
                    "url": "/api/set?id=" + sid,
                    "hasPackets": any(it.get("p") for it in items + bonuses),
                    "custom": True,
                    "private": bool(d.get("private")),
                })
            except Exception:
                pass
    return out


def _built_by_script(sid):
    path = os.path.join(SETS_DIR, sid + ".json")
    if not os.path.isfile(path):
        return False
    try:
        return not json.load(open(path, encoding="utf-8")).get("uploaded")
    except Exception:
        return True


# A set as served: Anki-annotated, which takes seconds (one AnkiConnect check per answer). Each set's copy is kept in
# memory and on disk (data/drill/.cache), so switching sets and restarting the server don't redo it; a copy over 10
# minutes old is served as it is and rechecked in the background, as cards change. A changed set file starts over.
PACK_CACHE_DIR = os.path.join(STORE_DIR, ".cache")
_PACK_REFRESHING = set()


def _build_pack(set_path, mtime):
    with open(set_path, encoding="utf-8") as f:
        pack = json.load(f)
    _annotate_anki(pack.get("items") or [], pack.get("bonuses") or [])
    body = json.dumps(pack, ensure_ascii=False).encode("utf-8")
    _PACK_CACHE[set_path] = (mtime, body, time.time())
    try:
        os.makedirs(PACK_CACHE_DIR, exist_ok=True)
        stem = os.path.splitext(os.path.basename(set_path))[0]
        for old in os.listdir(PACK_CACHE_DIR):   # the set's earlier versions
            if old.startswith(stem + "@"):
                os.remove(os.path.join(PACK_CACHE_DIR, old))
        with open(os.path.join(PACK_CACHE_DIR, "%s@%d.json" % (stem, int(mtime))), "wb") as f:
            f.write(body)
    except OSError:
        pass
    return body


def _refresh_pack(set_path, mtime):
    try:
        _build_pack(set_path, mtime)
    finally:
        _PACK_REFRESHING.discard(set_path)


def _pack_body(set_path):
    mtime = os.path.getmtime(set_path)
    hit = _PACK_CACHE.get(set_path)
    if not (hit and hit[0] == mtime):
        disk = os.path.join(PACK_CACHE_DIR, "%s@%d.json" % (os.path.splitext(os.path.basename(set_path))[0], int(mtime)))
        if os.path.isfile(disk):
            with open(disk, "rb") as f:
                hit = (mtime, f.read(), os.path.getmtime(disk))
            _PACK_CACHE[set_path] = hit
        else:
            return _build_pack(set_path, mtime)
    if time.time() - hit[2] > 600 and set_path not in _PACK_REFRESHING:
        _PACK_REFRESHING.add(set_path)
        threading.Thread(target=_refresh_pack, args=(set_path, mtime), daemon=True).start()
    return hit[1]


def _list_buzzpoints():
    out = []
    if not os.path.isdir(BP_DIR):
        return out
    for fn in sorted(os.listdir(BP_DIR)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        path = os.path.join(BP_DIR, fn)
        mtime = os.path.getmtime(path)
        hit = _BP_INDEX.get(fn)
        if not hit or hit[0] != mtime:
            try:
                d = json.load(open(path, encoding="utf-8"))
            except Exception:
                continue
            if d.get("format") != "buzzdrill-buzzpoints":
                continue
            hit = (mtime, {"id": fn[:-5], "set": d.get("set") or fn[:-5], "private": bool(d.get("private")),
                           "sites": [s.get("name") for s in d.get("sites") or []], "built": d.get("built") or "",
                           "tossups": len(d.get("tossups") or []), "bonuses": len(d.get("bonuses") or []),
                           "url": "/api/buzzpoints?id=" + fn[:-5]})
            _BP_INDEX[fn] = hit
        out.append(hit[1])
    return out


class DrillHandler(BaseHTTPRequestHandler):
    server_version = "BuzzDrillServer"

    def log_message(self, _fmt, *_args):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        raw = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urlsplit(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        if path == "/api/health":
            return self._send(200, json.dumps({"app": "BuzzDrill", "ok": True, "version": 3}))
        if path == "/api/sets":
            return self._send(200, json.dumps({"sets": _list_sets()}, ensure_ascii=False))
        if path == "/api/set":
            sid = _slug((qs.get("id") or [""])[0])
            set_path, _, _ = _set_paths(sid)
            if not os.path.isfile(set_path):
                return self._send(404, json.dumps({"error": "Set not found"}))
            # checking every answer against Anki takes about a second, so keep the result until the file changes
            return self._send(200, _pack_body(set_path))
        if path == "/api/anki-queue":
            try:
                queue = json.load(open(ANKI_QUEUE_JSON, encoding="utf-8"))
            except Exception:
                queue = {"items": []}
            return self._send(200, json.dumps(queue, ensure_ascii=False))
        if path == "/api/profile":
            try:
                prof = json.load(open(PROFILE_JSON, encoding="utf-8"))
            except Exception:
                prof = {}
            return self._send(200, json.dumps(prof, ensure_ascii=False))
        if path == "/api/buzzpoints":
            bid = (qs.get("id") or [""])[0]
            if not bid:
                return self._send(200, json.dumps({"files": _list_buzzpoints()}, ensure_ascii=False))
            bp_path = os.path.join(BP_DIR, _slug(bid) + ".json")
            if not os.path.isfile(bp_path):
                return self._send(404, json.dumps({"error": "Buzzpoints file not found"}))
            with open(bp_path, "rb") as f:
                return self._send(200, f.read())
        if path == "/api/bonuses":
            sid = _slug((qs.get("set") or qs.get("id") or [""])[0])
            bonuses = _load_set_bonuses(sid)
            _annotate_anki([], bonuses)
            return self._send(200, json.dumps({"set": sid, "bonuses": bonuses}, ensure_ascii=False))
        if path == "/api/state":
            sid = (qs.get("set") or [""])[0]
            if not sid:
                return self._send(400, json.dumps({"error": "Missing set"}))
            _, buzz_path, sess_path = _set_paths(sid)
            bonus_path = _bonus_log_path(sid)
            with LOCK:
                payload = {
                    "set": _slug(sid),
                    "buzzes": _read_jsonl(buzz_path),
                    "bonuses": _read_jsonl(bonus_path),
                    "sessions": _read_json_list(sess_path),
                }
            return self._send(200, json.dumps(payload, ensure_ascii=False))

        rel = "buzz-drill.html" if path in ("", "/") else path.lstrip("/")
        safe = os.path.normpath(os.path.join(DRILL_DIR, rel))
        if not safe.startswith(os.path.abspath(DRILL_DIR) + os.sep) or not os.path.isfile(safe):
            return self._send(404, json.dumps({"error": "Not found"}))
        ctype, _ = mimetypes.guess_type(safe)
        if safe.endswith(".json"):
            ctype = "application/json; charset=utf-8"
        elif safe.endswith(".html"):
            ctype = "text/html; charset=utf-8"
        with open(safe, "rb") as f:
            return self._send(200, f.read(), ctype or "application/octet-stream")

    def do_POST(self):
        path = urlsplit(self.path).path
        length = int(self.headers.get("Content-Length") or "0")
        if length <= 0 or length > 25_000_000:
            return self._send(400, json.dumps({"error": "Invalid body size"}))
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return self._send(400, json.dumps({"error": "Invalid JSON"}))

        if not isinstance(data, dict):
            return self._send(400, json.dumps({"error": "Expected a JSON object"}))
        if path in ("/api/buzz", "/api/unbuzz", "/api/bonus", "/api/unbonus", "/api/session"):
            # a record with no set used to land in the first pack's log; now it is refused
            sid = data.get("setId")
            if not sid:
                return self._send(400, json.dumps({"error": "Missing setId"}))
            if path == "/api/buzz":
                return self._send(200, json.dumps({"ok": True, "added": _append_buzz(sid, data)}))
            if path == "/api/unbuzz":
                return self._send(200, json.dumps({"ok": True, "removed": _remove_buzz(sid, data)}))
            if path == "/api/bonus":
                return self._send(200, json.dumps({"ok": True, "added": _append_jsonl(_bonus_log_path(sid), data)}))
            if path == "/api/unbonus":
                return self._send(200, json.dumps({"ok": True, "removed": _remove_jsonl(_bonus_log_path(sid), data)}))
            _upsert_session(sid, data)
            return self._send(200, json.dumps({"ok": True}))
        if path == "/api/clue-match":
            return self._send(200, json.dumps(_clue_match(data), ensure_ascii=False))
        if path == "/api/set-clue-audit":
            return self._send(200, json.dumps(_set_clue_audit(data), ensure_ascii=False))
        if path == "/api/anki-queue":
            with LOCK:
                try:
                    queue = json.load(open(ANKI_QUEUE_JSON, encoding="utf-8"))
                except Exception:
                    queue = {"items": []}
                items = [x for x in queue.get("items") or [] if x.get("key") != (data.get("key") or (data.get("item") or {}).get("key"))]
                if data.get("op") == "add" and isinstance(data.get("item"), dict) and data["item"].get("key"):
                    items.append(data["item"])
                _write_atomic(ANKI_QUEUE_JSON, json.dumps({"items": items}, ensure_ascii=False, indent=1))
            return self._send(200, json.dumps({"ok": True, "count": len(items)}))
        if path == "/api/profile":
            names = [str(n).strip()[:80] for n in data.get("realNames") or [] if str(n).strip()][:20]
            with LOCK:
                _write_atomic(PROFILE_JSON, json.dumps({"realNames": names}, ensure_ascii=False, indent=2))
            return self._send(200, json.dumps({"ok": True, "realNames": names}, ensure_ascii=False))
        if path == "/api/buzzpoints":
            if data.get("format") != "buzzdrill-buzzpoints" or not isinstance(data.get("tossups"), list):
                return self._send(400, json.dumps({"error": "Not a Buzz Drill buzzpoints file"}))
            bid = _slug(data.get("id") or data.get("set") or "uploaded")
            os.makedirs(BP_DIR, exist_ok=True)
            with LOCK:
                _write_atomic(os.path.join(BP_DIR, bid + ".json"), json.dumps(data, ensure_ascii=False, separators=(",", ":")))
            return self._send(200, json.dumps({"ok": True, "id": bid, "url": "/api/buzzpoints?id=" + bid}))
        if path == "/api/sets":
            name = (data.get("name") or "Uploaded Pack").strip()[:120]
            items = data.get("items") or []
            bonuses = data.get("bonuses") or []
            if (not isinstance(items, list) or not items) and (not isinstance(bonuses, list) or not bonuses):
                return self._send(400, json.dumps({"error": "No tossups or bonuses in uploaded pack"}))
            sid = _slug(data.get("id") or name)
            if sid == "studied" or _built_by_script(sid):   # an upload never replaces a set a build script made
                sid = sid + "_custom"
            items, bonuses = _annotate_anki(items, bonuses)
            payload = {"built": time.strftime("%Y-%m-%d %H:%M"), "set": name, "items": items, "bonuses": bonuses,
                       "private": bool(data.get("private")), "uploaded": True}
            with LOCK:
                _write_atomic(os.path.join(SETS_DIR, sid + ".json"),
                              json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
            return self._send(200, json.dumps({"ok": True, "id": sid, "name": name, "count": len(items),
                                              "bonusCount": len(bonuses), "url": "/api/set?id=" + sid,
                                              "items": items, "bonuses": bonuses}, ensure_ascii=False))
        return self._send(404, json.dumps({"error": "Unknown endpoint"}))


def _already_running(port):
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/api/health" % port, timeout=1.5) as r:
            if r.status != 200:
                return False
            data = json.loads(r.read().decode("utf-8"))
            return data.get("app") == "BuzzDrill"
    except Exception:
        return False


def open_window(url):
    """Open Buzz Drill in a standalone app-style Chrome/Edge window when available."""
    if sys.platform == "win32":
        for base, relative in (("PROGRAMFILES", "Google/Chrome/Application/chrome.exe"),
                               ("PROGRAMFILES(X86)", "Microsoft/Edge/Application/msedge.exe")):
            executable = Path(os.environ.get(base, "")) / relative
            if executable.is_file():
                subprocess.Popen([str(executable), "--app=" + url, "--new-window", "--window-size=920,860"])
                return
    webbrowser.open(url)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--open", action="store_true")
    args = ap.parse_args(argv)

    url = "http://127.0.0.1:%d/" % args.port
    if _already_running(args.port):
        print("Buzz Drill server already running at", url, flush=True)
        if args.open:
            open_window(url)
        return 0

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), DrillHandler)
    # loading the Anki index takes ~25 s; start it now so the first pack opened doesn't wait for it
    threading.Thread(target=_anki_index, daemon=True).start()
    print("Serving Buzz Drill at", url, flush=True)
    if args.open:
        threading.Timer(0.3, lambda: open_window(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
