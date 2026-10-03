# -*- coding: utf-8 -*-
"""cleanup_1001.py -- the small cleanups from the 2026-09-29 "what else" list (item 6).

Carter, 2026-10-01: "do ... 6".
  * Era notation: every deck writes BCE/CE; four strays wrote "BC" or "B.C.E." (Satyr Pouring Wine, Kritios
    Boy, Borghese Gladiator, the Corinthian order's Lysicrates caption). "A.D. 1639" and "A.D. 1753" on the
    Crabtree card stay: they are part of Ford Madox Brown's titles.
  * Pithoprakta stays tier 1, on checking: the work itself is the answer once (9 mentions), but it is the
    deck's only Xenakis card and Xenakis answers 17 questions, so it is how he is studied.

    py -3.9 cleanup_1001.py [--apply]
"""
import json, re, sys, time
import concept_add as C

FIX = {
    1787890521346: ("Date", "c. 370s B.C.E.", "c. 370s BCE"),
    1787890521361: ("Notes", "480 BC.", "480 BCE."),
    1787890521363: ("Notes", "100 BC.", "100 BCE."),
    1788585239103: ("Caption 3", "(330s B.C.E.)", "(330s BCE)"),
}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(FIX))}
    ch = {}
    for nid, (f, old, new) in FIX.items():
        v = ns[nid]["fields"][f]["value"]
        assert old in v, (nid, f, v[:120])
        ch[nid] = {f: v.replace(old, new)}
        print(nid, f, ":", old, "->", new)
    if "--apply" in sys.argv:
        json.dump({str(n): {"fields": {f: ns[n]["fields"][f]["value"] for f in d}} for n, d in ch.items()},
                  open("backups/cleanup_1001_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for nid, d in ch.items():
            C.anki("updateNoteFields", note={"id": nid, "fields": d})
        print("applied")
