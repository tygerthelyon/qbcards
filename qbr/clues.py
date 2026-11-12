# -*- coding: utf-8 -*-
"""qbr.clues -- what quizbowl asks about one answer: its stock clues, counted. Called as qbr.profile().

    p = qbr.profile("Kazimir Malevich")
    for t in p["things"]: print(t["n"], t["thing"], t["where"], t["example"])

How it works. Take every unit the name answers (find.answered) and every other unit that mentions it. Propose
candidates from them: titles in italics or quotes, runs of capitalised words, recurring word n-grams. Then let the
index count each candidate properly:
    n     distinct questions on this answer that hold it
    m     distinct other questions that hold it in a sentence about this answer
    all   units in the whole mirror that hold it
    tied  the share of `all` that involve this answer at all -- 100% means the clue is unique to it
    lift  how many times more often it turns up here than across the mirror
Candidates that are not over-represented go, and of two that overlap the one that says more stays. Nothing is merged
by similarity of meaning, so a famous clue cannot be averaged away (StockFisher 1.0 chained 31 of 55 Malevich
sentences into one group and kept a sentence without Black Square).

A name that is never an answer line (Tilman Riemenschneider) still gets a profile, built from the questions that
mention it.
"""
import difflib
import math
import re
import statistics
from collections import Counter, defaultdict

from . import find, store
from .text import SEP, _key, _OPEN, _STOP, fold, grams, nested, sentences, things, where

CAP_MENTIONS = 4000      # most "mentioned in" units read for one answer
CAP_COMMON = 12000       # a candidate in more units than this (novel, painting) is a common word, not a clue
CAP_NAMED, CAP_GRAMS = 260, 150      # most candidates counted against the index

# one-word candidates that describe rather than identify: "this German philosopher"
_DEMONYM = frozenset("""american british english french german italian spanish russian chinese japanese greek roman dutch
irish scottish welsh polish austrian swiss swedish norwegian danish finnish hungarian czech portuguese belgian turkish
indian persian iranian egyptian mexican canadian australian brazilian argentine korean vietnamese african european asian
latin arabic arab hebrew jewish christian catholic protestant muslim islamic soviet western eastern northern southern
january february march april may june july august september october november december""".split())
# words a recurring phrase may not start or end on: they frame a clue, they are not the clue
_FRAME = frozenset("""wrote written author authored writer work works book novel poem play essay titled entitled called
named known painted painting painter artist created composed composer piece opera symphony thinker philosopher
philosophy movement school style group member founder founded leader ruler king emperor city country state building
church structure designed built architect man woman figure character title titular namesake eponymous described
describes argued argues claimed claims stated wrote said says published first second third later earlier also used
uses using include includes including one another name names identify performed conducted discovered invented
observed demonstrated proposed developed formulated introduced showed found studied won award awarded received""".split())
# Common n-gram boundaries that usually mean the phrase was cut off before its head
# noun or after its framing clause. Keep meaningful compounds such as "black hole" and
# "electric field"; this set only rejects them when they sit at an edge.
_GRAM_EDGE = _OPEN | _FRAME | frozenset("""according cannot cant greater greatest equal equals less least standard quantum electric black
study studies store storing states stating""".split())
_BOILER = frozenset(("points", "point", "this", "these", "ftp"))
_CATALOGUE_SUFFIX = re.compile(
    r"\s*,?\s*(?:op(?:us)?\.?\s*\d+[a-z]?(?:\s*,?\s*no\.?\s*\d+[a-z]?)?)\s*$", re.I)


def _without_catalogue_suffix(name):
    """Remove a trailing opus/catalogue number for a fallback work-title lookup."""
    return _CATALOGUE_SUFFIX.sub("", name or "").strip(" ,.-")


def _balanced_quotes(text):
    """Reject n-grams from malformed question sentences with an unmatched quote."""
    # Do not count curly apostrophes (the common possessive marker) as quotation marks.
    return text.count('"') % 2 == 0 and text.count("“") == text.count("”")


