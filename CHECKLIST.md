# Outstanding checklist

Status: `[ ]` not started `[~]` in progress `[x]` done `[!]` blocked / needs Carter

## Architecture — specific cards flagged
- [x] A1 Trinity Church — images depict different things
- [x] A2 Göbekli Tepe — unclear what 2nd image shows
- [x] A3 Barrel vault — low quality images
- [x] A4 Fan vault — images too similar
- [x] A5 Spandrel — 2 of 3 images have the word written in them
- [x] A6 Doric order — image 1 reveals the word, image 3 poor quality
- [x] A7 Machicolation — image 3 says the name
- [x] A8 Mullion — says the name
- [x] A9 Atrium — bad images
- [x] A10 Stylobate — image 2 says the name
- [x] A11 Stalinist architecture STILL shows Stalin
- [x] A12 Leon Battista Alberti — duplicate images
- [x] A13 Kisho Kurokawa — bad images
- [x] A14 Tempietto — three pictures of the same thing
- [x] A15 Bublik Apartments — single image is left-aligned, not centred
- [x] A16 Statue of Liberty — left cropped, right not relevant
- [x] A17 Lotus Temple — three of the same
- [x] A18 NMAAHC — needs a better/more images
- [x] A19 Walt Disney Concert Hall — 2nd image bad
- [x] A20 Borobudur — 3rd image has text on it

## Failure mechanisms to sweep across ALL decks
- [x] M1 Images with the answer word written inside them (labelled diagrams)
- [x] M2 Duplicate / near-identical images on one card
- [x] M3 Low-quality images
- [x] M4 Images showing something other than the subject (all 22 same-angle batches + captioning sheets reviewed by eye)

## Architecture — text and data
- [x] B1 Western Wall year "0019" — strip leading zeros, render single-digit years as AD/CE
- [x] B2 Work cards must show architect/designer beside style, location, built (Vietnam Veterans Memorial → Maya Lin)
- [x] B3 Bramante description cuts off at "St." — sentence-splitter bug
- [x] B4 Major works should name the medium; italicise painting titles, e.g. *Christ at the Column* (painting)
- [x] B5 Tier chip collides with the line above Major Works (Andrea Palladio)
- [x] B6 Major Works renders BELOW the tier chip on figure cards
- [x] B7 Don't move the period below the "figure?" box on reveal — keep it in place
- [x] B8 Giulio Romano caption — *The Fall of the Giants* italic + title case
- [x] B9 "Secession" renders in a different font on the Otto Wagner card
- [x] B10 *The Harvest Moon* in the Mackintosh caption — italicise all painting titles in captions
- [x] B11 Bold the single most quizbowl-important term in figure descriptions
- [x] B12 Descriptions not specific enough to pin the person (Alvar Aalto)
- [x] B13 Figure cards: show captions BEFORE reveal when the work is named in the description (Eero Saarinen)
- [x] B14 Descriptions too long — one card should not test many facts
- [x] B15 Many images still have no caption
- [x] B16 Italics render oddly — *Delirious New York* on Rem Koolhaas — checked: the deck's italic serif, not a bug
- [x] B17 Baroque architecture detail is a run-on with errors — use bullet points; avoid long paragraphs everywhere
- [x] B18 Vierzehnheiligen not italicised — ALL foreign text in ALL fields, especially Alternate
- [x] B19 Drop non-Latin script foreign text as a rule (Cyrillic "Дом-бублик")
- [x] B20 Ospedale degli Innocenti not italicised
- [x] B21 Remove redundant alternates (Guggenheim Museum Bilbao; Rietveld Schröderhuis)
- [x] B22 Why is "Hope" italicised in the Walt Disney Concert Hall description
- [x] B23 Rietveld Schröder House description "Mrs. It…" — same cut-off bug as B3
- [x] B24 Katedrala sv. Jakova — "sv." is Croatian for "saint"; the card already carries "Cathedral of Saint James" as its alternate

## Styling
- [x] C1 Art deck's image outline is liked — try it on the other decks (done as N1)
- [x] C2 Captions missing on concept images (squinch); all images captioned on reveal unless named unambiguously in the text

## Art
- [x] D1 Grisaille has one image; every technique/style/movement card needs several

## Classical Music
- [x] E1 Layout — label above value (PERIOD above "Medieval") on the organum card etc.
- [x] E2 Audio examples for techniques and styles where possible
- [x] E3 Put the catalogue number beside the work title to free a row so Genre stops wrapping

## Geography
- [x] F1 Historical regions — add a line of history, not just the modern country (N17, P11)
- [x] F2 Abyssinia is tagged "historical flag" but shows a map
- [x] F3 Aconcagua-style maps — outlines soft, red dot too faint. Benchmark: the Adriatic Sea map's dot
- [x] F4 Chongqing / Córdoba city maps are poor
- [x] F5 Christmas Island "city map" is a picture of a crab

## Performing Arts
- [x] G1 Verify spacing on the cards

## Global rule
- [x] H1 Italicise paintings, sculptures, books and one-off architectural works.
      Do NOT italicise houses, churches, basilicas and other buildings.

## Carried over from before
- [x] Z1 Same-angle review — batches 11–23 of 24 still to review
- [!] Z2 Empty `media.trash` (7.41 GB) — blocked, needs Carter in Explorer

## Second round (2026-09-08)
- [x] N1 Restore image borders ("black boxes") on every deck — I had wrongly stripped them
- [x] N2 Click any image to enlarge, on all decks
- [x] N3 Replace click-through slideshows with side-by-side images
- [x] N4 Art: brackets no longer italic ([131 miniatures], [plate I]) — 24 fields
- [x] N5 Art: TITLE→ARTIST rebuilt — artist prominent, title a caption, no collision, tier normalised
- [x] N6 Art: series revealed on the answer only
- [x] N7 Art: movement cards given labelled sections like Architecture's
- [x] N8 Art/Photography concept captions (79 + 20)
- [x] N9 Architecture: Moscow Kremlin + Temple of Olympian Zeus descriptions rewritten
- [x] N10 Architecture: location card suppressed where the name gives the location
- [x] N11 Architecture: location card now features the location in the answer plate
- [x] N12 Architecture: WORK→ARCHITECT front rebuilt
- [x] N13 Geography: feature maps use the country, not the continent (Gullfoss → Iceland)
- [x] N14 Geography: cities keep the country map only (Monterrey, Melbourne)
- [x] N15 Geography: Cappadocia → Turkey locator; Pingyuan → historical region
- [x] N16 Geography: Source / Mouth / Borders / Subdivision facts added
- [x] N17 Geography: 82 historical regions given a line of history
- [x] N18 Performing Arts: card alignment made consistent
- [x] N19 Art: Balloon Dog + White Crucifixion — no larger copy exists (in copyright)
- [x] N20 Geography: city photo captions + pronunciation guides (superseded by P14)
- [x] N21 Geography: country maps use three different styles (see verification rollout)
- [x] N22 Art: Very Rich Hours / Giverny "series" wording
- [x] N23 B12–B14 description specificity and length
- [x] N24 Z1 same-angle review, batches 11–23
- [!] N25 "Revert UG deck images" — see note; my replacements are higher-resolution

## Third round (2026-09-08)
- [x] P1 Always reveal what is actually being asked — audited all 24 templates;
      3 genuinely buried the answer and were rebuilt (Art MOVEMENT→FIGURES, the
      PRB card Carter named; Architecture PICTURE/NAME→STYLE; WORK→ARCHITECT)
- [x] P2 Works italicised in captions everywhere — 53 captions across
      Architecture, Art and Photography; a final sweep on 2026-09-18 caught
      10 stragglers (Architecture 5, Art 3, Geography 2) and a re-run of
      caption_works_italic.py --dry now reports 0 in every deck
- [x] P3 Geography: information missing or incomplete — 827 descriptions and
      ~950 facts written from Wikipedia and Wikidata; 18 river-system/ambiguous
      names left as they were. Every article matched to its note was checked
      (0 wrong-parent matches after fixing Acre → unit of area, Hidalgo/Basque
      Country → disambiguation pages)
- [x] P4 Geography: new facts — Part of, Waters, Elevation; Subdivision row no
      longer duplicates the "In" label
- [x] P5 Geography: reveal layout — descriptions now bullets like Architecture;
      facts row held to the description's width instead of spread edge to edge;
      Subdivision row renamed so a city no longer says "In" twice
- [x] P6 Geography: city images — every photo reviewed on contact sheets. 49 of
      119 cities replaced with their defining landmark (Sydney Opera House,
      Alhambra, Château Frontenac, Potala Palace…), each checked by eye; Kano's
      first pick was rejected because a sign on it names the city. ~55 non-city
      photos found wrong or useless and queued: French frigate for Aquitaine,
      Michigan office block for Livonia, road signs spelling out Occitania and
      Jervis Bay, blank tiles for Bengal/Persia/Odisha
- [x] P7 Geography: captions on every image (merged into P14)
- [x] P8 Iguazu Falls "elevation says 1 metre" — no elevation field existed on
      that note — "Elevation 1 m." had been glued onto the description. Cause:
      P2044 is height above sea level, meaningless for a waterfall. All 8 falls
      now show their drop in a new Height row (Iguazu 82 m); stats moved out
      of prose into fields; implausible numbers refused
- [x] P9 Update the checklist after every pass
- [x] P10 "My Notes" — no such deck, tag, field, flag or marked card on this
      computer. If it was made on another device it needs a sync, which I have
      not run (note-type changes force a full one-way sync; see report)
- [x] P11 Redirect failure (new mechanism): Persia → Iran article gave a historical
      region modern Iran's area, "Existed 1979" and description. Audited all 1063;
      5 genuine (Burma, Ceylon, Persia, Republic of China, Siam) rewritten by hand;
      9 single-year "Existed" values (successor-state founding dates) corrected
- [x] P12 Namesake maps: Formosa's map was a municipality in Goiás, Brazil → now
      Taiwan's; swept every map filename, no others
- [x] P13 Foreign names italicised in the new photo captions (14); the automatic
      detector was NOT extended to captions — it italicised Tomáš Masaryk (a
      person) and Ponte City (English)
- [x] P15 Non-city photos: 54 replaced after review (Persepolis for Persia, Winter
      Palace for Russian Empire, Carcassonne for Occitania, Konark for Odisha…);
      Guanajuato kept its old image (no landmark photo resolved)
- [x] P16 "In: Italy" on the Adriatic — features crossing borders now list every
      country (146 fixed; the enrichment script now does this itself)
- [x] P17 Formal state names shortened (People's Republic of China → China, 67 notes)
- [x] P18 16 unresolvable notes (river systems like "Amazon – Ucayali – Apurimac",
      Lake Albert, Jeju…) given explicit articles and filled; coordinates stripped
      from descriptions
- [x] P19 One-line stub descriptions ("Overseas territory of France.") extended with
      where the place is — dry run in progress
- [x] P14 Captions on the ~500 remaining photos — writing (English-only; Spanish
      Commons descriptions refused)

## Recovered "My Notes" (SynapsePro add-on, recovered from notebook.sqlite)
- [x] R1 Art: Glazing and Scumbling use the same image (scan also found Pop art/Precisionism,
      Cubism/Orphism, Minimalism/Suprematism, Conceptual art/Readymade, Northern
      Renaissance/Pentimento, Lithography/Mezzotint/Screenprint)
- [x] R2 Art: "from the [language] for [word]" — put the word in quotation marks
- [x] R3 Art: a technique must be self-evident from the image or described in text;
      Pentimento and wet-on-wet don't make clear what is being asked
- [x] R4 Art: Repoussé 3rd image is weird
- [~] R5 Art: every technique needs several images — Foreshortening, Lost-wax (16 cards have ≤1)
- [x] R6 Art: technique images captioned on reveal (see below)
- [x] R7 Art: Fête galante needs its accent and italics; all foreign-language text italic
- [x] R8 Art: "Pietà" is not a technique — check every card's label
- [x] R9 Architecture: bold key phrase in descriptions runs into the next word (no space)
- [x] R10 Architecture: Takatori Catholic Church description cut off ("…in 1995. It…")
- [x] R11 Architecture: Paolo Soleri image

### Recovered-notes pass — what was done
- R2 glosses quoted (Italian for "light-dark", Latin for "remember that you must die"…, 5)
- R3 32 techniques an image can't show (glazing, pentimento, alla prima, printmaking…)
  no longer get a picture-only card; they keep the definition card with text + images;
  the 32 blank card copies are suspended (Tools > Empty Cards can delete them)
- R4 Repoussé's Colombian mask removed; Mask of Agamemnon captioned
- R7 8 accents restored (Fête galante, Repoussé, Pietà, Trompe-l'œil…), 31 foreign
  names italicised (incl. Die Brücke); absorbed loanwords (fresco, collage) left roman
- R8 15 cards relabelled: Pietà/Odalisque/Memento mori → Subject, Vanitas → Genre,
  Tondo/Diptych/Triptych/Polyptych/Predella → Format, Kouros/Illuminated manuscript/
  Readymade/Cartoon → Object type, Tenebrism → Style
- R9 13 bold phrases given their missing space (12 Architecture, 1 Art)
- R10 Takatori caption rewritten; swept every caption: 34 more were cut off mid-sentence
  (my first trim mistook "St."/"(c."/"Sgt." for sentence ends — repaired from backup)
- R11 Paolo Soleri's caricature replaced with Arcosanti and Cosanti
- R1 duplicate images removed from the wrong card of each pair (Glazing/Scumbling,
  Cubism/Orphism, Minimalism/Suprematism, Pop art/Precisionism, Conceptual art/Readymade,
  the print-shop engraving on 3 printmaking cards); Orpheus paintings off Orphism;
  the image fill now refuses any picture already used on another card
- R5 multiple images: reviewed on two contact sheets; wrong picks removed (a decal
  advert on Decalcomania, geometry diagrams and the Last Supper on Foreshortening, a
  toilet-sign pictogram and a SANAA building on Minimalism, Orpheus paintings pulled
  from the *religion* article on Orphism, Rockwell on Regionalism, a Schwitters collage
  on Automatism). Named examples added: Titian + Vermeer (Glazing), two Turners
  (Scumbling), Braque + Picasso (Papier collé), two Caravaggios (Foreshortening),
  Böcklin (Symbolism), Ernst (Decalcomania). Still short: Minimalism (2, both Judd),
  Arte Povera, Art Informel, Neo-expressionism (post-war work is under copyright, few
  free images)
- R8 applied across decks too: Photography 8 (FSA → Program, The decisive moment →
  Concept, Street photography → Genre…), Classical Music 15 (programme music → Concept,
  scales → Scale, Alberti bass/ostinato → Technique…; Idée fixe, musique concrète
  accented), Architecture 3 (stupa, ziggurat, torii → Building type), Geography 9
  (Northern Ireland → country; Hong Kong, Macau → SAR; French overseas regions)
- R5 (cont.) from Commons, chosen by eye: Štyrský + a modern decalcomania (Decalcomania
  now 3), Anselmo's *Torsion* (Arte Povera now 2), Flavin (Minimalism now 3, no longer
  two Judds). Papier collé stays at 1: the two Juan Gris candidates are catalogued as
  paintings, not papiers collés, so they were not added
- [x] R6 captions on every concept image — slot filler running over Art (125 empty) and
  Photography (52 empty)
- P10 resolved: "My Notes" was the SynapsePro add-on's notebook; text recovered from notebook.sqlite
- P14 done: 248 more Geography photos captioned; 94 left blank (no trustworthy match)
- P19 done: 73 stub descriptions extended
- [x] A2/A3/A9/A13/A16/A18/A19/A20 flagged Architecture images — reviewed on a contact sheet,
      replacements chosen by eye (Saint-Savin and Fontenay barrel vaults, a Pompeian atrium
      with impluvium, Göbekli Tepe enclosure + carved pillar, NMAAHC by day and night,
      Liberty Island); text-stamped, tiny and irrelevant pictures dropped; all captioned.
      Staged in arch_flagged_fix.py, runs once the caption/italics pass finishes
- [x] Z3 Low-resolution sweep: 93 of 1,535 Architecture pictures under 800 px — upgrade
      dry run (contact sheet first) in progress
- [x] R6 caption slots, second pass with Wikidata lead-image fallback, then per-caption
      italics (the old pass skipped a whole field if any caption was italic)
- Z3 (cont.) low-res upgrades: 33 candidates compared side by side with the picture they
  would replace; 6 applied (Arch of Constantine, Moscow Kremlin, Bernini, Ralph Adams
  Cram, Fazlur Rahman Khan, Great Zimbabwe), 27 rejected — most would have swapped a
  work for a portrait, or brought a wrong subject (Apollo Belvedere on Balanchine's
  *Apollo*, a flat flag graphic on Johns' *Three Flags*, Soleri's caricature again).
  Found on the way: Bernini's card showed a portrait labelled PIETRO BERNINI (his
  father); Cram's picture was a TIME cover and Khan's a sign printing the name.
  Wrong-person portraits and name-bearing images can't be swept without OCR — flagged
- 60 Architecture pictures under 800 px remain where no larger copy of the same subject exists
- [x] A2/A3/A9/A13/A16/A18/A19/A20 flagged Architecture images — applied: Göbekli Tepe
      (enclosure + carved pillar), Barrel vault (Saint-Savin, Fontenay), Atrium (Pompeian
      impluvium), NMAAHC (day + night), Statue of Liberty (Liberty Island), Borobudur /
      Kurokawa / Walt Disney Concert Hall bad pictures removed; every picture captioned
- R6 (cont.) concept-image captions: automatic passes filled 95; 60 more written by eye
  where the picture could be identified with certainty (Impression, Sunrise; Black Square;
  the Ghent Altarpiece; Migrant Mother…); ~41 left blank rather than guessed. Found on the
  way: Ambrotype and Collodion process shared a photo, New Objectivity showed a modern
  snapshot — both removed
- [x] T1 Italic titles never showed in Art/Photography concept captions: the script that
      pairs captions with pictures copied them as plain text, stripping <i>. Fixed in all 7
      templates (4 Art, 3 Photography) — the underlying reason "works italicised in captions
      upon reveal" kept failing on concept cards
- [x] T2 Definition-card pictures were squeezed into one narrow column at uneven heights (a
      grid nested inside a two-column grid); now side by side at one height, both decks
- R5 (Photography) multi-image fill: Gelatin silver print, Rule of thirds, Photo-Secession +1;
  Zone System, Straight photography, New Topographics have no further free images

## Standing rule (Carter, 2026-09-13): every failure → its mechanism → sweep all decks
Mechanisms found this pass, and the sweep for each:
- Caption script copied captions as plain text → italics stripped. Swept all templates: 7 fixed, 0 left.
- Picture grid nested in a two-column grid → pictures squeezed. Fixed on both decks that use it.
- Pictures that print the answer (cover, poster, sign, inscription). Swept every captioned picture:
  7 found, 6 removed (Surrealism manifesto, De Stijl journal page, lithography centenary poster,
  Memento mori gravestone, Blaue Reiter almanac, Fluxus poster; plus Photo-Secession poster and a
  "Rule of thirds" text page earlier). LIMIT: uncaptioned pictures can't be checked without OCR.
- Before-a-year italics rule took three-word names for titles (Sir John Herschel). Rule changed;
  all captions swept: 9 reverted, 2 of those restored as real titles (Just So Stories, Fading Away).
- Same work twice on one card as different scans; same picture on two cards outside Art.
  Sweep running over Art, Photography, Architecture.
- [x] Surrealism and Fluxus down to 1 picture after removals — fill running
- Duplicate sweep over Art, Photography, Architecture (the glazing/scumbling mechanism, every deck):
  · Art: 0 cross-card duplicates left; Lost-wax casting 2~3 are different stages, kept
  · Photography: Photomontage/Pictorialism shared Robinson's *Fading Away* → kept on Photomontage
  · Architecture element cards: Frieze/Triglyph, Tracery/Rose window, Stylobate/Cella shared photos →
    each kept on the card it illustrates; a labelled "Architecture Orders" diagram printed "stylobate"
    and "composite" → removed from both
  · Architecture architect/style cards repeating their building card's photo: 16 removed (Portland
    Building off Michael Graves, Fagus Factory off Bauhaus…); 4 handled by image match
  · 4 same-card duplicates created by my own low-res upgrades (the "larger copy" was already picture 1)
    → removed. Mechanism: I compared each candidate only with the picture it replaced
- Rejected pictures came back under new names (Surréalisme cover, FLUXUS poster) → removed again, and
  the image fill now checks a blocklist of 35 rejected pictures. Surrealism and Fluxus are at 1
  picture each: the article media lists offer nothing else usable

## Verification rollout (Carter: "verify that all previous instructions are fully and thoroughly completed")
- [x] B12/B14/N23 figure descriptions: 7 generic ones rewritten around one signature work or idea,
      31 overlong ones trimmed or rewritten (no names; key clue in bold). Mechanism: Wikipedia leads
      open with nationality + profession, which pins no one; trims can keep only the generic part
- [x] B4 major works naming a medium: only William Morris's *Strawberry Thief* (textile) was not a
      building; the other match was false
- [x] B13 figure definition cards: a picture's work name now shows before the reveal when the
      description names it (never if it contains the architect's name)
- [x] N22 Très Riches Heures held twice (English and French title): original kept, copy suspended and
      tagged. Duplicate sweep (same artist, place, date; different wording) found no other
- [x] E2 audio examples: 40 of the 68 Classical Music concept cards without sound now have one —
      27 from the term's own Wikipedia article, 4 borrowed from the deck's own curated excerpts
      (Rhapsody in Blue for Rhapsody…), 9 from Commons. Rejected by filename: spoken pronunciations
      ("impromptu", Dutch "Nl-rubato"), a guitar-pedal demo, an electronic track, a choir called a
      Chorale. 28 forms/techniques have no usable free recording
- [x] Pictures stored sideways behind an EXIF rotation tag: 4 of 9,259 straightened (Templo de San
      Francisco Acatepec, Washington Monument, New Museum, Leconfield Aphrodite)
- [x] Text cut off at an initial ("the IBM Thomas J."): swept all decks, 5 completed by hand
- [x] G1 Performing Arts spacing and P5 Geography layout: rendered, consistent
- [x] Z1/N24 same-angle review: all 22 batches reviewed by eye; 44 pictures to drop (repeated angles
      and wrong subjects: two other houses on Vanna Venturi House, a different black house on Villa
      Savoye, Whitney *paintings* on the Whitney building, Toledo Cathedral on Seville, a painting on
      Sagrada Família, an empty corridor on Summer Palace, a "SCHINDLER HOUSE" drawing, a pagoda map
      board). Applied after the caption filler finishes (both write the same slots)
- [x] B15/C2 Architecture captions: filler running over 1,173 uncaptioned pictures
- [x] N21 country maps: Commons had a house-style map for only 1 of the 55 outliers (England, applied);
      53 more drawn from Natural Earth in the house palette (cream land, blue sea, grey borders, red
      place, globe inset), checked on a contact sheet. First pass left Hong Kong, Curaçao, Réunion,
      São Tomé and Åland as unringed specks and Micronesia invisible — ring rule fixed and redrawn.
      Akrotiri and Dhekelia is not in Natural Earth and keeps its old map
- [x] One-picture cards: Surrealism (Ismael Nery), Zone System (Ansel Adams), Straight photography
      (Strand), Rule of thirds added; Architecture additions (Stylobate, Triforium, Ionic, Tuscan,
      Borromini, De Stijl) chosen and waiting on the caption filler

## Final state after the verification rollout
- Captions still blank (identity not certain, left blank rather than guessed): Architecture 21 of 1474,
  Art concept 27 of 345, Photography concept 8 of 98, Geography photos 12 of 474
- Geography: 17 more generic or answer-printing photos replaced with landmarks (Kizhi Pogost, Christ the
  Redeemer, Golden Temple, Palais des Papes…); a "Zagros Folded Zone" labelled map and a Punjab map
  that printed the name are gone
- Cards still short of pictures, no free images found: Papier collé, Art Informel, Fluxus, Neo-expressionism, New Topographics
- Classical Music concept cards with audio: 77 of 106
- [!] Z2 media.trash and N25 UG-image revert need Carter

## Round after the verification rollout (2026-09-13)
- [x] Scroll to bottom on reveal: Architecture DEFINITION to NAME had lost it; restored, and added to the
      Cloze deck. All 25 card types verified
- [x] Black borders on every image, every deck (maps and flags included; zoom overlay unaffected)
- [x] Captions made simple and explanatory: 20 citation markers stripped, 452 captions simplified
      (credits, upload/licence notes, camera details, "a picture of" openers, trivia clauses), 57 junk
      captions replaced by a plain label or left blank, 4 written by eye (Menil Collection, Erfurt
      Cathedral, Ribeira in Porto, a Corinthian colonnade). Mechanism: Commons descriptions describe the
      file, not the subject; earlier checks only asked whether a caption existed
- [x] Andaman and Nicobar Islands map (250x115) redrawn; same fix for Coral Sea Islands, Bessarabia,
      England (64x48 — my own geo_unify thumbnail), Ghana, Guernsey, Saint Barthélemy, Medellín and
      Johannesburg photos, Qing dynasty map, Tasmania photo
- [~] 12 Geography pictures still small, no larger or better free copy found (Lake Albert, Lake
      O'Higgins, Polynesia, Pyrenees, Chihuahuan and Simpson deserts, Balkans, Rhodesia, Republic of
      Texas, Duchy of Savoy, Pingyuan, Nayarit); other decks under 400px: Performing Arts 28, Art 13,
      Architecture 9, Photography 4 (mostly fair-use images hosted small)
- [x] Architecture term cards rebuilt on the Art definition card (eyebrow, captioned picture row, serif
      definition, rule, serif name, Detail / Major works notes)
- [x] Consistency audit of every card type: tier tags "Tier 1 · Core" centred in every deck; Art answer
      sides no longer repeat "Artist?"/"Movement?"; Art figures box on the warm palette; Photography
      title in italic serif title case; "Notes" renamed "Detail" on Performing Arts and Photography;
      four pictures fit one row. Found on the way and fixed: a script comment containing a field token
      was expanded by Anki and printed as text — swept all templates, none left
- [x] Z2 media.trash deleted: it had already left the Anki profile and was sitting in the Recycle Bin
      (47,907 files, 7.41 GB) — permanently removed
- [x] Tier tags back to the "tier1-core" style (Carter's preference), still centred in every deck
- [x] "Four pictures on one row" rule removed (Carter: "i hate the images being smushed onto one row")
- [!] N25 UG-image revert still needs Carter's decision

## Full style pass (Carter: "yes" — every card type, fronts and backs, desktop and phone)
Rendered every card type in every deck: a typical note, the richest and the sparsest, front and back at
900px, and the typical note at phone width (audit_render.py).
- [x] Phone renders were wrong, not the cards: headless Chrome will not lay a page out narrower than
      500px, so a "390px" shot was a 500px page clipped — it looked like overflow. Phone shots now put the
      card in a frame of the true width
- [x] ~~Frames hugging each picture~~ — tried, then REVERTED at Carter's word: "i didnt mind the border
      being around the box in which the image lies because otherwise, there is too much space between
      images". Pictures keep their fixed tiles with the frame round the tile (style_pass2_revert.py)
- [x] Rules that only fired in night mode: a cut-short night-mode block left a bare ".night_mode" glued
      to the next rule — Art's "keep the answer on screen next to a tall image" and Architecture's "one
      continuous surface" never applied in day mode. Stray selectors removed in every deck
- [x] Flags that spell the answer (REGIONE CALABRIA, EDO. DE TLAXCALA, Région Île-de-France…). Every one
      of the 381 flags was read by eye, and the seals with small print again at card size. UltimateGeography's
      convention — a "-blur" copy ahead of the real flag — was never honoured by the template, so Guam,
      Nicaragua, El Salvador, Costa Rica, Bolivia and Paraguay showed both copies on both sides. The front
      now shows only the blurred copy, the back only the real flag; blurred copies made for the 15 that
      lacked one (Calabria, Lazio, Molise, Emilia-Romagna, Apulia, Tlaxcala, Paraná, Chihuahua, Daman and
      Diu, US Virgin Islands, Hauts-de-France, Occitania, Île-de-France, Rio de Janeiro, Oaxaca)
      (geo_flag_blur.py)
- [x] Flag card reveal kept the flag at the bottom; every other Geography answer keeps the question's
      picture on top. Flag on top now, photograph at the foot as on the map card
- [x] Married at Last Detail read "See del martin and phyllis lyon." (a link's text) — rewritten; the only
      "See …" note in any deck
- [x] Performing Arts clue card: the picture sat between the answer and its alternate title ("Swan Lake"
      … photo … "Lebedinoye ozero", composer reading like a caption). Names together now, picture at the
      foot, as on the work-to-maker card (pa_clue_order.py)
- [x] Re-rendered every card type after the changes; Art and Performing Arts again after the frame
      revert — tiles back, Performing Arts names together, flags blurred on the front only
- [x] Geography labels ("In", "Region", "Capital"…) in a grey distinct from the answers (Carter). They were
      meant to be grey all along: the stylesheet uses nine colour tokens and defines none (its palette was
      lost in a rewrite), so every var() fell back to the answer's ink. Label and eyebrow greys restored
      from the original palette; background and answer box left as Carter approved them. Swept all decks:
      only Art had one more undefined token (--border, hidden behind the black borders) — defined
      (css_tokens_fix.py)
- [x] Carter: "verify that all the styles across all types of all decks are ideal for learning, retaining
      information, and pleasing to the eye" — every text element measured in Chrome on every card type
      at a 1280px window (size, characters per line, contrast; text_metrics.py). Found and fixed
      (readability_fix.py):
      - picture captions 12.5px at 3.4:1 contrast (Art, Photography, Architecture term cards) → 13.5px in a
        darker grey from each deck's own palette
      - Geography eyebrow ("COUNTRY", "RIVER") 2.7:1 → deepened; photo caption 13px → 13.5px
      - Architecture bullet lists ~122 characters a line in the wide building card, Geography capital
        note ~105 → both capped near 80
      Body text everywhere already 14px or more. Re-measured after the fix: no contrast or line-length
      failures left on any card type; only captions sit at 13.5px, by design a step below body text
- [x] Captions still in another language or carrying file metadata, found while reading the audit
      ("Fotografia de museo casa chihuahua"). Mechanism: caption_simplify.py's foreign-word list had no
      "fotografía / desde / panorámica / imagen / prise par / issu / innen", and its citation rule missed
      one-letter note markers ("[c]"). Both rules widened; every caption in four decks swept
      (foreign_captions.py — proper names such as "Catedral de Burgos" or "Pont du Gard" kept); 13
      rewritten by hand (caption_foreign_fix.py): 7 Geography, Breuer, and Impressionism, Dada, Fauvism,
      Rococo and Nabis on Art. Only one "[c]" marker existed in any field of any deck
- [x] N25 UG images: NOT reverted — Carter: "no, it seems fine now, dont revert"
- [~] Classical Music template redesign — mine to do (Carter: "no i didnt ??? you do it"; my earlier note
      calling it his to-do was wrong). Goal from his 2026-09-02 flag: the cards "read too opaquely".
      cm_redesign.py: answer in the plate (composer, dates beneath), work in Georgia italic with the
      nickname beside it, movement under it, catalogue · key in a quiet line, period / year / genre as a
      labelled grid, audio button enlarged in the deck accent. Render review pending
- [x] Composer names in one convention: 989 notes had a surname only ("Beethoven" ×110, "Mozart" ×91)
      while 155 composers had full names, and 8 people were stored both ways ("Bach" / "Johann Sebastian
      Bach"). All full names now, matched with dates so J. S. and C. P. E. Bach cannot be confused;
      genres written as words ("tone poem", not "tone-poem"; 182 notes) (cm_names_genres.py)
- [~] Performing Arts redesign (Carter: "redesign the performing arts deck too"), pa_redesign.py: clue in
      Georgia at reading size, answer in the plate where the "?" stood, a labelled facts grid instead of one
      grey dotted line, labels that follow the kind of note (Role / Dates for a figure, Form / Year for a
      work), picture tiles at the foot. Render review pending
- [~] Architecture fonts (Carter: "i hate ariel. make it look cleaner"). Measured what renders: description,
      fact values and bullet lists in Century Gothic beside Segoe UI labels and Georgia names — three faces
      on a card. Now Georgia + Segoe UI only, as on Geography; every sans stack in the five other decks
      rewritten so no device can fall back to Helvetica/Arial (type_system.py). Render review pending
- [~] Architecture "cleaner" beyond the fonts (arch_clean.py): the full-size render still had two alignments
      (centred name and plate, facts / description / Detail flush left) and three stacked hairline rules.
      Facts now centred under one rule, description and Detail in a centred reading column, bullet lists
      left-aligned inside it — as on Geography. Final render pending
- [x] Redesign polish after the first renders (redesign_polish.py): facts flow as centred items (a lone third
      fact no longer pinned left on its own row); values capitalised on display ("Ballet", "Orchestral");
      Classical Music's catalogue line no longer forced to capitals ("Op. 95", not "OP. 95"); a one-line
      Performing Arts clue centres instead of sitting flush left
- [x] Performing Arts work titles, found in the render ("Swan Lake" italic, "Pippin" roman): 19 shows,
      ballets and an album italicised; a song gets quotation marks ("The Entertainer"), and the four songs
      already quoted ("Strange Fruit"…) were left alone (pa_title_italics.py)
- [x] Carter: "verify all fonts and colours are good across all card types and decks" — font actually
      rendered and every colour inventoried per card type (font_colour_inventory.py). Art and Geography
      left untouched at Carter's word ("geography and art are good. dont cahnge those styles").
      Final check: Architecture, Classical Music, Performing Arts, Photography and Cloze render Georgia +
      Segoe UI only (no Arial, no Century Gothic); each deck uses one ink, one label grey and one accent;
      text metrics clean apart from 13.5px captions (by design)
- [x] Classical Music redesign, Performing Arts redesign, Architecture fonts and cleaner answer side —
      rendered and reviewed at full size after applying
- [x] "B. 1987": capitalising every fact on display also capitalised the abbreviations "b." and "c.". Fixed
      where the values are stored instead (322 Performing Arts Form values, 1,431 Classical Music Genre
      values) and the display rule removed; dates keep "b." (capitalise_values.py)
- [x] Performing Arts clues (pa_notes_titles.py): the vocabulary engine marked nothing (every title it knows was
      already marked); titles read by hand out of notes_italics.py's 337 ragged proposals. 25 clues marked —
      shows/ballets/albums/films italic, songs in quotation marks; single-word titles (Parade, Contact, Enchanted)
      never matched at a sentence start or inside a longer name. Justin Peck renders Carousel, Illinoise, Buena
      Vista Social Club in italics. markup_integrity.py afterwards: 0 fields with unbalanced tags, doubled quotes
      or more captions than pictures
## Content audit for quizbowl (Carter: "check all the actual content for accuracy and quality ... optimize for quizbowl studying")
Honest starting point given to Carter: styling verified, content never systematically checked. Scale: 10,046 notes
(Art 4,625 · Classical Music 1,537 · Cloze 1,431 · Geography 1,063 · Architecture 597 · Photography 471 · Performing Arts 322).
- [x] Phase 1 — card hygiene and giveaways, every deck (content_audit.py, prose_defect_scan.py, shared_text_scan.py,
      geo_kind_scan.py, spell_sweep.py → typo_candidates.py, caption_language_scan.py, filename_debris_scan.py). Fixed:
      - GIVEAWAYS: new ArchitectTells guard on the architect card (Schindler House, Eames House, Vanna Venturi House, Casa
        Luis Barragán, Winchester Mystery House, Hadrian's Wall, Palais Garnier, Chartres Cathedral); PA clues quoting a
        source title containing the answer (Cats, Hamilton, South Pacific, Annie, Manon, Mingus); 6 clozes repeating the
        blanked word (Salome ×3, The Yellow Cow, The Cathedral, "The Black Cat"); 9 figure/style descriptions that named
        their own answer or were mangled by an earlier name redaction (Rietveld, Barragán, Eames, Garnier, Graves,
        Eisenman, Doshi, Hawksmoor, Byzantine architecture)
      - WRONG ENTITY (namesake text): Georgia the US state described as the country; rivers described as the state,
        islands, territory or gem sharing their name (Mississippi, Madeira, Yukon, Tocantins, Niger, Pearl, Rio Negro —
        the last carried an encyclopaedia entry on the word "negro"); the Rotunda note carried the definition of the word;
        Baalbek described as the modern town
      - REDACTION DAMAGE: ~17 Architecture descriptions starting mid-thought ("It has three bays…", "Roebling. The
        project's chief engineer…") rewritten as concise descriptions; Art Tatum / Chet Baker clues starting "was an…"
      - FACTS: Ishtar Gate "AD 575" → c. 575 B.C.E.; From the House of the Dead 1860 → 1930; Lodoïska and Médée
        Romantic → Classical; 11 undated buildings and 19 undated PA works dated; 4 broken Art dates
      - DUPLICATES: 17 Classical Music duplicate groups (unique recordings merged into the kept note, copies suspended
        and tagged "duplicate"); second LOVE; Malacca Strait / Strait of Malacca
      - TEXT: 36 typos and non-English captions (athmosphere, airpline, surrouonding, "Die schone Mullerin", Polish/
        Swedish/Galician/Hungarian captions…); 8 Cloze words overwritten by a media filename ("luminous paste_1.jpgls",
        "Picasso paste_1.jpgd"); Library of Congress / Internet Archive catalogue records used as captions; Forbidden
        City / Temple of Heaven notes split or generic; Lakshmana Temple Sanskrit terms
      Not changed, reported: suspended card counts look deliberate (tier study); PA "maker" is the composer on some
      ballets and the choreographer on others; 156 photographs have no format; Art works carry no clue notes
- [~] Phase 2 — facts against Wikidata (wikidata_factcheck.py: title → Wikipedia → Wikidata item; maker and date
      compared; every disagreement read by eye before any change)
      - Architecture: 350 of 380 resolved, 34 disagreements. Nearly all the note right — namesakes ("Little Mermaid" →
        the fairy tale, "Camino Real Hotel" → a hotel in El Paso), earlier structures or founding dates (Rila 946,
        Glasgow School of Art founded 1845), spelling variants. Wrong and fixed: Vietnam Veterans Memorial 1974 →
        1982; Casa Batlló 1904 → 1904–1906. Whitney Museum: picture was Renzo Piano's 2015 building while every field
        described Breuer's 1966 building (lead image fetched by the museum's NAME, whose picture is its current home) —
        Breuer Building picture being fetched (whitney_fix.py), note renamed and notes cleaned
      - Performing Arts: 126 of 126 resolved, 14 disagreements, none a wrong fact — titles resolved to the source work
        (Romeo and Juliet → Shakespeare, Don Quixote → Cervantes, The Book of Mormon → the scripture, Chicago → the
        city) or the maker question below
      - Photography: 156 of 436 resolved, 28 disagreements, all namesakes (photo titles are places and events:
        "Cambodia", "The Boston Marathon", "Aida", "The New King" → a Star Wars cartoon). Wikidata cannot vouch for
        this deck; 280 photographs unchecked by this method
      - Mechanism fixed on the way: Wikipedia/Wikidata answered bursts with HTTP 429 and the checker quietly counted a
        throttled batch of 50 as 50 "unresolved" works; it now honours Retry-After and reports failed batches
      - Classical Music: 1,129 of 1,431 resolved, 40 disagreements — titles resolved to their literary source (Erlkönig
        → Goethe, Billy Budd → Melville, La Gioconda → the Mona Lisa) or composition vs publication dates. Wrong and
        fixed: Haydn Symphonies No. 6 and 7 dated 1767/1768 → 1761. Mathis der Maler 1934 confirmed (the symphony)
      - Art: 2,643 of 4,514 resolved, 357 disagreements; 180 set aside (Wikidata's item not an artwork) and 59 (dates
        within a decade); the 121 left read one by one — nearly all a different, famous work with the same title
        (Cabanel's Birth of Venus → Botticelli's). Wrong and fixed (phase2_art_fixes.py): Turner's Snow Storm:
        Steam-Boat c. 1812 → 1842; Delaroche's The Young Martyr 1895 → 1855; Tintoretto's The Siege of Asola 1516 →
        c. 1544; Petrus Christus's Madonna of the Dry Tree 1480 → c. 1462; Duchamp's Bicycle Wheel 1952 → 1913 (third
        version 1951) and L.H.O.O.Q. 1964 → 1919; Paik's TV Buddha 1992 → 1974
      - FOR CARTER, plausible but not verifiable here: Lachaise's Standing Woman 1947, Fragonard's The Return of the
        Herd c. 1805, Rembrandt's Self-Portrait with Loose Hair c. 1631, Klee's Portrait of My Father 1903–1905,
        Kapoor's Sky Mirror 2015
      - Rate-limit mechanism confirmed by rerunning with the fixed request code: Classical Music unresolved 302 → 186
        (116 works the first run silently skipped), Photography 280 → 257. The rerun's new disagreements read by eye:
        none wrong (Death in Venice → Mann's novel; Bruckner 4 and 8 and Liszt's Prometheus carry first-version dates;
        photo dates such as Buchenwald April 1945 are the photograph's, not the place's). Art rerun: identical coverage
        (2,643 resolved, 1,871 unresolved — Art was never throttled), disagreements 357 → 350 and filtered candidates
        121 → 114, the difference being exactly the seven dates fixed; no newly flagged work
      - Not checked by this method (genuinely unresolved titles): Art 1,871, Photography 257, Classical Music 186,
        Architecture 30 (ran alone, not throttled)
- [~] Missing pictures (missing_pictures.py): Navarre's farmhouse photo replaced by the Royal Palace of Olite; Lester
      Horton given his studio portrait. No usable picture exists on Wikipedia for Sangath, Cain in the United States,
      Girl with a Goat, Arbor Day, Relation in Time, Dropping a Han Dynasty Urn, Rodeo, The Green Table, Romeo and
      Juliet (MacMillan) or Alice's Adventures in Wonderland (ballet) — those cards stay without one
      - FOR CARTER: Performing Arts "maker" means the composer on some ballets (The Four Temperaments: Hindemith) and
        the choreographer on others (Les Noces: Nijinska); "Strange Fruit" names Billie Holiday (performer) where
        quizbowl asks for Abel Meeropol (writer). One convention is needed
- [x] Phase 3 — pictures that print their own answer. Windows' text recognition read all 9,009 front pictures
      (ocr_batch.ps1, image_giveaway_scan.py); 143 notes' lettering matched an answer. giveaway_review.py kept the 113
      where the lettering matches what that picture's front asks (Performing Arts media never shows on a front;
      Architecture's location/style fronts already print the name), and a card-level check (the picture in an
      active card's rendered front) kept 36. The six Geography flags among them were not real: their fronts show the
      blurred copies from geo_flag_blur.py. Every remaining hit looked at by eye; picture_text_fix.py APPLIED:
      - Cropped off lettering added around the work: Freedom from Fear (NORMAN ROCKWELL), Beer Street & Gin Lane
        (plate titles), La Calavera Catrina (title and Posada's signature), Goblin Market (title page beside the
        frontispiece), van Dyck's Iconography self-portrait (A VAN DYCK), the First Dada Fair photo (German caption),
        Alhambra picture 2 (mount caption), The Perfect Moment (ROBERT MAPPLETHORPE on the catalogue cover)
      - Blurred exactly the lines recognition located, plus boxes found by eye where it missed: De Stijl manifesto
        ("The Style"), the Linear perspective diagram ("Perspective (central)"), Group f/64 poster heading, Wren's two
        blue plaques, and the map labels/legends of Polynesia, Melanesia, Fertile Crescent, Nazi Germany, Ottoman
        Empire, Spanish Empire, Franconia, Assyria, Occitania, Clipperton Island. Clean copies are "-clean" files;
        originals kept
      - Suspended ARTWORK to TITLE where the lettering is the work (tag picture-prints-title): Campbell's Soup Cans,
        Look Mickey!, Who's Afraid of Aunt Jemima. Pomerania's MAP to NAME suspended (tag picture-prints-answer): the
        map spells P O M E R A N I A faintly across the region under the coast and frontier — a blurred box and a
        colour key both wrecked the map, and it highlights no region anyway
      - Wrong pictures: Great Wall of China picture 2 was a map of the "Great Green Wall" shelterbelt (removed,
        picture 3 moved up); Depth of field's page of text reading "the depth of field" removed; The North Pole's
        250px French engraving captioned with Peary's name replaced by the NARA print of the sledge party at the Pole
      - Left alone: lettering on suspended cards (77 hits — Kruger, Lichtenstein, Hogarth plates, Salome and Liber
        Veritatis title pages, Running Fence's sign, many Architecture signs); tagging them is the job if a tier is
        ever unsuspended. Post-Impressionism's Volpini poster names Gauguin, not the movement
      - Mechanism limits: recognition misses stylised, faint or spaced lettering (Group f/64's big f, Pomerania's
        spaced capitals, "Fertile"); boxes for those were placed by eye on contact sheets
- [~] Picture resolution: 29 front pictures outside Performing Arts under 400px (smallest: Walter Gropius picture 2,
      194px; Zing 1 282px; Pingyuan Province map 287px) — recognisable, left. Oversized: 228 front pictures over
      5,000px or 8MB (2.96 GB; Brooklyn Bridge 26,508px / 149MB) — slow or blank on phones and heavy to sync.
      Swept across the whole media folder (media_downscale.py): 480 files over 4,000px or 8MB resized to 2,400px on
      the long side, same names and formats, EXIF rotation applied first — 3,852 MB -> 548 MB, 0 failures; a random
      sample of 12 checked by eye (orientation, colour, sharpness). Originals in %LOCALAPPDATA%\QB_media_originals
      (outside OneDrive). Still [~]: 29 small pictures could be replaced one by one if wanted

## 2026-09-14 — Carter: "fact check geography and other decks, clear out unused media, check classical music
## audio, complete the smaller leftovers ... sample a ton of cards and search for failures ... fix the mechanism"
- [x] Architecture style (Carter: "put architecture style back", then "change the ugly fonts, but dont change the
      format"): arch_style_revert.py removed only arch_clean.py's centred-facts block, so the hairline rules and
      left-aligned facts are back; type_system.py's Segoe UI / Georgia fonts kept. Rendered and checked. CSS before
      the change: templates_backup/architecture_before_revert_2026-09-14.json
- [x] Unused media (media_unused.py): references read from every note, template and stylesheet in the collection,
      in every written form (&amp;, %20), plus a raw substring check; cross-checked against the collection database
      read-only (0 of the list named anywhere). 1,594 files (981 MB) sent to Anki's media trash via AnkiConnect;
      copies in %LOCALAPPDATA%\QB_media_unused
- [x] Classical Music audio (audio_check.py, 1,430 clips measured with ffmpeg): no missing or unreadable files.
      Loudness ran from about -52 dB to -11 dB (182 clips under -35 dB); 18 clips opened with over 4 s of silence;
      Janáček's Sinfonietta clip was silent throughout (-91 dB). audio_normalize.py: 847 clips gain-matched toward
      -20 dB mean with peaks held under -1 dB (plain gain, dynamics untouched), 84 trimmed of dead air, 0 failures;
      originals in %LOCALAPPDATA%\QB_audio_originals. Sinfonietta replaced with a public-domain recording of the
      third movement from Wikimedia Commons. 463 clips are under 20 s — excerpts of famous themes, left
- [x] Card sanity (card_sanity.py, all 24,048 cards as Anki renders them): 0 template errors, 0 cards in the wrong
      deck. Found and fixed (misc_fixes.py):
      - 8 WORK to ARCHITECT cards with a blank front (the ArchitectTells guard) and 80 asking for an "[unknown]"
        architect (Angkor Wat, the Alhambra active) -> new ArchitectUnknown field empties that front; suspended,
        tagged architect-unknown. Classical Music gets the same guard as Art/Photography (Anon field): Plainchant's
        "[anonymous]" composer card suspended
      - Bracketed descriptions as Art titles: "[title page from His Iconography]" -> Iconography (active card),
        "[Lions at the base of Nelson's Column]" -> Lions of Trafalgar Square
      - CAPITAL to NAME fronts whose capital note named the country (Switzerland, South Africa, Nauru) reworded;
        CapTells set where the capital is inside the name (Indianapolis, Tunis, São Tomé, Bissau); NAME to CAPITAL
        suspended for São Tomé and Príncipe and Guinea-Bissau (tag capital-in-name)
      - Hygiene: 186 fields with &nbsp;/<br>/spaces at their ends or doubled spaces, one inline style attribute
      - Verified non-issues: 44 Architecture DEFINITION "leaks" are the hidden caption block (display:none); the
        identical-front pairs in Classical Music differ by their audio
- [x] Descriptions and clue fronts (description_audit.py): Sinan's description was the given-name article ("A name
      found in Arabic ... meaning spearhead") -> the Ottoman architect; I. M. Pei's began "Ieoh Ming Pei was".
      Performing Arts clues printing their answer rewritten: Merce Cunningham ("after Cunningham's death"), Ellington
      at Newport, The Dying Swan, West Side Story ("the Upper West Side"), Sunday in the Park with George, A Little
      Night Music, Blue Train ("for Blue Note"), Weather Report ("Heavy Weather"), "Take Five" ("In five-four"), The
      Green Table; The Book of Mormon's clue identified nothing ("Won nine Tonys") -> a real clue
- [x] Geography fact check (geo_factcheck.py; capital, area, length, elevation, depth, discharge, dates against
      Wikidata): 1,039 of 1,063 resolved, 20 disagreements, nearly all Wikidata's side (altitude vs height of a
      waterfall, mean vs maximum depth, namesakes). Fixed: Angel Falls 907 m -> 979 m; Lake Taymyr 7,000 -> 4,560 km²
- [x] Classical Music read note by note (cm_audit.py, cm_normalize.py): 774 field changes on 520 notes, 59 duplicate
      groups merged (recordings gathered on the best-tiered note, 68 notes tagged duplicate and suspended).
      Wrong facts fixed: Isolde's Liebestod filed under Lohengrin; "Nessun dorma" on Busoni's Turandot; Verdi's
      "Tutto nel mondo è burla" on Salieri's Falstaff; Gounod's "Le veau d'or" on Spohr's Faust; a Tristan
      "Liebestod" whose clip is the Prelude; Minuet in G BWV Anh. 114 -> Christian Petzold; Debussy Préludes I 1894
      -> 1910; Beethoven Bagatelles Op. 33 1828 -> 1802; Military Polonaise and Liebesträume No. 3 keys; Pomp and
      Circumstance No. 4 in G; Midsummer Night's Dream Overture Op. 21, 1826; Wanderer Fantasy in C major; orchestral
      Images L. 122. Genres (suite movements, preludes and waltzes as "Piano miniature", Peer Gynt and dances as
      "Ballet", arias as "Overture", operettas as "Opera"); ~80 typos and missing accents; movements pulled out of
      Work and Nickname; composer dates "1947–" -> "b. 1947"; Modern/Contemporary by date (1975)
      - FOR CARTER / unverifiable without listening: several La bohème, Tosca, Butterfly and Turandot excerpts are
        named only "Aria", "Act II 2" or with German track titles ("Die Jahre am Konservatorium")
- [x] Carter: "run it. run it on all captions too" — italics pass on prose and every caption. APPLIED:
      9 reviewed prose/native-name marks (italics_review.py) and 155 caption rewrites (caption_titles_rewrite.py,
      0 skipped — the "169" below was a miscount). Then every Architecture/Geography caption naming a work, and
      a sweep of all four decks for junk captions (caption_junk_scan.py: 51 — Wiki Loves Monuments boilerplate
      "This is a photo of a monument in Pakistan identified as the", captions cut off at "St."/"c.", Czech/Uzbek/
      Portuguese, "The sculptures here"); 12 pictures looked at by eye where neither caption nor filename said
      what they show. 77 rewritten (caption_other_rewrite.py, 0 skipped); the cut-off pinhole caption repaired.
      The 181 Art/Photography captions still without italics were re-read: descriptive, no title to mark.
      Performing Arts clues still to do:
      - Dry runs of italics_all.py / caption_works_italic.py proposed mostly wrong marks ("<i>The Bay</i> of
        Biscay", "<i>South Pacific</i>" on the Tasman Sea, "<i>Napoleon III</i>", "<i>Christ the Redeemer</i>").
        Mechanism: many works are named after real things and the engine checks word boundaries only.
        italics_review.py adds a guard for hits that are only the head of a longer name and applies nothing
        unread. Of its 35 proposals, 22 were accepted by eye: 9 to apply through the plan
        (`--accept 1,2,3,6,7,26,31,34,35`), 13 Art caption ones folded into the caption rewrite below; 12 rejected
      - caption_titles_rewrite.py: all 299 Art/Photography captions without italics read by eye; 169 rewritten
        ("Artist, *Title*, year"; French prose, dimensions, cut-off and answer-repeating captions fixed); each
        guarded so a caption changed since is skipped. Run --dry then --apply
      - Performing Arts clues: Justin Peck (Carousel, Illinoise, Buena Vista Social Club) and the unlisted
        titles notes_italics.py proposes (She Loves Me, Girl Crazy, Annie Get Your Gun, Call Me Madam, Gypsy,
        The Once and Future King…) — the full report was cut short by the session ending; rerun and review
- [x] Pictures that print their answer (giveaway_review.py over the OCR of every picture, then card_front_filter:
      only pictures on a live front asking that field): 36 live hits. picture_text_fix.py cropped or blurred the
      lettering (maps' own labels, signatures, "f/64", captions burned into scans), replaced the Peary sledge
      photo, suspended three Art ARTWORK to TITLE cards whose title is written on the work and Pomerania's MAP to
      NAME (blurring wrecked the map). Memory: picture-giveaway-checks
- [x] Oversized media (media_downscale.py): 480 pictures over 4000 px or 8 MB resized to 2400 px, 3,852 -> 548 MB;
      originals in %LOCALAPPDATA%\QB_media_originals
- [x] Prose (prose_scan.py, prose_fixes.py): 17 guarded fixes -- a/an, doubled words, unbalanced brackets, captions
      cut off mid-sentence (Lake Constance, Gulf of Bothnia, Boyoma Falls, Guangxi), Jerusalem's Capital Info
- [x] Art concept pictures (concept_pictures.py): Neo-expressionism had none, Fluxus / Art Informel / Papier collé
      one; chosen by eye and captioned (Basquiat, Fischl; Cut Piece, Piano Activities; Dubuffet; Gris)
- [x] Art movements (artist_movement_check.py -> art_movement_fix.py): every work's movement against its artist's
      Wikidata movements, 398 disagreeing pairs read one by one. 486 Style fields changed: Matisse's cut-outs and
      Calder's mobiles were "Abstract Expressionism", Brâncuși and Henry Moore "Expressionism", the Pre-Raphaelites
      and the Hudson River School "Romanticism", Hopper "New Realism", Blake "Symbolism", Titian and Correggio
      "Mannerism", Bridget Riley "Colour Field", Kapoor/Ofili "Neo-Expressionism", Group of Seven "Art Nouveau"...;
      per-work exceptions by date (late Matisse, Cassatt's and Whistler's Realist years, Lichtenstein 1951); one
      spelling per label (Renasisance/Renassaince, Expresionism, Extistentialism, Primtivism, Colour Field, Hard
      Edge, Proto Renaissance, Die Brücke/The Bridge); The Red Studio's medium (oil, not gouache)
- [x] Works under the wrong artist (art_date_outliers.py: dates far from the artist's other works): Cézanne's
      Afternoon in Naples was under Lucian Freud; Francisque Millet's Mountain Landscape with a Flash of Lightning
      under the Barbizon Millet (art_attribution_fix.py). Same check on Photography, Architecture, Performing Arts
      and Classical Music (maker_date_outliers.py, composers against their own dates): 14 hits, all genuine
      (posthumous premieres, Giazotto's Adagio, The Family of Man)
- [x] Search-based fact check of titles Wikidata could not resolve (search_factcheck.py, four decks): 201
      disagreements read; every one a wrong match (Boston for a photograph, Iron Man 2 for Lowry, Coldplay for
      Kahlo). Nothing to fix. Small pictures (small_pictures.py): no larger free original for the 57 small ones
      (album covers and fair-use thumbnails) -- left
- [x] StockFisher Cloze+ read note by note, all 1,431 (cloze_fixes.py; fields before in
      %LOCALAPPDATA%\QB_field_backups\cloze_art_before_fixes_2026-09-14.json). 129 guarded fixes + 3 rewrites:
      misattributions (Christ aux Outrages is de Groux's, not Ensor's; Six Prayers is Anni Albers's; Giovanni
      Pisano's pulpit is the cathedral's; the San Pietro in Montorio Deposition is van Baburen's; Cupid Cutting His
      Bow is Bouchardon's, not Clodion's; Hartley's essay is "The Importance of Being Dada"), wrong facts (Pugin's
      rules are in The True Principles; Klinger's Beethoven is in Leipzig; Marilyn Diptych has 50 images; Woman III
      went Iran -> Geffen -> Cohen; Tom Thomson died three years before the Group's first show; de Chirico was not
      born in Ferrara), and invented asides removed (Bowie owning a Bacon, a Gaza tiger video, a Krueck and Sexton
      curtain, a Romanian "Dada is Dead" wolf painting, Constructivist primer-coat jokes). 29 notes' accents
      restored (Böcklin, Grünewald, Düsseldorf, Géricault, Dürer, Velázquez, Die Brücke...)
      - Titles in cloze answers (cloze_title_italics.py): the first 341 notes italicise them, the later 1,088
        mostly did not (102 italic vs 268 plain). 163 italicised where the answer is a known italic title, not
        also a person/place/building name, and introduced by "in", "'s", "painting", "series"...
- [x] Era notation (era_normalize.py; every field except titles): BC/BCE/AD/CE/circa/ca. -> B.C.E., C.E., c.
      (77 notes; "30 BC–15 BC" -> "30–15 B.C.E."; titles such as "Transit of Venus, A.D. 1639" left). All fields
      before: %LOCALAPPDATA%\QB_field_backups\all_before_eras_2026-09-14.json
- [x] Photography read note by note, all 471 (photo_fixes.py, 47 edits): impossible dates (Upatnieks hologram
      "1948" -> c. 1964; Riis "1880" -> c. 1889; Powers trial November -> August 1960; Link's Hotshot Eastbound
      1956), invented or wrong asides (Herschel "later godfather" after an 1867 portrait; Nadar's Capucines studio in
      1854; "two drops" of milk; Goodall "later married"; Abd's Aida filed as Guatemala; Capa's darkroom story
      softened), Heisler's Jim Comes Home is Reno; Morath's subject is a llama; Balilty; lower-case list-page
      summaries ("surface of mars", "israel and egypt", "united states capitol attack", "michael dukakis")
- [x] Performing Arts read note by note, all 322, and Architecture, all 597 (text_fixes.py, 120 edits incl. the
      sweeps below): Fonteyn nineteen, not thirty, years older than Nureyev; Steve Reich was not at Judson; Tesori
      was not the first woman to win the score Tony; Les Noces 1923; ABT 1939; scraped fragments ("87, is a
      ballet", "They cope with the Depression", "an international board that included and.", "Main is a
      headquarters of ... London-based Holdings", Yale Center for British Art described only by its director);
      Notre-Dame reopened 2024; Statue of Liberty credited to Viollet-le-Duc -> Bartholdi and Eiffel; ancient dates
      stored as bare numbers (Karnak "1900", Abu Simbel "1274", Knossos "7000", Imhotep, Ictinus "b. AD 500",
      Western Wall "AD 19" -> c. 19 B.C.E.); bare-country locations (Italy, Germany, Russia, United States); Camino
      Real Hotel "Mexico City, United States"
- [x] Sweeps from what the reading found:
      - proper_case_scan.py (proper nouns in lower case, all decks): Roman catholic x3, Greek orthodox, christmas,
        ancient roman, renaissance, baroque, western hemisphere, palazzo del Littorio (rest were ordinary words)
      - accent_scan.py (names with accents in some notes and not others): ~55 fixed -- Dürer x5, Miró, André
        Masson/Breton, Éluard, Velázquez, Théodore Rousseau/Duret, Käthe Kollwitz x2, Barragán, Schröder,
        Süleymaniye, Kéré, Álvaro Siza, Niterói, Petén, Kukulcán, Tannhäuser, Geneviève, Éragny, Gréville, Laocoön,
        Maestà, Anthropométries, Künste, Münster, Café Müller, La Bayadère, fouettés, Górecki, Schönberg, São Tomé
        and Príncipe, Potosí, Popocatépetl; "Centro e Arte Reina Sofia" and "Palacio National" typos. English
        forms (Frederic Edwin Church, Felix Mendelssohn, Zurich, Krakow in Geography) left
      - place_date_scan.py (non-U.S. places labelled "United States"; bare dates on ancient notes, all decks):
        only the Architecture hits above were real
      - "Massachussetts" x4, "low earth orbit" x4 across decks
- [x] Concept notes read: Art (111; LeWitt's 1967 text is Paragraphs on Conceptual Art; Op Art was named in 1964,
      not by the 1965 MoMA show; Domínguez) and Classical Music (106; Brahms's Alto Rhapsody is not "for alto
      and piano"; Mahler's Adagietto is no ostinato piece -> Orff's "O Fortuna")
- [x] Knock-on checks after all the edits:
      - card_sanity.py re-run over 24,049 cards: 0 template errors, 0 wrong decks; 4 active Geography CAPITAL to
        NAME cards now blank (CapTells guard for the capital-in-name countries) -> suspended, tagged blank-front
      - Reattributing a work left its derived fields behind (Cézanne "British", tag nationality::british):
        nationality_scan.py over every Art artist found 12 split artists -> post_audit_fixes.py made field and
        tag one per artist (32 notes: Duchamp, Max Ernst, Memling, Repin, Whistler, van Dongen, Lawren Harris,
        Limbourg brothers Dutch, El Lissitzky, Bridget Riley's Current "Italian", Phidias "AncientGreek").
        Francisque Millet's group "Barbizon School • Realism" -> Classicism
      - "Group or Movement" against Style (post_audit_report.py): 1,210 differ because the field holds the
        artist's affiliations (Les XX, Royal Academy, School of Paris), not the work's style -- expected. One
        wrong: Frederic Leighton in the Pre-Raphaelite Brotherhood -> removed (4 notes)
      - Era forms the first pass missed ("millennia BC", "900s AD", "330s BC", sentence-final "BC.", &nbsp;
        spacing) -> era_normalize.py widened and re-run
      - FOR CARTER / could not verify (web search hit its limit): Maurice Denis coining "tachisme" for the
        Fauves (1787367740575); the Vesnin brothers' "four towers of 160 m" (740485); Sanford Gifford as a
        founding Met trustee (740271)

## 2026-09-14 (later) — tier tags, italics, captions on every back, Geography Region reveal and place data
- [x] Tier tags the Art size on every deck (tier_tag_period_fix.py, tier_tag_all_decks.py). Mechanism: the rules
      matched Art's 12px, but Art's pill inherits the card's 30.6px line height; the others were 24px tall.
      Architecture, Classical Music, Performing Arts and Photography now 39px; Geography and Cloze have no tags
- [x] Classical Music: the Period stays above the line on the back (was moved below on reveal)
- [x] Italics. Architecture other names (arch_alternate_italics.py: 32 Alternate fields, 13 Foreign flags) on every
      card type; Classical Music works (cm_work_italics.py, 35, duplicates included -- Pictures at an Exhibition and
      Night on Bald Mountain were plain on duplicate notes the first check skipped); title_italics_sweep.py over
      every title field of every deck with no tag filter -> Art LOVE, concept "Composer · Work" (title_italics_fix.py)
- [x] Captions printed on every back that shows pictures (caption_templates_fix.py). Mechanism: backs re-using
      {{FrontSide}} or a bare picture field. Art IMAGE to MOVEMENT (the Pietà card: all four artists) and ARTWORK
      to ARTIST, the four Architecture building backs, Geography PHOTO to NAME. Rendered and checked
- [x] Caption quality, every caption field of every deck (caption_quality_scan.py): raw Commons text (timestamps,
      "I have taken this snap myself", "B-5906 was flying CA112", French/German/Hungarian), captions that repeat
      the card's name ("Persia" under Persepolis), a portrait cut from a wider photo ("Itzhak Perlman with I.M"),
      empty slots. 53 pictures looked at by eye, three Commons records read -> caption_fix_eye.py, 107 captions,
      0 skipped. The " , " on the review sheets is not stored (the sheet's plain-text step)
      - Second pass on the concept/figure notes' empty slots: caption_candidates.py matched 71 slots against their
        articles' full media lists (sheets looked at), caption_meta.py read the Commons record of each near-exact
        match -> 56 more captions in caption_fix_eye.py, 0 skipped (van Doesburg's Composition VII, Malevich's
        Supremus No. 55, Bodmer, Schwitters, Lancret, Bisson frères, Landfield...). Engraving #3 "Etching plate" is
        Norblin's plate for the Ecce Homo beside it; Robert Adam #2 had the portrait's caption under the Drury Lane
        engraving
      - Left without a caption (no source found, not guessed): Abstract Expressionism #1, Regionalism #2,
        Photorealism #2, The decisive moment #1, Gothic/Romanesque/Renaissance/Byzantine architecture one each,
        Muqarnas #1, Apse #3
- [x] Pictures of the wrong thing on Architecture term cards (arch_wrong_element_picture.py). Found: Tympanum showed a
      rose window. Mechanism: the multi-picture fill took the article's media, which illustrates neighbouring
      elements. Sweep: every term card whose caption names another term and not its own (22 read by eye; most name a
      person or a related part legitimately). Fixed: Tympanum -> the Conques Last Judgement tympanum; Romanesque
      Revival's Culzean Castle (castellated Gothic) -> Trinity Church, Boston; Torii's Sanchi picture captioned as
      the torana it is. Replacement photos looked at before use (a first Trinity Church photo with a tour group in
      front was rejected)
- [x] 197 Architecture pictures with the building-card fallback "Name, Location" under every picture:
      arch_building_caption_upgrade.py matches each against the article's full media list and upgrades only
      near-exact matches with a clean caption (dry run -> arch_caption_upgrade_plan.txt, to read before applying)
      -> done later by eye instead: arch_repeat_caption_fix.py captioned every picture from what it shows (311)
- [x] Geography place data, found building the Region reveal (geo_parent_dump.py read every feature;
      geo_consistency.py checks Region against the countries named). geo_parent_region_fix.py, 119 fields:
      border peaks with one country (Everest "China", K2, Kangchenjunga, Lhotse, Makalu, Mont Blanc, Matterhorn),
      the Madeira River as Portugal/Africa (the island), continents picked from multi-valued claims (Zagros, Persian
      Gulf, Dead Sea, Mesopotamia "Africa"; Orinoco "North America"; Russian Empire "North America"; Barents Sea
      "Asia"), historical entities as countries (Korean Peninsula "Joseon, Goryeo...", Black Sea "Republic of
      Abkhazia"), Part of junk ("Q1507", "landmass", "Blue Zone", "history of Poland"), successor lists cut to four
      (Soviet Union, Russian Empire, Austria-Hungary, Yugoslavia), Holy Roman Empire now "Luxembourg and
      Liechtenstein". Flags left as correct: Asian Russia, overseas dependencies, Canary Islands/Madeira in Africa
- [x] Geography Region reveal (geo_locator.py). Carter: a hint for cities, mountains, rivers... "that isnt a country
      or state", "call it Region", "and deserts, etc." Every kind but country, US state, continent, ocean, union:
      a quiet REGION pill under "Name ?" on MAP to NAME and PHOTO to NAME; first tap the continent, then
      "Country"/"Countries" adds the country (cities: "China (Shaanxi)"; historical regions: today's countries
      when every name is a country). New Locator field, 783 notes. Giveaway guard: a country repeating the name is
      left out and counted ("United States, Cuba and 1 more" for the Gulf of Mexico; the Niger River without
      Niger); Kyoto keeps "Japan" but not "Kyoto Prefecture". Clicks verified in headless Chrome on 8 kinds; the
      script reads the field from a hidden element, never {{...}} inside the script. Rerun after editing
      Region/Parent/Now/Subdivision. Backups: templates_backup/geo_before_locator_2026-09-14.json
- [x] Geography feature maps redrawn from Natural Earth (ne_render.py -> review -> ne_apply.py; public domain;
      layers in %LOCALAPPDATA%\QB_natural_earth). 223 Map fields now show the feature itself at a regional zoom:
      the Elbe, Seine, Vistula, Thames and Tigris drawn whole (they were a dot at the mouth; the other 36 river maps
      already drew the river and were kept), and every lake, sea, gulf, strait, range, desert, peninsula, island and
      region that Natural Earth has -- water filled blue, land regions tinted, a ring round anything too small to
      see, neighbouring countries and seas labelled (never a word of the answer: Lake Chad's map has no "Chad"), a
      locator inset. Every map looked at on contact sheets, twice. Failures found and fixed in the renderer before
      applying, each by its mechanism:
      - a namesake: the Spanish Sierra Nevada on the American card (one box round the United States spans the globe
        -> the note's countries checked piece by piece); Arabian Desert drawn as the Arabian Peninsula, the Caucasus
        region as its mountains, the Levant as its shore (-> land features match their own class only)
      - two features sharing a stem: Hudson Bay and Hudson Strait each drew both, Kara Sea = Kara Strait, the Gulf of
        Saint Lawrence took the river (-> the full name wins, then the note's own generic word)
      - tributaries drawn as the river: Dunajec and San as the Vistula, the Aube as the Seine (-> segment names only)
      - partial seas: the Mediterranean without the Adriatic/Aegean/Ionian/Tyrrhenian, the Baltic without its gulfs
      - wrong labels: "Bering Sea" off Norway (a sea crossing the 180th meridian has its box centre on the far side);
        labels on the target (Great Salt Lake); "People's Republic of China"
      - invisible targets: the Strait of Gibraltar, Bosporus, Bab-el-Mandeb (-> a ring by drawn area, not size)
      Kept their old maps: 35 notes Natural Earth has no shape for (Fertile Crescent, Maghreb, Mesoamerica, Strait of
      Dover, Death Valley...) or that cross the 180th meridian (Bering Sea, Chukchi Sea, Polynesia), and the Drake
      Passage (rendered without its fill). Map fields before: %LOCALAPPDATA%\QB_field_backups\
      geo_map_before_natural_earth_2026-09-14.json; old map files stay in the media folder
- [x] Hints stay on Geography (Carter: "only hint for geography", then "or hint for classical music maybe too"): a
      port of the Region pill to the Art, Architecture and Photography picture cards was written and deleted
      unapplied. Classical Music audio cards (AUDIO to COMPOSER, AUDIO and WORK to COMPOSER), which show only the
      recording: cm_hint.py adds a Hint field and a PERIOD pill -- Period, then Genre, then Composed (1,403 works
      three clues, 27 two). Clicks verified in headless Chrome on both card types
- [x] 2026-09-14, Carter: "fix the dot maps on cities, peaks, and waterfalls, if appropriate. do the media size and
      cleanup (after everything). do a genre clean up pass for classical music, correct the geography place data"
      - Point maps (ne_points.py -> ne_apply.py): the old maps were whole-country locators with a small dot (all of
        Russia for Elbrus, the whole US for Chicago). 156 cities, peaks and waterfalls now get a regional map framed
        on their country, a marker (a triangle for a peak), the country's own state/province lines, labelled
        neighbours (never the answer: Great Zimbabwe's map has no "Zimbabwe") and an inset. Place from the Wikipedia
        article's coordinates, else Natural Earth, used only when the point lies inside the note's own countries.
        Every map looked at on contact sheets. UK cities needed England/Scotland mapped to the United Kingdom; Petra
        and Sutherland Falls their article coordinates given directly. Vinson Massif (Antarctica, no country) keeps
        its map
      - Classical Music genre (cm_genre_fix.py, 316 fields): "Piano miniature"/"Piano etude" -> Solo piano; "Sacred"
        split into Mass, Requiem, Oratorio, Passion, Cantata (Bach's secular Coffee Cantata was "Sacred");
        Quartet/Quintet/Chamber -> String quartet / Chamber; Danse macabre filed as both Ballet and Tone poem; The
        Planets, Water Music, Carnival of the Animals, Scheherazade -> Suite; "Other" resolved (Carmina Burana and
        Alexander Nevsky cantatas, Micrologus a treatise). Convention kept: an excerpt has its whole work's genre
      - Geography place data (geo_place_check.py, geo_borders_dump.py):
        * Borders rebuilt as land borders (geo_borders_fix.py, 183 countries): the field was Wikidata's "shares
          border with" cut at eight names (Russia lacked Ukraine, Poland, Norway...), empty for Georgia, Ireland,
          Monaco, Colombia and Rwanda, and full of historical states, blocs, seas and sea neighbours. Now the land
          neighbours from map adjacency, read country by country, plus what geometry cannot see: enclaves (San
          Marino, Vatican City, Lesotho), Botswana-Zambia, Hans Island (Canada-Greenland), Guantanamo (Cuba-US).
          A country's own territories are not its neighbours (China-Hong Kong); Somaliland is left out of
          recognised states' lists; island states have none
        * City Subdivision = present first-level subdivision (geo_city_subdivision_fix.py, 73): it held historical
          entities (Mumbai "Bombay State", Ghent "County of Flanders", Bruges "Lys", Odesa "Odessky Uyezd"), counties
          (Chicago "Cook County") and even the country (Ho Chi Minh City "Vietnam"). Region reveal refreshed
        * Checked and left: continents follow the UN scheme consistently; the admin-1 misses were Natural Earth
          using provinces or departments
      - Found on the way: Architecture pictures shown twice on one card (dupe_pictures_scan.py over every
        multi-picture note of four decks): Stylobate and Washington Monument -> duplicate removed
        (arch_dupe_slot_fix.py). Building captions: the automatic upgrade proposed 11 and was not applied as is
        (junk, a typo, an over-long caption); 9 written by hand (caption_fix_eye.py)
      - Media, last: the 379 new maps stored as 256-colour PNGs, 103.8 MB -> 35.9 MB, mean colour difference at most
        0.07 (media_optimize_maps.py; originals in %LOCALAPPDATA%\QB_media_originals\maps); 387 unused files (the
        replaced maps, the replaced and duplicate Architecture pictures, the old silent Sinfonietta clip), 206 MB,
        copied to %LOCALAPPDATA%\QB_media_unused and sent to Anki's media trash (media_unused.py)
- [x] Classical Music periods, found through the hint (Schubert's Mass No. 6 "Classical"): Period had been set from
      each work's date against fixed cut-offs, splitting composers -- Rachmaninoff's Second Concerto and Mahler's
      Fifth "Modern" beside their earlier "Romantic" works. cm_period_fix.py, 89 fields: one period per composer
      (Romantic: Schubert, Mahler, Rachmaninoff, R. Strauss, Sibelius, Elgar, Puccini, Dukas, Debussy; Classical:
      Beethoven; Modern: Ravel, Satie, Schoenberg). Post-war composers split Modern/Contemporary by 1975 left
- [x] 2026-09-14, Carter: "the region hints dont help when the maps are already labelled with the country. an example
      of a good hint would be revealing the state in which the mountain lies". On the Natural Earth maps (which label
      countries, not states) the Region reveal now names the state or province: a city's Subdivision; for peaks and
      waterfalls the admin-1 unit at the point (both sides within ~5 km of a border); for lakes, deserts, ranges,
      islands, peninsulas and rivers the units holding most of the outline, four at most (geo_admin1_hints.py ->
      geo_admin1_hints.json, read by geo_locator.py). Natural Earth's out-of-date units corrected by hand (Nepal's
      provinces, Kenya's counties, Ağrı for Ararat, Central Papua for Puncak Jaya); any hint repeating a word of the
      answer is dropped whole. 217 hints
- [x] 2026-09-14, Carter: "do 2. and 3. first" -- the Wikidata first-value fields and the captions
      - Wikidata fields (wd_field_fixes.py, 239 notes): Geography "Part of" alliances, eras and "Earth" removed (Ottoman
        Empire "Central Powers", Qing "Late Imperial China", the oceans, Great Bear Lake's biosphere reserve); the
        last historical city subdivisions (Antwerp "Margraviate of Antwerp" -> Flanders, Salzburg, Zurich, Lyon, Cusco;
        Jerusalem -> Jerusalem District to match its Parent); Seine source and Volga mouth; lake areas "square km" ->
        km². Architecture: figures' Location was their birthplace or its old state (Louis Kahn "Russian Empire",
        Borromini "Switzerland", Palladio "Republic of Venice") -> the modern country where they worked; buildings'
        places all end in their country, present French regions, English region names, no "near"/"outside".
        Photography: German Empire/Kingdom of Bavaria, province-only places (Aydın Province, Ituri), lowercase starts,
        one spelling per city. Art: Bellows's Massacre at Dinant had Harvard placed in New Haven. Region reveal refreshed
      - Architecture captions (arch_repeat_caption_fix.py, 311): 184 cards repeated one "Name, Location" caption under
        every picture. Every picture looked at and captioned from what it shows (the view, the part, the artwork)
      - Architecture wrong pictures and gaps (arch_wrong_picture_fix.py, 62 cards): pictures of another building
        removed -- Santa Maria dei Miracoli on San Marco, the Prophet's Mosque on the Great Mosque of Mecca, Beijing's
        Bank of China head office on the Hong Kong tower, a broch on Skara Brae, a modern block on Sultanhanı, an
        unidentified tower drawing, a sculpted head, a register plaque. Saint Mary's Church, Lübeck had three
        pictures of St. Mary's Basilica, Kraków: replaced with its towers, nave and the bells that fell in 1942.
        Failure found on the way: 56 cards had an empty slot before a filled one, and the caption sheets numbered
        pictures in order while the fix wrote by slot, so some captions sat under no picture; every card closed up with
        each caption under its picture, checked on sheets (Spandrel, Ogee arch, Aldo Rossi had their right caption in
        an empty slot)
      - Lead pictures that never showed (accent_media_fix.py): Tōdai-ji, Ryōan-ji and Niterói's fields named the file
        with its accent, the download was saved without it, and media_unused.py then trashed the "unused" file.
        Restored from %LOCALAPPDATA%\QB_media_unused under the exact on-disk name. missing_media_scan.py checked every
        picture and sound in all 10,046 notes: no other reference without its file
      - Geography photo captions (geo_caption_place_fix.py, 146): file names, stock text ("NASA - Visible Earth",
        "Location of XY (see filename) on the globe"), German and Spanish, cut-off sentences and addresses rewritten
        from the photo. Photos of the wrong place replaced and looked at: Haryana (the Yamuna at Agra -> Pinjore
        Gardens), Guanajuato (its flag -> the capital at dusk), Coral Sea Islands (Green Island, Queensland -> Willis
        Island), Assyria (a map of the Roman province of 116-118 -> the Nimrud lamassu)
      - Same defect looked for in Art and Photography (dup_caption_scan.py): no repeated captions; one card short of a
        caption -- Photorealism's second picture. Both identified by file hash and captioned with their painters:
        John Baeder, John's Diner with John's Chevelle; Magda Torres Gurza, La hora del té
        (art_photorealism_caption_fix.py). Stralsund's unplaced vault picture: a caption that says only what is seen
      - Performing Arts had no field for a caption: Caption added after Media and shown under the picture on both
        answer sides in the Geography/Architecture caption style, only when present (pa_caption_field.py; templates
        backed up in templates_backup/pa_before_caption_2026-09-14.json)
- [x] 2026-09-14, Carter: "lots of audio missing from the CM deck". No clip was missing (1,492 of 1,492 on disk):
      209 AUDIO to COMPOSER cards had been created with nothing to play. Anki makes a card when its front uses a
      non-empty field; the front used only {{Audio}}, until cm_hint.py put the {{#Hint}} block outside {{#Audio}} and
      filled Hint for every work -- so every early work without a recording (Plainchant, Micrologus, Josquin's masses)
      got an audio card. The hint now sits inside {{#Audio}}; the 209 cards (none reviewed) are suspended and are empty
      cards for Tools > Empty Cards (cm_blank_audio_fix.py). Swept: Geography's Locator hint is inside each front's own
      condition ({{#Map}}, {{#Image}}), so it made no cards
- [x] 2026-09-14, Carter on the picture grids (figs_layout_fix.py, Art, Photography, Architecture; every case rendered):
      - "four images ... condense to 3 images on the top row and 1 on the bottom ... go down to two rows": grids were
        auto-fit with 190-200px cells, so a 700px Art card fit three. Four pictures now take four columns at 784px and
        wider, otherwise two -- checked on Mantegna's four panels at 900 and 480px and a four-picture Architecture
        term card at 1100 and 640px
      - "kara walker cards have two images and they are left-centred": the old slideshow's prev/next arrows were still
        in the ARTWORK to ARTIST grid, shown by its script for two or more pictures, and each took a cell. Hidden
      - "photography images condense their borders upon reveal": the answer side wraps a captioned photograph in a
        figure inside the old slideshow grid, and both shrank to the picture, so the frame hugged the photograph where
        the question side framed the tile (Niépce: 584x300 in front, 430x300 behind). Both now fill the row, at the
        question side's 300px
- [x] Performing Arts captions (pa_captions.py proposes, pa_caption_review.py writes): each of the 318 pictures matched
      to its source file by hash, drawn on 27 sheets and captioned by eye -- the automatic text was German or Dutch,
      biography, or nothing for 100 of them. 309 captions. Seven pictures of the wrong thing removed: stacked café
      chairs on Café Müller, the footballer Michael Bennett on the choreographer's card, Geraldine Farrar's operatic
      Manon on MacMillan's ballet, an unidentified house on Kenneth MacMillan, the Bitches Brew Live compilation cover,
      the scripture on The Book of Mormon, a black image on San Francisco Ballet. Uncaptioned: Serenade, Sweeney Todd
- [x] 2026-09-14, Carter: "ok, complete the items from the Concerns"
      - Performing Arts pictures (pa_picture_replace.py, 11 cards; candidates on Commons contact sheets and in each
        article's own media, every one looked at): Swan Lake, The Nutcracker, Cinderella and The Merry Widow showed
        their composer and now show a production (Brisbane 1953; the Nutcracker's leap; Liashenko in Ashton's
        Cinderella; Conti and Kulczycka, 1936); the removed seven replaced where a true picture exists (Prague's
        L'Histoire de Manon, MacMillan's blue plaque, the Bitches Brew cover, the Eugene O'Neill marquee, Jocelyn Vollmar
        with San Francisco Ballet, 1947); Serenade's opening tableau and Sweeney Todd with Mrs. Lovett replace the two
        unusable pictures, all captioned. No free picture exists of Café Müller or of the director Michael Bennett
        (every Commons "Michael Bennett" is a footballer): both left without one
      - Stralsund St. Marien: the unplaced vault picture matched by eye to Commons "Westwerk Netzgewölbe" -- the church's
        own westwork; kept and captioned
      - Classical Music recordings (cm_audio_candidates.py searched Commons for all 210 works without a clip;
        cm_audio_fill.py): 13 added, each a recording whose description names that work or the card's own movement --
        Josquin's Missa Pange lingua, Die Walküre, a Transcendental Étude, the Fra Diavolo and Gypsy Baron overtures,
        Béatrice et Bénédict, "Il lacerato spirito", Mignon, Chaliapin's "Le veau d'or", the Libuše fanfare, Ruslan and
        Lyudmila, Lully's "Enfin, il est en ma puissance", Handel's "Bel piacere". 75-second excerpts, loudness-normalised,
        MP3; their audio cards unsuspended. Refused: pronunciation files, namesakes by other composers, arrangements, MIDI,
        another act than the card's. The other 197 have no free recording on Commons (mostly 20th-century operas)
      - Found choosing them: Rossini's Otello carried Verdi's "Credo in un Dio crudel" -> the Willow Song, "Assisa a' piè
        d'un salice" (cm_movement_fix.py); every movement shared across composers read -- no other copy
- [x] 2026-09-14, Carter: "proceed with all" (the seven remaining items)
      - Caption junk, Art/Photography/Architecture (caption_junk_fix.py, 61 notes): Commons catalogue records, file
        names and foreign text rewritten from the picture (Cole's The Oxbow, Kritios Boy, Isle of the Dead, El Escorial,
        Pont du Gard, the Royal Pavilion, Palmyra, the Darwin D. Martin House); 27 Architecture portraits whose caption
        was only the architect's name (the card's answer) emptied. Backup caption_junk_before_2026-09-14.json
      - media_unused.py made accent/case-safe before any cleanup: a file matching a reference only once accents and case
        are folded is kept and listed ("referenced under another spelling") -- the Tōdai-ji mechanism
      - Geography river maps: the 36 older river maps redrawn in the Natural Earth style (ne_render.py -> ne_apply.py),
        every map looked at on sheets. Renderer defects found on the way, each fixed at its mechanism:
        * the largest lakes and rivers were never drawn as context: "scalerank or 9" read rank 0 (Superior, Baikal,
          Victoria, the Amazon) as 9. Swept: 46 maps already on cards had a rank-0 lake or river in view (the Great
          Lakes, Ladoga, Balkhash, the Aral Sea, Malawi, Tanganyika...) -> re-rendered under new _v2 file names (a
          same-name file would neither be re-applied nor re-fetched by synced devices) and applied
        * a namesake inside the note's countries: Rio Negro (Patagonia), Brazil's and Bolivia's Rio Grandes, southern
          Mexico's, Ontario's Mississippi River -> NOTE_BOX per system
        * reaches filed under their own names: the Brahmaputra's Dihang, the Congo's Luapula and Luvua, the Yellow
          River's upper course and loop ("Huang"), the Salween's Nu, the Amazon's "Amazonas", Selenga, Xi for the
          Pearl, the Nile's White/Mountain/Albert/Victoria Nile -> ALIASES; the lower Mamoré (under "Guaporé") clipped
          to its box; the St. Lawrence and Congo systems drawn with their lakes (Superior to Ontario; Bangweulu, Mweru)
        * the locator inset hid the Amazon's lower course when no corner was clear of the river's box -> the corner the
          drawing crosses least
      - Geography Info rebuilt (geo_info_rebuild.py, 309 notes; geo_info_scan.py found the classes, the rest came from
        reading all 1,063 notes). Mechanism: sentences were split at every full stop ("a U.S" cut, "The exact." kept)
        and paragraph fields cut at a character count, leaving 142 unbulleted paragraphs, cut and run-together bullets,
        Wikidata descriptions glued in front, pronunciation debris and bullets whose referent sentence was dropped;
        also a city lead on three state cards (Rio de Janeiro, São Paulo, Bremen), Pondicherry city on the union
        territory, a 2019-abolished state on Jammu and Kashmir. Rebuilt as the article's first three consecutive
        sentences, abbreviations protected as whole words (a first dry run's "ca." inside "Africa." merged sentences
        and dropped Morocco's opening), respellings, other-language names and unused acronyms removed, B.C.E./C.E.
        Every proposal read, three times after each splitter fix; Guam, Sutherland Falls and Manchuria written by
        hand; Yellow Sea and Denmark Strait kept. Backup geo_info_before_2026-09-14.json (+ attica_peloponnese)
      - Geography figures (geo_measure_check.py set every Depth/Height/Length/Area beside its infobox;
        geo_measure_fix.py, 36 notes). Mechanism: Wikidata "vertical depth" is a mean on some items, a maximum on
        others; Depth is now the maximum throughout (Mediterranean 1,541 -> 5,109 m; Baltic, Marmara, Galilee,
        Labrador, Andaman, Gulf of Oman, Pacific). Also Yosemite Falls 436 m (upper fall) -> 739; Strait of Malacca
        8,765 -> 200 m; Elbe 368 -> 1,094 km; Andes, Carpathians, Deccan, Celebes Sea and three oceans contradicted their
        own Info; five reservoirs carried "Largest reservoir (180 km³)" as Depth -> real depth, volume rank into Info.
        Definition-only differences left (shrinking lakes, deserts' areas)
      - geo_misc_fix.py: Strasbourg's commune population (the lead gave the metro figure); Equatorial Guinea's capital
        Ciudad de la Paz (decree of 2 January 2026) and its Capital Info; "France - Lille"; Christmas Island's photo
        slot held a globe locator -> Flying Fish Cove (looked at); Balkans (region) duplicated Balkan Peninsula's
        article and figures -> suspended and tagged duplicate, as Malacca Strait already was
      - Classical Music recordings from Internet Archive 78s (ia_audio_candidates.py searched archive.org for works still
        without a clip, 1890-1925 -- US public domain; cm_audio_ia.py): 24 added, each an item whose title and tracks
        name the work (and the card's movement): the Lener Quartet's Op. 131 (1924), Heifetz's Caprice No. 13, "Tu che
        invoco" (Mazzoleni 1909), Korsoff's "La belle Inès", "Rachel, quand du Seigneur", Euryanthe, Lortzing's Undine,
        Der Barbier von Bagdad, the Tancredi overture, "Nacqui all'affanno", Poliuto, "O mio Fernando", "I dreamt I dwelt
        in marble halls", Attila, "Je veux vivre", "Ebben? Ne andrò lontana", "Son pochi fiori", Muzio's "Senza mamma",
        the Véronique donkey duet, Hänsel und Gretel, Königskinder, the Vilja-Lied, Jeritza's "Glück, das mir verblieb",
        De Luca's "Lascia ch'io pianga". 75 s, loudness-normalised (every clip measured: mean -26 to -19 dB, no silent
        stretch); audio cards unsuspended. Refused: J. S. Bach's suite for C. P. E. Bach's concerto, Finlandia for
        Sibelius's symphonies, Lortzing's Undine for Hoffmann's, arias from another act than the card's. Guard: the
        note's own Work/Composer must match (the candidate list's movement column was misaligned on one row)
      - Performing Arts generic captions (pa_generic_caption_fix.py, 38): each picture paired with its source file on
        sheets (same photograph confirmed by eye) and captioned from the record -- Agnes de Mille as the Priggish Virgin
        (1941), Weill in Vienna for Mahagonny (1932), Mingus on the Bicentennial, Loie Fuller's is an engraving from the
        Album Mariani; the six unsourced production photos found on Commons by eye (Hair in Montreal; The Producers, The
        Pajama Game and Bye Bye Birdie at The Muny; Funny Girl in Brno). Left: Lester Horton (no source), Damn Yankees
        (record names no company)
      - Follies showed the Geritol Follies, a seniors' revue (matched on the word): picture removed, no free photograph of
        Sondheim's musical exists (pa_follies_picture_remove.py). Swept: pa_category_check.py over every Performing Arts
        picture whose Commons categories never name the card's subject -> 4 flagged, all looked at and right (Martha
        Graham on Appalachian Spring, Nijinsky as Petrushka, Cambon's signed Le Corsaire design, the Panovs' Faun)
      - Phone width and night mode, every card type of all seven note types, question and answer (render_pass.py, 150
        renders on 7 sheets): nothing overflows or clips at 400px. Night mode: Art, Architecture, Classical Music,
        Geography, Performing Arts and Photography keep their light palette on purpose (each night rule restates the day
        colours); StockFisher Cloze+ has its dark theme; both render correctly. Harness fixes on the way: headless Chrome
        will not size a window under 500px (a 400px render was a clipped 500px layout) -> the card loads in a 400px
        iframe; Anki's night classes go on html as well as body. Checked and left: the gap before "." after a cloze is
        the highlight's padding (no stored space in 1,431 notes)
      - Media, last (media_unused.py, now accent/case-safe): 112 unused files, 32 MB -- the 46 map files superseded by
        their _v2 renders, the 36 old river maps, the replaced and removed pictures (Follies' Geritol Follies, Christmas
        Island's globe, the Performing Arts and Architecture pictures of the wrong thing) -- copied to
        %LOCALAPPDATA%\QB_media_unused and sent to Anki's media trash. No file matched a reference only under another
        spelling. missing_media_scan.py afterwards: every picture and sound referenced has its file
- [x] 2026-09-14, Carter: "yes, do all of them" (the eight follow-ups)
      1. Maps in Geography photo slots (geo_photo_map_scan.py: caption/file words and flat-colour pictures, 21 drawn on a
         sheet): 12 PHOTO to NAME cards showed a relief, topographic or history map -- one with a "Rise of the Ottoman
         Empire" legend. geo_photo_map_replace.py: photographs chosen by eye on Commons sheets, none lettered with the
         answer -- Central Balkan ridge, Kunlun valley, Tana Toraja, the Süleymaniye, a jacaranda in 1970s Salisbury
         (Rhodesia's stamp refused), Kandy Lake c. 1880, the Taj Mahal, the Pella stag-hunt mosaic, Dodona's theatre, the
         Mekong at Luang Prabang, the Appian Way, Kangding. Balkans (suspended duplicate) left
      2. Figures contradicting their own Info (geo_self_conflict_scan.py; geo_self_conflict_fix.py, 9): the Yellow River
         called "Longest river in Asia" (the Yangtze is), Pearl 2,200 vs 2,400 km, Bay of Bengal, Jeju, Sonoran, Thar and
         Chihuahuan areas, Qinghai Lake's depth; the Arabian Sea's lead gave 5,395 m against the card's 5,800 (Britannica
         5,803) -> the Info clause removed rather than a guess
      3. Cloze+ context lines (cloze_vague_scan.py over 1,431): the flagged lines nearly all add a real fact; the one pure
         filler, Chesterton's "How I Found the Superman" ("both prominent literary figures ... friendly debates"), now says
         the sketch mocks the Übermensch Shaw had staged in Man and Superman (cloze_context_fix.py)
      4. Scandinavia's map was the Scandinavian Peninsula's polygon: now Denmark, Norway and Sweden from the country layer,
         Svalbard, Jan Mayen and Bouvet clipped off (ne_render.py regions), applied as _v3
      5. Classical Music, openly licensed recordings of any date (ia_cc_candidates.py -> ia_cc_filter.py, 22 works with a
         title match, each read): almost all refused -- radio shows and lectures, commercial CDs/LPs with uploader-added
         licences, 1926-1946 recordings still protected in the US (1934 Mathis der Maler), other acts, a Pavane of unstated
         instrumentation. Added (cm_audio_cc.py): Barber's Violin Concerto, Elena Urioste / DuPage Symphony under Eric
         Pancer, 2011, CC BY-SA by the conductor. The other ~170 works have no free recording that can be verified
      6. Leftover pictures (leftover_picture_fix.py, 10 notes, each looked at): Frankenthaler's The Bay on Abstract
         Expressionism, Benton's People of Chilmark on Regionalism, the Old New Synagogue on Gothic architecture, Saint-Ouen's
         chevet on Apse; the Romanesque capital, Byzantine opus sectile floor and Seljuk muqarnas portal captioned as seen.
         Renaissance architecture showed a Baroque altar at the Salute -> Brunelleschi's Ospedale degli Innocenti. Lester
         Horton's portrait matched no source anywhere -> Bella Lewitzky and Sondra Orans in his Warsaw Ghetto, 1949; Damn
         Yankees named as Otterbein University Theatre and Dance, 2017. Café Müller, Michael Bennett, Follies: no free
         picture exists
      7. Paganini's clip was Kreisler's arrangement with piano: now Ivan Dolgunov's unaccompanied Caprice No. 9 (his own
         CC BY-NC-ND release)
      8. Night themes (night_theme_apply.py): the "night mode shows the light design" blocks removed from Art, Architecture,
         Classical Music, Geography, Performing Arts and Photography, and one marked dark block appended last in each --
         Cloze+'s ground and ink with each deck's accent lightened, plus the colours written as literals (Art's picture
         plates, tag pill and captions; Architecture's slideshow buttons; figure captions). Day mode untouched. Stylesheets
         backed up in templates_backup/night_theme_before_2026-09-14.json. Rendered all 25 card types (render_pass.py:
         phone day, phone night, desktop night): Art's names and titles came out dark on dark -- its frozen templates
         write colours inline (#2b2b2b, #6b4c3b, three greys, #1f3f66, the #efe8da plate) -> matched by value with
         !important in Art's night block and re-rendered: every card readable, day renders unchanged

## 2026-09-15 — Carter: "delete the duplicates. add the captions to the art deck, finish all other incomplete tasks"; then the series italics, movement cards, Geography hints, night mode and Geography info
- [x] Duplicates deleted: Malacca Strait and Balkans (geo_duplicate_delete.py; backup geo_duplicates_deleted_2026-09-14.json)
- [x] Art captions (art_caption_fill.py, 118 notes): every picture of the 119 uncaptioned notes read on 15 contact sheets,
      the doubtful ones drawn large and checked against Wikipedia (media file names, article images). Artwork cards already
      name the work, so a caption says which view, part, version or companion piece ("Left wing: Étienne Chevalier with
      Saint Stephen", "<i>Sight</i>", "The Dresden version, 1819"). Pictures of something else removed: a cake on Klein's
      Anthropometries, Kaprow's Yard on 18 Happenings, Salcedo's Bogotá chairs on Shibboleth, a boat on the Kota
      reliquary, Ai Weiwei's Porcelain Cube (twice) on Man in a Cube. My Lonesome Cowboy showed two other Murakami works:
      now the Marianne Boesky Gallery's photograph of the sculpture (art_murakami_fix.py). Spot-rendered
- [x] Series italics. Carter: "the name of the series should be italicized, but the [brackets] and the words 'series' or
      'period' or whatever should not be". Mechanism: the templates italicised the whole Title and Series fields whatever
      their markup. art_italics_fix.py: Art CSS makes the title elements roman with their own <i> italic; the two italic
      Series divs set to normal; all 306 Series values read -- titled series [<i>Name</i> series], artists' periods and
      place-named groups roman, notes roman with titles inside italic (345 notes); 15 titles with a descriptor inside the
      <i>. Errors found reading them: Brunelleschi's Sacrifice of Isaac was the north-doors competition, not the Gates of
      Paradise; af Klint's series is The Paintings for the Temple ("Paintings for the Future" was the 2018 exhibition);
      the "My Lonesome Cowboy series"; Dürer's Portrait of a Young Man. art_title_back_paren.py: the (or ...) spans on
      TITLE to ARTIST's back line. Same mechanism swept: Photography's title classes (CSS rule + 6 titles), Performing
      Arts (1 title) -- photo_pa_italics_fix.py. Rendered
- [x] Movement cards (art_movement_cards.py, 46 movements). Carter: "there should be a main proponents or something and it
      shouldnt mention those guys in the description". Artist = main proponents, full names; Notes (Detail) rewritten
      without the proponents' names; Descriptions written for the 26 older movements (new DEFINITION to NAME cards);
      DEFINITION to NAME back labels "Main proponents" and "Detail"; MOVEMENT to FIGURES asks "Main proponents?" and adds
      the Description as "About"; labels change only for Kind Movement; names shown with middots. Rendered
- [x] Geography hints (geo_locator.py rewritten). Carter: "should never be the continent, and should only be the country
      when its not apparent by the image ... the michoacan card ... the only logical hint would be its capital city".
      Locator is now "map tiers##photo tiers", each labelled (Country, Region, Capital); no continent anywhere. Map card:
      Natural Earth maps the state/province; subdivisions the capital (geo_capitals_fetch.py -> geo_capitals.json, 216
      read, 19 corrected: district seats for city-provinces, Maharashtra's winter capital...); other old maps the country
      only where the map does not show it (every map looked at on sheets). Photo card: the country, then state or
      capital. No country where it is the answer renamed (Ceylon, Siam, Zaire...). Modern countries corrected: Punjab,
      Bessarabia, Moldavia, Papal States. 781 notes; templates' script replaced
- [x] Night mode (contrast_check.py measures every visible text on every card type in headless Chrome). Night: nothing
      under WCAG AA on any deck (lowest 5.7:1). Day: 144 small labels in every deck's muted colour at 3.4-4.3:1 ->
      contrast_fix.py darkened each to 4.8:1 (day stylesheet; Art by override since its colours are inline). Rechecked:
      0 low. Carter's phone still shows the old night design until the upload sync
- [x] Geography info trim (geo_info_trim.py, 486 notes). Carter: "remove useless geography info (like coordinates, exact
      details for unimportant things, extensive other names)". 475 flagged bullets read and decided by hand: coordinates
      (Great Bear Lake, Athabasca, Svalbard...), census counts and "as of 2026" estimates, GDP, municipality counts,
      trivial other names ("also known as the Channel") removed or rounded into their fact; exact dates to the year;
      imperial conversions after metric figures dropped throughout; km2 -> km²
- [x] Cloze+ second read (cloze_factcheck.py support list, every clue read; web checks): 33 notes fixed in
      cloze_clue_fix.py to _fix5.py -- invented anecdotes and quotations (Bernini's "lost-lizard method", Triton quote,
      fruit claim; Evelyn's stage fire), misattributions (Cut the Line is Benton's, Boccioni's Fist Balla's, The Abandoned
      Town Khnopff's), invented precision and names (KURI, Six Stunners, chessboards of the night, Vesnin towers),
      anachronisms (Rayonism/agitprop, Wylie at Pont-Aven)
- [x] Low-resolution Architecture pictures (arch_hires_match.py): the 33 under 400px matched against their articles'
      images by hash -- no larger copy of the same picture exists (portraits, article thumbnails); left
- [ ] Romanesque capital, Byzantine opus sectile floor, Seljuk muqarnas portal: no source found by image matching;
      captions stay descriptive
- [x] Media: 11 unused files (the removed and replaced Art pictures, the deleted duplicates' maps) copied to
      %LOCALAPPDATA%\QB_media_unused and sent to Anki's media trash

## 2026-09-15 (later) — second fact-check read of the other decks; Carter's founder, Kremlin, main-architect and caption requests
- [x] Art "Group or Movement" (art_group_fix.py, 525 notes). Carter: "holman hunt card says 'hunt was a founder of...'. as per
      my other cards, put the word founder in brackets". Mechanism: prose and stray words in the list field. Swept all 3,000+
      values: Hunt -> "Pre-Raphaelite Brotherhood (founder)"; "movement" suffixes, "Ashcan School (of American Realism)",
      &nbsp; around bullets, Fontainebleu, Royal Academy of Art, Color Field; wrong founder marks removed (Vermeer/Delft,
      Lissitzky/Suprematism, Guston/New York School, Titian/Venetian School, Ambrogio Lorenzetti/Sienese); verified founders
      marked (Millais, Kandinsky, Marc, Kirchner, Schmidt-Rottluff, Arp, Sérusier, Tatlin, Monet, Group of Seven, Ensor,
      Khnopff, Duchamp/Gleizes/Stella for the Society of Independent Artists); Jeff Koons had Willem de Kooning's groups
      (name match) -> Neo-Pop Art; partly empty artists filled from their other notes (field is back-only). Rerun 0
- [x] Art concept cards (art_concept_cards.py, 36 notes): the 11 older technique notes given Descriptions, "Practised by"
      tails removed, title italics fixed, Pointillism -> Seurat's chromoluminarism
- [x] Photography and Performing Arts prose (prose_fix_second_read.py, 134 fields; every line read, web checks): wrong facts
      (Anne Frank photo was 1939, not one of the last; Country Doctor eleven pages; Golden Spike champagne not water; Mamie
      Till's words; Le Gray's Brig one negative; Donahue 30 August; Old Faithful 1871; Alicia Alonso's company names; Béjart
      citizenship invented; Graham 65 years; Tim Rice's Aida was with Elton John; Time Out not every track odd metre),
      "The Blue Marble Selfie" was really the STS-31 crew portrait (retitled, cards suspended: shirts and patch give it
      away), and 70 encyclopedia-lead notes rewritten as clues
- [x] Front-answer scan (front_answer_scan.py renders every front with the answer blanked, hidden blocks removed): my own
      Performing Arts rewrites had put answers on CLUE to WORK fronts (Bournonville style, Béjart Ballet Lausanne, Betty Bebop,
      fall of Saigon, producers, Washington Heights, Yankees, pajama factory, Ballet Theatre, Stuttgart) plus Mame, Wicked,
      Concerto Barocco; Classical Music definitions using the answer word; Titus van Rijn / Tamara in a Green Bugatti get
      TitleTells (front_giveaway_fix.py, 18). Remaining hits are inherent (building name contains its location on the
      NAME-shown cards, coincidental first names)
- [x] Moscow Kremlin and main architects (arch_architect_fix.py, 97). Carter: "moscow kremlin should not say its own name.
      also should have a better pic. also palace of facets?? ... underline the most prominent or 'main architect'".
      Kremlin: picture 2 was a cabinet card printed VUE DU KREMLIN -> Commons 2026 spring view; "Palace of Facets" was a
      building given as architect -> Solari (underlined), Ruffo, Aloisio, Fioravanti; date 1485–1495; captions without the
      name. All 55 multi-architect works: semicolons, main architect(s) underlined, firms left whole. Patrons marked
      (patron): Hadrian, al-Mutawakkil, Doge Contarini, Absalon, Ikeda Terumasa, Qutb al-Din Aibak, Ur-Nammu, Desi Sangye
      Gyatso, Prince Toshihito, Nerses III; Cluny -> Gunzo, Hézelon, Abbot Hugh (patron). Name spellings matched to figure
      notes; 25 inception years given construction spans; ArchitectTells on 5 works whose name or alternate names the
      architect (Rudolph Hall, Breuer Building, Sullivan Center, Rietveld Schröder, Qutb Minar) -- **run Tools > Empty Cards**
- [x] Architecture prose (arch_prose_fix.py, 101): Kölner Dom "tallest church 1880–1994" (tallest building 1880–84),
      Lincoln "tallest until the Eiffel Tower", Ulm "currently tallest church" (Sagrada Família topped out Feb 2026),
      Skytree, Aparecida second largest, Roskilde, Qutb Minar, Bublik, Golden Temple, Pisa Cathedral notes about the tower,
      typos; 30 encyclopedia-lead Descriptions rewritten; 40 Notes that repeated their Description given another fact
- [x] Pictures that print their own name (Windows OCR of all ~1,300 Architecture pictures, each hit looked at):
      arch_picture_fix.py crops postcard/print inscriptions (Djenné, Notre-Dame du Haut, Spanish Steps, Sacré-Cœur, Paxton,
      Ziggurat, Karnak model, Corniches plate, Jugend cover), blurs signs (Parkroyal, Ivanovo, Piazza d'Italia, Colosseum,
      Letchworth), crops Casa Batlló's banners, drops the Panama "THIRD SET OF LOCKS" board and the 1925 Arts Décoratifs
      poster, replaces the Bauhaus sign view and the Eames exhibition poster. Replaced originals backed up and trashed
      (media_trash_replaced.py)
- [x] Captions. Carter: "the captions need not contain the city, location, etc. they are intended to explain images that
      are uncertain". arch_caption_trim.py (496 Architecture captions: names and places removed, Commons leftovers removed,
      captions that explain nothing emptied, ~250 written by hand); geo_caption_fix.py (131 Geography photo captions).
      Art, Performing Arts and Photography captions identify the version, performer or example shown and stay
- [x] Architecture figures (arch_figure_fix.py, 138 fields on ~80 figure notes): encyclopedia-lead Descriptions with
      "Architect of X" tails rewritten as clues, and database "notable work" lists replaced by the works quizbowl asks
      about (Zumthor "Feldkapelle", Scarpa "ashtray", Sullivan "Holy Trinity Cathedral", Safdie a book, Eisenman a
      stadium). Descriptions sit on DEFINITION to NAME fronts, so the script refuses any that contain the figure's name;
      H. H. Richardson's said "Richardsonian Romanesque". Front scan rerun: no new hits
- [x] Second OCR pass (multi-, back- files the first pass missed): Paxton portrait, Ziggurat plan, Karnak model, Corniches
      plate and Jugend cover cropped (arch_picture_fix.py); originals backed up and trashed
- [x] Classical Music concept notes (all 86 read): Song cycle and Sprechstimme titles italicised, Fantasia wording
      (cm_nickname_fix.py, 3). Work notes carry no prose
- [x] Geography Info second read: read_geo.txt never existed (progress lost, not just unfinished), so
      re-approached as a structural diagnostic sweep of all 1,061 notes instead of a blind manual
      re-read -- flagged 84 candidates (33 images without captions, 11 "no Region", 40 "no Parent"),
      hand-checked every one: the 11 are continents/oceans (correctly have no Region, they ARE the
      top level) and the 40 resolved into U1 (35 historical/cultural regions needed Now filled) and
      confirmed-fine cases (Lake Vostok, Balkan Peninsula, Micronesia use Region/Part of correctly).
      The 33 uncaptioned images (mountains, peninsulas, islands, a few cities) were captioned in the
      same pass -- reviewed all 33 on a contact sheet, wrote a one-line caption describing what's
      actually shown rather than restating the Name, matching the deck's existing caption style
- [x] U1 Geography: 35 still-existing historical/cultural regions (Mesopotamia, Gaul, Bohemia,
      Silesia, Bengal, Manchuria, Thrace, Dalmatia, Moravia, Pomerania, Bessarabia, Wallachia,
      Ruthenia, Alsace-Lorraine, Epirus, Deccan, Sindh, Punjab, Formosa, Siberia, Normandy, Bavaria,
      Saxony, Swabia, Franconia, Tuscany, Lombardy, Latium, Attica, Peloponnese, Cappadocia,
      Aquitaine, Burgundy, Republic of Venice, Republic of Genoa) had no Now field -- written and
      verified by re-read. The other 6 flagged (Abyssinia, Galicia, Livonia, Macedonia, Khorasan,
      Sogdia) already had Now; left Existed blank since they are geographic terms with no clean
      founded/dissolved date, not defunct polities
- [x] U2 Geography bug fixed: Aquitaine and Burgundy Existed "1960-2015" (the modern French
      administrative region's dates, not the historical region) cleared. Mechanism: an automated
      fill pulled Wikidata P571/P576 off the administrative-region entity instead of the
      historical-region entity. Swept all 1,061 notes for the same pattern (Existed both years
      >= 1900): 16 of 18 are correct dissolved 20th-century states, only these two were wrong
- [x] U3 Architecture: Work-to-Architect front no longer shows Style -- a work's style often
      strongly implies its architect or era, making the front too easy. No replacement hint added:
      a bare name matches how DEFINITION to NAME already works and keeps recall difficulty honest
- [x] U4 Geography: Ladakh subdivision map recolored to match the family palette (cream landmass, dark-red highlight, blue water) -- Wikidata's P242 for Ladakh only has a flat-grey "de-facto" disputed-boundary style map, unlike other states' cream/red locator series, and no matching-style file exists on Commons for this union territory. Fetched IN-LA.svg at 3000px, remapped its 5 flat colors to the standard family palette, cropped a black frame artifact
- [x] U5 Geography bug fixed: Quintana Roo Pronunciation field held "/h (170 mph), with gusts up to 320 km/" -- a hurricane wind-speed fragment from the climate section, not a pronunciation guide. Mechanism: an extractor looking for IPA text between two "/" characters matched a km/h unit instead. Swept all 1,061 Pronunciation fields for the same pattern (digits/mph/km present, no IPA characters): isolated to this one note. Cleared the field, matching the other 31 Mexican states which correctly have no Pronunciation value
- [x] U6 Geography: Balkan Peninsula's single-point dot replaced with a proper shaded-region map
      matching the other 12 peninsulas' style. Cause: Natural Earth's named-regions layer has no
      "Balkan Peninsula"/"Balkans" polygon at all (real data gap; Sinai Peninsula has the same gap
      but its Info/Parent are correct, so left alone) -- ne_render.py's existing "region = union of
      countries" path (already used for Scandinavia) extended to the 10 countries every definition
      of the Balkans agrees on; filled the note's own empty Parent field so the match could run
- [x] U7 Geography: Flag Note now reads "SIMILAR TO Iraq (text instead of emblem), Yemen (no emblem)"
      instead of a bare list -- added a label (matching the deck's existing .geo-fact-label style),
      no data changes needed since all 43 Flag Note values already follow the same "Country
      (difference)" format
- [x] U8 Geography: Borders fact (list of neighbouring countries) removed from the FLAG to NAME back
      -- irrelevant to identifying a flag and just clutter; left in place on MAP/PHOTO/CAPITAL to NAME
      where a country's neighbours are relevant context
- [x] U9 Geography: Region fact hidden on subdivision and US-state cards, where it's always fully
      implied by Parent (verified: 0 of 266 subdivision/US-state notes have a Region that differs
      from their parent country's) -- kept visible on dependency/overseas-region cards, where 21 of
      37 genuinely differ from the metropole's region (French Guiana is South America though France
      is Europe, Guam is Oceania though the US is North America, etc.) and showing it is the point.
      Read via the Kind value already rendered in .geo-eyebrow, no template plumbing needed
- [x] BONUS (found while testing U9): California's Info showed "163,696 square miles (423,970 km²)"
      -- imperial-before-metric that the earlier geo_info_trim.py pass was supposed to have caught
      but missed 30 notes across every US state map card, several mountains/lakes/islands, and 2
      cities (Liverpool, Seattle). Same mechanism swept and fixed everywhere: strips the imperial
      number+unit, keeps the metric figure. Re-scanned after: 0 remaining
- [x] Copilot audit (copilot_audit_report.txt, 41 lines) triaged: 28 of 29 findings were false
      positives from its own check design (mojibake check matched a literal "?" with no encoding
      issue at all; "TODO"/"XXX" placeholder checks fired on substrings inside real words -- "TODO"
      hides inside "masTODOn", "XXX" inside a random CDN hash; "broken image" and "empty field" both
      matched files that exist and render fine, just with ugly CDN-scraped filenames). 1 real hit: a
      stray backtick after Untitled (Heroic Symbols)'s <img> tag would have rendered as a visible
      stray character (Artwork renders raw in 6 templates) -- fixed. Swept for the same backtick
      pattern everywhere: 3 more, all inside invisible alt= text or a legitimate Commons filename
      convention, left alone. Swept for the garbled-CDN-filename mechanism (URL query params leaked
      into src): isolated to the one Dante note already found, cosmetic only since the file resolves
- [x] V1 Architecture: multi-image figures ("mosaic") -- Carter: tall/long images needed a click to see
      in full. Cause: .arch-figs/.arch-concept-figs forced every image into an equal-size grid cell
      (260px height, width:100%), so a 3.3:1 panorama (Villa Godi) rendered as a sliver and 260px-tall
      images with object-fit:cover were outright cropped. Rebuilt as a flex row: each image keeps its
      own natural width at a shared height (never cropped, never squeezed), wrapping to new rows as
      needed -- a true mosaic instead of a uniform grid. Found and removed a leftover legacy rule
      that was still winning on specificity after the rewrite (verified by re-rendering, not just
      reading the CSS). Also fixed a bug the rewrite introduced and Carter caught immediately: with
      align-items:flex-end, a captioned image sat higher than an uncaptioned sibling since flex-end
      aligned their bottoms including the caption text; changed to flex-start so images always align
      at the top regardless of caption. Verified on 3 real cards (Palladianism 3 images incl. a 3.3:1
      panorama, Sagrada Familia 2 images with one caption). Architecture only for now -- Art,
      Photography and Performing Arts have the same fixed-cell pattern (though object-fit:contain
      there, so awkwardly small rather than cropped) and are next
- [x] V2 Classical Music: 149 notes had 2-4 different recordings of the same passage stacked in one
      Audio field (Anki plays every [sound:] tag in a field in sequence, so the card played the same
      excerpt repeatedly). Carter: dedupe same-passage repeats, keep genuinely different passages
      from the same work. Checked every note's Movement field plus the movement markers embedded in
      each filename (mv I/II/III..., bare digits) for a real mismatch that would mean two different
      movements got bundled together: found 0 genuine cases among 149 (7 looked like mismatches but
      were a type bug in my own checker comparing "1" the string to 1 the number). Since I can't
      listen to judge recording quality, kept the largest file per note (usually the longer/more
      complete excerpt) and moved the other 179 files to %LOCALAPPDATA%\QB_audio_dedupe_removed
      (recoverable, not deleted); original Audio field values backed up first. Re-scanned after:
      0 notes left with more than one audio tag
- [x] V3 Caption audit triaged: report was aggregate-only (no note IDs), and its one concrete claim
      ("fa�ade" mojibake) was a false alarm, same mechanism as before (correctly-encoded façade
      misdisplayed by whatever tool printed the report). Checked the one real, checkable pattern
      myself instead: a caption repeated on the SAME note across two different pictures (genuinely
      confusing, unlike reuse across different notes). Found 4 in Architecture, 0 in Art/Photography.
      Looked at the actual images for all 4: Chandigarh Capitol Complex and Otto Wagner and Alvar
      Aalto were genuinely different views needing distinguishing captions (fixed); Hotel Tassel's
      two "Street façade" photos turned out to be a near-duplicate same-angle shot that slipped past
      the earlier angle review, not a captioning problem -- removed the redundant one instead of
      forcing artificial captions onto identical photos
- [x] V4 Classical Music: 222 Movement field values were named pieces/movements/arias sitting in
      plain text (Carter: "works should be italicized EVERYWHERE, for the last time this must be
      fixed"). Classified all 327 flagged candidates by hand: 105 are generic structural labels with
      no proper-noun character (Overture, Aria, Act II, Theme, Variation 18, and liturgical Mass-part
      names shared by every Requiem setting like Kyrie/Dies Irae) and correctly stay plain; 35 follow
      a "No. N, Subtitle" pattern where only the subtitle got italicized (mvt. V (<i>Songe d'une nuit
      du sabbat</i>)); 187 were straightforward named pieces (Turkish March, Ride of the Valkyries,
      The Swan) and got wrapped whole. Caught my own false positive before applying: "Prelude No. 1"
      is a bare catalogue number like "Symphony No. 5", not a nicknamed piece -- left plain. Verified
      on a real render (Ruins of Athens / Turkish March)
- [x] V1b Art mosaic (cap-figs, art-concept-figure): same fix as Architecture's V1, applied to Art's
      captioned-figure grid, which uses a different mechanism (a JS pairs captions to images at
      render time, wrapping only captioned pictures in a <figure>; uncaptioned ones stay bare <img>
      children) -- CSS handles both cases. Verified on Silverpoint (4 images, one an extreme 5:1
      panorama): no cropping, captions align correctly
- [x] V1c Found and fixed a real bug while extending the mosaic to Art's "ARTWORK to ARTIST" card:
      its .art-figs container still ran a leftover slideshow script (one image visible at a time,
      hidden prev/next arrows with no way to click through) that the other decks had already had
      removed ("the slideshow is gone" per an existing code comment) -- this one template alone was
      missed. Carter: "i dont want any slideshows that require clicking through". Removed the dead
      JS and nav buttons entirely; both images now show side by side in the mosaic, matching every
      other card type. Verified on Étant donnés (the piece where hiding the second image was
      probably defeating the intended surprise reveal, not helping it)
- [x] V1d Photography mosaic: same fix, plus the same dead-slideshow bug found in 3 places (PHOTOGRAPH
      to PHOTOGRAPHER Front and Back, TITLE to PHOTOGRAPHER Back) -- all had the identical leftover
      one-at-a-time JS with hidden nav arrows. Removed all 3. Verified on Daguerreotype (4 images,
      DEFINITION to NAME): all show, mosaic-packed, captions intact. No current Photography WORK
      note actually has 2+ images, so PHOTOGRAPH to PHOTOGRAPHER's fix couldn't be render-verified
      against real data, but it's the identical CSS/template change already confirmed working
- [x] V1e Performing Arts mosaic: same fix (no slideshow JS here, simpler single-Caption-field
      design, so no extra bug to find). No current PA note has 2+ images either, so multi-image
      packing isn't render-verifiable against real data yet; single-image case verified (Swan Lake)
- [x] Image mosaic (V1) now complete across all 5 decks that show images: Architecture, Art,
      Photography, Performing Arts done; Geography's single-image .geo-photo was already using the
      right pattern (natural aspect ratio, no forced box) and needed no change; Classical Music
      shows no images on cards. Along the way: found and removed dead one-at-a-time slideshow JS in
      4 templates across Art and Photography (Carter: "i dont want any slideshows that require
      clicking through") -- all images now show simultaneously everywhere, matching the site-wide
      click-to-zoom overlay for closer inspection instead
- [x] V5 Tier audits (architecture_tier_audit.txt, performing_arts_classical_music_canon_audit.txt)
      verified against live data -- both checked out accurately (Eiffel Tower/Petronas Towers/Milan
      Cathedral genuinely tier3-deepcut, Lucia di Lammermoor/Norma genuinely tier4-rare, Otello
      genuinely split tier2/tier3). Carter: "only correct egregious errors in tiering, it *is* a
      quizbowl studying thing after all" -- promoted only the 3 clearest cases (a top-20-by-frequency
      or extremely mainstream work sitting at the deck's absolute bottom tier): Lucia di Lammermoor
      tier4-rare -> tier2-solid (matching Carmen/Turandot, other rank-2-6 operas already at that
      level), Norma tier4-rare -> tier3-deepcut (matching Nabucco, a similarly-ranked opera), Jesus
      Christ Superstar tier4-rare -> tier3-deepcut (matching Les Misérables/Cabaret, comparably
      famous musicals already there). Left everything else alone: Architecture's tier3 items aren't
      at the bottom tier so promoting them is a judgment call, not an error; Otello's split may
      reflect the two arias' genuinely different individual fame rather than an inconsistency; the
      report's "may deserve tier1" suggestions were explicitly speculative
- [x] V6 all_notes_accuracy_audit.txt triaged: of 6 "confirmed" claims, 1 was real (Adagio in G minor's
      Composer field bare-credited "Tomaso Albinoni" -- the piece is a 1958 forgery/reconstruction
      by Remo Giazotto, only loosely based on an alleged Albinoni fragment; fixed to "Remo Giazotto
      (attributed to Tomaso Albinoni)", matching the nuance the Date field already had), 1 was a
      real false positive (San Marco's Architect field already correctly says "Domenico I Contarini
      (patron)" -- the audit didn't notice the qualifier already there), 1 is a deliberate design
      choice not a bug (O'Keeffe tagged "Precisionism" across all 26 of her Art notes, consistently
      -- debatable art-history categorization, but applied uniformly on purpose, not a slip on one
      card), 2 were cosmetic media-filename typos ("Brandenberg"/"Carmone", don't affect playback,
      left alone per the earlier Dante precedent), 1 was the reviewer's own missing-export note
      (Geography.txt), and 1 was explicitly labelled low-confidence by the report itself (Swan Lake's
      "failed/rescued" wording -- accurate shorthand, not an error)
- [ ] V7 Classical Music missing audio (started): 200 notes had no Audio field. Triaged by composer
      death year: 89 public-domain-era (findable in principle), 111 modern/still-copyrighted (mostly
      won't have a legal free source). Built a working pipeline: pip-installed a bundled ffmpeg (no
      system install needed), used it to extract a clean ~35s excerpt directly from a remote
      archive.org URL (no need to download full files first, some of which run 1-2.5 hours). 8 done
      and verified so far: Hildegard Ordo Virtutum, Ives Symphony No. 4, Bruckner Symphony No. 8,
      Haydn L'incontro improvviso (Overture), Prokofiev Betrothal in a Monastery, Cimarosa Il
      matrimonio segreto (Sinfonia), Janacek The Makropulos Affair (found by accident on a Sinfonietta
      LP that also had this), Adam Giselle. Most archive.org hits are multi-track compilation LPs
      needing their own file listing checked before extracting (same amount of work per piece as
      what's already been done), so this is realistically a multi-session task -- continuing in
      later passes rather than claiming false completion
- [x] V8 Real bug in the V1 mosaic fix: Carter caught that Art's Technique/Movement/Style cards (and
      likely others) still weren't packing side by side -- every image sat on its own row even with
      plenty of width to spare. Root cause took real digging (screenshot comparisons weren't enough;
      had to inject computed-style dumps and walk the CSSOM for matching rules): a flex item
      containing a <figcaption> takes its PREFERRED width from the caption's un-wrapped text (a
      standard flexbox quirk -- min-width:0 only fixes the item's minimum, not this initial
      preferred-size calculation), so a long caption like "Giovanni Baglione, Divine Love Conquering
      Earthly Love, 1602-03" was inflating its figure to ~420px even though the image inside was only
      150px wide -- invisible in a screenshot since there's no border on the figure itself, only the
      image, so it just looked like images refused to pair up. Pure CSS can't fix this (can't
      reference a sibling's rendered width). Fixed by extending the existing caption-pairing JS (Art,
      Photography) to measure each image's actual rendered width once loaded and pin the figure's
      max-width to match; added an equivalent new script to Architecture's static figures, which
      don't go through JS caption-pairing at all. Verified on all 3 decks with real renders at the
      actual 900px viewport (not just my wider diagnostic one): Chiaroscuro 2x2, Daguerreotype 2x2,
      Palladianism's first two images now also pair where they didn't before
- [x] V9 Classical Music: "Plainchant" was wrongly italicized in the Monophony concept card's Nickname
      ("<i>Plainchant</i> is the central Western repertory of it") -- it's a repertory/genre name,
      not a specific work, fixed. "Für Elise" was correctly italicized on its own Work note but
      NOT in the Bagatelle concept card's Nickname where it's also named -- fixed for consistency
- [x] V10 Geography: water-body cards (sea, ocean, gulf, strait, lake) showed "IN" for their
      bordering-countries fact, which is wrong -- a sea isn't "in" the countries around it. Rivers/
      mountains/deserts left alone since they're more defensibly "in" their countries (they occupy
      land within them, unlike a body of water). Added a Kind-based relabel script (same pattern as
      the Region-hide fix) that changes the label to "Bordered by" for water kinds only. Verified on
      the Adriatic Sea
- [ ] N (not started, scoped) Carter: add neighbouring-country labels to the 214 country maps,
      matching the labelled style already used on river/lake/sea/mountain maps (ne_render.py's
      base_map() already draws these labels as a matter of course -- confirmed by inspection, e.g.
      Italy/Switzerland/Austria on the France and Adriatic Sea maps -- but "country" was never wired
      up as a highlightable feature kind, only as unlabelled background). Carter also asked for
      labels to show only on reveal, not on the question side: real complication, since Front and
      Back currently share one Map field, so that needs a second field (e.g. "Map Labeled") and a
      Back-template change, not just new images. Feasibility confirmed, scope is real (214 notes),
      not started this session given everything else already in flight
- [ ] Carter: Tools > Empty Cards once (ArchitectTells on 5 works, TitleTells on 2 Art notes), then Sync

## W. Session 2026-09-18 (late)
- W1 Mosaic: row widths now flush (one common width per block); narrow-width scoring so phones get 2x2 grids, not a row of thumbnails. Deployed to 26 templates via `deploy_mosaic.py` (`py`, not `python`).
- W2 International Style: Oxford comma; Equitable Building caption now "Equitable Building, Atlanta".
- W3 Geography country maps: new field `Map Labeled` (206 of 214 country notes; skipped England/Scotland/Wales/N. Ireland, Abkhazia, South Ossetia, Transnistria, Akrotiri). Reveal-only, back of MAP to NAME; front unchanged. Built by `ne_country.py`, applied by `ne_country_apply.py`. Russia framed on west/centre only.
- W4 Geography Info: dropped "officially the <long form>" clauses from the opening sentence (212 notes); kept renamings, non-English forms, "also/formerly known as". Backup: `%LOCALAPPDATA%\QB_field_backups\geo_info_before_official_names_2026-09-18.json`.
- Still not logged here: description cards/performance clues, Surrealism swap, caption-artist sweep, hero layout, Vietnam/Taipei changes, backups/OneDrive incident.
- W5 Labeled reveal maps ("Map Labeled") now on 529 Geography notes: countries, states/subdivisions, dependencies, overseas regions, SARs, Svalbard, and 54 historical polities (aourednik/historical-basemaps snapshots, captioned "Borders c. YEAR (approximate)"). Each is drawn at its plain map's aspect ratio; small islands widen until >=3 neighbours are named. Back of MAP to NAME shows both maps in one row; capital cards show the labeled map only. Tools: ne_country.py, ne_region.py, ne_historical.py, apply_map_labeled.py.
- W6 Reveal now scrolls to the answer (qb-scroll-answer, 25 back templates), not the foot of the card. Checked in a 720px window on 8 templates; answer landed in view on all.
- W7 Deserts with only a dot (Arabian, Mojave, Death Valley, Patagonian, Great Basin) redrawn (Mojave/Death Valley outlines are approximate). ~21 other notes still use a marker-on-country "geofeat" map (lakes, seas, straits, Sinai...) -- same mechanism, not yet redone.
- W8 Geography: flags larger; 25 area/size bullets dropped from country Info (backups in QB_field_backups); Region on countries now sub-regional.
- W9 Map fixes: borders in my renders thickened (were faint when shown small); back maps sit in equal boxes with no plate/border, paper ground, capped at 52vh; plate-to-map gap on capital cards. Spain/Italy/France subdivisions drawn at the deck's level (communities/regions). Modern-state historical notes (Bavaria, Saxony, Tuscany, Lombardy, Latium, Peloponnese, Sindh, Punjab, Galicia) now get modern labeled maps.
- W10 Question-side maps replaced where the Wikipedia image was unusable: Attica, Republic of Texas, Phoenicia, Australian Antarctic Territory (new polar map, ne_antarctic.py), and 8 historical polities (Nazi Germany, Ottoman Empire, Venice, HRE, Byzantine, Savoy, Portugal, Genoa). Originals backed up (geo_maps_before_fronts_2026-09-18.json). NOT replaced (dataset polygon too crude): Kingdom of Poland, Swabia, Pomerania; Pingyuan Province, Polynesia, Franconia, Deccan, Khorasan, Livonia/Bessarabia/Thrace dots still have the old map.
- W11 New field Seat (capital of a subdivision/dependency), 236 notes, shown beside IN on backs; no new cards generated.
- Still old-style (thin lines): the ~420 geone maps (rivers, lakes, seas...) -- re-render + ne_apply if wanted.
- W12 Map Labeled now on every Geography note that lacks an NE-labelled map, except: Spanish Empire (too scattered), Xikang, Daman and Diu, Württemberg-Baden, South Baden, Württemberg-Hohenzollern, Christmas Island, Cocos (Keeling) Islands (no boundary data). New scripts: ne_more.py (UK nations, France's old regions, country-set regions, EU, continents), ne_more2.py (historical regions on modern borders, hand-outlined waters, oceans), ne_antarctic.py (AAT, Vinson, Vostok, Antarctica), ne_fronts.py. Many outlines are hand-drawn/approximate and captioned as such.
- W13 Geography fixes: capital-plate qualifier spacing ("While Porto-Novo..."); shapely installed for clean merged-region outlines.
- W14 Maps: 13 bad historical/region front maps replaced (Poland, Swabia, Pomerania, Pingyuan, Franconia, Deccan, Khorasan, Livonia, Bessarabia, Thrace, Silesia, Normandy, Moldavia) + Polynesia; labeled maps for Swabia/Pomerania/Thrace/Poland. All ~420 NE-rendered river/lake/sea/range/desert/peninsula/island maps and 156 city/peak/waterfall maps re-rendered with thicker lines (geo_map_before_thick_lines backup).
- W15 CM audio: Commons + IA rescanned for the 61 pre-1900 works still silent; no verifiable match (the one candidate, a C.P.E. Bach flute concerto, is Wq. 169 in G, not the deck's Wq. 168 in A). New tool cm_audio_inbox.py: drop recordings into C:\QB\audio_inbox, run it, it attaches and clips them.
- W16 Architecture: "[unknown]"/"[not applicable]" architect rows hidden on backs; 26 bloated/scarce descriptions and notes rewritten (arch_before_trim backup); Geography: 2 scarce Info fixed (Denmark Strait, Tuscany). No Geography note was >900 chars or empty.
- W17 Verification: Geography (light + night, phone), PA, Photography, Architecture rendered at 390px; layouts held. Not checked on a physical phone.
- W18 Oxford comma: 64 notes (Geography Parent/Now lists, Architecture, etc.) fixed conservatively (oxford_before backup).
- W19 Region: 347 non-country notes (cities, rivers, lakes, seas, islands, peaks, dependencies...) now sub-regional (geo_region_nonCountry_before backup); mixed-country features keep the continent.
- Art "Subject" lines for mythology/Bible works: DROPPED by Carter 2026-09-20 (no longer pending). Architect "work/name -> details" card: also dropped.
- W20 Outlines tightened from real sources: Bessarabia (Prut/Dniester courses), Franconia (OSM Oberfranken+Mittelfranken+Unterfranken), Sinai, Bering Strait, Hormuz, Easter Island, Lake Matano, Death Valley (OSM). Dalmatia uses Croatian counties. Still approximate/hand-drawn: Republic of Texas, Phoenicia, Pingyuan, Celtic Sea, Alaska/BC coastal waters, Gulf of Boni, Strait of Dover, South Ossetia, Mojave (OSM returned only a small fragment), Apennines.
- W21 Architects: 5 "[unknown]" filled (Pisa, Djenné, Golden Temple, Great Pyramid, Dome of the Rock). PA Raymonda/Les Noces notes rewritten. text_audit/ folder + Copilot prompt for text problems (report: text_audit_report.txt).
- W22 CM audio wide search: IA + Commons scan of all 163 silent works, verified by track list; cm_audio_wide.py attached 26 clips (commercial IA-hosted recordings; private-study use only, do not share the deck). 137 remain silent. Text audit: only &nbsp; fixed (9 notes).
- W23 Persia/Gaul/Ruthenia/Latium: missing front maps added. Reveal: duplicate plain map hidden when it is our own geofront/geone render; scroll no longer passes the first image.
- W24 Media gaps: PA Michael Bennett image added (small); Follies/Rodeo/Cafe Muller/Green Table/MacMillan R&J/Alice have no free image; Art Cain in the US, Girl with a Goat, Arbor Day, Relation in Time, Dropping a Han Dynasty Urn: none found (copyrighted).
- W25 CM audio: +7 symphonies (Shostakovich 5/10, Sibelius 2/5, Prokofiev 1, Gorecki 3, Lutoslawski 4) via cm_audio_wide.py --generic. Art: 29 more description-guess clues (batch2 in art_clues.json), DESCRIPTION to TITLE cards unsuspended.
- W26 (2026-09-20 review, USER_FEEDBACK_2026-09-20.md): Architecture Works -> semicolon lists with flagship underlined; Style cards gated by new StyleCard field (102 suspended); foreign-term italics, bold removed, 6 text fixes; "More" button on backs. Geography Borders now geometry-derived clockwise, Waters from geometry, US census-division regions, island/peninsula Region map. Flag back shows map, no details. Renderer: labelled provinces/islands/rivers, tinted river countries, per-group rings, optional inset. All CSS/HTML comments stripped from all 8 note types (models_before_cleanup_2026-09-20.json); spot-render of Architecture/Art/Photography/Geography unchanged.
- W26 pending: apply renders F_geone/F_pts/F_reg (and labelled reruns); Architecture Figure images (_fig_apply.py, check apply_report.json); ~45 element notes + geology notes; South Ossetia; Copilot fact_audit_report.txt review; CM audio retries (Mazeppa, Walton Facade).
- W27 (2026-09-20): Applied Geography map renders: F_geone/F_pts (question maps, 421 files), Map Labeled on 900 notes (F_reg, F_geolab, F_ptslab, F_cty). Province-name clutter ("Prefecture", "Voivodeship", long names) now cleaned in ne_render.py (only affects future renders; F_geone/F_pts still carry old labels). Architecture Figure images verified (Palladio, Wren, Le Corbusier = portrait + 2 works, same as Gehry).
- W27 Architecture: 32 new Element notes with 2-3 images and captions each (arcade, buttress, dome, arch, column, capital, pier, nave, aisle, choir, spire, parapet, balustrade, plinth, obelisk, pagoda, rotunda, lantern, gable, dormer, pilotis, keep, barbican, niche, chevet, westwork, onion dome, gopuram, madrasa, triumphal arch, impluvium, mashrabiya). Portico/colonnade/architrave/triglyph/metope/baldachin already existed. Stupa and Ziggurat already exist as Building type notes.
- W27 Geography: new note type "Geology" (clone of Architecture element design, one DEFINITION to NAME card) with 58 landform notes (endorheic basin, cirque, caldera, glacier, rift lake ... continental shelf), 1-3 images and captions each, in deck Geography, tag Geo::kind::landform. Seamount, Stalactite, Stalagmite, Geyser, Butte, Sill, Atoll, Barrier island, Sea stack, Continental shelf have only 1-2 images (few free photos).
- W28 Copilot fact audit (625 claims, 15 flagged): 12 Geography "Seat WRONG" flags were false positives (Xikang, Daman and Diu, Alsace, Upper/Lower Normandy, Auvergne, Champagne-Ardenne, Languedoc-Roussillon, Midi-Pyrenees, Wurttemberg-Baden, South Baden, Wurttemberg-Hohenzollern are former units; the seat is their historical seat and each Info says they are former). Liverpool Cathedral "largest cathedral in Britain" is correct per Wikipedia (kept). Fixed: Faisal Mosque capacity (hall ~10,000; ~300,000 with grounds); Borobudur note that Gunadharma is known only from folk tradition (fact_audit_before backup).
- W29 (2026-09-20): F_geone/F_pts re-rendered with cleaned province labels and applied (G_geone, G_pts). CM audio: deno + ffmpeg installed; cm_audio_yt.py now uses py -3.14 yt-dlp with deno/ffmpeg on PATH; Judith Weir Blond Eckbert attached. Prokofiev Fiery Angel and Andriessen Rosa candidates are age-gated (need cookies; not used). 5 silent works have no YouTube match. South Ossetia now OSM outline, label fitted, Kind "partially recognised state" (also Abkhazia, Transnistria, Somaliland, N. Cyprus, Kosovo).
- W30 (2026-09-20) Final pass on USER_FEEDBACK_2026-09-20.md: Oxford comma restored on 22 Geography country lists (Parent) that had 3 items without the serial comma (oxford_geo_before backup); Balkan/Anatolian Waters fixed (no redundant Mediterranean/Sea of Crete, Sea of Marmara added); Architecture secondary Style names unified (Postmodernism, Modernism, Neoclassical, Deconstructivism, International Style; arch_style_names_before backup); Brancusi The Kiss photo cropped (original in QB_field_backups); Baikonur circle now always labelled; labelled maps re-rendered with cleaned labels (H_geolab/H_ptslab/H_cty/H_reg, 897 notes). Checked OK: bullets end without periods (0 exceptions), Gurdwara/Sight and Hearing italics, Pantheon/Angkor/Sullivan text, Bauhaus images, Haryana/Delhi, Vesuvius/Campania, Wallis two rings, Tripura grey Bangladesh, State of Mexico.
- W30 images: third image added to 45 more element/landform cards (Geology 13 + Seamount, Architecture 32). Still 2 images: Horst, Continental shelf, Pier, Tuscan order, Volute (Seamount 2). Parapet's second/third are weak.
- W30 CM audio: YouTube cookies needed for the age-gated Fiery Angel and Rosa; Chrome/Edge hold the cookie DB locked while running (close the browser, or export cookies.txt).
- W31 (2026-09-20): Label overkill fixed in ne_render.py (backup ne_render_backup_2026-09-20b.py): countries always named; provinces only where they touch the feature (max 6); seas/lakes/rivers/islands only if near the feature (seas 5, islands 4, lakes 2, rivers 2). All labelled maps re-rendered and applied (I_geolab, I_ptslab, I_cty, I_reg). CM audio: Fiery Angel and Rosa attached via exported YouTube cookies (cookies file deleted).
- W32 (2026-09-20): Question-side maps no longer carry province names (ADMIN1_LABELS now only with --labeled in ne_render.py/ne_points.py); J_geone/J_pts re-rendered and applied (421 files). Black Sea, Lake Albert, Bordeaux checked.
- W33 (2026-09-20): CM audio: last 4 silent works attached from YouTube (Webern Symphony Op. 21 - Berlin Philharmonic; Salieri Tarare overture - Les Talens Lyriques; Sallinen The Red Line choir scene - Finnish National Opera; Leonin Viderunt omnes - Roberto Pintos Cadillac upload, unverified performer). Micrologus is a treatise: no audio. Cleared superseded render folders (F_, G_, H_, candidate-image dirs, scratch sheets): renders 3.0 GB -> 1.7 GB. Field backups kept.
- W34 (2026-09-20) Integrity check found 41 Classical Music notes whose Audio file was missing from collection.media (files existed at audio_inventory 2026-09-04; not found in any backup/cache; cause unknown, likely an earlier cleanup). Re-sourced 39 from YouTube (cmc- clips) + 3 concept notes mapped to main-note clips; new Mozart K.545 clip. Duplicates that would now play the same clip suspended (notes 1787711405292, ...308, ...320, ...374). Backup of the old references: cm_missing_audio_before_2026-09-20.json. Media references now all resolve (0 missing of ~12,100).
- W35 (2026-09-20): Oxford comma for 3-item lists ("A, B and C" -> "A, B, and C") in Info/Notes/Description/Now/Nickname/Parent etc.: 37 notes (oxford3_before backup); excluded compounds (Bosnia and Herzegovina, Antigua and Barbuda), titles in quotes/italics, place-name appositives. Geology process line "Solutional" -> "Dissolution". Shield volcano first image replaced (Mauna Loa from space). fact_audit2/ holds COPILOT_PROMPT.txt + facts_to_check2.jsonl (522 claims: 58 Geology + 32 new Architecture element notes) for the next Copilot accuracy check.
- W36 (2026-09-20) Inconsistency scan (typography, empty fields, duplicates, near-duplicate values, cross-field checks, image reuse, borders symmetry, typo candidates). Fixed 65 notes' stray spaces/doubled punctuation/CM date hyphen/medium case (scan_typo_fixes_before backup), Art movement case (Pop Art, Conceptual Art), Bo Bardi "Glass House (São Paulo)". Found, not changed: mixed British/American spelling (British majority in Architecture/Art/Geography/Performing Arts/CM/Photography, American majority in Cloze+); 83 Architecture pictures with no caption (by design after generic captions were removed); 26 CM notes with no Date (Schubert masses, Haydn quartets, etc.); Art "The Card Players", "Portrait of Henry VIII" and "LOVE" have two notes each (different versions/pieces).
- W37 (2026-09-20): CM Dates added to 16 notes (Schubert Der Strom c. 1817, Mass in B-flat 1815 x5, Piano Trio No. 2 1827 x2; Liszt Angelus 1877; Scriabin Op. 63 poems 1912 x2; Mendelssohn String Sinfonia 9 1823; Mozart Serenade K. 375 1781 x3; String Quintet K. 614 1791) (cm_dates_before backup). Left blank, need decisions: Schubert Piano Sonata in A minor and Tantum Ergo (which work?), Chopin Etude in C minor / Mazurka in D minor / Nocturne in E-flat minor (audio files named CM/DM/EbM; Chopin wrote no E-flat minor nocturne or D minor mazurka, so the Work names look wrong), Haydn Concerto for Two Horns Hob. VIId:2 (that concerto is lost; the audio is probably VIId:5), Haydn Flute Trio 15, Notturno 1, String Quartets Op. 3 (now attributed to Hoffstetter) and Op. 5. LOVE notes: sculpture note now sculpture only (Date 1970, Style Pop Art; Cor-Ten steel, Philadelphia photo); print note (1967 screenprint) stays; 'duplicate' tag removed.
- W38 (2026-09-20) Carter's map/template batch: Apurimac (3rd arm of Amazon-Ucayali-Apurimac) was missing from Natural Earth entirely -- fetched from OpenStreetMap (relation 251092) and spliced into the river's feature set, now drawn and labelled. Flag reveal (FLAG to NAME Back) no longer shows the place photo, only the maps. GREY (locator-map "other land") darkened #dedede -> #c7c7c0 for contrast against SEA. Berlin now redrawn on top of a highlighted Brandenburg (and Bremen on top of Lower Saxony) instead of being painted over -- general "enclosed" dict in ne_render.py. Info bullets that only restated the Borders field as prose ("X borders Y to the north...") removed from 20 country notes where a Borders field already existed and the bullet added no other fact (geo_info_borders_redundant_before backup); left alone where the bullet also carried a real fact (Liechtenstein, Greenland, etc.). Bare directional admin-1 names (Sudan/Ghana/Sierra Leone/Zambia/Rwanda/Fiji "Northern") now qualified ("Northern State", "Northern Region", ...) instead of showing bare on labelled maps. India subdivision Map field: Jammu and Kashmir, Chandigarh, Puducherry and Andaman and Nicobar Islands were on a different-styled/low-quality source (orange disputed-territory shading or a whole-India dot too small to see); replaced with the same "in India (claimed and disputed hatched)" family used by the other 33 Indian states (india_maps_before backup). Full labelled-map + US-state/subdivision re-render in progress to pick up the GREY/enclosure/bare-name fixes everywhere (K_geolab/K_ptslab/K_cty/K_reg).
- W38 CM audio identification (chroma/DTW match against YouTube candidates): Chopin "Etude in CM" = Op. 10 No. 1 in C major; "Mazurka in DM" = Op. 33 No. 2 in D major; "Nocturne in EbM" = Op. 9 No. 2 in E-flat major (the DM/CM/EbM suffixes were major-key shorthand, not minor as the old Work names said). Schubert "Piano Sonata in A minor" = No. 4, D. 537 (1817). "Tantum Ergo" = D. 739 (1822, not 1815 as first guessed -- corrected). Haydn "Str. Q. Op.3, 5" = Op. 3 No. 5 (the "Serenade" quartet, Hob. III:17), now attributed to Romanus Hoffstetter, not Haydn -- Carter should decide whether to keep it under Haydn's name or relabel. Unresolved: "Concert for 2 Horns in Eb" -- audio scores are statistically tied between Haydn Hob. VIId:5 and Rosetti's Concerto for 2 Horns; "Op. 5" string quartet does not exist in any Haydn catalogue (the numbering jumps Op.1, Op.2, Op.3-spurious, then Op.9) -- needs Carter's source or a straight listen; Flute Trio No. 15 and Notturno No. 1 (Hob. IV:15, II:25) could not be dated or verified against Wikipedia. cm_id_before backup holds the old Work/Key/Date values for the six fixed notes.
- W39 (2026-09-21): US state (50) and Indian subdivision (36) question-side Map now drawn by my renderer in the Germany/Mexico style (ne_usfront.py: whole country in view, target red, other states cream with borders, Canada/Mexico/neighbours grey #c7c7c0, sea light blue, no labels, ring on tiny targets; renderer got VIEW_BOX and NO_LABELS globals). Replaced Wikipedia locator images (us_state_maps_before backup holds the old Map fields; the India batch overwrote the same backup key file name, old India Map values are in india_maps_before). Daman and Diu has no Natural Earth polygon and keeps its previous map.
- W40 (2026-09-21) Haydn: Op. 3 No. 5 -> Romanus Hoffstetter (1742-1815), c. 1770, nickname Serenade Quartet; the "Op. 5, 2" clip matched Haydn Op. 55 No. 2 "Razor" (F minor, Hob. III:61, 1788) by audio fingerprint (Work/Catalogue/Nickname/Key/Date fixed); Concerto for Two Horns -> Hob. VIId:5, 1784 (attribution to Haydn itself doubtful); Notturno No. 1 -> Hob. II:25, 1790; Flute Trio 15 still undated (could not verify). Carter: notes must not be bloated with alternate names and statistics. Geography Info: alternate-name clauses removed from lead sentences ("X, also known as Y, is ..." -> "X is ...", 107 edits), naming-only bullets and demographic/size-statistic bullets deleted (56 bullets; lead sentences never deleted; geo_info_bloat_before backup). Other decks scanned: no comparable bloat. wd_audit.py (Wikidata fact audit tool) started.
- W41 (2026-09-21) Overnight audit (Carter: "find and correct all errors, inconsistencies, shortcomings"; Copilot found nothing). Independent method: deck values vs Wikidata/Wikipedia (wd_audit.py, wp_verify.py, _verify_dates.py). Art dates corrected from Wikipedia: Watson and the Shark 1778, Sky Mirror 2001, Bonaparte Crossing the Alps 1848-1850, Magdalene with the Smoking Flame c. 1640, Seven Deadly Sins c. 1500, Ecstasy of St. Teresa 1647-1652, On the Threshold of Liberty 1929, Harvest Wagon c. 1767 (Barber version), Panciatichi Assumption c. 1522-1523 (art_dates_before backup). Canadian spelling applied to our own writing only (-ize, -our, centre, metre, tire, neighbour; quoted titles and italics left alone): 78 notes (canadian_before backup). Architecture: 78 pictures that had no caption now have one (viewed each); 4 wrong pictures replaced (Hoover Dam [3] was Horseshoe Bend, Registan [2] unidentified, US Capitol [2] was the Pennsylvania capitol, Institut du Monde Arabe [3] was a hoarding) and New Museum [3] (people at a table) removed. Still running: wp_verify.py over Art/Architecture/Performing Arts/Photography (results in wd_audit_out/wp_*.json).
- W42 (2026-09-21) wp_verify.py Wikipedia date check finished for Art (4,514 works; 2,658 matched to an article) and Architecture (292 matched): after hand triage, 3 more Art dates fixed (Cezanne Portrait of Ambroise Vollard 1899, Rogier van der Weyden Descent from the Cross c. 1435, Morning in a Pine Forest 1889; art_dates2_before backup). Architecture dates: all flags were foundation-vs-current-building differences, none wrong. Thin cards: Horst, Seamount, Continental shelf, Volute, Pier and Tuscan order each gained a third image. Performing Arts has no dated works to check by article. Photography check still running.
- W42b Photography Wikipedia date check finished: 179 works matched an article, 33 flagged, all false alarms on inspection (wrong article, e.g. Hillary Step, Family of Man); no Photography dates changed. Performing Arts and Classical Music dates are premiere/composition years and matched their composers' lives.
- W43 (2026-09-21) Art: Magritte Treachery of Images photo cropped and perspective-corrected out of its frame (original in QB_field_backups); "Vache period" now has Vache italic (Series on both Magritte notes, and the Cloze+ card). Along the River During the Qingming Festival: added the whole 5.3 m scroll, Rainbow Bridge, boats and pre-restoration detail with captions (qingming_before backup). Shared-title clue (TitleShared) is now "Location . Date" on all 324 notes that share a title (titleshared_before backup) and is shown on the reveal side of TITLE to ARTIST as well as the front. Movement cards: Period and Region/Seen-at blocks merged into one "Period and place" line ("1915-1930s . Russia") on IMAGE to MOVEMENT, MOVEMENT to FIGURES and DEFINITION to NAME; 20 movements that had no place now have one (art_movement_loc / art_templates before backups).
- W44 (2026-09-21) Architecture layout/UI: picture grids are now aligned (equal cells, images shown whole on a light matte; 2 pictures side by side, 3 = wide top + 2 below, or a tall first picture as a left column beside the other two, 4 = 2x2, odd counts get a wide first cell) on all Architecture and Geology cards (arch_grid_templates_before backup). Pictures no longer touch the More button (extra top margin), and the button is redesigned: full-width accent-tinted "Show details" bar instead of a grey pill that looked like the tier tag (Architecture CSS/templates backed up). Architect field: 48 multi-architect buildings now state each person's contribution ("Michelangelo (dome), with Donato Bramante (original plan), Carlo Maderno (nave and facade), and Gian Lorenzo Bernini (baldachin and colonnade)") (arch_architect_contrib_before backup); Saint Basil's, Ryugyong, Lloyd's, Oriental Pearl, HSBC, Bublik, Seville and Dome of the Rock left as is (roles unknown or a single firm). Buckingham Palace style Baroque -> Neoclassical (Wikidata and Wikipedia).
- W45 (2026-09-21) Architecture picture grid: the tall-first-picture layout now has the two right pictures spanning exactly the height of the left one (front and back, captions accounted for). Postmodernism style card pictures replaced with Portland Building, Vanna Venturi House, Piazza d'Italia and Guild House (postmodernism_pics_before backup). Leon Battista Alberti has no single most notable work (Sant'Andrea, Santa Maria Novella facade, Palazzo Rucellai and Tempio Malatestiano are comparable), so nothing is underlined. Term italics: a term introduced by "called / known as / termed / named / dubbed" is italicised at its first mention in Description/Notes/Nickname of concept notes (16 notes, e.g. tarn, groins, chromoluminarism, ferrotype, tunnel roof; italic_terms_before backup). Rule (Chicago Manual of Style 7.53 / APA): italicise a term once, where it is introduced or defined, never common words, never after it is defined; foreign words and titles already italic. Descriptions are left alone because the card name itself is the defined term (already the answer).
- W46 (2026-09-21) Architect field: contributions in parentheses and the connecting words are now a lighter, smaller, muted span (class arch-role) so the architects' names stand out (48 notes; CSS added to Architecture/Geology).
- W47 (2026-09-21) Architect field rule (Carter): people are separated by semicolons (no "and"), and a contribution in parentheses appears only when someone worked on one specific part (Michelangelo: dome of Saint Peter's); collaborative works (Hagia Sophia, Pisa Cathedral, Empire State, Sullivan and Adler, ...) list plain names. 48 notes re-set (arch_architect_semicolon_before backup; earlier list in arch_architect_contrib_before).
- W48 (2026-09-21) Mies van der Rohe pictures replaced (cigar-smoking snapshot, obscure Haus Lange, Barcelona Pavilion) with a clean 1934 portrait, Farnsworth House, Seagram Building and Barcelona Pavilion (mies_pics_before backup). This exposed two layout bugs that were stacking 4-picture cards in one column: an old CSS rule forcing a 4-image grid (removed from Architecture/Geology) and the qb-fig-pin script (removed). "Show details" bar spacing increased.
- W49 (2026-09-21) Captions: 69 Architecture concept/figure captions gained the city of the building shown (arch_caption_places_before); Mannerism card: painting removed, Laurentian Library vestibule added, Description no longer says "manner"/"knowing", captions state city. Transept card: two non-transept pictures replaced by Canterbury (aerial), York Minster and Notre-Dame transepts (transept_before). Rule (Carter): a work named in a concept card's Description/Notes is now shown as one of its main pictures with a caption; 18 Element/Style cards got the referenced building added first (arch_refs_pictures_before). Geography Info rewrite for quizbowl (concise, distinctive facts; alternate names, statistics and capital/border repetition dropped; introduced terms italic) started: countries Afghanistan-Gabon done (63 notes; geo_info_quizbowl_c1_before backup).
- W50 (2026-09-21) Front-side captions on Architecture concept cards: a work whose name appears in the Description now gets its caption on the front regardless of a leading "The" or possessive ("The Seagram Building", "Mies's ..."), and this now applies to every kind (Element/Style too), not just Figure. Geography quizbowl Info rewrite: countries Georgia-Mozambique done (geo_info_quizbowl_c2_before).
- W51 (2026-09-21) Removed "(pictured)" from the Fallingwater caption (Wikipedia leftover); scanned all decks' captions for pictured/shown/(left)/(right) leftovers: none others. Geography quizbowl Info: countries Myanmar-Aland done (geo_info_quizbowl_c3_before); all 207 countries now rewritten.
- W52 (2026-09-21) Major works: foreign-language work names get their English in brackets (Palazzo Rucellai (Rucellai Palace), Altes Museum (Old Museum), Casa da Música (House of Music), ...): 14 figure notes. I interpreted "if the most common name is in English, put it in brackets" as the earlier rule (foreign name first, English in brackets); tell me if you meant the reverse. Geography quizbowl Info: US states (c4) and rivers (c5) rewritten.
- W53 (2026-09-21) Buttress card: Durham tower picture (no buttresses visible) replaced by Exeter Cathedral's massive buttresses; Westwork card: duplicate second picture replaced by Speyer's west front. Geography quizbowl Info: lakes done (c6).
- W54 (2026-09-21) Gothic Revival: caption italics removed from a cathedral name (buildings, streets and memorials are never italic: fixed The Circus x2, The Cloisters, Vietnam Veterans Memorial, Temple of Concord); captions now give cities; Notes give Augustus Pugin and John Ruskin full names; Palace of Westminster added as a main picture (named in Notes). Image duplicate scan of Architecture/Geology/Art/Photography: only 4 near-duplicates (US Capitol, Triforium, Hermitage Museum, Atmospheric perspective) still to resolve.
- W55 (2026-09-21) Geography MAP to NAME: the "Region" hint button removed from the front (Carter: it did nothing on the Arafura Sea and the map already shows the region); PHOTO to NAME keeps its hint. Duplicate pictures removed (Triforium, Hermitage Museum, Atmospheric perspective; Capitol second picture now the Rotunda). Card-skipping-after-reveal: deck options have auto-advance off and no template navigates; add-ons installed: ImageResizer, Cloze Overlapper, Symbols As You Type, AnkiConnect, SynapsePro, extended editor -- SynapsePro is the only one that could act on the reviewer.
- W56 (2026-09-21) Geography Info rewritten as physical/human geography (no straight history, no restated Capital/Seat/Borders, full first names, no poetic phrasing) for every kind: 207 countries, 50 states, 41 rivers, 51 lakes, 91 seas/gulfs/straits/oceans, 119 cities, peaks, ranges, deserts, peninsulas, islands, waterfalls, continents, archipelagos, 216 subdivisions, historical/regional/dependency entries (scripts _geo_g1..g15, backups geo_info_quizbowl_*). Kind labels fixed: 32 gulfs/straits/lakes had been tagged "sea"; 34 places still existing were tagged "historical region"; Bengal/Caucasus/Melanesia/Punjab/Wallachia/Macedonia/Bessarabia/Prussia/Kingdom of Italy question and reveal maps redrawn to show the same extent.
- W57 (2026-09-21) Map labels (ne_render.py): English names for seas/islands/lakes/rivers (name_en, LAKE_FIX/RIVER_FIX), lakes and rivers nearest the feature are named, islands and seas try several points, no duplicate labels (Nova Scotia), microstates (San Marino, Vatican, Monaco, Liechtenstein, Andorra) drawn close with the surrounding provinces named, US and Indian small-state question maps zoomed in without the ring, front captions no longer name the answer (11 historical/regional fronts), Anki image cache means renamed copies (_b/_c/_t) for changed maps.
- W58 (2026-09-21) Sample audit across decks: Performing Arts figure alternates de-italicized (22), "The" now inside the italics for titles (The Magic Flute, ...; 11 wrongly changed restored), Photos added to 45 Geography notes that had none (peaks, deserts, islands, straits, regions, subdivisions).
- W59 (2026-09-21) All labelled reveal maps re-rendered with the improved labeller (English names, nearest lakes/rivers, no duplicates; 1,000+ images replaced, only files a note's Map Labeled uses); Spanish Empire reveal map added (Americas + Iberia, Philippines omitted); Ottoman Empire maps at c. 1530; Art nationality pairs unified birth-country-first; first mentions of people in Performing Arts/Photography/Classical Music/Architecture/Art notes given full names; PA figure spacing; Architecture Style/Notes trimmed; five Element cards given photos; Minaret pictures replaced. Changed images keep old filenames: restart Anki to clear its image cache.
- W60 (2026-09-21) Quizbowl (StockFisher Cloze+) deck exported to C:\QB\Quizbowl_export.csv (1,430 notes: Text/BackExtra/Tags, cloze markup left literal) and deleted from the collection at Carter's instruction. Deck-gap sweep across the other five: Performing Arts gained 4 images (Café Müller, Follies, MacMillan Romeo and Juliet, Rambert Dance Company -- the last matched a caption already written for an image that was never applied), two stale duplicate Photography stubs deleted (old empty Autochrome/Photogram). Ten notes stay text-only for want of a freely licensed image, nearly all contemporary and still in copyright: Photography The New First Family + The Last Resort; Architecture Sangath; Art Cain in the United States, Girl with a Goat, Arbor Day, Relation in Time, Dropping a Han Dynasty Urn; PA Rodeo, The Green Table, Alice's Adventures in Wonderland. Nothing was pulled from stock/press sites.
- W61 (2026-09-21) History deck begun (China/Japan/Korea, prehistory to present; Carter's #World Hist.pdf is the style model, full prose for China to Sui and Japan to Nara, Korea only to Gojoseon). Workflow per period: scope -> broad qbreader sweep -> narrative from sources -> targeted qbreader re-sweep per entity -> draft -> verify. hist_qb.py queries the public qbreader API (no auth) and caches; clue_profile() counts recurring quoted titles, proper nouns and accepted answerline variants, which is what decides coverage depth and the Alternate field. New "History" note type (hist_model.py), Geography's CSS with the prefix renamed, two cards: CLUE to NAME and NAME to INFO. hist_load.py tags under a single History:: parent, matching the convention every other deck uses (Art::, Architecture::, Geo::, PA::): History::country::, ::period::, ::kind::, ::cat::, ::tier::. Tier uses the same four levels as the other decks (tier1-core..tier4-rare) and is assigned from measured qbreader answerline counts, not from how important an entity feels. It also enforces house style at load (a short poem takes quotation marks, not quotes and italics both). No era:: bucket yet -- that should be set once across the whole timeline, not guessed per period.
- W62 (2026-09-21) Tang pilot: 16 notes, every Kind represented, 32 cards. The sweep's finding that shaped it -- Tang in quizbowl is a literature category first (Li Bai ~256 answerline instances, outweighing every emperor combined; History 550 vs Literature 280 by category). Wade-Giles is mandatory in Alternate, not optional: Li Po appears in 58 instances and Tu Fu in 34. Disputed stories are given with the doubt attached where packets clue them anyway (papermaking at Talas is doubted by modern scholars -- paper predates the battle in Central Asia and no Chinese or contemporary Arabic source records it; Li Bai drowning for the moon's reflection is a later story). Confusable pairs get a "Not to be confused with" field: Emperor Xuanzong vs the monk Xuanzang, Wu Zetian's Zhou vs the Zhou dynasty, Wang Wei the poet vs the Xin general. Tang extent map rendered from the historical-basemaps snapshot (hist_maps.py) at c. 800 and captioned as post-rebellion, not the height, since no usable height snapshot exists -- world_700.geojson mislabels the period as "Sui Empire".
- W63 (2026-09-21) Card design corrected after Carter: "i cant possibly recall that amount of information on one card. flashcards are supposed to be FLASH cards." He was right and the first design was wrong. Consulted SuperMemo's twenty rules (minimum information principle: a card holding several facts makes the brain take a different path each repetition, so the trace never consolidates, and the card is scheduled at the interval of its hardest part) and quizbowl practice (qbwiki/QBRC: one clue per card, because one clue is what you buzz on). The "NAME to INFO" card was the worst offender -- "What do you know?" is unbounded and cannot be graded. New note type "History Clue" (hist_model2.py): Prompt, Answer, Extra (one line, read after answering, never recalled), Entity, Image. Tang rebuilt as 79 atomic cards over the same 14 entities, answers all under 46 characters, card count per entity tracking measured qbreader frequency (Li Bai 9, An Lushan Rebellion 9, Du Fu 7, Wu Zetian 7). The dense per-entity notes are kept as the read-before-you-drill layer in History::Reference with all 32 cards suspended, so they never enter the review queue.
- W64 (2026-09-22) Audited the 79 Tang clue cards against the failure modes rather than assuming they were fine, and found six real defects. Self-containment (Carter's "singular"): "In this poem the poet toasts the moon and his own shadow" never said which poet; two prompts said "the rebellion" without naming it; the Uyghur card said "their capitals" instead of Chang'an and Luoyang. Card quality: the census card asked you to recall "about 53 million" given 17 million -- weak numeric recall that buried the actual insight, so it now asks what explains the fall (register collapse, not deaths); the two Japanese capitals card had a two-part answer with parentheticals, now just "Nara and Kyoto". Answer leakage: the Talas Extra said "Against the Abbasids", giving away a separate card's answer. Mis-tagging: Mahler's Das Lied von der Erde was filed under the Cathay entity -- both are Tang poetry reaching the West but they are unrelated works. Design fix: the front no longer shows a country/period eyebrow, since "CHINA - TANG" over a prompt narrows the answer for free once the deck spans three countries and four millennia, and a prompt needing it should say it itself. hist_sync.py reconciles source to Anki by prompt, falling back to (Entity, Answer) with closest prompt, so rewording updates in place instead of orphaning a note and losing its review history; it initially treated a matching prompt as a matching note and so missed the Mahler retag, now fixed to compare Answer and Entity too. Final: 79 cards, 15 entities, median answer 13 characters, median prompt 76.
- W65 (2026-09-22) Carter, on the stripped-down cards: "i need some kind of flair/style in my cards to effectively study them... maybe consider improving the design." Correct, and the first correction had overshot. Minimum information governs how much you must RECALL, not how bare the card looks: an image and a line of context on the BACK cost nothing at retrieval and help encoding (picture superiority, elaboration). Every card now carries its entity's image and an Extra line; one image per entity on purpose, so Liang Kai's Li Bai recurs across all nine Li Bai cards as a consistent anchor rather than decoration. Card CSS rebuilt: answer in accent serif, Extra in a tinted callout with an accent rule so it never reads as part of what you were meant to recall, framed images, quiet entity footer. Three CSS bugs found and fixed: the shared palette is defined ONLY under night-mode selectors, so every var() in day mode was invalid and the divider, callout and accent colour silently vanished (all var() calls now carry light-mode fallbacks); a mangled escape rendered the entity footer as "4NANZHAO"; and the front template was showing the entity image, which on a Nanzhao or Li Bai card simply hands over the answer -- images are back-only now.
- W66 (2026-09-22) Carter: "i fear that you didnt include all of the stock... i identified nanzhao and the pear academy... is it that you overlooked them, decided they werent important enough, or was i inappropriate to have included them?" Pear Academy was already covered, under its commoner English name Pear Garden (liyuan); both names are now on the card. Nanzhao was a real miss, and the cause was a flaw in the sweep, not a judgement call: the sweep ranked ANSWERLINES, so it is structurally blind to entities that only ever appear inside other questions' clues. Nanzhao is the answer to nothing in the database but appears in seven question texts, mostly Burmese and Mongol questions rather than Tang ones. Re-swept by scanning the text of all 871 Tang-mentioning questions for proper nouns and diffing against coverage, which surfaced Nanzhao, Li Linfu, Zhang Xun, the Grand Canal, Tang-Tibetan relations (Princess Wencheng; Tibet took Chang'an in 763) and the Korean wars (Baekje 660, Baekgang 663, Goguryeo 668, the Silla-Tang war). 14 cards added. Checking Nanzhao against sources also caught an error I was about to write: it repeatedly attacked Chengdu but never took it. Scope correction in the same pass: Pound's Cathay, Fenollosa, Eliot's phrase and Mahler's Das Lied von der Erde were cut -- Western reception is not Chinese history, and Das Lied is already a note in the Classical Music deck. A reception fact earns a place only on the Chinese entity it helps identify, which is why Pound's "Rihaku" stays as a Li Bai card. 88 cards, 18 entities.
- W67 (2026-09-22) Maps verified rather than assumed. One was plainly wrong: the Tang-and-Korea cards were showing the Tang extent map, which says nothing about Baekje or Goguryeo -- they now carry a Korean Three Kingdoms map, and the English-labelled version of it (Goguryeo, Baekje, Silla, Gaya, Wa) rather than the Korean/Chinese-labelled one. Checked a Commons "greatest extent" Tang map as a replacement for my rendered c.800 one and kept mine: it is post-rebellion, but it names the Tibetan Empire, the Uyghurs and the Abbasid Caliphate, which are entities on other cards, and an unlabelled extent blob teaches nothing. Every other assignment holds (Talas 751 theatre map, An Lushan campaign map, Chang'an ward plan, Yan Liben's Bunian tu for Tang-Tibet, the Three Pagodas of Dali for Nanzhao). Click-to-expand added: the same qb-zoom script the Art and Geography decks use, on the back only, with cursor zoom-in on the plates.
- W68 (2026-09-22) Card styling brought into the house family (hist_style.py). The cards had been sitting on stark white because they inherited Geography's sheet, whose palette exists only under the night-mode selectors -- in day mode every var() was undefined and those rules collapsed. The Art deck defines both palettes, which is where its warm ground comes from. History now states both, in the same family (paper #f7f3ea, ink #2b2b2b, brown accent #6b4c3b, night #1b1a18/#d2ab8f): answer in accent serif, prompt demoted to a caption on the reveal, hairline rule, Extra set off by a left border, pictures mounted on a plate with a hairline and soft shadow as the Art deck mounts artworks, entity as a quiet pill like the Art tier chips. Replacing the inherited sheet also dropped the base font stack, centring and the eyebrow rule, which had to be restated -- caught by rendering, not by reading the CSS.
- W69 (2026-09-22) Pre-Tang China written: 142 cards over 13 periods, legend through Sui, from Carter's notes checked against qbreader sweeps and sources. The sweep's shape for pre-Tang is philosophy the way Tang's was literature -- Confucius alone about 169 answerline instances, Legalism 60, Analects 43, Mencius 44, Mohism 27, more than the political history of the period combined -- so the Hundred Schools got the depth the poets got. Corrections to his notes, which he asked me not to treat as gospel: HEZONG is the vertical north-south alliance AGAINST Qin (Su Qin) and LIANHENG the horizontal alliance WITH Qin (Zhang Yi) -- his notes swap both the labels and the descriptions; Li Si was not Qin Er Shi's father (Huhai was Qin Shi Huang's own son); the Houmuwu ding is 832.84 kg with a real naming dispute (si vs its mirror hou, settled by the museum only in 2011). The burning of books and burying of scholars, the Xia's historicity and the Erlitou identification are all given as contested rather than as facts.
- W70 (2026-09-22) Applied the clue-text scan to pre-Tang, which I had fixed after the Nanzhao miss and then failed to run on the new batch -- the same methodological hole, repeated. Scanning 2,305 pre-Tang question texts and diffing against coverage surfaced the Five Classics (55 mentions), Vietnam and the Trung sisters (over 50), the Oath of the Peach Garden (28), the Battle of Mingtiao (21), Zisi (17) and Gongsun Long (17). Mingtiao and the Trung sisters are in Carter's own notes and had simply been skipped. 10 cards added. Lesson worth keeping: fixing a method is not the same as applying it, and the answerline sweep must always be followed by the text scan before a period is called done.
- W71 (2026-09-22) Density fix for Qin, Han and Confucius (hist_china_depth.py): normalised against clue frequency the Han had 0.41 cards per 10 answerline instances against the Tang's 0.77, and Spring and Autumn (Confucius) 0.35. clue_profile() turned up Jing Ke, Gao Jianli, Lü Buwei, Lao Ai and the Twelve Metal Colossi -- all in Carter's notes and all skipped -- plus the Four Books, Silver Rule, Five Relationships. Carter then set the rule for pre-Tang: strictly his notes. Asked about the one real consequence (his notes give the Hundred Schools one line, qbreader ranks Confucius the most-clued pre-Tang entity at ~169), he chose to keep the philosophy cluster as the single exception. The two genuinely stray cards were cut: the Oath of the Peach Garden and the Qin cart-axle standard. 257 cards (Tang 88, pre-Tang 169).
- W72 (2026-09-22) Early Japan (to Nara) and Korea (to Gojoseon): 74 cards, strictly from Carter's notes, verified. Clue-text scan run BEFORE writing this time (Kojiki 98 text mentions, Nihon Shoki 69, Dangun 57, Amaterasu 57); it also shows Izanagi and Izanami, which the notes do not cover and which were left out under the notes-only rule. Corrections to the notes: Jeulmun means "comb-patterned", not "cord-patterned" (cord-marked is Jomon; "Pit-Comb Ware" is Jeulmun, and Yunggimun is the earlier raised-design pottery); Emperor Shomu reigned 724-749, not 724-729; Jomon pottery was named by Edward S. Morse, not Edward R.; Izumo Taisha is in the Chugoku region, not "Chigoku". hist_sync now scopes by (country, period), since China, Japan and Korea each have a Prehistory; tags are folded to ASCII (period::jomon, not period::jōmon) for tag search.
- W73 (2026-09-22) Image rule fixed across all 331 history cards (hist_imgmap.py). The one-image-per-entity rule works for a person (Li Bai's portrait on every Li Bai card) but on a period grab-bag it pinned the wrong picture to most cards: 132 cards showed a portrait or object of something other than their answer -- Cao Cao's portrait on the Jin cards and on Liu Bei's, Qin's terracotta army on Warring States cards, Laozi on Mencius, Hōryū-ji on the Asuka-dera card, a dolmen on pottery cards. Now a portrait or specific object goes only on cards about that subject; grab-bag entities carry a period map or a site (Spring and Autumn, Warring States, Qin, Three Kingdoms, Jin, Sui and Gojoseon maps fetched), or the card gets its own picture (about 45 portraits and objects fetched), or none. Rechecked in Anki afterwards: 0 mismatches, 306 of 331 cards with an image.

## W74 — Classical Music movement markings (2026-09-22)
- 368 of 383 bare "mvt. N" notes now read "mvt. N · marking" (e.g. "mvt. II · Largo"). Source: IMSLP movement lists, accepted only when composer + catalogue match; 80 set by hand (programmatic works in English: Pastoral, Scheherazade, Harold; well-known works IMSLP didn't match). Script: stockfisher/cm_movements.py (fetch / replan / report / apply). Backup: QB_field_backups/cm_movement_before.json.
- Data fixes: Schubert SQ13 "Rosamunde" D. 797/1823 -> D. 804/1824; generic titles resolved: Schubert Piano Trio -> No. 2 D. 929; Mozart Serenade (E-flat, 1781) -> No. 11 K. 375; Mozart String Quintet (1791) -> No. 6 K. 614, E-flat.
- Left bare (15): Haydn quartet sets with no number (Op. 20/33/50/64/76), Haydn two-horn concerto, flute trio, notturno; Mendelssohn string sinfonias; Boulez Marteau. Suspect movement numbers: Beethoven Cello Sonata 3 "mvt. IV" and Quintet Op. 16 "mvt. V" (both are 3-movement works).

## W75 — History reference doc (2026-09-22)
- Downloads/#World Hist.docx is corrupt (binary passed through a text conversion: 3.6M U+FFFD bytes); the .rtf is intact. Word converted the RTF to stockfisher/_worldhist_src.docx.
- hist_refdoc.py writes era notes in Carter's format into Downloads/#World Hist - reference.docx (originals untouched). Tang: his 15 fragments -> 70 notes in 8 sub-sections, every fragment kept; corrected Xuanzong->Xuanzang (monk), Faxian dated to Eastern Jin, Huang Chao under Xizong. Add future eras to ERAS.
- Japan (to Nara) and Korea (to Gojoseon) already written by Carter; nothing added there.

## W76 — Tag cleanup (2026-09-22)
- History night mode: html kept the day palette on phones (night class sits on <body>) -> dark box on the front, light border on the back. hist_style.PALETTE now carries the html:has(> body.night_mode) rule the other decks use.
- Removed the flat audit-marker tags (blank-front 4, architect-unknown 80, capital-in-name 2, duplicate 86, picture-prints-title 3, picture-prints-answer 1, duplicate-of::… 1). Their note lists are in QB_field_backups/tag_markers_removed.json. NOTE: cm_normalize.py, cm_work_italics.py, geo_duplicate_delete.py test the "duplicate" tag -- read that file instead if they are ever re-run.
- Every remaining tag sits under a deck root: Architecture, Art, Geo, History, Music, PA, Photo.
- Media: 14 field references with the wrong filename case fixed (worked on Windows only; 3 on active Architecture cards: Palais Garnier, Moscow Kremlin, Art Nouveau). 387 unreferenced files (189 MB) deleted incl. 50 "_" files Anki never cleans (old BBC/recipe images, unused fonts); copies in QB_field_backups/media_removed_2026-09-22. Bronzino "Allegorical Portrait of Dante" had a mangled src -> Commons image art-Bronzino_Allegorical_Portrait_of_Dante.jpg.
- Left for Carter (AnkiConnect cannot delete note types): empty "StockFisher Cloze+" and "Cloze (overlapping)".
- History::Reference kept (Carter likes them). "History" note type restyled: hist_model.css() now appends hist_style.PALETTE + accent serif name + plated images, so the 16 reference notes match the clue cards in both modes.

## W77 — Art image fixes (2026-09-22)
- Beer Street & Gin Lane: the single combined plate split into two images (art-Hogarth-Beer_Street.jpg left, art-Hogarth-Gin_Lane.jpg right) with captions naming each; captions render on the back only, so the ARTWORK front still asks.
- Qingming scroll: qb-mosaic now honours data-solo (own row, uncropped -- the row packer clamps ratios at 2.4:1 and object-fit: cover, which mangled a 21:1 handscroll) and data-row="N" (pins which images share a row). Patched into all 17 template sides that carry the script (Art, Performing Arts, Photography); backup QB_field_backups/mosaic_templates_before.json. Note now: scroll on row 1, four details on row 2.
- Bauhaus: images 1-2 both spelled BAUHAUS (answer leak on IMAGE to MOVEMENT). Now Dessau workshop wing cropped clear of Bayer's lettering, Breuer's Wassily Chair, Schlemmer's Triadic Ballet costumes, Gropius portrait.
- Post-Impressionism: the 1889 Volpini poster ("GROUPE IMPRESSIONNISTE ET SYNTHETISTE") replaced with Seurat's Grande Jatte.
- Field backup: QB_field_backups/art_image_fixes_before.json.

## W78 — Art/Architecture fixes and a Geography map audit (2026-09-22)
- Art: Gaudí picture 3 (a family snapshot) -> Sagrada Família; Bernini pictures 2-3 (bust of Paul V, Aeneas group) -> St Peter's Square colonnade and Sant'Andrea al Quirinale; "navis" italicised on the Nave card.
- Oxford comma sweep (oxford_comma.py): 261 fields across all decks. Rules: only the last two items are judged; italics, title fields and media fields skipped; protected names (Trinidad and Tobago, São Tomé and Príncipe...) masked so they count as one item; adjective pairs, participles and appositives left alone. Backup: QB_field_backups/oxford_comma_before.json.
- ne_render.py: historical maps now draw rivers (NO_DETAIL suppressed them while the label pass still named them -- Assyria was captioned "Firat"/"Euphrates" over blank land); canals and delta branches unlabelled on historical maps; Firat->Euphrates, Dicle->Tigris; each sea named once (Atlantic appeared twice on Gulf of Guinea); small countries in plain sight labelled (Togo); "Mainland X" labels dropped; HAND_LABELS for Bass Strait (King I., Flinders I.).
- ne_fronts.py: the "modern region" maps never set OTHER_GREY, so Poland and the Czech Republic read as German states on the Saxony map. Fixed and all nine re-rendered (Bavaria, Saxony, Tuscany, Lombardy, Latium, Peloponnese, Sindh, Punjab, Galicia). Berlin now labelled (small sister regions get a 15px label).
- ne_region.py: added --redact so subdivisions can have a question-side map; Bremen's front map was a Wikipedia locator of red blobs on white -> rendered map.
- Assyria: map caption now "Assyria at its height under the Neo-Assyrian Empire, c. 670 BCE"; Info says Assyria ran 2025-609 BCE in three phases. Saxony: Capital Dresden added.
- Caribbean and Mediterranean border lists (28 and 23 entries) replaced with regional summaries; the other ten water bodies (<= 11) keep explicit lists.

## W79 — Geography map re-render finished; two rendering bugs found from live review (2026-09-22)
- Finished the scraped-front sweep from W78: 598 -> ~4 still scraped (Cocos Islands and 3 obscure Antarctic-adjacent territories with no capital, unrelated to maps). ne_more.py and ne_more2.py already had most of the hard cases built (UK's four nations, France's pre-2016 regions, Maghreb/Levant/Fertile Crescent/Melanesia/Micronesia/Mesoamerica/EU as country-sets, the continents, Sinai/Hormuz/Bering Strait/Dalmatia/Lake Matano/Easter Island from OSM) but the ocean loop never rendered a front at all (see below) and most others had never been run to completion; ne_fronts.py's "modern region" companion maps (Bavaria/Saxony/Tuscany/Lombardy/Latium/Peloponnese/Sindh/Punjab/Galicia) also lacked a redacted front. Added: Antarctica continent (no CONT entry existed; drawn whole-world style like the oceans, since a rectangular frame can't crop tightly to a pole-centred landmass), Lake Vostok (entirely subglacial, hand-drawn extent, Parent set to Antarctica which no note had used before), Vinson Massif (Parent likewise), the three West German occupation-zone states (Württemberg-Baden/South Baden/Württemberg-Hohenzollern, no Natural Earth polygon -- drawn from the Baden-Württemberg Regierungsbezirke by OpenStreetMap), Christmas Island (OSM). Cocos (Keeling) Islands has no OSM administrative relation found under several name variants; Xikang, Daman and Diu remain (former subdivisions with no matching modern polygon).
- Also fixed while at it: Transnistria and Abkhazia had real Natural Earth admin-1 polygons all along (filed as Georgia's/Moldova's own province) despite the front never being drawn; "partially recognised state" was missing from geo_rerender.py's ROUTE and ne_region.py's KINDS entirely, so Kosovo/N. Cyprus/Somaliland/Abkhazia/Transnistria had never even been attempted. South Ossetia has no Natural Earth match (Georgia doesn't administratively split it out) and keeps its existing OSM-outline map. 27 front/reveal mismatches (different render passes/cache-busted filenames -- Andorra/Liechtenstein/Monaco/San Marino/Vatican City, Kingdom of Prussia, Kingdom of Italy, Assyria, Republic of Texas, Kingdom of Poland, Gaul, Galicia, Thrace, Pomerania, Bessarabia, Ruthenia, Macedonia, Phoenicia, Sindh, Bavaria, Saxony, Swabia, Franconia, Tuscany, Lombardy, Latium, Pingyuan Province) re-rendered both sides from the same call so they now agree exactly.
- Carter's live-review pass (viewing applied cards) surfaced two real rendering bugs, both now fixed and applied across every Geography front (country + subdivision-family: 203 + 286 notes; region/historical/feature family: 62 + 50 notes; all re-uploaded to their existing filenames, so Anki's image cache needs a restart to show them):
  1. **Lake label leak**: the reveal-side labeller was allowed to place a big lake's name directly over the highlighted target (`over_target=True`, ne_render.py) so a lake distinctive enough to place the answer -- Lake Winnipeg inside Manitoba's outline -- was named on the *question* side too. `base_map()`/`render()` now take a `redact` flag (true whenever `target_label` is None) that turns this off only on the front; the reveal side is unchanged. Caught on Manitoba; the fix is in the shared renderer so it covers every kind.
  2. **Enclave misrouting**: ne_country.py drew any country with a small bounding box (< 0.6 degrees) using the "microstate surrounded by one country's provinces" path meant for Andorra/Liechtenstein/Monaco/San Marino/Vatican City -- which also caught nine actual island nations (Saint Kitts and Nevis, Nauru, Singapore, Malta, Barbados, Dominica, Saint Lucia, Grenada, Niue), drawing unlabelled foreign arrondissements/provinces next to them instead of naming the real neighbouring countries. `ENCLAVE` is now an explicit 5-name set; the nine island nations go through the normal country-neighbour-widening path and get real labelled neighbours.
- Ceram Sea's front was naming "Seram Island" right next to the highlighted sea -- same word, different transliteration, so the existing avoid-word guard never saw it as the same name. Alternate field set to "Seram Sea" (its real modern spelling); fixed itself on re-render, no code change needed.
- Cappadocia's historical map was a crude 10-point polygon with the base snapshot's "Kingdom of Antigonus" label sitting inside it, and a diagonal border-edge artifact bleeding through the semi-transparent highlight -- both from the 300 BCE snapshot being anachronistic here (Antigonus I died at Ipsus in 301 BCE, and Cappadocia was never his). Outline smoothed with a Catmull-Rom spline through the same anchor points (Assyria's hand outline smoothed the same way); moved off the snapshot's own labels onto hand-placed ones (Pontus, Galatia, Cilicia, Armenia), matching the pattern Assyria already used.
- Bohemia's map left Moravia and Silesia as blank unlabelled space in the same country (Carter: "no mention of moravia or whatever"). ne_more2.py regions built from one country's admin-1 union (Bohemia, Moravia, Silesia are the concrete case) now pass their siblings as labelled sister regions, the same way ne_region.py already does for ordinary subdivisions.
- Oxford comma / phrasing: Heilongjiang and Manchuria Info fields fixed ("Songhua, Nen and Ussuri" -> "..., Nen, and Ussuri"; Manchuria's "Korea, Mongolia and the Amur, and Ussuri rivers" was actually ambiguous, not just missing a comma -- reworded).
- Checked, not a bug: Heilongjiang's current reveal map already shows all sister provinces correctly (Inner Mongolia, Jilin, Liaoning, Russia, Mongolia, North Korea) -- likely Carter was seeing a stale cached copy under the old filename; restarting Anki should clear it. Maluku Islands are correctly in eastern Indonesia (confirmed via the corrected Ceram Sea map, which shows Seram/Buru/Halmahera in that group).
- Christmas Island: OSM's `named()` lookup returned four same-named relations (a Cape Breton hamlet and a sub-area were also called "Christmas Island"), and combining all four gave a bounding box that crossed the 180th meridian -- switched to the one correct relation ID by hand. Now down to 3 unsolved: Xikang, Daman and Diu (former subdivisions with no matching modern polygon), Cocos (Keeling) Islands (no OSM administrative relation found under any name tried).
- Carter, re-checking Bohemia after the sister-region fix above: "not showing Czechia at all... seems like one mass" -- correct, and a second real bug: a subdivision's sister-region borders (Moravia/Silesia next to Bohemia, but also every ordinary province-vs-province case ne_region.py draws) were the exact same grey and weight as a real international border, so nothing told the eye "same country" from "different country". Sister-region borders are now dashed and a shade lighter (ne_render.py, applies to every reveal/front that passes `regions=`, not just Bohemia); and since the sister regions fill the entire country, leaving no free spot for the country's own name, ne_more2.py's Bohemia/Moravia/Silesia captions now say "part of the Czech Republic" / "part of Poland (and a small Czech part)" outright, reveal side only. Re-rendered and re-applied every front and reveal touched by either fix today (country 203+203, subdivision-family 286+286, region/historical/feature family ~65+65 each across ne_more/ne_more2/ne_fronts/ne_historical) since the fix is in the shared renderer.
- Not yet done: Carter's "keep both" request (keep every intensely-zoomed labelled map as is, and *add* a second, zoomed-out, unlabelled map alongside it rather than replacing anything) -- needs a new field and template change, scoped separately.

## W80 -- Classical Music: which act, and a still-missing-Movement sweep (2026-09-22)
- Carter, checking a Madama Butterfly note whose Movement field just said "Arioso": confirmed correct, not a bug -- an arioso is a real, distinct term (shorter and more speech-like than a full aria), and this is the well-documented Act I passage where Cio-Cio-San tells Pinkerton she converted to Christianity for him. Not "arioso e scena" or any compound form; standalone "arioso" is right.
- 147 Classical Music Opera notes had a Movement naming a piece with no act ("Habanera", not "Act I - Habanera"). cm_opera_acts.py: fetches each opera's Wikipedia wikitext, splits it into Act-headed sections, and looks for the movement's name inside one. First pass matched 56 of 147 -- but hand-checking the suspicious ones against search caught real errors in 4 of them (Andrea Chénier "La mamma morta" is Act III, not the auto-matched IV; Idomeneo "Fuor del mar" is Act II, not III; Monteverdi's "Possente spirto" is Act III, not V; Barber's "Must the Winter Come So Soon" is Act I, not IV) -- corrected by hand. Lesson: substring-matching a synopsis is not reliable enough to apply blind; a word like "overture" or "prelude" turns up constantly in prose for unrelated reasons (Bartered Bride's bare "Overture" and Tristan's "Prelude" both false-matched to Act 3 this way before GENERIC was added to skip them outright). Applied 50 verified acts; parked 6 as genuinely version-dependent or ambiguous (Don Carlos "Ella giammai m'amò" is Act III in the standard 4-act revision but IV in the original 5-act French version; Hoffmann's Barcarolle likewise moves between Act II and III across editions; Die Entführung's Janissary chorus, Le Grand Macabre, Golden Cockerel and Snow Maiden need a real listen, not a guess); 91 of the 147 remain unresolved -- next pass.
- Carter caught that the newly-added acts weren't italicised ("Ein Mädchen... not italicized in the magic flute card") even though the Work field already is (`<i>Die Zauberflöte</i>`). Fixed across the whole Genre:Opera Movement field, not just today's 50 additions -- 37 notes gained `<i>...</i>` around the foreign-language title itself (English generic terms -- Aria, Chorus, March, Dance of the ..., Gavotte, Bacchanale -- correctly left plain, matching how "aria" itself is never italicised as a fully assimilated word).
- Carter: "Titan symphony doesn't mention what the piece is from" -- Mahler's Symphony No. 1 "Titan" had no Movement field despite its audio being specifically the withdrawn "Blumine" movement (filename said so). Fixed, then swept the *whole* deck per his "apply across the whole deck" instruction: 692 of 1,536 Classical Music notes have no Movement field at all. Most are legitimate -- a single-movement work (many Solo piano/Song/Tone poem/Overture entries) has no movement to name, and 231 of the 692 are Opera-genre "whole work" identification clips (see La Dame Blanche below), which is a different, likely-intentional category, not the same gap. Scanning every no-Movement audio filename for a decodable movement marker (Mov.N, a lone Roman numeral, a two-digit track number) found only 4 real cases: Beethoven's Eroica mvt. I turned out to be a straight duplicate of an existing, already-labelled note (suspended rather than re-labelled, matching the W40 duplicate convention), and Mahler 4, Mahler 9, and Bruckner 7 got their movements filled in properly (mvt. III coda, mvt. I, mvt. I).
- Carter asked whether La Dame Blanche (Boieldieu) was an aria, since it just says "Opera" with nothing else: it's the whole opera (1825 opéra comique), and the note is one of the 231 whole-opera generic clips above (30 s, almost certainly the Overture's opening) -- correct as a category, just worth knowing it's not a per-aria card.

## W81 -- Consolidated feedback batch: History, Classical Music, Geography (2026-09-23)
- History: italicised *Chibi* and *Iomante* (matching the deck's convention for romanised/foreign terms); Guangwu's card showed the generic Han-wall fallback image used for concept/event notes instead of a portrait -- he's a named emperor like Liu Bang or Wang Mang and should have had one; replaced with his portrait from Yan Liben's Thirteen Emperors Scroll (Museum of Fine Arts, Boston; public domain). Oxford comma sweep: 13 History notes, 22 Geography notes (including a genuine punctuation bug in the Five Classics note: "Changes and the Spring, and Autumn Annals" should never have had a comma splitting "Spring and Autumn Annals").
- Two systemic ne_points.py (city/peak/waterfall) bugs, found while chasing Carter's Seville river-label report and fixed at the source, then re-rendered across all 157 notes of those kinds:
  1. The "near the feature" proximity logic (rivers, admin-1 units) anchored on the bbox centre of `targets`, which defaulted to the *view's* centre when none was passed -- never the point's own location. A city far from the middle of its regional frame (Seville, well south of the Iberia box's centre) got no nearby-river label at all. Fixed with a synthetic point target at the marker's own coordinates.
  2. Natural Earth's own rank filter still dropped a locally important river as "minor" at a country-scale zoom (the Guadalquivir at Seville, rank 8 against a threshold of 4) even with the anchor fixed. Added a separate, rank-blind pass that finds whichever river's course comes closest to the marker itself and labels that one regardless of NE's importance ranking.
- Denali: region context labelled "United States" instead of "Alaska", and that "United States" then rendered directly on top of "Denali" itself. Root cause was general: an overseas/remote territory sharing its parent country's admin_0 polygon (Alaska and Hawaii as part of "United States", French Guiana as part of "France") was always labelled with the *owning* country's name -- Carter: "ensure the actual place is being labelled not the country which claims ownership over it". Fixed in ne_render.py's country-labelling loop: when the polygon actually visible in view sits far from the country's own official label point, it now looks up and uses the admin-1 region's own name instead. Also fixed the resulting duplicate-label collision in ne_points.py (the admin-1 lookup now runs before the general label pass and reserves its own space, rather than colliding with it after the fact). Verified against Suriname (neighbour was labelled "France"; now "French Guiana") and Denali (now "Alaska", no collision, "Kodiak Island" fits too).
- Lake Nasser: the "Red Sea" sea-name label landed in the desert, not on water -- `ne_10m_geography_marine_polys` is a coarse, label-placement-only layer, fine at country scale but not accurate enough at a tight lake-scale crop. Added a land-rejection check (a sea-label candidate actually inside a country's coastline at the current view's own resolution is now discarded) and bumped `MIN_SPAN["lake"]` from 5 to 7 degrees for more breathing room generally.
- Root-cause bug behind "US states don't render properly (light grey on blue)": `draw_polys()` filled each ring of a feature as its own separate solid polygon, which paints straight over a hole ring -- Canada's own polygon carves no separate hole for the Great Lakes at all in the source data (a single exterior ring that follows the shoreline), and depending on rendering order this could self-mask or not. Rewrote it to build one compound Path per feature (all rings as sub-paths, filled by the nonzero winding rule), which is the geometrically correct way to fill a multi-ring polygon regardless of holes. Re-rendered and re-applied every Geography front/reveal map across country, subdivision/US-state, city/peak/waterfall, physical-feature (river/lake/sea/gulf/strait/ocean/island/peninsula/range/desert/archipelago/estuary/bay/continent), and the UK-nations/old-French-regions/breakaway-region family (ne_more.py, ne_more2.py) -- all of them route through the same shared renderer, so all of them picked up this fix plus the darker map borders below in the same passes.
- Map borders darkened for contrast (`BORDER` #8f8f84 -> #6b6b60). Geography template: when a note has no Map Wide, the back was showing the plain unlabelled Map *and* Map Labeled side by side even though they're the same view with only the target's own name differing (Carter: "For maps that are exactly the same except for the label in question... it is only necessary to show the labelled version") -- back now shows Map Labeled alone in that case, falling back to plain Map only if Map Labeled is itself missing.
- List card type: Early China list cut dates off on phone width. Root cause was the classic flexbox overflow bug -- flex children default to `min-width: auto`, so a long unbreakable date string ("c. 2070-1600 BCE") refused to shrink and forced the whole row wider than the viewport instead of wrapping. Added `min-width: 0` to the name/stat cells plus a <480px breakpoint that shrinks the thumbnail and text further.
- Der Barbier von Bagdad (Cornelius) overture audio was crackly: spectrogram showed a hard cutoff at 16 kHz and a constant elevated noise floor even in quiet passages, consistent with an old, heavily compressed source. Used the existing chroma+DTW identification pipeline (_cm_id.py) to confirm several YouTube alternatives were genuinely the same piece (scores 0.056-0.068, all well within the confirmed-match range), then picked the one with visibly the cleanest spectrum (full extension to ~18 kHz, near-silent noise floor between notes) and swapped it in.
- New feature: Classical Music got a "Composer Image" field (none existed before) shown beside the composer plate on reveal only, degrading cleanly when absent. Carter's call after discussing the tradeoff (audio ID is the tested skill here, not portraits, so a picture mostly helps for placing an unfamiliar name rather than as a general aid): scoped to less-famous-but-quizbowl-relevant composers only, not the whole deck. First batch of 29 done (Corelli, Palestrina, Hildegard von Bingen, Webern, Villa-Lobos, Szymanowski, Josquin, Buxtehude, etc.), portraits sourced from Wikipedia's REST summary API, 39 notes updated. ~120 more of the 151-name less-famous tail remain if Carter wants the rest done.
- New feature: Geography got a "Flag Symbolism" field, shown as a caption under the flag on reveal only, after Carter clarified the map-captioning idea with examples (Easter Island's reimiro, Oman's khanjar). First batch of 30 flags captioned with genuine iconography (Oman, Nepal, Mexico, Brazil, Portugal, Bangladesh, Kosovo, Zimbabwe, Mozambique, etc., not just color/stripe descriptions). 381 Geography notes have a flag in total; the rest are unstarted.

## W82 -- Border contrast follow-up (2026-09-24)
- Carter, reviewing Maryland: the sister-state dashed border (from W79's fix distinguishing same-country splits from real frontiers) was too light to tell neighbouring states apart on its own, separately from the international-border darkening in W81. Darkened `#a8a89e` -> `#82826f` and bumped 1.5px -> 1.6px; also darkened the faint province-outline lines ne_points.py draws under a peak/city inset (`#cfcfc4` -> `#9a9a8a`, 0.5px -> 0.7px). Re-rendered and re-applied every Geography note that draws sister-region borders: country, subdivision/US-state, city/peak/waterfall, and the ne_more.py/ne_more2.py family (UK nations, old French regions, Bohemia/Moravia/Silesia and the other breakaway/historical-on-modern-borders set).

## W83 -- VFA movements and BISE terms: the Art concept gap closed (2026-09-24)
- Source: `#VFA.pdf`, the front "Movements" list (99 terms, pp. 2-4) and the later "BISE terms" list (53 terms, pp. 37-38). Deduped against each other by folded name -> 122 distinct terms; 48 were already Art concept notes. `art_vfa_terms.py`, running through concept_add.py's duplicate/leak/completeness checks unchanged: 71 proposed, 0 rejected, 71 added. 129 cards (71 DEFINITION to NAME, 58 MOVEMENT to FIGURES where a leading-figures list exists).
- Three list entries are not new cards: **Favusim** is a typo for Fauvism, which the deck has; **Les Nabis** is the deck's existing "Nabis"; **Academic** and **Academic art** are the same term across the two lists and got one card.
- Kind calls made without asking. Period/school/-ism terms are filed as **Movement**, matching the 46 the deck already files that way -- Baroque, Rococo, Mannerism, Neoclassicism and Northern Renaissance are all periods as much as movements, and consistency with what's there beats a tidier taxonomy. Two Kind values new to *Art* but already used elsewhere in the collection, so the template's "{{Kind}}?" still reads as a real question: **Period** (Classical antiquity, Hellenistic, Dutch Golden Age, Ottonian Renaissance -- "Movement?" would be plainly wrong) and **Concept** (Avant-garde, Gesamtkunstwerk, Humanism, Kitsch, Happening). Final spread: 54 Movement, 5 Style, 5 Concept, 4 Period, 3 Genre.
- Caravaggisti and (Utrecht) Caravaggisti both appear in the source list and both got a card, with definitions doing different work -- the pan-European followers who carried the manner to Naples, Utrecht, Spain and France, versus the three Dutch Catholics (ter Brugghen, Honthorst, Baburen) specifically.
- Artist deliberately left empty on nine notes, because the MOVEMENT to FIGURES card it generates would be unanswerable or self-answering: the broad periods (Gothic, Renaissance, Romanesque, Byzantine art, Modernism, Classical antiquity, Hellenistic, Ottonian Renaissance) and **Utagawa School**, whose leading figures are all named Utagawa and so are given away by the Title printed on that card's own front.
- No Artwork images on these 71. concept_add.py's argument is precisely that the definition-to-name card needs no picture and so cannot print a prompt over a blank; supplying Artwork would also switch on the IMAGE to MOVEMENT card, which is a separate image-sourcing-and-verifying job. **Follow-up**: the 46 older Movement notes all carry 2-4 captioned example images, so these 71 look thinner than their neighbours in the browser; worth a later image pass, at which point they gain a third card each.
- Dates normalised to en dashes afterwards to match the existing notes ("1924-1966" is stored as "1924–1966" throughout the deck); 57 notes touched. Backups: `art_all_before_vfa_2026-09-24.json` (all 4,625 Art notes, pre-run) and `art_vfa_terms_before_endash.json`.

## W84 -- Art gets a Figure card, and 118 artists who had none (2026-09-24)
- The Art note type had no biography card at all: every artist existed only as the Artist field on individual artwork notes. `art_figure_model.py` adds two fields (**Works**, a semicolon list with the most iconic work `<u>underlined</u>`, the Architecture Figure convention; **FigureCard**, the flag the templates branch on, since Anki cannot test `Kind == "Figure"`) and one template, **FIGURE to ARTIST**, built out of the deck's own `.art-concept-*` classes and its `.cap-figs` caption machinery. Architecture gets its Figure card by reusing its generic DEFINITION to NAME branch and so asks "Figure?"; Art already asks "Artist?" on three of its cards, so this one asks the same thing. `{{^FigureCard}}` guards added to DEFINITION to NAME and IMAGE to MOVEMENT, which both fire on any note with a Kind -- without them a Figure note would make three cards and Carter asked for one. No existing note has FigureCard set, so the guards changed nothing for the 4,625 notes already there (cards before 13,897, after 13,897).
- **Requires a one-time full sync.** Adding fields and a template sets Anki's schema-modified flag, so `anki('sync')` now returns "Sync status 2" and AnkiConnect has no action that can resolve it -- the direction has to be chosen once in the Anki GUI (Upload to AnkiWeb, since this machine holds the newer collection). Everything below is saved locally; nothing is at risk, but **nothing syncs until that is done**.
- The audit: 387 names in the VFA artist list (pp. 4-39), matched against every Artist and Title value in the deck by folded token-subset, then by fuzzy surname for the misses. 246 matched outright. 21 more are the deck's own spelling of the same person and were **not** re-added -- Mary Cassat/Cassatt, Vassily/Wassily Kandinsky, Kasimir/Kazimir Malevich, Michelangelo Buonarroti/Michelangelo, Jan/Johannes Vermeer, Joseph Turner/J.M.W. Turner, Claude Lorraine/Lorrain, Francesco Parmigianino/Parmigianino, Sol Le Witt/LeWitt, Lawrence Lowry/L.S. Lowry, Anton Raphael Mengz/Mengs, Lucio Fontano/Fontana, Mathis Gruenwald/Matthias Grünewald, Alexei/Alexej von Jawlensky, Angelica Kauffmann/Kauffman, Janis/Jannis Kounellis, Joachim Patenier/Patinir, Pierre August/Pierre-Auguste Renoir, Karl Schmidt-Rotluff/Rottluff, Fra Bartolommeo/Bartolomeo, Marie Elizabeth-Louise Vigee Lebrun/Élisabeth Louise Vigée Le Brun. Two more (Robert Mapplethorpe, Cindy Sherman) already have cards in the **Photography** deck, so they were skipped on the "has any card" rule rather than duplicated into Art. That leaves **118**, all added.
- Near-misses checked by hand and confirmed as genuinely different people, not spelling variants: Filippino vs Fra Filippo Lippi (son and father, both now present), Peter vs William Blake, John vs Agnes/Simone Martin(i), Avis vs Barnett Newman, Mary vs Ellsworth Kelly, Germaine Richier vs Gerhard Richter, Salvator Rosa vs Salvador Dalí, Hans Hofmann vs Josef Hoffmann, Thomas vs Jacob Lawrence, Jan Bruegel vs Pieter Bruegel.
- Content: the 41 names with research bullets in the PDF used them as the factual basis, checked against Wikipedia; the other 77 researched from scratch. Two PDF claims were **not** copied because they did not hold up: Elisabeth Frink's Goggle Heads are usually traced to the Moroccan general Oufkir (the bullets implied something vaguer), and the bullet crediting Richard Deacon as co-curator of *The Stage of Drawing* does not match the record, so that entry names no co-curator. Every Description omits the artist's own name (concept_add.py's leak check enforces it; 0 of 118 rejected).
- Images: Wikipedia REST summary for all 118 (2 needed a disambiguated title: Craigie Aitchison (painter), Peter Howson), then a Commons file search for the 19 with no article image. **Every candidate was viewed before use**, tiled twelve to a contact sheet rather than one at a time. Two were rejected on sight: the only "Rebecca Horn" image on her article is an Indian government photograph that cannot be confirmed as her, and the only John Bratby hit was a blue plaque -- which would also have printed his name on the question side. 104 notes carry a picture, captioned by what it actually is (portrait / self-portrait / a named work); 14 ship text-only, which the template handles, since `{{#Artwork}}` is conditional.
- **Known, deliberately not fixed here**: media filenames embed the artist's name (`artfig-gwen-john-1.jpg`), which is a leak to anyone who inspects the card HTML. This is the collection's existing convention -- Architecture's 116 Figure notes use `archp-jørn_utzon.jpg`, Classical Music's portraits the same -- so half-fixing it in one batch would be worse than leaving it. Worth one consistent sweep across all three decks later.
- Also this session, logged in W83: the 71 new VFA/BISE term cards. Art concept notes now stand at 300 (118 Figure, 100 Movement, 51 Technique, 6 Style, 5 Format, 5 Concept, 4 Object type, 4 Genre, 4 Period, 3 Subject). Backup of the model before the change: `templates_backup/art_before_figure_2026-09-24.json`.

## W85 -- BISE main and BISE other: every work on both lists (2026-09-24)
- The two artwork lists (`#VFA.pdf` pp. 28-37) hold 200 works once the six period headings in each are dropped. Matching by folded title, then past leading articles and parenthetical subtitles, then by hand: **121 already in the deck, 77 added, 2 deliberately not added.**
- The match needed three passes because so many are in the deck under a different title. Worth recording, since a future audit of the same list will hit them again: Venus / Woman of Willendorf = Venus of Willendorf; Tomb of Marie Christina = Tomb of Maria Christina of Austria; States of Mind: Those Who Go = States of Mind II; The Cow with the Subtile Nose = ...Subtle Nose; Achilles and Ajax Gaming = ...Playing a Game; Judith Slaying Holofernes = Judith Beheading Holofernes; Head of Charles I in Three Positions = Charles I in Three Positions; Bentheim Castle = View of Bentheim Castle; Portland Vasse = Portland Vase; Under the Wave off Kanagawa = The Great Wave off Kanagawa; Sunday on La Grande Jatte = Sunday Afternoon on the Island of La Grande Jatte; Easter Island statues = Moai; Studies for The Virgin and Child with St. Anne = Burlington House Cartoon; Santa Trinita Maesta = Madonna and Child Enthroned; Salt Cellar = The Salt Cellar of Francis I; Louis XIV = Portrait of Louis XIV; Pilgrimage to the Isle of Cythera = Embarkation to Cythera; Trajan's Column = Column of Trajan; Sir John Hawkwood = Funerary Monument to Sir John Hawkwood; Colleoni statue = Bartolomeo Colleoni; Allegory with Venus and Cupid = Venus, Cupid, Folly, and Time; Absinthe = The Absinthe Drinker; Adoration of the Magi (Strozzi Altarpiece) = The Adoration of the Magi.
- **Two not added, with reasons.** "A Rake's Progress: The Levee" is plate 2 of a series the deck already carries as "A Rake's Progress [plate 1]" -- a second plate is a near-duplicate, not new coverage. Ghiberti's "Sacrifice of Isaac" collides by title with the deck's existing Brunelleschi competition panel, and Commons has Brunelleschi's panel and the two together but not Ghiberti's alone, so there was nothing to put on the card; left for a later pass.
- **One source error corrected rather than copied**: the PDF lists "La Loge, Pierre-Auguste Rodin". La Loge is Renoir's, and the deck has it as The Loge.
- Schema read off six existing artwork notes before writing any: Title in `<i>`, Location wrapped in `<span class="loc-noise">` with the `Art::loc::noise` tag (4,032 of the 4,513 notes with a location do this), Style as "Movement; Medium", Nationality as a demonym. Tier tag `Art::tier::tier2-solid` for the whole batch -- works off a national study list are solidly clued, but claiming tier1 for all 77 would be false. 207 cards: 65 notes get three (ARTWORK to ARTIST, ARTWORK to TITLE, TITLE to ARTIST), 12 get one.
- **The image pass rejected 21 of the first 78 on sight**, and the pattern is worth knowing: Wikipedia's lead image for a *work* is very often a photograph of the building that holds it, the site it came from, or the artist -- San Vitale's exterior stood in for the Justinian and Theodora mosaics, Chartres's west front for its windows, Santa Croce's facade for a Giotto fresco inside it, the Baptistery exterior for Nicola Pisano's pulpit, a modern street photo for Daguerre's 1838 daguerreotype of it, the abbey ruins for Turner's watercolour of them, and portraits of Barye, Martinez Montanes, Gaulli, Deineka, Heartfield and Schnabel for their works. All re-sourced from Commons and viewed again. One more was caught on the second pass: a search for Ghiberti's competition panel returned Brunelleschi's.
- **12 ship with no picture**, which is a deliberate, safe state: an Art note with an empty Artwork generates no ARTWORK card at all (Anki will not create a card whose front renders no non-empty field), so they fall back to TITLE to ARTIST rather than printing "Artist?" over a blank -- the exact failure concept_add.py was written against. Nine are in copyright with nothing usable (Ned Kelly series, Big Red, Cubi XIX, Woman Descending the Staircase, Away from the Flock, The Clock, Humanity Asleep, The Defence of Petrograd, Hurrah, the Butter is Finished!); three had no image actually of the work (Reliquary of Teuderic, Bonampak murals, Tomb of Henry VII and Elizabeth of York).
- **Latent bug found and fixed while here**: 27 artwork notes with Artist "[unknown]" had no `Anon` flag, so they generated an ARTWORK to ARTIST card asking "Artist?" whose answer is "[unknown]", and a TITLE to ARTIST card doing the same. `Anon` is set on 25 of them (the two without an image are left alone, since Anon would leave them with no card at all: Reliquary of Teuderic and Bonampak murals, both of which want an image anyway). Backup: `art_anon_before_2026-09-24.json`.
- **Two GUI actions are now waiting for Carter**, both one-off: (1) the full sync from W84, and (2) Tools > Empty Cards, to clear the ~50 cards the Anon fix just turned off -- Anki leaves existing cards in place when a template conditional stops matching, and AnkiConnect has no action for it.
- Art deck now: 4,891 notes, 14,222 cards.

## W86 -- Architecture concept list audited against the deck (2026-09-24)
- Source: `#VFA.pdf` pp. 41-46, the Architecture "Bise main" list. 106 entries, six of them the section headings the list is grouped under, leaving 100 terms. `arch_vfa_terms.py`: **37 added**, 0 rejected by the leak check, one card each (every Architecture template except DEFINITION to NAME is `{{^Kind}}`-guarded).
- **The list is a book's table of contents, not a glossary**, and about a third of it is chapter titles no one could be asked to name -- Shelter, Dwellings, Reviving the past, Statement architecture, Industrial aesthetics, Expressive mass housing, Elemental architecture, Architectural design, Metro style, American Modern, Humane Functionalism, Late Le Corbusier, Postwar skyscrapers, Sensual modernity, A new city, Free spirits, Pure form, Modern monumentalism, Connecting heaven and earth, Sensationalism, Accessibility, Soulful modern, New forms, Response to the earth, Mountain cities, Italian hill towns, Secular Gothic, Early and Late imperial China, Edo-period Japan, Russian Empire, War memorials, The Industrial Revolution. Those got no cards. The Great Wall is a named building, not a term, so it is out of scope here too.
- 26 were already covered (the ziggurat, column, stupa, arch, dome, Byzantine, Romanesque, Gothic, Mannerism, Palladianism, Baroque, Rococo, Gothic Revival, Arts and Crafts, Art Nouveau, Art Deco, Brutalism, Postmodernism, Deconstructivism, Expressionism, The Renaissance, Organic forms = Organic architecture, The Ottoman Empire = Ottoman, Mughal India = Mughal, Architecture of the Russian Revolution = Constructivism, The new vernacular = Vernacular). Classicism and Classical Revival were left out as duplicates of the deck's existing Neoclassical and Greek Revival.
- **Where a chapter title had a real term behind it, the term was used**, which is most of the value in this pass: Latin American Baroque -> Churrigueresque; French and Spanish Renaissance -> Plateresque; Late-flowering Gothic -> Perpendicular Gothic *and* Flamboyant (English and French phases, both clued, both distinct); Building Minimalism -> Minimalism; Italian Empire -> Rationalism; Spanish Colonial revisited -> Spanish Colonial Revival; Postmodern Classical -> New Classical architecture; Green architecture -> Sustainable architecture; West African architecture -> Sudano-Sahelian architecture; Modernism in Sri Lanka -> Tropical Modernism; The Islamic garden -> Charbagh; The concrete frame -> Reinforced concrete; Gridshells and webs -> Gridshell; Mud -> Adobe; Pioneering Modernism -> Modernism (which the deck did not have as a style at all, only its branches).
- Spread: 21 Style, 7 Building type, 5 Element, 4 Concept. "Concept" is new to Architecture but is an established Kind elsewhere in the collection (Photography, Performing Arts, Classical Music), so "Concept?" reads as a real question on the card. Style notes get Style/Main style set to their own name and Architect "[not applicable]", matching the 41 already there.
- No pictures, same call as W83: the definition-to-name card needs none and a Kind-bearing note makes only that card. The 41 existing Style notes all carry three captioned photographs, so these 37 will look thinner in the browser until an image pass is run -- logged with the Art one.

## W87 -- A Film deck: design, then the source list (2026-09-24, in progress)
- New note type and deck, `film_model.py`. **Four card types**, so the deck tests four different things instead of drilling one:
  1. **CLUE to TITLE** -- a quizbowl-flavoured paragraph (specific images first, director last as the giveaway) answered with the title. The workhorse, and the only card every film gets, because it needs no picture and so can never render a prompt over a blank.
  2. **STILL to TITLE** -- pure recognition from a frame. Built only where a genuinely free still exists, which in practice means public-domain films. **Deliberately not a poster card**: a poster has the title printed on it, which is the leak the brief warns about.
  3. **TITLE to DIRECTOR** -- attribution, suppressed by a `DirectorTells` flag for titles that give the director away.
  4. **FIGURE to NAME** -- a director's portrait and a one-sentence career, same shape as the Art and Architecture Figure cards, for directors who recur across the list.
- Leaks are designed out rather than checked afterwards: the poster is on the **answer side only**, the still's caption likewise, and every clue goes through concept_add.py's leak check against its own title before being written. Two were caught and rewritten on the first two batches (*Beauty and the Beast* said "the Beast's hands"; *The Spirit of the Beehive* said "a spirit she can call"). The check is skipped for titles of one or two characters -- *M*, later *Kes* -- where a substring test fires on any English sentence.
- Look: the collection's shared `.qb-card` / `.qb-panel` / `.qb-eyebrow` skeleton and the same custom-property palette structure as Classical Music, Performing Arts and Photography, with its own accent (deep blue-green, against Classical Music's rust and Performing Arts' purple) so the deck reads as part of the set without being a copy. **Dark mode follows the house rule exactly**: every `.night_mode` / `.nightMode` selector re-declares the light palette, which is what every other deck here does. It does not use `:root:not([data-theme="light"])`, which is wrong for Anki and has been a real bug in this collection before.
- 17 fields: Title, Original title, Director, Year, Country, Movement, Cast, Clue, Still, Still caption, Poster, Picture, Works, Notes, Kind, DirectorTells, Alternate. Foreign films carry both titles; the original is shown under the English one on the answer side and on the TITLE to DIRECTOR front.
- Source list: 202 films across BISE main (115) and BISE other (87), once the six chapter headings in each are dropped. **74 done so far** (film_data1.py and film_data2.py), 148 cards. Two PDF slips corrected on the way: "Gone with the Wine" and "Zero do Conduite" (= *Zéro de conduite*, stored as *Zero for Conduct*).

## W88 -- Film deck finished: 250 films, 38 directors, all four card types live (2026-09-24)
- Completes W87. **288 notes, 547 cards**: 250 CLUE to TITLE, 250 TITLE to DIRECTOR, 38 FIGURE to NAME, 9 STILL to TITLE.
- **Coverage.** All 202 films on the two BISE lists, then 48 more, which puts the deck at the top of the 150-250 band the brief asked for.
  - *Pre-2014 gaps* (film_data6.py, 22): the lists have no Buster Keaton at all, no *Rear Window* or *North by Northwest*, no *8 1/2*, no *Lawrence of Arabia*, no Tarkovsky before *Stalker*, no Varda, no Chytilová, no Mizoguchi, no Edward Yang, no Claire Denis, no *Goodfellas*, no *Schindler's List*, no *Grave of the Fireflies*. Each was picked on one test: would a packet written today expect it?
  - *2015 onward* (film_data7.py, 26): the source stops dead at *The Grand Budapest Hotel*, so a full decade is missing. Added the Palme d'Or and Best Picture winners that stuck, the international-feature winners, and the genre films that became reference points -- *Mad Max: Fury Road*, *Son of Saul*, *Moonlight*, *Get Out*, *Parasite*, *Roma*, *Portrait of a Lady on Fire*, *Drive My Car*, *Everything Everywhere All at Once*, *Oppenheimer*, *Anatomy of a Fall*, *The Zone of Interest*, *Poor Things* and the rest.
- **Director cards.** One note for each of the 38 directors with two or more films in the deck. The Works list is generated from the deck itself rather than typed, oldest first with the iconic film underlined, so it cannot drift out of date as films are added. Portraits from Wikipedia, all 38 viewed on contact sheets.
- **Nine answer leaks caught by the automated check and rewritten**, which is the check earning its keep: *Beauty and the Beast* ("the Beast's hands"), *The Spirit of the Beehive* ("a spirit she can call"), *Raise the Red Lantern* ("lanterns outside a courtyard"), *The Lord of the Rings* ("carry a ring"), *Closely Watched Trains* ("ammunition train"), *Hearts of Darkness* ("a heart attack"), *Drive My Car*, *Everything Everywhere All at Once* ("a bagel with everything on it"), *Past Lives* ("ties built over past lives"), *Portrait of a Lady on Fire* ("a marriage portrait"), and *Andrei Rublev*, where the director's own first name is the film's first word, so the clue now says only "Tarkovsky directed".
- **Three leaks caught by eye, not by code**, all on images, which is why the look-at-it rule exists: Wikipedia's lead image for **Andrei Tarkovsky** is a Russian postage stamp with his name and dates printed on it in Cyrillic (his Figure note ships without a picture); the only *Passion of Joan of Arc* still on Commons is a release poster with the title across the top; and the *Intolerance* "still" is a murky tinted video thumbnail. *Sunrise* was dropped too -- a publicity head-and-shoulders of the lead is not a scene, and makes a poor recognition prompt.
- **The still card is small on purpose.** Film stills are in copyright, and a poster is an answer leak by construction, so STILL to TITLE exists only where a genuinely free frame does: nine public-domain films (A Trip to the Moon, Caligari, The General, Un Chien Andalou, The Great Train Robbery, City Lights, His Girl Friday, Meshes of the Afternoon, The Jazz Singer). Adding more means a rights judgement Carter should make, not an automated scrape.
- The short-title rule: the leak check is skipped for titles of three characters or fewer (*M*, *Kes*), where a substring test fires on ordinary English -- "kes" sits inside "kestrel", which is the bird *Kes* is named for and exactly what its clue should say.
- Two source slips corrected rather than copied: "Gone with the Wine", and "Feften" for *Festen*.

## W89 -- Session close: what is done, and the two things waiting for Carter (2026-09-24)
- All five parts of the night's brief are complete. Totals: **Art 4,891 notes / 14,222 cards** (was 4,625 / 13,897), **Architecture 676 / 1,517**, **Film 288 / 547** (new). 591 notes added in all: 71 Art concept terms, 118 Art Figure biographies, 77 BISE artworks, 37 Architecture concept terms, 288 Film notes. No note anywhere in the new work has zero cards; 213 media files added (104 artist portraits, 65 artwork images, 44 film stills and director portraits).
- **Two GUI actions are required before any of this syncs, and nothing syncs until the first one is done:**
  1. **Full sync.** Adding fields and templates to Art, and creating the Film note type, set Anki's schema-modified flag. `anki('sync')` now returns "Sync status 2" and AnkiConnect has no action that resolves it. In Anki: Tools > Preferences > Sync, or just hit sync and choose **Upload to AnkiWeb** -- this machine holds the newer collection. Everything is saved locally in the meantime; nothing is at risk.
  2. **Tools > Empty Cards.** The `Anon` fix in W85 turned off about 50 unanswerable "Artist?" cards on notes whose artist is "[unknown]". Anki leaves existing cards in place when a template conditional stops matching, so they need clearing once.
- **Left undone, deliberately, and worth a later pass:**
  - *Images for the 108 new concept cards* (71 Art, 37 Architecture). The definition-to-name card does not need one, which is why they were skipped; but the 46 older Art Movement notes and the 41 older Architecture Style notes all carry two to four captioned photographs, so the new ones look thinner in the browser. Adding images also switches on a third card (IMAGE to MOVEMENT) for the Art ones.
  - *13 BISE artworks and 14 artist biographies with no picture*, listed in W84 and W85. Most are in copyright; a few just need a better search.
  - *Media filenames embed the answer* (`artfig-gwen-john-1.jpg`, `filmdir-stanley-kubrick.jpg`). This is the collection's existing convention -- Architecture's Figure notes and Classical Music's portraits do the same -- so it was left alone rather than half-fixed in one batch. One consistent sweep across all decks would close it.
  - *The Film deck's STILL to TITLE card covers nine films.* Extending it past public-domain material is a rights judgement, not an automation problem.

## W90 -- Pictures for the 108 new concept cards (2026-09-24)
- Closes the largest of the follow-ups logged in W89. **Architecture: all 37** terms now carry a captioned picture (card count unchanged at 1,517 -- a Kind-bearing Architecture note makes one card either way). **Art: 70 of 71**, which also switches on the deck's IMAGE to MOVEMENT card; term cards went 129 -> 194 (71 DEFINITION to NAME, 58 MOVEMENT to FIGURES, 65 IMAGE to MOVEMENT). Art deck now 4,891 notes / 14,287 cards.
- **The five Concept notes get `TextOnly` set** (Avant-garde, Gesamtkunstwerk, Humanism, Kitsch, Happening). The picture still shows on the definition card, but the image-only card is suppressed: "Concept?" over a photograph is not a fair question, where "Movement?" over a Gauguin is.
- **The Art template puts the picture on the FRONT of the definition card**, so anything with the answer written on it is unusable. Twelve of the first 71 were rejected on sight and re-sourced, and the pattern is instructive: *Les XX* returned an 1889 exhibition poster with "LES XX" in the design; *CoBrA* returned a photograph of the Cobra Museum with the name across the facade; *Action painting* returned a book cover with the collection's name on it. The rest were wrong rather than leaky -- *Body art* got body painting, *Classical antiquity* got a 19th-century academic painting **of** antiquity rather than any of it, *Group of Seven* got a photograph of the seven men instead of the landscapes, *Primitivism* got a Rousseau that was already the Naive art picture, *Synthetic Cubism* got the same Analytic Cubist figure as Analytic Cubism, *Grand Manner* got a Raphael fresco two centuries early.
- Five of the 37 Architecture images were replaced the same way: *Theatre* was a bronze statuette of an actor, *Basilica* a CGI reconstruction, *Minimalism* a Donald Judd sculpture (minimalist art, not architecture), *Spanish Colonial Revival* a Mexico City post office rather than anything Californian, and the *Garden city movement* diagram has the word GARDENS printed in it.
- **One term ends with no picture: Action painting.** Pollock is in copyright and Commons has no free reproduction of a drip painting; the only candidates were a photograph of the man and a book cover, and neither is the work. It keeps its text-only card, which is the same call made for the in-copyright artworks in W85.

## W91 -- Audit pass, and a key work beside the portrait on 19 Figure cards (2026-09-24)
- **Residual-leak audit over everything added tonight: 0 hits.** Checked beyond what the build-time check covers -- for every Film note, whether the clue contains the title *or the original-language title*; for every director note, the name or surname; for all 306 new Art and Architecture concept and Figure notes, the name in the Description. **Structural audit: 0 problems** -- no duplicate titles within a batch, no note without a card, no unbalanced `<i>`/`<u>`, no stray HTML entity, no `<img>` without a src.
- **Two director portraits had silently failed to attach**, both name-key mismatches the audit caught: the Coen brothers' image was filed under "Coen brothers" while the note is titled "Joel and Ethan Coen", and Ozu's under "Yasujirō" (macron) against a note reading "Yasujirô" (circumflex). Both fixed; only Tarkovsky is now deliberately picture-less.
- Confirmed by direct search that the **14 artist biographies with no picture are a rights problem, not a search problem** -- Atkinson, Boyce, Bratby, Cooper, Hitchens, Horn, Kelly, Kiff, Kossoff, Lanyon, Milroy, Newman, Olitski, Oulton are all living or recent, and Commons has neither their work nor a usable photograph of them. Worth re-checking in a year, not worth more searching now.
- **Key work added beside the portrait on 19 Art Figure notes**, matching the Architecture Figure pattern of portrait-plus-work: Blake, Bouts, Chadwick, Chillida, Cuyp, Epstein, Hambling, de Heem, Hobbema, Lawrence, Lely, Martin, Opie, Paolozzi, Piero di Cosimo, Pollaiolo, Sutherland, Witz, Zoffany.
- **That pass tried 118 and kept 19, which is the useful finding.** Looking up a work by its bare title on Wikipedia lands on the generic article about the subject roughly half the time, and the failures are comic but would have been shipped blind: Polke's *Bunnies* returned a photograph of a rabbit, Rosenquist's *F-111* an aircraft, Rothenberg's *Butterfly* a butterfly, Sickert's *Ennui* a stock photo of a bored woman, Hodler's *Night* a night sky, Horn's *Unicorn* a woodcut unicorn, Lanyon's *Thermal* a meteorological diagram, Ayres's *Distillation* a still, Oulton's *Fool's Gold* a pyrite crystal, Feininger's *Cathedral* a cathedral in Brazil, Yeats's *The Liffey Swim* a photograph of the actual race. Two more were dropped as duplicates of the note's existing picture (Hilton, Crivelli). **A work title needs the artist's name in the lookup; the REST summary API cannot take one, so this is a Commons-search job, not a summary-API job** -- worth knowing before anyone repeats it for the other 79.

## W92 -- Film card rendering bug, and the missing Geography images (2026-09-24)
- **Carter: "film card not rendering properly (dark on dark on white)".** Real bug, and mine. Anki puts `night_mode` on `<body>`, which has two consequences the new Film CSS got wrong: a class selector cannot reach `<html>` without `:has()`, so my `.night_mode html, .night_mode body` block could never match anything; and Anki's own night-mode rule for `.card` is more specific than a bare `.card`, so **Anki's dark background won while my dark `--ink` still won on the text** -- dark on dark, with the page behind it left white. I had also pinned the *light* palette for night mode, copying Classical Music and Performing Arts. Those two predate the fix; **Architecture, Geography and Art are the pattern to follow**, and they carry a real dark palette on `:root.night_mode, :root.nightMode, html:has(> body.night_mode), html:has(> body.nightMode), .night_mode, .nightMode, .night_mode .card, .nightMode .card` plus a second rule forcing `background-color` and `color` with `!important`. Film now does the same, with a dark palette keyed to its blue-green accent (`--bg #17181a`, `--ink #e7e5df`, `--accent #8fc3bd`).
- **Carter: "some geography images not rendering/loading".** 643 of the 644 `Map Wide` values in Geography pointed at files that do not exist. `Map Wide` is the second, zoomed-out, unlabelled map from the "keep both" request parked at the end of W79: the field was written across the deck and the images were never rendered. A walk of the project, `C:\QB` and `collection.media` (48,962 files) found none of the 643 names. 128 were repairable by case alone and were re-pointed at the file that does exist; the other 515 were cleared, after backing up all 1,061 notes' `Map` and `Map Wide` values, so the card falls back to the W81 behaviour (show Map Labeled alone) instead of drawing a broken-image box. **Re-rendering Map Wide is now the outstanding Geography task** -- the filenames record which map each note wanted, so nothing is lost.
- **A second, quieter failure of the same kind, found by sweeping every deck**: nine images whose filenames were written onto notes by the W78 fixes but never stored -- Hogarth's Beer Street and Gin Lane, Bronzino's Allegorical Portrait of Dante, the Grande Jatte on the Post-Impressionism note, the Wassily chair and the Triadic Ballet on the Bauhaus note, Bernini's St Peter's colonnade and Sant'Andrea al Quirinale, and Gaudí's Sagrada Família. All nine sourced, viewed and stored under the exact filenames the notes already expect. **Collection-wide, exact-case broken image references are now 3**, all of them the Xikang / Daman and Diu / Cocos (Keeling) maps that W79 recorded as having no usable polygon source.
- **Worth knowing: this collection's media folder is case-folded.** `storeMediaFile` came back with `art-hogarth-beer_street.jpg` for a file sent as `art-Hogarth-Beer_Street.jpg`, and the same is true of the older `alabama.png` against a note reading `Alabama.png`. Windows has a case-insensitive filesystem, so a case-mismatched reference renders on the desktop and **breaks on AnkiDroid, iOS and macOS** -- which means the phone shows breakage the desktop does not. Fifteen such references (6 Art, 3 Architecture, 128 Geography earlier in this entry) were re-pointed at the stored spelling.
- **Method note for anyone auditing media again**: the obvious regex `src\s*=\s*["']([^"']+)["']` is wrong here and reports about a hundred false positives, because it stops at an apostrophe *inside* a filename (`Christ's_Entry...`, `Ginevra_de'_Benci`, `Blind_man's_bluff`). Match the quote character instead: `src\s*=\s*"([^"]*)"|src\s*=\s*'([^']*)'`. I ran the bad version first and it nearly sent me repairing 105 images that were fine.

## W93 -- Images: the Film deck given a gallery, and captions for the BISE artefacts (2026-09-24)
- **Carter: "ensure the cards have lots of high quality images with captions, like the art/architecture decks", then "i want the card to give me a 'taste of the film'", "at least 2" stills, and "go through lists of famous stills, objects, scenes... if they belong to a film in the deck".**
- **Film deck went from 9 images to 495**, across 250 notes: a poster on all 250, and 244 stills spread over 127 films (43 with three, 31 with two, 53 with one). The answer side now renders a captioned grid -- stills first, poster last -- built with `<figure>`/`<figcaption>` rather than the JS caption machinery, so it needs no script and degrades cleanly. New fields: Still 2/3 and their captions, Poster caption, Caption.
- **The source is Wikipedia's media-list endpoint, which returns every image on a film's page together with the caption the article gives it** -- "The Tramp meets the Blind Flower Girl", "Peter Lorre as Hans Beckert", "Costume worn by Judy Barton/Madeleine Elster". Those captions are reused verbatim, so each picture arrives already explained. 1,140 candidates were cached for the 250 films, once, so the picking could be re-run without re-fetching.
- **Carter's reframing changed the filter and was right.** My first pass asked "is this a film still?" and threw away Radio Raheem's boombox, the preserved U-boat from *Das Boot*, the Bradbury Building, the *Days of Heaven* locusts, Vertigo's green dress, the Tikal temple that plays Yavin 4 and the Tunisian hotel that plays the Lars homestead. Those are exactly the recognisable things that give a taste of a film, so the rule became: keep anything from or about the film, exclude only what is genuinely unrelated.
- **All 273 downloaded stills were looked at; 29 were cut.** Three kinds: images with the title burned in, which would be an answer leak on the STILL to TITLE question side (*Singin' in the Rain*'s marquee, *The Big Heat*'s title screen, *The Night of the Hunter*'s trailer frame, *The Red Shoes*' flyer, both *Jaws* items); modern red-carpet and panel photos (*Tár*, *Toy Story*, *Boyhood*, *Get Out*, *Crouching Tiger*); and things simply not of the film (a Hogarth painting on *Barry Lyndon*, a Renoir painting on *The Rules of the Game*, a Schopenhauer portrait on *Caligari*, a still from *Bicycle Thieves* on the *Pather Panchali* page).
- **Posters were checked differently, and this is worth recording.** A visual pass covered 60 of 250; the rest were verified programmatically against the failure mode that actually matters -- a wrong film or wrong year -- by testing each poster's source article against the note's own title and year. Two flagged, both correct (*Festen* is filed under *The Celebration*, and 8 1/2 under 8½). The resolver asks for "Title (Year film)" first, which is why nothing drifted.
- **The ceiling here is copyright, not effort.** Wikipedia allows essentially one non-free image per article, so films with several pictures are mostly public domain; 114 of the 250 yield no still at all and 83 yield two or more. Commons per-film categories were probed as a second source and are noisy (videocassettes, a festival photo, book editions) for a modest gain. **The clean unlock is a free TMDB API key**, which would give several real stills for essentially every film in the deck, including the modern ones; the gallery fields are already in place to receive them.
- Separately, Carter: "Add explanatory captions for the artifacty/old artworks... nothing crazy just simple brief explanations." **All 65 BISE works that carry an image now have a one-line caption** saying what the object is and where -- the Coatlicue's twin snake heads and necklace of hands and hearts, the Teotihuacan mask's hollow eyes that were never meant to be worn, Boulevard du Temple's street that looks empty because only a man having his boots polished stood still long enough. They render on the answer side of all three artwork cards through the deck's existing `qb-caption-data` mechanism, so no question side changed. The twelve works with no image were skipped.

## W94 -- Style and movement cards given real picture sets (2026-09-24)
- **Carter: "style / movement cards must have multiple images -> e.g., spanish revival does not"**, then **"khmer style repeats the same two images (both of angkor wat)"** and **"same with the timber framing"**.
- All **108 new terms now carry 3-4 captioned pictures** (Architecture 35 with four, 2 with three; Art 64 with four, 7 with three), matching the 41 Architecture Style and 46 Art Movement notes already in those decks. Captions come from Wikipedia's media-list, which returns each article image with the caption the article gives it, so the pictures arrive described. Picture and caption counts match exactly on every note.
- **Repetition was the real defect, and it needed a different fix from scarcity.** A style article's media-list often returns the same monument three times -- Angkor Wat from the moat, its central prang, one of its galleries -- or three near-identical half-timbered streets. A subject-repetition detector over the captions flagged 13 terms; Timber framing was not among them, because its three pictures were different towns that simply *look* the same, which is Carter's point and the reason the rule became one picture per *article*, from deliberately different subjects. Khmer now runs Angkor Wat, the Bayon's faces, Banteay Srei and Ta Prohm's roots; timber framing runs a 1568 Hoefnagel watercolour of Nonsuch Palace, the Rokumeikan in Tokyo and a carved Strasbourg frame; action painting runs Kline, Krasner and de Kooning.
- **One image per article needed a second pass of its own.** Taking the first acceptable image off an artist's page returns memorabilia: a commemorative plaque on de Kooning's birth house, an engraving of Benjamin West's birthplace, a stack of Asger Jorn's books, a 1976 photograph of the Castle of Mirandola. Candidates are now scored for actually being a work -- a date, or a medium named in the caption -- with that test relaxed for buildings, which are photographed with neither. That relaxation is why Khmer came back empty on the first attempt.
- **14 images rejected on sight**: printed matter carrying the answer (the Futurism manifesto page, the Les XX exhibition poster, the Volpini poster, two labelled pyramid diagrams, the Knave of Diamonds catalogue in Cyrillic), wrong subject (a Taos Indians painting under Adobe, a restroom sign under Minimalism), wrong phase (a 1916 Gris under Analytic Cubism, a 1907 Braque under Synthetic Cubism), and two duplicates of the note's own picture.
- **A regression I caused and caught**: rebuilding the picture lists from the image log blanked the *first* caption on all 107 notes, because those were hand-written in W90 and had only ever existed inside a shell heredoc -- Angkor Wat stayed on the Khmer card and lost its line. Restored, and the Architecture map now lives in `term_first_captions.py` rather than in a one-off command. Lesson: data typed into a heredoc is not saved anywhere.
- Separately, **Carter: "replace the bank of england image in john sloane's card"**. John Soane's Picture 2 was a mostly-black line elevation of the museum's facade, captioned "The Dome area, Sir John Soane's Museum" -- caption and image did not match and the image was close to unreadable. Replaced with a photograph of the Dome area itself, top-lit and packed with casts, under the same filename so nothing else had to change.

## W95 -- Photography and Performing Arts audited against quizbowl (2026-09-24)
- **Carter: "is the photography and performing arts decks optimized for quizbowl?"** Audited both; answer was no, in different ways. He approved every fix except adding drama to Performing Arts.
- **Photography's largest defect: every card on a work note had the same answer type.** 432 PHOTOGRAPH to PHOTOGRAPHER plus 427 TITLE to PHOTOGRAPHER -- one fact asked twice, and the photograph itself was never an answer, though in quizbowl it routinely is. *Migrant Mother*, *The Falling Man*, *Moonrise Hernandez*, *Raising the Flag on Iwo Jima*, *The Steerage*, *Earthrise*, *A Harvest of Death* and *Saigon Execution* were all already in the deck and none could be asked for. **PHOTOGRAPH to TITLE added: 894 -> 1,325 cards.** A new `TitleGeneric` field suppresses it where the title cannot be an answer; only a bare "Untitled" qualified, since "Untitled (Cowboy)" and "Untitled Film Still #21" are real answer lines.
- **Performing Arts had 319 images and no card that used one as a prompt** -- media appeared on answers only, in a collection whose Classical Music deck is built on identification from the media. **MEDIA to NAME added: 448 -> 721 cards.** It asks "{{Kind}}?", the shape Architecture already uses. **46 notes are suppressed by a new `MediaTells` field because their image is the answer in print**: about thirty jazz notes use the original album cover (*Kind of Blue*, *Bitches Brew*, *Giant Steps*, *Mingus Ah Um*), plus Ballets Russes posters, a company logo and a full-score cover. Photographs that merely *mention* a title in the caption -- "Carlotta Grisi in the title role" -- keep their card, since the caption is answer-side.
- **Two gaps in the Photography canon**, found while spot-checking: the deck has *Bratislava* Tank Man but not the Tiananmen one, and no *Lunch atop a Skyscraper*.
- Not done, at Carter's instruction: adding drama to Performing Arts. The deck covers dance (138), musical theatre (98) and jazz (86) and contains no Ibsen, Chekhov, Beckett, Stanislavski, kabuki, noh or commedia; Brecht appears once, through *The Threepenny Opera*. Recording it here as a deliberate scope decision rather than an oversight.

## W96 -- Two review reports: History Clue images, Architecture figure size (2026-09-24)
- **Carter: "the history images are a bit weird - like there is images of rammed earth after a bunch of unrelated cards, whats the rationale behind that?"** The answer itself is sound -- "rammed earth" (*hangtu*) is a real Chinese-history answer line, clued off Xia and Erlitou wall construction. **The image is the problem: History Clue images are keyed to the note's Entity, not its Answer, and are reused across every clue about that entity.** 93 distinct images cover 299 notes; `histim-hist_HanWall.jpg` appears on 23 different cards, `histim-hist_Confucius.jpg` on 13, and the Erlitou site photo on four, one of which is the rammed-earth card. So a construction-technique question is illustrated with a photograph of a site. Worse for learning than for tidiness: a picture that recurs on 23 cards stops being information and becomes a cue for "this is a Han question", which can be answered from the picture without knowing the answer. **Not yet fixed** -- options are a per-answer image, or dropping the image where it illustrates only the topic.
- **Carter: "the architecture deck can be a bit hard on the eyes, idk if some of the images are just a bit too big"**. Real, and caused by W94. `.arch-concept-figs` gives every image a fixed `height: 260px`, and the generous `:only-child` rule stops applying as soon as there is more than one picture -- so raising 35 notes from one picture to four made them wrap into two 260px rows, about 600px of images above the definition. Figure height now steps down with the count (215px at two, 180px at three, 150px at four, 135px under 560px wide), with captions shrinking at four.

## W97 -- Tier gating: my new cards were breaking it (2026-09-24)
- **Carter: "currently i have tiers 2-4 suspended. i need to learn tier 1 before i learn the rest."** The gating was already his; the breakage was mine. **1,877 cards added tonight were unsuspended**, and most carried no tier tag at all (71 Art terms, 118 Art figures, 37 Architecture terms, 38 Film director notes) or a blanket tier2 I had applied because the deck was new (250 Film works). All of them would have entered a queue meant to be tier1 only.
- Fixed in two steps. **First**, every card added tonight that was not on a note already tagged tier1-core was suspended -- 1,720 of them, leaving 157 active. **Then** the 553 untagged notes and the 250 blanket-tagged Film works were given a real tier, and only the tier1 ones unsuspended:

  | batch | tier1 | tier2 | tier3 |
  |---|---|---|---|
  | Art concept terms | 18 | 31 | 22 |
  | Architecture concept terms | 14 | 12 | 11 |
  | Art Figure biographies | 0 | 52 | 66 |
  | Film | 77 | 191 | 20 |

  Rule used: **tier1 is tight.** Anything I was unsure about went to tier2, because the cost of a wrong tier1 is drilling something rare ahead of something core, which is the problem being solved. The Art Figure notes get no tier1 at all -- an artist who had no card in a 4,600-note Art deck before tonight is by definition not core; pre-1900 names any art-history set expects went to tier2, the living and recent mostly-British names to tier3. 271 cards became active, so tonight's additions now contribute 428 active cards rather than 1,877.
- **Two pre-existing holes in the gating, not caused by tonight**, found while verifying:
  1. **182 non-tier1 cards were already unsuspended** -- History 136 (the Spring and Autumn / Zuo Zhuan clue cards), Art 23 (Abramović performance works), Architecture 23.
  2. **Geography has no tier tags at all.** 2,110 of its 2,113 cards are active, which is more active cards than any deck except Art. Tier gating currently does nothing for the largest active block in the collection. Left alone deliberately -- it may be intentional, since a map card arguably is always core -- but flagged as Carter's call.
- Active cards per deck after the fix: Art 3,239 · Geography 2,110 · Photography 306 · Classical Music 300 · History 260 · Architecture 221 · Film 214 · Performing Arts 173.

## W98 — card-type pruning: Architecture and Geography

Two questions, both answered by suspending rather than deleting, so either is one
search-and-unsuspend away from being undone.

**Architecture** — "cards that ask for the name, location, architect, and style.
is that overkill?" Yes, by two of four. Suspended:

| template | cards | was active |
|---|---|---|
| PICTURE and NAME to LOCATION | 298 | 29 |
| PICTURE and NAME to STYLE | 278 | 27 |

Kept PICTURE to NAME (379), WORK to ARCHITECT (266), DEFINITION to NAME (296).
Reason: those three are the three things quizbowl actually asks for. Location is
a *clue* in a tossup, never the answer, and both suspended cards hand you the
building's name before asking, so they test a fact you have already been told the
owner of. Style is worth knowing but belongs on the 62 Style notes, where it is
the answer, not appended to each of 380 buildings.
Architecture active cards 221 -> 165; deck total 1,517 -> 941 live.
Undo: `note:Architecture card:"PICTURE and NAME to LOCATION"` -> unsuspend.

**Geography** — "is it really worth my time to be studying the flags of all the
indian states or japanese prefectures?" The premise was off: there are 3 Indian
subdivision flags and 3 Japanese, because most of those subdivisions have no
official flag. The bulk is European and Latin American — France 21, Italy 17,
Mexico 14, Canada 11, Australia 10, Germany 8, Spain 7, Brazil 7.

Suspended FLAG to NAME on all 107 subdivision/US-state notes, then, on Carter's
instruction ("just keep the canadian province/territory flags"), unsuspended the
11 Canadian ones. 96 suspended, 274 flag cards still live (206 countries, plus
dependencies, partially recognised states, SARs and historical regions).

That unsuspend surfaced a real gap: **Newfoundland and Labrador and Yukon had no
note at all** — "Yukon" was in the deck only as the river — so a set he is meant
to know cold was missing 2 of 13. Added both (`geo_canada_missing.py`) to the
Manitoba pattern: P242 locator map at 3000px, P41 flag, one landmark photo
(Cabot Tower on Signal Hill; Mount Logan), seat, and the three Geo:: tags. Yukon
needed `allowDuplicate` against the river, which is the deck's existing situation
with Niger. All five images were checked on a contact sheet before applying, and
the three unused Newfoundland candidates were deleted from collection.media.

Geography active cards 2,110 -> 1,881.

**Closed:** I offered to tier Geography, since it is the only deck with no tier
tags at all (1,881 of 1,896 cards active). Carter declined, and the reason is a
standing one: "no geo tiers; the world is not more or less important that
others." The tier scheme ranks how often a thing comes up, which is reasonable
for artworks and films and is not something he wants applied to places. Do not
re-offer. Pruning Geography on the strength of a *card type* is still fine --
that is what the subdivision flags were -- but not on the importance of a place.

## W99 — four-deck audit: Film, Performing Arts, Photography, Architecture

Carter: "inspect the film, PA, photography, and architecture decks (across all
elements: aesthetics, canon, layout, amount of information, card type, others,
etc.) to ensure that they are optimal for studying quizbowl and for learning."

**Method note, because it nearly produced three wrong findings.** A leak check
that feeds it every field on a note reports leaks that cannot happen. Photography
looked like it had 316 leaks; the fronts of those cards print only the title, or
only the photograph, so the real number was 11. Architecture looked like 676; its
DEFINITION card is gated on `{{#Kind}}` and buildings have no Kind, so 116 of
those notes have no such card, and the front's `{{Name}}` sits inside a
`display:none` div the caption script reads. The check now strips hidden divs and
uses only fields the template actually prints. **Read the template before
believing a leak count.** Of the leaks that survived, most were already
suppressed by TitleTells — the machinery was in use and the audit had not
accounted for it.

Fixed: 4 self-answering cards suppressed (Les Sylphides, Hubble Deep Field,
STS-31 Crew Portrait, Ken Moody and Robert Sherman); 2 clues rewritten that named
their answer inside a coined term (Labanotation -> Laban, Denishawn -> St. Denis);
10 Architecture Figure notes had no tier tag at all, so the gate could not see
them — tiered (Michelangelo, Utzon, Jefferson, Van Alen core; the rest solid) and
the non-core ones suspended.

**Film stills: the gap cannot be closed from Wikimedia.** 122 of 250 films carry
no still, including 17 of the 77 tier1 films, against Carter's standing "at least
2" requirement. Cause is structural, not a bug: film stills are in copyright, so
Commons holds them only where the film is public domain or a US trailer lapsed. A
search across the 39 short tier1 films returned 55 candidates, of which about 8
were real — "Chinatown" returned a photograph of a Chinatown, "Wild Strawberries"
fruit still-lifes, "Blue Velvet" magnolias, "Oppenheimer" two unrelated men of
that name. Batch not applied. This needs a TMDB key, which is still outstanding.

**Photography canon is the biggest real defect.** Of 434 work notes, a large
group are news photographs carrying a descriptive label rather than a title —
"Aida" (the name of a wounded girl), "Climate Change" (a polar bear), "Fashion
Week", "Snow", "Brussels", "Homecoming", "Bricklayer", "The Hague", "Air Jordan".
Two of the three cards on those notes ask for, or from, that label, and neither
is answerable. `TitleGeneric` exists for exactly this and is set on 1 note of 434.
Not yet fixed: needs a judged list, not a regex.

**Canon otherwise checks out.** Film tier1 is 64% pre-1970 with 10 silent films
and one film from the 2020s; 60% of the deck is non-US. PA tier1 is sound.

**Still open:** PA is the one deck that never got the multi-image treatment —
every one of its 322 notes has exactly one picture, and 3 works have none.

## W100 — Photography title triage, then Performing Arts galleries

**Photography.** Read all 434 work titles and sorted them into three classes.
78 are GENERIC: a caption filed as a title, where neither title card is
answerable — "Aida" (the name of a wounded girl), "Climate Change" (a polar
bear), "Fashion Week", "Snow", "Brussels", "Homecoming", "The Hague", "Air
Jordan". Both title cards off; the note keeps PHOTOGRAPH to PHOTOGRAPHER, which
was always the card doing the work. 64 are EVENT: they name a real historical
event, so PHOTOGRAPH to TITLE stays (recognising the event from the image is
worth having) and TITLE to PHOTOGRAPHER goes, because who shot it is arbitrary.
292 are real titled works and were not touched.

Doubtful cases were left alone on purpose, since suppressing is the change:
"Bliss" is genuinely the name of the Windows XP wallpaper, Sander titled
"Bricklayer" and "Young Farmers", and "Tereska" is how that picture is indexed.

TitleGeneric 1 -> 79, TitleTells 7 -> 151. **Tools -> Empty Cards removes 230
cards**; Photography 1,325 -> ~1,095.

**Performing Arts.** The deck had one picture per note and one caption printed
under all of them, so extra pictures had nowhere to go. Ported the Art/
Photography mechanism — a pipe-separated Captions field, a hidden data div and
the qb-caps script that pairs the nth caption to the nth image — and migrated the
302 existing single captions into it.

Then a design error of mine, caught on the first contact sheet: extras must not
go into Media, because every image in Media prints on the MEDIA to NAME *front*,
which shows a picture and asks what it is. The media-list for "Maple Leaf Rag"
returns its sheet-music cover with Joplin's name in type and "Take Five" returns
the Columbia 45 label. So extras live in **Gallery / Gallery captions, rendered
on backs only**, and Media keeps the single picture that is the prompt.

Second pass fixed two more faults the sheets showed. "Camelot" had returned
Doré's Arthurian castle because the musical lives at "Camelot (musical)" — the
disambiguated title, built from the note's own Form and Discipline, is now tried
first and the bare title only as a fallback. Brecht had returned the Brechthaus
and his Santa Monica bungalow, the memorabilia failure from the Art pass, now
filtered unless the note is about a venue.

145 candidates over 5 sheets, 23 struck off by eye (Romani families for "Gypsy",
signatures for Baker/Bernstein/Rivera, a commemorative coin for Romeo and Juliet,
theatre marquees, a newspaper column about Armstrong's arrest as a boy).
**56 of the 72 tier1 notes now carry 2-4 pictures; 122 images, 112 captioned**
(36 of those from the Commons filename where the media-list gave none).

Not done: the 16 tier1 notes Wikipedia had nothing extra for, and tiers 2-4
(250 notes). Same scripts, `py -3.9 pa_gallery2.py tier2-solid`.

## W101 — caption hygiene, and two wordings on Architecture cards

Carter, reading the Islamic architecture card: "Oxford comma timber framing /
Islamic architecture described a 'Muslim'... / faulty captions: either very long,
contain met-data (like [25]), etc."

**Captions.** All three faults traced to one source: the captions were taken from
Wikipedia's media-list, which hands back the article's own caption HTML. So the
footnote markers came with it, and so did paragraphs written to sit beside a body
of text rather than under a thumbnail. The worst was an Art caption of 1,131
characters; another carried a raw `.mw-parser-output` CSS rule where a fraction
should have rendered.

`caption_clean.py` swept all 4,503 captions in six decks: reference markers
removed, leftover MediaWiki CSS and its empty spans removed, and anything over
130 characters cut back to its first sentence -- or, where the first sentence was
itself over 160, cut at a word boundary with an ellipsis. Italics are preserved
and any tag the cut left open is closed again. 97 notes changed: Film 42, Art 30,
Architecture 19, PA 4, Photography 2, Geography 0. Verified afterwards: 0 markers,
0 over 170 characters, 0 occurrences of mw-parser-output anywhere in the
collection.

Captions that were already short and clean were not touched -- this was not a
rewrite for style.

**Timber framing**, Oxford comma: "filled by wattle and daub, plaster or brick"
-> "...plaster, or brick". The serial comma is doing real work here, because
"wattle and daub" already contains an "and" and without it the list reads as two
items.

**Islamic architecture** had opened "The building tradition of the Muslim
world", which defines the tradition by the faith of the people living under it --
the standard objection to the phrase, since the same tradition built markets,
palaces, synagogues and churches. Recast to "the societies shaped by the faith
Muhammad preached -- its palaces, markets and tombs as much as its mosques".
Note this card cannot simply say "the Islamic world": the answer is *Islamic
architecture*, so that phrasing would answer the card, which is why the original
reached for "Muslim" in the first place. Re-checked with `leaks()`: clean.

## W102 — tier gate enforced; Art deck audit

**1. Tier gate.** 199 cards were active despite carrying tier2/3/4 tags —
History 153 (tier3 Chinese mythology and prehistory: Nüwa, Shennong,
Zhoukoudian, Yangshao), Art 23, Architecture 23. All predate tonight; they were
tiered at some point and never suspended. Suspended. Every deck except Geography
is now tier1-only in the queue, which is the gate Carter asked for; Geography
stays ungated by his decision (W98).

Active after: Art 3,216 | Geography 2,018 | Classical Music 300 | Photography 227
| Film 214 | Performing Arts 173 | Architecture 136 | History 107.

**2. Art audit.** 4,891 notes (4,591 artworks), 14,238 cards, 3,216 active —
by far the largest deck, and the only major one never inspected.

*The headline: the deck has no content.* `Notes` is empty on 4,590 of the 4,591
artwork notes and only 92 carry a `Clue`. So ~4,500 works are image + title +
artist + date + location and nothing else. Compare the other decks' back text:
Film 433 characters median, Architecture 177, Photography 112, Art effectively 0.
The deck trains recognition and teaches nothing about why any of it matters,
which is the half quizbowl actually rewards — tossup clues are content.

*Second: ARTWORK to TITLE never showed the artist.* Its back printed the picture
and the title and stopped, so the most-reviewed card in the collection let you
answer "The Night Watch" without ever being shown Rembrandt. Fixed — artist and
date now sit under the title, in #6b4c3b because Art's dark mode works by
matching its 55 hardcoded inline colours with attribute selectors
(`.night_mode [style*="#6b4c3b"]`), and a new colour would have no such rule.

*Card shape:* three cards per artwork at 3.0 active cards per tier1 note, two of
them answering "artist" (ARTWORK to ARTIST and TITLE to ARTIST). Not recommending
a cut yet — with the artist now on the title card's back, the honest next
question is whether ARTWORK to ARTIST still earns its 991 active cards, and that
is worth deciding after Carter has seen the changed card.

*Clean:* title hygiene is good (TitleShared 324, TitleGeneric 16, TitleTells 28,
Anon 54), so the duplicate-title problem Photography had is already handled here.
Only 17 artworks lack an image and none are tier1. Dark mode works.

*Fixed:* 5 clues that used the title's own words — Painted Bronze ("painted"),
Watson and the Shark ("shark"), Early Sunday Morning ("morning"), The Death of
General Wolfe ("general"), Cut Piece ("cut"). Two left alone: L.H.O.O.Q. cannot
be described without its moustache and its primary title is not given away.

## W103 — Performing Arts galleries, tiers 2-4

The first tier2-4 pass was wrong and was thrown away. Its contact sheets showed
the article lookup failing in a block: **Cabaret, Carousel, Cats, Chicago and
Company** all returned their literal meanings -- fairground carousels, three
domestic cats, the Chicago skyline and the L train, Toulouse-Lautrec's dance
halls -- and "Arabesque" returned Islamic ornament instead of the ballet
position. Cause was mechanical: the disambiguator was built from the note's Form,
and this deck's Forms are "Book musical" and "Concept musical", so the lookup
asked for `Cats (book musical)`, got nothing, and fell back to the bare title.
Wikipedia's actual disambiguator is `(musical)`.

`pa_gallery3.py` rebuilds it with two changes. Form and Discipline now map onto
the disambiguators Wikipedia really uses -- musical, ballet, opera, operetta,
album, song, ballet position -- and, as a second line of defence, **the resolved
article must prove itself**: its own summary has to mention the note's domain, so
"Cats" the animal is rejected and the note is left bare rather than given a wrong
picture. 51 notes now land on a correctly disambiguated article, including Rodeo,
Serenade, Jewels, Manon, Petrushka, Apollo and Kind of Blue.

Fixing that immediately exposed a fault in the fix: Bill Evans resolved to
*Bill Evans (choreographer)*. Works carry common-noun names and need
disambiguating first; people do not, so for Figure notes the bare name is tried
first and the qualifiers are the fallback.

513 candidates over eleven sheets, 41 struck off by eye — theatre marquees for
The Producers, The Book of Mormon, Spring Awakening, Miss Saigon and The Sound of
Music; a trumpeter filed under the pianists Bill Evans and Bud Powell and two men
under the singer Anita O'Day; houses for Roy Eldridge, Sidney Bechet and Bix
Beiderbecke, Walk of Fame stars for Scott Joplin, a Jaco Pastorius bass
sculpture; a character-relationship diagram for Mayerling.

**278 of 322 PA notes now carry a gallery, 594 images, 559 captioned.**

Three works still have no picture at all — Rodeo, The Green Table, Alice's
Adventures in Wonderland. A targeted fetch with every filter switched off
returned zero candidates: those articles carry no free images. Modern ballet
production photography is in copyright, the same wall the film stills hit. These
three generate no MEDIA to NAME card and will not until there is another source.

## W104 — 50 sample clues for tier1 artworks

Carter asked whether the Art content gap was worth filling. Checking the
templates before answering changed the answer, and it is worth recording why.

**My original proposal was the wrong shape.** I had offered to write `Notes` for
1,069 tier1 artworks. But `Notes` prints on only one of the three artwork cards
(TITLE to ARTIST), so that work would have produced prose on one back, to be read
passively, never tested. `Clue` is the field that matters: it is the entire front
of DESCRIPTION to TITLE, so writing one *creates a card* that tests the quizbowl
motion -- hear the work described, name it. Only 72 of 997 tier1 artworks had one.

**And 1,069 was the wrong number.** Writing a thousand art-historical claims is a
thousand chances to be confidently wrong with no way for Carter to spot the bad
ones. Agreed scope: 50 now as a sample, ~150-200 if he likes them.

Each clue was written against the work's own article summary, fetched first
(`art_clues_fetch.py`), rather than recalled, and skewed toward what a question
would actually say -- the suffragette who slashed the Velazquez in 1914, the US
customs case that taxed the Brancusi as a manufactured metal object, the
anamorphic skull in the Holbein, the self-portrait in Goliath's severed head, the
critic's sneer that named Impressionism.

All 50 matched a deck note, **0 rejected by the leak check**, median length 139
characters. DESCRIPTION to TITLE: 92 -> 142 cards, 72 -> 122 active, all on tier1
notes, so nothing entered the queue that the gate should have kept out.

Worth noting where this pays most: the deck holds four works called *David*, four
called *The Kiss*, five called *The Last Supper* and four called *The Dance*. The
picture card cannot tell Rodin's Kiss from Klimt's. The clue can, and now does.

## W105 — History images rekeyed to the answer; 50 Art clues reverted

**History.** Carter, earlier: "the history images are a bit weird - like there is
images of rammed earth after a bunch of unrelated cards, whats the rationale
behind that?" There was none. The Image field on the 331 History Clue notes was
keyed to the note's *Entity* -- its topic -- rather than its Answer:

    histim-hist_hanwall.jpg    23 cards  Feast at Hong Gate, the Xiongnu,
                                         the Discourses on Salt and Iron ...
    histim-hist_confucius.jpg  13 cards  ren, li, the junzi, the Analects
    histim-hist_mapwarring.jpg 12 cards  hezong, lianheng, Bai Qi
    histim-hist_daisen.jpg     11 cards  every Kofun-period question

93 images over 299 cards. Not merely decorative: a Great Wall photograph beside
"Discourses on Salt and Iron" teaches an association that is false.

The image renders on the back only, so illustrating the *answer* is safe. Each
answer was resolved to its own article and given that article's lead image.

**The first attempt rebuilt the bug in a new form and had to be caught.** A plain
Wikipedia search for the answer returns whatever is nearby: "An Lushan" resolved
to Mount Lu, "Autumn Meditations" to Chinese martial arts, and the date range
"690-705" to a portrait of Wu Zetian -- which is entity-keying again, one step
removed. The resolved article must now actually match the answer, and bare dates
are refused outright. That dropped the hit rate from 38/40 to 17/40 on the probe,
which is the honest number.

Six images arrived solid black: transparent PNGs of Chinese characters -- tianming
for the Mandate of Heaven, the titles of the Four Books -- flattened onto JPEG.
Found by measuring every image's mean luminance rather than trusting the eye
across 205 thumbnails, and recovered by compositing onto white.

Reviewed on five contact sheets; one rejection, Mawei, where the search found the
modern district of Fuzhou rather than the post station where Yang Guifei died.

**204 cards now carry a picture of their own answer; 114 had a wrong one cleared.**
Abstractions get nothing, deliberately -- ren, li, the junzi, "Rihaku",
"Xuanzong's own son" -- because a blank beats a misleading picture.

    before   93 distinct images over 299 cards, one used 23 times
    after   200 distinct images over 204 cards, most reused twice

**Art.** The 50 clues of W104 were reverted. Carter: "I'd rather only have
descriptions for things that need it like ancient artifacts and confusing things
or installations and performances ... I don't just want explanation for the sake
of it", and separately that he wants "facts that say things that I can't tell by
looking at the painting", without poetic phrasing. The 50 were visual
descriptions of self-evident paintings -- the opposite on both counts. Texts kept
in art_clues_write.py; the emptied cards go on the next Empty Cards.

Proposed instead and **awaiting his word**: plain factual context in `Notes`, not
`Clue`, since this is reference to read rather than a card to answer; chosen by
hand, not by rule (a mechanical filter caught Frida Kahlo and Remington's Bronco
Buster, which need no explaining); on the ~80-120 works that fail the test
"would someone looking straight at this still get it wrong without this fact?"

## W106 — Geography maps: legibility and context

**Two-map system for subdivisions.** Carter: "the entities are so hard to parse
in relation to the overall country. Eg guizhou is so zoomed in." True of most:
the P242 locator maps frame a province on its immediate neighbours. Wikipedia
carries whole-country locators under a few naming conventions
(`Yunnan_in_China.svg`, `Tuscany_in_Italy.svg`, `Locator_map_Bavaria_in_Germany.svg`);
resolved 181 of 226, rejected 7 by eye, **applied 174** as a second image in both
Map and Map Labeled, which the deck's CSS already lays out side by side.

Gaps are mostly city-states (Berlin, Delhi, Moscow), defunct entities
(Württemberg-Baden, pre-2016 French regions) and remote territories.

**India restyled.** Carter: "The Indian map of that style (the dark grey one)
sucks". The `IN-XX.svg` series is dark grey with a red state; swapped all 33 to
`India <State> locator map.svg` — cream country, orange neighbours, blue sea,
matching the rest of the deck.

**Andhra Pradesh.** Carter: "the map of India doesn't have telangana on it lol".
Telangana's own map was fine. Andhra's was drawn on black *and* pre-2014, with
Telangana still inside it. Swapped to the claims-hatched series. A luminance
check over all 181 locators found only 5 dark backgrounds, 4 of them already
rejected.

**US states.** Carter: "Us states still render as light grey over blue background
and is hard to see." Not the template: the 50 files in Map Wide are transparent
PNGs and the deck's CSS paints `background: #c6ecff` behind map images, so light
grey states sat on pale blue. Highlight colour was inconsistent too (Nevada blue,
Texas yellow). All 50 flattened onto white with the highlight normalised to the
deck's red. Map Wide kept, because these *are* the whole-country view he wants.

**Mexico City.** Carter: "Entity to the right of state of Mexico not labelled."
The State of Mexico wraps around it and the source map labels every neighbour
except that enclave. Labelled on both maps.

**Kuril Islands.** Carter: "Kuril islands label disappears upon Hokkaido reveal."
Confirmed: the labelled render moves "Kunashir Island" into the space "Kuril
Islands" occupied and drops the latter, so a feature named on the question side
vanishes on the answer side. Restored in the map's own italic-with-halo style.

**Hawaii.** Added the eight main islands (`geo_hawaii.py`) to the shape of the
deck's existing island notes, all sharing the "Map of Hawaii highlighting X"
locator so the chain is visible. Two photos were wrong on first fetch -- Oahu
returned none and Lanai a relief map -- refetched, and the captions corrected to
match what the photographs actually show.

**Could not reproduce.** Carter reported that the Liaoning note "removes labels
from front to back" and that North Korea is "grey in the front map but cream in
the back". Pixel comparison: `geofront-liaoning` and `geolab-liaoning` are
identical except for a 168x46 box, which is the word "Liaoning" -- 0.21% of the
image. North Korea is (199,199,192) grey in both, and the China locator greys
foreign countries the same way. Needs a screenshot to go further.

**Open, not yet done:** 72 maps that are >85% open sea and give no sense of
location (Wallis and Futuna, Northern Mariana Islands, American Samoa and the
rest) -- the fix is the Commons "X on the globe (small islands magnified)"
series as a second map; Bohemia's borders; the Lena unlabelled on the Laptev Sea;
Niger's front/back aspect mismatch (the only one in the deck); real photographs
after reveal; and 29 NAQT You Gotta Know items missing.

**NAQT coverage** (7 geography lists, 89 items): Asian rivers 10/10, deserts
9/12, mountains 9/10, African bodies of water 16/23, North American rivers 7/13,
active volcanoes 5/10, western European rivers 4/11. Note the deck files rivers
source-to-mouth ("Nile – Kagera", "Padma – Ganges"), which the first check
mis-scored as missing.

## W107 — the map backlog, NAQT coverage, Hawaii, Oxford commas

**One-offs.**
*Nunavut* ("so ugly"): the detail map washed the Arctic archipelago out in pale
pink against a grey United States and Greenland. Dropped it; the country locator
beside it is clean, and a labelled copy was stamped for the back.
*Niger*: the country note and the river note **shared one labelled map**, the
river's, so the country's answer side showed a different subject from its
question side. Gave the country its own, stamped from its own front map. A scan
found this was the only such collision in the deck.
*Lena* ("not labelled on laptev sea"): true, and the map labels the Olenekskaya
Protoka, which is one of the Lena's own distributaries. Added in the map's water
style.
*Bohemia* ("still confusing"): the source map never draws the Czech Republic's
border, so the highlight could be the whole country and Moravia was a floating
label. Added the Czech lands map to the back only -- it prints the word
"Bohemia", so on the front it would be the answer. Also applied to Moravia and
Silesia.

**Ocean-filled maps.** Wallis and Futuna is 99% open sea with two circled specks
and an inset that is itself empty blue. 72 maps are >85% sea. Added the Commons
"on the globe (small islands magnified)" series as a second map to **44** of
them, after excluding places that need no help (Chile, New Zealand, Malta) and
the Hawaiian islands, whose maps already show the chain. All 44 arrived on a
black background and were converted to white.

**NAQT You Gotta Know, all seven geography lists: 0 missing.** Added 29 notes
with maps and photographs. Three maps the picker chose were wrong and were
replaced or dropped -- the Negev got a 19th-century Palmer survey map, the Rhine
an annual-discharge chart of the Dutch delta, and the Suez Canal a map of the
*ancient* Canal of the Pharaohs. Coverage before: volcanoes 5/10, western
European rivers 4/11, North American rivers 7/13.

**Oxford commas.** Carter, on Bali: "tut tut tut". Its Info also ran two bullets
together and said "volcano" twice; rewritten as two bullets. A first detector
flagged 272 notes, most not lists at all ("a flat state, bounded by the
Mississippi and the Ohio" has one comma and an "and" but two items), so items
must now be short noun phrases free of clause words. **45 notes** fixed.

**My own bug, caught by Carter.** "Why is there three odisha maps now?" The back
renders Map Wide *and* Map Labeled, and 33 Indian subdivisions already carried a
whole-India locator in Map Wide -- so the country locator I added made three. The
deck's `geohq-` series was there all along and the India work was never needed.
Removed my `geoctry-` image from all 33. No subdivision now shows more than two.

**Running:** photographs for the answer side of the 541 notes that have none.
Skipping sea, ocean, gulf, strait and estuary, where a photograph of open water
identifies nothing -- the "don't just add images for the sake of it" half.

## W108 — photographs on the answer side of Geography

Carter: "Add more images after reveal (like real images of the actual place, that
add substantial value (don't just add images for the sake of it)) to places".

541 notes had no photograph. **275 now do**, taking Geography from 559 to 834 of
1,100. The Image field already renders on the back only, so this is purely the
answer side.

**Kinds skipped on purpose.** Sea, ocean, gulf, strait and estuary get nothing: a
photograph of open water does not identify which water it is. Historical regions
and states were dropped after the first pass, because a place that no longer
exists cannot be photographed and its article offers maps, portraits and
paintings instead -- the re-picker gave the Weimar Republic Max Ernst's *The
Elephant Celebes*, the Republic of Texas a London wine merchant, and the Holy
Roman Empire a 1572 town view.

**Three passes, because filters were not enough.**
1. Article lead images: about a third were paintings, engravings or 19th-century
   photographs. US state articles are the worst, opening on their history.
2. A filename filter plus a **saturation test** on the downloaded file -- an
   engraving or a historical photograph is nearly greyscale. That caught 122.
   A date in the filename had to be dropped as evidence: "1997 Agadez mosque" is
   a photograph.
3. The suspect test then had to check the *reject* pattern too, not just the
   "arty" one: "The Death of General Wolfe" contains no word like "painting", so
   Canada kept its battle scene through the first re-pick.

**Then 91 of 366 were struck off by eye across seven contact sheets**, which is
what the filters could never do: a Putin handshake for Cuba and again for Russia,
an electricity generation chart for El Salvador, a nuclear test for the Marshall
Islands, a supermarket aisle for Kiribati, a city bus for Rhode Island, a gas
pipeline for South Ossetia, a fish for Lake Biwa, antelopes for Uganda, twelve
lakes that returned maps, and a street sign reading "Rue des Nègres" for the
Negro river.

Nothing was substituted for a rejected image. A note with no photograph is the
right outcome when no photograph of the place exists, which is the "don't just
add images for the sake of it" half of the instruction.

## W109 — context notes on the Art works that need them

Carter approved the reshaped version of W104: plain factual context in `Notes`
rather than clues in `Clue`, on the works where meaning is not visible, written
by hand rather than by rule.

**104 notes applied**, median 187 characters. They render on the back of all
three artwork cards since the W102 template fix, generate no card, and are
therefore reference rather than a test.

Selection was by one question -- would someone looking straight at the image
still get this wrong without the fact? Three things trigger it: the object's
function is not visible, the work is an idea rather than a picture, or the
subject cannot be identified by sight. Nothing here narrates the picture, which
is what was wrong with the reverted W104 clues.

Written against each work's own article, fetched first (`art_notes_fetch.py`),
because a hundred art-historical claims written from memory is a hundred chances
to be quietly wrong. Nine articles returned a summary about the artist rather
than the work and were written with more care.

What they carry: the 1917 Society of Independent Artists promised to exhibit
anything submitted and rejected Fountain anyway; the Willendorf limestone is not
local to Willendorf; Étant donnés was built in secret over twenty years while
Duchamp claimed to have quit art for chess; Rodin's Balzac was refused by the
society that commissioned it and not cast until 1939; Dostoevsky saw Holbein's
dead Christ in Basel and wrote that it could make a man lose his faith; the
Colleoni monument is in the wrong square because Venice took the bequest and
ignored the condition; Salvator Mundi sold for £45 in 1958 and $450 million in
2017; Perfect Lovers is two clocks that drift apart as their batteries die.

Not done, deliberately: the other ~890 tier1 artworks. Starry Night, Las Meninas
and The Night Watch need no explaining, and adding a line to each would be
exactly the "explanation for the sake of it" Carter ruled out.

## W110 — Performing Arts: enumerations, and the missing atomic route

Carter: "a card that names all of stephen sondheim's works doesnt really help me
recall his name when only one of his lesser known works is mentioned. do some
research into learning and flashcard learning."

He had diagnosed a known failure. Wozniak's twenty rules put the **minimum
information principle** first and separately say to **avoid sets and
enumerations**, because a list is learned as a list rather than as its members;
work on cue design adds that with a repeated compound cue learners come to
recognise the first few words rather than the content. His Sondheim card names
eight works and is answered at word four.

**The measured version was worse than the complaint.** Eight active tier1
Figures were *never the answer on any active work card*:

    Sondheim  9 works credited, 0 active      Kander      2 credited, 0 active
    Coltrane  4 works credited, 0 active      Adderley    1 credited, 0 active
    Davis     3 works credited, 0 active      Ellington   1 credited, 0 active
    Balanchine 2 works credited, 0 active     Petipa      1 credited, 0 active

Sondheim's two *active* works, West Side Story and Gypsy, are credited to
Bernstein and Styne, because he wrote only their lyrics. So the bundled list was
the single place in the deck where "Stephen Sondheim" is the answer: the one card
that cannot teach the retrieval, with every card that could switched off.

**Fix 1** — promoted one signature work per figure to tier1 and unsuspended it
(Sweeney Todd, Into the Woods, A Love Supreme, Kind of Blue, Concerto Barocco,
Cabaret, Somethin' Else, Ellington at Newport, Raymonda). Figures with no atomic
route: 8 -> **0**. PA active cards 173 -> 195.

**Fix 2** — Notes was serving as both the question on CLUE to WORK and the
reference on every back, so an enumerated cue could not be trimmed without losing
the catalogue from the answer side. Added a **Clue** field; the front now prefers
it and falls back to Notes, so the 279 non-enumerated notes are untouched.
Wrote 43 clues that are one distinguishing fact rather than a list, each written
to separate its subject from the person nearest them -- Comden and Green get the
two halves of the same partnership, Lerner the words and Loewe the music, Kander
the composer and Ebb the lyricist. A clue that fits both halves of a pair is not
a clue. 0 rejected by the leak check, median 101 characters.

**Photography does not have this problem.** Zero enumerations, and it is already
atomic: one photograph, one photographer. Its weakness is the opposite -- 286 of
339 photographers appear on exactly one photograph, and 83 of 90 tier1
photographers have a single active photo, so each name is welded to one image.
Not repaired; that is expansion rather than a defect.

**Still open from this audit:** 67 works named inside Figure clues have no note
of their own.

## W111 — descriptions for the classical pieces

Carter: "could i have you give written descriptions of all the classical music
pieces so that i have the most important facts about a work and can buzz on them
in quizbowl more easily".

**281 of 281 tier1 work notes now carry one.**

Two things had to be fixed before writing. `Description` was gated on `{{#Kind}}`
and work notes have no Kind, so on all 1,430 of them it rendered nowhere -- the
text would have been invisible. Added to the back of both work cards as
reference; no new card type, since Carter had declined one for this deck.

And the 281 notes are only **149 distinct pieces**: eleven are Nutcracker
movements, ten are movements of the Brahms Requiem, eight of the Mozart Requiem.
So one description per work, applied to every note of it; the movement is already
printed separately on the card. 154 descriptions written in all.

Resolving a piece to its article was the real work. "Symphony No. 5" is useless
alone, so candidates were built from the composer's surname, the nickname and the
catalogue number, and the resolved article had to mention the surname -- otherwise
Beethoven's Fifth lands on Mahler's. 276 of 281 resolved; twelve landed on a
composer biography rather than a work and five found nothing, and those
seventeen were written by work title instead.

Written for buzzing rather than summary, so each carries what a question would
say and the card does not already show: that the Moonlight nickname came from a
critic five years after Beethoven died; that Mozart's Requiem was commissioned
anonymously by a count who meant to pass it off as his own; that Tallis's forty
voices answer an Italian model; that the celesta in the Nutcracker was smuggled
from Paris so no one would use it first; that Shostakovich's Leningrad score was
flown out of the siege as propaganda; that Smyth conducted The March of the Women
with a toothbrush from a prison window.

Not done: the other 1,149 work notes, all tier2-4 and suspended.

## W112 — tier2 classical descriptions

Same pipeline as W111, extended to tier2. **784 of 784 work notes across tier1
and tier2 now carry a description** — 281 tier1 and 503 tier2.

503 tier2 notes resolved to **265 distinct pieces**, of which several already had
a tier1 description (the Magic Flute, the Brahms Requiem, Tristan, the Barber of
Seville) and were inherited rather than rewritten. 413 descriptions in total
across both tiers.

494 of 503 resolved automatically. Six landed on a composer biography or a list
page — Schoenberg, Smetana, Scarlatti, Vaughan Williams, the Schumann Quartet,
and a page literally titled "List of compositions by Franz Liszt" — and four
found nothing, so those ten were written by work title. One key needed both
spellings because the Work field stores its ampersand as `&amp;`.

Same rule throughout: what a question says, not what the card already shows. The
Waldstein's discarded slow movement published separately as the Andante favori;
Diabelli sending a trivial waltz to fifty composers and Beethoven answering with
thirty-three; the Tannhäuser Paris riot caused by moving the ballet to Act I so
the Jockey Club arrived too late for it; Rubinstein calling Tchaikovsky's first
concerto worthless and unplayable; Haydn writing the Nelson Mass without wind
because his patron had dismissed the players; Sibelius finding the finale of the
Fifth in sixteen swans taking off.

Not done: the 646 tier3 and tier4 work notes, all suspended.

## W113 — Architecture rebuilt around how architects are actually clued

Carter: "the vast majority of architecture tossups are about a specific
architect, where it successively clues their works... frank lloyd wright is the
most common qbreader architect and he has tons of tossups about particular
works."

**The orphan test first.** The same check that found eight unreachable figures in
Performing Arts found twelve here: Brunelleschi, Alberti, Palladio, Borromini,
Gaudí, Gropius, Kahn, Hadid, Gehry, Pei, Sinan and Jefferson were **never the
answer on any active card**. Every building credited to them sat suspended at
tier2-4. Promoted one signature work each: 12 -> 0.

**Then the coverage problem Carter named.** 25 tier1 architects held a median of
two buildings and 22 active between all of them, so a tossup naming four works
would meet at most one the deck had ever shown. The works were mostly not
missing -- Robie House, the Guggenheim, Johnson Wax, Unity Temple, the Barcelona
Pavilion, Farnsworth, Casa Batlló and Sant'Ivo were all present and all
suspended. Promoted 38.

**Then Carter corrected the promotion, rightly.** "the art deck prioritizes
individual works that are the best known work of a more obscure artist (the
'pavlov' method) over the tenth most popular work of a very popular artist."
Blanket-promoting everything by a famous architect breaks that rule exactly.
Pulled seven back down: La Tourette, Yale Center for British Art, Villa
Tugendhat, Taliesin West, Johnson Wax, Guangzhou Opera House, Sant'Andrea al
Quirinale.

**Then the genuine gaps.** 26 buildings added, each tiered by **its own**
canonicity rather than its architect's: Teatro Olimpico, St Peter's Square, the
Guaranty Building and Djoser's Step Pyramid at tier1; the Imperial Hotel, Larkin,
Taliesin, Greenwich, San Lorenzo and the NGA East Building at tier2; Hollyhock,
Price Tower, Marin County, the Sheldonian, the Monument, St Stephen Walbrook,
Sant'Agnese, MAXXI, Vitra, Casa Vicens and the rest at tier3.

Buildings 380 -> 406. Architecture active cards 136 -> 319. Wright 6 -> 12 in the
deck. Wren 1 -> 5.

**Image quality**, which Carter asked for explicitly: 48 fetched, 13 rejected by
eye -- a bronze plaque for the Auditorium Building, portraits of Gaudí and Morris
in place of their houses, a wooden *model* of Hollyhock House, the modern
Imperial Hotel rather than Wright's demolished one, a statue of Djoser rather
than his pyramid, a section drawing of the Teatro Olimpico. Three works whose
articles gave nothing usable were filled from a Commons search. No note was left
imageless.

## W114 — testing the deck against real questions

Carter: "do some more testing around with your new deck to try to confirm its
effectiveness."

Tested against qbreader's public API rather than my own judgement: **1,013 real
Architecture tossups**, pulled with their answer lines, full text and each set's
difficulty grade.

**Baseline.** Of the answers those tossups ask for, 76% were somewhere in the
deck and 53% on an active card; on a held-out pull the honest figure was 62%
in-deck. So roughly a quarter of real Architecture answers the deck simply does
not contain, and a further slice was buried below tier1.

**Two mistakes I made and corrected, both caught by Carter.**

First I promoted every note that answered any tossup -- 56 of them -- which is
exactly the "everything in tier1" failure he warned about: Ryugyong Hotel and
Gando Primary School are not core on a single appearance. Reverted all 56.

Then the matcher itself was wrong. Fifteen cathedrals scored *identically* --
4.61, six answers each -- because short generic names were matching one another
through shared words like "cathedral" and "dom". A match must now share a
non-generic token; scored notes fell 532 -> 455 and the phantom block vanished.
Had I applied the loose rule, fifteen cathedrals would have entered tier1 on
evidence that did not exist.

**The model Carter specified**, using all three signals he named:

    frequency   how often it is the answer, as a share of the sample
    difficulty  qbreader grades sets 1-10; answering a difficulty-4 tossup is
                worth far more than answering a difficulty-9 one
    position    where in the tossup it is named -- a pyramidal question runs
                obscure to obvious, so a lead-in mention is a deep cut and a
                mention in the last quarter is the giveaway

Being the answer is weighted far above being mentioned. Top of the ranking comes
out as Frank Lloyd Wright (47 answers at difficulty 4.3), Pei, Le Corbusier,
Gehry, Saarinen -- which matches Carter's own statement that Wright is the most
common qbreader architect.

**Applied: seven promotions**, each answering six or more real tossups in sets
easy enough to count as core. Tower of London answers thirteen at an average
difficulty of 3.9, high-school level, and was sitting at **tier4**. The loose
rule would have promoted 108; this promoted 7, and tier1 went 174 -> 181.

**Deliberately not demoted:** 20 tier1 notes never appeared in the sample --
Karnak, Delphi, Knossos, Hadrian's Wall, the Moscow Kremlin, Borromini, Sinan.
They are clued in History and Geography tossups, not Architecture ones, so
absence from this subcategory is not evidence against them.

## W115 — Classical Music: making the audio load-bearing (2026-09-25)

Carter: "i know almost nothing about classical music. i am essentially just
associating the names of pieces with artists... they all sound the same to me. is
this just a matter of time on task?"

It is not time on task. Two measured causes, neither fixed by more drilling.

**The deck never asked him to listen.** `AUDIO to COMPOSER` — audio alone on the
front — had 1,428 cards and **0 active**. The only active work card was
`AUDIO and WORK to COMPOSER`, which prints the title beside the player, so the
title alone answers it. Every correct answer he has ever given on this deck was
given by reading. A cue that is never required is never encoded.

**The queue massed composers.** Measured on the live new queue: mean run 2.1
consecutive cards by the same composer, **longest run 20** — twenty Beethovens,
then four Chopins. Massing is what makes everything sound the same; hearing
twenty Beethovens in a row teaches the sound of "orchestra". Interleaving
excerpts by different composers is the manipulation that produces classification
of *unheard* pieces (Wong/Roark et al. 2020).

Done:
- `cm_ear.py` — unsuspended 280 ear cards for tier1 pieces that have audio, and
  repositioned the whole new queue so **no two adjacent cards share a composer**
  (longest run 20 → 1). Active Classical Music cards 263 → 558.
- `cm_dupe.py` — 17 duplicate tier1 groups, 20 redundant notes, suspended and
  demoted. Keyed on Nickname as well as work/movement after a first pass would
  have wrongly collapsed Chopin's Heroic and Military polonaises into one.
  Also cleared two `Movement` values that were German Wikipedia section headings
  ("Die Jahre am Konservatorium") on La bohème.
- `cm_listen_model.py` — new `Listen` field, rendered directly under the replayed
  audio on both audio-card backs, so it is read while the sound is still in the ear.
- `cm_listen_data.py` / `cm_listen_write.py` — **260 of 260** tier1 pieces with
  audio now carry a "Listen for" line: forces, texture, tempo, key colour and the
  one identifying gesture. Written to be discriminative, not descriptive, and to
  contain nothing knowable from the title — `Description` already holds the history.

## W116 — workspace cleanup (2026-09-25)

`tidy.py`. 1,276 files in one flat directory: 671 one-off scripts, 175 contact
sheets, 189 json caches, 185 logs. Moved 1,252 items (386 MB of loose files)
under `archive/{scripts,data,logs,sheets,images,css,dirs}/`. Nothing deleted.
Top level is now 21 files: `concept_add.py`, the re-runnable tools
(`qb_tier_model.py`, `qb_coverage_test.py`, `cm_*.py`, `caption_clean.py`,
`tidy.py`), the basemaps, the backups and the notes. Scripts imported by a kept
script were kept transitively rather than by hand — that is what saved
`cm_listen_data.py`.

`archive/` is 8.0 GB, almost all regenerable contact sheets and renders.

## W117 — Carter's live-review batch; tier model parameterised (2026-09-25)

**Art title back printed the artist twice** (Carter: "on the medusa card back it
has [image], medusa, artist name and year, artist name, year"). Caused by W102,
which added an `Artist, Date` line under the title on ARTWORK to TITLE believing
the card "never showed the artist". It already did, in the Artist / `— Date —`
block below. Line removed, Notes kept (`art_title_dedupe.py`). **W102's finding
was wrong** — the audit read the template's top half and not the rest.

Swept every template for the same fault by rendering ~400 active cards per deck
and looking for block-level text repeated on one side. One more real case:
**Film STILL to TITLE** showed Still 1 and its caption twice — under the question
and again as the first figure of the W93 gallery. Removed from the gallery on
that card only (`film_still_dedupe.py`). Remaining hits are by design (eyebrow
"Genre" + plate "Genre", map labels echoing the name).

**Classical Music Description** moved above the tier tag and centred
(`cm_desc_move.py`; it sat after the tag with `text-align:left`).

**Suor Angelica audio** replaced. The W34 YouTube clip was chosen for the opera,
not the aria the card names, and had a broadband noise floor at about -55 dB
across the whole spectrum. Now 75 s of Adriana Guerrini's 1950 Columbia DX 1651
*Senza mamma* (archive.org, public-domain mark). Old reference in
`backups/cm_suor_angelica_audio_before_2026-09-25.json`.

**Ear cards suspended.** Carter: name -> composer is what quizbowl scores. 260
active `AUDIO to COMPOSER` cards suspended; list in
`backups/cm_ear_cards_suspended_2026-09-25.json` (reverses W115's unsuspension).
`AUDIO and WORK to COMPOSER` (the title card) and the 37 term cards stay active.

**Italics in the new CM text** (`cm_italics.py`): all 662 distinct Description
and Listen texts read by hand over an automatic proposal. 283 texts, 412 notes.
Titles of anything (works, numbers, nicknames, songs, poems, films) and foreign
words / Italian markings italic, per Carter's *cor anglais* and *Goin' Home*;
style names, generic forms, institutions and characters roman. Corrections in
`data/cm_italics_fix.txt`. Not yet done for the other decks — see below.

**Later in W117 (same session, Carter's live review):**
- **Oxford comma** — the old `oxford_comma.py` proposed 94 fields; 33 of its
  proposals were wrong (it split "cellos and basses", "quiet and broken",
  "Bernstein and Sondheim") and were refused; 66 applied. A wider scan found 906
  "A, B and C" candidates it had missed (the Art "About" descriptions among them);
  all read by hand, 291 applied across 283 fields. Backups `backups/oxford_comma_before_*`.
- **Art Notes centred** on ARTWORK to TITLE / ARTWORK to ARTIST; on TITLE to ARTIST
  the note (front and back) lost its parentheses and got a margin — it was flush
  under the title. Only 105 artworks carry Notes (the W109 context notes), so
  "title + description -> artist" exists for those and title-only for the rest.
- **Period · place dot** — the HTML was symmetric; Century Gothic's middot glyph
  sits off-centre. Now a span with equal margins in Georgia (`art_dot_spacing.py`).
  CM, Film and History use the same pattern in other fonts: not yet checked.
- **Renaissance** movement card: two copies of the same Piero *Baptism* (the second
  captioned "Prado, 1507" — wrong) and 500 px thumbnails. Now Piero, Masaccio's
  *Trinity*, *School of Athens*, *Sacred and Profane Love* at 1920 px, viewed first.
- "at MoMA" -> "at the MoMA" (6 fields). *The Idiot* italicised in the Holbein note.
- **Open:** italics pass over all other decks' text, captions included (Carter:
  "i need works in captions italicized"); *Among the Ruins* image (750 px WikiArt;
  Commons rate-limited the search); tier-model report.
- **Teatro Olimpico** picture: 500 px shot with a sofa and orchestra chairs on stage
  -> clean full-width *scaenae frons* plus the forced-perspective street through the
  central arch. **Robie House**: cabinet close-up and tree-hidden exterior -> the
  cantilevered terrace roof, the street front, the art-glass windows.
- **Locations**: City, Region, Country everywhere (Carter's choice), 216 changed
  (`arch_location_regions.py`). "Vicenza, Veneto, Italy" -- Vicenza is not Venice.
  Region-only entries got the real town (Stonehenge -> Amesbury, Ur -> Nasiriyah).
- ***espantabruixes*** italicised (Casa Milà caption).
- **Architecture laid out like Art** (`arch_artstyle.py`, Carter: "yes do it"): one
  centred column -- name large, architect, "- date -", style, location,
  description, Detail; the field a card asks for set large in the accent colour;
  no labelled grid, no "Show details" fold; Art's paper colour and type; pictures
  at natural proportion, no grey matte. Scroll-to-answer classes kept.
- **Descriptive cards: text only on the front** (`text_fronts.py`, Carter: "your
  call"). DEFINITION to NAME in Architecture, Geology, Art, Photography, and the
  Art and Film FIGURE cards no longer show pictures on the front; every back
  already showed them. A tossup gives a description, never a picture.
- **Hints removed** from both Classical Music fronts (Carter: "not useful") -- the
  only templates that had them.
- **CM phone cut-off**: the description now ends the card and sat under
  AnkiMobile's answer bar; 110 px of room added below (Architecture too). Both
  names of a work (*Symphony No. 9* and "From the New World") now bold.
- **La bohème** clip ended on a German narrator starting "Die populäre…"; cut at
  20.6 s with a fade (original in `backups/`).
- **Full names** for people who are not household names (Carter: "idk who
  [Murger] is"): 66 CM texts, 145 notes (`cm_full_names.py`).
- **Suor Angelica "0 seconds"** on the phone: the file is fine on desktop (75 s);
  new media reaches the phone only after a sync, which is still pending.
- **Tier model**: qbreader stops paging after 10 x 1000, so pools are now fetched
  per difficulty (Art 10,261 unique after mirror de-duplication, not 9,938);
  scoring indexed by distinctive token (45 s instead of 30+ min), Architecture
  regression still identical. Stale runs from the first attempt were killed.
- **Key names** hyphenated per convention ("E-flat major", "C-sharp minor"; major
  and minor stay separate): 30 notes whose Description or Listen used "E flat",
  "D♭", "C♯". Key and Work fields already conformed. Brahms's motto "F–A-flat–F".
- Schubert *Great* description rewritten (Carter: "syntax ... 'the great C major,
  found by...'").
- **39 CM term cards** (`cm_terms_add.py`) for terms the deck's own text uses
  without a card: recitative, aria, opéra comique, grand opera, masque,
  semi-opera, ballad opera, *tragédie en musique*, opéra-ballet, operetta,
  intermezzo, melodrama, incidental music, suite, serenade, character piece,
  *Dies irae*, Tristan chord, mad scene, trouser role, countertenor, Mannheim
  rocket, *Sturm und Drang*, tone cluster, microtonality, *Querelle des
  Bouffons*, paraphrase mass, solmization, quodlibet, church parable, gamelan,
  cor anglais, celesta, ondes Martenot, cimbalom, glass harmonica, basset horn,
  flat and sharp (Carter: "i should learn what the symbols mean"). Tier1 only the
  first two, *Dies irae*, the Tristan chord, flat and sharp (6 active); 33 suspended.
- **Tier matcher, second trap found**: an answer of "Venus" or "Rome" counted for
  every painting with that word in its title (64 "answers" for Correggio's *Venus
  and Cupid with a Satyr*), because the rule accepted the answer as a *part* of the
  title, and plural-stripping ("venus" -> "venu") slipped past the generic list.
  Now a work must be named whole in the answer, generic words are stripped the
  same way, and a title needs four distinctive words to count without its maker.
- **Architecture night mode**: my Art-style palette was forced on in night mode
  too, so AnkiMobile showed a cream box on its dark background (Carter). Now Art's
  night palette (#1b1a18 paper, light text, #d2ab8f accent); rendered both modes.
- **Architecture pictures drawn exactly as Art's** (Carter: "are there borders
  around images or no?"): 1 px black border (white at night), soft drop shadow,
  white backing, 260 px each when several, a single picture up to half the
  screen; captions in Art's size and colour.
- **Tier matcher, more traps** (each found by reading the evidence, not the
  scores): answers naming a genre ("Symphony (ies)", "requiems") or listing
  specific works in accept clauses; instrument words ("Flute Concerto No. 2"
  took every "flute" answer); generic-only titles ("Requiem") that could never
  match; titles split at "/" into stray names ("Venice"); answers with extra
  distinctive words ("United Kingdom" for Hirst's *The Kingdom*); shared titles
  needing the maker's full name. `qb_verify.py` checks any "never appears"
  finding against qbreader's own full-text search across every category.
- **One note per movement** (`cm_merge.py`, Carter: "attach multiple audio clips on
  the same card"): 77 groups, 90 duplicate notes folded in; the kept note carries
  every clip and the best tier; the rest suspended and tagged `Music::merged`.
- **Justified picture rows** (`figs_justify.py`, Architecture and Art, every
  template): pictures in a row share one height, widths by aspect ratio, 2-3 in
  a row, 4 as 2x2, capped at 300 px; never cropped or stretched. Fixes the
  Ospedale's pictures wrapping and the Heydar Aliyev pair at different sizes.
  Re-runs when Art's caption script rebuilds the figures.
- Architecture backs now show only what each card asks (Carter), as Art's do.
  Alternate names back in the system font (Optima lacks "ə"). Style cards show
  their pictures on the front again (Carter); elements stay text-only.
- Art Detail blocks restyled to Classical Music's. Islamic architecture definition
  rewritten (Carter: "shaped by the faith Muhammad preached -- this is terrible").
- **Tier report**: `data/tier_report_2026-09-25.md`, IDs in
  `data/tier_proposal_2026-09-25.json`. Proposed, not applied: 30 CM works to
  tier1 (58 notes), 21 CM works tier1 -> tier3; Art and Photography no changes
  (evidence not certifiable -- see the report).
- **Spacing pass** (Carter: "verify that all spacing is ok"): every card type of
  Architecture, Art, and Classical Music rendered at phone width (`render_sheet.py`)
  and read. Fixed: a rule between question and answer on every Architecture back
  (name -> architect was cramped under the name); Detail label spacing; Art pictures
  and CM descriptions running to the screen edges on phones; no rule before the
  pictures that close the name -> architect back (Fagus Factory).
- Three pictures stay one row only while each is >=170 px tall, else 1 + 2 (phones).
- Architecture style backs now name the architect under the style (Carter).
- "Major works" in Art and Architecture restyled like Detail (centred, same font);
  Art works italicised, best-known one bold instead of an underline that read as a link.
- Michelangelo (Architecture figure): 330 px portrait, dome, and staircase replaced
  with full-resolution Commons images, viewed first.
- Carter asked about the dark background and white text: that is night mode (Art's
  night palette); cream is the day palette.
- **Tier changes applied** (Carter: "apply"): 30 CM works (58 notes) to tier1,
  title cards active, ear cards left suspended; 21 CM works tier1 -> tier3, all
  cards suspended. Tags backed up in `backups/cm_tier_apply_before_*`. CM active 340.
- **Oxford commas that did not stick**: the earlier pass fixed one note per
  distinct sentence, but CM movement notes share descriptions, so the copies kept
  the old text (and the merge sometimes kept an unfixed copy). Re-applied every
  approved fix to every note containing it: 12 more fields.
- **Composer portrait** (Carter: "not a fan of the circular image"): now a small
  rectangle in its own proportions with Art's border and shadow, centred above
  the composer's name.
- **Low-res images** (`img_upgrade.py`): measured every picture; tier1 under
  700 px: Film 163 of 201, Art 80, Architecture 62, Performing Arts 16, History
  Clue 16, Photography 11. Finder: Wikidata P18 for the main picture (creator or
  place must match), Commons search by caption for the others; old|new sheets read
  by eye before any swap. Film waits on the TMDB key (steps given to Carter).
- **Film stills from TMDB** (`film_stills.py`; Carter added `.tmdb_key`): all 122
  films without a still filled. Each matched by title and year with the director
  confirmed from TMDB credits; text-free backdrop at 1280 px; every one viewed.
  19 first picks were promotional art or collages, not frames, and were swapped for
  a real frame from the alternatives. New cards on non-tier1 notes suspended.
- **Image upgrades, Art and Architecture tier1**: 51 candidates read on sheets, 19
  applied (same work at 2-10x the resolution, or the captioned subject photographed
  properly); 32 rejected -- wrong work, a portrait swapped for a building, a worse
  angle. Commons full-text search is unreliable for this; Wikidata P18 is not.
- **Film: sharper versions of existing stills.** For every captioned still under
  900 px, the closest of the film's TMDB frames by image fingerprint; all 43 under
  the cut-off read by eye. 16 are the same shot at up to 1280 px -- swapped, caption
  kept. 13 "stills" were not frames at all (a boombox for *Do the Right Thing*, the
  Parthenon replica for *Nashville*, a concert hall for *Tár*): a real frame now
  asks the question, and the old photo moved with its caption into the back
  gallery. Three whose gallery was full (*Shawshank*, *Gravity*, *Rear Window*)
  restored unchanged. Film stills still under 700 px: see next pass.
- **China History Podcast ep. 1** (Carter's ChatGPT screen transcription; prehistory
  to the Zhou founding): 38 History Clue cards (`hist_chp1_add.py`, tag
  `History::source::chp_ep1`). 25 on topics the deck lacked (Nine Tripods, Yao,
  Shun, Jie, Wu Ding, Pan Geng, Wang Yirong, Wang Guowei, jiaguwen, the sexagenary
  cycle, paolao, Kings Wen and Wu, Huangdi Neijing, Five Phases, Li Ji...); 13 are
  second clues from a different angle on entities that had one card (Carter:
  "it's about effective learning", not one card per entity). Written from the
  standard record, not the OCR text. Fu Hao's new clue tier1, the rest suspended.
- **Media case mismatch**: the Suor Angelica audio still did not play because the
  file is stored lowercase and the field used capitals -- fine on Windows, silent
  on the phone. Found 3 such references (2 Architecture pictures too) and fixed
  them; `img_upgrade.py` now writes lowercase names.
- **Geography**: Nunavut had the plain Wikipedia locator though rendered maps
  existed -- swapped. 140 other subdivisions have no rendered map at all (Chinese
  provinces, German and Italian regions, Sindh...). Map + globe on one back ran
  together (Marshall Islands); now separated by a gap and hairline. Saint Kitts
  and Nevis: no "France" label in any current or archived map image -- asked Carter.
- **Film fronts**: 25 more tier1 films now open on a sharp TMDB frame; 23 kept
  their old captioned image in the back gallery, 2 were the same scene. 18 left
  unchanged: no free gallery slot, and swapping would lose a captioned photo.

## W118 — Geography maps rebuilt; opera excerpts; captions (2026-09-26)

Carter: "review the maps ... for consistency and accuracy and optimize them."
Sampled 31 notes front and back, found the faults were systematic, and fixed them
in the renderer (`archive/scripts/ne_render.py`, backup `ne_render_backup_2026-09-26.py`)
rather than map by map; then re-rendered all 2,106 maps and applied 1,877 swaps
(`geo_v3_apply.py`, new files named `-v3` so the phone fetches them).
- **Answer label one size** (28 pt; above the shape when it won't fit), not
  tiny on Manicouagan and huge on Anguilla.
- **No name twice**: "Bay of Plenty" twice, "Auckland" under Auckland, "L'viv"
  under Lviv, "Genève" under Geneva -- a context label may no longer repeat the
  answer or a name already placed.
- **Rivers the note names are always drawn and labelled** (Wei at Xi'an, Yamuna at
  Delhi): 418 places, from the note's own Info text (`_force_rivers.json`).
- **Capitals starred** on every answer map (501 located, `_capitals.json`).
- **Full names**: "Central African Republic", not "Central African Rep."; English
  region names on city maps ("Bavaria", not "Bayern").
- **1.35x type scale**: labels were unreadable at phone width.
- Island labels on wider views; seven seas named instead of five.
- 130 subdivisions still on Wikipedia locator maps now have the house detail map
  plus a wide context map. 10 former regions (pre-2016 France, Daman and Diu) kept
  theirs: no current boundary data.
- Map and globe on one card now the same width, separated.
- **Capitals filled** for 226 subdivisions/territories that had none; the 452
  capital cards this generated are suspended (tag `Geography::capital_added_2026-09-26`).
  Seat shown only when Capital is empty (it duplicated). Port Blair ->
  Sri Vijaya Puram (Port Blair).
- **Regions**: 226 subdivisions given their country's official region (North
  China, Southern Italy, Atlantic Canada...) instead of "Asia"/"Europe"; 254 more
  continent-only or synonym regions refined. Latium merged into Lazio.
- **Captions**: 39 cut off mid-word at 140/150 chars (Monaco "jutt") rewritten;
  23 Wikipedia footnote markers ([195] on Czechia) removed.
- Definition fronts no longer print the kind twice ("LANDFORM ... Landform?"), 6 decks.
- **Opera excerpts**: 14 of 155 unnamed opera clips identified (filenames and
  audio fingerprinting against cached sources) and their aria named. The rest have
  no surviving source record.

## W119 — AUDIT_2026-09-26 triage: clear errors fixed (2026-09-26)
- Nationalities (211 CM notes): Mozart, Haydn Austrian; Martinů Czech; Chopin, Szymanowski
  Polish; Gluck German; Clementi Italian (last two not in the audit); England-born
  composers "English" throughout (was mixed with "British").
- Lawren Harris "Art Deco" -> Canadian Modernism; Tom Thomson "Art Nouveau" ->
  Post-Impressionism and linked to the Group of Seven; Emily Carr linked. Hopper's
  invented "[Windows series]" removed from 6 works (Delaunay's and Chagall's real
  series kept).
- Peer Gynt: suites dated 1888 (Op. 46) and 1891 (Op. 55), not 1875; Op. 23 is
  incidental music. Galerie, Bauhaus (Sullivan's phrase removed), Sant'Andrea, Mantua
  (begun 1472, dome 1732), Taj Mahal note, Suez Canal kind "canal", Cuba border
  (Guantánamo only), Somaliland (recognised only by Israel since 2025), Köln Concert
  venue (Cologne Opera House).
- Answer leaks: Art TITLE to ARTIST front no longer shows the context note (40
  leaks); two disambiguators named the artist's museum; 3 Architecture location
  cards whose name gives the place suppressed (NameTells).
- 26 captions cut off with "…" rewritten; Cabaret's Camelot photo removed.
- Three Geography maps pointed at files that never existed: Daman and Diu fixed;
  Xikang and Cocos (Keeling) Islands have no boundary data -- map cards suspended.

## W120 — Audit plan, part 1: BISE complete, new card types, standardisation (2026-09-26)
- **BISE (VFA pdf pp. 27-38) now complete.** 195 of 200 works and all 53 terms were
  already in; the last five added at tier2 (`art_bise_last5.py`): Ghiberti's
  *Sacrifice of Isaac* (cut from the side-by-side Bargello photo -- left panel,
  Isaac kneeling nude on the altar), Rubens's Munich *Lion Hunt*, Elsheimer's
  *Flight into Egypt*, Serpotta's *Fortitude* (plinth reading FORTITVDO cropped off,
  it would print the answer), Piranesi's *Colosseum*. Each new title collides with an
  existing one, so TitleShared disambiguators were added to both sides (Brunelleschi's
  panel is now "the losing entry").
- **Card types for the commonest answers.** 28 music term notes (`cm_core_terms.py`):
  17 instruments and 10 genres (string quartet, concerto, waltz, mass, symphony,
  sonata, march, ragtime ...), tier1 at 10+ pool answer lines; cor anglais promoted.
  DESCRIPTION to WORK card for Classical Music (`cm_clue_card.py`, new Clue field and
  template): 155 tier1 works, one note per work, the description with the title and
  nickname masked. 68 FIGURE to ARTIST notes for the most-answered artists in the VFA
  pool (`art_fig_canon.py`, David to Mondrian); the W84 figures were a British-heavy
  list with almost no answer lines, so only the 10 with evidence were activated. All
  38 Film director cards activated.
- **Redundant music cards**: at most two active AUDIO and WORK cards per work, the
  best-known movements kept (`cm_trim_movements.py`, 88 suspended, tag Music::trimmed).
- **Non-Western**: most of the audit's list was already present, only suspended; six
  missing staples with pool evidence added (`art_nonwestern_add.py`): Narmer Palette,
  Olmec colossal heads, *Dwelling in the Fuchun Mountains*, lamassu, *The Court of
  Gayumars*, and a Mughal painting style term.
- **Carter's phone review**: picture rows no longer re-flow while scrolling (the
  layout scripts re-ran on the height-only "resize" a phone fires when its toolbar
  hides; now width changes only, 19 templates); TITLE to ARTIST front keeps the title
  alone, with the disambiguator and clue behind a Hint button; spacing fixed under the
  clue (DESCRIPTION to TITLE) and under Notes (ARTWORK backs); Installation art given
  four distinct, properly captioned works; *Anthropométries* no longer names Klein and
  shows a finished *Anthropometry*; *Among the Ruins* demoted to tier4 (zero qbreader
  questions pair the title with Alma-Tadema, and no scan larger than 800px exists).
- **Tier gate repairs**: the seven W114 Architecture promotions (Tower of London,
  Dome of the Rock ...) had never been unsuspended; now active, except the location
  card where the name contains the city.
- **Mechanical standardisation** (`std_mech.py`, one pass at a time, backups per pass):
  BCE/CE everywhere (177 fields); Canadian spelling, lowercase words only so proper
  names keep theirs (57 fields; isorhythm's Latin "color" kept); straight double
  quotes curled in 266 fields, judged across tags, with six source errors fixed by
  hand; Japanese romanised with macrons (Tōkyō, Yasujirō, Tōdai-ji); Film director
  works lists italicised; proponent-list dots spaced evenly. Bullet punctuation was
  already uniform (the audit's "with a period" were brackets and quotes).
- **Performing Arts**: 221 gallery pictures that repeated the main picture removed
  (perceptual hash, sample checked by eye); 26 captions rewritten (file names, cut-off
  text, and 12 pictures that had none).
- Left as they are, by judgement: Art's Title Case media ("Oil on Canvas") is
  consistent, not mixed; "English"/"British" follows the usual labels for each artist;
  Architecture italicises foreign building names through its Foreign flag, by design.
- **Carter: "activate them"**: the 37 tier1 Tang clue cards that were suspended are
  active (the 12 dense History reference notes stay suspended, W63).
- **Carter: "ensure that none of the descriptions of art works mention the artist"**
  (`art_artist_mentions.py`): every artwork note's Clue, Notes, Description, and
  Captions scanned for the artist's own name in all its forms (surname, full name,
  parenthesised alternates, first-name artists like Leonardo and Rembrandt). 53 fields
  rewritten by hand to refer to "the painter", "the sculptor", "the artist" (other
  people keep their names; titles italicised on the way); rescan finds 0. Two
  disambiguators behind the new Hint button named the artist's own museum (Van Gogh
  Museum, Norman Rockwell Museum) and now give only the city.

## W121 — "Go through every single card": Geography text, Architecture detail, maps v4 (2026-09-27)

- **Geography text audit** (`geo_text_fix.py`, data in `data/geo_text_fixes.py`): all 1,100
  notes read field by field. Two cards carried another card's text: Georgia (the
  country) had the US state's Info and Niger (the country) had the river's; both
  rewritten, and the state's generic history line replaced with its geography. 142
  notes corrected in all: wrong facts (Maine "northernmost", Malawi's Mulanje "highest
  in central Africa", Kinabalu, the Elbe "past Prague", Everest's neighbours "a few
  kilometres"), straight history swapped for geography per the Geo Info rule (Suez
  Canal, Belgium, Germany, Greenland, Grenada, Turin, Samarkand, Negev, Lake Geneva,
  Lake Tanganyika), filler ("... are features") replaced with facts, comma slips,
  straight quotes curled (15 fields). Number fields made consistent: Everest 8,849 m
  (the Himalayas card already said so), Rainier 4,392 m, Alps 4,808 m; Gulf of
  Thailand "Part of" South China Sea; Kingdom of Hawaii ended 1893; Manchukuo "Now"
  China only; a stray Capital on the Yukon River cleared.
- **Duplicates**: "Mount Saint Helens" (new, unreviewed) suspended into "Mount St.
  Helens" (5 reviews), and "Saint Lawrence Seaway – Saint Louis" into "Saint
  Lawrence", each keeping the other's tags (NAQT, superlative). Latium was already
  merged into Lazio.
- **Photo captions** (`geo_caption_fix.py`): 122 captions that were pasted Wikipedia
  sentences, some with citation stubs ("[122", "[4"), cut to what the photo shows;
  four photos (Albania, Asia, French Polynesia, Germany) checked by eye first.
- **Architecture DETAIL** (`arch_detail_rewrite.py`, data in
  `data/arch_notes_rewrites.py`): all 533 notes read; 140 rewritten where the detail
  restated the description, was filler ("Enduring symbol of ..."), ran bullet
  fragments together, or had slips (Maison Carrée, Gaudí, "form ever follows
  function"). Titles and foreign terms italicised.
- **Maps v4, full run** (`geo_maps_v4.py`, `archive/scripts/ne_render.py`, `ne_points.py`): the
  first full run failed 77 of 129 landform maps that render fine alone. Cause: the country
  index was cached from whichever map's projection was active first, so later notes looked
  up their Parent in projected coordinates. Now always built in lon/lat. Other fixes found
  reviewing the sheets:
  - Garbled or local Natural Earth names corrected where the data loads ("Rhne", "Sane",
    "Gta lv", "Kiz?lirmak", "Sapt" for the Kosi, the Icelandic Þjórsá filed as "Drau");
    labels in English (Donau, Tevere, Maas, Schelde, Tajo, Tikahtnu Inlet → Cook Inlet).
    A control character had replaced the `\b` in the lake-name pattern, giving
    "Lake Georgian Bay"; restored.
  - Rivers matched under all their names (the Rhine stopped at the German border, the
    Tagus at Portugal's, the Yangtze above Yibin); irrigation canals no longer labelled;
    a river named like a country (Niger) gets no capital star.
  - Points: a border peak is framed on the smaller country (K2 on Pakistan, not all of
    China); a place in a very large country on its state (Mount Rainier's close-up was half
    of North America); the state/province label under the marker restored (a variable mix-up
    had dropped every one); bare "Southern"/"Eastern" region labels dropped.
  - One label per name per map (the Big Island said "Hawaii" twice); small islands'
    names placed off other land (Kahoolawe's sat on Maui); "Great Britain" and "British
    Isles" no longer printed under "United Kingdom"; a breakaway state's country named.
  - Historical maps draw today's land under the historical states (the 1530 Ottoman map
    showed inner Africa as sea). Kiribati framed across the 180th meridian with all its
    island groups; a scatter of specks (Tuvalu) ringed on the locator.
  - Previously failing notes built: Xikang (approximate outline from Natural Earth
    provinces, captioned), the Australian Antarctic Territory, Daman and Diu and Dadra and
    Nagar Haveli (each its own pieces of the merged territory; the district card had drawn
    all three), Cocos and Christmas Islands (framed with Java and Australia), Molokai,
    Niihau, Kahoolawe, the Painted Desert, the Suez Canal, the Peloponnese, the Red River of
    the South, and eight waters whose Parent named a region, not countries.
  - Second pass, every map read on review sheets (countries, waters, subdivisions, points,
    regions, landforms; details in `renders/geo_v4/REVIEW_LOG.md`):
    - Borders: Crimea shown as Ukraine's, as Western Sahara is shown apart from Morocco (UN depiction).
    - Seas with arms drawn whole: the Baltic with its gulfs, the Gulf of Mexico with the Bay of
      Campeche, Hudson Bay with James Bay, the Red Sea with the Gulfs of Suez and Aqaba. Seams from
      the 180th meridian closed (Bering, Chukchi, Pacific). The Arctic Ocean with its marginal seas
      on a polar view; the Southern Ocean as the water south of 60° S. The Drake Passage drawn by hand.
    - Rivers completed where Natural Earth breaks them: the Euphrates (Firat, Al Furat), the
      Irtysh (Ertis), the St. Lawrence to Tadoussac, and the whole Snake.
    - Labels:
      - English names (Sekong, Teesta, Manas, Kokemäenjoki, Tripoli, "Amur Oblast", "Moscow Oblast").
      - One label per island group (not "Andaman Islands" and "North Andaman Island" both).
      - Tiny neighbours named (Barbados, Grenada, Saint Martin); enclaves named (Lesotho, Beijing, Tianjin).
      - "Portugal" on the mainland, not the Azores; Japan's name on Honshu.
      - No "Polynesia" or "Malay Archipelago" as island labels; a city-state's capital not repeated (Singapore).
    - Scattered island states (Kiribati, the Marshall Islands, Maldives) get a dot on each atoll
      instead of a ring on each. Speck names are kept off their own rings and placed beside the
      main part or the capital's part (Colima, Puducherry).
    - Frames:
      - The Spanish Empire renders again (Americas and Iberia, with Spanish Louisiana and Florida).
      - Tokyo is cropped to the mainland and the Izu Islands, with a caption.
      - The French Southern and Antarctic Lands show all their island groups.
      - Tighter frames for Nunavut, the Great Salt Lake, and several lakes.
      - Sindh is drawn as today's province, not the 900 CE state.
  - Final render of all 1,100 notes: `renders/geo_v4/h1`–`h6`. A last regression was caught
    there and fixed: the target named beside itself under Natural Earth's other name ("Western
    Sahara" in the sea on the Sahrawi question map).
  - Applied 2026-09-28 (`geo_maps_apply.py`; old fields in `backups/geo_maps_before_20260928_205542.json`):
    Map, Map Labeled, and Map Wide on all 1,100 notes. The MAP to NAME card now shows the
    unlabelled map with the locator on the front, and the labelled map with the locator on the
    back (`geo_template_v4.py`; template backup `templates_backup/geo_v4_before_20260928_2056.json`).
- **Sahrawi photo**: the 120×140 thumbnail replaced with the El Aaiún refugee camp near
  Tindouf (Commons, CC BY-SA 3.0), captioned. All 832 Geography photos checked: none else
  under 300 px or missing.
- **Carter's phone review, Architecture and Art** (`arch_review_fixes.py`): alternate
  names in one format (foreign italic, English meaning in brackets, no quotes, "lit." or
  leading "The"; non-names such as Faisal Mosque's "Islamabad", Petra's "Al-Khazneh",
  and street addresses removed; 60 notes); 61 Locations lose a region that only repeats
  the city ("London, Greater London, England" → "London, England"; Kyoto Prefecture, New
  York for New York City); Casa Batlló, Il Gesù, and the UN Secretariat descriptions no
  longer name or describe the architect; Reinforced concrete's "[fr]" and sentence
  captions cut; Functionalism's two copies of one blurry photo replaced by the Van Nelle
  Factory (Commons) and the Bauhaus at Dessau; lists in centred blocks align left
  (Gothic's bullets were already prose after the DETAIL rewrite). Brâncuși: ş/ţ for
  ș/ț in 33 Art and 2 Photography notes, since Optima lacks the comma-below letters.

## W122 — "Review everything" in Geography; Carter's map, Music, Art, and List notes (2026-09-28/29)

- **Geography photos** (`geo_photo_fix.py`, picks in `data/geo_photo_picks.json`): all 832 read on
  contact sheets. 113 replaced from Commons, each chosen by eye:
  - strips and thumbnails (Missouri 500×139, Crater Lake, Martinique, Seychelles);
  - photos that did not show the place (a Nevada road sign on Oregon, hurricane debris on Sint
    Maarten, Masaryk's portrait on Czechoslovakia, labelled maps and satellite images);
  - dark, dated, or generic shots (Antigua at night, a 1986 Andorra street, parliament buildings on
    German and Mexican states, UN offices on Austria);
  - duplicates of another card's photo (Argentina/Aconcagua, Ukraine/Ruthenia, Bukhara/Kyzylkum,
    Mexico/Chichen Itza, Kilauea/Hawaii, Table Mountain/Cape Town).
  97 captions written or rewritten to say what the photo shows (30 were blank). Backup
  `backups/geo_photos_before_*.json`.
- **Flags**: all 383 read beside their names and symbolism text; none wrong. Jammu and Kashmir's
  flag now says it is the former state's (to 2019).
- **Regions** (`geo_region_fix.py`, 111 notes): US states use the regions in common use (New
  England, Mid-Atlantic, Southeast, Midwest, Southwest, Mountain West, Pacific Northwest, West
  Coast, Pacific) instead of Census divisions; descriptive or self-naming Region values replaced
  ("Northwest African Atlantic" → Macaronesia, "Hokkaido region" → Northern Japan); the African
  Great Lakes told apart from North America's. "Now" cleared where it only repeated "In" (Bengal and
  33 others; on historical states "In" is cleared instead). The merged duplicate "Mount Saint
  Helens" had been unsuspended; re-suspended.
- **Maps, Carter's notes** (`ne_render.py`, `geo_maps_v4.py`; render `renders/geo_v4/i1`–`i6`, applied):
  - internal borders (states, provinces) drawn once as merged dashed linework above the rivers:
    they had been drawn once per neighbour, so the two dash patterns interleaved into solid
    lines on some borders, and river-borders (New Jersey's Delaware) were hidden under the river;
  - a province's map greys every other country (Franche-Comté), and a region's locator outlines its
    sister regions;
  - a country's name must sit on its own land or the sea, not a neighbour's (Netherlands on
    Germany, Bangladesh and Jharkhand on Bengal, Rhode Island on Connecticut); river names keep
    off other rivers (Ganges in the delta);
  - a sliver of a big federal country is named for its state or province (Florida on Cuba,
    Ontario on Ohio);
  - a cache bug fixed: after a batch's first map, a province's own shape could be drawn as one of
    its neighbours (Beijing went unnamed in Hebei's hole);
  - the target is never named under Natural Earth's other name (Western Sahara on the Sahrawi map).
- **Classical Music** (`cm_text_0929.py`, `cm_audio_0929.py`; backups `backups/cm_text_before_*`,
  `cm_audio_before_*`, `templates_backup/cm_before_*`):
  - all 482 active "Listen for" lines read against their descriptions: 32 Listen lines rewritten
    to name what the passage sounds like, and 104 descriptions (with their clue where it was the
    same text) that only repeated the sound now give other facts (Gnossiennes, Danse macabre,
    Canon, Boléro, Zarathustra, Tell, ...);
  - 9 clues that nearly named the answer reworded (Woyzeck, Kreisler, Rhine gold, Erlking, Caesar,
    Bach/Bachianas, Matthias/Mathis, Orfeo, Der Tod und das Mädchen);
  - 68 movement titles: sung numbers in curly quotes, instrumental movements italic, one act style ("Act III · ");
    *Mars* and *Ring* italicised;
  - audio: Cavalleria rusticana (modern Intermezzo), Norma (Justina Didyk's "Casta diva"), Nixon in
    China (recut to start on "News, news, news", checked by speech recognition), the Ring Cycle (Ride
    of the Valkyries: "Fort denn eile" exists free only in the acoustic-era recording the bad clip
    came from), Recitative (Bach's Cantata 140 secco recitative); 32 concept cards now play their
    "Heard in" example from clips already in the deck;
  - DESCRIPTION to WORK asks "Title?" under a "Piece" eyebrow; more room between clip and title.
- **Art**: the definition on DEFINITION to NAME centred.
- **List cards** (`list_redesign_0929.py`): the front shows only numbered slots with the asked-for
  one marked (the old front showed every other row, answering the list's other cards); the back
  reveals the whole list; a Measure line ("Ranked by maximum depth"); Geography thumbnails are the
  items' own maps (Issyk-Kul's was a beach photo).

## W123 — Carter's notes of 2026-10-01: maps, pictures, italics, two broken layouts

- **Map labels** (`ne_render.py`; full re-render `renders/geo_v4/j1`–`j6`, applied to all 1,100 notes and verified
  by a dry run; `geo_maps_apply.py` now takes `--start`/`--count` and waits out Anki's media sync):
  - a river is named only where its own line shows: not inside a lake (the centreline runs on
    through it: Klarälven was printed on Vänern, Semliki and Nile on Lake Albert, Waikato on Taupō,
    Mackenzie on Great Slave Lake) and not on a stretch that is a border or coast (Serbia's
    "Danube" sat on the Romanian frontier with no river visible);
  - river names stay off a lake or sea that is the card's answer; near the place first, then clear of
    other rivers (Serbia's Danube had moved up into Hungary);
  - a lake's map names the island it is on (Sulawesi on Lake Matano, North Island on Taupō); island
    names never sit on a water target.
- **Architecture pictures** (`arch_images_1001.py`; sources `data/arch_image_sources_1001.json`):
  every live work now has at least two pictures (30 had one; 60 added from each building's Wikipedia
  article and Commons, chosen on contact sheets). Hill House, the British Museum, and the
  Transportation Building showed prints with the building's name printed under them (replaced, or
  cropped); MoPOP's abstract close-up replaced by the aerial, the monorail, and the street front.
  Captions for the seven works that had none.
- **Location cards**: Sant'Andrea, Mantua and Imperial Hotel, Tokyo name their city; NameTells set and
  the PICTURE and NAME to LOCATION card suspended (the only two live names that contain their city;
  the card shows Name, not Alternate).
- **Classical Music** (`cm_text_1001.py`, 144 notes): instrumental pieces and movements italic
  everywhere, sung numbers quoted (*Prélude*, *Menuet*, *Clair de lune*, *Passepied* on *Suite
  bergamasque*; *Putnam's Camp*, *Golliwogg's Cakewalk*, the *Concord* movements, *Hoedown*, ...);
  Movement fields in one form ("mvt. III · *Title* · *Tempo*", "Act III · “Aria”", "Act III ·
  *Orchestral piece*"), tempo markings italic; works after a possessive italicised (Brahms's
  *Hungarian Dances*, Bach's *Orgelbüchlein*, Reich's *Piano Phase*); the Diabelli card names
  Leporello's aria, not "Mozart's Leporello"; four clips labelled "Aria (Mimi)"/"Act III - Aria"
  identified by speech recognition ("Sì, mi chiamano Mimì", "Tu che di gel sei cinta", ...).
- **Art** (`art_text_1001.py`, 59 notes): YBA card shows Hirst's shark, Emin's bed, and Ofili's
  Virgin (was an unreadable grid, a college doorway, and a thumbnail); *Le Déjeuner sur l'herbe* as
  an alternate title; about 120 movement/technique captions rewritten as "Artist, *Title*, date"
  (they were Commons text: roman titles, dimensions, one cut off mid-sentence); Blake's *Newton*,
  Whistler's *Nocturnes*. *Tomb of Oscar Wilde* stays italic: it is Epstein's sculpture, and the
  deck italicises every work's title, tombs and memorials included.
- **Qingming scroll card** (`art_solo_1001.py`): the qb-justify layout script paired the 21:1 scroll
  with the next picture, which shrank to 30px with its caption running down the card a letter at a
  time; a data-solo picture now gets a full-width row.
- **Phone answer bar** (`phone_bar_1001.py`): Art, Geography, Geology, History Clue, and List now
  leave 110px under the last line, as Architecture and Classical Music did, and no main deck
  rubber-bands past its ends. Film, Performing Arts, and Photography not touched (other session).
- **Park Güell**: *trencadís*.
- **Art roles** (applied 10-02): `art_roles_1001.py` sets a second hand's part in a lighter face, as
  Architecture's `.arch-role` (Rubens *(figures)* and Jan Brueghel *(setting)* on the Senses; Miró
  *(ceramics by Josep Llorens i Artigas)*); 30 notes + CSS.

## W124 — Classical Music written for quizbowl (2026-10-02)

Carter: "the listen for should be just the passage clipped", in the way tossups clue passages ("E,
long-F, D, ..."), and aria cards should clue the aria, not just the famous opera.

- **Facts, nicknames, movements** (`cm_facts_1002.py`, `cm_nick_1002.py`, `cm_mvt_1002.py`): Period tags
  match the field (Debussy → Modern); premiere dates → composition dates; nicknames printed as
  written (“Moonlight”, (*The Magic Flute*)); 121 Movement fields in the W123 form.
- **Listen / Clue rewrite** (`cm_qb_apply.py`, `data/cm_qb/batch_00`–`19`, `19b`, `20_extra`; backups
  `backups/cm_qb_*`): all 486 live notes plus Threnody and qb-e8's seven `gap_1002` notes.
  - Every clip was analysed first (scratchpad `clip_analyze.py`: key estimate, loudness by thirds,
    opening melody by basic-pitch, sung words by Whisper) and checked against qbreader tossups that
    mention the work (`qb_dossier.py`: 10,414 questions).
  - **Listen** = only what the clip holds, in tossup voice ("This symphony opens with…", "The
    *Adagio*:…"), with the canonical note clues where the clip has them: Beethoven 5's horn call,
    Dowland's falling tear, Brahms 3's F–A-flat–F, Mozart 40's E-flat–D–D, Tchaikovsky 5's motto,
    Tchaikovsky PC1's F–D-flat–C–B-flat, the Tristan chord, Parsifal's Communion theme, ...
    Description stays about the whole work.
  - **Clue** (DESCRIPTION → WORK) clues the excerpt and points to the work, with no title words
    (the apply script warns on any 5+-letter title word; "serva" in "servant" and "concerti" in
    "concertino" were false alarms; the real ones were fixed: "dance", "cantata", "sonatas", "American").
  - **Clips that were not what their label said** (Movement corrected): Diabelli Var. 33; Pêcheurs
    "Comme autrefois"; Fille du régiment "Chacun le sait"; Beggar's Opera "Pretty Polly, say"; Faust
    "Le veau d'or"; Haydn 45 finale; Fledermaus *Du und du*; Mahler 2 "Urlicht"; Manon "Ah! fuyez";
    Clemenza "Torna di Tito a lato"; Boris Coronation Scene; Butterfly "Tu, tu, piccolo Iddio";
    Dido "Thanks to these lonesome vales"; Cenerentola "Nacqui all'affanno"; Pierrot No. 9 "Gebet an
    Pierrot"; Serva padrona recitative; Queen of Spades Lisa's arioso; Don Carlos Queen's ballet;
    Ernani "O sommo Carlo" (Battistini 1906); Falstaff "Dal labbro il canto"; Trovatore "Tacea la notte
    placida"; Ballo Riccardo's "Forse la soglia attinse"; Dutchman sailors' chorus; Salome's clip
    (a sung line, not the Dance of the Seven Veils) left with no Movement rather than a guess.
  - Where a clip could not be pinned down, the Listen describes only the sound (no invented passage).
- **Porgy and Bess clip is speech**, not "Summertime" (Whisper, twice: "So yeah, it was very nice..."):
  its AUDIO + WORK card is suspended and the note tagged `Music::clip_speech_1002`; it needs a new clip.
- **No repeats on one card** (`batch_21_dedup`, `batch_22_desc`): the DESCRIPTION → WORK answer shows
  the Clue and Listen together, and the audio cards show Listen and Description; 88 notes repeated a
  4-word phrase. Clues now carry other tossup facts (premieres, dedicatees, plot), Listens keep the
  passage; only aria/piece titles still appear in both.
- `cm_qb_apply.py` skips any field holding an `<img>` (qb-e8 swaps Composer Image only).
- **La bohème "Mimi 2" / "Mimi 3" clips** (suspended): "Mimi 3" is most likely the D-major climax of “Sì. Mi
  chiamano Mimì” (Whisper: "anno a me lo svelo" for "ma quando vien lo sgelo"), a near-duplicate of the live
  card, so it stays suspended; "Mimi 2" (F-sharp minor, barely any clear voice) is still unidentified.

## W125 — Architecture: foreign building names italic in running text (2026-10-02)

- `arch_foreign_italics_1002.py` (backup `backups/arch_foreign_italics_*.json`): 161 fields on 102 notes
  (captions, Description, Notes, Works). Names: every Foreign=1 note's name plus the foreign names in
  Works lists and captions (*Palazzo Rucellai* (Rucellai Palace), *Dôme des Invalides*, *Hôtel Solvay*,
  *Schauspielhaus* (*Konzerthaus Berlin*), *Santa Maria dei Carmini*, ...). Places (Piazza San Marco,
  San Lorenzo de El Escorial), people, museums as institutions (Musée de l'Armée), and "Villa + surname"
  (Villa Savoye, as its own card) stay roman. Rendered check: "*Villa La Rotonda*, Vicenza".

## W126 — Geography pictures to 1000px+; Spanish Empire map; Syndics (2026-10-02)

- **Photos** (Carter's rule: nothing under 1000px). 237 active Images and 5 flags were under 1000px:
  - 189 re-fetched as the same Commons file at 1600px (`geo_photo_upscale_1002.py`; sources from
    `archive/data/_geo_photos.json` and `geo-img-` filenames, each checked against the old picture);
  - 48 with no larger copy replaced by another photo of the same subject chosen on contact sheets, and the
    5 PNG flags by Commons SVGs (Weimar, French Indochina, Dutch East Indies, Siam, Persia's state flag)
    (`geo_photo_replace_1002.py`, picks and captions in `data/geo_photo_replace_1002.json`). Captions
    rewritten where the subject moved (Dry Falls on the Cullasaja; the Wind River Range; Kathleen Lake,
    Kluane; the 1915 Çanakkale Bridge; Bight of Biafra from orbit, replacing a labelled map; Red Cloud
    Peak WSA rejected: it is in Colorado). Re-scan: 0 active Geography pictures under 1000px.
  - The 227 `ug-flag-*.svg` flags the audit listed at 0×0 are SVGs and need nothing.
- **Spanish Empire map** (`geo_maps_v4.py`): the 1800 snapshot's sub-Saharan polities (scattered blobs),
  a "Guanches" outline on the Spanish Canaries, and a Shuar ring in New Granada dropped; re-rendered
  (`renders/geo_v4/k1`) and applied.
- **List** (`list_maps_1002.py`): 15 Geography List thumbnails pointed at superseded map renders; now the
  current ones. Only map thumbnails are touched.
- **Broken media**: a full scan of 14,326 images in every deck found Iowa's locator and Kansas's front map
  unreadable (restored from the i5 renders) and Brâncuşi's *Gate of the Kiss* missing (the ș→ş text pass had
  renamed the reference; a copy stored under the ş name; qb-1c is upgrading the 800px file).
- **Syndics of the Drapers' Guild off-centre** (Carter): old pastes wrapped 10 Art pictures and 1
  Architecture picture in empty links, inline divs, bold tags, or Google/X/Whitney links;
  `img_wrapper_clean_1002.py` reduces them to the bare `<img>`. Étant donnés (two pictures) and the
  `img-pending` spans untouched.
- **Architecture second pictures** (`arch_second_1002.py`, sources in `data/arch_second_1002.json`): the 31
  suspended works and figures with one picture got a second, chosen on contact sheets (the Porch of the
  Caryatids, the Painted Hall at Greenwich, Houdon's *George Washington* in the Virginia rotunda, a red
  *folie* at La Villette, ...). Rejected: Pania of the Reef and *Girl in a Wetsuit* offered for the Little
  Mermaid. Bavinger House, the Bublik house, and the demolished Home Insurance Building have no second
  usable photo on Commons. Louis Le Vau is down to one after qb-1c removed his sub-1000px portrait (their slot).
