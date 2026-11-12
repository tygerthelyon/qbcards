# -*- coding: utf-8 -*-
"""Independent sanity checks for the QBReader mirror and its search layer.

Run from C:\QB\stockfisher with ``py -3.9 -m qbr.selftest``. The checks compare
the local copy with the live API and write only to a temporary scratch database;
they never write to the production mirror or Anki.
"""
import argparse
import contextlib
import io
import math
import os
import re
import statistics
import sys
import tempfile

from . import anki as anki_module, api, clues as clue_module, find as find_module, store
from .clues import profile as clue_profile, verify_clue
from .find import answered as search_answered
from .find import search as clue_search
from .text import fold, near, parse_answer, sentences, takes, things


MALEVICH = "Kazimir Malevich"
MALEVICH_VFA_BENCHMARK = (3, 24)   # tossups, bonus parts at diff 4+ in Visual Fine Arts
MALEVICH_ALL_BENCHMARK = (3, 27)   # all categories and difficulties
SEARCH_CASES = (
    ("Black Square", "Visual Fine Arts", {"categories": "Fine Arts", "subcategories": "Visual Fine Arts"}),
    ("Higgs boson", "Science", {"categories": "Science"}),
    ("DNA polymerase", "Biology", {"categories": "Science", "subcategories": "Biology"}),
    ("photoelectric effect", "Physics", {"categories": "Science", "subcategories": "Physics"}),
)
SEARCH_DIAGNOSTICS = (
    ("double helix", "Biology", {"categories": "Science", "subcategories": "Biology"}),
)
ANSWER_LINE_REGRESSIONS = (
    ("description is not an alternate",
     "facial recognition [prompt on object recognition; accept any answer indicating the ability to perceive or differentiate faces]",
     "<b><u>facial recognition</u></b> [prompt on <u>object recognition</u>; accept any answer indicating the ability to perceive or differentiate faces]",
     (), ("differentiate faces",)),
    ("quoted semicolon in alternate",
     'hares or rabbits [accept "Br\'er Rabbit;" accept bunny or bunnies]',
     '<b><u>hare</u></b>s or <b><u>rabbit</u></b>s [accept “Br’er <b><u>Rabbit</u></b>;” accept <b><u>bunny</u></b> or <b><u>bunnies</u></b>]',
     ("br er rabbit", "bunny", "bunnies"), ("accept bunny",)),
    ("moderator note is not an alternate",
     "Tom Wolfe [or Thomas Kennerly Wolfe, Jr.] NOTE TO MODERATOR: DO NOT REVEAL ALTERNATE ANSWERS TO THE FIRST BONUS PART",
     "Tom <b><u>Wolfe</u></b> [or Thomas Kennerly <b><u>Wolfe</u></b>, Jr.] NOTE TO MODERATOR: DO NOT REVEAL ALTERNATE ANSWERS TO THE FIRST BONUS PART",
     ("thomas kennerly wolfe",), ("jr",)),
    ("rubric description is not a list of aliases",
     'Greek gods [or the Olympian gods; or the Greek pantheon; answers mentioning Greek or Greece or Olympic or Olympian and the idea of divinities or deities, or other synonyms; prompt on "gods" or synonyms]',
     '<u>Greek god</u>s [or the <u>Olympian</u> gods; or the <u>Greek pantheon</u>; answers mentioning <u>Greek</u> or <u>Greece</u> or <u>Olympic</u> or <u>Olympian</u> and the idea of <u>divinitie</u>s or <u>deitie</u>s, or other synonyms; prompt on “<u>god</u>s” or synonyms]',
     (), ("greece", "olympic", "deities", "olympian and the idea of divinities")),
)
PARSER_REGRESSIONS = (
    ('fables [or Aesop\'s fables; prompt on short stories; do not accept "fabliau"]',
     ("aesop s fables",), ("fabliau",)),
    ('Planet Earth II [do not prompt on or accept "Planet Earth"]', (), ("planet earth",)),
    ('John Adams [do not accept or prompt on "John Quincy Adams"]', (), ("john quincy adams",)),
    ('Ethiopia [accept Ethiopian Empire or Abyssinia; do not accept "Eritrea"]',
     ("ethiopian empire", "abyssinia"), ("eritrea",)),
    ('imine [do not accept "amine," and ask them to spell if necessary]', (), ("amine", "and ask them to spell")),
    ('linear momentum [or canonical momentum; accept linear momentum operator; prompt on p; do not accept "angular momentum"]',
     ("canonical momentum", "linear momentum operator"), ("angular momentum", "p")),
    ('after [accept After Walker Evans]', ("after walker evans",), ("evans",)),
    ('novel [or For Whom the Bell Tolls; or Before Sunrise; or Once Upon a Time in the West]',
     ("for whom the bell tolls", "before sunrise", "once upon a time in the west"), ("tolls",)),
    ('strong nuclear force [or strong interaction or similar answers]', ("strong interaction",), ("similar answers",)),
    ('conclave [accept papal election or any description of choosing or selecting a new Pope]',
     ("papal election",), ("selecting a new pope",)),
    ('IBM (accept International Business Machines Corporation, prompt on Big Blue)',
     ("international business machines corporation",), ("prompt on big blue", "big blue")),
    ('owls [accept Strix; accept Strigidae; accept Eurasian Eagle Owl accept Tyto; accept screech owl; prompt on birds]',
     ("strix", "eurasian eagle owl", "tyto", "screech owl"), ("birds", "eurasian eagle owl accept tyto")),
    ('Pete Buttigieg [Peter Paul Montgomery Buttigieg; accept Mayor Pete, prompt on Peter]',
     ("mayor pete",), ("peter", "prompt on peter")),
    ('airfoils [or aerofoils; accept aircraft wings; prompt on foils before "air" is read and accept afterwards; reject "jets"]',
     ("aerofoils", "aircraft wings"), ("afterwards", "jets", "foils")),
    ('the Master [accept the Master Letters; accept but DO NOT OTHERWISE MENTION answers like "Emily Dickinson\'s Master"]',
     ("master letters",), ("but", "but do not otherwise mention")),
    ('acetylcholine (accept AcH before mention, accept Otto Loewi before mention)',
     ("ach", "otto loewi"), ()),
    ('tax havens [accept corporate tax havens or corporate havens; accept offshore financial centers or OFCs until "OFCs" is read] (The 2013 book is The Hidden Wealth of Nations.)',
     ("corporate tax havens", "corporate havens", "offshore financial centers", "ofcs"), ()),
    ('Kazimir Malevich [or Kazimir Severinovich Malevich; prompt on Suprematist]',
     ("kazimir severinovich malevich",), ("suprematist",)),
    ('the Hagia Sophia [or Ayasofya; or Church of the Holy Wisdom; accept Sancta Sophia until "Sophia" is read; prompt on mosque]',
     ("ayasofya", "church of the holy wisdom", "sancta sophia"), ("mosque",)),
    ('John Wayne [or Marion Morrison or Marion Robert Morrison; accept "the Duke"; accept Jesus and John Wayne; accept John Wayning]',
     ("marion morrison", "marion robert morrison", "duke"), ()),
    # One-letter alternates are deliberately discarded by the parser's minimum-length rule.
    ('X [before "Y" is read, accept Z; after "Y" is read, prompt on Z]', (), ("y", "z", "before y is read")),
    ('Magic Johnson (or Earvin Johnson , Jr.)', ("earvin johnson",), ("jr",)),
    ('apraxia [do not accept "aphasia" or "ataxia" or "agnosia"]', (), ("aphasia", "ataxia", "agnosia")),
    ('books [accept obvious equivalents like texts or novels]', (), ()),
    ('the answer [accept "I am in training don\'t kiss me"]',
     ("i am in training don t kiss me",), ("kiss me",)),
    ('United States [accept either underlined part, or USA, or US]', ("usa", "us"), ()),
)
SENTENCE_REGRESSIONS = (
    ("689a0d672d8608f4ad8516e3", "Milone et al. 2017"),
    ("6a2cc108c2299b5c28965500", "Gentile et al. 2009"),
    ("68486967b074cbb48b99b348", "Tom B. Brown et al. 2020"),
)


