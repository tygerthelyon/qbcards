# Curated Quizbowl Sample Datasets

This directory contains representative, curated sample datasets formatted for spaced-repetition study and knowledge testing across three academic domains:

1. **`sample_fine_arts.json` (Visual Fine Arts Tier 1)**:
   * 30 world-famous artworks across Western and East Asian art history.
   * Fields: `title`, `artist`, `date`, `style`, `location`, `clue`, `notes`, and difficulty tags.
   * Demonstrates the multi-card model mapping artwork imagery to artist, title, and movement.

2. **`sample_philosophy.json` (Classical Philosophy)**:
   * 30 structured cloze flashcard notes covering Presocratics (Thales, Anaximander, Heraclitus, Parmenides) and Plato's dialogues.
   * Features progressive disclosure with `{{c1::...}}` cloze tossup blanks and `{{c2::...}}` bonus-level concept blanks.

3. **`sample_history.json` (World History Clues)**:
   * 30 atomic prompt-and-answer clues covering key historical figures, treaties, and dynasties.
   * Metadata includes period, country, entity classification, and contextual extra information.

## Schema Specification

### Fine Arts
```json
{
  "id": 1787890520242,
  "model": "Art",
  "title": "The Starry Night",
  "artist": "Vincent van Gogh",
  "date": "1889",
  "style": "Post-Impressionism; Oil on canvas",
  "location": "Museum of Modern Art, New York City",
  "clue": "A cypress tree looms in the foreground before a swirling night sky over Saint-Rémy-de-Provence.",
  "tags": ["Art::tier::tier1-core", "Art::nationality::dutch"]
}
```

### Philosophy Cloze
```json
{
  "model": "QB Cloze",
  "answerline": "Thales",
  "set": "Presocratics",
  "text": "{{c1::Thales::this thinker}} held that {{c2::water}} is the arche, the first principle of all things.",
  "source": "HoP 1",
  "tags": ["Philosophy::Classical", "Classical::Presocratics"]
}
```

## Importing into Anki

These JSON files can be imported directly into Anki using AnkiConnect (`addNotes` action) or converted to standard CSV/TSV format for the Anki Desktop file importer (`File > Import`).
