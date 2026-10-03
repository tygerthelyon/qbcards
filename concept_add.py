"""
CONCEPT_ADD.PY
Add definition-to-name concept cards, without creating the faults that
concept cards in this collection have historically had.

    python concept_add.py --deck Architecture --dry
    python concept_add.py --deck Architecture --apply

WHY THESE CARDS KEEP BREAKING
    Every concept card I have found broken in this collection broke the same
    way: the card asked for something the note could not supply. The Art
    technique card read "Technique?" over an empty space because Artwork
    held the string [IMAGE PENDING]. The Architecture style card asked for a
    style and printed "Brick Gothic, Romanesque (side chapels in Dutch
    Renaissance, Neoclassicism, Byzantine Revival and Modernist styles)".

    So the card built here is the one shape that cannot fail that way: a
    definition on the front, a single name as the answer. It needs no
    picture, so it cannot render a prompt over a blank. Architecture already
    has exactly this card and it works.

WHAT IS CHECKED BEFORE ANY NOTE IS ADDED
    duplicates   against every existing Name/Title in the deck, folded, so
                 a term already covered is skipped rather than doubled
    leak         the definition must not contain the answer -- a clue that
                 says "the Corinthian order is..." gives away Corinthian
    completeness every note must have a name, a kind and a definition

--dry prints what would be added and writes nothing.
"""
import argparse, json, re, sys, unicodedata, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def anki(action, **params):
    req = urllib.request.Request(
        "http://127.0.0.1:8765",
        data=json.dumps({"action": action, "version": 6,
                         "params": params}).encode(),
        headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    if r.get("error"):
        raise RuntimeError(r["error"])
    return r["result"]


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s.lower())).strip()


STOPWORD = set("the a an of in on and or to for with is are was were".split())

# The category noun in a term is not the answer. "Barrel vault" is answered
# by "barrel", not by "vault", and a definition of it can hardly avoid
# saying what kind of thing it is. Only the distinguishing word is guarded.
CATEGORY = set("""vault arch order window roof style architecture church
    column capital dome tower house building form technique process print
    printing painting music note scale chord texture voice line plan
    ceiling wall gate room space temple hall period movement school
    sonata concerto symphony opera mass motet suite dance song aria
    photo photograph photography camera lens exposure image film plate print""".split())


def leaks(name, text):
    """True when the definition gives the answer away."""
    t = fold(text)
    n = fold(name)
    if n and n in t:
        return True
    words = [w for w in n.split()
             if w not in STOPWORD and w not in CATEGORY and len(w) > 4]
    return any(re.search(r"\b%s" % re.escape(w[:-1] if w.endswith("s") else w),
                         t) for w in words)


def existing(model, key, concepts_only=False):
    """Names already in the deck.

    concepts_only restricts the comparison to notes that already carry a
    Kind. The Classical Music deck holds PIECES called Canon, Nocturne and
    Toccata; a concept card for the form of that name does not collide with
    them, because the two are told apart by Kind and by which card asks."""
    notes = anki("notesInfo", notes=anki("findNotes", query='note:"%s"' % model))
    out = set()
    for n in notes:
        if concepts_only and not plain(n["fields"].get("Kind", {}).get("value", "")):
            continue
        out.add(fold(plain(n["fields"][key]["value"])))
        for alt in ("Alternate",):
            if alt in n["fields"]:
                for a in re.split(r"[;,]", plain(n["fields"][alt]["value"])):
                    if a.strip():
                        out.add(fold(a))
    return out


def add(model, key, deck, rows, fieldmap, dry=True, tags=(),
        concepts_only=False):
    have = existing(model, key, concepts_only)
    todo, skipped, bad = [], [], []
    for r in rows:
        name = r["name"]
        if fold(name) in have:
            skipped.append(name)
            continue
        if not r.get("definition") or not r.get("kind"):
            bad.append((name, "missing kind or definition"))
            continue
        if leaks(name, r["definition"]):
            bad.append((name, "definition contains the answer"))
            continue
        todo.append(r)
        have.add(fold(name))

    print("%d proposed, %d already in the deck, %d rejected"
          % (len(todo), len(skipped), len(bad)))
    for n, why in bad:
        print("   REJECTED %-34s %s" % (n[:34], why))
    if skipped:
        print("   already present: %s%s"
              % ", ".join(skipped[:8]) if False else
              ("   already present: %s%s"
               % (", ".join(skipped[:8]), " ..." if len(skipped) > 8 else "")))
    if dry:
        for r in todo:
            print("   + %-34s [%s] %s" % (r["name"][:34], r["kind"],
                                          r["definition"][:70]))
        return 0

    made = 0
    for r in todo:
        fields = {}
        for field, source in fieldmap.items():
            v = r.get(source, "")
            if v:
                fields[field] = v
        try:
            anki("addNote", note={
                "deckName": deck, "modelName": model, "fields": fields,
                "tags": list(tags),
                "options": {"allowDuplicate": True}})
            made += 1
        except RuntimeError as e:
            print("   FAILED  %-30s %s" % (r["name"][:30], e))
    print("added %d notes" % made)
    return made
