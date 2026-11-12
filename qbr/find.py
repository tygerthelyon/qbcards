# -*- coding: utf-8 -*-
"""qbr.find -- the searches over the mirror: clue text, clue-to-answer, frequency lists, fact checks, sets.

Every function takes the same filters:
    cat    category, subcategory or alternate subcategory, by name or short form, several with commas:
           "vfa", "Philosophy", "architecture,film"
    diff   qbreader difficulty: 7, "7-9", "6,7", or "ms" / "hs" / "college" / "open"
    year   2026, "2018-", "2015-2020"
    sets   part of a set name ("ACF Nationals"), or a list of them
    kind   "tossup" or "bonus"
and returns plain dicts and lists, so a script can use the results directly.
"""
import math
import re
from collections import Counter, defaultdict

from . import store
from .text import SEP, _key, _STOP, fold, near, sentences, takes

ALIAS = {
    "lit": "Literature", "hist": "History", "sci": "Science", "fa": "Fine Arts", "rel": "Religion", "myth": "Mythology",
    "phil": "Philosophy", "ss": "Social Science", "ce": "Current Events", "geo": "Geography", "trash": "Pop Culture",
    "pc": "Pop Culture", "other": "Other Academic",
    "amlit": "American Literature", "britlit": "British Literature", "eurolit": "European Literature",
    "worldlit": "World Literature", "classlit": "Classical Literature", "otherlit": "Other Literature",
    "amhist": "American History", "eurohist": "European History", "worldhist": "World History",
    "ancient": "Ancient History", "otherhist": "Other History", "bio": "Biology", "chem": "Chemistry", "phys": "Physics",
    "othersci": "Other Science", "vfa": "Visual Fine Arts", "afa": "Auditory Fine Arts", "ofa": "Other Fine Arts",
    "cs": "Computer Science", "astro": "Astronomy", "econ": "Economics", "psych": "Psychology", "arch": "Architecture",
    "photo": "Photography",
}
LEVELS = {"ms": [1], "hs": [2, 3, 4, 5], "college": [6, 7, 8, 9], "open": [10]}
COLS = ("u.uid, u.qid, u.part, u.kind, u.text, u.lead, u.answer, u.main, u.akey, u.rkey, u.accepts, u.set_name, u.year, "
        "u.difficulty, u.category, u.subcategory, u.alt")
CLUE = "{text lead}: "


# Filters
def _cat(token, facets):
    want = ALIAS.get(token.lower().replace(" ", ""), token).lower()
    for col in ("category", "subcategory", "alt"):
        for v in facets[col]:
            if v.lower() == want:
                return col, v
    near = [(col, v) for col in ("category", "subcategory", "alt") for v in facets[col] if v.lower().startswith(want)]
    if len({v for _, v in near}) == 1:
        return near[0]
    raise ValueError("no category %r. Categories: %s. Subcategories: %s. Alternate: %s." % (
        token, ", ".join(facets["category"]), ", ".join(facets["subcategory"]), ", ".join(facets["alt"])))


def _ints(v, named=None):
    """7 / "7-9" / "6,7" / [6, 7] -> sorted ints; an open end ("2018-") runs to 2100"""
    if v is None or v == "":
        return None
    if isinstance(v, int):
        return [v]
    if isinstance(v, (list, tuple, set)):
        return sorted(int(x) for x in v)
    out = set()
    for piece in str(v).split(","):
        piece = piece.strip().lower()
        if named and piece in named:
            out.update(named[piece])
        elif "-" in piece:
            a, b = piece.split("-", 1)
            out.update(range(int(a or 0), int(b or 2100) + 1))
        elif piece:
            out.add(int(piece))
    return sorted(out)


