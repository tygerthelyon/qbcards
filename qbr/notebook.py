"""Interactive Jupyter controls for the StockFisher search and profiling tools."""
import csv
import html
import sqlite3
import warnings
from datetime import datetime, timezone
from pathlib import Path

import ipywidgets as widgets

import qbr
from . import find, store
from .ui import connect_database, _validate_range


def _escape(value):
    return html.escape(str(value if value is not None else ""))


def _table(headers, rows, profile=False):
    if not rows:
        return "<p class='sf-no-results'>No results to show.</p>"
    heading = "".join("<th>%s</th>" % _escape(h) for h in headers)
    body = "".join(
        "<tr>%s</tr>" % "".join('<td data-label="%s">%s</td>' % (_escape(headers[i]), cell)
                                  for i, cell in enumerate(row))
        for row in rows
    )
    table_class = "sf-table sf-profile-table" if profile else "sf-table"
    return "<div class='sf-table-wrap'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (table_class, heading, body)


def _question_details(uid):
    """Render trusted structure with escaped corpus text, including every bonus part."""
    if uid is None:
        return ""
    result = qbr.show(uid)
    if not result:
        return ""
    question = result["question"]
    source = "%s · packet %s · %s %s · difficulty %s" % (
        question.get("set_name", ""), question.get("packet", "?"),
        "tossup" if question.get("kind") == "T" else "bonus",
        question.get("number", "?"), question.get("difficulty", "?"))
    passages = []
    for unit in result["units"]:
        if unit.get("lead"):
            passages.append("<p>%s</p>" % _escape(unit["lead"]))
        label = "Part %s. " % unit["part"] if unit.get("part") else ""
        passages.append("<p>%s%s</p><p><b>Answer:</b> %s</p>" % (
            label, _escape(unit.get("text", "")), _escape(unit.get("answer", ""))))
    return ("<details class='sf-question'><summary>Read full question</summary>"
            "<p class='sf-meta'>%s · ID %s · unit %s</p>%s</details>" % (
                _escape(source), _escape(question.get("id", "")), uid, "".join(passages)))




_STYLE = "<style>" + Path(__file__).with_suffix(".css").read_text(encoding="utf-8") + "</style>"