def _gram_quote_ok(sentence, gram, source=None):
    """Keep a phrase only when its matched source span does not cut through a quote."""
    if not any(q in sentence for q in ('"', "“", "”")):
        return True
    if source is None:
        source = fold_keep(sentence)
    pattern = r"(?<!\w)" + r"[\W_]+".join(re.escape(w) for w in gram.split()) + r"(?!\w)"
    for match in re.finditer(pattern, source, re.I):
        if _balanced_quotes(sentence[match.start():match.end()]):
            return True
    return False


def _own(key, names):
    """is this candidate just the answer's own name, or a piece of it?"""
    k = set(key.split()) - _STOP
    return not k or any(k <= n for n in names)


def _in(key, folded):
    """is the folded phrase `key` inside the space-padded folded text?"""
    return (" %s " % key) in folded


def _names(con, A, asked):
    """the phrases that count as mentioning this answer: its usual answer line, its usual alternates, and the
    required part alone (the surname) when no other answer shares it"""
    if not A:
        return [asked]
    akeys = Counter(r["akey"] for r in A)
    canon = akeys.most_common(1)[0][0]
    out = [canon]
    alts = Counter(a for r in A for a in r["accepts"].split(SEP) if a not in akeys)
    out += [a for a, c in alts.most_common(3) if c >= 2 and c >= 0.25 * len(A) and len(a) > 3]
    rk = Counter(r["rkey"] for r in A).most_common(1)[0][0]
    if rk and rk not in out and set(rk.split()) <= set(canon.split()) and len(rk) > 3:
        share = con.execute("SELECT akey, count(*) c FROM u WHERE rkey=? GROUP BY akey", (rk,)).fetchall()
        if sum(r["c"] for r in share if r["akey"] in akeys) >= 0.8 * sum(r["c"] for r in share):
            out.append(rk)
    return out


