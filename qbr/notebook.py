"""Interactive Jupyter controls for the StockFisher search and profiling tools."""
import csv
import html
import sqlite3
from pathlib import Path

import ipywidgets as widgets

import qbr
from . import anki, store


def _escape(value):
    return html.escape(str(value if value is not None else ""))


def _table(headers, rows):
    if not rows:
        return "<p>No results to show.</p>"
    heading = "".join("<th>%s</th>" % _escape(h) for h in headers)
    body = "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % cell for cell in row)
        for row in rows
    )
    return "<table class='sf-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (heading, body)


_STYLE = """<style>
.stockfisher {color:#202a35; font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:#fff; border:1px solid #dfe5eb; border-radius:10px; padding:22px 24px; box-sizing:border-box;}
.stockfisher .sf-heading {font-size:19px; font-weight:600; letter-spacing:-.02em; margin:0 0 2px; color:#182535;}
.stockfisher .sf-subtitle {color:#667687; margin:0 0 12px; font-size:13px;}
.stockfisher .sf-status {color:#607181; font-size:12px; margin:0 0 14px;}
.stockfisher .sf-status .dot {display:inline-block; width:7px; height:7px; border-radius:50%; background:#4c9b76; margin-right:6px;}
.stockfisher .widget-tab > .p-TabBar {margin-top:14px;}
.stockfisher .widget-tab .p-TabBar-tab {font-size:13px; text-transform:none; background:#f7f9fb;
  color:#526578; border-color:#e4eaf0;}
.stockfisher .widget-tab .p-TabBar-tab.p-mod-current {background:#fff; color:#1b4a72;
  border-top:2px solid #467ba4;}
.stockfisher .widget-tab-contents {padding:14px 4px 4px !important; border:0 !important;}
.stockfisher .widget-label {font-size:13px; color:#425363;}
.stockfisher input, .stockfisher textarea, .stockfisher select {font-size:13px; border:1px solid #d5dfe8;
  border-radius:4px; background:#fff;}
.stockfisher .sf-table {width:100%; border-collapse:collapse; margin:12px 0; font-size:13px;}
.stockfisher .sf-table th {text-align:left; padding:9px 10px; color:#68798a; font-size:11px; font-weight:600;
  border-bottom:1px solid #dfe5eb; white-space:nowrap;}
.stockfisher .sf-table td {padding:12px 10px; border-bottom:1px solid #edf0f3; vertical-align:top; line-height:1.5;}
.stockfisher .sf-clue {font-weight:600; color:#253c56;}
.stockfisher .sf-example {display:block; color:#5d6b78; margin-top:4px;}
.stockfisher .sf-source {display:block; color:#8a98a5; font-size:11px; margin-top:3px;}
.stockfisher .sf-meta {color:#68798a; font-size:12px;}
.stockfisher details.sf-meta {margin:10px 0;}
.stockfisher details.sf-meta summary {cursor:pointer;}
</style>"""


def connect_database(path):
    """Validate and select an existing mirror. The database is opened read-only."""
    db_path = Path(path).expanduser().resolve()
    if not db_path.is_file():
        raise FileNotFoundError("Mirror not found. Choose an existing qbreader.sqlite file.")
    con = sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True, timeout=10)
    try:
        tables = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')")}
        if not {"u", "q", "f", "sets", "meta"}.issubset(tables):
            raise ValueError("This file does not have the expected StockFisher mirror tables.")
        units = con.execute("SELECT count(*) FROM u").fetchone()[0]
        sets = con.execute("SELECT count(*) FROM sets").fetchone()[0]
    finally:
        con.close()

    if store._CON is not None:
        store._CON.close()
        store._CON = None
    store.PATH = str(db_path)
    anki.CACHE = str(db_path.parent / "anki_index.json")
    return {"path": str(db_path), "units": units, "sets": sets}


