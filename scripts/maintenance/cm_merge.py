# -*- coding: utf-8 -*-
"""cm_merge.py -- one note per movement, with every clip attached.

Carter (2026-09-25): "my issue was with having multiple cards for different clips
of the same movement, in which case i suggested you just attach multiple audio
clips on the same card."

cm_dupe.py (W115) only suspended duplicate tier1 notes and threw their clips
away. This works across every tier: notes are the same movement when composer,
work, movement and nickname all match. The richest note is kept, it takes the
best tier in its group, and every distinct clip in the group is added to its
Audio field (Anki shows one play button per clip). The others are suspended and
tagged Music::merged -- not deleted, so review history survives and the merge
can be undone.

    py -3.9 cm_merge.py --dry | --apply
"""
import collections
import json
import re
import sys
import time

import concept_add as C
from cm_dupe import score

RANK = {"tier1-core": 1, "tier2-solid": 2, "tier3-deepcut": 3, "tier4-rare": 4}


def tier(n):
    t = [x.split("::")[-1] for x in n["tags"] if x.startswith("Music::tier::")]
    return t[0] if t else "tier4-rare"


def main():
    apply = "--apply" in sys.argv
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query='note:"Classical Music" Kind: -tag:Music::merged'))
    groups = collections.defaultdict(list)
    for n in ns:
        f = n["fields"]
        k = tuple(C.fold(C.plain(f[x]["value"])) for x in ("Composer", "Work", "Movement", "Nickname"))
        groups[k].append(n)
    plan, backup = [], {}
    for k, g in sorted(groups.items()):
        if len(g) < 2:
            continue
        g.sort(key=lambda n: (-score(n), RANK[tier(n)]))
        keep, rest = g[0], g[1:]
        clips = []
        for n in g:
            for s in re.findall(r"\[sound:[^\]]+\]", n["fields"]["Audio"]["value"]):
                if s not in clips:
                    clips.append(s)
        best = min((tier(n) for n in g), key=RANK.get)
        plan.append((keep, rest, clips, best))
    print("%d groups, %d notes to fold in" % (len(plan), sum(len(r) for _, r, _, _ in plan)))
    for keep, rest, clips, best in plan[:40]:
        f = keep["fields"]
        print("  %-24s %-30s %-28s keep %s (%s->%s), %d clips, fold %d"
              % (C.plain(f["Composer"]["value"])[-24:], C.plain(f["Work"]["value"])[:30],
                 C.plain(f["Movement"]["value"])[:28], keep["noteId"] % 100000, tier(keep), best, len(clips), len(rest)))
    if not apply:
        return
    for keep, rest, clips, best in plan:
        backup[keep["noteId"]] = {"Audio": keep["fields"]["Audio"]["value"], "tags": keep["tags"]}
        C.anki("updateNoteFields", note={"id": keep["noteId"], "fields": {"Audio": "".join(clips)}})
        if best != tier(keep):
            C.anki("removeTags", notes=[keep["noteId"]], tags="Music::tier::" + tier(keep))
            C.anki("addTags", notes=[keep["noteId"]], tags="Music::tier::" + best)
            if best == "tier1-core":
                cards = C.anki("findCards", query="nid:%d" % keep["noteId"])
                # the title card is the one the queue uses; ear cards stay as they are
                title = [c["cardId"] for c in C.anki("cardsInfo", cards=cards) if c["ord"] == 1]
                if title:
                    C.anki("unsuspend", cards=title)
        ids = [n["noteId"] for n in rest]
        C.anki("addTags", notes=ids, tags="Music::merged")
        cards = C.anki("findCards", query=" OR ".join("nid:%d" % i for i in ids))
        if cards:
            C.anki("suspend", cards=cards)
    json.dump(backup, open("backups/cm_merge_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"),
              ensure_ascii=False)
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
