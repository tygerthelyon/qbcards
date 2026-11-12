# -*- coding: utf-8 -*-
"""qbr.store -- the local mirror: every qbreader question in one SQLite file with a full-text index.

    q    one row per question as qbreader has it (the formatted text is kept, compressed, in `body`)
    u    one row per answerable unit: a tossup, or one part of a bonus. This is what gets searched and counted.
         part is 0 for a tossup and 1-3 for a bonus part; a bonus's lead-in is stored on its part 1.
    f    the full-text index over u: text, lead, accepts
    u_top  an index holding every column a count needs (answer keys, categories, year, difficulty), so frequency
         lists read it and never touch the question text
    fv   f's vocabulary (how many units hold each word)
    sets one row per set, with when it was last fetched

sync() fetches set by set, so a new tournament costs one request and an interrupted run resumes where it stopped.
"""
import json
import os
import re
import sqlite3
import time
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from pathlib import Path

from . import api
from .text import SEP, parse_answer

PATH = os.environ.get("QBR_DB") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "qbreader.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS sets(name TEXT PRIMARY KEY, year INT, difficulty INT, standard INT, tossups INT, bonuses INT,
                                synced REAL);
CREATE TABLE IF NOT EXISTS q(qid INTEGER PRIMARY KEY, id TEXT UNIQUE, kind TEXT, set_name TEXT, year INT, difficulty INT,
                             packet INT, packet_name TEXT, number INT, category TEXT, subcategory TEXT, alt TEXT,
                             body BLOB, updated TEXT);
CREATE TABLE IF NOT EXISTS u(uid INTEGER PRIMARY KEY, qid INT, part INT, kind TEXT, text TEXT, lead TEXT, answer TEXT,
                             main TEXT, akey TEXT, rkey TEXT, accepts TEXT, set_name TEXT, year INT, difficulty INT,
                             category TEXT, subcategory TEXT, alt TEXT, mod TEXT);
CREATE INDEX IF NOT EXISTS q_set ON q(set_name);
CREATE INDEX IF NOT EXISTS u_qid ON u(qid);
DROP INDEX IF EXISTS u_akey;
CREATE INDEX IF NOT EXISTS u_top ON u(akey, rkey, main, kind, category, subcategory, alt, difficulty, year, set_name, qid);
CREATE INDEX IF NOT EXISTS u_rkey ON u(rkey);
CREATE INDEX IF NOT EXISTS u_set ON u(set_name);
CREATE VIRTUAL TABLE IF NOT EXISTS f USING fts5(text, lead, accepts, content='u', content_rowid='uid',
                                                tokenize="unicode61 remove_diacritics 2");
CREATE VIRTUAL TABLE IF NOT EXISTS fv USING fts5vocab(f, 'row');
"""


@lru_cache(maxsize=256)
def _rx(p):
    return re.compile(p, re.I)


def connect(write=False):
    """The mirror. Read-only unless write=True; raises FileNotFoundError before the first sync."""
    if not write and not os.path.exists(PATH):
        raise FileNotFoundError("no mirror yet at %s -- run: python -m qbr sync" % PATH)
    if write:
        os.makedirs(os.path.dirname(os.path.abspath(PATH)), exist_ok=True)
        con = sqlite3.connect(PATH, timeout=120)
        # Write-ahead logging, switched on once and left on: a search running in another session reads the last
        # committed state and never waits on a sync. The switch itself needs the file to itself, so it is retried,
        # and if something keeps the file open the write goes ahead in the old mode.
        for _ in range(20):
            if con.execute("PRAGMA journal_mode").fetchone()[0].lower() == "wal":
                break
            try:
                con.execute("PRAGMA journal_mode=WAL")
            except sqlite3.OperationalError:
                time.sleep(3)
        con.execute("PRAGMA synchronous=NORMAL")
        con.executescript(SCHEMA)
    else:
        con = sqlite3.connect(Path(PATH).resolve().as_uri() + "?mode=ro", uri=True, timeout=60)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA cache_size=-200000")
    con.create_function("regexp", 2, lambda p, s: 1 if s and _rx(p).search(s) else 0, deterministic=True)
    return con


_CON = None


def db():
    """one shared read-only connection for the process"""
    global _CON
    if _CON is None:
        _CON = connect()
    return _CON


def meta(k, default=None, con=None):
    r = (con or db()).execute("SELECT v FROM meta WHERE k=?", (k,)).fetchone()
    return json.loads(r[0]) if r else default


def body(con, qid):
    """a question's formatted text: {"q", "a"} for a tossup, {"l", "p", "a"} (lead-in, parts, answers) for a bonus"""
    r = con.execute("SELECT body FROM q WHERE qid=?", (qid,)).fetchone()
    return json.loads(zlib.decompress(r[0]).decode("utf-8")) if r and r[0] else {}


