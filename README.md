# QBCards & StockFisher

Quizbowl study tools: a QBReader clue finder, a buzzer drill, and Anki note types and samples.

| Project | Description |
| --- | --- |
| [StockFisher](StockFisher.ipynb) | Finds recurring clues in QBReader questions and compares them with Anki notes. |
| [Buzz Drill](drill/) | Reads tossups word by word and records self-scored practice sessions. |
| [Anki models and samples](samples/) | Note types and examples from a collection spanning science, fine arts, history, and other subjects. |

## StockFisher

StockFisher searches a local [QBReader](https://www.qbreader.org/) mirror. For an answer, it ranks recurring clues by frequency, specificity, or position in a tossup; it can also show where those clues appear in an Anki collection. The November 2026 mirror contained 671,413 answerable units from 716 sets.

[Open the notebook](StockFisher.ipynb) to see the inputs and an interactive interface for profiling clues, searching questions, checking a draft, and exporting results to CSV.

![StockFisher notebook showing a photoelectric effect clue profile](docs/images/stockfisher-notebook.png)

### Setup

Python 3.9+ and SQLite with FTS5 are required. Build the mirror with:

```bash
git clone https://github.com/tygerthelyon/qbcards.git
cd qbcards
python -m qbr sync
```

The first sync requires internet access and extra disk space; the finished mirror is roughly 900 MB. To run the notebook:

```bash
python -m pip install -r requirements-notebook.txt
python -m notebook StockFisher.ipynb
```

Run the notebook cells and select **Find stock clues**. If your mirror is elsewhere, enter its path in the notebook or set `QBR_DB` before starting Jupyter. Anki comparisons require AnkiConnect and do not change the collection.

The command-line tools use the same mirror:

```bash
python -m qbr profile "photoelectric effect" -c physics --spec
python -m qbr search "pendentives" -c architecture -d 7-9
python -m qbr who "zero of form"
```

Counts depend on the last sync. Review the source questions before using a suggested clue: frequency alone does not establish accuracy or a unique answer. The [StockFisher guide](qbr/README.md) covers filters, Python usage, and limitations.

## Buzz Drill

![Buzz Drill setup screen, showing categories, session length, and reading speed](docs/images/buzz-drill.png)

The practice pool contains 1,864 tossups selected for the study collection. Choose categories and a reading speed, buzz with **Space**, then reveal the answer and score yourself. Session history stays in browser storage.

Serve the repository locally:

```bash
python -m http.server 8000
```

Open <http://localhost:8000/drill/buzz-drill.html>. Buzz Drill does not require the StockFisher mirror or Anki.

## The collection

The Anki collection spans physics, biology, fine arts, geography, history, philosophy, and other subjects. A November 2026 audit counted 11,921 notes and 34,848 cards; many cards are suspended until earlier material has been studied.

This repository includes [sample notes](samples/), [note-type definitions](templates/models.json), and [collection utilities](scripts/). The full collection, media, and importable deck packages are not included.

## Tests

Run the offline tests with:

```bash
python -m unittest discover -s tests -v
```

`python -m qbr.selftest` also compares a synced mirror against the live QBReader API; it needs the database and a network connection.

## Question sources

StockFisher and Buzz Drill use questions made available through QBReader. The questions remain the work of their writers and tournament hosts; see [QBReader's notes on question sources and non-commercial use](https://github.com/qbreader#questions).
