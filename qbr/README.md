# `qbr` ? StockFisher CLI & Python API

`qbr` is the indexing and clue-extraction engine behind StockFisher. It mirrors questions from the QBReader API into a local SQLite database with FTS5 (`qbr/data/qbreader.sqlite`, ~900 MB) so searches, frequency lists, and clue rankings run offline in milliseconds.

Run `python -m qbr sync` once from the repository root to build the database. For the standalone desktop UI, run `python -m qbr.app` (or `Open StockFisher.cmd` on Windows); see [`docs/stockfisher.md`](../docs/stockfisher.md).

## CLI commands

```bash
python -m qbr profile "Kazimir Malevich"          # stock clues ordered by importance
python -m qbr profile "John Adams" -c afa --anki  # the composer, diffed against Anki
python -m qbr search "zero of form" -c vfa -d 7-9
python -m qbr who "zero of form"                  # answers associated with a clue
python -m qbr top -c architecture -n 100          # answer frequency list (--rising, --anki, --missing)
python -m qbr fact "Bury St. Edmunds|eel"         # passages containing both terms
python -m qbr like "a white fish obscures the image of a tuxedoed man"
python -m qbr sets "ACF Nationals"                # tournament sets in the mirror
python -m qbr set "2026 ACF Nationals" -c vfa     # questions in packet order
python -m qbr show <id or uid>                    # one full question (--html keeps italics)
python -m qbr brief "OVFA::Dance" -t 1 -c fa      # compare existing Anki notes with stock clues
python -m qbr sql "SELECT ..."                    # read-only SQL against the mirror
python -m qbr sync                                # fetch new sets; `status` prints mirror age
```

Most commands accept the same filter flags:
- `-c` category (`vfa`, `phil`, `architecture`, `"Other Fine Arts"`, or comma-separated `vfa,ofa`)
- `-d` difficulty (`7`, `7-9`, `hs`, `college`, `open`; levels 6?9 correspond to 1?4 college dots, 10 is open)
- `-y` year (`2018-`, `2015-2020`)
- `-s` set name substring
- `-t` question type (`tossup` or `bonus`)
- `--json` raw JSON output

## Reading a CLI profile

```text
    n  +m  tied  levels  where     clue
   16   1   58%  3-10    giveaway  Black Square  (title)
```

- `n`: questions on this answer that use the clue. Default `--spec` ranking orders clues by importance across frequency/exclusivity (`n`, `tied`, `lift`), tossup position (`pos`, `power`), and difficulty (`davg`). Pass `--pyramid` to sort strictly from lead-in to giveaway.
- `+m`: questions on other answers that mention this clue alongside the target answer.
- `tied`: share of all occurrences of the clue across the mirror that involve this answer. Near 100% means the clue uniquely identifies the answer; a low percentage means the clue is shared across several topics.
- `levels`: lowest and highest difficulty (`dmin`?`dmax`) at which the clue appears.
- `where`: median position in a tossup (`lead-in`, `early`, `middle`, `late`, `giveaway`, or `bonus`). An asterisk `*` marks clues that appear in power (`(*)`) at least half the time.

## Search syntax

Plain words are searched first as an exact phrase, then as all words anywhere in the question unit. FTS5 operators also work directly:

| Query | Matches |
| --- | --- |
| `"black square" tatlin` | Both terms in the same unit |
| `suprematism OR suprematist`, `supremat*` | Boolean OR / prefix wildcard |
| `malevich -tatlin` | First term without the second |
| `NEAR(malevich vitebsk, 15)` | Within 15 words of each other |
| `ans:malevich "zero of form"` | Answerline matches `malevich`, clue text matches `"zero of form"` |
| `--in answer` | Search answerlines only |
| `--re "arkhitekton(a\|s)?"` | Full-table regex scan (takes a couple of seconds) |

## Python API

```python
import qbr

p = qbr.profile("Hagia Sophia")                      # dict; p["things"] is the ranked clue list
hits = qbr.search("pendentives", cat="architecture", n=20)["hits"]
qbr.who("built by Anthemius of Tralles")             # [{answer, n, share, first, last}, ...]
qbr.top(cat="vfa", diff="7-9", sort="rising")
pool = qbr.rows(cat="Philosophy", kind="tossup")     # all matching units as dicts
mine = qbr.rows(answer="Immanuel Kant")              # units with this answer
con = qbr.db()                                       # read-only sqlite3.Connection
```

## Database schema (`qbr/data/qbreader.sqlite`)

- `q`: one row per question (`qid`, `set_name`, `year`, `difficulty`, `category`, `subcategory`, and zlib-compressed HTML `body`).
- `u`: one row per answerable unit (`part = 0` for a tossup, `1..3` for bonus parts). Holds `main` (printed answer), `akey` (normalized key), `rkey` (underlined required core), and `accepts` (all accepted alternates).
- `f`: FTS5 full-text index over `u.text`, `u.lead`, and `u.accepts`.
- `sets`: packet metadata and sync timestamps.

## Module layout

- `text.py`: accent folding, answerline parser, sentence splitter, and named-entity/title extractor.
- `api.py`: QBReader HTTP client (handles pagination and splits queries that exceed QBReader's 10,000-row cap).
- `store.py`: SQLite schema, incremental `sync`, and `--reparse`.
- `find.py`: FTS5 search, answer tallies (`top`), and reverse clue lookup (`who`, `like`, `fact`).
- `clues.py`: stock-clue extraction, deduplication, and importance ranking (`profile`, `verify_clue`).
- `anki.py`: read-only AnkiConnect client and 12-hour local note index (`qbr/data/anki_index.json`).
- `app.py`, `ui.py`, `web/`: local loopback web server and standalone desktop UI.
- `selftest.py`: offline and live-API regression suite (`python -m qbr.selftest`).
