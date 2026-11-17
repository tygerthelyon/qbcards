#!/usr/bin/env python3
"""
export_friend_apkg.py — Export Anki decks for sharing with their study order, suspensions, and deck presets, and
with all personal review history stripped.

Why this exists:
  Exporting without scheduling loses suspensions and presets; exporting with scheduling keeps the exporter's review
  history and intervals. This exports with scheduling, then cleans the copy. The live collection is never changed.

What it does:
  1. Exports the deck with `includeSched=True` via AnkiConnect.
  2. In the package's `collection.anki21`:
     - Orders cards: studied (not new) active cards first, in the order of their first review; then active new cards
       in their New-queue `due` order (a card reset to new counts as new); then suspended cards.
     - Gives them positions `due = 1, 2, ..., N`, sets `col.conf.nextPos = N + 1`, and makes every card new.
     - Clears `revlog`, `graves`, intervals, reps, lapses, ease, FSRS `data`, deck day counters, and `usn` flags.
     - Replaces the Default options the exporter assigns with each deck's live preset (learning steps, limits,
       new-card order, FSRS settings), read through AnkiConnect.
  3. Writes `<out_dir>/<deck>_friend.apkg` and checks it. `split_friend_apkg.py` cuts large ones for release.

Import with "Import any learning progress" and "Import deck presets" ticked to keep the order, suspensions, and
presets; every card arrives as new.

Usage:
  py -3.9 export_friend_apkg.py VFA AFA [--out-dir <folder>]
"""

import argparse
import json
import os
import sqlite3
import tempfile
import time
import urllib.request
import zipfile

ANKI_URL = "http://127.0.0.1:8765"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anki_exports")


