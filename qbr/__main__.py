# -*- coding: utf-8 -*-
"""The command line: py -3.9 -m qbr <command> ...   (run from C:\\QB\\stockfisher)

    profile "Kazimir Malevich"          the stock clues for an answer, counted
    search "zero of form" -c vfa        clue text; also "a b" AND/OR/NOT, supremat*, NEAR(a b, 10), ans:malevich, --re
    who "zero of form"                  which answers a clue points to (is it unique?)
    top -c architecture -n 100          the frequency list for a category; --rising for what is trending
    fact "Bury St. Edmunds|eel"         fact check: sentences holding the keyword in questions holding the phrase
    like "a white fish obscures ..."    clues worded like this one
    sets "ACF Nationals"                sets in the mirror;  set "2026 ACF Nationals" -c vfa  lists its questions
    show <id>                           one whole question
    sync                                update the mirror;  status  says how fresh it is
    sql "SELECT ..."                    anything else, read-only

Filters on most commands: -c category   -d difficulty (7, 7-9, hs, college)   -y year (2018-, 2015-2020)
                          -s part of a set name   -t tossup|bonus        --json prints the raw result
"""
import argparse
import json
import sys
import time

from . import find, store
from .text import DOTS


def _filters(p):
    p.add_argument("-c", "--cat", help="category, subcategory or alternate subcategory; commas for several")
    p.add_argument("-d", "--diff", help="difficulty: 7, 7-9, 6,7, ms, hs, college, open")
    p.add_argument("-y", "--year", help="2026, 2018-, 2015-2020")
    p.add_argument("-s", "--set", dest="sets", help="part of a set name")
    p.add_argument("-t", "--type", dest="kind", help="tossup or bonus")
    p.add_argument("--json", action="store_true", help="print the raw result as JSON")


def _kw(a):
    return {k: getattr(a, k) for k in ("cat", "diff", "year", "sets", "kind") if getattr(a, k, None)}


def _tag(r):
    cat = r.get("alt") or r.get("subcategory") or r.get("category") or ""
    part = "T" if r["kind"] == "T" else "B%d" % r["part"]
    return "%s | d%s | %s | %s" % (r["set_name"], r["difficulty"], cat, part)


def _pct(x):
    return "%3.0f%%" % (100 * x)


def _answers(groups, n=8):
    return "  ".join("%s %d" % (g["answer"], g["n"]) for g in groups[:n])


def cmd_search(a):
    mode = "all" if a.all else "any" if a.any else "auto"
    r = find.search(a.query, scope=a.scope, mode=mode, regex=a.re, sort=a.sort, n=a.n, offset=a.offset, **_kw(a))
    if a.json:
        return r
    print('%d units in %d questions   [%s]' % (r["units"], r["questions"], r["match"]))
    if r["answers"]:
        print("under: " + _answers(r["answers"]) + ("  ... %d answer lines" % len(r["answers"]) if len(r["answers"]) > 8 else ""))
    for i, h in enumerate(r["hits"], a.offset + 1):
        print("\n%2d. %s  ->  %s   (uid %d)" % (i, _tag(h), h["main"], h["uid"]))
        if a.full:
            if h["lead"]:
                print("    " + h["lead"])
            print("    " + h["text"])
            print("    ANSWER: " + h["answer"])
        else:
            for s in h["sentences"]:
                print("    " + s["s"])


def cmd_who(a):
    r = find.who(a.phrase, mode="all" if a.all else "auto", **_kw(a))
    if a.json:
        return r
    if not r:
        return print("nothing holds %r" % a.phrase)
    print("%d questions hold it, under %d answer lines" % (sum(g["n"] for g in r), len(r)))
    print("   n  share  years       answer")
    for g in r[:a.n]:
        print("%4d  %s  %s-%s   %s%s" % (g["n"], _pct(g["share"]), g["first"], g["last"], g["answer"],
                                        "   (also: %s)" % ", ".join(g["also"][:3]) if g["also"] else ""))


