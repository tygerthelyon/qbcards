# QBCards & StockFisher

Study tool for academic quizbowl.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](#)
[![SQLite FTS5](https://img.shields.io/badge/sqlite-FTS5-green.svg)](#)
[![Anki Integration](https://img.shields.io/badge/anki-AnkiConnect-purple.svg)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](#)

---

## Overview

Quizbowl rewards recall, and real-world and canon coverage. The tools here provide a software to process, index, and learn academic tournament material:

* **StockFisher Engine (`qbr`)**: offline SQLite FTS5 search and clue frequency pipeline indexing public quizbowl question database. Profiles "stock" (recurring) clues, and their frequency and difficulty in under 3 seconds per query.
* **Tossup Simulator (`drill/`)**: web application simulating live question-reading with configurable reading speeds, keyboard buzzer interrupts, and session performance telemetry.
* **Anki Card Architecture (`templates/`, `samples/`)**: Anki flashcard models with responsive WebKit-compliant layouts.

---

## Architecture

```
                                  [ Quizbowl Canon / Question Corpus ]
                                                    │
                                                    ▼
   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
   │                                  StockFisher 2.0 Engine (qbr)                                   │
   │                                                                                                 │
   │  ┌───────────────────────┐      ┌─────────────────────────────┐      ┌───────────────────────┐  │
   │  │   Text & NLP Parser   │ ───► │      SQLite WAL + FTS5      │ ───► │    Clue Profiler      │  │
   │  │ Answerline directives │      │ 670k units · 700+ sets      │      │ Stock score, pyramid  │  │
   │  │ Compound surnames     │      │ Fast full-text search       │      │ position & uniqueness │  │
   │  └───────────────────────┘      └─────────────────────────────┘      └───────────────────────┘  │
   └────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    ▼
   ┌────────────────────────────────────────────────┴────────────────────────────────────────────────┐
   │                                     Applications & Practice                                     │
   │                                                                                                 │
   │  ┌────────────────────────────────────────────────────────┐  ┌───────────────────────────────┐  │
   │  │                 Interactive Buzz Drill                 │  │       Anki Spaced Repetition  │  │
   │  │ Real-time tossup streamer · Keyboard interrupt buzzer  │  │ Responsive card models (CSS)  │  │
   │  │ Session metrics · Accuracy by category · Misses log    │  │ Dynamic mosaic layout engine  │  │
   │  └────────────────────────────────────────────────────────┘  └───────────────────────────────┘  │
   └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. StockFisher 2.0 (`qbr`)

The `qbr` package provides offline search, clue extraction, and canon profiling. It replaces external API roundtrips with an indexed local mirror.

#### Key Features:
* **FTS5 Full-Text Search**: Optimized queries across question text, lead-ins, and answer lines.
* **Robust Answerline Normalization**: Custom parsing for complex tournament rubrics (`[accept any answer mentioning...]`, `[prompt on...]`, `_WHEN`, `_VAGUE`, `_UNDERLINED_META`, and hyphenated/Catalan/Spanish compound surnames like *Antoni Gaudí i Cornet*).
* **Clue Uniqueness (`who` & `profile --spec`)**: Quantifies whether a clue uniquely identifies a single subject or is shared across multiple canonical answers.
* **Pyramid Positioning**: Tracks where clues appear within tossups—from early power lead-ins to late giveaways.

#### CLI Usage:

```bash
# Profile stock clues for an answer line with pyramid positioning
py -3.9 -m qbr profile "Kazimir Malevich" --spec --pyramid

# Check clue uniqueness across the entire canon
py -3.9 -m qbr who "zero of form"

# Filtered search by category and difficulty
py -3.9 -m qbr search "pendentives" -c architecture -d 7-9

# Frequency ranking for top answers in a category
py -3.9 -m qbr top -c vfa -n 50 --rising

# Fact check two terms co-occurring in questions
py -3.9 -m qbr fact "Bury St. Edmunds|eel"
```

#### Python API:

```python
import qbr

# Extract ranked stock clues
profile = qbr.profile("Hagia Sophia")
for item in profile["things"][:5]:
    print(f"{item['n']:2d} hits | {item['tied']}% unique: {item['text']}")

# Search question units with structured filters
results = qbr.search("pendentive", cat="Architecture", diff="7-9")
print(f"Total hits: {results['total']}")

# Direct connection to the SQLite database
with qbr.db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM u")
    print(f"Total units indexed: {cursor.fetchone()[0]}")
```

---

### 2. Interactive Buzz Drill (`drill/`)

A client-side practice application designed to build buzzer reflexes on learned tossup material.

* **Word-by-Word Streaming**: Simulates realistic tournament reading speeds (configurable from 3 to 7 words per second).
* **Keyboard Buzzer Interrupts**: Hit `Space` to buzz, freezing the reader and opening the answer entry prompt.
* **Offline Telemetry**: Uses browser `localStorage` for session history, recording accuracy, power buzzes, and a persistent list of missed clues.
* **Zero Dependencies**: Pure HTML/CSS/JavaScript with responsive layout for desktop and mobile.

To use: open `drill/buzz-drill.html` directly in any modern browser.

---

### 3. Knowledge Architecture & Anki Models (`templates/`, `samples/`)

The repository includes custom Anki note types engineered for academic knowledge retention:

* **Visual Fine Arts & Architecture**: Multi-image figure cards with dynamic JavaScript mosaic layouts, caption management, and image zoom modals.
* **Classical Philosophy**: Structured cloze models supporting thinker-level answerlines (`c1`), bonus-level concepts (`c2`), and complete contextual lecture backs.
* **World History Cloze**: Cloze cards with bolded primary entities and detailed historical chronologies.
* **Night Mode Compliance**: Full support for Anki desktop and mobile night mode using CSS variables and WebKit-tested contrast ratios.

---

## Directory Structure

```text
qbcards/
├── qbr/                # StockFisher 2.0 query and profiling package
│   ├── clues.py        # Stock clue extraction algorithms
│   ├── find.py         # Fast FTS5 search queries
│   ├── text.py         # NLP folding, normalization, and answerline parser
│   ├── store.py        # SQLite mirror schema and sync operations
│   ├── api.py          # HTTP API client for upstream question databases
│   └── selftest.py     # Regression test suite
├── drill/              # Tossup buzzer simulator
│   ├── buzz-drill.html # Standalone drill web application
│   └── tossups.json    # Sample practice dataset
├── templates/          # Production Anki card models and CSS templates
│   └── models.json     # Card schemas, fields, templates, and styles
├── samples/            # Curated academic trivia datasets
│   ├── sample_fine_arts.json
│   ├── sample_philosophy.json
│   ├── sample_history.json
│   └── README.md       # Dataset schema documentation
├── scripts/            # Pipeline automation and verification tools
├── .gitignore          # Keeps large databases (>900MB), media, and local caches untracked
└── README.md
```

---

## Getting Started

### Prerequisites

* Python 3.9+
* SQLite 3.35+ (with FTS5 enabled)
* Anki with [AnkiConnect](https://foosoft.net/projects/anki-connect/) (optional, for direct card synchronization)

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tygerthelyon/qbcards.git
   cd qbcards
   ```

2. **Verify the environment:**
   ```bash
   py -3.9 -m qbr.selftest
   ```

3. **Launch the Buzz Drill:**
   Open `drill/buzz-drill.html` in your browser to start a practice session.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