def rpc(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(ANKI_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        res = json.loads(r.read().decode("utf-8"))
    if res.get("error"):
        raise RuntimeError(res["error"])
    return res["result"]


def sanitize_collection_db(db_path):
    """Strip personal review history while encoding release+insertion order into `due`."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    first_rev = dict(cur.execute("SELECT cid, MIN(id) FROM revlog GROUP BY cid").fetchall())
    rev_count_before = cur.execute("SELECT COUNT(*) FROM revlog").fetchone()[0]

    # id, nid, did, ord, type, queue, due, flags
    rows = cur.execute(
        "SELECT id, nid, did, ord, type, queue, due, flags FROM cards"
    ).fetchall()

    def sort_key(row):
        cid, nid, _did, ord_, ctype, queue, due, _flags = row
        # A card reset to new (forgetCards after its answer changed) still has old revlog rows; it is new now and
        # keeps its New-queue place, so classify by the card's current type, not by its history.
        if queue == -1:
            bucket = 2
            sub_bucket = 0 if ctype != 0 else 1
            pos = first_rev.get(cid, due) if ctype != 0 else due
            return (bucket, sub_bucket, pos, due, nid, ord_, cid)
        if ctype != 0:
            # Previously studied / released active card (including queue 1/2/3 learning/review):
            # place first in chronological release order.
            bucket = 0
            pos = first_rev.get(cid, due)
            return (bucket, 0, pos, due, nid, ord_, cid)
        # Unstudied active New card: preserve exact New-queue `due` position.
        bucket = 1
        return (bucket, 0, due, nid, ord_, cid)

    ordered = sorted(rows, key=sort_key)
    now_sec = int(time.time())

    updates = []
    active_count = 0
    suspended_count = 0
    studied_active_count = 0
    new_active_count = 0
    for idx, row in enumerate(ordered, start=1):
        cid, _nid, _did, _ord, ctype, queue, _due, flags = row
        is_susp = (queue == -1)
        new_queue = -1 if is_susp else 0
        if is_susp:
            suspended_count += 1
        else:
            active_count += 1
            if ctype != 0:
                studied_active_count += 1
            else:
                new_active_count += 1
        # Reset card strictly to unstudied state (type=0, ivl=0, factor=0, reps=0, lapses=0, data='')
        updates.append((now_sec, 0, 0, new_queue, idx, 0, 0, 0, 0, 0, 0, 0, flags, "", cid))

    cur.executemany(
        """
        UPDATE cards
           SET mod=?, usn=?, type=?, queue=?, due=?,
               ivl=?, factor=?, reps=?, lapses=?, left=?,
               odue=?, odid=?, flags=?, data=?
         WHERE id=?
        """,
        updates,
    )

    cur.execute("DELETE FROM revlog")
    cur.execute("DELETE FROM graves")
    cur.execute("UPDATE notes SET usn = 0")

    conf_raw, dconf_raw, decks_raw = cur.execute("SELECT conf, dconf, decks FROM col").fetchone()
    conf = json.loads(conf_raw)
    conf["nextPos"] = len(ordered) + 1

    dconf = json.loads(dconf_raw)
    decks = json.loads(decks_raw)
    # The package exporter files every deck under the Default options; carry each deck's own preset instead
    # (learning steps, daily limits, new-card gather/sort order, FSRS settings), read live from Anki.
    for dk in decks.values():
        if isinstance(dk, dict) and not dk.get("dyn") and dk.get("name") != "Default":
            cfg = dict(rpc("getDeckConfig", deck=dk["name"]), usn=0)
            dconf[str(cfg["id"])] = cfg
            dk["conf"] = cfg["id"]
    for cfg in dconf.values():
        if isinstance(cfg, dict) and isinstance(cfg.get("new"), dict):
            cfg["new"]["order"] = 1  # Sequential (due ascending)

    for dk in decks.values():
        if isinstance(dk, dict):
            dk["usn"] = 0
            for k in ("lrnToday", "revToday", "newToday", "timeToday"):
                if k in dk:
                    dk[k] = [0, 0]

    cur.execute(
        "UPDATE col SET mod = ?, usn = 0, conf = ?, dconf = ?, decks = ?",
        (now_sec * 1000, json.dumps(conf), json.dumps(dconf), json.dumps(decks)),
    )
    con.commit()
    con.execute("VACUUM")
    con.close()

    return {
        "cards": len(ordered),
        "active": active_count,
        "studied_active": studied_active_count,
        "new_active": new_active_count,
        "suspended": suspended_count,
        "revlog_stripped": rev_count_before,
        "next_pos": len(ordered) + 1,
    }


def verify_output_apkg(apkg_path, expected_cards, expected_active, expected_suspended):
    with zipfile.ZipFile(apkg_path, "r") as z:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            tf.write(z.read("collection.anki21"))
            tmp_db = tf.name
    try:
        con = sqlite3.connect(tmp_db)
        n_cards = con.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
        n_rev = con.execute("SELECT COUNT(*) FROM revlog").fetchone()[0]
        types = con.execute("SELECT DISTINCT type FROM cards").fetchall()
        queues = con.execute("SELECT queue, COUNT(*) FROM cards GROUP BY queue ORDER BY queue").fetchall()
        min_due, max_due, n_distinct_due = con.execute(
            "SELECT MIN(due), MAX(due), COUNT(DISTINCT due) FROM cards"
        ).fetchone()
        nonempty_data = con.execute("SELECT COUNT(*) FROM cards WHERE data != ''").fetchone()[0]
        con.close()
    finally:
        os.remove(tmp_db)

    assert n_cards == expected_cards, f"card count mismatch: {n_cards} != {expected_cards}"
    assert n_rev == 0, f"revlog not empty: {n_rev}"
    assert types == [(0,)], f"unexpected card types: {types}"
    assert min_due == 1 and max_due == expected_cards and n_distinct_due == expected_cards, (
        f"due range invalid: {min_due}..{max_due} ({n_distinct_due})"
    )
    assert nonempty_data == 0, f"nonempty card FSRS data: {nonempty_data}"
    qmap = dict(queues)
    assert qmap.get(0, 0) == expected_active, f"active mismatch: {qmap}"
    assert qmap.get(-1, 0) == expected_suspended, f"suspended mismatch: {qmap}"


def export_deck(deck_name, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in deck_name)
    raw_path = os.path.join(out_dir, f"_raw_{safe_name}.apkg")
    out_path = os.path.join(out_dir, f"{safe_name}_friend.apkg")

    if os.path.exists(raw_path):
        os.remove(raw_path)

    print(f"[{deck_name}] Exporting raw package via AnkiConnect...")
    ok = rpc("exportPackage", deck=deck_name, path=raw_path, includeSched=True)
    if not ok:
        raise RuntimeError(f"exportPackage failed for {deck_name}")

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        tmp_db = tf.name

    try:
        with zipfile.ZipFile(raw_path, "r") as zin:
            with open(tmp_db, "wb") as f:
                f.write(zin.read("collection.anki21"))

            stats = sanitize_collection_db(tmp_db)
            with open(tmp_db, "rb") as f:
                clean_db_bytes = f.read()

            with zipfile.ZipFile(out_path, "w") as zout:
                for info in zin.infolist():
                    if info.filename == "collection.anki21":
                        zi = zipfile.ZipInfo("collection.anki21", date_time=info.date_time)
                        zi.compress_type = info.compress_type
                        zout.writestr(zi, clean_db_bytes)
                    else:
                        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                        zi.compress_type = info.compress_type
                        zout.writestr(zi, zin.read(info.filename))
    finally:
        if os.path.exists(tmp_db):
            os.remove(tmp_db)
        if os.path.exists(raw_path):
            os.remove(raw_path)

    verify_output_apkg(out_path, stats["cards"], stats["active"], stats["suspended"])
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"[{deck_name}] Wrote {out_path} ({size_mb:.1f} MB): {stats}")
    return out_path, stats


def main():
    ap = argparse.ArgumentParser(description="Export order-preserved clean .apkg files for sharing.")
    ap.add_argument("decks", nargs="+", help="Deck names (e.g. VFA AFA)")
    ap.add_argument("--out-dir", default=OUT_DIR, help="Output directory")
    args = ap.parse_args()

    for d in args.decks:
        export_deck(d, os.path.abspath(args.out_dir))      # Anki writes the file, so it needs a full path


if __name__ == "__main__":
    main()