def cmd_profile(a):
    from .clues import profile
    sort = "pyramid" if getattr(a, "pyramid", False) else "spec" if getattr(a, "spec", False) else "n"
    p = profile(a.name, exact=a.exact, exclude=a.exclude or (), top=a.top, anki=a.anki, sort=sort, **_kw(a))
    if a.json:
        return p
    if not p["found"]:
        print("%r is neither an answer line nor named in any question." % a.name)
        if p["suggest"]:
            print("closest answer lines: " + "  ".join("%s %d" % s for s in p["suggest"]))
        return
    if a.anki and p.get("anki_stale"):
        print("(" + p["anki_stale"] + ")", file=sys.stderr)
    mark = "   [anki: %s]" % (p["anki"] or "no card") if a.anki else ""
    if not p["questions"]:
        print("%s   never an answer line; named in %d questions%s" % (p["name"], p["mentioned"], mark))
    else:
        print("%s   %d tossups, %d bonus parts (%d questions, %d sets, %s-%s); named in %d%s other questions%s" % (
            p["name"], p["tossups"], p["bonuses"], p["questions"], p["sets"], p["first"], p["last"], p["mentioned"],
            "+" if p.get("mentioned_truncated") else "", mark))
        print("answer lines: " + "  ".join("%s %d" % l for l in p["lines"]))
        print("difficulty:   " + "  ".join("%s: %d" % (DOTS.get(d, d), n) for d, n in p["difficulty"].items()))
        print("in:           " + "  ".join("%s %d" % c for c in p["categories"].items()))
        cats = sorted(p["categories"].values(), reverse=True)
        if len(cats) > 1 and cats[1] >= 0.25 * p["questions"] and len(p["lines"]) > 1:
            print("              (these may be two different answers under one name: narrow with -c, --not or --exact)")

    def table(rows, examples):
        print("    n  +m  tied  levels  where     %sclue" % ("anki       " if a.anki else ""))
        for i, t in enumerate(rows):
            lev = "%s-%s" % (t["dmin"], t["dmax"]) if t["dmin"] else "  -"
            pwr = "*" if t.get("power", 0) >= 0.5 else " "
            print("  %3d %3d  %s  %-6s  %-8s%s %s%s%s" % (
                t["n"], t["m"], _pct(t["tied"]), lev, t["where"], pwr, ("%-10s " % (t.get("anki") or "-")) if a.anki else "",
                t["thing"], "" if t["kind"] == "name" else "  (%s)" % t["kind"]))
            if i < examples and t["example"]:
                print("                                    > %s  [%s]" % (t["example"], t["source"]))

    if p["things"]:
        print("\nSTOCK CLUES  (n = questions on this answer that use it; +m = other questions that use it of this answer;")
        print("              tied = share of everything holding it that involves this answer; * = >=50% power)")
        table(p["things"], a.examples)
    if p["elsewhere"]:
        print("\nSAID OF IT IN OTHER ANSWERS' QUESTIONS" if not p["questions"] else
              "\nSAID OF IT ONLY IN OTHER ANSWERS' QUESTIONS")
        table(p["elsewhere"], a.examples)
    if p.get("foils"):
        print("\nCONFUSABLE / SHARED-CLUE ANSWERS: " + "  ".join(
            "%s (%s)" % (f["answer"], ", ".join(f["shared"][:3])) for f in p["foils"][:6]))
    if p["under"]:
        print("\nNAMED IN QUESTIONS ON: " + "  ".join(
            "%s %d%s" % (g["answer"], g["n"], " [%s]" % (g.get("anki") or "-") if a.anki else "") for g in p["under"]))