def profile(name, cat=None, diff=None, year=None, sets=None, kind=None, exact=False, exclude=(), top=30, min_n=None,
            anki=False, sort="n"):
    """The clue profile of an answer. Filters as in qbr.search; exact and exclude as in find.answered.
    sort: "n" (raw question count, default), "spec" (specificity-weighted: balances n with tied/lift), or "pyramid"
    (chronological tossup position from lead-in/power to giveaway).

    Returns a dict:
        found, name, names (the phrases counted as mentioning it), lines (answer lines matched, with counts),
        tossups, bonuses, questions, sets, mentioned, first, last, difficulty {level: questions}, categories
        things     the stock clues. Each: thing, kind ("title", "name" or "phrase"), n, m, sets, all,
                   tied, lift, score, pos, power, first, last, dmin, dmax, where (lead-in ... giveaway, by where it
                   falls in tossups), example (one sentence holding it) and source
        elsewhere  things said about this answer only in other answers' questions (same fields)
        under      the other answer lines whose questions mention this answer, with counts
        foils      confusable / related answers in the same category that co-occur most strongly with its clues
    With anki=True each thing and each `under` line gains "anki": "card", "suspended", "text" or "" (see qbr.anki).
    When the name is neither an answer line nor mentioned anywhere: {"found": False, "suggest": [(line, questions)]}.
    """
    con = store.db()
    A = find.answered(name, cat, diff, year, sets, kind, exact, exclude)
    # Quizbowl work answerlines often append an opus number that is metadata rather than
    # part of the title ("Christmas Concerto, Op. 6"). Retry the title without it only
    # when the full query found no answerline.
    lookup_name = _without_catalogue_suffix(name)
    if not A and lookup_name and lookup_name != name:
        A = find.answered(lookup_name, cat, diff, year, sets, kind, exact, exclude)
    names = _names(con, A, _key(name))
    name_sets = [set(x.split()) for x in dict.fromkeys(list(names) + [a for r in A for a in r["accepts"].split(SEP)]) if x]
    a_uids = {r["uid"]: r for r in A}
    a_qids = {r["qid"] for r in A}
    total_units = con.execute("SELECT count(*) FROM u").fetchone()[0]
    thin = len(a_qids) < 12
    floor = min_n if min_n is not None else (1 if thin else 2)
    gfloor = max(floor, 2 if thin else 3)

    # the other units that mention it
    wsql, wargs = find.where(cat, diff, year, sets, kind)
    m_rows = con.execute(
        "SELECT %s FROM f JOIN u ON u.uid=f.rowid WHERE f MATCH ?%s ORDER BY u.year DESC LIMIT ?" % (find.COLS, wsql),
        [find.CLUE + "(" + " OR ".join('"%s"' % n for n in names) + ")"] + wargs + [CAP_MENTIONS + len(A) + 1]).fetchall()
    mentioned_truncated = len(m_rows) > CAP_MENTIONS + len(A)
    M = [dict(r) for r in m_rows[:CAP_MENTIONS + len(A)] if r["uid"] not in a_uids]
    m_uids = {r["uid"] for r in M}
    if not A and not M:
        guess = find.search(name, cat, diff, year, sets, kind, scope="answer", mode="any", n=0)["answers"][:8]
        return {"found": False, "name": name, "suggest": [(g["answer"], g["n"]) for g in guess]}

    # ---- candidates from the answer's own questions
    bodies = {q: store.body(con, q) for q in a_qids}
    cand = defaultdict(lambda: {"shown": Counter(), "title": 0, "mid": 0, "q": set(), "mq": set()})

    def propose(kind_, shown, qid, into):
        k = _key(shown)                                       # "The Critique of Pure Reason" and "Critique of ..." are one
        # not the answer's own name, nor a longer run that merely contains it ("Altar ... by Tilman Riemenschneider"),
        # nor a bare description ("German", "German Philosopher")
        if k and not _own(k, name_sets) and not any(_in(n, " %s " % k) for n in names) and \
           not all(w in _DEMONYM or w in _FRAME or w in _STOP for w in k.split()):
            c = cand[k]
            c["shown"][shown] += 1
            c["title"] += kind_ == "title"
            c["mid"] += kind_ != "open"
            c[into].add(qid)

    a_sents = []                                              # (padded folded sentence, sentence, row)
    for r in A:
        b = bodies.get(r["qid"], {})
        if r["kind"] == "T":
            htm = b.get("q", "")
        else:
            htm = " ".join(([b.get("l", "")] if r["part"] == 1 else []) + (b.get("p") or [])[r["part"] - 1:r["part"]])
        for kind_, shown in things((r["lead"] + " " if r["lead"] else "") + r["text"], htm):
            propose(kind_, shown, r["qid"], "q")
        for s in sentences(r["lead"]) + sentences(r["text"]):
            a_sents.append((" %s " % fold(s["s"]), s, r))
    # ---- and from the sentences that mention it in other questions
    m_sents = []
    for r in M:
        for s in sentences(r["lead"]) + sentences(r["text"]):
            f = " %s " % fold(s["s"])
            if any(_in(n, f) for n in names):
                m_sents.append((f, s, r))
                for kind_, shown in things(s["s"]):
                    if _key(shown) != r["akey"]:
                        propose(kind_, shown, r["qid"], "mq")
    # A 1-word candidate that only ever appeared capitalised as the first word of a sentence (mid == 0, e.g. "Light",
    # "Electrons", "Poems") is an ordinary sentence opener, not a proper name.
    named = sorted(((k, c) for k, c in cand.items()
                    if len(c["q"]) + len(c["mq"]) >= (1 if thin else 2) and (c["mid"] > 0 or " " in k)),
                   key=lambda kc: -(len(kc[1]["q"]) + 0.5 * len(kc[1]["mq"])))[:CAP_NAMED]
    # ---- recurring wording that is not a name
    gq = defaultdict(set)
    gq_quoted = defaultdict(list)
    for f, s, r in a_sents:
        raw = s["s"]
        if not _balanced_quotes(raw):
            continue
        has_q = any(q in raw for q in ('"', "“", "”"))
        fk = fold_keep(raw) if has_q else None
        qid = r["qid"]
        for g in grams(f.strip(), hi=6):
            if has_q:
                gq_quoted[g].append((qid, raw, fk))
            else:
                gq[g].add(qid)
    counted = {k for k, _ in named}
    # What the questions call the answer ("this organelle", "this poet"). Wording built on that word frames a clue
    # ("found in this organelle") and is not one.
    called = Counter(m.group(1) for f, s, r in a_sents for m in re.finditer(r" (?:this|these) ([a-z]+)", f))
    called = {w for w, c in called.most_common(4) if c >= 0.1 * sum(called.values())}
    called |= {w + "s" for w in called} | {w[:-1] for w in called if w.endswith("s")}
    worded_cands = []
    for g in set(gq) | set(gq_quoted):
        if g in counted:
            continue
        gw = g.split()
        if (_BOILER & set(gw)) or (called & set(gw)) or _own(g, name_sets) or \
           gw[0] in _GRAM_EDGE or gw[-1] in _GRAM_EDGE or gw[0] in _DEMONYM or gw[-1] in _DEMONYM:
            continue
        qs = set(gq.get(g, ()))
        q_hits = gq_quoted.get(g, ())
        if len(qs) + len(q_hits) < gfloor:
            continue
        for qid, raw, fk in q_hits:
            if qid not in qs and _gram_quote_ok(raw, g, fk):
                qs.add(qid)
        if len(qs) >= gfloor:
            worded_cands.append((g, qs))
    worded = sorted(worded_cands, key=lambda x: -len(x[1]))[:CAP_GRAMS]

    def _recalc(t):
        S = t["all_uids"]
        mine = [a_uids[u] for u in S if u in a_uids]
        t["q"] = {r["qid"] for r in mine}
        t["n"] = len(t["q"])
        t["sets"] = len({r["set_name"] for r in mine})
        t["suids"] = [u for u in S if u not in a_uids]
        t["all"] = len(S)
        t["tied"] = sum(1 for u in S if u in a_uids or u in m_uids) / max(1, len(S))
        t["lift"] = (len(mine) / max(1, len(a_uids))) / (len(S) / total_units)
        return t

    raw_cur = con.cursor()
    raw_cur.row_factory = None

    def measure(key, kind_, mq=(), spans=0):
        """count one candidate against the whole index. spans: how many times it was proposed as a whole run of
        text, which is what tells a thing ("Critique of Pure Reason") from a piece of one ("of Pure Reason")"""
        S = {r[0] for r in raw_cur.execute("SELECT rowid FROM f WHERE f MATCH ? LIMIT ?",
                                           ('%s"%s"' % (find.CLUE, key), CAP_COMMON + 1))}
        if not S or len(S) > CAP_COMMON:
            return None
        mine = [a_uids[u] for u in S if u in a_uids]
        d = [r["difficulty"] for r in mine if r["difficulty"]]
        y = [r["year"] for r in mine if r["year"]]
        return _recalc({"key": key, "kind": kind_, "m": len(mq), "spans": spans, "all_uids": S,
                        "first": min(y) if y else None, "last": max(y) if y else None,
                        "dmin": min(d) if d else None, "dmax": max(d) if d else None})

    kept = {}
    for k, c in named:
        spans = sum(c["shown"].values())
        t = measure(k, "title" if 2 * c["title"] >= spans else "name", c["mq"], spans)
        if t:
            t["thing"] = c["shown"].most_common(1)[0][0]
            kept[k] = t
    for g, _ in worded:
        t = measure(g, "phrase")
        if t:
            t["thing"] = g
            kept[g] = t

    def absorb(big, small):
        big["all_uids"] |= small["all_uids"]
        big["m"], big["spans"] = max(big["m"], small["m"]), big["spans"] + small["spans"]
        _recalc(big)
        del kept[small["key"]]

    # plurals and possessives of one thing, and near-spellings (El Lissitzky / El Lissitsky), count once
    for k in sorted(kept, key=len):
        for longer in (k + "s", k + " s", k + "es"):
            if longer in kept and k in kept:
                a, b = kept[k], kept[longer]
                absorb(*((a, b) if a["n"] + a["m"] >= b["n"] + b["m"] else (b, a)))
    keys = sorted((k for k in kept if len(k) >= 6), key=lambda k: -(kept[k]["n"] + kept[k]["m"]))
    for i, k in enumerate(keys):
        for o in keys[i + 1:]:
            if k in kept and o in kept and k[0] == o[0] and abs(len(k) - len(o)) <= 2 and \
               difflib.SequenceMatcher(None, k, o).ratio() >= 0.9 and not (k[-1].isdigit() or o[-1].isdigit()):
                absorb(kept[k], kept[o])

    def strong(t):
        if t["kind"] == "phrase":
            return t["n"] >= gfloor and t["lift"] >= 12 and t["tied"] >= 0.3
        # a common word ("Exhibition") survives only if it is in a good share of the answer's questions, the way
        # "Hagia Sophia" is for Isidore of Miletus
        return t["n"] >= floor and (t["lift"] >= 6 or t["tied"] >= 0.3) and \
            (t["tied"] >= 0.04 or t["n"] >= 0.4 * len(a_qids))

    def kin(a, b):
        """do two keys share a word, or a word's first seven letters (suprematist / suprematism)?"""
        x, y = set(a.split()) - _STOP, set(b.split()) - _STOP
        return bool(x & y) or any(len(w) >= 7 and len(v) >= 7 and w[:7] == v[:7] for w in x for v in y)

    main = {k: t for k, t in kept.items() if strong(t)}
    # Of two candidates where one holds the other and they sit in mostly the same questions, one is the thing and the
    # other is a piece of it or it with a stray word. The thing is whichever the text more often presents as a whole
    # run: "Critique of Pure Reason" over "of Pure Reason", "Anthemius of Tralles" over "Designed by Anthemius of
    # Tralles". Two bare wordings tie, and the longer says more. A short one mostly covered by several longer ones
    # ("Critique" under the three Critiques, "Square" under "Black Square") goes the same way.
    for k in sorted(main, key=lambda k: len(k.split())):
        for o in [o for o in main if o != k and _in(k, " %s " % o)]:
            if k not in main:
                break
            a, b = main[k], main[o]                           # a is inside b
            # When `a` is the surname/nested short form of a unique person/entity `b` in `main` ("einstein" inside
            # "albert einstein", "millikan" inside "robert millikan"), fold `a`'s questions into `b` so the full
            # name carries the full count instead of listing both or dropping the first name.
            if a["kind"] == "name" and b["kind"] == "name" and nested(k, o) and \
               not any(w in o.split() for w in ("on", "in", "with", "over", "for", "to", "at", "from", "by", "after", "before", "under", "into", "as")) and \
               len([x for x in main if x != k and main[x]["kind"] == "name" and nested(k, x)
                    and not any(w in x.split() for w in ("on", "in", "with", "over", "for", "to", "at", "from", "by", "after", "before", "under", "into", "as"))]) == 1:
                b["all_uids"] |= a["all_uids"]
                b["m"], b["spans"] = max(a["m"], b["m"]), a["spans"] + b["spans"]
                _recalc(b)
                del main[k]
                break
            if b["n"] < 0.7 * a["n"]:
                continue
            if b["spans"] >= a["spans"] or (b["kind"] == "title" and a["kind"] != "title" and len(a["q"] & b["q"]) >= 0.85 * a["n"]):
                b["all_uids"] |= a["all_uids"]
                b["m"] = max(a["m"], b["m"])
                _recalc(b)
                del main[k]
            else:
                a["all_uids"] |= b["all_uids"]
                a["m"] = max(a["m"], b["m"])
                _recalc(a)
                del main[o]
        if k in main:
            over = [o for o in main if o != k and _in(k, " %s " % o)]
            if over and main[k]["spans"] < sum(main[o]["spans"] for o in over):
                cov = len(main[k]["q"] & set().union(*(main[o]["q"] for o in over)))
                if (cov >= 0.9 * main[k]["n"] and (main[k]["kind"] != "title" or main[k]["spans"] < 0.5 * main[k]["n"])) or (
                        main[k]["spans"] < 5 and main[k]["kind"] != "title" and cov >= 0.7 * main[k]["n"]):
                    del main[k]
    for t in main.values():
        t["score"] = round((t["n"] + 0.35 * t["m"]) * math.log1p(max(1.0, t["lift"])) * (0.1 + 0.9 * (t["tied"] ** 0.7)), 2)
    ranked = []
    for t in sorted(main.values(), key=(lambda t: (-t["score"], -t["n"], t["key"])) if sort == "spec"
                    else (lambda t: (-t["n"], t["kind"] == "phrase", -t["tied"], t["key"]))):
        # wording that only ever appears alongside a thing already listed is that thing again ("opera victory")
        if t["kind"] == "phrase" and any(kin(t["key"], o["key"]) and len(t["q"] & o["q"]) >= 0.8 * t["n"]
                                         for o in ranked):
            continue
        ranked.append(t)
    ranked = ranked[:top]
    other = []
    for t in sorted((t for k, t in kept.items() if k not in main and t["kind"] != "phrase" and t["n"] < floor
                     and t["m"] >= (1 if thin else 2) and t["tied"] >= 0.25
                     and not any(_in(k, " %s " % o) or _in(o, " %s " % k) for o in main)),
                    key=lambda t: (-t["m"], -len(t["key"]), -t["tied"])):
        if not any(_in(t["key"], " %s " % o["key"]) or _in(o["key"], " %s " % t["key"]) for o in other):
            other.append(t)
    other = other[:top if not A else max(8, top // 3)]
    used = set()

    def place(t, sents):
        """where in a tossup it tends to fall, and one sentence that shows it"""
        got = [(s, r) for f, s, r in sents if _in(t["key"], f)]
        by_tu = {}
        for s, r in got:
            if r["kind"] == "T" and r["qid"] not in by_tu:
                by_tu[r["qid"]] = s
        tu = list(by_tu.values())
        if tu:
            t["pos"] = round(statistics.median(s["pos"] for s in tu), 2)
            t["power"] = round(sum(1 for s in tu if s["power"]) / len(tu), 2)
            t["where"] = where(t["pos"], sum(s["give"] for s in tu) > len(tu) / 2)
        else:
            t["pos"], t["power"] = 1.0, 0.0
            t["where"] = "bonus" if got else ""
        # a sentence not already shown for another clue, not the giveaway, from a tossup, of middling length
        pick = sorted(got, key=lambda sr: (sr[0]["s"] in used, sr[0]["give"], sr[1]["kind"] != "T",
                                           abs(len(sr[0]["s"]) - 150)))
        t["example"], t["source"] = (pick[0][0]["s"], "%s, %s" % (pick[0][1]["set_name"], pick[0][1]["main"])) if pick \
            else ("", "")
        used.add(t["example"])
        if t["kind"] == "phrase" and pick:                    # show the wording as printed; capitalised, it is a name
            m = re.search(r"\b" + r"[\W_]+".join(map(re.escape, t["key"].split())) + r"\b", fold_keep(t["example"]), re.I)
            if m:
                t["thing"] = t["example"][m.start():m.end()]
                caps = [w[:1].isupper() for w in t["thing"].split() if w.lower() not in _STOP]
                if caps and sum(caps) >= 0.6 * len(caps) and not (set(t["key"].split()) & _FRAME):
                    t["kind"] = "name"

    for t in ranked:
        place(t, a_sents)
        if not t["example"]:
            place(t, m_sents)
    if sort == "pyramid":
        ranked.sort(key=lambda t: (t["where"] == "bonus", t["pos"], -t["n"]))
    for t in other:
        place(t, m_sents)

    # ---- confusable foils: other answer lines that share this answer's discriminative stock clues
    foil_clues = defaultdict(set)
    foil_u = {}
    for t in ranked[:20]:
        if 0.05 <= t["tied"] < 0.99 and t.get("suids") and len(t["suids"]) <= 400:
            for u in t["suids"]:
                foil_u[u] = None
                foil_clues[u].add(t["thing"])
    foils = []
    if foil_u:
        own_keys = set(names) | {r["akey"] for r in A}
        f_ans, f_shared, f_qids = Counter(), defaultdict(set), defaultdict(set)
        for r in con.execute("SELECT u.uid, u.qid, u.akey, u.main FROM u WHERE u.uid IN (%s)%s" %
                             (",".join(map(str, foil_u)), wsql), wargs):
            if r["akey"] and r["akey"] not in own_keys and not _own(r["akey"], name_sets):
                f_ans[(r["akey"], r["main"])] += 1
                f_qids[r["akey"]].add(r["qid"])
                f_shared[r["akey"]] |= foil_clues[r["uid"]]
        best_main = {}
        for (ak, mn), c in f_ans.most_common():
            best_main.setdefault(ak, mn)
        for ak, shared in sorted(f_shared.items(), key=lambda kv: (-len(kv[1]), -len(f_qids[kv[0]])))[:10]:
            if len(shared) >= 2:
                foils.append({"answer": best_main[ak], "akey": ak, "shared": sorted(shared)[:5], "n": len(f_qids[ak])})

    diffs, cats, seen = Counter(), Counter(), set()
    for r in A:
        if r["qid"] not in seen:
            seen.add(r["qid"])
            diffs[r["difficulty"] or 0] += 1
            cats[r["alt"] or r["subcategory"] or r["category"] or "?"] += 1
    years = [r["year"] for r in A if r["year"]]
    out = {
        "found": True, "name": Counter(r["main"] for r in A).most_common(1)[0][0] if A else name, "names": names,
        "lines": Counter(r["main"] for r in A).most_common(8),
        "tossups": sum(r["kind"] == "T" for r in A), "bonuses": sum(r["kind"] == "B" for r in A),
        "questions": len(a_qids), "sets": len({r["set_name"] for r in A}), "mentioned": len({r["qid"] for r in M}),
        "mentioned_truncated": mentioned_truncated,
        "first": min(years) if years else None, "last": max(years) if years else None,
        "difficulty": dict(sorted(diffs.items())), "categories": dict(cats.most_common(6)),
        "things": ranked, "elsewhere": other, "foils": foils[:8],
        "under": [g for g in find._tally(M) if g["n"] >= (1 if thin else 2)][:15],
    }
    for t in ranked + other:
        t.pop("q", None)
        t.pop("suids", None)
        t.pop("all_uids", None)
    if anki:
        from . import anki as deck
        idx = deck.index()
        tnames = [out["name"]] + list(names)
        for t in ranked + other:
            t["anki"] = deck.have(idx, t["key"], target_names=tnames)
        for g in out["under"]:
            g["anki"] = deck.have(idx, g["akey"], g["also"], target_names=tnames)
        out["anki"], out["anki_stale"] = deck.have(idx, out["name"], names), idx.get("stale")
    return out


def verify_clue(name, clue_text, cat=None, diff=None, year=None, sets=None):
    """Agent clue validator: check a proposed flashcard clue against an answer's qbreader profile and the mirror.
    Returns {"ok": bool, "leaks": [words], "length": int, "terms": [{term, n, all, tied}], "similar": [(sc, set, year, ans, s)]}.
    `ok` requires: no answer-word leak, length <= 190, and evidence tying the clue to `name` (either an extracted term
    with n >= 1 and tied >= 0.05, or a similar sentence in the mirror on `name`).
    """
    from .text import plain
    clean = plain(clue_text)
    bare = plain(re.sub(r"“[^”]*”|\"[^\"]*\"|<i>.*?</i>", " ", clue_text))
    bare = re.sub(r"\b(?:this|these|that|those|such\s+a|such\s+an)\s+(?:[a-z]+\s+){0,2}([a-z]+)", " ", bare, flags=re.I)
    own = set(_key(name).split()) - _STOP - _FRAME
    leaks = sorted(own & (set(fold(bare).split()) - _STOP))
    hits = []
    for _, th in things(clean, clue_text):
        k = _key(th)
        if len(k) >= 3 and k not in own:
            w = find.who(th, cat=cat, diff=diff, year=year, sets=sets)
            tot = sum(g["n"] for g in w)
            mine = sum(g["n"] for g in w if _key(g["akey"]) == _key(name) or _own(g["akey"], [own]))
            if tot:
                hits.append({"term": th, "n": mine, "all": tot, "tied": round(mine / tot, 2)})
    sents = find.like(clean, cat=cat, diff=diff, year=year, sets=sets, n=5)
    tied_hit = any(h["n"] >= 1 and h["tied"] >= 0.05 for h in hits) or \
        any(_key(ans) == _key(name) or _own(_key(ans), [own]) for _, _, _, ans, _ in sents)
    return {
        "ok": not leaks and len(clean) <= 190 and tied_hit,
        "leaks": leaks,
        "length": len(clean),
        "terms": hits,
        "similar": [(round(sc, 2), st, yr, ans, s) for sc, st, yr, ans, s in sents],
    }


def fold_keep(s):
    """`s` with every character that fold() would drop or change replaced one-for-one, so a match found in the result
    sits at the same offsets in `s`"""
    if s.isascii():
        return re.sub(r"[^A-Za-z0-9\s]", " ", s)
    return "".join(c if c.isascii() and (c.isalnum() or c.isspace()) else (" " if c.isascii() else (fold(c) if len(fold(c)) == 1 else " "))
                   for c in s)
