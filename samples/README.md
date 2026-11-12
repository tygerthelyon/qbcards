# Study-note samples

These files show a small cross-section of the larger Anki collection:

For rendered card examples, see the [gallery](../README.md#anki-cards).

| File | Records | Contents |
| --- | ---: | --- |
| [sample_fine_arts.json](sample_fine_arts.json) | 27 | Works, artists, dates, locations, and selected clues |
| [sample_philosophy.json](sample_philosophy.json) | 30 | Short cloze notes on early Greek philosophy |
| [sample_history.json](sample_history.json) | 30 | History and literature prompts with answer and context fields |

For example, a philosophy record contains an answerline and cloze-formatted text:

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

These are illustrative JSON records, not Anki deck packages. Importing them requires a matching note type and a conversion or import script that maps each record's fields. The [model definitions](../templates/models.json) are provided as a reference; they are not directly importable as an `.apkg`. Images, audio, and the full collection are not included.