# Writing
def _fetch_set(name):
    return name, list(api.pages(setName=name))


def _drop_units(con, where, arg):
    """delete units and their index entries (the index needs the old text handed back to forget it)"""
    old = con.execute("SELECT uid, text, lead, accepts FROM u WHERE " + where, (arg,)).fetchall()
    con.executemany("INSERT INTO f(f, rowid, text, lead, accepts) VALUES('delete', ?, ?, ?, ?)", [tuple(r) for r in old])
    con.execute("DELETE FROM u WHERE " + where, (arg,))


def _drop_set(con, name):
    _drop_units(con, "set_name=?", name)
    con.execute("DELETE FROM q WHERE set_name=?", (name,))
    con.execute("DELETE FROM sets WHERE name=?", (name,))


def _put_set(con, name, rows):
    """replace one set's questions with the rows just fetched"""
    _drop_set(con, name)
    year = diff = std = None
    n = {"T": 0, "B": 0}
    for r in rows:
        s, p = r.get("set") or {}, r.get("packet") or {}
        if s.get("name") != name:
            continue
        kind = r["_kind"]
        n[kind] += 1
        year, std = s.get("year"), int(bool(s.get("standard")))
        diff = r.get("difficulty")
        if kind == "T":
            blob = {"q": r.get("question") or "", "a": r.get("answer") or ""}
        else:
            blob = {"l": r.get("leadin") or "", "p": r.get("parts") or [], "a": r.get("answers") or []}
        moved = con.execute("SELECT qid FROM q WHERE id=?", (r["_id"],)).fetchone()
        if moved:                                           # the question now sits in another set
            _drop_units(con, "qid=?", moved[0])
            con.execute("DELETE FROM q WHERE qid=?", (moved[0],))
        cur = con.execute(
            "INSERT INTO q(id, kind, set_name, year, difficulty, packet, packet_name, number, category, "
            "subcategory, alt, body, updated) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (r["_id"], kind, name, year, diff, p.get("number"), p.get("name"), r.get("number"), r.get("category"),
             r.get("subcategory"), r.get("alternate_subcategory"),
             zlib.compress(json.dumps(blob, ensure_ascii=False).encode("utf-8"), 6), r.get("updatedAt")))
        qid = cur.lastrowid
        if kind == "T":
            units = [(0, r.get("question_sanitized") or "", "", r.get("answer_sanitized") or "", blob["a"], None)]
        else:
            parts, answers = r.get("parts_sanitized") or [], r.get("answers_sanitized") or []
            mods = r.get("difficultyModifiers") or []
            units = [(i + 1, parts[i] or "", (r.get("leadin_sanitized") or "") if i == 0 else "", answers[i] or "",
                      blob["a"][i] if i < len(blob["a"]) else "", mods[i] if i < len(mods) else None)
                     for i in range(min(len(parts), len(answers)))]
        for part, text, lead, answer, ahtml, mod in units:
            a = parse_answer(answer, ahtml)
            acc = SEP.join(a["accepts"])
            c = con.execute(
                "INSERT INTO u(qid, part, kind, text, lead, answer, main, akey, rkey, accepts, set_name, year, difficulty,"
                " category, subcategory, alt, mod) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (qid, part, kind, text, lead, answer, a["main"], a["akey"], a["rkey"], acc, name, year, diff,
                 r.get("category"), r.get("subcategory"), r.get("alternate_subcategory"), mod))
            con.execute("INSERT INTO f(rowid, text, lead, accepts) VALUES(?,?,?,?)", (c.lastrowid, text, lead, acc))
    con.execute("INSERT OR REPLACE INTO sets VALUES(?,?,?,?,?,?,?)", (name, year, diff, std, n["T"], n["B"], time.time()))
    return n


def _settle(con):
    """fold the write-ahead log back into the main file, so the next reader is not reading through it"""
    try:
        con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    except sqlite3.OperationalError:
        pass                                    # someone is mid-read; the next write will settle it


