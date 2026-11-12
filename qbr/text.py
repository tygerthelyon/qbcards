# -*- coding: utf-8 -*-
"""qbr.text -- the text handling everything else leans on: folding, answer lines, sentences, named things.

Nothing here touches the network or the database, so any script can import it.
"""
import difflib
import functools
import html
import re
import unicodedata

# letters NFKD leaves alone
_ODD = str.maketrans({"ø": "o", "Ø": "O", "ł": "l", "Ł": "L", "đ": "d", "Đ": "D", "ß": "ss", "æ": "ae", "Æ": "AE",
                      "œ": "oe", "Œ": "OE", "þ": "th", "Þ": "Th", "ð": "d", "Ð": "D", "ı": "i"})

DOTS = {0: "?", 1: "MS", 2: "easy HS", 3: "HS", 4: "hard HS", 5: "HS nats", 6: "1 dot", 7: "2 dot", 8: "3 dot",
        9: "4 dot", 10: "open"}


_NONWORD = re.compile(r"[^\w]+|_")


def fold(s):
    """Lower case, no accents, no punctuation: the key every comparison uses. Splits words exactly where the
    full-text index does, so a folded phrase can be handed straight to it."""
    s = s or ""
    if not s.isascii():
        s = unicodedata.normalize("NFKD", s.translate(_ODD))
        s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(_NONWORD.sub(" ", s.lower()).split())


def plain(h):
    """formatted text (qbreader's <b><u><i>) -> plain"""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h or ""))).strip()


_GUIDE = re.compile(
    r'\s*\(\s*(?:["“][^"“”()]{1,90}["”]'
    r'|(?:uh\s+)+(?=[A-Za-z-]*[A-Z]{2})[A-Za-z-\s]{3,60}'
    r'|(?=[A-Za-z-\s]*-[A-Za-z-\s]*)(?=[A-Za-z-\s]*[A-Z]{2})[A-Za-z]+(?:-[A-Za-z]+)+(?:\s+[A-Za-z]+(?:-[A-Za-z]+)*)*)\s*\)'
)


def no_guides(s):
    """drop pronunciation guides: Kazimir Malevich ("kah-zih-MEER") -> Kazimir Malevich"""
    return _GUIDE.sub("", s or "")


# Sentences
_ABBR = frozenset("mr mrs ms dr st ste jr sr prof gen col lt sgt capt cmdr rev fr gov sen rep pres vs etc no nos op ca cf "
                  "vol pp mt ft inc ltd co corp bros mme mlle viz".split())
_BOUND = re.compile(r'([.?!]+)(["”’\')\]]*)\s+(?=["“‘(\[]?[A-Z0-9])')
_GIVE = re.compile(r"\bfor\s+(?:10|ten|15|fifteen|20|twenty|5|five)\s+points?\b|\bFTP\b", re.I)


def sentences(text):
    """A question's sentences in order, as dicts: s (the sentence), i and n (index, count), pos (0 = the question's
    first character, 1 = its last), power (before the power mark), give (holds "for 10 points")."""
    text = no_guides(text or "").strip()
    star = text.find("(*)")
    spans, last = [], 0
    for m in _BOUND.finditer(text):
        if m.group(1) == "." and not m.group(2):
            w = re.search(r"([A-Za-z.]+)$", text[max(last, m.start() - 14):m.start()])
            w = w.group(1) if w else ""
            if w.lower() in _ABBR or (len(w) == 1 and w.isupper()) or re.fullmatch(r"(?:[A-Za-z]\.)+[A-Za-z]", w):
                continue                                    # Dr. / A. L. Lloyd / U.S. are not sentence ends
            if w.lower() == "al" and re.search(r"\bet\s+al$", text[max(last, m.start() - 10):m.start()], re.I) and \
               re.match(r"[\(\[]?\d{4}\b", text[m.end():]):
                continue                                    # Milone et al. 2017 is not a sentence end
        spans.append((last, m.end()))
        last = m.end()
    spans.append((last, len(text)))
    out = []
    for a, b in spans:
        s = re.sub(r"\s+", " ", text[a:b].replace("(*)", " ")).strip()
        if len(s) < 3:
            continue
        out.append({"s": s, "pos": a / max(1, len(text)), "power": 0 <= a < star, "give": bool(_GIVE.search(s))})
    for i, d in enumerate(out):
        d["i"], d["n"] = i, len(out)
    return out


