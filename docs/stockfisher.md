# StockFisher Guide

StockFisher searches a local SQLite copy of QBReader questions to find recurring stock clues across tournament history. It runs as a local desktop web app on top of Python's standard library, with an optional CLI and Python API underneath.

## Starting & stopping the app

Once you have built the index (`python -m qbr sync`), start the interface from the repository root:

```bash
python -m qbr.app
```

On Windows, you can double-click `Open StockFisher.cmd`. Chrome or Edge will open a dedicated app window without browser toolbars; other setups open a tab in your default browser.

By default, the local server binds to `127.0.0.1:8766` so it never collides with AnkiConnect on `8765`. You can pass `--port` or `--no-browser` if needed:

```bash
python -m qbr.app --port 8767 --no-browser
```

To stop the background server when running from the Windows shortcut, open `Index` in the top right and click `Quit StockFisher` (or press `Ctrl+C` if running in a terminal).

## Profiling an answer

Type an artist, work, place, or concept into the search box and press `Enter`. Leaving the filters blank gives you the broadest picture first; you can narrow by category, difficulty, or year once you see what the corpus holds.

| Control | What it does |
| --- | --- |
| Category | Filter by one or more categories or subcategories (e.g., `Literature`, `Visual Fine Arts`, `Physics`). |
| Difficulty | Filter by preset (`High School`, `College`, `Open`) or specific QBReader levels (`1` through `10`). |
| Years | Under `More options`: e.g. `2018-`, `2015-2022`, or a single year. |
| Exclude answer terms | Under `More options`: comma-separated words to exclude when an answerline has collisions (e.g. `shark, diamond`). |
| Rank clues by | Under `More options`: `Importance` (default), `Frequency`, or `Clue position`. |
| Audit against Anki | Under `More options`: checks each clue against your open Anki collection via AnkiConnect. |
| Exact answerline match | Under `More options`: restricts the profile to exact answerline matches. |

### How clues are ordered

Quizbowl clues aren't all equally useful: a clue that only appears once in a four-dot packet shouldn't sit above a classic two-dot clue asked twenty times. By default, StockFisher organizes results in two layers:

1. Clues are bucketed by where they typically fall in a tossup: `Power` (lead-in and early clues), `Middle`, `Giveaways`, and `Bonuses`.
2. Within each bucket, clues are ordered by an importance score that weighs three factors together:
   - Frequency and exclusivity: how many questions on this answer use the clue (`n`), plus how strongly the clue points to this answer over the rest of the database (`tied` and `lift`).
   - Position: earlier tossup clues and reliable power clues receive a boost over late or bonus-only mentions.
   - Difficulty: clues that reach down into high school and regular college packets (`davg`, `dmin`?`dmax`) rank ahead of obscure open-only clues with similar raw counts.

If an answer goes by multiple names in the corpus, clickable `Alternates` chips appear under the heading so you can pivot to a specific variant.

## Reading source questions

Click any clue card to open the full source tossup or bonus in a side-by-side panel. The sentence containing the clue is highlighted and the matched terms are underlined. For bonuses, all three parts and their lead-in are shown together. Press `Escape` or click `×` to close the reader.

## Checking a draft clue & exporting

- `Check a draft` (top right of a profile) tests a clue you're writing against the corpus: it flags accidental answer-word giveaways, checks character length, and pulls the closest matching sentences from real packets.
- Ticking clue checkboxes (or `Select clues`) enables `Export CSV`, which downloads the selected clues along with their question counts, specificity ratios, tossup positions, example sentences, and packet citations.

## Anki coverage badges

When `Audit against Anki` is enabled under `More options` and Anki is running with AnkiConnect, each clue card shows its status in your deck:

| Badge | Meaning |
| --- | --- |
| `● In deck` | Covered by an active (unsuspended) card in your collection, or present on the target answer's own note. |
| `● In deck (suspended)` | A matching note exists in Anki, but all of its cards are currently suspended. |
| `○ Missing` | Not found on any audited note in your collection. |

## Keyboard shortcuts

- `Ctrl+K` (or `⌘K`): Focus and select the search bar.
- `Escape`: Close an open filter menu, the source question panel, or a modal dialog.
- `Enter`: Run the search.

## Scripting & notebook

The web app calls the `qbr` Python package directly:

```python
import qbr

profile = qbr.profile("Damien Hirst", cat="fa", sort="spec", top=15)
for clue in profile["things"]:
    print(clue["thing"], clue["n"], clue["where"], clue["example"])
```

If you prefer working in Jupyter, `StockFisher.ipynb` is also in the repository root (`python -m notebook StockFisher.ipynb`). For CLI commands and full-text search across answers (`python -m qbr search`), see [`qbr/README.md`](../qbr/README.md).