def cmd_top(a):
    r = find.top(n=0 if a.missing else a.n, sort="rising" if a.rising else "n", recent=a.recent, min_n=a.min, **_kw(a))
    if a.anki or a.missing:
        from . import anki
        idx = anki.index()
        if idx.get("stale"):
            print("(" + idx["stale"] + ")", file=sys.stderr)
        for g in r:
            g["anki"] = anki.have(idx, g["akey"], g["also"])
        if a.missing:
            r = [g for g in r if g["anki"] not in ("card", "suspended")][:a.n]
    if a.json:
        return r
    print("       n  toss bonus  level  years       last %dy  %sanswer" % (a.recent, "anki       " if a.anki or a.missing else ""))
    for i, g in enumerate(r, 1):
        print("%3d %4d  %4d %5d   %4.1f  %s-%s  %7d  %s%s%s" % (
            i, g["n"], g["tossups"], g["bonuses"], g["difficulty"], g["first"], g["last"], g["recent"],
            ("%-10s " % (g["anki"] or "-")) if a.anki or a.missing else "", g["answer"],
            "   (also: %s)" % ", ".join(g["also"][:3]) if g["also"] else ""))


def cmd_fact(a):
    out = []
    for arg in a.checks:
        phrase, _, kw = arg.partition("|")
        r = find.fact(phrase, kw or None, n=a.n, **_kw(a))
        out.append(dict(r, check=arg))
        if not a.json:
            print("== %s | tossups %d bonuses %d" % (arg, r["tossups"], r["bonuses"]))
            for s, y, ans, sent in r["sentences"]:
                print("   [%s -> %s] %s" % (s, ans, sent))
            if not r["sentences"]:
                print("   (no sentence holds %s)" % ("the keyword in those questions" if kw else "it"))
    return out if a.json else None


def cmd_like(a):
    r = find.like(a.text, n=a.n, **_kw(a))
    if a.json:
        return r
    for score, s, y, ans, sent in r:
        print("%s  [%s -> %s]\n      %s" % (_pct(score), s, ans, sent))


def cmd_sets(a):
    r = find.sets(a.pattern, a.year, a.diff)
    if a.json:
        return r
    for s in r[:a.n]:
        print("%-52s d%-2s  %4d tossups %4d bonuses" % (s["name"][:52], s["difficulty"], s["tossups"], s["bonuses"]))
    print("%d sets" % len(r))


def cmd_set(a):
    hit = [s["name"] for s in find.sets(a.name)]
    name = a.name if a.name in hit else (hit[0] if len(hit) == 1 else None)
    if not name:
        return print("which set? " + ("; ".join(hit[:20]) if hit else "no set name holds %r" % a.name))
    r = find.packet(name, cat=a.cat, kind=a.kind, number=a.packet)
    if a.json:
        return r
    print("%s: %d units" % (name, len(r)))
    for u in r:
        print("%3s.%-2s %s  %-22s %s" % (u["packet"], u["number"], "T " if u["kind"] == "T" else "B%d" % u["part"],
                                         (u["alt"] or u["subcategory"] or "")[:22], u["main"]))
        if a.full:
            print("        " + (u["lead"] + " | " if u["lead"] else "") + u["text"])


def cmd_show(a):
    r = find.show(a.ref)
    if a.json:
        return r
    if not r:
        return print("no question %r" % a.ref)
    q = r["question"]
    print("%s | packet %s (%s) question %s | d%s | %s / %s%s | id %s" % (
        q["set_name"], q["packet"], q["packet_name"], q["number"], q["difficulty"], q["category"], q["subcategory"],
        " / " + q["alt"] if q["alt"] else "", q["id"]))
    f = r["formatted"]
    if q["kind"] == "T":
        print("\n" + (f["q"] if a.html else r["units"][0]["text"]))
        print("ANSWER: " + (f["a"] if a.html else r["units"][0]["answer"]))
    else:
        print("\n" + (f["l"] if a.html else r["units"][0]["lead"]))
        for i, u in enumerate(r["units"]):
            print("[%d] %s\nANSWER: %s" % (i + 1, f["p"][i] if a.html else u["text"], f["a"][i] if a.html else u["answer"]))


