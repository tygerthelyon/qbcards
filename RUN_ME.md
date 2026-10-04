# What to do with tonight's work (2026-10-03)

Everything is on the branch **`claude/cloud-session-testing-sc5gq7`** of github.com/tygerthelyon/qbcards.
None of these steps need Claude.

## 1. Get the files onto your PC (2 min)
On GitHub, switch to the branch `claude/cloud-session-testing-sc5gq7`, then **Code → Download ZIP**. Unzip it
and copy these into `C:\QB\stockfisher\`:
- `CLAUDE.md` and `STATUS.md` — your VS Code sessions read these instead of the 350 KB checklist, which
  saves tokens.
- `export_for_cloud.py`
- the whole `history\` folder

## 2. Read the notes
- `history\notes\01_supplement_mythology_literature.docx` — the qbreader gaps in your notes, from Mythology
  through the Classics, plus 10 corrections at the top.
- `history\notes\02_prehistory_xia_writeup.docx` — a rewrite of Prehistory and the Xia (my test write-up).
- `history\notes\03_shang_supplement_bonus.docx` — a bonus: the same qbreader gap sweep for the Shang.
- `history\notes\04_zhou_supplement.docx` — the same sweep for the Zhou (mostly the Hundred Schools, which is how quizbowl asks it).
- `history\deck\DESIGN.md` — how the deck is built and why (one page).

## 3. Add the History cards to Anki (Anki open)
Open a terminal in `C:\QB\stockfisher` (click the address bar, type `cmd`, press Enter):
```
py -3.9 history\deck\hist_qb_apply.py
```
This is a dry run: it prints what it would create. If it looks right:
```
py -3.9 history\deck\hist_qb_apply.py --apply
```
That run:
- creates 3 note types (QB Clue, QB List, QB Tossup);
- uploads the 24 pictures;
- adds 230 cards for Mythology → Classics;
- orders new cards giveaway-first and interleaved.

Re-running it is safe: it updates the same notes instead of adding duplicates.

Optional:
- `--include prehistory` also adds the 49 Prehistory/Xia cards (check the write-up first).
- `--supersede` lists your old History Clue cards on the same topics; `--supersede --apply` suspends
  them and tags them `History::v1_superseded`, which you can undo.

Then **sync**. The new note types are a schema change, so Anki will ask for a full upload. Say yes.

## 4. For the Classical Music descriptions
Run `py -3.9 export_for_cloud.py` (Anki open), then upload the `export` folder it makes to the repo
(GitHub → Add file → Upload files → drag the folder). A cloud session can then write the missing
descriptions as a script you apply the same way.
