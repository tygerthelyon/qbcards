# QBCards & StockFisher

Tools for studying and practicing quizbowl: a searchable question mirror, a buzzer drill, and the card models behind a large Anki collection.

| Project | What it does |
| --- | --- |
| [StockFisher](qbr/) | Indexes QBReader questions in SQLite and finds recurring clues, shared answers, and gaps in an Anki collection. |
| [Buzz Drill](drill/) | Streams tossups word by word, tracks buzz position, and saves self-scored practice sessions in the browser. |
| [Anki models and samples](samples/) | Shows how the collection is organized, from visual arts cards to philosophy and history notes. |

![Buzz Drill setup screen, showing categories, session length, and reading speed](docs/images/buzz-drill.png)

## StockFisher

Quizbowl questions are pyramidal: harder clues come first, with more familiar clues later. StockFisher searches a local [QBReader](https://www.qbreader.org/) mirror for recurring clues and reports how often they occur, how widely they are shared, and where they tend to appear in a tossup. Answerline parsing handles accepted alternatives and moderator instructions. Optional AnkiConnect integration compares results with existing notes; it reads the collection without changing it.

The November 2026 mirror contained **671,413 answerable units from 716 sets**. The database is built locally and is not included in this repository. Counts depend on the last sync, and suggested clues need human review: a frequent association is not by itself proof of a fact or a unique answer.

```bash
git clone https://github.com/tygerthelyon/qbcards.git
cd qbcards

# Download and index the QBReader corpus; the first sync is large.
python -m qbr sync

python -m qbr profile "photoelectric effect" -c physics --spec
python -m qbr search "pendentives" -c architecture -d 7-9
python -m qbr who "zero of form"
```

Python 3.9+ and SQLite with FTS5 are required. The first sync needs internet access and extra disk space while the database is built; the resulting mirror is roughly 900 MB. Later searches run against the local mirror. See the [StockFisher guide](qbr/README.md) for filters, Python usage, Anki integration, and limitations.

## Buzz Drill

The included practice pool contains 1,864 tossups selected for the study collection. Choose categories and a reading speed, buzz with **Space**, then reveal the answer and score yourself. Session history stays in browser storage.

Serve the repository locally so the browser can load the question data:

```bash
python -m http.server 8000
```

Open <http://localhost:8000/drill/buzz-drill.html>. The drill does not require the StockFisher mirror or Anki.

## The collection

The personal Anki collection spans physics, biology, fine arts, geography, history, philosophy, and other subjects. A November 2026 audit counted **11,921 notes and 34,848 cards**; many cards are deliberately suspended until earlier material has been studied. The repository contains [small JSON samples](samples/) and [note-type definitions](templates/models.json), not the full collection, its media, or ready-to-import deck packages. Collection-specific [backup and maintenance utilities](scripts/) are included too.

## Tests

Run the offline parser and temporary-database tests with:

```bash
python -m unittest discover -s tests -v
```

The larger `python -m qbr.selftest` compares a synced mirror against the live QBReader API. It needs both the local database and a network connection.

## Question sources

The drill pool and StockFisher mirror draw on questions made available through QBReader. Question text remains the work of its writers and tournament hosts; see [QBReader's description of its question sources and non-commercial use](https://github.com/qbreader#questions). The mirror is not bundled here.
