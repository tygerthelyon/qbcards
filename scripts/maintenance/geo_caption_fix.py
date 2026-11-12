# -*- coding: utf-8 -*-
"""geo_caption_fix.py -- Geography photo captions that were pasted Wikipedia sentences.

Part of the 2026-09-27 audit ("every single card"): captions carrying citation stubs ("[122", "[4"),
trivia unrelated to the picture, or whole sentences are cut to what the photo shows.

    py -3.9 geo_caption_fix.py [--apply]
"""
import json
import sys
import time

import concept_add as C

CAP = {
    "Afghanistan": "Tents of nomads in Badghis Province",
    "Albania": "Shkodër (ancient Scodra) from Rozafa Castle",
    "Andorra": "Andorra la Vella in 1986",
    "Antigua and Barbuda": "Antigua's lights seen from Barbuda's south coast",
    "Argentina": "Aconcagua, the highest peak outside Asia",
    "Armenia": "The first-century Garni Temple",
    "Asia": "Singapore's downtown and the Singapore River",
    "Azerbaijan": "Petroglyphs in Gobustan National Park",
    "Belgium": "The Palace of the Nation, seat of the Federal Parliament, Brussels",
    "Bolivia": "The Kalasasaya temple at Tiwanaku",
    "Bosnia and Herzegovina": "Stari Most, the Old Bridge at Mostar",
    "British Virgin Islands": "Ruins of St. Phillip's Church, Tortola",
    "Bulgaria": "Independence Square, Sofia",
    "Cambodia": "Koh Tonsay (Rabbit Island)",
    "Cameroon": "Unity Palace, the presidential residence, Yaoundé",
    "Caspian Sea": "Hyrcanian forest on Iran's Caspian slopes",
    "Chile": "Santiago Metropolitan Cathedral",
    "Colorado": "Trains meeting in Glenwood Canyon on the Colorado River",
    "Connecticut": "The Pearl Harbor Memorial (“Q”) Bridge over the Quinnipiac River, New Haven",
    "Costa Rica": "The ruined church at Ujarrás (1686–1693), Orosí Valley",
    "Cyprus": "Kyrenia Castle",
    "Czech Republic": "Wenceslas Square, Prague",
    "Democratic Republic of the Congo": "Villagers displaced by fighting in North Kivu, 2012",
    "Delaware": "Blackbird Pond, New Castle County",
    "Dominican Republic": "Santa María la Menor, the oldest cathedral in the Americas, Santo Domingo",
    "Egypt": "Cleopatra VII and Caesarion in relief, Temple of Dendera",
    "Eritrea": "The Mosque of the Companions, Massawa",
    "Falkland Islands": "Stanley, the capital",
    "Faroe Islands": "Skipanes, on Eysturoy",
    "Finland": "Senate Square, Helsinki",
    "France": "The Maison Carrée, a Roman temple in Nîmes",
    "French Polynesia": "A palm-lined lagoon beach",
    "Germany": "The Reichstag, seat of the Bundestag, Berlin",
    "Ghana": "Elmina Castle, built by the Portuguese in 1482",
    "Greenland": "Sermiligaaq, a village in East Greenland",
    "Guinea": "The Grand Mosque of Conakry",
    "Guyana": "Kaieteur Falls",
    "Honduras": "The Fortaleza de San Fernando de Omoa",
    "Indiana": "A Lake Michigan beach beside steel mills",
    "Iran": "The Presidential Administration building, Tehran",
    "Iraq": "Shanidar Cave, where Neanderthal remains were found",
    "Ireland": "The Uragh Stone Circle, County Kerry",
    "Italy": "Mont Blanc (Monte Bianco) from the Aosta Valley",
    "Kansas": "Wheat under a summer storm",
    "Kentucky": "Lake Cumberland",
    "Kenya": "Lake Turkana",
    "Kuwait": "The Marine Museum, Kuwait City",
    "Kyzylkum Desert": "Bukhara's Kalyan Minaret, on the desert's southern edge",
    "Lake Balkhash": "Turquoise meltwater in April 2023",
    "Lake Erie": "From the International Space Station, 2022",
    "Lake Geneva": "Geneva, where the Rhône leaves the lake, from the air",
    "Lake Michigan": "The northern lake and its islands from the International Space Station, 2022",
    "Lake Taupo": "Māori rock carvings at Mine Bay",
    "Lake Titicaca": "From Copacabana, Bolivia",
    "Lake Vänern": "From the Gamla Ekudden nature reserve",
    "Laos": "Ruins of Muang Khoun, bombed in the 1960s",
    "Lazio": "The Colosseum, Rome",
    "Libya": "The Atiq Mosque at Awjila, the oldest in the Sahara",
    "Liechtenstein": "Vaduz Castle, the Prince's residence",
    "Luxembourg": "The Chamber of Deputies, Luxembourg City",
    "Malaysia": "Mount Kinabalu before sunrise, Sabah",
    "Mali": "The monument to the “Armée Noire”, Bamako",
    "Malta": "Ġgantija, a megalithic temple complex on Gozo",
    "Manicouagan Reservoir": "The Daniel-Johnson Dam, which holds back the reservoir",
    "Mauritania": "Nouakchott, the capital",
    "Mayotte": "Lake Dziani, a volcanic crater lake on Petite-Terre",
    "Michigan": "Mackinac Island in the Straits of Mackinac",
    "Minnesota": "Tilted rock beds in Jay Cooke State Park",
    "Missouri": "Bell Mountain Wilderness, Mark Twain National Forest",
    "Monaco": "La Condamine, Fontvieille, and the Rock with the Prince's Palace",
    "Mozambique": "The Island of Mozambique, the former capital",
    "Myanmar": "Temples of Bagan",
    "Nauru": "Coral pinnacles on the coast",
    "Nepal": "Changu Narayan Temple",
    "New Zealand": "Queen Street, Auckland",
    "Nicaragua": "Granada, on Lake Nicaragua",
    "North Korea": "The Mansudae Grand Monument, Pyongyang",
    "North Macedonia": "Heraclea Lyncestis, founded by Philip II of Macedon",
    "North Rhine-Westphalia": "Gerard ter Borch, <i>The Ratification of the Treaty of Münster</i>, 1648",
    "Northern Cyprus": "Sarayönü Square, North Nicosia, 1969",
    "Pakistan": "Makli Necropolis, Thatta",
    "Palestine": "Mount Gerizim, near Nablus, the Samaritans' holiest site",
    "Pennsylvania": "The Shelter House in Emmaus (1734)",
    "Peru": "The Legislative Palace, Lima",
    "Philippines": "Malacañang Palace, the president's residence, Manila",
    "Poland": "Wawel Castle, Kraków",
    "Portugal": "The Roman Temple of Évora",
    "Puerto Rico": "A reconstructed Taíno village",
    "Rio Grande": "An islet in the Rio Grande at Albuquerque, New Mexico",
    "San Marino": "Guaita, the first of the three towers on Monte Titano",
    "Saudi Arabia": "Qasr al-Farid, a rock-cut tomb at Hegra",
    "Scotland": "Parliament House, Edinburgh",
    "Seine": "The Seine in Paris, with the Pont des Invalides and the Eiffel Tower",
    "Senegal": "The African Renaissance Monument, Dakar",
    "Serbia": "Ruins of Felix Romuliana, Galerius's palace",
    "Seychelles": "Praslin, the second-largest island",
    "Shaanxi": "The Terracotta Army",
    "Sierra Leone": "The Supreme Court, Freetown",
    "Singapore": "An MRT train near Eunos station",
    "Sint Maarten": "Damage from Hurricane Irma, 2017",
    "South America": "Gran Roque, Los Roques Archipelago, Venezuela",
    "South Dakota": "The Black Hills",
    "South Korea": "Haeundae Beach, Busan",
    "Switzerland": "Zurich, the largest city",
    "Tennessee": "Gatlinburg, beside Great Smoky Mountains National Park",
    "Thailand": "Wat Phra Prang Sam Yod, a 13th-century Khmer temple in Lopburi",
    "Thames": "Tamesis, the river god, on Henley Bridge",
    "The Gambia": "Arch 22, Banjul",
    "Tigris": "The Tigris valley in southeastern Turkey",
    "Tunisia": "Temple ruins at Dougga",
    "Turkey": "Tulips in Emirgan Park, Istanbul",
    "Ukraine": "Saint Sophia Cathedral, Kyiv",
    "United Kingdom": "The Palace of Westminster, London",
    "Uruguay": "The old town of Colonia del Sacramento",
    "Vatican City": "The obelisk in St. Peter's Square, brought from Egypt by Caligula",
    "Venezuela": "Lake Valencia",
    "Virginia": "Colonial Williamsburg",
    "Wales": "Snowdon (Yr Wyddfa), the highest mountain in Wales",
    "West Virginia": "Spruce Knob, the highest point, in the distance",
    "Wisconsin": "Aztalan State Park, site of a Mississippian settlement",
    "Zambezi": "Victoria Falls, between the upper and middle Zambezi",
    "Åland Islands": "Degersand Beach, Eckerö",
}


