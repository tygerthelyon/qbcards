# -*- coding: utf-8 -*-
"""caption_clean.py [--dry|--apply] -- tidy every caption in the collection.

Carter, on the Islamic architecture card: "faulty captions: either very long,
contain met-data (like [25]), etc."

Both faults come from the same place. The captions were taken from Wikipedia's
media-list, which returns the article's own caption HTML -- so footnote markers
came with it, and so did whole explanatory paragraphs written to sit beside a
body of text rather than under a thumbnail. One Art caption is 1,131 characters;
another carries a raw `.mw-parser-output` CSS rule where a fraction was meant to
render.

Three passes over 4,503 captions in six decks:

  markers   [25], [citation needed], [a] and the like, removed.
  markup    leftover MediaWiki CSS and the empty spans it hangs on.
  length    a caption longer than 130 characters is cut to its first sentence;
            if that is still over 160 it is cut at a word boundary and given an
            ellipsis. Italics are preserved, and any tag left open by the cut is
            closed again.

Nothing is rewritten for style -- a caption that is already short and clean is
left exactly as it is.
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import concept_add as C

FIELDS = {
 "Architecture": ["Caption 1", "Caption 2", "Caption 3", "Caption 4"],
 "Art": ["Captions"],
 "Photography": ["Captions"],
 "Performing Arts": ["Captions", "Gallery captions", "Caption"],
 "Film": ["Caption", "Still caption", "Still 2 caption", "Still 3 caption",
          "Poster caption"],
 "Geography": ["Photo caption"],
}
REF = re.compile(r"\s*\[\s*(?:\d+|citation needed|note \d+|[a-z])\s*\]", re.I)
MWCSS = re.compile(r"\.mw-[^{]*\{[^}]*\}", re.I)
MWSPAN = re.compile(r"<span class=\"mw-[^\"]*\"[^>]*>\s*</span>", re.I)
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
SOFT, HARD = 130, 160


def balance(s):
    for tag in ("i", "b", "em", "strong"):
        open_n = len(re.findall(r"<%s\b" % tag, s, re.I))
        close_n = len(re.findall(r"</%s>" % tag, s, re.I))
        if open_n > close_n:
            s += ("</%s>" % tag) * (open_n - close_n)
        elif close_n > open_n:
            s = re.sub(r"</%s>" % tag, "", s, count=close_n - open_n, flags=re.I)
    return s


def clean(raw):
    s = MWCSS.sub("", raw)
    s = MWSPAN.sub("", s)
    s = REF.sub("", s)
    s = re.sub(r"\s+", " ", s).strip(" ;,")
    if len(C.plain(s)) <= SOFT:
        return balance(s)
    parts = SENT.split(s)
    if parts and len(C.plain(parts[0])) <= HARD:
        return balance(parts[0].strip())
    # still too long: cut at a word boundary inside the first sentence
    head = parts[0] if parts else s
    cut = head[:HARD]
    cut = cut[:cut.rfind(" ")] if " " in cut else cut
    return balance(cut.rstrip(" ,;:") + "…")


def main():
    dry = "--apply" not in sys.argv
    changed = shown = 0
    for model, fs in FIELDS.items():
        ns = C.anki("notesInfo", notes=C.anki("findNotes", query='note:"%s"' % model))
        hits = 0
        for n in ns:
            upd = {}
            for f in fs:
                if f not in n["fields"]:
                    continue
                raw = n["fields"][f]["value"]
                if not raw.strip():
                    continue
                parts = raw.split("|")
                new = [clean(p) for p in parts]
                joined = " | ".join(new) if len(parts) > 1 else new[0]
                if joined != raw:
                    upd[f] = joined
                    if shown < 12 and len(C.plain(raw)) > SOFT:
                        print("  %-14s %s" % (model, C.plain(raw)[:88] + "..."))
                        print("  %-14s -> %s\n" % ("", C.plain(joined)[:96]))
                        shown += 1
            if upd:
                hits += 1
                if not dry:
                    C.anki("updateNoteFields", note={"id": n["noteId"], "fields": upd})
        print("%-16s notes changed: %d" % (model, hits))
        changed += hits
    print("\ntotal notes changed: %d" % changed)
    if dry:
        print("-- dry run --")


if __name__ == "__main__":
    main()
