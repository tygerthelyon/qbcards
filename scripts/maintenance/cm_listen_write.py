# -*- coding: utf-8 -*-
"""cm_listen_write.py [--dry|--apply] -- fill the Listen field.

Matched on composer / work / nickname / movement fragment. The most specific rule
wins, scored by how many of the four parts it actually constrains, so a rule for
one movement beats the whole-work fallback.
"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import concept_add as C
from cm_listen_data import L


def main():
    dry = "--apply" not in sys.argv
    ns = C.anki("notesInfo",
                notes=C.anki("findNotes",
                             query='note:"Classical Music" tag:Music::tier::tier1-core'))
    hits, miss, out = 0, [], []
    for n in ns:
        f = n["fields"]
        if C.plain(f["Kind"]["value"]).strip():
            continue
        if not C.plain(f["Audio"]["value"]).strip():
            continue
        comp = C.fold(C.plain(f["Composer"]["value"]))
        work = C.fold(C.plain(f["Work"]["value"]))
        nick = C.fold(C.plain(f["Nickname"]["value"]))
        mv = C.fold(C.plain(f["Movement"]["value"]))
        best, bestspec = None, -1
        for c, w, nk, m, text in L:
            if c and c not in comp:
                continue
            if w and w not in work:
                continue
            if nk and nk not in nick:
                continue
            if m and m not in mv:
                continue
            spec = sum(1 for x in (c, w, nk, m) if x) * 10 + len(m) + len(w)
            if spec > bestspec:
                best, bestspec = text, spec
        label = "%s / %s%s%s" % (C.plain(f["Composer"]["value"])[:20],
                                 C.plain(f["Work"]["value"])[:28],
                                 " ~" + C.plain(f["Nickname"]["value"])[:12]
                                 if nick else "",
                                 " / " + C.plain(f["Movement"]["value"])[:22] if mv else "")
        if best:
            hits += 1
            out.append((n["noteId"], best, label))
        else:
            miss.append(label)

    print("tier1 pieces with audio : %d" % (hits + len(miss)))
    print("   matched a Listen line: %d" % hits)
    print("   no line yet          : %d" % len(miss))
    if miss:
        print("\nstill unwritten:")
        for m in sorted(miss):
            print("   %s" % m)
    print("\nsample of what will be written:")
    for _i, t, lab in out[:6]:
        print("   %s\n      %s" % (lab, t[:150]))

    if dry:
        json.dump([{"id": i, "listen": t, "label": l} for i, t, l in out],
                  open("_cm_listen.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("\n-- dry run -- plan in _cm_listen.json")
        return
    for nid, text, _l in out:
        C.anki("updateNoteFields", note={"id": nid, "fields": {"Listen": text}})
    print("\nwrote Listen on %d notes" % len(out))


if __name__ == "__main__":
    main()