def report(label, passed, detail):
    print("%s: %s -- %s" % ("PASS" if passed else "FAIL", label, detail))
    return bool(passed)


def mirror_question_counts(con, where="", args=()):
    out = {"T": 0, "B": 0}
    for r in con.execute("SELECT kind, count(*) AS n FROM q" + where + " GROUP BY kind", args):
        out[r["kind"]] = r["n"]
    return out["T"], out["B"]


def rejected_answers_accepted(con):
    """Recount apparent accept/reject contradictions with the live parser.

    Uses a conservative corpus-wide heuristic: flags are candidates rather than
    guaranteed errors, as several hundred are legitimate accepted phrases that
    contain a rejected look-alike.
    """
    bad = 0
    sql = ("SELECT answer FROM u WHERE answer LIKE '%do not%' OR answer LIKE '%reject%' "
           "OR answer LIKE '%don''t%'")
    for row in con.execute(sql):
        answer = row["answer"] or ""
        accepts = parse_answer(answer)["accepts"]
        first = re.search(r"do not|don'?t|reject", answer, re.I)
        head = " %s " % fold(answer[:first.start()] if first else answer)
        negative = " %s " % fold(" ; ".join(
            m.group(1) for m in re.finditer(r"(?:do not|don'?t|reject)\b([^;\]\)]*)", answer, re.I)))
        if any((" %s " % accepted) in negative and (" %s " % accepted) not in head
               for accepted in accepts[1:]):
            bad += 1
    return bad


