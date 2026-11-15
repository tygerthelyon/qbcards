# Sample Notes

A small JSON slice of the collection showing how note fields are structured across different subjects. For rendered card screenshots, see the [card gallery](../docs/card-gallery.md); for importable `.apkg` decks, see [`docs/decks.md`](../docs/decks.md).

| File | Notes | Contents |
| --- | ---: | --- |
| [`sample_fine_arts.json`](sample_fine_arts.json) | 27 | Works, artists, dates, locations, and stock clues |
| [`sample_philosophy.json`](sample_philosophy.json) | 30 | Short cloze notes on Presocratic philosophy |
| [`sample_history.json`](sample_history.json) | 30 | History and literature prompts with context fields |

Example record from `sample_philosophy.json`:

```json
{
  "model": "QB Cloze",
  "answerline": "Thales",
  "set": "Presocratics",
  "text": "{{c1::Thales::this thinker}} held that {{c2::water}} is the arche, the first principle of all things",
  "source": "HoP 1",
  "tags": ["Philosophy::Classical", "Classical::Presocratics"]
}
```

The matching note-type schemas and card stylesheets live in [`templates/models.json`](../templates/models.json).
