# -*- coding: utf-8 -*-
"""apply_audit.py -- apply the cloud audit's field fixes through AnkiConnect (Anki must be open).

    py -3.9 audit\\apply_audit.py                 dry run: what would change, and what is skipped
    py -3.9 audit\\apply_audit.py --apply         write the high-confidence findings
    py -3.9 audit\\apply_audit.py --rewrites      also take audit/lapsed_rewrites.jsonl (dry run)
    py -3.9 audit\\apply_audit.py --rewrites --apply

Options:
    --deck "Film"        only findings for one note type (repeatable)
    --include-medium     also write medium-confidence rows (only after reading them in the dry run)
    --only ID:FIELD      only this note/field (repeatable), e.g. --only 1788490082193:Clue

Reads audit/*_findings.jsonl (and lapsed_rewrites.jsonl with --rewrites). Each row carries the field's
text as exported on 2026-10-04 ("current"). A row is written only if the field in Anki still equals that
text exactly, so anything another session has edited since is skipped, never overwritten.

Only updateNoteFields is called: no template, tag, deck, or card-state changes. Every field written is
backed up first to backups/audit_<timestamp>.json (note id, field, old value, new value).
"""
import glob
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NEVER = {"Listen"}   # never written, whatever a row says


def anki(action, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", data=json.dumps(
        {"action": action, "version": 6, "params": params}).encode(), headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    if r.get("error"):
        raise RuntimeError("%s: %s" % (action, r["error"]))
    return r["result"]


def chunk(xs, n=200):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def arg_list(flag):
    out, a = [], sys.argv
    for i, x in enumerate(a):
        if x == flag and i + 1 < len(a):
            out.append(a[i + 1])
    return out


def load_rows(rewrites):
    files = sorted(glob.glob(os.path.join(HERE, "*_findings.jsonl")))
    if rewrites:
        files.append(os.path.join(HERE, "lapsed_rewrites.jsonl"))
    rows = []
    for fn in files:
        if not os.path.exists(fn):
            print("missing: %s" % fn)
            continue
        with open(fn, encoding="utf-8") as f:
            for ln, line in enumerate(f, 1):
                if line.strip():
                    r = json.loads(line)
                    r["_src"] = "%s:%d" % (os.path.basename(fn), ln)
                    rows.append(r)
    return rows


def short(s, n=110):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[:n - 1] + "…"


def main():
    apply = "--apply" in sys.argv
    rewrites = "--rewrites" in sys.argv
    medium_ok = "--include-medium" in sys.argv
    decks = set(arg_list("--deck"))
    only = set(arg_list("--only"))

    rows = load_rows(rewrites)
    if decks:
        rows = [r for r in rows if r["model"] in decks]
    if only:
        rows = [r for r in rows if "%s:%s" % (r["note_id"], r["field"]) in only]

    ids = sorted({r["note_id"] for r in rows})
    live = {}
    for ch in chunk(ids):
        for n in anki("notesInfo", notes=ch):
            if n:   # deleted notes come back as {}
                live[n["noteId"]] = n

    todo, review, skipped = [], [], []
    seen = set()
    for r in rows:
        key = (r["note_id"], r["field"])
        n = live.get(r["note_id"])
        if r["field"] in NEVER:
            skipped.append((r, "Listen fields are never edited"))
        elif key in seen:
            skipped.append((r, "a second row for the same field (fix the jsonl)"))
        elif n is None:
            skipped.append((r, "note no longer exists"))
        elif n.get("modelName") != r["model"]:
            skipped.append((r, "note type is now %r" % n.get("modelName")))
        elif r["field"] not in n["fields"]:
            skipped.append((r, "field no longer exists"))
        elif n["fields"][r["field"]]["value"] == r["proposed"]:
            skipped.append((r, "already applied"))
        elif n["fields"][r["field"]]["value"] != r["current"]:
            skipped.append((r, "field changed since the export"))
        elif r.get("confidence") != "high" and not medium_ok:
            review.append(r)
        else:
            todo.append(r)
        seen.add(key)

    print("%d rows read; %d to write, %d medium for review, %d skipped.\n"
          % (len(rows), len(todo), len(review), len(skipped)))
    for r in todo:
        print("WRITE  %s  %s %s [%s/%s]\n   - %s\n   + %s\n   why: %s"
              % (r["model"], r["note_id"], r["field"], r["kind"], r.get("confidence"),
                 short(r["current"]), short(r["proposed"]), r["why"]))
    if review:
        print("\nMEDIUM confidence -- not written. Read each; apply the ones you agree with using\n"
              "  --include-medium --only NOTE_ID:FIELD [--only ...]\n")
        for r in review:
            print("REVIEW %s  %s:%s [%s]\n   - %s\n   + %s\n   why: %s\n   sources: %s"
                  % (r["model"], r["note_id"], r["field"], r["kind"], short(r["current"]),
                     short(r["proposed"]), r["why"], " ".join(r.get("sources", [])) or "-"))
    if skipped:
        print("\nSKIPPED")
        for r, why in skipped:
            print("  %s %s:%s  -- %s" % (r["model"], r["note_id"], r["field"], why))

    if not apply:
        print("\nDry run. Nothing written. Add --apply to write the %d rows above." % len(todo))
        return
    if not todo:
        print("\nNothing to write.")
        return

    os.makedirs(os.path.join(ROOT, "backups"), exist_ok=True)
    bk = os.path.join(ROOT, "backups", "audit_%s.json" % time.strftime("%Y%m%d_%H%M%S"))
    with open(bk, "w", encoding="utf-8") as f:
        json.dump([{"note_id": r["note_id"], "model": r["model"], "field": r["field"],
                    "old": r["current"], "new": r["proposed"], "src": r["_src"]} for r in todo],
                  f, ensure_ascii=False, indent=1)
    print("\nBackup: %s" % bk)

    by_note = {}
    for r in todo:
        by_note.setdefault(r["note_id"], {})[r["field"]] = r["proposed"]
    done = 0
    for nid, fields in by_note.items():
        anki("updateNoteFields", note={"id": nid, "fields": fields})
        done += len(fields)
    print("Wrote %d fields on %d notes. No templates, tags, decks, or card states were touched." % (done, len(by_note)))


if __name__ == "__main__":
    main()