def where(pos, give=False):
    """a sentence's place in a tossup, in words"""
    return "giveaway" if give else "lead-in" if pos < 0.2 else "early" if pos < 0.45 else "middle" if pos < 0.7 else "late"


# Answer lines
_DIRECTIVE = re.compile(r"\b(?:do\s+not|don'?t|reject|anti-?prompt|prompt|also\s+accept|accept)\b", re.I)
_CONTINUES = re.compile(r"\b(?:do\s+not|don'?t|not|never|or|nor|and|but)\s*$", re.I)
# a clause with no directive of its own that says when the next one applies: 'before "X" is read,', 'for the first clue,'
_WHEN = re.compile(r"^(?:before|after|until|once|for)\b.*(?:,|\b(?:read|mentioned|mention|given)\b[\"”']?)\s*$", re.I)
# words left around an alternate that are about accepting it, not part of it
_ASIDE = frozenset("otherwise afterwards generously grudgingly begrudgingly reluctantly leniently liberally guess".split())
_POS = re.compile(r"^(?:or|accept|also accept|accept also|also|and accept)\b[:,]?\s*", re.I)
_NEG = re.compile(r"^(?:prompt|anti-?prompt|do not|don'?t|reject|but do not|but prompt|not)\b", re.I)
_TRAIL = re.compile(r"\s+(?:until|before|after|in place of|instead of|if|since|because|but|by asking|once)\b.*$", re.I)
_VAGUE = re.compile(r"\b(?:either|any|word forms?|equivalents?|synonyms?|answers?|descriptions?|clear[- ]knowledge|"
                    r"underlined|anything|translations?|reasonable|similar|indicating|mentioning|referring)\b", re.I)
_UNDERLINED_META = re.compile(
    r"^(?:either|any|both)\s+underlined?\s+(?:parts?|words?|names?|portions?|sections?|answers?|terms?)$", re.I)
_ART = re.compile(r"^(?:the|a|an)\s+")
_INNER = re.compile(r"^([^\[(]+?)\s*\(([^()\[\]]{1,40})\)\s*([^\s\[(][^\[(]*)")
_OR = re.compile(r",?\s+or\s+")
_TAG = re.compile(r"\s*<[^<>]{0,60}>\s*$")          # a writer's tag left on the end: Immanuel Kant <BW, Philosophy>
SEP = " | "


def _key(s):
    return _ART.sub("", fold(s))