class StockFisherNotebook:
    """Build the notebook dashboard. Queries and Anki access are read-only."""

    def __init__(self, answer="photoelectric effect", category="Physics", difficulty="", year="",
                 ranking="spec", limit=15):
        self.result = None
        self.profile_context = None
        self.connected = False
        self.db_path = widgets.Text(value=store.PATH, description="File", layout=widgets.Layout(width="100%"))
        self.db_button = widgets.Button(description="Connect", button_style="")
        self.db_status = widgets.HTML()
        self.db_settings = widgets.Accordion(children=[widgets.VBox([self.db_path, self.db_button])])
        self.db_settings.set_title(0, "Database settings")
        self.db_settings.selected_index = None
        self.db_settings.add_class("sf-database")

        self.answer = widgets.Text(value=answer, description="Answer", placeholder="e.g. Damien Hirst", layout=widgets.Layout(width="340px"))
        self.category = widgets.Combobox(value=category, description="Category", placeholder="All categories", ensure_option=False, layout=widgets.Layout(width="300px"))
        self.difficulty = widgets.Text(value=difficulty, description="Difficulty", placeholder="e.g. 6-9", layout=widgets.Layout(width="230px"))
        self.year = widgets.Text(value=year, description="Years", placeholder="e.g. 2018-", layout=widgets.Layout(width="230px"))
        self.ranking = widgets.Dropdown(options=[("Specificity", "spec"), ("Frequency", "n"), ("Clue position", "pyramid")],
                                        value=ranking, description="Rank by", layout=widgets.Layout(width="245px"))
        self.limit = widgets.BoundedIntText(value=limit, min=1, max=100, description="Clues", layout=widgets.Layout(width="160px"))
        self.exact = widgets.Checkbox(value=False, description="Exact answerline")
        self.use_anki = widgets.Checkbox(value=False, description="Compare with Anki")
        self.exclude = widgets.Text(description="Exclude", placeholder="Terms to exclude, comma-separated", layout=widgets.Layout(width="360px"))

        for field, width in ((self.answer, "100%"), (self.category, "100%"),
                             (self.difficulty, "100%"), (self.year, "100%"),
                             (self.ranking, "156px"), (self.limit, "72px")):
            field.layout.width = width
            field.add_class("sf-field")

        self.profile_button = widgets.Button(description="Find clues", button_style="primary",
                                             layout=widgets.Layout(width="100%"))
        self.profile_button.add_class("sf-primary-action")
        self.profile_status = widgets.HTML()
        self.profile_output = widgets.HTML()
        self.search_query = widgets.Text(description="Search phrase", placeholder="e.g. butterflies OR cocoons", layout=widgets.Layout(width="100%"))
        self.search_button = widgets.Button(description="Search questions", button_style="primary")
        self.search_output = widgets.HTML()
        self.clue_text = widgets.Textarea(description="Clue", placeholder="Write a clue for your chosen answer",
                                          layout=widgets.Layout(width="100%", height="90px"))
        self.check_button = widgets.Button(description="Check clue", button_style="primary")
        self.check_output = widgets.HTML()

        self.selection = widgets.SelectMultiple(options=[], description="Clues", rows=8, layout=widgets.Layout(width="100%"))
        self.select_all = widgets.Button(description="Select all")
        self.clear_selection = widgets.Button(description="Clear")
        self.export_path = widgets.Text(value="stockfisher-clues.csv", description="Save as", layout=widgets.Layout(width="100%"))
        self.export_button = widgets.Button(description="Export selected", button_style="primary")
        self.export_status = widgets.HTML()
        self.context_status = widgets.HTML()
        self.export_context = widgets.HTML("<p>Run a profile to select clues.</p>")

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
            self.exact, self.use_anki, self.exclude,
        ])])
        options.set_title(0, "More options")
        options.selected_index = None
        options.add_class("sf-options")
        actions = widgets.HBox([self.ranking, self.limit])
        actions.add_class("sf-actions")
        profile_tab = widgets.VBox([
            actions, self.profile_status, self.profile_output,
        ])
        search_tab = widgets.VBox([widgets.HTML("<h2 class='sf-panel-title'>Search the questions</h2>"
                                  "<p class='sf-panel-description'>Find a phrase across answers. Category, difficulty, and year filters apply.</p>"),
                                  self.search_query, self.search_button, self.search_output])
        check_tab = widgets.VBox([widgets.HTML("<h2 class='sf-panel-title'>Review a draft clue</h2>"
                                 "<p class='sf-panel-description'>Check for answer words and supporting passages. Use the Answer field for the intended answer.</p>"),
                                 self.clue_text, self.check_button, self.check_output])
        selection_actions = widgets.HBox([self.select_all, self.clear_selection])
        selection_actions.add_class("sf-selection-actions")
        review_tab = widgets.VBox([
            widgets.HTML("<h2 class='sf-panel-title'>Save your shortlist</h2>"
                         "<p class='sf-panel-description'>Select clues from the latest profile to export with their supporting evidence.</p>"),
            self.export_context,
            self.selection, selection_actions, self.export_path,
            self.export_button, self.export_status,
        ])
        for panel in (search_tab, check_tab, review_tab):
            panel.add_class("sf-panel-body")
        self.tabs = widgets.Tab(children=[profile_tab, search_tab, check_tab, review_tab])
        for index, title in enumerate(("Profile", "Search", "Check clue", "Review & export")):
            self.tabs.set_title(index, title)

        range_fields = widgets.HBox([self.difficulty, self.year])
        range_fields.add_class("sf-range-fields")
        fields = widgets.VBox([self.answer, self.category, range_fields])
        fields.add_class("sf-fields")
        filter_help = widgets.HTML("<details class='sf-help'><summary>Filter guide</summary>"
                         "<p>Leave a filter blank to include everything. Category accepts names or shortcuts such as "
                         "Physics, fa, vfa, or vfa,ofa. Older art questions may use Other Fine Arts; "
                         "start with Fine Arts for a broad artist audit.</p>"
                         "<p>Difficulty: 1–10, ranges such as 6-9, or ms / hs / college / open. "
                         "College dots: 6 = one, 7 = two, 8 = three, 9 = four. Years: 2018- or 2015-2020.</p>"
                         "<p>Specificity ranking balances frequency and association with the answer. Frequency ranks by question count; "
                         "Clue position runs from early clues to giveaways. Extraction can miss works and paraphrases; read the full questions.</p></details>")
        sidebar = widgets.VBox([
            widgets.HTML("<p class='sf-section-label'>Research scope</p>"),
            fields, self.profile_button, options, filter_help,
        ])
        sidebar.add_class("sf-sidebar")
        main = widgets.VBox([self.context_status, self.tabs])
        main.add_class("sf-main")
        workbench = widgets.HBox([sidebar, main])
        workbench.add_class("sf-workbench")
        header = widgets.HBox([
            widgets.HTML(_STYLE + "<div class='sf-brand'><span class='sf-mark' aria-hidden='true'><i></i><i></i><i></i></span>"
                         "<div><h1 class='sf-heading'>StockFisher</h1><p class='sf-subtitle'>Quizbowl research</p></div></div>"),
            self.db_status,
        ])
        header.add_class("sf-header")
        self.view = widgets.VBox([header, workbench, self.db_settings],
                                layout=widgets.Layout(max_width="1180px", width="100%"))
        self.view.add_class("stockfisher")

        self.db_button.on_click(self.connect)
        self.profile_button.on_click(self.run_profile)
        self.search_button.on_click(self.run_search)
        self.check_button.on_click(self.check_clue)
        self.select_all.on_click(self._select_all)
        self.clear_selection.on_click(self._clear_selection)
        self.export_button.on_click(self.export)
        for control in (self.answer, self.category, self.difficulty, self.year, self.ranking,
                        self.limit, self.exact, self.use_anki, self.exclude):
            control.observe(self._inputs_changed, names="value")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.answer.on_submit(self.run_profile)
            self.category.on_submit(self.run_profile)
            self.search_query.on_submit(self.run_search)
        self.connect()

    def connect(self, _button=None):
        self.result = None
        self.profile_context = None
        self.context_status.value = ""
        self.export_context.value = "<p>Run a profile to select clues.</p>"
        self.export_button.disabled = True
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
            self.db_status.value = "<p class='sf-error'>Database not connected. %s</p>" % _escape(exc)
            return False
        self.connected = True
        self.category.options = info["categories"]
        synced = (datetime.fromtimestamp(info["synced"], timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
                  if info["synced"] else "unknown")
        self.db_status.value = "<div class='sf-status'><span class='dot'></span><strong>%s units · %s sets</strong><br>Last sync %s</div>" % (
            format(info["units"], ","), format(info["sets"], ","), synced)
        if not self.answer.value.strip():
            self.profile_output.value = (
                "<div class='sf-welcome'>"
                "<h2 class='sf-welcome-title'>Find the clues that recur.</h2>"
                "<p class='sf-welcome-desc'>Start with a person, work, place, or concept. "
                "StockFisher brings recurring clues and their source questions together for review.</p>"
                "<div class='sf-workflow'>"
                "<div><span>01</span><b>Choose an answer</b><p>Enter an answer and select Find clues. Keep filters blank to start broad.</p></div>"
                "<div><span>02</span><b>Read the evidence</b><p>Compare recurring clues and open the questions behind them.</p></div>"
                "<div><span>03</span><b>Build a shortlist</b><p>Select useful clues and export them with their sources.</p></div>"
                "</div>"
                "</div>"
            )
        self.db_settings.selected_index = None
        return True

    def _filters(self):
        _validate_range(self.difficulty.value.strip(), "Difficulty", 1, 10, find.LEVELS)
        _validate_range(self.year.value.strip(), "Years", 1, 2100)
        return {"cat": self.category.value.strip() or None, "diff": self.difficulty.value.strip() or None,
                "year": self.year.value.strip() or None}

    def _context(self):
        return tuple(control.value for control in (self.answer, self.category, self.difficulty,
                     self.year, self.ranking, self.limit, self.exact, self.use_anki, self.exclude))

    def _inputs_changed(self, _change=None):
        self.search_output.value = ""
        self.check_output.value = ""
        stale = self.profile_context is not None and self.profile_context != self._context()
        self.context_status.value = ("<p class='sf-notice'>Inputs changed. Results still show %s. "
                                     "Select Find clues to update them before exporting.</p>" % _escape(self.result["name"])) if stale else ""
        self.export_button.disabled = stale or not bool(self.result and self.result.get("found"))

    def _ready(self, output):
        if self.connected:
            return True
        output.value = "<p>Connect a database in Database settings before running this action.</p>"
        return False

    def run_profile(self, _button=None):
        self.tabs.selected_index = 0
        if not self._ready(self.profile_status):
            return None
        name = self.answer.value.strip()
        if not name:
            self.profile_status.value = "<p>Enter an answer first.</p>"
            return None
        self.result = None
        self.selection.options = []
        self.profile_context = None
        self.context_status.value = ""
        self.export_context.value = "<p>Run a profile to select clues.</p>"
        self.export_button.disabled = True
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
            self.profile_context = self._context()
            if not result.get("found"):
                guesses = ", ".join(_escape(x[0]) for x in result.get("suggest", [])) or "No close answerlines found."
                self.profile_status.value = "<p>No matching answer. %s Try fewer filters or another spelling.</p>" % guesses
                return result
            stats = ("<div class='sf-result-header'><div><h2 class='sf-result-heading'>%s</h2>"
                     "<div class='sf-result-summary'>%s questions · %s tossups · %s bonus parts · %s sets</div></div>"
                     "<span class='sf-result-count'>%s clues shown</span></div>") % (
                _escape(result["name"]), result["questions"], result["tossups"], result["bonuses"], result["sets"],
                len(result.get("things", [])))
            if result.get("mentioned_truncated"):
                stats += "<br><small>Mentions reached the search cap; related-answer counts may be incomplete.</small>"
            if result.get("anki_stale"):
                stats += "<br><small>%s</small>" % _escape(result["anki_stale"])
            self.profile_status.value = stats
            self.export_context.value = "<p><b>Profile:</b> %s · %s · difficulty %s · years %s</p>" % (
                _escape(result["name"]), _escape(self.category.value or "all categories"),
                _escape(self.difficulty.value or "all"), _escape(self.year.value or "all"))
            lines = ", ".join("%s (%s)" % (_escape(line), count) for line, count in result.get("lines", []))
            rows = []
            for clue in result.get("things", []):
                title = "<span class='sf-clue'>%s</span>" % _escape(clue.get("thing"))
                if clue.get("example"):
                    title += "<span class='sf-example'>%s</span><span class='sf-source'>%s</span>" % (_escape(clue["example"]), _escape(clue.get("source", "")))
                title += _question_details(clue.get("example_uid"))
                pos = clue.get("where", "")
                badge_key = pos.replace("-", "").lower() if pos else "bonus"
                pos_html = ("<span class='sf-badge sf-badge-%s'>%s</span>" % (badge_key, _escape(pos))) if pos else ""
                cells = [title, _escape(clue.get("n", 0)), "%.0f%%" % (100 * clue.get("tied", 0)),
                         pos_html]
                if self.use_anki.value:
                    cells.append(_escape({"": "No match", "card": "Active match", "text": "Text mention", "on-note": "On target note", "suspended": "Suspended"}.get(clue.get("anki", ""), clue.get("anki"))))
                rows.append(cells)
            headers = ["Clue and example", "Questions", "Specificity", "Position"] + (["Anki"] if self.use_anki.value else [])
            foils = ", ".join(_escape(foil["answer"]) for foil in result.get("foils", []))
            self.profile_output.value = (_table(headers, rows, profile=True) +
                                         ("<p class='sf-meta'>Related answers: %s</p>" % foils if foils else "") +
                                         "<p class='sf-meta'>Specificity compares this profile's target-associated units with all matching units in the mirror. "
                                         "Ranking also weights frequency. Position summarizes tossups. These are extracted candidates, not complete coverage.</p>" +
                                         "<details class='sf-meta'><summary>Matched answerlines</summary>%s</details>" % (lines or "none"))
            self.selection.options = [("%d. %s" % (i + 1, clue["thing"]), i)
                                      for i, clue in enumerate(result.get("things", []))]
            self.export_button.disabled = not bool(self.selection.options)
            return result
        except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
            self.profile_status.value = "<p class='sf-error'>%s</p>" % _escape(exc)
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
            result = qbr.search(phrase, n=40, **self._filters())
            hits = result.get("hits", [])
            seen_answers = {}
            filtered_hits = []
            for hit in hits:
                akey = hit.get("akey") or hit.get("main")
                if seen_answers.get(akey, 0) < 1:
                    filtered_hits.append(hit)
                    seen_answers[akey] = seen_answers.get(akey, 0) + 1
                if len(filtered_hits) >= 20:
                    break
            if len(filtered_hits) < 15 and len(filtered_hits) < len(hits):
                for hit in hits:
                    if hit not in filtered_hits:
                        filtered_hits.append(hit)
                    if len(filtered_hits) >= 20:
                        break

            rows = []
            for hit in filtered_hits:
                sentences = hit.get("sentences", [])
                excerpt = sentences[0].get("s", "") if sentences else hit.get("text", "")
                rows.append([_escape(hit.get("main")), _escape(hit.get("set_name")), _escape(hit.get("difficulty")),
                             _escape(excerpt) + _question_details(hit.get("uid"))])
            self.search_output.value = (
                "<div class='sf-result-summary'>%s questions · %s answerable units · showing %s examples</div>" % (
                    format(result["questions"], ","), format(result["units"], ","), len(filtered_hits)) +
                "<p class='sf-meta'>Examples favor different answers from the first 40 hits. Narrow the filters to inspect more specific results.</p>" +
                _table(["Answer", "Set", "Difficulty", "Matching passage"], rows)
            )
            return result
        except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
            self.search_output.value = "<p class='sf-error'>%s</p>" % _escape(exc)
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
            self.check_output.value = "<p class='sf-error'>%s</p>" % _escape(exc)
            return None
        finally:
            self.check_button.disabled = False

    def _select_all(self, _button=None):
        self.selection.value = tuple(value for _label, value in self.selection.options)

    def _clear_selection(self, _button=None):
        self.selection.value = ()

    def export(self, _button=None):
        if self.profile_context is not None and self.profile_context != self._context():
            self.export_status.value = "<p>Inputs changed. Select Find clues again before exporting.</p>"
            return None
        if not self.result or not self.result.get("found") or not self.selection.value:
            self.export_status.value = "<p>Profile an answer and select at least one clue first.</p>"
            return None
        path_text = self.export_path.value.strip()
        if not path_text:
            self.export_status.value = "<p>Choose a CSV filename.</p>"
            return None
        path = Path(path_text).expanduser()
        fields = ["answer", "clue", "questions", "tied", "position", "example", "source", "anki", "example_uid",
                  "category", "difficulty", "years"]
        try:
            with path.open("x", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for index in self.selection.value:
                    item = self.result["things"][index]
                    writer.writerow({"answer": self.result["name"], "clue": item.get("thing", ""),
                                     "questions": item.get("n", 0), "tied": item.get("tied", ""),
                                     "position": item.get("where", ""), "example": item.get("example", ""),
                                     "source": item.get("source", ""), "anki": item.get("anki", ""),
                                     "example_uid": item.get("example_uid", ""), "category": self.category.value,
                                     "difficulty": self.difficulty.value, "years": self.year.value})
        except FileExistsError:
            self.export_status.value = "<p>That file already exists. Choose another filename.</p>"
            return None
        except OSError as exc:
            self.export_status.value = "<p class='sf-error'>%s</p>" % _escape(exc)
            return None
        self.export_status.value = "<p>Saved %d clues to %s.</p>" % (len(self.selection.value), _escape(path.resolve()))
        return path

    def display(self):
        """Return the widget to display as the last expression of a notebook cell."""
        return self.view
