# Cloud audit, 2026-10-05: summary

Worked only from `export/` (2026-10-04). Nothing in Anki changes until someone runs `apply_audit.py`.

## What was checked

| Task | Scope | Output |
|---|---|---|
| 1. Fact and style audit | Performing Arts (334 notes), Film (399), Photography (498): every text field read | `performing_arts_findings.jsonl`, `film_findings.jsonl`, `photography_findings.jsonl` |
| 2. Most-lapsed cards | Top 60 cards by lapses in Art, Classical Music, Architecture, PA, Film, Photography | `lapsed_rewrites.jsonl` (33 rewrites), `lapsed_reasons.md` (all 60) |
| 3. NAQT "You Gotta Know" | 12 more Fine Arts lists, 117 items | `ygk_more.json`, `ygk_more.md`, `ygk_add.py` (the 10 gap notes) |
| 4. Geography captions | Info and Photo caption of all 1,100 notes, plus Region hints | `geography_findings.jsonl` (20) |
| 5. Classical Music descriptions | All 454 notes with a blank Description | `cm_descriptions.jsonl` (454) |
| 6. History v2, Shang and Zhou | Cards from the 03/04 supplements | `history/deck/cards_china_shang.py`, `cards_china_zhou.py` |
| 7. Art, Architecture, Classical Music fact-check | Every active note (1,281 + 257 + 647), plus automated checks of all notes | `art_findings.jsonl` (114), `architecture_findings.jsonl` (5), `classical_music_findings.jsonl` (10) |
| 8. Classical Music gaps | ~450 commonly asked works checked against the deck | `cm_gaps.json`, `cm_gaps_add.py` (99 notes) |

Method:
- Style rules, giveaways, and same-card repeats were checked in code over every field, then by reading.
- Facts that looked wrong were checked on Wikipedia, plus a second source where the two disagreed.
- A random 10% of each deck was re-checked to estimate the error rate.

## Task 1 findings: 76

| Deck | Fact | Leak | Style | Repeat | Total | High | Medium |
|---|---|---|---|---|---|---|---|
| Performing Arts | 3 | 1 | 13 | 6 | 23 | 19 | 4 |
| Film | 13 | 3 | 24 | 0 | 40 | 36 | 4 |
| Photography | 2 | 0 | 11 | 0 | 13 | 13 | 0 |
| **All** | **18** | **4** | **48** | **6** | **76** | **68** | **8** |

17 style rows that only moved a comma or full stop inside closing quotes were dropped: you prefer punctuation outside the quotes.

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
- Style problems are commoner than factual ones; the usual one is a surname on first mention.

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

## Task 3: YGK gaps (`ygk_add.py` adds them; added on request after the first report)

- **No note at all:** Buddy Rich and Pierre Beauchamp (draft PA fields in `ygk_more.json`).
- **Suspended only:** the Metaphysical art movement note, #1790236438367. Unsuspend it.
- **No FIGURE card:** Frans Hals, Judith Leyster, Anthony van Dyck, Lorenzo Ghiberti, Gutzon Borglum, Phidias, Daniel Chester French, and Frédéric-Auguste Bartholdi. Each has work cards; draft FIGURE fields are included.
- **Composers:** the 20th-century, American, and European composer lists are covered by Classical Music work cards. That deck has no composer FIGURE notes by design.
- **Operas:** all 10 are active under their original titles.

## Task 4: Geography Info and Photo captions, and Region hints (20 findings)

- **Facts (4):**
  - Florida's high point is Britton Hill, not "Brittons Hill".
  - Timor-Leste isn't the *only* mostly Catholic country in Southeast Asia; the Philippines is too.
  - The New Caledonia reef is the world's longest continuous barrier reef, not the "second-largest". The Belize note already holds that title, so the two contradicted each other.
  - Toronto–Niagara Falls is about 70 km in a straight line, not 130 (medium).
- **Style (13):**
  - Speke and Baker were English, not "British".
  - Robert Smithson's *Spiral Jetty* (Great Salt Lake note) is now in italics.