def main(apply):
    ids = C.anki("findNotes", query='note:"Geography"')
    notes = []
    for i in range(0, len(ids), 500):
        notes += C.anki("notesInfo", notes=ids[i:i + 500])
    by = {}
    for n in notes:
        by.setdefault(C.plain(n["fields"]["Name"]["value"]).strip(), []).append(n)
    backup, todo = {}, []
    for nm, cap in CAP.items():
        hits = [n for n in by.get(nm, []) if n["fields"]["Photo caption"]["value"].strip()]
        if len(hits) != 1:
            sys.exit("%s: %d notes with a caption" % (nm, len(hits)))
        n = hits[0]
        if n["fields"]["Photo caption"]["value"] != cap:
            backup[n["noteId"]] = n["fields"]["Photo caption"]["value"]
            todo.append((n["noteId"], cap))
            print("%-24s %s\n%24s -> %s" % (nm, C.plain(backup[n["noteId"]])[:90], "", cap))
    if apply:
        json.dump(backup, open("backups/geo_captions_before_%s.json" % time.strftime("%Y%m%d_%H%M"), "w",
                               encoding="utf-8"), ensure_ascii=False)
        for nid, cap in todo:
            C.anki("updateNoteFields", note={"id": nid, "fields": {"Photo caption": cap}})
    print(("updated" if apply else "would update"), len(todo), "captions")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
