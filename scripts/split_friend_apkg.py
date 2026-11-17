#!/usr/bin/env python3
"""split_friend_apkg.py -- cut a *_friend.apkg (export_friend_apkg.py) into importable parts under GitHub's 2 GB limit.

Each part is a whole .apkg: some of the notes with all their cards, only the media those notes use (plus the
underscore files templates load), and every deck and preset. Notes go in deck order, so subdecks stay together.
Cards keep the global `due` positions the export gave them, so importing every part rebuilds the exact order.

Usage:
  py -3.9 split_friend_apkg.py anki_exports/VFA_friend.apkg VFA   ->  VFA-1.apkg, VFA-2.apkg, ...
  (a deck that already fits is written whole as VFA.apkg)
"""
import argparse
import html
import json
import math
import os
import re
import shutil
import sqlite3
import tempfile
import zipfile
from urllib.parse import unquote

LIMIT = 1.45e9          # bytes of media per part, well under GitHub's 2 GB per release file
# a quoted name runs to its own closing quote: "Le_Violon_d'Ingres.png" holds an apostrophe
_REF = re.compile(r"""src\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s"'>]+))|\[sound:([^\]]+)\]|url\(\s*(?:"([^"]+)"|'([^']+)'|([^"')\s]+))""", re.I)


def _refs(flds, known):
    out = set()
    for m in _REF.finditer(flds):
        raw = next(g for g in m.groups() if g).strip()
        for name in (raw, html.unescape(raw), unquote(html.unescape(raw))):
            if name in known:
                out.add(name)
                break
    return out


def split(apkg, stem, out_dir, limit=LIMIT):
    z = zipfile.ZipFile(apkg)
    media = json.loads(z.read("media"))                       # {"0": "file.jpg", ...}
    size = {name: z.getinfo(key).file_size for key, name in media.items()}
    key_of = {name: key for key, name in media.items()}
    tmp = tempfile.mkdtemp()
    src_db = os.path.join(tmp, "src.db")
    with open(src_db, "wb") as f:
        f.write(z.read("collection.anki21"))
    con = sqlite3.connect(src_db)
    decks = {int(k): v["name"] for k, v in json.loads(con.execute("SELECT decks FROM col").fetchone()[0]).items()}
    first = {}
    for nid, did, due in con.execute("SELECT nid, did, due FROM cards ORDER BY ord"):
        first.setdefault(nid, (decks.get(did, ""), due))
    notes = [(nid, _refs(flds, size)) for nid, flds in con.execute("SELECT id, flds FROM notes")]
    con.close()
    always = {n for n in size if n.startswith("_")}
    notes.sort(key=lambda nr: first.get(nr[0], ("", 0)))
    used = set().union(*(r for _, r in notes)) | always
    total = sum(size[n] for n in used)
    parts_n = max(1, math.ceil(total / limit))
    # cut in deck order at equal shares of media
    parts, cur, acc, target = [], [], 0, total / parts_n
    for nid, refs in notes:
        cur.append((nid, refs))
        acc += sum(size[n] for n in refs)
        if acc >= target * (len(parts) + 1) and len(parts) < parts_n - 1:
            parts.append(cur)
            cur = []
    parts.append(cur)

    written = []
    for i, part in enumerate(parts, start=1):
        name = "%s.apkg" % stem if len(parts) == 1 else "%s-%d.apkg" % (stem, i)
        out = os.path.join(out_dir, name)
        db = os.path.join(tmp, "part%d.db" % i)
        shutil.copyfile(src_db, db)
        c = sqlite3.connect(db)
        c.execute("CREATE TEMP TABLE keep(id INTEGER PRIMARY KEY)")
        c.executemany("INSERT INTO keep VALUES (?)", [(nid,) for nid, _ in part])
        c.execute("DELETE FROM cards WHERE nid NOT IN (SELECT id FROM keep)")
        c.execute("DELETE FROM notes WHERE id NOT IN (SELECT id FROM keep)")
        c.commit()
        c.execute("VACUUM")
        c.close()
        files = sorted(set().union(*(r for _, r in part)) | always) if part else sorted(always)
        with zipfile.ZipFile(out, "w") as zo:
            for meta_name in ("meta", "collection.anki2"):
                if meta_name in z.namelist():
                    info = z.getinfo(meta_name)                # a fresh entry: writing must not touch the reader's
                    zi = zipfile.ZipInfo(meta_name, date_time=info.date_time)
                    zi.compress_type = info.compress_type
                    zo.writestr(zi, z.read(meta_name))
            zo.write(db, "collection.anki21", compress_type=zipfile.ZIP_DEFLATED)
            new_map = {}
            for j, fname in enumerate(files):
                info = z.getinfo(key_of[fname])
                zi = zipfile.ZipInfo(str(j), date_time=info.date_time)
                zi.compress_type = info.compress_type
                zo.writestr(zi, z.read(info))
                new_map[str(j)] = fname
            zo.writestr("media", json.dumps(new_map))
        written.append(out)
    shutil.rmtree(tmp, ignore_errors=True)
    return written, total, len(notes)


