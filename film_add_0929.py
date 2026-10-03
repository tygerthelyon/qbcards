# -*- coding: utf-8 -*-
"""film_add_0929.py -- the Film canon the deck was missing, found by checking it against what quizbowl asks.

Carter asked for "the canon ... covered" in the History review; the same test on Film, against the 2,279 qbreader
Film tossups (_qb_pool_other_fine_arts_film.json), found names asked as answers several times that the deck never
mentions at all: Michelangelo Antonioni (six tossups, and two more each on L'Avventura and Blowup), The Good, the Bad
and the Ugly and Ran (three each), Bicycle Thieves and Grand Illusion (two each, and both on every critics' list),
Buster Keaton (a card for The General but none for him), Pasolini, von Stroheim, Ophuls, Vertov, Wong Kar-wai's
Chungking Express, Tarr's Satantango. Fifteen films and six directors, written like the rest of the deck (one clue,
a detail, the cast), with stills, posters, and portraits from TMDB looked at on a contact sheet before they go in.
Tiers follow the evidence: answer-line tossups and all mentions across the Film pool, by the History rule.

    py -3.9 film_add_0929.py find            (TMDB candidates and a contact sheet)
    py -3.9 film_add_0929.py [--apply]       (with data/film_add_picks_0929.json)
"""
import json, os, re, sys, time, urllib.request
import concept_add as C

WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_add_0929")
PICKS = "data/film_add_picks_0929.json"

