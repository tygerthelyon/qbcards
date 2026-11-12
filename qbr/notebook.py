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


def _table(headers, rows, profile=False):
    if not rows:
        return "<p>No results to show.</p>"
    heading = "".join("<th>%s</th>" % _escape(h) for h in headers)
    body = "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % cell for cell in row)
        for row in rows
    )
    table_class = "sf-table sf-profile-table" if profile else "sf-table"
    return "<table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (table_class, heading, body)


_STYLE = """<style>
.stockfisher {
  --ink:#202723; --muted:#5e6a64; --rule:#c9d1cb; --accent:#315b4b;
  box-sizing:border-box; color:var(--ink); background:#fdfdfb;
  border:1px solid #aebbb2; padding:22px 26px 18px;
  font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
.stockfisher .sf-heading {font-size:22px; font-weight:650; letter-spacing:-.035em; line-height:1.2; color:#1e3026;}
.stockfisher .sf-subtitle {color:#596760; font-size:13px; margin:4px 0 0;}
.stockfisher .sf-status {font:12px/1.4 ui-monospace,Consolas,monospace; color:#50665a;
  margin:12px 0 16px; padding:0 0 11px; border-bottom:1px solid #c9d1cb;}
.stockfisher .sf-status .dot {display:inline-block; width:6px; height:6px; background:#558467; margin-right:8px;}
.stockfisher .sf-fields {display:flex; flex-wrap:wrap; gap:14px; box-sizing:border-box;}
.stockfisher .sf-field {display:flex !important; flex-direction:column !important; align-items:stretch !important; gap:4px;}
.stockfisher .sf-field > .widget-label {width:auto !important; min-width:0 !important; text-align:left !important;
  padding:0 !important; margin:0 !important; color:#4d5c53; font:12px/18px ui-monospace,Consolas,monospace;}
.stockfisher .sf-field > input, .stockfisher .sf-field > select, .stockfisher .sf-field > textarea {
  box-sizing:border-box; width:100% !important; height:34px !important; min-height:34px !important;
  padding:6px 9px !important; color:#17251d; background:#fff !important; border:1px solid #aebbb2 !important;
  border-radius:0 !important; box-shadow:none !important; font-size:13px;}
.stockfisher .sf-field > select {appearance:auto !important; padding-right:24px !important;}
.stockfisher .sf-long > textarea {height:90px !important; resize:vertical;}
.stockfisher .sf-field > input:focus, .stockfisher .sf-field > select:focus,
.stockfisher .sf-field > textarea:focus {outline:2px solid #71927f; outline-offset:1px;}
.stockfisher .widget-tab-bar {margin:12px 0 0 !important; border-bottom:1px solid #aebbb2 !important;}
.stockfisher .widget-tab-bar .lm-TabBar-content {gap:18px;}
.stockfisher .widget-tab-bar .lm-TabBar-tab {background:transparent !important; border:0 !important;
  border-bottom:2px solid transparent !important; margin:0 !important; padding:0 1px 8px !important;
  color:#596a60 !important; font-size:13px !important; min-width:0 !important;}
.stockfisher .widget-tab-bar .lm-TabBar-tab.lm-mod-current {color:#1e4632 !important; border-bottom-color:#315b4b !important;}
.stockfisher .widget-tab-bar .lm-TabBar-tab::before {display:none !important;}
.stockfisher .widget-tab-contents {padding:12px 0 0 !important; border:0 !important;}
.stockfisher .sf-actions {display:flex; flex-wrap:wrap; align-items:flex-end; gap:12px;}
.stockfisher .sf-actions .widget-button {height:34px !important; margin:0 0 5px !important; padding:0 14px !important;
  border:1px solid #315b4b !important; border-radius:0 !important; background:#315b4b !important;
  color:#fff !important; font-size:13px; font-weight:600; box-shadow:none !important;}
.stockfisher .sf-actions .widget-button:hover {background:#234738 !important;}
.stockfisher .sf-button:not(.mod-primary) {height:34px !important; padding:0 14px !important;
  border:1px solid #9eafa4 !important; border-radius:0 !important; background:#fff !important;
  color:#2e4d3b !important; font-size:13px; box-shadow:none !important;}
.stockfisher .sf-button:not(.mod-primary):hover {background:#f0f4f0 !important;}
.stockfisher .sf-options {margin:0 0 3px;}
.stockfisher .sf-options .jupyter-widget-Collapse-header,
.stockfisher .sf-database .jupyter-widget-Collapse-header {background:transparent !important; border:0 !important;
  color:#536b5d !important; padding:6px 0 !important; font-size:12px; font-weight:500;}
.stockfisher .sf-options .widget-checkbox {width:auto !important; margin-right:20px;}
.stockfisher .sf-options .widget-checkbox > .widget-label {display:none;}
.stockfisher .sf-options .jupyter-widget-Collapse-contents,
.stockfisher .sf-database .jupyter-widget-Collapse-contents {border:0 !important; padding:4px 0 10px !important;}
.stockfisher .sf-database {margin-top:10px; border-top:1px solid #d9e0db;}
.stockfisher .sf-result-heading {font-size:17px; font-weight:600; color:#1d2c24; margin:13px 0 2px;}
.stockfisher .sf-result-summary {font:12px/1.5 ui-monospace,Consolas,monospace; color:#596960; margin:0 0 9px;}
.stockfisher .sf-table {width:100%; border-collapse:collapse; margin:8px 0; font-size:13px;}
.stockfisher .sf-table th {text-align:left; padding:8px 8px; color:#4f6156;
  font:12px/1.3 ui-monospace,Consolas,monospace; border-top:1px solid #aebbb2; border-bottom:1px solid #aebbb2; white-space:nowrap;}
.stockfisher .sf-table td {padding:11px 8px; border-bottom:1px solid #e0e5e1; vertical-align:top; line-height:1.45;}
.stockfisher .sf-profile-table th:not(:first-child), .stockfisher .sf-profile-table td:not(:first-child) {text-align:right; white-space:nowrap;}
.stockfisher .sf-profile-table td:not(:first-child) {font:12px/1.5 ui-monospace,Consolas,monospace; color:#34483b;}
.stockfisher .sf-clue {font-weight:600; color:#203a2b;}
.stockfisher .sf-example {display:block; color:#44554c; margin-top:4px;}
.stockfisher .sf-source {display:block; color:#697b70; font-size:11px; margin-top:3px;}
.stockfisher .sf-meta {color:#62726a; font-size:12px;}
.stockfisher details.sf-meta {margin:10px 0;}
.stockfisher details.sf-meta summary {cursor:pointer;}
@media (max-width:620px) {.stockfisher {padding:18px 14px;} .stockfisher .widget-tab-bar .lm-TabBar-content {gap:9px;}}
</style>"""


