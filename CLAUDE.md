# Carter's quizbowl Anki collection — read this first

Copy this file into `C:\QB\stockfisher\` and Claude Code loads it automatically, so a session never has
to read the 350 KB `CHECKLIST.md` to get oriented. **Current state and open work: `STATUS.md`.** Read
CHECKLIST.md only for the history of one specific thing (grep it, don't read it whole).

## Setup
- The collection is driven through **AnkiConnect on localhost:8765**; Anki must be open. Helpers are in
  `concept_add.py`: `anki(action, **params)`, `plain()` (strip HTML), `fold()` (normalise and deaccent),
  `leaks(name, text)`.
- **`python` is not on PATH — use `py -3.9`.**
- Running log: `CHECKLIST.md` (newest entries at the bottom, `## Wnnn`). Audit log: `AUDIT_2026-09-26.md`.
- Old one-off scripts and contact sheets are in `archive/` (8 GB). Ask before deleting any of it.
- Backups of field values go to `backups/` (or `%LOCALAPPDATA%\QB_field_backups\`) **before** any bulk edit.

## House rules (learned the hard way)
- **Measure before acting; dry-run before applying.** Every tool takes `--dry` / `--apply`.
- **Read the card template before concluding anything from field contents.** Fields can be hidden behind
  `{{^Suppression}}` gates or `display:none`.
- **Look at every image before uploading it** (PIL contact sheet, then actually view it). Automated checks
  have passed paintings, engravings, and wrong-subject photos.
- **Pictures: at least 1000 px on the long side, everywhere.** Use Wikimedia thumbnails at the standard
  widths (960, 1280, 1920), one connection at a time, with UA contact `carteryott@icloud.com`
  (Wikimedia only).
- The picture must show **the card's answer**, never a stand-in from the same period. No picture or
  caption on a front may print the answer.
- **No fluff:** context and straight facts, not poetic description or padding. Full names for people who
  aren't household names.
- **Tiers**: tags `<Deck>::tier::tier1-core | tier2-solid | tier3-deepcut | tier4-rare`, with decks Art,
  Music, Photo, PA, Architecture, History, Film. **Never tier Geography.**
  - Tier 1 is tight. The best-known work of an obscure artist beats the tenth work of a famous one.
  - Change a tier only on certifiable evidence (`qb_tier_model.py`), never a blanket promotion.
- Only tier-1 cards are normally active; the rest are suspended.
- **Flash cards stay flash cards:** one thing to recall per card, one clue per card, as tossups give it.
- Titles of works in *italics* (captions too); sung numbers in "quotes"; Canadian spelling; Oxford comma.
- Night mode uses `html:has(> body.night_mode) …` / `.night_mode …` — **never** `:root:not([data-theme])`.
- After a schema change, Carter must do a **full sync / upload to AnkiWeb by hand**. Tell him.
- After template changes that blank cards: tell Carter to run **Tools > Empty Cards**.

## How Carter works
- He's on Windows; deck folder `C:\QB\stockfisher`; repo `github.com/tygerthelyon/qbcards` (cloud sessions
  work from it and can't reach Anki).
- He wants to be told plainly what changed and what he has to do. Short reports.
- Cloud sessions prepare data and `--dry/--apply` scripts in the repo. The local session (or Carter
  himself) runs them with `py -3.9 <script> --apply`, which costs no Claude tokens.
