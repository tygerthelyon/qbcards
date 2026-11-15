# Using StockFisher

StockFisher finds recurring clues across tournament history in a local SQLite copy of QBReader questions. It runs locally as a native desktop web app using Python's standard library. An optional Jupyter notebook interface remains available for interactive scripting.

## Open it

Follow the [first-time setup](../README.md#setup) to download questions and build the index. After that, launch the app:

- **Windows shortcut**: Double-click **Open StockFisher.cmd** in the repository root.
- **Command line**: Run this from the repository folder:

```bash
python -m qbr.app
```

On Windows, Chrome or Edge opens StockFisher in a dedicated app window without browser bars. Other setups open your default browser. By default, StockFisher runs on port 8766 to avoid colliding with AnkiConnect on 8765. To specify a custom port or prevent opening a window automatically, pass flags:

```bash
python -m qbr.app --port 8767 --no-browser
```

The header status displays your connected index size and the date of the last successful sync. To exit cleanly, select **Index** in the top right, then select **Quit StockFisher**. You can also stop a command-line session with Ctrl+C in your terminal.

## Find clues for an answer

In **By answer** mode, enter an artist, work, place, or concept in **Answer**, then select **Find clues** (or press Enter). You can also select one of the suggested example buttons.

Start with blank filters when you want broad coverage, and narrow the results after inspecting them.

| Control | Examples and meaning |
| --- | --- |
| Category | `Physics`, `Fine Arts`, or shortcuts such as `fa` and `vfa`. Suggestions come from the connected index. Commas combine categories, such as `vfa,ofa`. |
| Difficulty | `8`, `6-9`, `college`, or blank. College dots map to 6 = one, 7 = two, 8 = three, 9 = four; 10 = open. |
| Years | `2018-`, `2015-2020`, or a single year. Blank includes all years. |
| Rank by | **Specificity** balances frequency and association with the answer. **Frequency** orders by raw question count. **Clue position** puts early tossup clues first. |
| Clues to show | Maximum number of extracted candidates displayed, from 1 to 100 (default 20). |
| More options | Match an exact answerline, compare with Anki, or exclude terms from answer matching. |

Older questions may use different categories. For example, some Damien Hirst tossups are classified as **Other Fine Arts**, so a `vfa` filter misses them. Start an artist audit with `Fine Arts` or no category filter.

Each result row displays the candidate clue, question count, specificity percentage, example passage, tossup position tag (or bonus indicator), and source citation. Expand **Matched answerlines** at the bottom of the profile to inspect the specific question variants grouped into the profile.

**Questions** counts distinct questions on the target answer that use the clue. **Specificity** compares target-associated units found by this profile with all matching units across the mirror; a unit is a tossup or one bonus part. Narrowing filters can lower that percentage because the comparison still uses the whole mirror. It is not a probability that a drafted clue is correct.

Extraction can miss titles, generic phrases, and descriptions that use different wording. A ranked list is a starting point for research, not proof of complete coverage. For work-level research, also profile its creator and read the underlying questions. Verify factual claims against reliable sources.

## Read source questions

Beside each clue row or search hit, select **Read question** (or press Enter when focused) to open the complete source question in a side-by-side reading drawer.

The source reader displays:
- The tournament set, packet number, question kind (Tossup or Bonus), question number, and difficulty.
- The full question text with the extracted clue highlighted. For bonuses, all parts and their point values are included.
- The official answerline and the unique QBReader question ID.

Select **×** or press **Escape** to close the reader and return focus to your results.

## Question text search and pagination

Select **Question text** above the search box to search passages across all answers in the index.

- Searches support exact phrases as well as boolean operators such as `butterflies OR cocoons`; see the [search syntax](../qbr/README.md#search-syntax).
- Category, difficulty, and year filters apply to question text searches.
- Results paginate 20 hits per page. Use **Previous** and **Next** beneath the list to browse through large result sets without losing your place.
- Each hit includes a **Read question** button to open the full question in the reader drawer.

## Check a draft clue

Select **Check a draft** at the top right of an answer profile to test proposed wording against the target answer and current filters.

The checker evaluates:
- **Answer leakage**: Flags if the proposed clue accidentally reveals the target answer or core terms.
- **Length**: Reports character count against standard tossup clue lengths.
- **Corpus evidence**: Displays similar matching passages from the index alongside their source set and difficulty.

A result of "No automatic flags" checks wording and corpus presence, but does not establish factual accuracy or uniqueness.

## Export selected clues to CSV

To save clues and sources for note drafting:

1. Tick the checkbox on each clue row you want to keep, or tick **Select clues** in the toolbar to select all visible candidates.
2. Select **Export CSV**.
3. Your browser downloads a CSV file named after the target answer (e.g., `photoelectric-effect-clues.csv`).

The CSV includes:
- `answer`: The target answerline.
- `clue`: The extracted clue or entity name.
- `questions`: Distinct question count on this answer.
- `tied`: Specificity ratio across the entire question corpus.
- `position`: Tossup clue position (`giveaway`, `middle`, `power`, or `bonus`).
- `example`: Representative clue passage.
- `source`: Tournament set, packet, and question number.
- `example_uid`: Local database unit ID for reproducible citation.
- `anki`: Anki coverage status (when compared).
- `category`, `difficulty`, `years`: Filter parameters used for the profile.

If you change the search term or any filter after generating a profile, an update notice appears and the export button disables until you rerun **Find clues** to avoid exporting out-of-sync results.

## Keyboard controls

- **Ctrl+K** (or **⌘K** on macOS): Focuses and selects the main search box.
- **Escape**: Closes the source question reader drawer or any open modal dialog.
- **Enter**: Submits the search form or triggers the focused button.

## Database settings

Select **Index** in the top right header to inspect database status or configure a custom database path:

- Displays total answerable units, sets, and the timestamp of the last successful sync.
- To use an index located outside the default repository directory, enter its path and select **Connect index**.
- Closing the browser window or stopping the terminal session cleanly stops the local server.

## Optional Anki comparison

Open Anki with AnkiConnect enabled, then select **Compare with Anki** under **More options**. Comparisons read notes and card state without modifying the collection. Cached data may be used; the interface reports when it is stale.

| Label | Meaning |
| --- | --- |
| Active match | A matching named note has at least one card that is not suspended. |
| Suspended | A matching named note has only suspended cards. |
| On target note | The clue occurs in the target's own note. |
| Text mention | The clue occurs in note text without a dedicated named match. |
| No match | The comparison found no match. |

Matching is heuristic. Inspect the actual card fronts and templates before concluding that a clue has active retrieval coverage.

## Optional Jupyter notebook interface

If you prefer scripting or interactive notebooks, `StockFisher.ipynb` remains available in the repository root:

```bash
python -m notebook StockFisher.ipynb
```

Select the startup cell and press **Shift+Enter**. The interactive widget controls connect to the same `qbr` engine and local SQLite index. The latest profile results are accessible in Python via `research.result`.

## Troubleshooting

| Symptom | What to do |
| --- | --- |
| App will not open from Windows shortcut | Ensure Python 3.9+ is installed with the Windows Python launcher (`pyw`). Check `%LOCALAPPDATA%\StockFisher\app.log` for startup messages. |
| Port already in use | Run `python -m qbr.app --port 8766` with another port number. |
| Index not connected | Select **Index** in the header and verify the path to `qbreader.sqlite`, or run `python -m qbr sync` to build it. |
| No matching answer | Clear filters, check spelling, and inspect suggested answerlines at the bottom of the empty result notice. |
| Missing expected works | Broaden the category, search distinctive words in **Question text**, and inspect creator profiles. Automatic extraction is incomplete. |
| Export button disabled | Ensure at least one clue is ticked. If filters were edited, select **Find clues** to refresh before exporting. |
| Changes not showing after updating files | Relaunch the app or restart your terminal session to reload Python modules. |

## Programmatic usage from Python

The interface runs on standard Python functions that return structured dictionaries and lists. Scripts can query the index directly:

```python
import qbr

profile = qbr.profile("Damien Hirst", cat="fa", sort="spec", top=15)
for clue in profile["things"]:
    print(clue["thing"], clue["n"], clue["example"])
    if clue.get("example_uid") is not None:
        question = qbr.show(clue["example_uid"])
```

See the [API and command reference](../qbr/README.md) for full-question retrieval, answer frequency, and coverage research.
