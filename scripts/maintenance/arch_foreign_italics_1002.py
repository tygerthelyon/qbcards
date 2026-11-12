"""Italicise foreign-language building names in Architecture captions and text (Carter, 2026-10-02: "do this").

Names: every Foreign=1 note's Name (city suffix dropped) plus foreign names that appear in Works lists, captions,
descriptions, and notes. Places, people, institutions (museums), and "Villa + surname" stay roman, as Villa
Savoye's own card does. Skips text already inside <i>...</i> and inside HTML tags.
Usage: py -3.9 arch_foreign_italics_1002.py [--apply]
"""
import json, os, re, sys, time
import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ["Caption 1", "Caption 2", "Caption 3", "Caption 4", "Description", "Notes", "Works"]
EXTRA = """Notre-Dame de Paris|Notre-Dame de l'Épine|Santa Maria dei Carmini|Palazzo Medici-Riccardi|San Pietro in Montorio|
Palazzo Giusti|Dôme des Invalides|Palau Sant Jordi|La Giralda|San Vitale|San Marco|Porta Especiosa|Palais de la Cité|
Torre del Mangia|La Pedrera|Santa María Tonantzintla|La Madeleine|La Marseillaise|Torre Agbar|San Giovanni Evangelista|
San Giovanni in Fonte|Santa Maria Gloriosa dei Frari|Basílica del Voto Nacional|Santa Giulia|San Salvatore|Palazzo Farnese|
San Francesco|San Bieito de Fefiñáns|Hôtel de Soubise|Salon de la Princesse|Palazzo Te|Palazzo del Te|Palazzo Pitti|
Sala de las Bóvedas|Palazzo Littorio|Tempio Malatestiano|Hôtel Lambert|Hôtel de Brunoy|Château de Louveciennes|
El Mas de la Calderera|Hôtel Solvay|Hôtel van Eetvelde|Hôtel Guimard|Castel Béranger|Palais Stoclet|Unité d'habitation|
Parc de la Villette|Parc de La Villette|Torre Glòries|Cuadra San Cristóbal|El Fureidis|San Zeno|Château de Carcassonne|
Palazzetto dello Sport|Palacio de los Deportes|Santa Cecilia Acatitlan|Palacio Salvo|Tour Saint-Jacques|Saint-Maclou|
Santa María del Salvador|Santa Prisca|La Grande Voile|Santa Croce|Trinità dei Monti|Casa Gilardi|Casa de Vidro|
San Lorenzo|Santo Spirito|Sant'Andrea|Santa Maria Novella|Santa Maria presso San Satiro|Tempietto|Villa Capra|
Il Redentore|Basilica Palladiana|Teatro Olimpico|Sala dei Giganti|Baldacchino|Scala Regia|Sant'Agnese in Agone|
Palazzo Spada|Santa Susanna|Palazzo Barberini|Grand Trianon|Château de Meudon|Château du Raincy|Vaux-le-Vicomte|
Hôtel Alexandre|Rotonde de la Villette|Hôtel d'Hallwyl|Altes Museum|Schauspielhaus|Konzerthaus Berlin|Neue Wache|
Bauakademie|Kirche am Steinhof|Looshaus|Kunsthal|Casa da Música|Maison à Bordeaux|Le Fresnoy|Tour bleue|Kunsthaus Bregenz|
Fondazione Querini Stampalia|Teatro del Mondo|Stadio San Nicola|Felix Nussbaum Haus|Piazza del Campidoglio|Dôme""".replace("\n", "")
ROMAN_CONTEXT = ["San Lorenzo de El Escorial", "Piazza San Marco", "Saint Peter's"]


def names():
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Architecture" Foreign:1'))
    out = set()
    for n in ns:
        nm = C.plain(n["fields"]["Name"]["value"]).strip()
        nm = re.sub(r",\s*[A-Z][\w ]+$", "", nm)          # "Frauenkirche, Dresden" -> "Frauenkirche"
        nm = re.sub(r"\s+in\s+Chichen Itza$", "", nm)
        if nm: out.add(nm)
    out |= {x.strip() for x in EXTRA.split("|") if x.strip()}
    return sorted(out, key=len, reverse=True)


def italicise(val, pat):
    res, i = [], 0
    for m in pat.finditer(val):
        s, e = m.span()
        pre = val[:s]
        if pre.count("<i>") > pre.count("</i>"): continue              # already italic
        if pre.rfind("<") > pre.rfind(">"): continue                     # inside a tag
        ctx = val[max(0, s - 30):e + 30]
        if any(r in ctx and r.find(m.group(0)) >= 0 for r in ROMAN_CONTEXT): continue
        res.append(val[i:s]); res.append("<i>" + m.group(0) + "</i>"); i = e
    res.append(val[i:])
    return "".join(res)


def main(apply):
    nm = names()
    pat = re.compile(r"(?<![\w'-])(?:" + "|".join(re.escape(x) for x in nm) + r")(?![\w-])")
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Architecture"'))
    changes, backup = {}, {}
    for n in ns:
        new = {}
        for f in FIELDS:
            v = n["fields"][f]["value"]
            w = italicise(v, pat)
            if w != v: new[f] = w
        if new:
            changes[n["noteId"]] = new
            backup[n["noteId"]] = {f: n["fields"][f]["value"] for f in new}
            for f, w in new.items():
                print("#%d %s | %s: %s" % (n["noteId"], C.plain(n["fields"]["Name"]["value"])[:28], f, w[:220]))
    print("notes", len(changes), "fields", sum(len(v) for v in changes.values()))
    if not apply: return
    json.dump(backup, open(os.path.join(HERE, "backups", "arch_foreign_italics_%s.json" % time.strftime("%Y%m%d_%H%M%S")), "w", encoding="utf-8"), ensure_ascii=False)
    for k, new in changes.items():
        C.anki("updateNoteFields", note={"id": k, "fields": new})
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
