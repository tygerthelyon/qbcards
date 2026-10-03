# Status — 2026-10-03

A two-page summary of where the collection stands, so new sessions don't have to read all of
`CHECKLIST.md` (W1–W126) and `AUDIT_2026-09-26.md`. Update it at the end of each session.

## Done recently (details in CHECKLIST, by W number)
- **W117 (09-25)** — `qb_tier_model.py` was changed to work on any subcategory and run on Art, Classical
  Music, and Photography.
  - Applied: 30 Classical Music works promoted to tier 1, 21 demoted to tier 3.
  - Art and Photography left alone: the evidence for changing their tiers wasn't strong enough.
  - Film stills now come from TMDB (the key is in `.tmdb_key`).
- **W120 (09-26)** — BISE (VFA pdf) is complete; Classical Music now has DESCRIPTION → WORK cards; 68 Art
  FIGURE cards were added.
- **W121 (09-27)** — every Geography card was read through; Architecture details fixed; maps v4.
- **W122 (09-28/29)** — Geography review (photos, flags, regions, list cards); Music audio fixes.
- **09-29 (audit file)** — Film, Performing Arts, and Photography overhaul.
  - The Film canon gaps were filled: Antonioni, *Ran*, and others.
- **10-01 (audit file)** — Performing Arts: *Brigadoon*, *Heathers*, *Brilliant Corners*.
  - Film: the directors Rivette, Terence Davies, Lynne Ramsay, and Miranda July; actor cards, including
    Dietrich and Mastroianni.
- **W123 (10-01)** — map label rules; every Architecture work has at least 2 pictures; Classical Music
  italics and Movement forms; Art captions.
- **W124 (10-02)** — Classical Music written for quizbowl.
  - `cm_qb_apply.py` rewrote Listen and Clue for all 486 live notes, from clip analysis plus 10,414
    qbreader questions.
- **W125–126 (10-02)** — Architecture foreign names in italics; Geography pictures all 1000 px+;
  broken-media scan.
- **10-02/03** — pictures under 1000 px are being replaced deck by deck. `five_pictures_1003.py` is the
  latest script.

## Open — needs Carter
- **Tools > Empty Cards**, then sync. This clears the blank DESCRIPTION → WORK cards and the PA/Photo
  leftovers.
- **8 suspended Photography notes** (`Photo::suspended_0929`): delete or keep.
- **Clips to supply**:
  - *Music for 18 Musicians* (Reich) and *Gesang der Jünglinge* (Stockhausen).
  - *Porgy and Bess* — its clip is speech, not "Summertime" (tag `Music::clip_speech_1002`).
- **Full sync / Upload to AnkiWeb** after any schema change (the History v2 note types are one).

## Open — work for a session
- **Pictures under 1000 px:** finish the sweep (`images_audit_1002.py` lists them). Ronchamp has no
  large photo yet, and Louis Le Vau has only one.
- **Classical Music `Description` backlog:** the tier 3/4 works that are still blank. Blocked: a cloud
  session needs `export/` from `export_for_cloud.py`.
- **Music:** Mahler 1's funeral march, *The Sorcerer's Apprentice*, and the *Barcarolle* have no usable
  free recording. *La bohème*'s "Mimi 2" clip is unidentified.
- **Coverage ideas from the audit:**
  - common-link answer types;
  - non-Western canon (Fan Kuan's *Travelers among Mountains and Streams*: only 3 qbreader hits, so it
    stays suspended);
  - the Performing Arts "Venue" field holds record labels on album cards.

## History deck v2 (new, 10-03) — `history/`
- `history/notes/01_supplement_mythology_literature.md` — qbreader gaps and corrections for the verified
  part of my notes (Mythology → Classics).
- `history/notes/02_prehistory_xia_writeup.md` — a rewrite of Prehistory and the Xia (not yet verified).
- `history/deck/` — design (`DESIGN.md`), the note types QB Clue / QB List / QB Tossup, 230
  mythology/literature cards plus 49 prehistory/Xia, pictures, and `hist_qb_apply.py` (dry run by default).
- To apply:
  - copy `history\` into `C:\QB\stockfisher\history\`;
  - run `py -3.9 history\deck\hist_qb_apply.py`, then `--apply`;
  - optionally `--supersede --apply`, to suspend the old History Clue notes on the same topics.

- Three History v2 pictures are still under 1000 px (no larger free copy found yet): Hou Yi (Xiao Yuncong
  woodcut), the Red Cliffs inscription photo, and the Wu Song Long Corridor painting.
- Bonus: `history/notes/03_shang_supplement_bonus.md` — the same qbreader gap sweep for the Shang.
- Practice page: China Buzzer Drill, https://claude.ai/artifact/NhJ6vwwAPa8MBByw4rBk4p (491 qbreader tossups).

## Tools worth knowing (in `C:\QB\stockfisher`; only some are in the repo)
`qb_tier_model.py` (tiers from qbreader), `qb_coverage_test.py` (what share of real answers the deck has),
`concept_add.py` (helpers and leak check), `cm_qb_apply.py` (Classical Music text),
`images_audit_1002.py`, `img_upgrade_1002.py` (picture upgrades), `export_for_cloud.py` (text export for
cloud sessions).