def cmd_sync(a):
    if a.reparse:
        return store.reparse() and None
    store.sync(full=a.full, years=a.years)


def cmd_status(a):
    con = store.db()
    c, when = store.meta("counts"), store.meta("synced")
    r = {"path": store.PATH, "tossups": c["tossups"], "bonuses": c["bonuses"],
         "units": con.execute("SELECT count(*) FROM u").fetchone()[0],
         "sets": con.execute("SELECT count(*) FROM sets").fetchone()[0],
         "newest": [x[0] for x in con.execute("SELECT name FROM sets ORDER BY synced DESC, year DESC LIMIT 5")],
         "synced": time.strftime("%Y-%m-%d %H:%M", time.localtime(when)), "days": (time.time() - when) / 86400}
    if a.json:
        return r
    print("%s\n%d tossups, %d bonuses, %d units, %d sets; last synced %s (%.0f days ago)" % (
        r["path"], r["tossups"], r["bonuses"], r["units"], r["sets"], r["synced"], r["days"]))


def cmd_sql(a):
    rows = [dict(r) for r in store.db().execute(a.statement)]
    if a.json:
        return rows
    for r in rows[:a.n]:
        print(" | ".join(str(v)[:a.width] for v in r.values()))
    if len(rows) > a.n:
        print("... %d rows" % len(rows))