class StockFisherNotebook:
    """Build the notebook dashboard. Queries and Anki access are read-only."""

    def __init__(self, answer="photoelectric effect", category="Physics", difficulty="", year="",
                 ranking="spec", limit=15):
        self.result = None
        self.connected = False
        self.db_path = widgets.Text(value=store.PATH, description="Mirror", layout=widgets.Layout(width="100%"))
        self.db_button = widgets.Button(description="Connect", icon="database", button_style="")
        self.db_status = widgets.HTML()
        self.db_settings = widgets.Accordion(children=[widgets.VBox([self.db_path, self.db_button])])
        self.db_settings.set_title(0, "Database settings")
        self.db_settings.selected_index = None

        self.answer = widgets.Text(value=answer, description="Answer", layout=widgets.Layout(width="340px"))
        self.category = widgets.Text(value=category, description="Category", layout=widgets.Layout(width="300px"))
        self.difficulty = widgets.Text(value=difficulty, description="Difficulty", placeholder="e.g. 6-9", layout=widgets.Layout(width="230px"))
        self.year = widgets.Text(value=year, description="Years", placeholder="e.g. 2018-", layout=widgets.Layout(width="230px"))
        self.ranking = widgets.Dropdown(options=[("Specificity", "spec"), ("Frequency", "n"), ("Clue position", "pyramid")],
                                        value=ranking, description="Rank by", layout=widgets.Layout(width="245px"))
        self.limit = widgets.BoundedIntText(value=limit, min=1, max=100, description="Clues", layout=widgets.Layout(width="160px"))
        self.exact = widgets.Checkbox(value=False, description="Exact answerline")
        self.use_anki = widgets.Checkbox(value=False, description="Compare with Anki")
        self.exclude = widgets.Text(description="Exclude", placeholder="Terms to exclude, comma-separated", layout=widgets.Layout(width="360px"))

        self.profile_button = widgets.Button(description="Find stock clues", icon="search", button_style="primary")
        self.profile_status = widgets.HTML()
        self.profile_output = widgets.HTML()
        self.search_query = widgets.Text(description="Phrase", placeholder="A clue, phrase, or FTS query", layout=widgets.Layout(width="100%"))
        self.search_button = widgets.Button(description="Search questions", icon="search")
        self.search_output = widgets.HTML()
        self.clue_text = widgets.Textarea(description="Clue", placeholder="Write a draft clue for the answer above",
                                          layout=widgets.Layout(width="100%", height="90px"))
        self.check_button = widgets.Button(description="Check clue", icon="check")
        self.check_output = widgets.HTML()

        self.selection = widgets.SelectMultiple(options=[], description="Clues", rows=8, layout=widgets.Layout(width="100%"))
        self.select_all = widgets.Button(description="Select all")
        self.clear_selection = widgets.Button(description="Clear")
        self.export_path = widgets.Text(value="stockfisher-clues.csv", description="Save as", layout=widgets.Layout(width="100%"))
        self.export_button = widgets.Button(description="Export selected", icon="download")
        self.export_status = widgets.HTML()

        profile_tab = widgets.VBox([
            widgets.HBox([self.ranking, self.limit]), widgets.HBox([self.exact, self.use_anki]), self.exclude,
            self.profile_button, self.profile_status, self.profile_output,
        ])
        search_tab = widgets.VBox([widgets.HTML("<p>Search question text using the category, difficulty, and year filters above.</p>"),
                                  self.search_query, self.search_button, self.search_output])
        check_tab = widgets.VBox([widgets.HTML("<p>Check a draft for answer leakage and corpus evidence. Review the sources before using it.</p>"),
                                 self.clue_text, self.check_button, self.check_output])
        review_tab = widgets.VBox([
            widgets.HTML("<p>After profiling an answer, select clues to save. The CSV contains evidence and is not an Anki deck.</p>"),
            self.selection, widgets.HBox([self.select_all, self.clear_selection]), self.export_path,
            self.export_button, self.export_status,
        ])
        self.tabs = widgets.Tab(children=[profile_tab, search_tab, check_tab, review_tab])
        for index, title in enumerate(("Profile", "Search", "Check clue", "Review & export")):
            self.tabs.set_title(index, title)

        self.view = widgets.VBox([
            widgets.HTML(_STYLE + "<div class='sf-heading'>StockFisher</div><p class='sf-subtitle'>Find recurring clues in QBReader questions.</p>"),
            self.db_status,
            widgets.HBox([self.answer, self.category], layout=widgets.Layout(flex_flow="row wrap")),
            widgets.HBox([self.difficulty, self.year], layout=widgets.Layout(flex_flow="row wrap")),
            self.tabs, self.db_settings,
        ], layout=widgets.Layout(max_width="940px", width="100%"))
        self.view.add_class("stockfisher")

        self.db_button.on_click(self.connect)
        self.profile_button.on_click(self.run_profile)
        self.search_button.on_click(self.run_search)
        self.check_button.on_click(self.check_clue)
        self.select_all.on_click(self._select_all)
        self.clear_selection.on_click(self._clear_selection)
        self.export_button.on_click(self.export)
        self.connect()

    def connect(self, _button=None):
        self.result = None
        self.selection.options = []
        self.export_status.value = ""
        self.profile_status.value = ""
        self.profile_output.value = ""
        self.search_output.value = ""
        self.check_output.value = ""
        try:
            info = connect_database(self.db_path.value.strip())
        except (OSError, sqlite3.Error, ValueError) as exc:
            self.connected = False
            self.db_settings.selected_index = 0
            self.db_status.value = "<p style='color:#a33'>Mirror not connected. %s</p>" % _escape(exc)
            return False
        self.connected = True
        self.db_status.value = "<p class='sf-status'><span class='dot'></span>QBReader index connected · %s units · %s sets</p>" % (
            format(info["units"], ","), format(info["sets"], ","))
        self.db_settings.selected_index = None
        return True

    def _filters(self):
        return {"cat": self.category.value.strip() or None, "diff": self.difficulty.value.strip() or None,
                "year": self.year.value.strip() or None}

    def _ready(self, output):
        if self.connected:
            return True
        output.value = "<p>Connect a mirror above before running this action.</p>"
        return False

    def run_profile(self, _button=None):
        if not self._ready(self.profile_status):
            return None
        name = self.answer.value.strip()
        if not name:
            self.profile_status.value = "<p>Enter an answer first.</p>"
            return None
        self.result = None
        self.selection.options = []
        self.export_status.value = ""
        self.profile_output.value = ""
        self.profile_status.value = "<p>Searching the mirror…</p>"
        self.profile_button.disabled = True
        try:
            result = qbr.profile(name, sort=self.ranking.value, top=self.limit.value,
                                 exact=self.exact.value, anki=self.use_anki.value,
                                 exclude=[s.strip() for s in self.exclude.value.split(",") if s.strip()],
                                 **self._filters())
            self.result = result
            if not result.get("found"):
                guesses = ", ".join(_escape(x[0]) for x in result.get("suggest", [])) or "No close answerlines found."
                self.profile_status.value = "<p>No matching answer. %s</p>" % guesses
                return result
            stats = "%s · %s questions · %s tossups · %s bonus parts · %s sets" % (
                _escape(result["name"]), result["questions"], result["tossups"], result["bonuses"], result["sets"])
            if result.get("mentioned_truncated"):
                stats += "<br><small>Mentions reached the search cap; related-answer counts may be incomplete.</small>"
            if result.get("anki_stale"):
                stats += "<br><small>%s</small>" % _escape(result["anki_stale"])
            self.profile_status.value = "<p>%s</p>" % stats
            lines = ", ".join("%s (%s)" % (_escape(line), count) for line, count in result.get("lines", []))
            rows = []
            for clue in result.get("things", []):
                title = "<span class='sf-clue'>%s</span>" % _escape(clue.get("thing"))
                if clue.get("example"):
                    title += "<span class='sf-example'>%s</span><span class='sf-source'>%s</span>" % (_escape(clue["example"]), _escape(clue.get("source", "")))
                cells = [title, _escape(clue.get("n", 0)), "%.0f%%" % (100 * clue.get("tied", 0)),
                         _escape(clue.get("where", ""))]
                if self.use_anki.value:
                    cells.append(_escape(clue.get("anki", "")))
                rows.append(cells)
            headers = ["Clue and example", "Questions", "Specificity", "Position"] + (["Anki"] if self.use_anki.value else [])
            foils = ", ".join(_escape(foil["answer"]) for foil in result.get("foils", []))
            self.profile_output.value = ("<details class='sf-meta'><summary>Matched answerlines</summary>%s</details>" % (lines or "none") +
                                         _table(headers, rows) +
                                         ("<p>Related answers: %s</p>" % foils if foils else "") +
                                         "<p class='sf-meta'>Specificity is the share of clue occurrences associated with this answer. Position summarizes tossups.</p>")
            self.selection.options = [("%d. %s" % (i + 1, clue["thing"]), i)
                                      for i, clue in enumerate(result.get("things", []))]
            return result
        except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
            self.profile_status.value = "<p style='color:#a33'>%s</p>" % _escape(exc)
            return None
        finally:
            self.profile_button.disabled = False

    def run_search(self, _button=None):
        if not self._ready(self.search_output):
            return None
        phrase = self.search_query.value.strip()
        if not phrase:
            self.search_output.value = "<p>Enter a search phrase first.</p>"
            return None
        self.search_output.value = "<p>Searching the mirror…</p>"
        self.search_button.disabled = True
        try:
            result = qbr.search(phrase, n=20, **self._filters())
            rows = []
            for hit in result.get("hits", []):
                sentences = hit.get("sentences", [])
                excerpt = sentences[0].get("s", "") if sentences else hit.get("text", "")
                rows.append([_escape(hit.get("main")), _escape(hit.get("set_name")), _escape(hit.get("difficulty")), _escape(excerpt)])
            self.search_output.value = "<p>%s questions · %s answerable units</p>" % (result["questions"], result["units"]) + _table(
                ["Answer", "Set", "Difficulty", "Matching passage"], rows)
            return result
        except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
            self.search_output.value = "<p style='color:#a33'>%s</p>" % _escape(exc)
            return None
        finally:
            self.search_button.disabled = False

    def check_clue(self, _button=None):
        if not self._ready(self.check_output):
            return None
        name, clue = self.answer.value.strip(), self.clue_text.value.strip()
        if not name or not clue:
            self.check_output.value = "<p>Enter both an answer and a draft clue.</p>"
            return None
        self.check_output.value = "<p>Checking the clue…</p>"
        self.check_button.disabled = True
        try:
            result = qbr.verify_clue(name, clue, **self._filters())
            label = "No automatic flags" if result["ok"] else "Review needed"
            leaks = ", ".join(_escape(word) for word in result.get("leaks", [])) or "none"
            rows = [[_escape(t["term"]), _escape(t["n"]), _escape(t["all"]), "%.0f%%" % (100 * t["tied"])]
                    for t in result.get("terms", [])]
            similar = "".join("<li>%s — %s: %s</li>" % (_escape(s[1]), _escape(s[3]), _escape(s[4]))
                              for s in result.get("similar", [])[:5])
            self.check_output.value = ("<p><b>%s</b> · %s characters · answer words found: %s</p>" %
                                       (label, result["length"], leaks) + _table(["Term", "On answer", "All", "Tied"], rows) +
                                       ("<p><b>Similar passages</b></p><ul>%s</ul>" % similar if similar else "") +
                                       "<p><small>This is a diagnostic, not a factual guarantee.</small></p>")
            return result
        except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
            self.check_output.value = "<p style='color:#a33'>%s</p>" % _escape(exc)
            return None
        finally:
            self.check_button.disabled = False

    def _select_all(self, _button=None):
        self.selection.value = tuple(value for _label, value in self.selection.options)

    def _clear_selection(self, _button=None):
        self.selection.value = ()

    def export(self, _button=None):
        if not self.result or not self.result.get("found") or not self.selection.value:
            self.export_status.value = "<p>Profile an answer and select at least one clue first.</p>"
            return None
        path_text = self.export_path.value.strip()
        if not path_text:
            self.export_status.value = "<p>Choose a CSV filename.</p>"
            return None
        path = Path(path_text).expanduser()
        fields = ["answer", "clue", "questions", "tied", "position", "example", "source", "anki"]
        try:
            with path.open("x", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for index in self.selection.value:
                    item = self.result["things"][index]
                    writer.writerow({"answer": self.result["name"], "clue": item.get("thing", ""),
                                     "questions": item.get("n", 0), "tied": item.get("tied", ""),
                                     "position": item.get("where", ""), "example": item.get("example", ""),
                                     "source": item.get("source", ""), "anki": item.get("anki", "")})
        except FileExistsError:
            self.export_status.value = "<p>That file already exists. Choose another filename.</p>"
            return None
        except OSError as exc:
            self.export_status.value = "<p style='color:#a33'>%s</p>" % _escape(exc)
            return None
        self.export_status.value = "<p>Saved %d clues to %s.</p>" % (len(self.selection.value), _escape(path))
        return path

    def display(self):
        """Return the widget to display as the last expression of a notebook cell."""
        return self.view