def where(cat=None, diff=None, year=None, sets=None, kind=None):
    """the shared filters -> (sql that starts with AND, or "", and its parameters)"""
    sql, args = [], []
    if cat:
        facets = store.meta("facets")
        ors = []
        for token in (cat if isinstance(cat, (list, tuple)) else str(cat).split(",")):
            if token.strip():
                col, v = _cat(token.strip(), facets)
                ors.append("u.%s=?" % col)
                args.append(v)
        sql.append("(" + " OR ".join(ors) + ")")
    d = _ints(diff, LEVELS)
    if d is not None:
        sql.append("u.difficulty IN (%s)" % ",".join(map(str, d)))
    y = _ints(year)
    if y is not None:
        sql.append("u.year BETWEEN ? AND ?")
        args += [y[0], y[-1]]
    if sets:
        names = [sets] if isinstance(sets, str) else list(sets)
        sql.append("(" + " OR ".join("u.set_name LIKE ?" for _ in names) + ")")
        args += ["%" + s + "%" for s in names]
    if kind:
        sql.append("u.kind=?")
        args.append({"t": "T", "b": "B"}[str(kind).lower()[0]])
    return (" AND " + " AND ".join(sql) if sql else ""), args


# Query language
_RAW = re.compile(r'"|\b(?:AND|OR|NOT)\b|NEAR\(|\*|(?i:\b(?:ans|answer|clue|text|lead)):\S|(?:^|\s)-\w')
_TOK = re.compile(r'"[^"]*"\*?|NEAR\(|\(|\)|,|[^\s(),"]+')
_COLUMN = {"ans": "accepts: ", "answer": "accepts: ", "clue": CLUE, "text": CLUE, "lead": "lead: "}


def _term(t):
    star = t.endswith("*")
    k = fold(t.strip('*"'))
    return ('"%s"%s' % (k, "*" if star else "")) if k else ""


def match(query, scope="clue", mode="phrase"):
    """What was typed -> a full-text MATCH expression.

    Plain words are a phrase (mode "phrase"), all required in any order ("all"), or any of them ("any"). Anything with
    an operator is passed through with its words folded: "a b" phrases, AND OR NOT, a leading - to exclude, supremat*
    prefixes, NEAR(a b, 10), and ans: to look in answer lines instead of clue text."""
    pre = {"clue": CLUE, "answer": "accepts: ", "all": ""}[scope]
    if not _RAW.search(query):
        words = fold(query).split()
        if not words:
            raise ValueError("nothing to search for in %r" % query)
        if mode == "phrase":
            return '%s"%s"' % (pre, " ".join(words))
        return "%s(%s)" % (pre, (" AND " if mode == "all" else " OR ").join('"%s"' % w for w in words))
    out, scoped, in_near = [], False, 0
    for t in _TOK.findall(query):
        if t == "NEAR(":
            in_near += 1
            out.append(t)
        elif t == "(":
            if in_near:
                in_near += 1
            out.append(t)
        elif t == ")":
            if in_near:
                in_near -= 1
            out.append(t)
        elif t in ("AND", "OR", "NOT"):
            out.append(t)
        elif t == ",":
            if in_near:
                out.append(t)
        elif out and out[-1] == "," and t.isdigit():
            out.append(t)                                       # the distance in NEAR(a b, 10)
        elif t.startswith("-") and len(t) > 1:
            out += ["NOT", _term(t[1:])]
        elif ":" in t and t.split(":", 1)[0].lower() in _COLUMN:
            col, rest = t.split(":", 1)
            scoped = True
            out.append(_COLUMN[col.lower()] + _term(rest))
        else:
            out.append(_term(t))
    expr = " ".join(x for x in out if x)
    return expr if scoped or not pre else "%s(%s)" % (pre, expr)


def _best(row, words, phrase=None, k=2):
    """the sentences of a unit that carry the match, best first"""
    sents = [dict(s, lead=True) for s in sentences(row["lead"])] + sentences(row["text"])
    scored = []
    for s in sents:
        f = " %s " % fold(s["s"])
        hit = 100 if phrase and (" %s " % phrase) in f else sum((" %s " % w) in f or (w.endswith("*") and (" " + w[:-1]) in f)
                                                                 for w in words)
        if hit:
            scored.append((-hit, s["i"], s))
    scored.sort(key=lambda x: x[:2])
    top = scored[0][0] if scored else 0
    return [s for h, _, s in scored if h == top][:k]


