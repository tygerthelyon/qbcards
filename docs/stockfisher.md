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
| Show Anki coverage | Under `More options`: marks each clue with its state in your Anki collection (see below). |
| Exact answerline match | Under `More options`: restricts the profile to exact answerline matches. |

### What the numbers mean

Each clue card shows:

- **Questions**: how many questions on this answer use the clue, in any of its forms. A surname counts with the full name (Stravinsky with Igor Stravinsky), plurals and spellings count together, and a fragment counts with its whole title only when it is nearly always that title.
- **% unique**: of every question in the mirror holding these words, the share that is about this answer (answers it or names it), whatever filters you set. 100% means the clue points only here.
- **Position**: where the clue itself falls in this answer's tossups. `In power` means it comes before the (*) in at least half of them; otherwise `Lead-in`, `Early`, `Middle`, `Late`, `Giveaway` (the "for 10 points" sentence) or `Bonus only`.
- **Level badge**: the median difficulty of the questions using the clue (hover for the range).
- **Also worded**: other wording of the same clue, folded into this card rather than listed again.

None of these is a standard quizbowl statistic; quizbowl has no agreed measure of clue importance.

### How clues are ordered

- `Importance` (default): questions × uniqueness, `(n + 0.35 m) × log(1 + lift) × (0.1 + 0.9 × tied^0.7)`, where `m` counts other answers' questions that say it of this answer and `lift` is how much more often it turns up here than across the mirror. A classic clue asked twenty times outranks a one-off, and a clue unique to the answer outranks a common word.
- `Frequency`: most questions first.
- `Clue position`: groups the clues as a tossup reads them: `Power`, `After power`, `Giveaway`, `Bonuses only`.

If an answer goes by multiple names in the corpus, clickable `Alternates` chips appear under the heading so you can pivot to a specific variant.

## Reading source questions

Click any clue card to open the full source tossup or bonus in a side-by-side panel. The sentence containing the clue is highlighted and the matched terms are underlined. For bonuses, all three parts and their lead-in are shown together. Press `Escape` or click `×` to close the reader.

## Checking a draft clue & exporting

- `Check a draft` (top right of a profile) tests a clue you're writing against the corpus: it flags accidental answer-word giveaways, checks character length, and pulls the closest matching sentences from real packets.
- Ticking clue checkboxes (or `Select clues`) enables `Export CSV`, which downloads the selected clues along with their other wordings, question counts, % unique, positions, levels, example sentences, packet citations and Anki state.

## Anki coverage badges

When `Show Anki coverage` is on, each clue card shows its state in your collection. The app reads Anki through AnkiConnect and keeps a copy for twelve hours; when Anki is closed it uses the last copy and says so.

| Badge | Meaning |
| --- | --- |
| `● Studied` | A note is named this clue and has an unsuspended card you have reviewed. |
| `◐ Card, not studied` | A note is named this clue and has an unsuspended card you have not reviewed yet. |
| `● Suspended` | A note is named this clue, but all its cards are suspended. |
| `◑ On its note` | Written on the answer's own note (back information), not a card of its own. `(suspended)` if that note's cards are all suspended. |
| `○ Only in another note` | The words appear in some other note's text. This is not coverage. |
| `○ Missing` | Nowhere in your collection. |

## Keyboard shortcuts

- `Ctrl+K` (or `⌘K`): Focus and select the search bar.
- `Escape`: Close an open filter menu, the source question panel, or a modal dialog.
- `Enter`: Run the search.

## Scripting

The web app calls the `qbr` Python package directly:

```python
import qbr

profile = qbr.profile("Damien Hirst", cat="fa", sort="spec", top=15)
for clue in profile["things"]:
    print(clue["thing"], clue["n"], clue["where"], clue["example"])
```

For CLI commands and full-text search across answers (`python -m qbr search`), see [`qbr/README.md`](../qbr/README.md).
