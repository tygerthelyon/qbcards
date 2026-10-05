# Cloud audit, 2026-10-05: summary

Worked only from `export/` (2026-10-04). Nothing in Anki changes until someone runs `apply_audit.py`.

## What was checked

| Task | Scope | Output |
|---|---|---|
| 1. Fact and style audit | Performing Arts (334 notes), Film (399), Photography (498): every text field read | `performing_arts_findings.jsonl`, `film_findings.jsonl`, `photography_findings.jsonl` |
| 2. Most-lapsed cards | Top 60 cards by lapses in Art, Classical Music, Architecture, PA, Film, Photography | `lapsed_rewrites.jsonl` (33 rewrites), `lapsed_reasons.md` (all 60) |
| 3. NAQT "You Gotta Know" | 12 more Fine Arts lists, 117 items | `ygk_more.json`, `ygk_more.md` |

Method:
- Style rules, giveaways, and same-card repeats were checked in code over every field, then by reading.
- Facts that looked wrong were checked on Wikipedia, plus a second source where the two disagreed.
- A random 10% of each deck was re-checked to estimate the error rate.

## Task 1 findings: 93

| Deck | Fact | Leak | Style | Repeat | Total | High | Medium |
|---|---|---|---|---|---|---|---|
| Performing Arts | 3 | 1 | 17 | 6 | 27 | 23 | 4 |
| Film | 13 | 3 | 29 | 0 | 45 | 41 | 4 |
| Photography | 2 | 0 | 19 | 0 | 21 | 21 | 0 |
| **All** | **18** | **4** | **65** | **6** | **93** | **85** | **8** |

Notable fixes:
- **PA:**
  - Anna Leonowens was Anglo-Indian, not "Welsh-born" (*The King and I*).
  - Frederick Loewe was born in Berlin, not Austria (two clues).
  - *Guys and Dolls* clue said "doll".
- **Film:**
  - *Spirited Away* is no longer the *only* hand-drawn non-English animation Oscar winner (*The Boy and the Heron* has since won).
  - Scorsese and De Niro have made ten films together, not nine.
  - Eight of Murnau's films are lost, not eleven.
  - Billy Wilder was raised in Vienna, not born there.
  - Hitchcock popularized "MacGuffin"; he didn't coin it.
  - The offer to destroy the *Citizen Kane* negative came from Louis B. Mayer, not Hearst.
  - Jiří Menzel was 30 at the Oscars, not 28.
  - Clues for *The Great Dictator*, *Sex, Lies, and Videotape*, and *The Bridge on the River Kwai* named words from their own titles.
  - 14 newer notes had italic `<i>` Title and Original title fields, against the Film house rule.
- **Photography:**
  - The Zapruder film was 8 mm, not 35 mm.
  - "the Louis Lumière brothers" corrected to "the Lumière brothers".
  - Surname-only people in the movement notes now have full names.

Error rate:
- Facts in the random samples:
  - PA: 0 of 33 notes.
  - Film: 2 of 40 (5%).
  - Photography: 0 of 50.
- Across the full read:
  - PA: 3 factual errors in 334 notes (0.9%).
  - Film: 13 in 399 (3.3%).
  - Photography: 2 in 498 (0.4%).
- Style problems are commoner than factual ones. The usual ones are a comma or full stop outside closing quotes, and a surname on first mention.

The 8 medium findings need your eye; the dry run prints them with sources:
- three "British" → "English" changes where it means the ballet scene or the state;
- a replacement Notes line for Ella Fitzgerald;
- *A Matter of Life and Death* "Foreign Office";
- Falconetti's "only film role";
- the *Kind Hearts and Coronets* "eight relatives";
- the *River Kwai* rewording.

## Task 2: lapsed cards

The lapse data is thin:
- Only 95 of 22,855 cards in these six decks have ever lapsed: 2 cards twice, the rest once.
- The 60 cards belong to 58 notes: 29 Art, 28 Architecture, and 1 Photography.
- No Classical Music, PA, or Film card made the list.

Rewrites:
- **Art (25 rewrites):** the notes had no Clue. Each gets one tossup clue.
  - The clue shows above the title on TITLE to ARTIST cards.
  - Adding it also **creates each note's DESCRIPTION to TITLE card** (new cards, not changes to existing ones).
- **Architecture (8 rewrites):** DEFINITION to NAME cards get a single-clue Description. Clerestory is now told apart from triforium, and Art Nouveau from Art Deco.
- **No rewrite (25 notes):** picture or name cards whose Description is back-only, plus three generic-title Art works best suspended. Reasons are in `lapsed_reasons.md`.
- Listen fields: none touched, and the script refuses to write any.

## Task 3: YGK gaps (no apply script, as asked)

- **No note at all:** Buddy Rich and Pierre Beauchamp (draft PA fields in `ygk_more.json`).
- **Suspended only:** the Metaphysical art movement note, #1790236438367. Unsuspend it.
- **No FIGURE card:** Frans Hals, Judith Leyster, Anthony van Dyck, Lorenzo Ghiberti, Gutzon Borglum, Phidias, Daniel Chester French, and Frédéric-Auguste Bartholdi. Each has work cards; draft FIGURE fields are included.
- **Composers:** the 20th-century, American, and European composer lists are covered by Classical Music work cards. That deck has no composer FIGURE notes by design.
- **Operas:** all 10 are active under their original titles.

## Skipped, and why

- **Geography Info and Photo captions:** dropped to stay within the credit budget.
- **Art, Classical Music, and Architecture fact-checks:** the local session is auditing them, as instructed. Task 2 still touches Art and Architecture text; every row carries the current text and is skipped if it has changed.
- **Not flagged as style problems** (judgment calls; tell me if you want them changed):
  - the PA "Caption" (singular) field, which no template uses;
  - jazz tunes and rags in quotation marks, treated as songs;
  - anglicized ballet terms in roman: *pas de deux*, adagio, fouetté;
  - "British" in movement names (British New Wave) and in British Army or UK-market uses.
- **NAQT lists not read:** *Pre-1700 composers* and *Romantic-era composers* are unchecked, and *early-20th-century European composers* is only partly read (Bartók, Debussy, Ravel). naqt.com returns 403 here, and those pages aren't in the search index.
- **Blocked sources:** partway through, the network policy began blocking en.wikipedia.org, qbreader.org, and commons.wikimedia.org. Checks after that used the built-in web fetch and search tools instead, which reached the same sites.

## Commands (Anki open, in `C:\QB\stockfisher`, after copying the `audit\` folder in)

```
py -3.9 audit\apply_audit.py
py -3.9 audit\apply_audit.py --apply
```

The first command is a dry run: it lists the 85 high-confidence writes and the 8 medium ones. The second writes the high-confidence findings and backs up every field to `backups\audit_<time>.json`. To apply some medium ones after reading them:

```
py -3.9 audit\apply_audit.py --include-medium --only 1788490082095:Notes --apply
```

For the Task 2 rewrites, dry-run first, then apply:

```
py -3.9 audit\apply_audit.py --rewrites
py -3.9 audit\apply_audit.py --rewrites --apply
```

After that, sync normally. There's no schema change, so no full upload is needed. If you don't want the 25 new Art DESCRIPTION to TITLE cards in the queue, suspend them in the browser with `deck:Art card:"DESCRIPTION to TITLE" is:new`.

Re-running is safe: rows already applied, or edited since the export, are skipped.