def _finish(con, changed, log):
    facets = {}
    for col in ("category", "subcategory", "alt"):
        facets[col] = [r[0] for r in con.execute("SELECT DISTINCT %s FROM u WHERE %s IS NOT NULL ORDER BY 1" % (col, col))]
    t, b = (con.execute("SELECT count(*) FROM q WHERE kind=?", (k,)).fetchone()[0] for k in "TB")
    put = lambda k, v: con.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (k, json.dumps(v)))
    put("facets", facets)
    put("synced", time.time())
    put("counts", {"tossups": t, "bonuses": b})
    con.commit()
    if changed > 50:
        log("optimising the index ...")
        con.execute("INSERT INTO f(f) VALUES('optimize')")
        con.commit()
    _settle(con)
    try:
        at, ab = api.counts()
        log("mirror: %d tossups, %d bonuses, %d sets  |  qbreader now: %d tossups, %d bonuses%s" % (
            t, b, con.execute("SELECT count(*) FROM sets").fetchone()[0], at, ab,
            "" if (t, b) == (at, ab) else "   <- differs; `sync --full` re-fetches everything"))
    except Exception as e:                      # the check is a courtesy; the mirror is already written
        log("mirror: %d tossups, %d bonuses (count check skipped: %s)" % (t, b, e))


def reparse(log=print):
    """Re-derive every unit's answer columns (main, akey, rkey, accepts) from its stored answer line and rebuild the
    index. Run after a change to text.parse_answer; nothing is fetched."""
    global _CON
    _CON = None
    con = connect(write=True)
    t0, changed = time.time(), 0
    top = con.execute("SELECT max(uid) FROM u").fetchone()[0] or 0
    for lo in range(0, top + 1, 20000):
        new = []
        for r in con.execute("SELECT u.uid, u.part, u.kind, u.answer, u.main, u.akey, u.rkey, u.accepts, q.body FROM u "
                             "JOIN q ON q.qid=u.qid WHERE u.uid>? AND u.uid<=?", (lo, lo + 20000)).fetchall():
            b = json.loads(zlib.decompress(r["body"]).decode("utf-8")) if r["body"] else {}
            ahtml = b.get("a", "") if r["kind"] == "T" else (b.get("a") or [""] * 3)[r["part"] - 1:r["part"]]
            a = parse_answer(r["answer"], ahtml if isinstance(ahtml, str) else (ahtml[0] if ahtml else ""))
            acc = SEP.join(a["accepts"])
            if (a["main"], a["akey"], a["rkey"], acc) != (r["main"], r["akey"], r["rkey"], r["accepts"]):
                new.append((a["main"], a["akey"], a["rkey"], acc, r["uid"]))
        con.executemany("UPDATE u SET main=?, akey=?, rkey=?, accepts=? WHERE uid=?", new)
        changed += len(new)
    con.commit()
    log("%d answer lines changed, %.0fs; rebuilding the index ..." % (changed, time.time() - t0))
    con.execute("INSERT INTO f(f) VALUES('rebuild')")
    con.commit()
    _settle(con)
    con.close()
    log("done, %.0fs" % (time.time() - t0))
    return changed


def sync(full=False, years=1, workers=4, only=None, log=print):
    """Bring the mirror up to date. Fetches sets it does not have, drops sets qbreader no longer lists, and re-fetches
    any set from the last `years` years whose question count has changed. full=True re-fetches everything; only=[names]
    just those sets. Returns the number of sets fetched."""
    global _CON
    _CON = None
    con = connect(write=True)
    names = api.set_list()
    have = {r["name"]: r for r in con.execute("SELECT * FROM sets")}
    gone = [n for n in have if n not in names]
    todo = list(only) if only else [n for n in names if full or n not in have]
    with ThreadPoolExecutor(workers) as pool:
        if not full and not only:
            floor = time.gmtime().tm_year - years
            recent = [n for n in names if n in have and (have[n]["year"] or 0) >= floor]
            for n, c in zip(recent, pool.map(lambda n: api.counts(setName=n), recent)):
                if c != (have[n]["tossups"], have[n]["bonuses"]):
                    todo.append(n)
        for n in gone:
            _drop_set(con, n)
            log("dropped (no longer on qbreader): %s" % n)
        log("%d sets on qbreader, %d in the mirror, %d to fetch" % (len(names), len(have) - len(gone), len(todo)))
        t0, done, tot = time.time(), 0, {"T": 0, "B": 0}
        for fut in as_completed([pool.submit(_fetch_set, n) for n in todo]):
            try:
                name, rows = fut.result()
            except Exception as e:
                log("   FAILED a set (%s); run sync again to retry it" % e)
                continue
            n = _put_set(con, name, rows)
            tot["T"] += n["T"]
            tot["B"] += n["B"]
            done += 1
            if done % 20 == 0 or done == len(todo):
                con.commit()
                log("   %d/%d sets, %d tossups, %d bonuses, %.0fs" % (done, len(todo), tot["T"], tot["B"], time.time() - t0))
    _finish(con, done + len(gone), log)
    con.close()
    return done
