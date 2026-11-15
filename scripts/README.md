# Collection Scripts

Small maintenance scripts for my Anki decks. Most talk to a running Anki instance through [AnkiConnect](https://foosoft.net/projects/anki-connect/), default to a dry run, and only write changes when passed `--apply`.

- `concept_add.py`: shared AnkiConnect helper and note builder used across the fine arts and architecture decks.
- `caption_clean.py`: strips Wikipedia footnote markers (`[25]`, `[citation needed]`), leftover MediaWiki parser CSS, and overly long paragraphs from image captions across six decks.
- `figs_justify.py`: injects a lightweight layout script into Architecture and Art templates so multi-image cards scale each picture by aspect ratio into even, justified rows instead of wrapping awkwardly.
- `dot_fix.py`: normalizes middle-dot (`·`) spacing in movement/proponent lists to use a consistent `.qb-dot` span.
- `export_for_cloud.py`: exports note fields, card metadata, and templates to `scripts/export/` (gitignored) for offline inspection or backup.
- `anki_backup_to_onedrive.ps1`: PowerShell task script that copies the Anki media folder and latest `.colpkg` backup to a backup directory (`C:\AnkiBackup` by default).
