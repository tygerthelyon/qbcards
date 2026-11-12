# qbr

A local copy of every qbreader question, with a searcher on top. It replaces StockFisher 1.0 and the hand-written
`urllib` fetches in the dated scripts. It does not replace qbreader.org for ordinary searching; it does what the site
cannot: count, compare, and answer in milliseconds without the network.

Run everything from `C:\QB\stockfisher` with `py -3.9`.

## Commands

```
py -3.9 -m qbr profile "Kazimir Malevich"         the stock clues for an answer (--spec, --pyramid)
py -3.9 -m qbr profile "John Adams" -c afa --anki  the composer only, marked against the Anki collection
py -3.9 -m qbr search "zero of form" -c vfa -d 7-9
py -3.9 -m qbr who "zero of form"                 which answers a clue points to
py -3.9 -m qbr top -c architecture -n 100         frequency list; --rising, --anki, --missing
py -3.9 -m qbr fact "Bury St. Edmunds|eel"        fact check
py -3.9 -m qbr like "a white fish obscures the image of a tuxedoed man"
py -3.9 -m qbr sets "ACF Nationals"               sets in the mirror
py -3.9 -m qbr set "2026 ACF Nationals" -c vfa    one set's questions, in packet order
py -3.9 -m qbr show <id or uid>                   one whole question; --html keeps the italics
py -3.9 -m qbr brief "OVFA::Dance" -t 1 -c fa     agent briefing: notes' existing clues + missing stock clues
py -3.9 -m qbr sql "SELECT ..."                   read-only SQL
py -3.9 -m qbr sync                               update the mirror;  status  says how fresh it is
```

Filters, on most commands: `-c` category (`vfa`, `phil`, `architecture`, `"Other Fine Arts"`, several with commas),
`-d` difficulty (`7`, `7-9`, `hs`, `college`), `-y` year (`2018-`, `2015-2020`), `-s` part of a set name, `-t tossup`
or `bonus`. `--json` prints the raw result.

Difficulty is qbreader's: 5 = HS nationals, 6 = one dot, 7 = two, 8 = three, 9 = four, 10 = open.

## Reading a profile

```
    n  +m  tied  levels  where     clue
   16   1   58%  3-10    giveaway  Black Square  (title)
```

- **n**: questions on this answer that use the clue. This is the stock-clue ranking (or use `--spec` to weight by exclusivity, `--pyramid` to order from lead-in/power to giveaway).
- **+m**: other answers' questions that say it of this answer.
- **tied**: of everything in the mirror that holds the clue, the share that involves this answer. Near 100% means
  the clue is unique to it; a low figure means the clue is shared, so a card built on it alone is ambiguous.
- **levels**: the lowest and highest difficulty it appears at.
- **where**: where it tends to fall in a tossup, from lead-in to giveaway (`*` marks clues appearing before the power mark `(*)` in >=50% of tossups).

`who "<clue>"` is the same question from the other side: every answer line the clue sits under.
`qbr.verify_clue(answer, clue_text)` checks a drafted flashcard clue for name leaks, length, term uniqueness (`tied`), and closest corpus sentences.

## Search syntax

Plain words are tried as a phrase, then as all-words-anywhere. Otherwise:

| write | to get |
|---|---|
| `"black square" tatlin` | both, anywhere in the unit |
| `suprematism OR suprematist`, `supremat*` | either; any ending |
| `malevich -tatlin` | without |
| `NEAR(malevich vitebsk, 15)` | within 15 words |
| `ans:malevich "zero of form"` | answer line holds one, clue text the other |
| `--in answer` | search answer lines only |
| `--re "arkhitekton(a\|s)?"` | a regular expression (a full scan, a few seconds) |

Matching ignores case, accents and punctuation.

## From Python

```python
import qbr
p = qbr.profile("Hagia Sophia")              # dict; p["things"] is the ranked clue list
hits = qbr.search("pendentives", cat="architecture", n=20)["hits"]
qbr.who("built by Anthemius of Tralles")     # [{answer, n, share, first, last}, ...]
qbr.top(cat="vfa", diff="7-9", sort="rising")
pool = qbr.rows(cat="Philosophy", kind="tossup")     # every unit, as dicts
mine = qbr.rows(answer="Immanuel Kant")              # only those it answers
con = qbr.db()                               # the SQLite connection, read-only
```

Each function's docstring lists what it returns. `qbr.api` is the live qbreader client (retries, paging, and the
split that gets past qbreader's 10,000-row paging ceiling) for anything not yet in the mirror.

## The mirror

`qbr/data/qbreader.sqlite`, about 900 MB, not in git. Tables:

- `q`: one row per question. `body` holds the formatted text (bold, underline, italics), compressed;
  `qbr.store.body(con, qid)` reads it.
- `u`: one row per answerable unit, which is a tossup or one part of a bonus. `part` is 0 for a tossup, 1 to 3 for
  a bonus part; a bonus's lead-in is on part 1. `main` is the answer as printed, `akey` its folded key, `rkey` the
  underlined (required) part, `accepts` every answer the line takes. This is the table to count over.
- `f`: the full-text index over `u.text`, `u.lead`, `u.accepts`. `sets`: one row per set.

`sync` fetches sets the mirror lacks, drops sets qbreader no longer lists, and re-fetches sets from the last year
whose question count changed. `sync --full` re-fetches everything (about eight minutes). `sync --reparse` re-derives
the answer columns after a change to `text.parse_answer`, with no download.

## Anki

`--anki` reads the collection through AnkiConnect and marks each clue or answer `card` (a note is named this and has
an active card), `suspended`, `on-note` (inside the target answer's own note), `text` (only mentioned inside another
note) or `-` (nowhere in the collection). Short `Title`, `Work`, `Name`, `Answerline`, and `Term` fields are indexed as
note names; acronyms separated by middle dots normalize to their unseparated spelling. It never writes. The index is
cached for twelve hours in `qbr/data/anki_index.json`.

For work notes with a populated creator field, `brief` profiles exact QBR answerlines and suppresses creator names
already shown on the card. It prints the matched QBR answerlines and suppressed names so an empty or filtered brief
is easy to audit. This reduces alternate-answer collisions; it does not resolve missing canonical aliases, which
still need an explicit alternate or a separate related-answer lookup.

## Limits worth knowing

- An answer is matched by name. "John Adams" is both the president and the composer; use `-c`, `--not coolidge`, or
  `--exact`. The `answer lines:` row of a profile shows what was matched.
- Named things are proposed by pattern (italics, quotes, capitals) and kept by count. A clue with no name in it shows
  only if its wording recurs.
- qbreader's older sets have no italics or underlining, so titles there are found by capitals alone.
- The mirror is as fresh as the last `sync`; commands warn after three weeks.

## Files

`text.py` folding, answer lines, sentences, named things · `api.py` live client · `store.py` mirror and sync ·
`find.py` the searches · `clues.py` stock clues (`qbr.profile`) · `anki.py` the read-only Anki index · `__main__.py` command line ·
`selftest.py` regression checks (`py -3.9 -m qbr.selftest`)
