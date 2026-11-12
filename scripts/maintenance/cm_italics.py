# -*- coding: utf-8 -*-
"""cm_italics.py -- italicise work titles and foreign words in Classical Music
Description and Listen.

Carter (2026-09-25): "Italicize all the foreign words and work titles in the new
CM text ... New world symphony should have 'from the new world', 'cor anglais',
'goin' home' all italicized."

Two stages, because neither alone is safe:
  1. PROPOSE  titles from the deck's own Work / Nickname / Movement fields
              (data/cm_italics_titles.json) and a foreign-term list, matched
              whole-word. Ambiguous one-word titles (London, Mars, Organ, Hunt)
              are never auto-matched: they are also cities, planets, instruments.
  2. CORRECT  every one of the 662 distinct texts read by hand; the result is in
              data/cm_italics_fix.txt as KEY +add|-remove ("+X@1" = first
              occurrence only). Keys are the order of first appearance.

Rules applied in the reading: titles of any work (music, numbers within works,
nicknames, songs, hymns, poems, books, films) italic; foreign words and Italian
performance markings italic, as Carter asked for cor anglais; style names
(Romantic, American), generic forms (the scherzo, the Prelude), institutions and
characters (Tosca stabs Scarpia, Oberon is a countertenor) roman. Quotation
marks around a title are dropped when it is italicised.

    py -3.9 cm_italics.py --dry [--all] | --apply
"""
import json
import re
import sys
import time

import concept_add as C

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TITLES = json.load(open("data/cm_italics_titles.json", encoding="utf-8"))
AMBIG = set("""Oxford London Thomas Organ Greek Harp Hunt Mars Titan Trout Fugue
    Largo Lento Rondo Kyrie Credo Octet Septet Galop Pavane Rosa Parade Modéré
    Animé Trauer Iberia Martha Louise Attila Hamlet Lear Faust Salome Tasso Undine
    Études Poème Élégie Syrinx Jeux Nuages Fêtes Razor Aoua Halt! Linz Prague
    Paris Jupiter Farewell Surprise Clock Military Drumroll Miracle Emperor
    Spring Winter Summer Autumn Tempest Pathétique Pastoral Eroica Unfinished
    Tragic Resurrection Italian Scottish Reformation Little Russian Polish
    Classical Leningrad Babi Yar Rhenish""".split())
FOREIGN = [
    "cor anglais", "col legno", "sul ponticello", "sul tasto", "con sordino",
    "pizzicato", "tremolo", "glissando", "glissandi", "ostinato", "ostinati",
    "staccato", "legato", "rubato", "cantabile", "coloratura", "bel canto",
    "a cappella", "da capo", "basso continuo", "basso ostinato", "ritornello",
    "ritornelli", "recitativo", "recitativo secco", "secco", "opera buffa",
    "opera seria", "opéra comique", "opéra-comique", "grand opéra", "grand opera",
    "Singspiel", "Lieder", "Lied", "Leitmotiv", "leitmotiv", "Gesamtkunstwerk",
    "verismo", "Sturm und Drang", "fortissimo", "pianissimo", "sforzando",
    "crescendo", "diminuendo", "accelerando", "ritardando", "rallentando",
    "cadenza", "arpeggio", "arpeggios", "arpeggiated", "obbligato", "tutti",
    "ripieno", "concertino", "concerto grosso", "cantus firmus", "ars nova",
    "ars antiqua", "organum", "style galant", "galant", "stile antico",
    "stile moderno", "idée fixe", "Klangfarbenmelodie", "Sprechstimme",
    "Sprechgesang", "pas de deux", "divertissement", "zarzuela", "fin de siècle",
    "habanera", "seguidilla", "furiant", "dumka", "Ländler", "ländler",
    "sotto voce", "mezza voce", "attacca", "alla breve", "alla turca",
    "alla marcia", "scherzando", "maestoso", "dolce", "espressivo", "ben marcato",
    "marcato", "sostenuto", "fugato", "stretto", "opus", "Kapellmeister",
    "Konzertstück", "Tafelmusik", "chanson", "chansons", "villancico", "lauda",
    "frottola", "tombeau", "passacaglia", "chaconne", "cantilena", "vocalise",
    "Heldentenor", "prima donna", "castrato", "castrati", "commedia dell'arte",
    "son et lumière", "kyrie", "Dies irae", "Dies Irae", "Agnus Dei",
    "Stabat Mater", "Te Deum", "Magnificat", "Nunc dimittis", "Lacrimosa",
    "Tuba mirum", "Rex tremendae", "Confutatis", "Benedictus", "Sanctus",
    "Hosanna", "Crucifixus", "Alleluia", "Ave Maria", "Salve Regina", "Libera me",
    "In paradisum", "Pie Jesu", "leggiero", "parlando", "martellato", "tenuto",
    "portamento", "vibrato", "morendo", "perdendosi", "misterioso",
    "appassionato", "agitato", "furioso", "Allegro", "Adagio", "Andante", "Largo",
    "Presto", "Allegretto", "Andantino", "Larghetto", "Lento", "Vivace",
    "Moderato", "Prestissimo", "Adagietto", "Menuetto"]
