# -*- coding: utf-8 -*-
"""cm_dupe.py [--dry|--apply] -- collapse duplicate tier1 pieces.

Listing the 280 tier1 pieces with audio showed the same excerpt more than once:
Chopin's Nocturne Op. 9 No. 2 three times, the Brahms Requiem's second and third
movements three times each, Eroica mvt I twice, Beethoven 5 mvt I twice, the
Nutcracker's Chinese Dance twice. Two separate notes for one excerpt is the
massing problem in miniature -- the same sound reviewed twice on the same day,
teaching nothing the first review did not.

Keep the richest note of each group (audio, then Description, then filled fields)
and suspend the rest. Suspend rather than delete: the review history is real and
Carter may have scheduling on them.
"""
import collections
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import concept_add as C

BAD_MOVEMENTS = ("Die Jahre am Konservatorium", "Die populare Trilogie",
                 "Die populäre Trilogie")


def score(n):
    f = n["fields"]
    s = 0
    if C.plain(f["Audio"]["value"]).strip():
        s += 8
    if C.plain(f["Description"]["value"]).strip():
        s += 4
    if C.plain(f["Composer Image"]["value"]).strip():
        s += 2
    s += sum(1 for k, v in f.items() if C.plain(v["value"]).strip())
    return s


def main():
    dry = "--apply" not in sys.argv
    ns = C.anki("notesInfo",
                notes=C.anki("findNotes", query='note:"Classical Music" tag:Music::tier::tier1-core'))
    works = [n for n in ns if not C.plain(n["fields"]["Kind"]["value"]).strip()]

    groups = collections.defaultdict(list)
    for n in works:
        f = n["fields"]
        k = (C.fold(C.plain(f["Composer"]["value"])),
             C.fold(C.plain(f["Work"]["value"])),
             C.fold(C.plain(f["Movement"]["value"])),
             C.fold(C.plain(f["Nickname"]["value"])))
        groups[k].append(n)

    kill, keep_report = [], []
    for k, g in sorted(groups.items()):
        if len(g) < 2:
            continue
        g.sort(key=score, reverse=True)
        keep_report.append((k, g))
        kill += g[1:]
    print("duplicate tier1 groups: %d, redundant notes: %d"
          % (len(keep_report), len(kill)))
    for (comp, work, mv, nk), g in keep_report:
        print("   %-22s %-30s %-22s  keep 1 of %d"
              % (comp[:22], (work + (" ~" + nk if nk else ""))[:30], mv[:22], len(g)))

    # the two bogus "movements" scraped from German Wikipedia headings
    bogus = [n for n in works
             if C.plain(n["fields"]["Movement"]["value"]).strip() in BAD_MOVEMENTS]
    print("\nnotes with a Wikipedia section heading as Movement: %d" % len(bogus))
    for n in bogus:
        print("   %s -- %s" % (C.plain(n["fields"]["Work"]["value"]),
                              C.plain(n["fields"]["Movement"]["value"])))

    if dry:
        print("\n-- dry run --")
        return

    cards = [c for n in kill for c in n["cards"]]
    for i in range(0, len(cards), 500):
        C.anki("suspend", cards=cards[i:i + 500])
    if kill:
        C.anki("addTags", notes=[n["noteId"] for n in kill], tags="Music::dupe-suspended")
        for n in kill:
            old = [t for t in n["tags"] if "::tier::" in t]
            if old:
                C.anki("removeTags", notes=[n["noteId"]], tags=" ".join(old))
            C.anki("addTags", notes=[n["noteId"]], tags="Music::tier::tier3-deepcut")
    print("\nsuspended and demoted %d duplicate notes (%d cards)" % (len(kill), len(cards)))

    for n in bogus:
        C.anki("updateNoteFields",
               note={"id": n["noteId"], "fields": {"Movement": ""}})
    print("cleared %d bogus Movement values" % len(bogus))
    print("active Classical Music cards: %d"
          % len(C.anki("findCards", query='deck:"Classical Music" -is:suspended')))


if __name__ == "__main__":
    main()