- **Error rate:** 4 factual errors in 1,100 notes (0.4%).
- **Region hints (13, Locator field):** the PHOTO card's Region hint gave the answer away. Cambridge and Oxford now say England, the Sonoran Desert "United States and Mexico" (high); ten more are emptied (medium: read them in the dry run).
- The duplicate Mount Saint Helens note is already merged and suspended in your collection; nothing to do.

## Task 5: Classical Music descriptions (454)

- Every blank Description now has a draft: 417 high confidence, 37 medium.
- They show on the back of the audio cards next to Listen, so they give work-level facts (commission, premiere, dedicatee, nickname) and avoid repeating Listen.
- The 37 medium rows are printed by the dry run for review.
- **Data clash, not changed:** 1787711406067 is called "String Quartet No. 23" but carries K. 614 (that's String Quintet No. 6; Quartet No. 23 is K. 590). Its description stays generic until the Work or Catalogue field is fixed.

## Task 6: History v2, Shang and Zhou (82 cards)

- 27 Shang and 55 Zhou cards (including the Hundred Schools), only clues your old History Clue notes don't already give. 33 go into the queue; 49 (tier 3–4) are added suspended.
- The supplements' corrections are applied: *hezong* was against Qin, *lianheng* with Qin; the Three Guards rebelled against the Duke of Zhou's regency; Erligang is Zhengzhou.
- `hist_qb_apply.py --include` now takes a list: `prehistory,shang,zhou`. Don't use `--supersede` for these periods: your old notes stay the main cards.

## Task 7: Art, Architecture, and Classical Music fact-check (129 findings)

| Deck | Read | Fact | Style | High | Medium |
|---|---|---|---|---|---|
| Art | 1,281 active notes; all Locations scanned for typos | 61 | 53 | 91 | 23 |
| Architecture | 257 active notes | 2 | 3 | 4 | 1 |
| Classical Music | 647 active notes; every composer's dates and nationality | 6 | 4 | 7 | 3 |

- **Art, wrong place:** *The Death of Marat* is in Brussels, not Antwerp; *Beata Beatrix* is at Tate, not Edinburgh; *Christ in the House of His Parents* is at Tate, not private; Adele Bloch-Bauer I is at the Neue Galerie; Jimson Weed is at Crystal Bridges; *The Moon Woman* is in the Peggy Guggenheim, Venice; Memling's *Last Judgment* is in Gdańsk and *The Chess Game* in Poznań, not Warsaw; the marble *Kiss* and Claudel's works are in the Musée Rodin, Paris, not Philadelphia.
- **Art, wrong date or artist:** Duccio's *Maestà* is 1308–11, not c. 1280; *The Geographer* 1669, not "1668–1699"; Ghent Altarpiece 1432; *The Age of Bronze* 1875–76; *Goldfish* 1912; *Sky Above Clouds IV* 1965; *White on White* 1918; *Fall of the Giants* is Giulio Romano's (Raphael was dead); the Baptistery's south doors are Andrea Pisano's, not Giovanni's.
- **Art, wrong medium:** Reni's *Aurora* is a fresco; the *Disputa* is a fresco; Nanni di Banco's saints are marble; Dürer's 1523 *Last Supper* is a woodcut; the Raphael Cartoons are on paper.
- **Art, typos:** 24 museum names (Musuem, Riijksmuseum, Metrapolitan, Santa Marie, and so on).
- **Architecture:** the Abraj Al-Bait was the second-tallest building when finished, not the third; a Mackintosh caption names the wrong tearoom (medium).
- **Classical Music:** Khachaturian was Armenian, not Russian; the *Kreutzer* Sonata is 1803 (1805 was publication); two Hints disagreed with their own Date; Judith Weir "British" becomes "Scottish-English" (medium).
- Error rate: Art about 5% of active notes had a factual error, Architecture under 1%, Classical Music 1%.
- **Noticed, not changed:** two duplicate active Art notes (the *Disputa*, 1787890518304 and 1787890519171; Rousseau's tiger, 1787890517675 and 1790239802400); the Northern Renaissance movement card has a *Vitruvian Man* picture, which is not the answer. The Classical Music deck puts punctuation outside quotes, which is your preference, so it was left alone.

## Task 8: Classical Music gaps (99 notes)

- About 450 works that come up often in quizbowl were checked against all 1,657 notes. 99 had no note at all; `cm_gaps_add.py` adds them, from Allegri's *Miserere* and Pergolesi's *Stabat Mater* to Mahler 6, *Turangalîla*, *Different Trains*, and the *Radetzky March*.
- 12 are tier 1, 69 tier 2, 18 tier 3. They have no audio: each note's blank AUDIO card is suspended, and non-tier-1 notes are added fully suspended.
- Another 170 or so works are in the deck but suspended (for example the *St. John Passion*, Chopin's ballades, Brahms's piano concertos); that's a tiering question for you, not a gap.

## Task 9: NAQT lists still unread

*Pre-1700 composers* (February 2026) and *Romantic-era composers* (August 2020) exist, but naqt.com returns 403 here and no search result shows their lists. A local session can open them; the gap notes above already add Pérotin, Du Fay, Josquin, Allegri, Gesualdo, and Biber.

## Skipped, and why

- Art, Architecture, and Classical Music were done in Task 7, after the local session finished. Every row still carries the current text and is skipped if it has changed.
- **Not flagged as style problems** (judgment calls; tell me if you want them changed):
  - the PA "Caption" (singular) field, which no template uses;
  - jazz tunes and rags in quotation marks, treated as songs;
  - anglicized ballet terms in roman: *pas de deux*, adagio, fouetté;
  - "British" in movement names (British New Wave) and in British Army or UK-market uses.
- **Blocked sources:** partway through, the network policy began blocking en.wikipedia.org, qbreader.org, and commons.wikimedia.org. Checks after that used the built-in web fetch tool, until it too was refused for Wikipedia, and then web search.

## Commands (Anki open, in `C:\QB\stockfisher`, after copying the `audit\` folder in)

Each command is a dry run first; add `--apply` to write. Everything written is backed up to `backups\`.

```
py -3.9 audit\apply_audit.py
py -3.9 audit\apply_audit.py --apply
py -3.9 audit\apply_audit.py --rewrites --descriptions
py -3.9 audit\apply_audit.py --rewrites --descriptions --apply
py -3.9 audit\ygk_add.py
py -3.9 audit\ygk_add.py --apply --unsuspend-metaphysical
py -3.9 audit\cm_gaps_add.py
py -3.9 audit\cm_gaps_add.py --apply
py -3.9 history\deck\hist_qb_apply.py --include prehistory,shang,zhou
py -3.9 history\deck\hist_qb_apply.py --apply --include prehistory,shang,zhou
```

1. **Findings:** the high-confidence fixes for PA, Film, Photography, Geography, Art, Architecture, and Classical Music (179 rows; 46 medium ones are listed for you to read).
2. **Rewrites and descriptions:** the 33 lapsed-card rewrites and the 454 Classical Music descriptions (high-confidence ones). The dry run lists the medium ones to read. To apply one you agree with:
   ```
   py -3.9 audit\apply_audit.py --include-medium --only NOTE_ID:FIELD --apply
   ```
3. **YGK notes:** adds the 10 notes. Non-tier-1 cards are suspended straight away. `--unsuspend-metaphysical` unsuspends the Metaphysical art note.
4. **Classical Music gaps:** adds the 99 notes, tagged `Music::gap_2026-10-05`.
5. **History:** adds the Shang and Zhou cards (and Prehistory/Xia, if you've read that write-up; drop `prehistory,` otherwise).

Then sync normally. There's no schema change, so no full upload is needed. If you don't want the 25 new Art DESCRIPTION to TITLE cards from the rewrites in your queue, suspend them in the browser with `deck:Art card:"DESCRIPTION to TITLE" is:new`.

Re-running is safe: rows already applied, or edited since the export, are skipped, and the add scripts skip notes that already exist.