def verify(paths, src_apkg):
    """every note and card of the source in exactly one part; every media a part's notes use is in that part"""
    def load(p):
        z = zipfile.ZipFile(p)
        t = tempfile.mktemp(suffix=".db")
        open(t, "wb").write(z.read("collection.anki21"))
        c = sqlite3.connect(t)
        notes = dict(c.execute("SELECT id, flds FROM notes"))
        cards = dict(c.execute("SELECT id, due FROM cards"))
        susp = {r[0] for r in c.execute("SELECT id FROM cards WHERE queue=-1")}
        c.close()
        os.remove(t)
        return notes, cards, susp, set(json.loads(z.read("media")).values())
    s_notes, s_cards, s_susp, s_media = load(src_apkg)
    seen_n, seen_c, seen_s = set(), {}, set()
    for p in paths:
        notes, cards, susp, media = load(p)
        assert not (seen_n & set(notes)), "a note is in two parts"
        seen_n |= set(notes)
        seen_c.update(cards)
        seen_s |= susp
        missing = set().union(*(_refs(f, s_media) for f in notes.values())) - media if notes else set()
        assert not missing, "%s lacks %d media files" % (p, len(missing))
        # independent of the pattern above: any media name written anywhere in this part's notes must be here
        text = "\n".join(notes.values())
        named = {m for m in s_media - media if m in text and re.search(
            r"""(?:^|[\s"'=:/>\x1f])""" + re.escape(m) + r"""(?:$|[\s"'\]<\x1f])""", text)}   # whole name, not 3.jpg in x3.jpg
        assert not named, "%s lacks %d media files named in its notes, e.g. %s" % (p, len(named), sorted(named)[:3])
        assert os.path.getsize(p) < 1.95e9, "%s is too big for a release file" % p
    assert seen_n == set(s_notes) and seen_c == s_cards and seen_s == s_susp, "parts do not add up to the source"
    return len(seen_n), len(seen_c), len(seen_s)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("apkg")
    ap.add_argument("stem", help="release file name stem, e.g. VFA")
    ap.add_argument("--out-dir", default=None)
    a = ap.parse_args()
    out_dir = a.out_dir or os.path.dirname(os.path.abspath(a.apkg))
    paths, total, n = split(a.apkg, a.stem, out_dir)
    notes, cards, susp = verify(paths, a.apkg)
    for p in paths:
        print("%-14s %7.1f MB" % (os.path.basename(p), os.path.getsize(p) / 1e6))
    print("%s: %d notes, %d cards (%d suspended), %.0f MB of media, in %d part(s); verified" % (
        a.stem, notes, cards, susp, total / 1e6, len(paths)))


if __name__ == "__main__":
    main()
