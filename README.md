# QBCards & StockFisher

## StockFisher

StockFisher downloads the [QBReader](https://www.qbreader.org/) question database into a local SQLite index (671,413 tossups and bonus parts across 716 sets as of November 2026) and extracts the recurring stock clues for any answerline. Each clue shows how many questions on the answer use it, how unique it is to that answer (the share of every question holding those words that is about this answer), where it falls in a tossup (in power, middle, giveaway, or bonus only), and its usual difficulty. Clues are ranked by importance, questions × uniqueness, so a classic clue asked twenty times outranks a one-off and a clue unique to the answer outranks a common word. Other wordings of the same clue are folded into one card.

![StockFisher showing recurring clues for the photoelectric effect alongside a full source question](docs/images/stockfisher-app.png)

Clicking any clue card opens the full tournament question beside your results with the matching sentence highlighted. If Anki is open with AnkiConnect, StockFisher also checks your collection and marks each clue as studied, a card not yet studied, suspended, written on the answer's own note, only mentioned in another note, or missing. You can also test a draft clue for answer giveaways or export a shortlist to CSV.

### Setup

Requires Python 3.9+ and uses only the standard library (no `pip install` step). The first sync downloads the corpus from QBReader and builds the local FTS5 index (~900 MB):

```bash
git clone https://github.com/tygerthelyon/qbcards.git
cd qbcards
python -m qbr sync
python -m qbr.app
```

On Windows, double-clicking `Open StockFisher.cmd` opens the app in a standalone Chrome or Edge window. Run `python -m qbr sync` whenever you want to pull newer tournament sets. If you already keep `qbreader.sqlite` in another folder, click Index in the top right to point the app at it, or set `QBR_DB` in your environment.

See [`docs/stockfisher.md`](docs/stockfisher.md) for a walkthrough of the app, or [`qbr/README.md`](qbr/README.md) if you prefer running queries from the terminal or Python scripts.

## Anki decks

The collection has 11,921 notes and 34,848 cards built over five years of study, covering visual art, architecture, classical music, geography, biology, physics, philosophy, and history.

| Art: front | Art: back |
| --- | --- |
| ![Front of the Fur Traders Descending the Missouri card](docs/images/cards-v2/art-front.png) | ![Back of the Fur Traders Descending the Missouri card](docs/images/cards-v2/art-back.png) |
| Classical music: front | Classical music: back |
| ![Classical music card front](docs/images/cards-v2/music-front.png) | ![Classical music card back](docs/images/cards-v2/music-back.png) |
| Ranked list: front | Ranked list: back |
| ![Ranked list card front](docs/images/cards-v2/list-front.png) | ![Ranked list card back](docs/images/cards-v2/list-back.png) |
| Geography: front | Geography: back |
| ![Sichuan map card front](docs/images/cards-v2/geography-sichuan-front.png) | ![Sichuan map card back](docs/images/cards-v2/geography-sichuan-back.png) |

More examples across all 11 note types are in the [card gallery](docs/card-gallery.md).

Packaged `.apkg` files are available on the [releases page](https://github.com/tygerthelyon/qbcards/releases/tag/decks-2026-11-12); see [`docs/decks.md`](docs/decks.md) for the subject breakdown. The repository also includes [sample JSON notes](samples/), [card templates and stylesheets](templates/models.json), and the [maintenance scripts](scripts/) used to keep formatting consistent across decks.

## Buzz Drill

A tossup reader for practising on real questions. It has two modes:

- **Deck Drill** reads 1,905 tossups on 695 answers from the study collection. Pick categories, question count, and reading speed, buzz with `Space`, press `G` to mark a guess, and score yourself. Questions you heard in the last 30 days are skipped.
- **Pack Analysis** plays a whole tournament set in pack order, tossups or bonuses. Upload a set as QBReader-format question JSON (or a `.zip` of pack files), then review every buzz on **Buzzpoints** and your performance on **Stats**.

![Buzz Drill setup screen](docs/images/buzz-drill.png)

Stats use standard quizbowl measures: conversion (correct ÷ tossups heard), BPA (buzz point AUC, 0–100: conversion at every point of the question, summed), points per 20 tossups heard (PP20TUH), and points per bonus (PPB), with breakdowns by category, pack, and buzz timing.

![Buzz Drill pack stats: conversion, BPA, and correct-by-buzz-depth chart for a full set](docs/images/buzz-drill-pack-stats.png)

To run it, start the local server and open the page it prints (<http://127.0.0.1:8788/>):

```bash
python drill_server.py --open
```

On Windows, double-clicking `launch_drill.pyw` does the same in an app window. The server saves every buzz, bonus, and session to `data/drill/` (one file per set, never committed), so results survive closing the browser. If Anki is open with AnkiConnect, the server also marks which answers are already in your collection. Served by any plain web server instead (`python -m http.server`, then open `/drill/buzz-drill.html`), the page runs Deck Drill in standalone mode and keeps results in the browser.

## Tests & attribution

Offline unit tests run with `python -m unittest discover -s tests -v`. A fuller regression suite (`python -m qbr.selftest`) also checks a synced database against the live QBReader API.

Questions indexed by StockFisher and used in Buzz Drill come from [QBReader](https://www.qbreader.org/) and are available on its public database; see [QBReader's notes on question sources](https://github.com/qbreader#questions). Code in this repository is under the [MIT License](LICENSE); artwork, maps, audio clips, and question text in the decks and examples remain under their respective rights.
