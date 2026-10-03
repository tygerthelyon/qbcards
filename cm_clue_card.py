# -*- coding: utf-8 -*-
"""cm_clue_card.py -- a DESCRIPTION to WORK card for Classical Music.

Audit 2026-09-26, 1.2: "The active music card shows the work title and asks for
the composer, so it reduces to title -> composer ... No card goes from a
description or plot to the work." Tossups run the other way: facts about a piece,
then "name this work".

One new field, Clue, and one template gated on it ({{#Clue}}), so the card exists
only where a clue has been written into the field -- one note per work (the
lowest-id movement), tier1 works only, per the tier gate. The clue is the note's
own Description with the title's distinctive words and the nickname masked as
"____", since several descriptions name the work ("The Pastoral, in five
movements ...", "the Moonlight name came from a critic ..."). Clues left under
50 characters after masking are skipped rather than shipped thin.

    py -3.9 cm_clue_card.py --dry | --apply
"""
import json
import re
import sys
import time

import concept_add as C
import qb_tier_model as T

M = "Classical Music"
NAME = "DESCRIPTION to WORK"
MASK = "____"
STOP = set("the and for with from der die das des dem den von und les des del della di da la le el los las une une op no".split())


def mask(desc, work, nick):
    words = set()
    for src in (work, nick):
        for t in re.split(r"[^\w'’-]+", C.plain(src)):
            f = C.fold(t)
            if len(f) > 2 and f not in T.GENERIC_MUSIC and f not in STOP and not f.isdigit():
                words.add(t)
    out = desc
    if nick:
        out = re.sub(re.escape(C.plain(nick)), MASK, out, flags=re.I)
    for w in sorted(words, key=len, reverse=True):
        out = re.sub(r"(?<![\w>])%s(?![\w<])" % re.escape(w), MASK, out, flags=re.I)
    out = re.sub(r"(%s[\s,]*){2,}" % re.escape(MASK), MASK + " ", out)
    return out.strip()


def ensure_model(dry):
    if "Clue" in C.anki("modelFieldNames", modelName=M):
        return
    t = C.anki("modelTemplates", modelName=M)
    if dry:
        print("would add field Clue and template", NAME)
        return
    json.dump(t, open("templates_backup/cm_before_clue_%s.json" % time.strftime("%Y%m%d_%H%M"), "w",
                      encoding="utf-8"), ensure_ascii=False)
    src = t["AUDIO and WORK to COMPOSER"]
    zoom = src["Front"][src["Front"].index('<script id="qb-zoom">'):]
    zoom = zoom[:zoom.index("</script>") + len("</script>")]
    front = ('{{#Clue}}<div class="cm2">\n<div class="cm2-eyebrow">Work</div>\n'
             '<div class="cm2-def">{{Clue}}</div>\n<div class="cm2-ask">Work?</div>\n</div>{{/Clue}}\n\n' + zoom)
    back = src["Back"].replace('<div class="cm2-eyebrow">{{#Audio}}Audio{{/Audio}}{{^Audio}}Work{{/Audio}}</div>',
                               '<div class="cm2-eyebrow">Work</div>\n<div class="cm2-def">{{Clue}}</div>', 1)
    back = back.replace('{{^Kind}}{{#Description}}<div class="cm2-desc">{{Description}}</div>{{/Description}}{{/Kind}}', "")
    back = back.replace("{{^Kind}}", "{{#Clue}}", 1).replace("</div>{{/Kind}}", "</div>{{/Clue}}", 1)
    C.anki("modelFieldAdd", modelName=M, fieldName="Clue", index=len(C.anki("modelFieldNames", modelName=M)))
    C.anki("modelTemplateAdd", modelName=M, template={"Name": NAME, "Front": front, "Back": back})
    print("added field Clue and template", NAME)


def main(apply):
    ensure_model(not apply)
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query='note:"%s" Kind: tag:Music::tier::tier1-core' % M))
    first = {}
    for n in sorted(ns, key=lambda n: n["noteId"]):
        k = (C.fold(C.plain(n["fields"]["Work"]["value"])), C.fold(C.plain(n["fields"]["Composer"]["value"])))
        first.setdefault(k, n)
    rows, skip = [], []
    for n in first.values():
        f = n["fields"]
        d = f["Description"]["value"].strip()
        if not d or f.get("Clue", {}).get("value"):
            continue
        c = mask(d, f["Work"]["value"], f["Nickname"]["value"])
        if len(C.plain(c).replace(MASK, "")) < 50:
            skip.append(C.plain(f["Work"]["value"]))
            continue
        rows.append((n["noteId"], C.plain(f["Work"]["value"]), c))
    for nid, w, c in rows:
        print("%-32s %s" % (w[:32], C.plain(c)[:150]))
    print(len(rows), "clues;", len(skip), "skipped as too thin:", ", ".join(skip[:20]))
    if apply:
        for nid, w, c in rows:
            C.anki("updateNoteFields", note={"id": nid, "fields": {"Clue": c}})
        print("written", len(rows))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