# Answer variants
def merge(groups):
    """Fold answer-line variants together. groups: akey -> dict with n, rkey and anything else; returns the same
    dicts with `also` listing what was merged in. Two keys merge only when they share the required (underlined) part
    and read as one name (text.near) -- "malevich" and "kasimir malevich" join "kazimir malevich", "i m pei" joins
    "ieoh ming pei", "barcelona chair" does not join "barcelona" -- and never when a short key could belong to two
    different longer ones ("adams" stays out of both "john adams" and "samuel adams")."""
    by_r = defaultdict(list)
    for k, g in groups.items():
        g.setdefault("also", [])
        by_r[g.get("rkey") or k].append(k)
    dead = set()
    for keys in by_r.values():
        if len(keys) < 2:
            continue
        for k in sorted(keys, key=lambda k: groups[k]["n"]):
            mates = [p for p in keys if p != k and p not in dead and near(k, p)]
            if not mates or not all(near(a, b) for a in mates for b in mates):
                continue
            p = max(mates, key=lambda p: groups[p]["n"])
            if groups[p]["n"] < groups[k]["n"]:
                continue
            for field, v in groups[k].items():
                if isinstance(v, (int, float)) and field not in ("first", "last"):
                    groups[p][field] = groups[p].get(field, 0) + v
            groups[p]["first"] = min(groups[p].get("first") or 9999, groups[k].get("first") or 9999)
            groups[p]["last"] = max(groups[p].get("last") or 0, groups[k].get("last") or 0)
            groups[p]["also"] += [k] + groups[k]["also"]
            dead.add(k)
    return {k: g for k, g in groups.items() if k not in dead}


def _tally(rows):
    """rows -> merged answer groups, counted once per question"""
    g, seen = {}, set()
    for r in rows:
        if not r["akey"] or (r["qid"], r["akey"]) in seen:
            continue
        seen.add((r["qid"], r["akey"]))
        d = g.setdefault(r["akey"], {"n": 0, "tossups": 0, "bonuses": 0, "rk": Counter(), "mains": Counter(),
                                     "first": 9999, "last": 0})
        d["n"] += 1
        d["tossups" if r["kind"] == "T" else "bonuses"] += 1
        d["rk"][r["rkey"]] += 1
        d["mains"][r["main"]] += 1
        d["first"], d["last"] = min(d["first"], r["year"] or 9999), max(d["last"], r["year"] or 0)
    for d in g.values():
        d["rkey"] = d.pop("rk").most_common(1)[0][0]
        d["answer"] = d.pop("mains").most_common(1)[0][0]
    out = merge(g)
    for k, d in out.items():
        d["akey"] = k
    return sorted(out.values(), key=lambda d: -d["n"])