def scratch_store_regressions():
    """Exercise set replacement/deletion against an isolated, disposable mirror."""
    old_path, old_con = store.PATH, store._CON
    old_env = os.environ.get("QBR_DB")
    old_set_list, old_pages, old_counts = store.api.set_list, store.api.pages, store.api.counts

    def row(set_name, qid, clue, answer):
        return {
            "_id": qid, "_kind": "T",
            "set": {"name": set_name, "year": 2026, "standard": True},
            "packet": {"number": 1, "name": "Scratch"}, "number": 1,
            "difficulty": 7, "category": "Science", "subcategory": "Physics",
            "question": clue, "question_sanitized": clue,
            "answer": answer, "answer_sanitized": answer,
        }

    try:
        with tempfile.TemporaryDirectory(prefix="qbr-selftest-") as temp:
            path = os.path.join(temp, "scratch.sqlite")
            os.environ["QBR_DB"] = path
            store.PATH = path
            store._CON = None
            con = store.connect(write=True)
            name = "QBR selftest disposable set"
            store._put_set(con, name, [row(name, "qbr-selftest-replaced", "old alpha phrase", "Old Answer")])
            con.commit()
            store._put_set(con, name, [row(name, "qbr-selftest-replaced", "new beta phrase", "New Answer")])
            con.commit()
            replacement_ok = (
                con.execute("SELECT count(*) FROM q").fetchone()[0] == 1 and
                con.execute("SELECT count(*) FROM u WHERE main='New Answer'").fetchone()[0] == 1 and
                con.execute("SELECT count(*) FROM f WHERE f MATCH ?", ('"old alpha"',)).fetchone()[0] == 0 and
                con.execute("SELECT count(*) FROM f WHERE f MATCH ?", ('"new beta"',)).fetchone()[0] == 1
            )
            con.close()

            # No set is listed by the fake API, so sync must remove the one in
            # this scratch mirror without making any network requests.
            store.api.set_list = lambda: []
            store.api.pages = lambda **kwargs: iter(())
            store.api.counts = lambda **kwargs: (0, 0)
            store.sync(log=lambda _message: None)
            check = store.connect(write=False)
            deletion_ok = (
                check.execute("SELECT count(*) FROM sets").fetchone()[0] == 0 and
                check.execute("SELECT count(*) FROM q").fetchone()[0] == 0 and
                check.execute("SELECT count(*) FROM u").fetchone()[0] == 0 and
                check.execute("SELECT count(*) FROM f WHERE f MATCH ?", ('"new beta"',)).fetchone()[0] == 0
            )
            check.close()
            return replacement_ok and deletion_ok, "replacement=%s; dropped missing set=%s" % (replacement_ok, deletion_ok)
    finally:
        store.PATH, store._CON = old_path, old_con
        store.api.set_list, store.api.pages, store.api.counts = old_set_list, old_pages, old_counts
        if old_env is None:
            os.environ.pop("QBR_DB", None)
        else:
            os.environ["QBR_DB"] = old_env