def cmd_brief(a):
    from .anki import brief_notes
    rows = brief_notes(a.deck, tier=a.tier, pattern=a.title, cat=a.cat, top=a.top)
    if a.json:
        return rows
    if not rows:
        return print("no notes matched deck=%r%s%s" % (
            a.deck, " tier=%s" % a.tier if a.tier else "", " title=%r" % a.title if a.title else ""))
    for u in rows:
        print("== %s | nid %d | %d questions (%d tossups)" % (u["title"], u["nid"], u["questions"], u["tossups"]))
        if u.get("answerlines"):
            print("   QBR answerlines: " + ", ".join("%s (%d)" % (a, n) for a, n in u["answerlines"]))
        elif not u["questions"]:
            print("   QBR: no matching answerline")
        for k, v in u["have"].items():
            print("   %s: %s" % (k, v))
        if u.get("suppressed"):
            print("   suppressed (creator already shown): " +
                  ", ".join(x["thing"] for x in u["suppressed"]))
        if u["stock"]:
            print("   stock: " + ", ".join("%s %d%s" % (s["thing"], s["n"], " [on-note]" if s["on_note"] else "")
                                           for s in u["stock"]))
        if u["missing"]:
            print("   missing: " + ", ".join(u["missing"][:8]))


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="py -3.9 -m qbr", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("search", help="search clue text")
    p.add_argument("query")
    p.add_argument("-n", type=int, default=10)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--all", action="store_true", help="all the words, anywhere in the unit")
    p.add_argument("--any", action="store_true", help="any of the words")
    p.add_argument("--re", action="store_true", help="the query is a regular expression (slower: a full scan)")
    p.add_argument("--in", dest="scope", default="clue", choices=["clue", "answer", "all"])
    p.add_argument("--sort", default="auto", choices=["auto", "new", "old", "hard", "easy", "rank"])
    p.add_argument("--full", action="store_true", help="print whole questions")
    _filters(p)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("who", help="which answers a clue points to")
    p.add_argument("phrase")
    p.add_argument("-n", type=int, default=15)
    p.add_argument("--all", action="store_true", help="the words anywhere, not as a phrase")
    _filters(p)
    p.set_defaults(fn=cmd_who)

    p = sub.add_parser("profile", help="the stock clues for an answer")
    p.add_argument("name")
    p.add_argument("--top", type=int, default=30)
    p.add_argument("-e", "--examples", type=int, default=8, help="how many clues get an example sentence")
    p.add_argument("--exact", action="store_true", help="only answer lines that are exactly this")
    p.add_argument("--not", dest="exclude", action="append", help="drop answer lines holding this word")
    p.add_argument("--spec", action="store_true", help="rank by specificity-weighted score instead of raw n")
    p.add_argument("--pyramid", action="store_true", help="order chronologically from lead-in/power to giveaway")
    p.add_argument("--anki", action="store_true", help="mark what the Anki collection already has")
    _filters(p)
    p.set_defaults(fn=cmd_profile)

    p = sub.add_parser("top", help="frequency list of answer lines")
    p.add_argument("-n", type=int, default=50)
    p.add_argument("--rising", action="store_true", help="rank by recent growth instead of total")
    p.add_argument("--recent", type=int, default=3, help="how many years count as recent")
    p.add_argument("--min", type=int, default=1, help="least questions an answer needs")
    p.add_argument("--anki", action="store_true", help="mark what the Anki collection already has")
    p.add_argument("--missing", action="store_true", help="only answers with no Anki note")
    _filters(p)
    p.set_defaults(fn=cmd_top)

    p = sub.add_parser("fact", help="fact check: 'phrase|keyword'")
    p.add_argument("checks", nargs="+")
    p.add_argument("-n", type=int, default=6)
    _filters(p)
    p.set_defaults(fn=cmd_fact)

    p = sub.add_parser("like", help="clues worded like this")
    p.add_argument("text")
    p.add_argument("-n", type=int, default=10)
    _filters(p)
    p.set_defaults(fn=cmd_like)

    p = sub.add_parser("sets", help="list sets")
    p.add_argument("pattern", nargs="?")
    p.add_argument("-n", type=int, default=60)
    p.add_argument("-d", "--diff")
    p.add_argument("-y", "--year")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_sets)

    p = sub.add_parser("set", help="one set's questions")
    p.add_argument("name")
    p.add_argument("-p", "--packet", type=int)
    p.add_argument("-c", "--cat")
    p.add_argument("-t", "--type", dest="kind")
    p.add_argument("--full", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_set)

    p = sub.add_parser("show", help="one whole question, by id or uid")
    p.add_argument("ref")
    p.add_argument("--html", action="store_true", help="with qbreader's formatting tags")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("sync", help="update the mirror")
    p.add_argument("--full", action="store_true", help="re-fetch every set")
    p.add_argument("--years", type=int, default=1, help="re-check sets this many years back for changes")
    p.add_argument("--reparse", action="store_true", help="re-derive answer columns after a parser change; no download")
    p.set_defaults(fn=cmd_sync)

    p = sub.add_parser("status", help="what the mirror holds and how fresh it is")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("sql", help="read-only SQL over the mirror (tables q, u, f, sets)")
    p.add_argument("statement")
    p.add_argument("-n", type=int, default=50)
    p.add_argument("--width", type=int, default=70)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_sql)

    p = sub.add_parser("brief", help="agent clue briefing for an Anki deck (read-only)")
    p.add_argument("deck", help="Anki deck name, e.g. OVFA::Dance or VFA")
    p.add_argument("-t", "--tier", type=int, choices=[1, 2, 3, 4], help="tier 1-4")
    p.add_argument("--title", help="regex filter on note Title/Work")
    p.add_argument("-c", "--cat", help="qbreader category filter")
    p.add_argument("--top", type=int, default=12)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_brief)

    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 0
    try:
        if a.cmd not in ("sync", "status"):
            when = store.meta("synced")
            if when and time.time() - when > 21 * 86400:
                print("(mirror last synced %.0f days ago; `py -3.9 -m qbr sync` updates it)" % ((time.time() - when) / 86400),
                      file=sys.stderr)
        out = a.fn(a)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print("qbr: %s" % e, file=sys.stderr)
        return 2
    if out is not None:
        print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