# Searches
def search(query, cat=None, diff=None, year=None, sets=None, kind=None, scope="clue", mode="auto", regex=False,
           sort="auto", n=10, offset=0):
    """Search clue text (scope "clue"), answer lines ("answer") or both ("all").

    mode "auto" tries the words as a phrase and, if nothing has it, as all-words-anywhere. regex=True treats the query
    as a regular expression over the clue text instead (a full scan, a few seconds). sort: "new", "old", "hard", "easy",
    "rank" (best match first); "auto" is rank for loose matches and newest first otherwise.

    Returns {"units", "questions": totals, "match": what ran, "answers": which answer lines the hits sit under,
    "hits": the n asked for, each with its matching sentences in "sentences"}."""
    con = store.db()
    wsql, wargs = where(cat, diff, year, sets, kind)
    used = "regex"
    if regex:
        col = {"clue": "(u.text REGEXP ?1 OR u.lead REGEXP ?1)", "answer": "u.answer REGEXP ?1",
               "all": "(u.text REGEXP ?1 OR u.lead REGEXP ?1 OR u.answer REGEXP ?1)"}[scope]
        light = con.execute("SELECT u.uid, u.qid, u.akey, u.rkey, u.main, u.kind, u.year, u.difficulty, 0 AS rank FROM u "
                            "WHERE " + col + wsql.replace("?", "?%d") % tuple(range(2, 2 + len(wargs))),
                            [query] + wargs).fetchall()
    else:
        light = []
        for m in (["phrase", "all"] if mode == "auto" else [mode]):
            used = match(query, scope, m)
            light = con.execute("SELECT u.uid, u.qid, u.akey, u.rkey, u.main, u.kind, u.year, u.difficulty, bm25(f) AS rank "
                                "FROM f JOIN u ON u.uid=f.rowid WHERE f MATCH ?" + wsql, [used] + wargs).fetchall()
            if light:
                break
    loose = not regex and ("AND" in used or " OR " in used)
    order = {"new": lambda r: (-(r["year"] or 0), -(r["difficulty"] or 0), r["uid"]), "old": lambda r: (r["year"] or 0, r["uid"]),
             "hard": lambda r: (-(r["difficulty"] or 0), -(r["year"] or 0)), "easy": lambda r: (r["difficulty"] or 0, -(r["year"] or 0)),
             "rank": lambda r: (r["rank"], -(r["year"] or 0))}[("rank" if loose else "new") if sort == "auto" else sort]
    light.sort(key=order)
    page = light[offset:offset + n]
    hits = []
    if page:
        full = {r["uid"]: dict(r) for r in con.execute(
            "SELECT %s, q.id, q.packet, q.number FROM u JOIN q ON q.qid=u.qid WHERE u.uid IN (%s)" % (
                COLS, ",".join(str(r["uid"]) for r in page)))}
        words = [w.strip('"') for w in re.findall(r'"[^"]+"\*?', used)] if not regex else []
        phrase = words[0] if len(words) == 1 and " " in words[0] else None
        for r in page:
            h = full[r["uid"]]
            if regex:
                rx = re.compile(query, re.I)
                h["sentences"] = [s for s in sentences(h["lead"]) + sentences(h["text"]) if rx.search(s["s"])][:2]
            else:
                h["sentences"] = _best(h, [w for x in words for w in x.split()], phrase)
            hits.append(h)
    return {"query": query, "match": used, "units": len(light), "questions": len({r["qid"] for r in light}),
            "answers": _tally(light), "hits": hits}


def who(phrase, cat=None, diff=None, year=None, sets=None, kind=None, mode="auto"):
    """Clue to answer: the answer lines a phrase sits under, most frequent first, each with n (questions), its share
    of all the phrase's questions, and first and last year. A clue that is unique to one answer shows one line."""
    r = search(phrase, cat, diff, year, sets, kind, mode=mode, n=0)
    total = max(1, sum(a["n"] for a in r["answers"]))
    for a in r["answers"]:
        a["share"] = a["n"] / total
    return r["answers"]