def live_answer_units(name, category=None, difficulty_range=None):
    """Count matching answerable units in live QBR results, including bonus parts.

    Search for the required surname first so answerlines that take the full name
    as an alternate are returned too, then parse/filter the complete answerline.
    """
    found = set()
    want = fold(name)
    params = {"queryString": name.split()[-1], "questionType": "all", "searchType": "answer",
              }
    if category == "Visual Fine Arts":
        params.update(categories="Fine Arts", subcategories="Visual Fine Arts")
    difficulties = list(difficulty_range) if difficulty_range is not None else [None]
    for difficulty in difficulties:
        query = dict(params)
        if difficulty is not None:
            query["difficulties"] = difficulty
        rows = api.rows(**query)
        for q in rows:
            qid = q.get("_id")
            if q.get("_kind") == "T":
                ans = parse_answer(q.get("answer_sanitized") or q.get("answer") or "", q.get("answer") or "")
                if takes(ans["accepts"], want) or any(near(a, want) for a in ans["accepts"]):
                    found.add((qid, 0))
                continue
            answers = q.get("answers_sanitized") or []
            formatted = q.get("answers") or []
            for i, answer in enumerate(answers):
                raw = formatted[i] if i < len(formatted) else ""
                parsed = parse_answer(answer or "", raw or "")
                if takes(parsed["accepts"], want) or any(near(a, want) for a in parsed["accepts"]):
                    found.add((qid, i + 1))
    tossups = sum(part == 0 for _, part in found)
    bonuses = sum(part != 0 for _, part in found)
    return tossups, bonuses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-only", action="store_true",
                        help="check mirror totals and search counts; skip answer/profile checks during parser/profile work")
    args = parser.parse_args()

    try:
        con = store.db()
    except Exception as e:
        report("open read-only mirror", False, repr(e))
        return 1

    failures = 0

    try:
        local = mirror_question_counts(con)
        live = api.counts()
        if not report("global mirror totals", local == live, "mirror=%s live=%s" % (local, live)):
            failures += 1
    except Exception as e:
        if not report("global mirror totals", False, repr(e)):
            failures += 1

    try:
        sets = con.execute("SELECT name, tossups, bonuses FROM sets WHERE standard=1 "
                           "ORDER BY year DESC, name LIMIT 3").fetchall()
        if not sets:
            if not report("set count checks", False, "no standard sets in the mirror"):
                failures += 1
        else:
            for row in sets:
                name = row["name"]
                local = mirror_question_counts(con, " WHERE set_name=?", (name,))
                summary = (row["tossups"], row["bonuses"])
                live = api.counts(setName=name)
                ok = local == summary == live
                if not report("set counts: %s" % name, ok,
                              "mirror=%s set-row=%s live=%s" % (local, summary, live)):
                    failures += 1
    except Exception as e:
        if not report("set count checks", False, repr(e)):
            failures += 1

    for phrase, category, api_filters in SEARCH_CASES:
        try:
            live = api.counts(queryString=phrase, questionType="all", searchType="question",
                              exactPhrase="true", **api_filters)
            local = clue_search(phrase, cat=category, scope="clue", mode="phrase", n=0)
            remote_total = sum(live)
            local_total = local["questions"]
            tolerance = max(5, int(math.ceil(remote_total * 0.15)))
            delta = abs(local_total - remote_total)
            if not report("search count: %s" % phrase, delta <= tolerance,
                          "mirror=%d live=%d delta=%d allowed=%d" %
                          (local_total, remote_total, delta, tolerance)):
                failures += 1
        except Exception as e:
            if not report("search count: %s" % phrase, False, repr(e)):
                failures += 1

    for phrase, category, api_filters in SEARCH_DIAGNOSTICS:
        try:
            live = api.counts(queryString=phrase, questionType="all", searchType="question",
                              exactPhrase="true", **api_filters)
            local = clue_search(phrase, cat=category, scope="clue", mode="phrase", n=0)
            remote_total = sum(live)
            local_total = local["questions"]
            delta = abs(local_total - remote_total)
            tolerance = max(5, int(math.ceil(remote_total * 0.15)))
            if delta > tolerance:
                print("WARN: search count diagnostic: %s -- mirror=%d live=%d delta=%d; "
                      "review tokenization scope (hyphenated forms are FTS phrase hits)." %
                      (phrase, local_total, remote_total, delta))
            else:
                report("search count diagnostic: %s" % phrase, True,
                       "mirror=%d live=%d delta=%d" % (local_total, remote_total, delta))
        except Exception as e:
            if not report("search count diagnostic: %s" % phrase, False, repr(e)):
                failures += 1

    for label, sanitized, formatted, required, forbidden in ANSWER_LINE_REGRESSIONS:
        try:
            parsed = parse_answer(sanitized, formatted)
            accepts = set(parsed["accepts"])
            missing = sorted(set(required) - accepts)
            leaked = sorted(set(forbidden) & accepts)
            ok = not missing and not leaked
            if not report("answer parser: %s" % label, ok,
                          "missing=%s; false accepts=%s" % (missing, leaked)):
                failures += 1
        except Exception as e:
            if not report("answer parser: %s" % label, False, repr(e)):
                failures += 1

    for qid, citation in SENTENCE_REGRESSIONS:
        try:
            row = con.execute("SELECT u.text, u.lead FROM u JOIN q ON q.qid=u.qid WHERE q.id=? LIMIT 1",
                              (qid,)).fetchone()
            found = []
            if row:
                for field in (row["lead"], row["text"]):
                    found.extend(s["s"] for s in sentences(field or ""))
            needle = fold(citation)
            matching = [s for s in found if needle in fold(s)]
            if not report("sentence boundary: %s" % qid, bool(matching),
                          "citation=%r in one sentence=%s" % (citation, bool(matching))):
                failures += 1
        except Exception as e:
            if not report("sentence boundary: %s" % qid, False, repr(e)):
                failures += 1

    if args.core_only:
        print("SKIP: answer and profile checks; run the full selftest after reparsing and profile readiness.")
        print("Selftest complete: %d failure(s)." % failures)
        return 1 if failures else 0

    try:
        live = live_answer_units(MALEVICH, category="Visual Fine Arts", difficulty_range=range(4, 11))
        mirror_rows = search_answered(MALEVICH, cat="Visual Fine Arts", diff="4-10")
        mirror = (sum(r["kind"] == "T" for r in mirror_rows), sum(r["kind"] == "B" for r in mirror_rows))
        if not report("live Malevich VFA 4+ benchmark", live == MALEVICH_VFA_BENCHMARK,
                      "live=%s expected=%s (tossups, bonus parts)" % (live, MALEVICH_VFA_BENCHMARK)):
            failures += 1
        if not report("Malevich VFA 4+ mirror counts", mirror == live,
                      "mirror=%s live=%s (tossups, bonus parts)" % (mirror, live)):
            failures += 1
        live_all = live_answer_units(MALEVICH)
        mirror_all_rows = search_answered(MALEVICH)
        mirror_all = (sum(r["kind"] == "T" for r in mirror_all_rows),
                      sum(r["kind"] == "B" for r in mirror_all_rows))
        if not report("live Malevich global benchmark", live_all == MALEVICH_ALL_BENCHMARK,
                      "live=%s expected=%s (tossups, bonus parts)" % (live_all, MALEVICH_ALL_BENCHMARK)):
            failures += 1
        if not report("Malevich global mirror counts", mirror_all == live_all,
                      "mirror=%s live=%s (tossups, bonus parts)" % (mirror_all, live_all)):
            failures += 1
    except Exception as e:
        if not report("Malevich answer checks", False, repr(e)):
            failures += 1

    try:
        adams = search_answered("Adams")
        john = {r["akey"] for r in adams if "john adams" in fold(r["main"])}
        samuel = {r["akey"] for r in adams if "samuel adams" in fold(r["main"])}
        ok = bool(john and samuel and john.isdisjoint(samuel))
        if not report("Adams answer separation", ok,
                      "John keys=%s; Samuel keys=%s" % (sorted(john), sorted(samuel))):
            failures += 1
    except Exception as e:
        if not report("Adams answer separation", False, repr(e)):
            failures += 1

    try:
        gaudi = search_answered("Antoni Gaudi")
        maternal = [r for r in gaudi if "antoni gaudi i cornet" in fold(r["akey"])]
        ok = near("antoni gaudi", "antoni gaudi i cornet") and takes(
            ["antoni gaudi i cornet"], "antoni gaudi") and bool(maternal)
        if not report("Gaudi maternal surname match", ok,
                      "near=%s; takes=%s; matching answer units=%d" %
                      (near("antoni gaudi", "antoni gaudi i cornet"),
                       takes(["antoni gaudi i cornet"], "antoni gaudi"), len(maternal))):
            failures += 1
    except Exception as e:
        if not report("Gaudi maternal surname match", False, repr(e)):
            failures += 1

    try:
        profile_cases = (
            ("Kazimir Malevich", ("black square",)),
            ("Immanuel Kant", ("critique of pure reason",)),
            ("Hagia Sophia", ("anthemius", "isidore")),
            ("Jane Austen", ("pride and prejudice", "sense and sensibility")),
        )
        for name, wanted in profile_cases:
            result = clue_profile(name, top=5)
            rows = result.get("things", [])
            thing_folds = [fold(t.get("thing", "")) for t in rows]
            hits = [x for x in wanted if any(x in thing for thing in thing_folds)]
            bad_titles = ([x for x in wanted if not any(fold(t.get("thing", "")) == x and t.get("kind") == "title"
                                                           for t in rows)] if name == "Jane Austen" else [])
            ok = bool(result.get("found") and hits) and not bad_titles
            if not report("profile top clues: %s" % name, ok,
                          "top=%s wanted=%s bad-title-kind=%s" % (thing_folds, list(wanted), bad_titles)):
                failures += 1
    except Exception as e:
        if not report("profile smoke tests", False, repr(e)):
            failures += 1

    try:
        unrelated = verify_clue("DNA polymerase", "Shakespeare wrote Hamlet.")
        relevant = verify_clue(
            "DNA polymerase",
            "Arthur Kornberg discovered this enzyme, whose Klenow fragment lacks 5-prime to 3-prime exonuclease activity.")
        ok = not unrelated["ok"] and relevant["ok"]
        if not report("clue validator rejects unrelated clue and accepts target clue", ok,
                      "unrelated=%s; Kornberg/Klenow=%s" % (unrelated["ok"], relevant["ok"])):
            failures += 1
    except Exception as e:
        if not report("clue validator regression", False, repr(e)):
            failures += 1

    try:
        dotted_source = "c\u00b7A\u00b7M\u00b7P L\u00b7C\u00b73 Ruv\u00b7C H\u00b7N\u00b7H A\u00b7T\u00b7G"
        dotted = fold(dotted_source)
        anki_dotted = anki_module._note_fold(dotted_source)
        bad_title_suffix = takes(["orfeo ed euridice"], "euridice")
        good_surname = takes(["kazimir severinovich malevich"], "malevich")
        euridice_rows = search_answered("Euridice", cat="Fine Arts")
        wrong_work = sorted({fold(r["main"]) for r in euridice_rows if fold(r["main"]) == "orfeo ed euridice"})
        joined = {"camp", "lc3", "ruvc", "hnh", "atg"} <= set(anki_dotted.split())
        ok = (dotted == "c a m p l c 3 ruv c h n h a t g" and joined and
              not bad_title_suffix and good_surname and not wrong_work)
        if not report("title suffix matching and dotted acronym normalization", ok,
                      "text.fold=%r; Anki-fold=%r; Orfeo suffix match=%s; Malevich surname match=%s; wrong work lines=%s" %
                      (dotted, anki_dotted, bad_title_suffix, good_surname, wrong_work)):
            failures += 1
    except Exception as e:
        if not report("title suffix matching and dotted acronym normalization", False, repr(e)):
            failures += 1

    try:
        euridice = clue_profile("Euridice", cat="Fine Arts", top=1000)
        sonata = clue_profile("Sonata pian' e forte", cat="Fine Arts", exact=True, top=1000)
        christmas = clue_profile("Christmas Concerto, Op. 6", cat="Fine Arts", top=1000)
        euridice_bad = [r[0] for r in euridice.get("lines", [])
                        if fold(r[0]) == "orfeo ed euridice"]
        sonata_bad = [r[0] for r in sonata.get("lines", [])
                      if fold(r[0]) in ("piano and forte", "piano forte")]
        ok = (not euridice_bad and not sonata_bad and christmas.get("found") and
              christmas.get("questions", 0) >= 4)
        if not report("work answerline disambiguation and catalogue suffix fallback", ok,
                      "Euridice wrong lines=%s; Sonata exact wrong lines=%s; Christmas Concerto=%s questions" %
                      (euridice_bad, sonata_bad, christmas.get("questions"))):
            failures += 1
    except Exception as e:
        if not report("work answerline disambiguation and catalogue suffix fallback", False, repr(e)):
            failures += 1

    try:
        bad_phrase_cases = (
            ("Missa L'homme arme", "Fine Arts",
             {'word "caput', 'song "L\'homme Arme'}),
            ("Action", "Physics", {'according to Hamilton', "Hamilton's principle states", 'abbreviated" form'}),
            ("Capacitors", "Physics", {"store electric"}),
            ("Fermions", "Physics", {"occupy the same quantum"}),
            ("Heisenberg's uncertainty principle", "Physics",
             {"product of the standard", "p is greater", "position and momentum cannot"}),
            ("Karl Schwarzschild", "Physics", {"horizon of a black"}),
            ("Body size", "Biology", {"Allometry is the study"}),
            ("Cas nucleases", "Biology", {"One-vector"}),
        )
        failures_by_answer = {}
        for answer, category, forbidden in bad_phrase_cases:
            result = clue_profile(answer, cat=category, top=1000)
            present = sorted(fold(t["thing"]) for t in result.get("things", [])
                             if fold(t["thing"]) in {fold(x) for x in forbidden})
            if present:
                failures_by_answer[answer] = present
        if not report("calibration fragments and malformed quote candidates are filtered",
                      not failures_by_answer, "remaining bad candidates=%s" % failures_by_answer):
            failures += 1
    except Exception as e:
        if not report("calibration fragment filtering", False, repr(e)):
            failures += 1

    try:
        original_call, original_cache = anki_module._call, anki_module.CACHE
        note = {
            "noteId": 9910001, "modelName": "QB Cloze", "tags": [],
            "fields": {
                "Text": {"order": 0, "value": "This note discusses c\u00b7A\u00b7M\u00b7P, L\u00b7C\u00b73, and Ruv\u00b7C."},
                "Clue 1": {"order": 1, "value": "Arthur Kornberg"},
                "Answerline": {"order": 2, "value": "DNA polymerase"},
            },
        }
        try:
            with tempfile.TemporaryDirectory() as tmp:
                anki_module.CACHE = os.path.join(tmp, "anki_index.json")
                def fake_call(action, **params):
                    if action == "findNotes":
                        return [note["noteId"]]
                    if action == "notesInfo":
                        return [note]
                    raise AssertionError("unexpected AnkiConnect action: %s" % action)
                anki_module._call = fake_call
                idx = anki_module.build()
        finally:
            anki_module._call, anki_module.CACHE = original_call, original_cache
        answer_status = anki_module.have(idx, "DNA polymerase")
        camp_status = anki_module.have(idx, "cAMP", target_names=("DNA polymerase",))
        lc3_status = anki_module.have(idx, "LC3", target_names=("DNA polymerase",))
        ruvc_status = anki_module.have(idx, "RuvC", target_names=("DNA polymerase",))
        ok = (answer_status == "card" and camp_status == "on-note" and
              lc3_status == "on-note" and ruvc_status == "on-note")
        if not report("QB Cloze Answerline and dotted acronyms index as on-note",
                      ok, "Answerline=%s; cAMP=%s; LC3=%s; RuvC=%s" %
                      (answer_status, camp_status, lc3_status, ruvc_status)):
            failures += 1
    except Exception as e:
        if not report("QB Cloze Anki index regression", False, repr(e)):
            failures += 1

    try:
        original_call = anki_module._call
        note = {
            "noteId": 9910002, "modelName": "Work", "tags": [],
            "fields": {
                "Title": {"order": 0, "value": "Ordo Virtutum"},
                "Composer": {"order": 1, "value": "Hildegard of Bingen"},
                "Clue 1": {"order": 2, "value": "porrigat"},
            },
        }
        try:
            def fake_call(action, **params):
                if action == "findNotes":
                    return [note["noteId"]]
                if action == "notesInfo":
                    return [note]
                raise AssertionError("unexpected AnkiConnect action: %s" % action)
            anki_module._call = fake_call
            brief = anki_module.brief_notes("AFA", cat="Fine Arts", top=20)
        finally:
            anki_module._call = original_call
        row = next(x for x in brief if x["nid"] == note["noteId"])
        leaked = [x["thing"] for x in row["stock"] if fold(x["thing"]) == "hildegard"]
        recorded = [x["thing"] for x in row["suppressed"] if fold(x["thing"]) == "hildegard"]
        ok = not leaked and bool(recorded) and any(x["on_note"] for x in row["stock"])
        if not report("work briefing uses exact answerlines and suppresses shown creator",
                      ok, "Hildegard in stock=%s; suppressed=%s; suggestions=%s" %
                      (leaked, recorded, [x["thing"] for x in row["stock"]])):
            failures += 1
    except Exception as e:
        if not report("work briefing creator-leak regression", False, repr(e)):
            failures += 1

    try:
        result = clue_profile("photoelectric effect", cat="Physics", top=1000, sort="spec")
        rank = {fold(t["thing"]): i for i, t in enumerate(result.get("things", []))}
        wanted = ("heinrich hertz", "stopping potential", "maximum kinetic energy")
        missing = [x for x in wanted + ("albert einstein",) if x not in rank]
        excluded = [x for x in ("electrons", "light") if x in rank]
        ok = not missing and not excluded and all(rank[x] < rank["albert einstein"] for x in wanted)
        if not report("physics specificity gold ranking", ok,
                      "ranks=%s; missing=%s; excluded=%s" %
                      ({x: rank.get(x) for x in wanted + ("albert einstein",)}, missing, excluded)):
            failures += 1
    except Exception as e:
        if not report("physics specificity gold ranking", False, repr(e)):
            failures += 1

    try:
        result = clue_profile("photoelectric effect", cat="Physics", top=1000, sort="spec")
        einstein = next(t for t in result["things"] if fold(t["thing"]) == "albert einstein")
        answer_rows = search_answered("photoelectric effect", cat="Physics")
        answer_by_uid = {r["uid"]: r for r in answer_rows}
        expr = find_module.CLUE + '("einstein" OR "albert einstein")'
        units = {r[0] for r in store.db().execute("SELECT rowid FROM f WHERE f MATCH ?", (expr,))}
        mine = {u: answer_by_uid[u] for u in units if u in answer_by_uid}
        wsql, wargs = find_module.where("Physics")
        mention_names = result["names"]
        mention_expr = find_module.CLUE + "(" + " OR ".join('"%s"' % n for n in mention_names) + ")"
        mention_rows = store.db().execute(
            "SELECT u.uid FROM f JOIN u ON u.uid=f.rowid WHERE f MATCH ?%s ORDER BY u.year DESC LIMIT ?" % wsql,
            [mention_expr] + wargs + [clue_module.CAP_MENTIONS + len(answer_rows)]).fetchall()
        mentioned_uids = {r[0] for r in mention_rows if r[0] not in answer_by_uid}
        total_units = store.db().execute("SELECT count(*) FROM u").fetchone()[0]
        expected_n = len({r["qid"] for r in mine.values()})
        expected_tied = sum(u in answer_by_uid or u in mentioned_uids for u in units) / max(1, len(units))
        expected_lift = (len(mine) / max(1, len(answer_rows))) / (len(units) / total_units)
        ok = (einstein["all"] == len(units) and einstein["n"] == expected_n and
              math.isclose(einstein["tied"], expected_tied, rel_tol=1e-9, abs_tol=1e-9) and
              math.isclose(einstein["lift"], expected_lift, rel_tol=1e-9, abs_tol=1e-9))
        if not report("merged clue statistics and unit-based lift", ok,
                      "reported n/all/tied/lift=%d/%d/%.4f/%.3f; expected=%d/%d/%.4f/%.3f" %
                      (einstein["n"], einstein["all"], einstein["tied"], einstein["lift"],
                       expected_n, len(units), expected_tied, expected_lift)):
            failures += 1
    except Exception as e:
        if not report("merged clue statistics and unit-based lift", False, repr(e)):
            failures += 1

    try:
        result = clue_profile("Hagia Sophia", cat="Architecture", top=1000)
        foils = {fold(f["answer"]) for f in result.get("foils", [])}
        forbidden = sorted(foils & {"the burial of count orgaz", "john the baptist"})
        if not report("category-scoped confusable foils", not forbidden,
                      "foils=%s; out-of-category=%s" % (sorted(foils), forbidden)):
            failures += 1
    except Exception as e:
        if not report("category-scoped confusable foils", False, repr(e)):
            failures += 1

    try:
        result = clue_profile("Jane Austen", top=20)
        previous = clue_module.CAP_MENTIONS
        try:
            clue_module.CAP_MENTIONS = 0
            capped = clue_profile("Jane Austen", top=20)
        finally:
            clue_module.CAP_MENTIONS = previous
        ok = not result.get("mentioned_truncated") and capped.get("mentioned_truncated") is True
        if not report("mention cap is surfaced", ok,
                      "normal=%s; forced-cap=%s" %
                      (result.get("mentioned_truncated"), capped.get("mentioned_truncated"))):
            failures += 1
    except Exception as e:
        if not report("mention cap is surfaced", False, repr(e)):
            failures += 1

    try:
        result = clue_profile("photoelectric effect", cat="Physics", top=1000, sort="spec")
        planck = next(t for t in result["things"] if fold(t["thing"]) == "planck")
        answer_rows = search_answered("photoelectric effect", cat="Physics")
        by_tossup = {}
        for r in answer_rows:
            if r["kind"] != "T":
                continue
            for s in sentences(r["lead"]) + sentences(r["text"]):
                if " " + planck["key"] + " " in " " + fold(s["s"]) + " ":
                    by_tossup.setdefault(r["qid"], s)
                    break
        expected_power = sum(s["power"] for s in by_tossup.values()) / max(1, len(by_tossup))
        expected_pos = round(statistics.median(s["pos"] for s in by_tossup.values()), 2)
        ok = bool(by_tossup) and planck["power"] == round(expected_power, 2) and planck["pos"] == expected_pos
        if not report("tossup-level power and position", ok,
                      "reported power/pos=%.2f/%.2f; per-tossup=%0.2f/%.2f over %d tossups" %
                      (planck["power"], planck["pos"], expected_power, expected_pos, len(by_tossup))):
            failures += 1
    except Exception as e:
        if not report("tossup-level power and position", False, repr(e)):
            failures += 1

    try:
        result = clue_profile("double-slit experiment", cat="Physics", top=1000)
        bad = sorted(fold(t["thing"]) for t in result.get("things", [])
                     if fold(t["thing"]) in ("performed by thomas young", "conducted by thomas young"))
        if not report("double-slit framing phrases are filtered", not bad,
                      "forbidden phrases=%s" % bad):
            failures += 1
    except Exception as e:
        if not report("double-slit framing phrases are filtered", False, repr(e)):
            failures += 1

    try:
        failed = []
        for line, required, forbidden in PARSER_REGRESSIONS:
            accepts = set(parse_answer(line)["accepts"])
            missing = sorted(set(required) - accepts)
            leaked = sorted(set(forbidden) & accepts)
            if missing or leaked:
                failed.append({"line": line, "missing": missing, "false_accepts": leaked})
        if not report("answer parser regression corpus", not failed,
                      "%d fixtures; failures=%s" % (len(PARSER_REGRESSIONS), failed[:3])):
            failures += 1
    except Exception as e:
        if not report("answer parser regression corpus", False, repr(e)):
            failures += 1

    try:
        flagged = rejected_answers_accepted(con)
        if not report("corpus-wide rejected-answer guard", flagged < 600,
                      "%d/%s answer lines flagged (review candidates, not confirmed errors)" %
                      (flagged, con.execute("SELECT count(*) FROM u WHERE answer LIKE '%do not%' "
                                            "OR answer LIKE '%reject%' OR answer LIKE '%don''t%'").fetchone()[0])):
            failures += 1
    except Exception as e:
        if not report("corpus-wide rejected-answer guard", False, repr(e)):
            failures += 1

    try:
        ok, detail = scratch_store_regressions()
        if not report("scratch mirror replacement and removal", ok, detail):
            failures += 1
    except Exception as e:
        if not report("scratch mirror replacement and removal", False, repr(e)):
            failures += 1

    try:
        title = "String Quartet in C major, Op. 54, No. 2, Hoboken III:57"
        result = clue_profile(title, cat="Fine Arts", top=5)
        if not report("colons and punctuation in a work title do not crash FTS5", isinstance(result, dict),
                      "profile returned found=%s questions=%s" %
                      (result.get("found"), result.get("questions"))):
            failures += 1
    except Exception as e:
        if not report("colons and punctuation in a work title do not crash FTS5", False, repr(e)):
            failures += 1

    try:
        extracted = things("Canon alla (*) Ottava", "<i>Canon alla (*) Ottava</i>")
        bad = [name for kind, name in extracted if "(*)" in name or fold(name) == "alla ottava"]
        if not report("power mark is excluded from italicized title extraction", not bad,
                      "extracted=%s; bad=%s" % (extracted, bad)):
            failures += 1
    except Exception as e:
        if not report("power mark is excluded from italicized title extraction", False, repr(e)):
            failures += 1

    try:
        from . import __main__ as cli_module
        original_profile = clue_module.profile
        original_brief = anki_module.brief_notes
        fake = {
            "found": True, "suggest": [], "name": "Selftest answer", "questions": 1,
            "tossups": 1, "bonuses": 0, "sets": 1, "first": 2020, "last": 2020,
            "mentioned": 0, "mentioned_truncated": False, "anki": None,
            "lines": [], "difficulty": {}, "categories": {"Science": 1},
            "things": [{"n": 1, "m": 0, "tied": 1.0, "dmin": 7, "dmax": 7,
                        "where": "early", "power": 0, "anki": None, "thing": "Kornberg",
                        "kind": "name", "example": "", "source": ""}],
            "elsewhere": [], "foils": [], "under": [],
        }
        profile_args = argparse.Namespace(
            name="Selftest answer", exact=False, exclude=[], top=5, anki=False,
            pyramid=False, spec=False, cat=None, diff=None, year=None, sets=None,
            kind=None, json=False, examples=0,
        )
        brief_args = argparse.Namespace(deck="__qbr_selftest_no_match__", tier=None,
                                        title=None, cat=None, top=12, json=False)
        try:
            clue_module.profile = lambda *args, **kwargs: fake
            anki_module.brief_notes = lambda *args, **kwargs: []
            profile_out, brief_out = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(profile_out):
                cli_module.cmd_profile(profile_args)
            with contextlib.redirect_stdout(brief_out):
                cli_module.cmd_brief(brief_args)
        finally:
            clue_module.profile = original_profile
            anki_module.brief_notes = original_brief
        profile_text, brief_text = profile_out.getvalue(), brief_out.getvalue()
        header_ok = "%%" not in profile_text and "n  +m" in profile_text
        empty_message_ok = "no notes matched" in brief_text
        if not report("profile and empty-brief CLI output", header_ok and empty_message_ok,
                      "profile_header_ok=%s; empty_brief_message=%s" % (header_ok, empty_message_ok)):
            failures += 1
    except Exception as e:
        if not report("profile and empty-brief CLI output", False, repr(e)):
            failures += 1

    print("Selftest complete: %d failure(s)." % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