def parse_answer(san, htm=""):
    """An answer line -> main (as printed), akey (its folded key), rkey (the underlined, required part, folded) and
    accepts (every folded answer the line takes: the main one, then each "or" and "accept"; never a prompt).

        Kazimir <b><u>Malevich</u></b> [or Kazimir Severinovich Malevich; prompt on <u>Suprematist</u>]
        -> main "Kazimir Malevich", akey "kazimir malevich", rkey "malevich",
           accepts ["kazimir malevich", "kazimir severinovich malevich"]
    """
    s = _TAG.sub("", html.unescape(no_guides(san or ""))).strip()
    extra = []
    # an optional piece inside the answer -- Kazimir (Severinovich) Malevich -- comes out of the main answer
    m = _INNER.match(s)
    if m and not _POS.match(m.group(2)) and not _NEG.match(m.group(2)):
        extra.append("%s %s %s" % m.groups())
        s = "%s %s%s" % (m.group(1), m.group(3), s[m.end():])
    cut = re.search(r"\s[\[(]|\[", s)
    main, tail = (s[:cut.start()], s[cut.start():]) if cut and cut.start() > 0 else (s, "")
    main = re.sub(r"\s+", " ", main).strip(" \"“”.,;:")
    head = re.sub(r"\([^()]*\)", " ", (htm or "").split("[", 1)[0])
    # "Hagia Sophia or Ayasofya", "Candide, or Optimism": the first is the answer, the rest are other ways to give it.
    # Left whole when the underlining runs straight across the "or" (Trick or Treat).
    pieces = _OR.split(main)
    if len(pieces) > 1 and pieces[0].strip() and not re.search(r"<u>[^<]*\sor\s[^<]*</u>", head):
        extra += [p for p in pieces[1:] if len(p.split()) <= 6] + [main]
        main, head = pieces[0].strip(" \"“”.,;:"), _OR.split(head, 1)[0]
    akey = _key(main) or fold(s)
    accepts = [akey] + [k for k in dict.fromkeys(_key(x) for x in extra) if k and k != akey and len(k) <= 90]
    for body in re.findall(r"[\[(]([^\[\]()]*)[\])]", tail):
        ok = None
        for clause in _clauses(body):
            if _NEG.match(clause):
                ok = False
            elif _POS.match(clause):
                ok, clause = True, _POS.sub("", clause)
            elif _WHEN.match(clause):
                continue                                    # 'before "X" is read,' qualifies the directive after it
            if not ok:
                continue                                    # a note, a prompt, or a "do not accept"
            for alt in re.split(r"\s*,\s*(?:or\s+)?|\s+or\s+", _TRAIL.sub("", clause)):
                alt = _POS.sub("", alt.strip())
                if _VAGUE.search(alt):
                    if _UNDERLINED_META.match(alt):
                        continue                            # "either underlined part, or USA, or US"
                    break                                   # a description starts here; what follows is still it
                k = " ".join(w for w in _key(alt).split() if w not in _ASIDE)
                if k and 1 < len(k) <= 60 and len(k.split()) <= 8 and k not in _SUFFIX and \
                   k not in accepts and not _NEG.match(alt) and not all(w in _STOP for w in k.split()):
                    accepts.append(k)
    rkey = fold(plain(" ".join(re.findall(r"<u>(.*?)</u>", head, flags=re.S)))) or akey
    return {"main": main or s, "akey": akey, "rkey": rkey, "accepts": accepts[:12]}


def _in_quotes(s, pos):
    return (s[:pos].count('"') % 2 == 1 and '"' in s[pos:]) or (
        s[:pos].count("“") > s[:pos].count("”") and "”" in s[pos:])


def _clauses(body):
    """One bracket of an answer line as its directives, in order. Semicolons separate them; so does a new "accept" or
    "prompt" with no semicolon ("accept Mayor Pete, prompt on Peter"). A directive word that only continues the one
    before it does not start a new one: in 'do not prompt on or accept "Planet Earth"' the "accept" is still
    forbidden, and reading it as its own directive would list a rejected answer as accepted."""
    out = []
    for clause in re.split(r';["”’\']*', body):
        cuts = [0]
        for m in _DIRECTIVE.finditer(clause):
            if m.start() and not _in_quotes(clause, m.start()) and not _CONTINUES.search(clause[:m.start()]):
                cuts.append(m.start())
        out += [clause[a:b].strip(" ,") for a, b in zip(cuts, cuts[1:] + [len(clause)])]
    return [c for c in out if c]


def _core(w):
    """words of a folded name past any trailing Iberian/Catalan maternal surname (i Cornet, y Picasso) or Jr/numeral"""
    w = list(w)
    if len(w) >= 4 and w[-2] in ("i", "y"):
        w = w[:-2]
    return [x for x in w if x not in _SUFFIX] or w


def last(key):
    """the word a folded name ends on, past any Jr, numeral or maternal surname: what a fuller form still ends on"""
    core = _core(key.split())
    return core[-1] if core else ""