FILMS = [
    dict(Title="L'Avventura", Director="Michelangelo Antonioni", Year="1960", Country="Italy", Movement="",
         Cast="Monica Vitti; Gabriele Ferzetti; Lea Massari",
         Clue="On a yachting trip to a volcanic island a woman vanishes, and her lover and her best friend drift into an affair instead of finding her.",
         Notes="Booed at Cannes, then given a special jury prize; the first of Antonioni's trilogy with Monica Vitti, followed by <i>La Notte</i> and <i>L'Eclisse</i>.",
         keys=["avventura"]),
    dict(Title="Blowup", **{"Original title": "Blow-Up"}, Director="Michelangelo Antonioni", Year="1966", Country="United Kingdom", Movement="",
         Cast="David Hemmings; Vanessa Redgrave; Sarah Miles",
         Clue="A fashion photographer in Swinging London enlarges his pictures of a park until they seem to show a body in the bushes.",
         Notes="Antonioni's first English-language film, from a Julio Cortázar story; it ends with mimes playing tennis without a ball.",
         keys=["blowup", "blow-up", "blow up"]),
    dict(Title="Bicycle Thieves", **{"Original title": "Ladri di biciclette"}, Director="Vittorio De Sica", Year="1948", Country="Italy",
         Movement="Italian Neorealism", Cast="Lamberto Maggiorani; Enzo Staiola",
         Clue="A bill-poster in postwar Rome searches the city with his small son for the stolen bicycle his job depends on.",
         Notes="Cast with non-professionals (Maggiorani was a factory worker), it topped the first <i>Sight and Sound</i> critics' poll in 1952.",
         keys=["bicycle thieves", "bicycle thief", "ladri di biciclette"]),
    dict(Title="Grand Illusion", **{"Original title": "La Grande Illusion"}, Director="Jean Renoir", Year="1937", Country="France",
         Movement="Poetic realism", Cast="Jean Gabin; Pierre Fresnay; Erich von Stroheim",
         Clue="French officers in a First World War prison camp plan escapes while the aristocratic German commandant befriends the one captain of his own class.",
         Notes="Von Stroheim plays the commandant, von Rauffenstein. Goebbels called it “cinematic public enemy number one”, and the Germans seized the negative in 1940.",
         keys=["grand illusion", "grande illusion"]),
    dict(Title="The Great Dictator", Director="Charlie Chaplin", Year="1940", Country="United States", Movement="Comedy",
         Cast="Charlie Chaplin; Paulette Goddard; Jack Oakie",
         Clue="A Jewish barber is mistaken for his double, Adenoid Hynkel, the dictator of Tomainia.",
         Notes="Chaplin's first true talkie, in which Hynkel dances with an inflatable globe; Chaplin later said he could not have made it had he known of the camps.",
         keys=["great dictator"]),
    dict(Title="It Happened One Night", Director="Frank Capra", Year="1934", Country="United States", Movement="Screwball comedy",
         Cast="Clark Gable; Claudette Colbert",
         Clue="A runaway heiress and a newspaperman hang a blanket, the “Walls of Jericho”, between their motel beds.",
         Notes="The first film to win all five major Academy Awards, since matched only by <i>One Flew Over the Cuckoo's Nest</i> and <i>The Silence of the Lambs</i>.",
         keys=["it happened one night"]),
    dict(Title="The Bridge on the River Kwai", Director="David Lean", Year="1957", Country="United Kingdom", Movement="War film",
         Cast="Alec Guinness; William Holden; Sessue Hayakawa",
         Clue="A British colonel in a Japanese prison camp in Burma drives his men to build a railway bridge properly, as a point of pride.",
         Notes="The blacklisted writers Carl Foreman and Michael Wilson went uncredited, so the Oscar for the script went to Pierre Boulle, who wrote the novel.",
         keys=["river kwai"]),
    dict(Title="Cries and Whispers", **{"Original title": "Viskningar och rop"}, Director="Ingmar Bergman", Year="1972", Country="Sweden",
         Movement="", Cast="Harriet Andersson; Ingrid Thulin; Liv Ullmann; Kari Sylwan",
         Clue="Two sisters and a maid keep watch over a third sister dying of cancer in a manor house of blood-red rooms.",
         Notes="Sven Nykvist's colour photography won the Academy Award; Bergman said he pictured the inside of the soul as a red membrane.",
         keys=["cries and whispers", "viskningar och rop"]),
    dict(Title="Ran", Director="Akira Kurosawa", Year="1985", Country="Japan", Movement="<i>Jidaigeki</i>",
         Cast="Tatsuya Nakadai; Akira Terao; Jinpachi Nezu; Mieko Harada",
         Clue="An old warlord, Hidetora Ichimonji, divides his domain among his three sons, who turn on him.",
         Notes="<i>King Lear</i> with sons for daughters; Kurosawa's last epic, made with French money after Japanese studios would not fund it.",
         keys=[r"^ran\b"]),                     # "ran" in question text is the verb; count the answer line only
    dict(Title="The Good, the Bad and the Ugly", **{"Original title": "Il buono, il brutto, il cattivo"}, Director="Sergio Leone", Year="1966",
         Country="Italy", Movement="Spaghetti western", Cast="Clint Eastwood; Lee Van Cleef; Eli Wallach",
         Clue="Three gunmen race through the Civil War after Confederate gold buried in a cemetery, and settle it in a three-way standoff.",
         Notes="The last of Leone's Dollars trilogy with Eastwood as the Man with No Name; Ennio Morricone's theme imitates a coyote's howl.",
         keys=["good, the bad", "good the bad and the ugly"]),
    dict(Title="Chungking Express", **{"Original title": "Chung Hing sam lam"}, Director="Wong Kar-wai", Year="1994", Country="Hong Kong",
         Movement="", Cast="Tony Leung; Faye Wong; Takeshi Kaneshiro; Brigitte Lin",
         Clue="A jilted Hong Kong policeman buys tins of pineapple that expire on the first of May, his birthday.",
         Notes="Shot in about two months while Wong was stuck editing <i>Ashes of Time</i>; Faye Wong plays “California Dreamin'” over and over.",
         keys=["chungking express"]),
    dict(Title="Sátántangó", Director="Béla Tarr", Year="1994", Country="Hungary", Movement="",
         Cast="Mihály Víg; Putyi Horváth; Erika Bók",
         Clue="A seven-hour film of a collapsing collective farm, in twelve parts that step forward and back like a tango.",
         Notes="From László Krasznahorkai's novel; it opens with a single take of cows wandering out of a barn.",
         keys=["satantango", "sátántangó"]),
    dict(Title="Koyaanisqatsi", Director="Godfrey Reggio", Year="1982", Country="United States", Movement="Documentary",
         Cast="",
         Clue="A wordless film of time-lapse deserts and city crowds, its Hopi title meaning “life out of balance”.",
         Notes="Philip Glass wrote the score and Ron Fricke shot it; the first of Reggio's Qatsi trilogy.",
         keys=["koyaanisqatsi"]),
    dict(Title="Touki Bouki", Director="Djibril Diop Mambéty", Year="1973", Country="Senegal", Movement="",
         Cast="Magaye Niang; Mareme Niang",
         Clue="A cowherd whose motorbike wears a zebu's horns and his girlfriend scheme their way out of Dakar toward Paris.",
         Notes="Restored by Martin Scorsese's World Cinema Foundation in 2008, and often named the greatest African film.",
         keys=["touki bouki"]),
    dict(Title="Man with a Movie Camera", **{"Original title": "Chelovek s kino-apparatom"}, Director="Dziga Vertov", Year="1929",
         Country="Soviet Union", Movement="Soviet montage", Cast="",
         Clue="A day of Soviet city life with no story, actors, or intertitles, which keeps showing its own cameraman and editor at work.",
         Notes="Vertov's kino-eye made the camera a better eye than the human one; it topped <i>Sight and Sound</i>'s 2014 poll of documentaries.",
         keys=["man with a movie camera"]),
]