def connect_database(path):
    """Validate and select an existing mirror. The database is opened read-only."""
    db_path = Path(path).expanduser().resolve()
    if not db_path.is_file():
        raise FileNotFoundError("Database not found. Choose an existing qbreader.sqlite file.")
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
        self.db_path = widgets.Text(value=store.PATH, description="File", layout=widgets.Layout(width="100%"))
        self.db_button = widgets.Button(description="Connect", icon="database", button_style="")
        self.db_status = widgets.HTML()
        self.db_settings = widgets.Accordion(children=[widgets.VBox([self.db_path, self.db_button])])
        self.db_settings.set_title(0, "Database settings")
        self.db_settings.selected_index = None
        self.db_settings.add_class("sf-database")

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

        for field, width, grow in ((self.answer, "230px", "2 1 210px"),
                                   (self.category, "170px", "1 1 150px"),
                                   (self.difficulty, "120px", "1 1 110px"),
                                   (self.year, "120px", "1 1 110px"),
                                   (self.ranking, "190px", "0 1 190px"),
                                   (self.limit, "95px", "0 1 95px")):
            field.layout.width = width
            field.layout.flex = grow
            field.layout.height = "66px"
            field.add_class("sf-field")

        self.profile_button = widgets.Button(description="Find clues", icon="search", button_style="primary",
                                             layout=widgets.Layout(width="130px"))
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

        for field in (self.exclude, self.db_path, self.search_query, self.export_path):
            field.add_class("sf-field")
            field.layout.height = "74px"
        self.clue_text.add_class("sf-field")
        self.clue_text.add_class("sf-long")
        self.clue_text.layout.height = "128px"
        for button in (self.db_button, self.search_button, self.check_button, self.select_all,
                       self.clear_selection, self.export_button):
            button.add_class("sf-button")
        for button, width in ((self.db_button, "110px"), (self.search_button, "160px"),
                              (self.check_button, "130px"), (self.select_all, "100px"),
                              (self.clear_selection, "80px"), (self.export_button, "160px")):
            button.layout.width = width

        options = widgets.Accordion(children=[widgets.VBox([
            widgets.HBox([self.exact, self.use_anki], layout=widgets.Layout(flex_flow="row wrap")), self.exclude,
        ])])
        options.set_title(0, "More options")
        options.selected_index = None
        options.add_class("sf-options")
        actions = widgets.HBox([self.ranking, self.limit, self.profile_button])
        actions.add_class("sf-actions")
        profile_tab = widgets.VBox([
            actions, options, self.profile_status, self.profile_output,
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

        fields = widgets.HBox([self.answer, self.category, self.difficulty, self.year])
        fields.add_class("sf-fields")
        self.view = widgets.VBox([
            widgets.HTML(_STYLE + "<div class='sf-heading'>StockFisher</div><p class='sf-subtitle'>Find recurring clues in QBReader questions.</p>"),
            self.db_status,
            fields,
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
            self.db_status.value = "<p style='color:#a33'>Database not connected. %s</p>" % _escape(exc)
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
        output.value = "<p>Connect a database in Database settings before running this action.</p>"
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
            stats = "<div class='sf-result-heading'>%s</div><div class='sf-result-summary'>%s questions · %s tossups · %s bonus parts · %s sets</div>" % (
                _escape(result["name"]), result["questions"], result["tossups"], result["bonuses"], result["sets"])
            if result.get("mentioned_truncated"):
                stats += "<br><small>Mentions reached the search cap; related-answer counts may be incomplete.</small>"
            if result.get("anki_stale"):
                stats += "<br><small>%s</small>" % _escape(result["anki_stale"])
            self.profile_status.value = stats
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
            self.profile_output.value = (_table(headers, rows, profile=True) +
                                         ("<p>Related answers: %s</p>" % foils if foils else "") +
                                         "<p class='sf-meta'>Specificity is the share of clue occurrences associated with this answer. Position summarizes tossups.</p>" +
                                         "<details class='sf-meta'><summary>Matched answerlines</summary>%s</details>" % (lines or "none"))
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