def nested(a, b):
    """One folded name inside the other and ending on the same word: "mies van der rohe" and "ludwig mies van der
    rohe", "wright" and "frank lloyd wright sr". Not "barcelona" and "barcelona chair", which end differently and
    are different things."""
    x, y = set(a.split()), set(b.split())
    return (x <= y or y <= x) and last(a) == last(b)


@functools.lru_cache(maxsize=1 << 18)
def _alike(w, v):
    """two words that are one word: an initial and its name (i / ieoh), or near-spellings (kasimir / kazimir)"""
    if w[0] == v[0] and 1 in (len(w), len(v)):
        return True
    if abs(len(w) - len(v)) > 2:
        return False
    m = difflib.SequenceMatcher(None, w, v)
    return m.real_quick_ratio() >= 0.8 and m.quick_ratio() >= 0.8 and m.ratio() >= 0.8


@functools.lru_cache(maxsize=1 << 20)
def near(a, b):
    """Two folded names that are the same name spelled or filled out differently: nested (above), or the words that
    differ are near-spellings (kasimir / kazimir) or initials of each other (i m pei / ieoh ming pei). Different
    first names (john adams / samuel adams) are not near."""
    x, y = set(_core(a.split())), set(_core(b.split()))
    if x <= y or y <= x:
        return last(a) == last(b)
    p, q = x - y, y - x
    if len(p) != len(q):
        return False
    return all(any(_alike(w, v) for v in q) for w in p)


_FILL = frozenset("the a an of s".split())
_SUFFIX = frozenset("jr sr i ii iii iv v vi vii viii ix x xi xii".split())
_TITLE_LINKERS = frozenset("and or et ed e und y sans senza with without".split())


def takes(accepts, want):
    """Does an answer line (its accepts, a list or the stored " | " string) take the folded answer `want`? True when
    one accepted answer holds every word of `want`, ends on the same word, is at most three words longer, and is not
    a pair. So "malevich" finds "kazimir severinovich malevich", and "immanuel kant" finds neither "immanuel kant s
    critiques" (ends elsewhere) nor "david hume and immanuel kant" (a pair)."""
    if isinstance(accepts, str):
        accepts = accepts.split(SEP)
    w = _core(want.split())
    ws = set(w)
    for a in accepts:
        t = [x for x in a.split() if x not in _FILL or x in ws]
        if not t or not ws <= set(t) or len(t) > len(ws) + 3 or ("and" in t and "and" not in ws):
            continue
        core = _core(t)
        # Surname shorthand is useful for people, but a title ending in the requested
        # word must not become the same answer ("Orfeo ed Euridice" != "Euridice").
        # Conjunctions and common title linkers distinguish these cases while leaving
        # personal-name particles such as van/de/der available to the name matcher.
        suffix_start = max(0, len(t) - len(w))
        title_suffix = len(w) == 1 and bool(_TITLE_LINKERS & set(t[:suffix_start]))
        if not title_suffix and (core[-1] == w[-1] or t[-1] == w[-1]):
            return True
    return False


# Named things
_STOP = frozenset("""a an the of in on at to for from by with as and or but nor so yet if then than that this these those
it its he him his she her they them their we our you your i me my who whom whose which what when where why how is are
was were be been being am do does did has have had having can could may might must shall should will would not no also
into onto over under after before during while about against between through one two three four five six seven eight
nine ten first second third other another each every some any many most more less much such only own same both all
there here very just up out off down again once s t points point name identify answer bonus tossup each""".split())
_OPEN = frozenset("""this these that those his her its their he she it they one a an the in at on for after before during
while when although despite because another other both each every some many most several along with by from as if
though since until unlike like to and but or so yet nor not no name identify give what which who whose where how why
there here all two three four five ten points point answer bonus tossup note according following later earlier early
late despite according upon among within without near under over through i""".split())
_CONN = r"(?:of|the|de|del|della|dei|di|da|du|des|la|le|les|el|al|von|van|der|den|ten|y|bin|ibn|ben|ap|zu)"
_CAPW = r"[A-Z][\w’'-]*"
_RUN = re.compile(r"%s(?:\s+(?:%s\s+){0,2}%s)*" % (_CAPW, _CONN, _CAPW))
# the same with the small words a title can hold (White on White, Victory over the Sun). No "and" (that would weld
# two titles in a list into one), and only title-like prepositions so clause bridges ("Einstein won a Nobel",
# "Performed by Thomas Young") are not proposed as single capitalised entities.
_WIDE = re.compile(r"%s(?:\s+(?:(?:%s|on|in|with|over|for|to|at|from|a|an|upon|under|without|into)"
                   r"\s+){0,3}%s)+" % (_CAPW, _CONN, _CAPW))