def answered(name, cat=None, diff=None, year=None, sets=None, kind=None, exact=False, exclude=()):
    """Every unit this name answers. First the lines whose main answer takes `name` (see text.takes). Then lines that
    only accept it as an alternate, kept when the two are the same thing under another name -- the main answers list
    that line's answer as an alternate in return ("Hagia Sophia [or Ayasofya]" and a line headed "Ayasofya") -- and
    dropped when the name is one acceptable instance of something broader ("mosques [accept Hagia Sophia]").
    exact=True keeps only lines whose main answer is exactly `name`; exclude drops lines whose main answer holds any
    of those words ("coolidge" when asking for the president John Adams)."""
    con = store.db()
    want = _key(name)
    if not want:
        return []
    wsql, wargs = where(cat, diff, year, sets, kind)
    rows = con.execute("SELECT %s FROM f JOIN u ON u.uid=f.rowid WHERE f MATCH ?%s" % (COLS, wsql),
                       ['accepts: "%s"' % want] + wargs).fetchall()
    bad = {fold(x) for x in exclude}
    out, second = [], []
    for r in rows:
        acc = r["accepts"].split(SEP)
        if (exact and r["akey"] != want) or (bad and bad & set(r["akey"].split())):
            continue
        if takes(acc[:1], want):
            out.append(dict(r))
        elif not exact and takes(acc[1:], want):
            second.append(dict(r))
    if out:
        canon = Counter(r["akey"] for r in out).most_common(1)[0][0]
        back = {a for r in out for a in r["accepts"].split(SEP)[1:]}
        out += [r for r in second if r["akey"] in back or near(r["akey"], canon)]
    elif second:
        # A name that only ever appears as an alternate. If nearly all of those lines are one answer (Samuel Clemens
        # under Mark Twain), the question was about that answer: return all of it.
        head, c = Counter(r["akey"] for r in second).most_common(1)[0]
        if c >= 0.7 * len(second) and head != want:
            return answered(head, cat, diff, year, sets, kind, exact, exclude)
        out = second
    if out and not exact:
        # Widen through the required part, to the same answer under another spelling or a fuller name: "Kasimir
        # Malevich" and "Kazimir Severinovich Malevich" share the underlined "Malevich". A sibling line joins only if
        # it reads as the same name (text.near) and could not equally belong to a different one: with "John Adams",
        # the bare line "Adams" stays out because "Ansel Adams" holds it too.
        akeys = Counter(r["akey"] for r in out)
        canon = akeys.most_common(1)[0][0]
        rk = Counter(r["rkey"] for r in out).most_common(1)[0][0]
        sibs = con.execute("SELECT akey, count(*) c FROM u WHERE rkey=? GROUP BY akey", (rk,)).fetchall() if rk else []
        rivals = [set(s["akey"].split()) for s in sibs if s["c"] >= 3 and not near(s["akey"], canon)]
        add = [s["akey"] for s in sibs if s["akey"] not in akeys and near(s["akey"], canon)
               and not any(set(s["akey"].split()) <= r for r in rivals)
               and not (bad and bad & set(s["akey"].split()))]
        if add:
            have = {r["uid"] for r in out}
            out += [dict(r) for r in con.execute(
                "SELECT %s FROM u WHERE u.rkey=? AND u.akey IN (%s)%s" % (COLS, ",".join("?" * len(add)), wsql),
                [rk] + add + wargs) if r["uid"] not in have]
    return out


def rows(cat=None, diff=None, year=None, sets=None, kind=None, answer=None):
    """A pool for scripts: every unit under the filters (and, with answer=, only those it answers), as dicts with
    uid, qid, part, kind, text, lead, answer, main, akey, rkey, accepts, set_name, year, difficulty, category,
    subcategory, alt. Replaces the _qb_pool_*.json dumps."""
    if answer:
        return answered(answer, cat, diff, year, sets, kind)
    wsql, wargs = where(cat, diff, year, sets, kind)
    return [dict(r) for r in store.db().execute("SELECT %s FROM u WHERE 1%s" % (COLS, wsql), wargs)]


