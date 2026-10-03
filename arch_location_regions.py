# -*- coding: utf-8 -*-
"""arch_location_regions.py -- every Architecture Location as City, Region, Country.

Carter (2026-09-25): "be consistent with place names. teatro olimpico says location
is vicenza. is that venice?" -- 270 locations were "City, Country", 127 "City,
Region, Country". Carter chose City, Region, Country (answer to the Vicenza
question: "Vicenza, Veneto, Italy").

Rules: UK -> county + England/Scotland (the deck's existing "Letchworth,
Hertfordshire, England"); region-only entries get the real town (Stonehenge ->
Amesbury, Ur -> Nasiriyah); cities that are their own first-level region
(Berlin, Vienna, Tokyo, Mexico City, Hong Kong...) stay two-part; Jerusalem,
Singapore and Vatican City stay single; structures spanning regions keep them
(Hadrian's Wall, the Great Wall, the Channel Tunnel).

    py -3.9 arch_location_regions.py --dry | --apply
"""
import json
import sys
import time

import concept_add as C

MAP = {
    "Abu Simbel, Egypt": "Abu Simbel, Aswan, Egypt",
    "Ahmedabad, India": "Ahmedabad, Gujarat, India",
    "Aksaray, Turkey": "Sultanhanı, Aksaray, Turkey",
    "Aleppo, Syria": "Aleppo, Aleppo Governorate, Syria",
    "Alfeld, Germany": "Alfeld, Lower Saxony, Germany",
    "Amiens, France": "Amiens, Hauts-de-France, France",
    "Apostolic Palace, Vatican City": "Vatican City",
    "Ararat Province, Armenia": "Lusarat, Ararat Province, Armenia",
    "Arc-et-Senans, France": "Arc-et-Senans, Bourgogne-Franche-Comté, France",
    "Athens, Greece": "Athens, Attica, Greece",
    "Baalbek, Lebanon": "Baalbek, Baalbek-Hermel, Lebanon",
    "Bad Staffelstein, Germany": "Bad Staffelstein, Bavaria, Germany",
    "Barcelona, Spain": "Barcelona, Catalonia, Spain",
    "Belém, Portugal": "Belém, Lisbon District, Portugal",
    "Bexleyheath, England": "Bexleyheath, Greater London, England",
    "Borgund, Norway": "Borgund, Vestland, Norway",
    "Brighton, England": "Brighton, East Sussex, England",
    "Brno, Czech Republic": "Brno, South Moravia, Czech Republic",
    "Cambridge, England": "Cambridge, Cambridgeshire, England",
    "Canterbury, England": "Canterbury, Kent, England",
    "Cluny, France": "Cluny, Bourgogne-Franche-Comté, France",
    "Coalbrookdale, England": "Coalbrookdale, Shropshire, England",
    "Coimbra, Portugal": "Coimbra, Coimbra District, Portugal",
    "Colón, Panama": "Colón, Colón Province, Panama",
    "Como, Italy": "Como, Lombardy, Italy",
    "Conques, France": "Conques, Occitania, France",
    "Copenhagen, Denmark": "Copenhagen, Capital Region, Denmark",
    "Cusco Region, Peru": "Urubamba, Cusco Region, Peru",
    "Dambulla, Sri Lanka": "Dambulla, Central Province, Sri Lanka",
    "Delphi, Greece": "Delphi, Central Greece, Greece",
    "Dessau, Germany": "Dessau, Saxony-Anhalt, Germany",
    "Dhaka, Bangladesh": "Dhaka, Dhaka Division, Bangladesh",
    "Dhi Qar, Iraq": "Nasiriyah, Dhi Qar, Iraq",
    "Djenné, Mali": "Djenné, Mopti Region, Mali",
    "Dorchester, England": "Dorchester, Dorset, England",
    "Durham, England": "Durham, County Durham, England",
    "Edirne, Turkey": "Edirne, Edirne Province, Turkey",
    "Fars Province, Iran": "Marvdasht, Fars Province, Iran",
    "Florence, Italy": "Florence, Tuscany, Italy",
    "Foz do Iguaçu, Brazil": "Foz do Iguaçu, Paraná, Brazil",
    "Fátima, Portugal": "Fátima, Santarém District, Portugal",
    "Gando, Burkina Faso": "Gando, Centre-Est, Burkina Faso",
    "Gateshead, England": "Gateshead, Tyne and Wear, England",
    "Giza, Egypt": "Giza, Giza Governorate, Egypt",
    "Glasgow, Scotland": "Glasgow, Glasgow City, Scotland",
    "Granada, Spain": "Granada, Andalusia, Spain",
    "Greenwich, London, United Kingdom": "Greenwich, Greater London, England",
    "Guangzhou, China": "Guangzhou, Guangdong, China",
    "Heraklion, Greece": "Heraklion, Crete, Greece",
    "Hiroshima, Japan": "Hiroshima, Hiroshima Prefecture, Japan",
    "Homs Governorate, Syria": "Al-Husn, Homs Governorate, Syria",
    "Ise, Japan": "Ise, Mie Prefecture, Japan",
    "Isfahan, Iran": "Isfahan, Isfahan Province, Iran",
    "Ivanovo, Bulgaria": "Ivanovo, Ruse Province, Bulgaria",
    "Jaipur, India": "Jaipur, Rajasthan, India",
    "Kairouan, Tunisia": "Kairouan, Kairouan Governorate, Tunisia",
    "Kanazawa, Japan": "Kanazawa, Ishikawa Prefecture, Japan",
    "King George Island, Antarctica": "King George Island, South Shetland Islands, Antarctica",
    "Kyoto, Japan": "Kyoto, Kyoto Prefecture, Japan",
    "Lalibela, Ethiopia": "Lalibela, Amhara Region, Ethiopia",
    "Lincoln, England": "Lincoln, Lincolnshire, England",
    "Liverpool, England": "Liverpool, Merseyside, England",
    "London, England": "London, Greater London, England",
    "London, United Kingdom": "London, Greater London, England",
    "Luxor, Egypt": "Luxor, Luxor Governorate, Egypt",
    "Lübeck, Germany": "Lübeck, Schleswig-Holstein, Germany",
    "Ma'an, Jordan": "Wadi Musa, Ma'an Governorate, Jordan",
    "Manhattan, New York City, United States": "New York City, New York, United States",
    "Mantua, Italy": "Mantua, Lombardy, Italy",
    "Marseille, France": "Marseille, Provence-Alpes-Côte d'Azur, France",
    "Masada, Israel": "Masada, Southern District, Israel",
    "Masvingo, Zimbabwe": "Masvingo, Masvingo Province, Zimbabwe",
    "Matosinhos, Portugal": "Matosinhos, Porto District, Portugal",
    "Mecca, Saudi Arabia": "Mecca, Makkah Province, Saudi Arabia",
    "Mechernich, Germany": "Mechernich, North Rhine-Westphalia, Germany",
    "Medina, Saudi Arabia": "Medina, Al Madinah Province, Saudi Arabia",
    "Metz, France": "Metz, Grand Est, France",
    "Modena, Italy": "Modena, Emilia-Romagna, Italy",
    "Montreal, Canada": "Montreal, Quebec, Canada",
    "Nara, Japan": "Nara, Nara Prefecture, Japan",
    "Nariño, Colombia": "Ipiales, Nariño, Colombia",
    "Naucalpan, Mexico": "Naucalpan, State of Mexico, Mexico",
    "Nevada–Arizona border, United States": "Black Canyon, Nevada and Arizona, United States",
    "New York City, United States": "New York City, New York, United States",
    "Ningbo, China": "Ningbo, Zhejiang, China",
    "Niterói, Brazil": "Niterói, Rio de Janeiro, Brazil",
    "Noormarkku, Finland": "Noormarkku, Satakunta, Finland",
    "Novgorod, Russia": "Veliky Novgorod, Novgorod Oblast, Russia",
    "Orkney, Scotland": "Skaill, Orkney, Scotland",
    "Ouro Preto, Brazil": "Ouro Preto, Minas Gerais, Brazil",
    "Oxford, United Kingdom": "Oxford, Oxfordshire, England",
    "Paimio, Finland": "Paimio, Southwest Finland, Finland",
    "Palmyra, Syria": "Palmyra, Homs Governorate, Syria",
    "Paris, France": "Paris, Île-de-France, France",
    "Paro, Bhutan": "Paro, Paro District, Bhutan",
    "Petén, Guatemala": "Flores, Petén, Guatemala",
    "Pisa, Italy": "Pisa, Tuscany, Italy",
    "Poissy, France": "Poissy, Île-de-France, France",
    "Pompeii, Italy": "Pompeii, Campania, Italy",
    "Poreč, Croatia": "Poreč, Istria, Croatia",
    "Potsdam, Germany": "Potsdam, Brandenburg, Germany",
    "Ravenna, Italy": "Ravenna, Emilia-Romagna, Italy",
    "Reykjavík, Iceland": "Reykjavík, Capital Region, Iceland",
    "Rila Mountains, Bulgaria": "Rila, Kyustendil Province, Bulgaria",
    "Rimini, Italy": "Rimini, Emilia-Romagna, Italy",
    "Rio de Janeiro, Brazil": "Rio de Janeiro, Rio de Janeiro, Brazil",
    "Rome, Italy": "Rome, Lazio, Italy",
    "Ronchamp, France": "Ronchamp, Bourgogne-Franche-Comté, France",
    "Roskilde, Denmark": "Roskilde, Zealand, Denmark",
    "Saint-Denis, France": "Saint-Denis, Île-de-France, France",
    "Salamanca, Spain": "Salamanca, Castile and León, Spain",
    "Salisbury, England": "Salisbury, Wiltshire, England",
    "Samarkand, Uzbekistan": "Samarkand, Samarkand Region, Uzbekistan",
    "Samarra, Iraq": "Samarra, Saladin Governorate, Iraq",
    "San Lorenzo de El Escorial, Spain": "San Lorenzo de El Escorial, Community of Madrid, Spain",
    "San Sebastián, Spain": "San Sebastián, Basque Country, Spain",
    "Saqqara, Egypt": "Saqqara, Giza Governorate, Egypt",
    "Schiers, Switzerland": "Schiers, Graubünden, Switzerland",
    "Seville, Spain": "Seville, Andalusia, Spain",
    "Siem Reap, Cambodia": "Siem Reap, Siem Reap Province, Cambodia",
    "Siena, Italy": "Siena, Tuscany, Italy",
    "State of Mexico, Mexico": "San Martín de las Pirámides, State of Mexico, Mexico",
    "Stuttgart, Germany": "Stuttgart, Baden-Württemberg, Germany",
    "Sydney, Australia": "Sydney, New South Wales, Australia",
    "Tallinn, Estonia": "Tallinn, Harju County, Estonia",
    "Thiepval, France": "Thiepval, Hauts-de-France, France",
    "Timbuktu, Mali": "Timbuktu, Tombouctou Region, Mali",
    "Utrecht, Netherlands": "Utrecht, Utrecht, Netherlands",
    "Vals, Switzerland": "Vals, Graubünden, Switzerland",
    "Venice, Italy": "Venice, Veneto, Italy",
    "Vers-Pont-du-Gard, France": "Vers-Pont-du-Gard, Occitania, France",
    "Versailles, France": "Versailles, Île-de-France, France",
    "Vicenza, Italy": "Vicenza, Veneto, Italy",
    "Weil am Rhein, Germany": "Weil am Rhein, Baden-Württemberg, Germany",
    "Wiltshire, England": "Amesbury, Wiltshire, England",
    "Woodstock, England": "Woodstock, Oxfordshire, England",
    "Yangon, Myanmar": "Yangon, Yangon Region, Myanmar",
    "York, England": "York, North Yorkshire, England",
    "Yucatán, Mexico": "Tinúm, Yucatán, Mexico",
    "Éveux, France": "Éveux, Auvergne-Rhône-Alpes, France",
    "Świdnica and Jawor, Poland": "Świdnica and Jawor, Lower Silesia, Poland",
    "Şanlıurfa, Turkey": "Şanlıurfa, Şanlıurfa Province, Turkey",
    "Šibenik, Croatia": "Šibenik, Šibenik-Knin County, Croatia",
}
# own first-level region, a single name, or a structure spanning regions
KEEP = {
    "Abu Dhabi, United Arab Emirates", "Baku, Azerbaijan", "Beijing, China", "Berlin, Germany",
    "Brasília, Brazil", "Brussels, Belgium", "Cairo, Egypt", "Chandigarh, India", "Damascus, Syria",
    "Delhi, India", "New Delhi, India", "Doha, Qatar", "Dubai, United Arab Emirates", "Hong Kong, China",
    "Islamabad, Pakistan", "Istanbul, Turkey", "Jerusalem", "Kuala Lumpur, Malaysia", "Mexico City, Mexico",
    "Moscow, Russia", "Prague, Czech Republic", "Pyongyang, North Korea", "Saint Petersburg, Russia",
    "Shanghai, China", "Singapore", "Taipei, Taiwan", "Tokyo, Japan", "Vatican City", "Vienna, Austria",
    "Yamoussoukro, Côte d'Ivoire", "[unbuilt]", "Folkestone, England, and Coquelles, France",
    "Northern China, China", "Northumberland and Cumbria, England"}


def main():
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query="note:Architecture"))
    upd, backup, left = [], {}, set()
    for n in ns:
        raw = n["fields"]["Location"]["value"]
        v = C.plain(raw)
        if v in MAP:
            upd.append({"id": n["noteId"], "fields": {"Location": MAP[v]}})
            backup[n["noteId"]] = raw
        elif v and len(v.split(",")) != 3 and v not in KEEP:
            left.add(v)
    print("to change:", len(upd), "| unhandled short locations:", sorted(left))
    if "--apply" in sys.argv:
        json.dump(backup, open("backups/arch_location_before_%s.json" % time.strftime("%Y%m%d_%H%M"),
                               "w", encoding="utf-8"), ensure_ascii=False)
        C.anki("multi", actions=[{"action": "updateNoteFields", "params": {"note": u}} for u in upd])
        print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