DIRECTORS = [
    dict(Title="Michelangelo Antonioni", Year="1912–2007", Country="Italy",
         Clue="The Italian director of alienation whose films with Monica Vitti end in empty streets and disappearances nobody solves.",
         Works="<u><i>L'Avventura</i></u>; <i>La Notte</i>; <i>L'Eclisse</i>; <i>Blowup</i>",
         Notes="<i>Blowup</i> was his first film in English; <i>Zabriskie Point</i> ends with a house exploding in slow motion.",
         keys=["antonioni"]),
    dict(Title="Buster Keaton", Year="1895–1966", Country="United States",
         Clue="The “Great Stone Face” of silent comedy, who stood still while the front of a house fell around him.",
         Works="<i>Sherlock Jr.</i>; <u><i>The General</i></u>; <i>Steamboat Bill, Jr.</i>",
         Notes="He did his own stunts; <i>The General</i>, his Civil War locomotive chase, flopped in 1926 and now ranks among the greatest films.",
         keys=["keaton"]),
    dict(Title="Pier Paolo Pasolini", Year="1922–1975", Country="Italy",
         Clue="The Italian poet and director killed on the beach at Ostia weeks before his adaptation of Sade, <i>Salò</i>, came out.",
         Works="<i>Accattone</i>; <u><i>The Gospel According to St. Matthew</i></u>; <i>Salò, or the 120 Days of Sodom</i>",
         Notes="A Marxist raised Catholic, he cast his own mother as the aged Mary in his <i>Gospel</i>.",
         keys=["pasolini"]),
    dict(Title="Erich von Stroheim", Year="1885–1957", Country="United States",
         Clue="The Vienna-born director whose <i>Greed</i> ran about nine hours before MGM cut it to two.",
         Works="<i>Foolish Wives</i>; <u><i>Greed</i></u>; <i>Queen Kelly</i>",
         Notes="Later an actor: the commandant in <i>Grand Illusion</i> and the butler Max in <i>Sunset Boulevard</i>.",
         keys=["stroheim"]),
    dict(Title="Max Ophüls", Year="1902–1957", Country="France",
         Clue="The German-born director of long gliding tracking shots through ballrooms and waltzes.",
         Works="<i>Letter from an Unknown Woman</i>; <i>La Ronde</i>; <u><i>The Earrings of Madame de…</i></u>; <i>Lola Montès</i>",
         Notes="He worked in Germany, France, and Hollywood; his son Marcel made <i>The Sorrow and the Pity</i>.",
         keys=["ophuls", "ophüls"]),
    dict(Title="Clint Eastwood", Year="born 1930", Country="United States",
         Clue="The Man with No Name in Leone's westerns, who directed himself as a retired gunfighter in <i>Unforgiven</i>.",
         Works="<u><i>Unforgiven</i></u>; <i>Mystic River</i>; <i>Million Dollar Baby</i>; <i>Letters from Iwo Jima</i>",
         Notes="<i>Unforgiven</i> and <i>Million Dollar Baby</i> each won him Best Picture and Best Director.",
         keys=["eastwood"]),
]


def evidence():
    pool = json.load(open("_qb_pool_other_fine_arts_film.json", encoding="utf-8"))
    pool += json.load(open("_qb_pool_other_fine_arts_misc_arts.json", encoding="utf-8"))
    rows = [(C.fold(C.plain(q["answer"])).lower(), C.fold(C.plain(q["question"])).lower()) for q in pool]
    out = {}
    for d in FILMS + DIRECTORS:
        ks = [re.compile(k if k.startswith("^") else re.escape(C.fold(k).lower())) for k in d["keys"]]
        ans = sum(1 for a, _ in rows if any(k.search(a) for k in ks))
        alls = sum(1 for a, q in rows if any(k.search(a) or (k.pattern[0] != "^" and k.search(q)) for k in ks))
        out[d["Title"]] = (ans, alls)
    return out


def tier(ans, alls):   # the History rule
    if ans >= 5 or (ans >= 3 and alls >= 12) or alls >= 40:
        return "tier1-core"
    if ans >= 1 or alls >= 8:
        return "tier2-solid"
    return "tier3-deepcut" if alls >= 3 else "tier4-rare"