def top(cat=None, diff=None, year=None, sets=None, kind=None, n=50, sort="n", recent=3, min_n=1):
    """The frequency list: answer lines under the filters, variants merged, most asked first. Each has n (questions),
    tossups, bonuses, first, last, mean difficulty, and recent (how many fall in the last `recent` years of the mirror).
    sort="rising" ranks by how much more often an answer has come up in those years than its history predicts."""
    con = store.db()
    wsql, wargs = where(cat, diff, year, sets, kind)
    latest = con.execute("SELECT max(year) FROM sets").fetchone()[0] or 0
    since = latest - recent + 1
    g = {}
    for r in con.execute("SELECT u.akey, u.rkey, u.main, u.kind, count(DISTINCT u.qid) c, min(u.year) a, max(u.year) b, "
                         "sum(u.difficulty) d, count(DISTINCT CASE WHEN u.year>=? THEN u.qid END) r FROM u "
                         "WHERE u.akey<>''%s GROUP BY u.akey, u.rkey, u.main, u.kind" % wsql, [since] + wargs):
        d = g.get(r["akey"])
        if d is None:
            d = g[r["akey"]] = {"n": 0, "tossups": 0, "bonuses": 0, "dsum": 0, "recent": 0, "first": 9999, "last": 0,
                                "rk": {}, "mains": {}}
        d["n"] += r["c"]
        d["tossups" if r["kind"] == "T" else "bonuses"] += r["c"]
        d["dsum"] += r["d"] or 0
        d["recent"] += r["r"]
        d["first"], d["last"] = min(d["first"], r["a"] or 9999), max(d["last"], r["b"] or 0)
        d["rk"][r["rkey"]] = d["rk"].get(r["rkey"], 0) + r["c"]
        d["mains"][r["main"]] = d["mains"].get(r["main"], 0) + r["c"]
    for d in g.values():
        rk, mains = d.pop("rk"), d.pop("mains")
        d["rkey"], d["answer"] = max(rk, key=rk.get), max(mains, key=mains.get)
    if n and sort == "n" and len(g) > 20000:
        # A list of the top n cannot be changed by variants of answers far below it, so on a very large pool only the
        # required parts of the leading answers are merged.
        lead = {d["rkey"] for d in sorted(g.values(), key=lambda d: -d["n"])[:max(400, 10 * n)]}
        rest = {k: d for k, d in g.items() if d["rkey"] not in lead}
        for d in rest.values():
            d["also"] = []
        g = dict(merge({k: d for k, d in g.items() if d["rkey"] in lead}), **rest)
    else:
        g = merge(g)
    span = con.execute("SELECT count(DISTINCT u.qid) n, count(DISTINCT CASE WHEN u.year>=? THEN u.qid END) r FROM u "
                       "WHERE 1" + wsql, [since] + wargs).fetchone()
    base = (span["r"] or 0) / max(1, span["n"])             # the share of all these questions that is recent
    out = []
    for k, d in g.items():
        if d["n"] < min_n:
            continue
        d["akey"], d["difficulty"] = k, d.pop("dsum") / max(1, d["n"])
        # recent count against what its history predicts, damped so one new question on a rare answer is not a trend
        d["rising"] = (d["recent"] + 1) / (d["n"] * base + 2) if base else 0
        out.append(d)
    out.sort(key=(lambda d: (-d["rising"], -d["n"])) if sort == "rising" else (lambda d: (-d["n"], d["akey"])))
    return out[:n] if n else out


def fact(phrase, keyword=None, cat=None, diff=None, year=None, sets=None, n=6):
    """A fact check: the sentences qbreader has that hold `keyword` (a regular expression) in questions that hold
    `phrase`. With no keyword, the sentences holding the phrase. Returns {"tossups", "bonuses": how many questions
    hold the phrase, "sentences": [(set, year, answer, sentence)]}."""
    con = store.db()
    wsql, wargs = where(cat, diff, year, sets)
    got = con.execute("SELECT %s FROM f JOIN u ON u.uid=f.rowid WHERE f MATCH ?%s ORDER BY u.year DESC" % (COLS, wsql),
                      [match(phrase)] + wargs).fetchall()
    rx = re.compile(keyword or re.escape(phrase), re.I)
    fp, out, seen = fold(phrase), [], set()
    for r in got:
        for s in sentences(r["lead"]) + sentences(r["text"]):
            if rx.search(s["s"]) and (keyword or fp in fold(s["s"])) and s["s"] not in seen:
                seen.add(s["s"])
                out.append((r["set_name"], r["year"], r["main"], s["s"]))
    return {"tossups": len({r["qid"] for r in got if r["kind"] == "T"}),
            "bonuses": len({r["qid"] for r in got if r["kind"] == "B"}), "sentences": out[:n] if n else out}