QUOTES = [("'", "'"), ("‘", "’"), ('"', '"'), ("“", "”")]


PATTERNS = [(t, re.compile(r"(?<![\w])" + re.escape(t) + r"(?![\w])"))
            for t in [t for t in TITLES if t not in AMBIG and len(t) >= 4]
            + sorted(FOREIGN, key=len, reverse=True)]


def propose(text):
    spans = []
    for t, rx in PATTERNS:
        if t not in text:
            continue
        for m in rx.finditer(text):
            if not any(m.start() < y and m.end() > x for x, y in spans):
                spans.append((m.start(), m.end()))
    return sorted(spans)


def keyed(rows):
    """Distinct texts in order of first appearance: D<n> descriptions, L<n> listens."""
    seen = {}
    for n in rows:
        f = n["fields"]
        for fld, p in (("Description", "D"), ("Listen", "L")):
            if fld == "Description" and f["Kind"]["value"].strip():
                continue
            t = f[fld]["value"].strip()
            if t and t not in seen:
                seen[t] = "%s%d" % (p, len(seen))
    return seen


def fixes():
    out = {}
    for line in open("data/cm_italics_fix.txt", encoding="utf-8"):
        line = line.rstrip("\n")
        if line.strip():
            k, rest = line.split(" ", 1)
            out.setdefault(k, []).extend(rest.split("|"))
    return out


def apply_fix(text, spans, ops, key, problems):
    spans = list(spans)
    for op in ops:
        sign, phrase, nth = op[0], op[1:], None
        if "@" in phrase and phrase.rsplit("@", 1)[1].isdigit():
            phrase, nth = phrase.rsplit("@", 1)
            nth = int(nth)
        if sign == "-":
            if not [s for s in spans if text[s[0]:s[1]] == phrase]:
                problems.append("%s: nothing proposed to remove as %r" % (key, phrase))
            spans = [s for s in spans if text[s[0]:s[1]] != phrase]
            continue
        ms = list(re.finditer(r"(?<![\w])" + re.escape(phrase) + r"(?![\w])", text))
        if not ms:
            problems.append("%s: %r not in text" % (key, phrase))
        if nth:
            ms = ms[nth - 1:nth]
        for m in ms:
            a, b = m.start(), m.end()
            spans = [s for s in spans if not (s[0] < b and s[1] > a)]
            spans.append((a, b))
    return sorted(spans)


def render(text, spans):
    out, i = [], 0
    for a, b in spans:
        pre, after = text[i:a], b
        for ql, qr in QUOTES:
            if pre.endswith(ql) and text[b:b + len(qr)] == qr:
                pre, after = pre[:-len(ql)], b + len(qr)
                break
        out += [pre, "<i>", text[a:b], "</i>"]
        i = after
    return "".join(out + [text[i:]])


def main():
    apply = "--apply" in sys.argv
    rows = C.anki("notesInfo", notes=C.anki("findNotes", query='note:"Classical Music"'))
    seen = keyed(rows)
    fx = fixes()
    changed, problems = {}, []
    for t, k in seen.items():
        if "<" in t:
            problems.append("%s already has markup, skipped" % k)
            continue
        v = render(t, apply_fix(t, propose(t), fx.get(k, []), k, problems))
        if v != t:
            changed[t] = v
    unknown = set(fx) - set(seen.values())
    if unknown:
        problems.append("fix keys with no text: %s" % sorted(unknown))
    for t, v in list(changed.items())[:1000 if "--all" in sys.argv else 25]:
        print(seen[t], "|", v)
    print("\n%d distinct texts, %d gain italics" % (len(seen), len(changed)))
    for p in problems:
        print("   PROBLEM", p)
    upd, backup = [], {}
    for n in rows:
        f = {}
        for fld in ("Description", "Listen"):
            if fld == "Description" and n["fields"]["Kind"]["value"].strip():
                continue
            v = n["fields"][fld]["value"].strip()
            if v in changed:
                f[fld] = changed[v]
        if f:
            upd.append({"id": n["noteId"], "fields": f})
            backup[n["noteId"]] = {k: n["fields"][k]["value"] for k in f}
    print("%d notes to update" % len(upd))
    if apply and not problems:
        json.dump(backup, open("backups/cm_italics_before_%s.json" % time.strftime("%Y%m%d_%H%M"),
                               "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        C.anki("multi", actions=[{"action": "updateNoteFields", "params": {"note": u}}
                                 for u in upd])
        print("applied")
    elif apply:
        print("NOT applied: resolve the problems first")


if __name__ == "__main__":
    main()