def find():
    import film_stills as S
    from film_img_0929 import tmdb_candidates
    os.makedirs(WORK, exist_ok=True)
    plan, tiles = {}, []
    for i, d in enumerate(FILMS):
        tid, stills = tmdb_candidates(9000 + i, d["Title"], d.get("Original title", ""), d["Year"], d["Director"])
        posters = []
        if tid:
            ps = [p for p in S.tmdb("/movie/%d/images" % tid, include_image_language="en,null")["posters"]]
            ps.sort(key=lambda p: (p.get("iso_639_1") not in ("en", None), -(p.get("vote_count") or 0)))
            for k, p in enumerate(ps[:2]):
                local = os.path.join(WORK, "poster_%d_%d.jpg" % (i, k))
                if not os.path.exists(local):
                    open(local, "wb").write(urllib.request.urlopen("https://image.tmdb.org/t/p/w780" + p["file_path"], timeout=60).read())
                posters.append(local)
        plan["F%d" % i] = {"title": d["Title"], "tmdb": tid, "stills": stills, "posters": posters}
        tiles += [("F%d.s%d %s" % (i, k, d["Title"][:24]), p) for k, p in enumerate(stills)]
        tiles += [("F%d.p%d %s" % (i, k, d["Title"][:24]), p) for k, p in enumerate(posters)]
        print(d["Title"], tid, len(stills), len(posters), flush=True)
    for i, d in enumerate(DIRECTORS):
        r = S.tmdb("/search/person", query=d["Title"])["results"]
        pics = []
        if r:
            profs = S.tmdb("/person/%d/images" % r[0]["id"])["profiles"]
            profs.sort(key=lambda p: -(p.get("vote_count") or 0))
            for k, p in enumerate(profs[:3]):
                local = os.path.join(WORK, "dir_%d_%d.jpg" % (i, k))
                if not os.path.exists(local):
                    open(local, "wb").write(urllib.request.urlopen("https://image.tmdb.org/t/p/w500" + p["file_path"], timeout=60).read())
                pics.append(local)
        plan["D%d" % i] = {"title": d["Title"], "pics": pics}
        tiles += [("D%d.%d %s" % (i, k, d["Title"][:24]), p) for k, p in enumerate(pics)]
        print(d["Title"], len(pics), flush=True)
    json.dump(plan, open(os.path.join(WORK, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    sys.path.insert(0, r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\4c6fe2ff-c3a6-47fb-8b54-226f916ad6af\scratchpad")
    import wm
    for s in range(0, len(tiles), 24):
        wm.sheet(tiles[s:s + 24], os.path.join(WORK, "sheet_%02d.jpg" % (s // 24)), cols=6, W=260)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", C.fold(C.plain(s)).lower()).strip("-")


def notes():
    plan = json.load(open(os.path.join(WORK, "plan.json"), encoding="utf-8"))
    picks = json.load(open(PICKS, encoding="utf-8"))
    ev = evidence()
    out = []
    for i, d in enumerate(FILMS):
        p, pk = plan["F%d" % i], picks.get("F%d" % i, {})
        f = {k: v for k, v in d.items() if k != "keys"}
        f["Title"] = "<i>%s</i>" % d["Title"]
        if d.get("Original title"):
            f["Original title"] = "<i>%s</i>" % d["Original title"]
        media = {}
        if "s" in pk:
            fn = "film-tmdb-%d-0929.jpg" % p["tmdb"]
            media[fn] = p["stills"][pk["s"]]
            f["Still"] = '<img src="%s">' % fn
        if "p" in pk:
            fn = "filmposter-%s-0929.jpg" % slug(d["Title"])
            media[fn] = p["posters"][pk["p"]]
            f["Poster"] = '<img src="%s">' % fn
            f["Poster caption"] = "%s &middot; %s, %s" % (pk.get("pc", "Release poster"), d["Director"], d["Year"])  # "Poster" for a reissue
        out.append((f, media, ["Film::canon_0929", "Film::tier::" + tier(*ev[d["Title"]])], ev[d["Title"]]))
    for i, d in enumerate(DIRECTORS):
        p, pk = plan["D%d" % i], picks.get("D%d" % i)
        f = {k: v for k, v in d.items() if k != "keys"}
        f["Kind"] = "Director"
        media = {}
        if pk is not None:
            fn = "filmdir-%s-0929.jpg" % slug(d["Title"])
            media[fn] = p["pics"][pk]
            f["Picture"] = '<img src="%s">' % fn
        out.append((f, media, ["Film::canon_0929", "Film::director", "Film::tier::" + tier(*ev[d["Title"]])], ev[d["Title"]]))
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:2] == ["find"]:
        find()
        sys.exit()
    have = {C.fold(C.plain(n["fields"]["Title"]["value"])).lower()
            for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Film"'))}
    todo = [x for x in notes() if C.fold(C.plain(x[0]["Title"])).lower() not in have]
    for f, media, tags, ev in todo:
        print("%-34s ans %2d all %3d  %-14s  %s" % (C.plain(f["Title"]), ev[0], ev[1], tags[-1].split("::")[-1], sorted(media)))
    if "--apply" in sys.argv:
        for f, media, tags, _ in todo:
            for fn, path in media.items():
                C.anki("storeMediaFile", filename=fn, path=path)
            C.anki("addNote", note={"deckName": "Film", "modelName": "Film", "fields": f, "tags": tags,
                                    "options": {"allowDuplicate": False}})
        print("added", len(todo))
