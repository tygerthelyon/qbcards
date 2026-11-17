# Anki Decks

The [16 November 2026 release](https://github.com/tygerthelyon/qbcards/releases/tag/decks-2026-11-16) packages the collection into `.apkg` files by subject. Download the subjects you want and import every file of a subject into Anki. Media, note types, and card templates are included; review history is stripped, so every card arrives as new.

| Package | Subject | Cards (suspended) |
| --- | --- | --- |
| `AFA.apkg` | Classical music (with audio clips) | 4,857 (4,408) |
| `Geography.apkg` | World and regional geography | 2,608 (593) |
| `OVFA-1.apkg`, `OVFA-2.apkg` | Architecture, dance, design, film, and photography | 5,367 (3,722) |
| `VFA-1.apkg`, `VFA-2.apkg`, `VFA-3.apkg` | Painting and sculpture (Visual Fine Arts) | 15,249 (11,214) |

## Importing

In Anki's import screen, tick **Import any learning progress** and **Import deck presets**. Those two boxes carry over:

- **Study order**: cards I have already learned come first, in the order I learned them, then the new cards in my queue order. Cards of one note stay together.
- **Suspensions**: later tiers arrive suspended, so you can unsuspend topics as you reach them.
- **Deck options**: each deck's own preset, with its learning steps, daily limits, new-card order, and FSRS settings.

Without them, Anki imports the cards in the same order but unsuspends everything and applies its default options.

`OVFA` and `VFA` are split by deck to keep each file under GitHub's 2 GB limit. Each part is a complete package with the media its cards use; import all parts for the whole subject.

## How the packages are made

[`scripts/export_friend_apkg.py`](../scripts/export_friend_apkg.py) exports a deck through AnkiConnect, strips review history, records the study order in each card's position, and copies in the deck's preset. [`scripts/split_friend_apkg.py`](../scripts/split_friend_apkg.py) splits a large export into importable parts and checks that every note, card, suspension, and media file lands in exactly one part.

Decks currently being built out or reorganized:
- Poetry
- History (East Asia, South America, and US)
- Other Auditory Fine Arts (opera, musicals, jazz, and world/folk music)
