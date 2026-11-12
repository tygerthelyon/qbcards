# Collection utilities

These scripts were written for the accompanying Anki collection and use [AnkiConnect](https://foosoft.net/projects/anki-connect/) where noted. Review the note types and fields they expect before using them with another collection. The cleanup scripts default to a dry run and require `--apply` to make changes.

- `anki_backup_to_onedrive.ps1` copies the media folder and latest `.colpkg` backup to `C:\AnkiBackup` by default. Pass `-ProfilePath` and `-Destination` to choose other locations. The historical filename is kept for scheduled tasks; the destination is a local folder unless changed.
- `export_for_cloud.py` exports note fields, card metadata, and note types to `scripts/export/`. Exports are ignored by Git and should be reviewed before sharing.
- `concept_add.py`, `caption_clean.py`, `dot_fix.py`, and `figs_justify.py` are collection-specific helpers for note creation and card presentation.