def like(text, cat=None, diff=None, year=None, sets=None, kind=None, n=10):
    """Clues like this one: the sentences across the mirror that share the most of the rarest words of `text`. Good for
    "has this been asked before, in other words?" Returns [(score 0-1, set, year, answer, sentence)]."""
    con = store.db()
    words = [w for w in dict.fromkeys(fold(text).split()) if w not in _STOP and len(w) > 2]
    if not words:
        return []
    total = con.execute("SELECT count(*) FROM u").fetchone()[0]
    df = dict(con.execute("SELECT term, doc FROM fv WHERE term IN (%s)" % ",".join("?" * len(words)), words).fetchall())
    idf = {w: math.log(total / df[w]) for w in words if df.get(w)}
    keep = sorted(idf, key=idf.get, reverse=True)[:14]
    if not keep:
        return []
    wsql, wargs = where(cat, diff, year, sets, kind)
    got = con.execute("SELECT %s FROM f JOIN u ON u.uid=f.rowid WHERE f MATCH ?%s ORDER BY bm25(f) LIMIT 400" % (COLS, wsql),
                      [CLUE + "(" + " OR ".join('"%s"' % w for w in keep) + ")"] + wargs).fetchall()
    norm = sum(idf[w] for w in keep)
    out, seen = [], set()
    for r in got:
        for s in sentences(r["lead"]) + sentences(r["text"]):
            f = set(fold(s["s"]).split())
            score = sum(idf[w] for w in keep if w in f) / norm
            if score > 0.25 and s["s"] not in seen:
                seen.add(s["s"])
                out.append((score, r["set_name"], r["year"], r["main"], s["s"]))
    out.sort(key=lambda x: -x[0])
    return out[:n]


# Sets and questions
def sets(pattern=None, year=None, diff=None):
    """the sets in the mirror, newest first: dicts with name, year, difficulty, tossups, bonuses"""
    sql, args = "SELECT * FROM sets WHERE 1", []
    if pattern:
        sql, args = sql + " AND name LIKE ?", args + ["%" + pattern + "%"]
    y, d = _ints(year), _ints(diff, LEVELS)
    if y:
        sql, args = sql + " AND year BETWEEN ? AND ?", args + [y[0], y[-1]]
    if d:
        sql += " AND difficulty IN (%s)" % ",".join(map(str, d))
    return [dict(r) for r in store.db().execute(sql + " ORDER BY year DESC, name", args)]


def packet(set_name, cat=None, kind=None, number=None):
    """One set's units in packet order (the whole set, or packet `number`), under the usual filters: the tournament
    audit. Each dict also has packet and number (the question's place in its packet)."""
    wsql, wargs = where(cat, kind=kind)
    sql = "SELECT %s, q.id, q.packet, q.number FROM u JOIN q ON q.qid=u.qid WHERE u.set_name=?%s" % (COLS, wsql)
    args = [set_name] + wargs
    if number:
        sql, args = sql + " AND q.packet=?", args + [number]
    return [dict(r) for r in store.db().execute(sql + " ORDER BY q.packet, u.kind DESC, q.number, u.part", args)]


def show(ref):
    """One whole question, by qbreader id or by the uid a search printed: {"question": its row, "units": its tossup
    or bonus parts, "formatted": the text with qbreader's bold, underline and italics}."""
    con = store.db()
    if str(ref).isdigit():
        r = con.execute("SELECT qid FROM u WHERE uid=?", (int(ref),)).fetchone()
    else:
        r = con.execute("SELECT qid FROM q WHERE id=?", (ref,)).fetchone()
    if not r:
        return None
    q = dict(con.execute("SELECT qid, id, kind, set_name, year, difficulty, packet, packet_name, number, category, "
                         "subcategory, alt, updated FROM q WHERE qid=?", (r[0],)).fetchone())
    units = [dict(u) for u in con.execute("SELECT %s FROM u WHERE u.qid=? ORDER BY u.part" % COLS, (r[0],))]
    return {"question": q, "units": units, "formatted": store.body(con, r[0])}
