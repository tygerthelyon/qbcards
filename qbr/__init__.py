# -*- coding: utf-8 -*-
"""qbr -- a local mirror of qbreader with a searcher on top.

    python -m qbr profile "Kazimir Malevich"  (run from the repository root)

From a script in this folder:

    import qbr
    qbr.profile("Kazimir Malevich")["things"]       # the stock clues, counted
    qbr.search("zero of form", cat="vfa", diff="7-9")
    qbr.who("zero of form")                         # which answers a clue points to
    qbr.top(cat="architecture", n=100)              # the frequency list
    qbr.rows(cat="Philosophy", kind="tossup")       # a pool, instead of a _qb_pool_*.json dump
    qbr.fact("Bury St. Edmunds", "eel")

README.md has the rest.
"""
from .anki import brief_notes
from .clues import profile, verify_clue
from .find import answered, fact, like, packet, rows, search, sets, show, top, who
from .store import db, reparse, sync
from .text import fold, near, parse_answer, plain, sentences, takes, things