_ITAL = re.compile(r"<i>(.*?)</i>", re.S)
_SOUND = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)+")
_QUOT = re.compile(r'"([^"]{2,90})"')


def things(san, htm=""):
    """The named things in a stretch of question text: (kind, as printed) pairs, where kind is "title" (in italics in
    the formatted text, or in quotes), "name" (a run of capitalised words), or "open" (a single capitalised word at the
    very start of a sentence that did not recur capitalised mid-sentence). Deliberately generous: the counting in
    qbr.clues throws out what is not a true named entity."""
    out, seen, idx = [], {}, {}

    def add(kind, t):
        t = re.sub(r"\s+", " ", (t or "").replace("(*)", " ")).strip(" .,;:!?'\"“”’‘()[]")
        k = fold(t)
        if _SOUND.fullmatch(t) and re.search(r"[A-Z]{2}", t):
            return                                          # a pronunciation guide: REE-mun-shnai-dur
        if len(k) > 1 and not k.isdigit() and not all(w in _STOP for w in k.split()):
            if k in seen:
                if seen[k] != "title" and kind == "title":
                    out[idx[k]] = (kind, t)
                    seen[k] = kind
                elif seen[k] == "open" and kind != "open":
                    out[idx[k]] = (kind, t)
                    seen[k] = kind
                return
            idx[k] = len(out)
            seen[k] = kind
            out.append((kind, t))

    # qbreader often closes and reopens the italics inside one title: <i>Critique</i> <i>of Pure Reason</i>
    for t in _ITAL.findall(re.sub(r"</i>(\s*)<i>", r"\1", htm or "")):
        t = plain(t)
        if len(t.split()) <= 10:
            add("title", t)
    text = no_guides(san or "")
    for t in _QUOT.findall(text):
        if len(t.split()) <= 10:                            # room for "I heard a Fly buzz - when I died"
            add("title", t)
    for sent in sentences(text) or [{"s": text}]:
        for rx in (_RUN, _WIDE):
            for m in rx.finditer(sent["s"]):
                words = m.group(0).split()
                if m.start() == 0:
                    while words and (words[0].lower() in _OPEN or
                                     ("-" in words[0] and words[0].split("-", 1)[0].lower() in _OPEN)):
                        words = words[1:]
                while words and words[-1].lower() in _OPEN:
                    words = words[:-1]
                if rx is _WIDE and (len(words) < 3 or len(words) > 9):
                    continue
                if rx is _WIDE and "<i>" in (htm or "") and any(w.lower() in ("on", "in", "with", "for", "to", "at", "from", "into") for w in words):
                    continue
                if words and not (len(words) == 1 and (len(words[0]) < 3 or words[0].lower() in _OPEN)):
                    add("open" if (m.start() == 0 and len(words) == 1) else "name",
                        " ".join(words).replace("’s", "").replace("'s", ""))
    return out


def grams(folded, lo=2, hi=4):
    """word n-grams of a folded text that neither start nor end on a filler word"""
    w = folded.split()
    out = set()
    for n in range(lo, hi + 1):
        for i in range(len(w) - n + 1):
            if w[i] not in _STOP and w[i + n - 1] not in _STOP and not (w[i].isdigit() and w[i + n - 1].isdigit()):
                out.add(" ".join(w[i:i + n]))
    return out
