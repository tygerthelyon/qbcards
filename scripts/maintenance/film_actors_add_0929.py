# -*- coding: utf-8 -*-
"""film_actors_add_0929.py -- step 2 of the Film actor cards: twenty actors, one clue each.

Carter, 2026-10-01: "do the actor card -- but use imdb or other established websites + qbreader database
to list only of the greatest actors ever". Candidates: AFI's 100 Years...100 Stars and Empire's 50 Greatest
Actors of All Time (film_actors_0929.py). Kept: every candidate with three or more qbreader answer lines,
or 25 or more mentions (Bogart 70, Grant 34, Wayne 28, who are named constantly but rarely the answer).
Twenty actors. They use Film's FIGURE to NAME card with Kind "Actor", like the director cards, with a TMDB
portrait looked at on a contact sheet. Tiers follow the History rule, as film_add_0929.py's did.

    py -3.9 film_actors_add_0929.py find      (TMDB portraits and a contact sheet)
    py -3.9 film_actors_add_0929.py [--apply] (with data/film_actors_picks_0929.json)
"""
import json, os, re, sys, urllib.request
import concept_add as C

WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_actors_0929")
EVID = "data/film_actors_evidence_0929.json"
PICKS = "data/film_actors_picks_0929.json"

A = [
    ("Marilyn Monroe", "1926–1962", "United States",
     "Her white dress billowed up over a subway grate in <i>The Seven Year Itch</i>.",
     "<i>Gentlemen Prefer Blondes</i>; <u><i>Some Like It Hot</i></u>; <i>The Misfits</i>",
     "Born Norma Jeane Mortenson; she sang “Happy Birthday, Mr. President” to Kennedy in 1962, and Warhol silkscreened her face after her death."),
    ("Toshiro Mifune", "1920–1997", "Japan",
     "The Japanese actor who played the bandit Tajōmaru and the would-be samurai Kikuchiyo for Kurosawa.",
     "<i>Rashomon</i>; <u><i>Seven Samurai</i></u>; <i>Throne of Blood</i>; <i>Yojimbo</i>",
     "He made sixteen films with Kurosawa; for the end of <i>Throne of Blood</i>, real arrows were shot at him."),
    ("Audrey Hepburn", "1929–1993", "United Kingdom",
     "She ate a pastry outside Tiffany's window as Holly Golightly.",
     "<u><i>Roman Holiday</i></u>; <i>Sabrina</i>; <i>Breakfast at Tiffany's</i>; <i>My Fair Lady</i>",
     "Born in Brussels, she won the Academy Award for her first starring role, in <i>Roman Holiday</i>, and spent her last years working for UNICEF."),
    ("Ingrid Bergman", "1915–1982", "Sweden",
     "She played Ilsa Lund, who asks Sam to play “As Time Goes By” in <i>Casablanca</i>.",
     "<u><i>Casablanca</i></u>; <i>Gaslight</i>; <i>Notorious</i>; <i>Autumn Sonata</i>",
     "Her affair with Roberto Rossellini during <i>Stromboli</i> was denounced on the floor of the U.S. Senate; she won three Academy Awards."),
    ("Judy Garland", "1922–1969", "United States",
     "She sang “Over the Rainbow” as Dorothy Gale.",
     "<u><i>The Wizard of Oz</i></u>; <i>Meet Me in St. Louis</i>; <i>A Star Is Born</i>",
     "Born Frances Gumm; Liza Minnelli is her daughter with Vincente Minnelli, who directed <i>Meet Me in St. Louis</i>."),
    ("Marlene Dietrich", "1901–1992", "Germany",
     "She played the cabaret singer Lola Lola, who ruins a schoolteacher in <i>The Blue Angel</i>.",
     "<u><i>The Blue Angel</i></u>; <i>Morocco</i>; <i>Shanghai Express</i>; <i>Touch of Evil</i>",
     "Seven films with Josef von Sternberg; she took American citizenship and entertained Allied troops at the front in the Second World War."),
    ("Marlon Brando", "1924–2004", "United States",
     "He bellowed “Stella!” as Stanley Kowalski.",
     "<i>A Streetcar Named Desire</i>; <u><i>On the Waterfront</i></u>; <i>The Godfather</i>; <i>Apocalypse Now</i>",
     "The leading screen exponent of Method acting; he declined his Academy Award for <i>The Godfather</i> and sent Sacheen Littlefeather in his place."),
    ("Laurence Olivier", "1907–1989", "United Kingdom",
     "The English actor who directed himself in Shakespeare films of <i>Henry V</i>, <i>Hamlet</i>, and <i>Richard III</i>.",
     "<i>Wuthering Heights</i>; <i>Rebecca</i>; <u><i>Hamlet</i></u>; <i>Richard III</i>",
     "His <i>Hamlet</i> was the first film from outside the United States to win Best Picture; he was the first director of the National Theatre, and married Vivien Leigh."),
    ("Shirley Temple", "1928–2014", "United States",
     "The child star who sang “On the Good Ship Lollipop” in <i>Bright Eyes</i>.",
     "<u><i>Bright Eyes</i></u>; <i>Curly Top</i>; <i>Heidi</i>",
     "Given a special juvenile Academy Award at six, she later served as ambassador to Ghana and to Czechoslovakia as Shirley Temple Black."),
    ("Greta Garbo", "1905–1990", "Sweden",
     "The Swedish star who says “I want to be alone” in <i>Grand Hotel</i>.",
     "<i>Anna Christie</i>; <i>Grand Hotel</i>; <u><i>Queen Christina</i></u>; <i>Ninotchka</i>",
     "Publicity ran “Garbo talks!” for <i>Anna Christie</i> and “Garbo laughs!” for <i>Ninotchka</i>; she retired at thirty-six."),
    ("Daniel Day-Lewis", "born 1957", "United Kingdom",
     "The only man to win three Academy Awards for Best Actor.",
     "<i>My Left Foot</i>; <u><i>There Will Be Blood</i></u>; <i>Lincoln</i>; <i>Phantom Thread</i>",
     "Known for staying in character through whole shoots; he played Christy Brown, Daniel Plainview, and Abraham Lincoln."),
    ("Robert De Niro", "born 1943", "United States",
     "He asked “You talkin' to me?” into a mirror as Travis Bickle.",
     "<u><i>Taxi Driver</i></u>; <i>The Godfather Part II</i>; <i>Raging Bull</i>; <i>Goodfellas</i>",
     "He starred in ten features for Martin Scorsese, and gained about sixty pounds to play the older Jake LaMotta in <i>Raging Bull</i>."),
    ("Rita Hayworth", "1918–1987", "United States",
     "She peeled off a long black glove singing “Put the Blame on Mame” in <i>Gilda</i>.",
     "<i>Only Angels Have Wings</i>; <i>Cover Girl</i>; <u><i>Gilda</i></u>; <i>The Lady from Shanghai</i>",
     "A pin-up of the Second World War; she married Orson Welles, who cut and bleached her hair for <i>The Lady from Shanghai</i>."),
    ("Jack Nicholson", "born 1937", "United States",
     "He played Randle McMurphy against Nurse Ratched in <i>One Flew Over the Cuckoo's Nest</i>.",
     "<i>Easy Rider</i>; <i>Chinatown</i>; <u><i>One Flew Over the Cuckoo's Nest</i></u>; <i>The Shining</i>",
     "Nominated for twelve Academy Awards, the most of any male actor; he improvised “Here's Johnny!” in <i>The Shining</i>."),
    ("Mae West", "1893–1980", "United States",
     "She asked a young Cary Grant to “come up sometime and see me” in <i>She Done Him Wrong</i>.",
     "<u><i>She Done Him Wrong</i></u>; <i>I'm No Angel</i>; <i>My Little Chickadee</i>",
     "Sentenced to ten days in jail in 1927 over her Broadway play <i>Sex</i>; Second World War airmen called their inflatable life vests Mae Wests."),
    ("Katharine Hepburn", "1907–2003", "United States",
     "The actor with the most Academy Awards for acting: four, all for Best Actress.",
     "<i>Bringing Up Baby</i>; <u><i>The Philadelphia Story</i></u>; <i>The African Queen</i>; <i>Guess Who's Coming to Dinner</i>",
     "She made nine films with Spencer Tracy; labelled “box office poison” in 1938, she bought the film rights to <i>The Philadelphia Story</i> to come back."),
    ("Barbara Stanwyck", "1907–1990", "United States",
     "As Phyllis Dietrichson she talks an insurance salesman into killing her husband in <i>Double Indemnity</i>.",
     "<i>Stella Dallas</i>; <i>The Lady Eve</i>; <u><i>Double Indemnity</i></u>",
     "Nominated four times without winning, she received an honorary Academy Award in 1982."),
    ("Humphrey Bogart", "1899–1957", "United States",
     "He played Rick Blaine, owner of Rick's Café Américain.",
     "<i>The Maltese Falcon</i>; <u><i>Casablanca</i></u>; <i>The Big Sleep</i>; <i>The African Queen</i>",
     "First among AFI's male screen legends; he married Lauren Bacall after <i>To Have and Have Not</i> and won his Academy Award for <i>The African Queen</i>."),
    ("Cary Grant", "1904–1986", "United States",
     "He ran from a crop-dusting plane across a cornfield in <i>North by Northwest</i>.",
     "<i>Bringing Up Baby</i>; <i>His Girl Friday</i>; <i>Notorious</i>; <u><i>North by Northwest</i></u>",
     "Born Archibald Leach in Bristol; four films with Hitchcock, and an honorary Academy Award in 1970 after never winning a competitive one."),
    ("John Wayne", "1907–1979", "United States",
     "He played Ethan Edwards, who searches for years for his kidnapped niece in <i>The Searchers</i>.",
     "<i>Stagecoach</i>; <i>Red River</i>; <u><i>The Searchers</i></u>; <i>True Grit</i>",
     "Nicknamed the Duke; he made more than twenty films with John Ford, and won his Academy Award as Rooster Cogburn in <i>True Grit</i>."),
]


def tier(ans, alls):   # the History rule, as in film_add_0929.py
    if ans >= 5 or (ans >= 3 and alls >= 12) or alls >= 40:
        return "tier1-core"
    if ans >= 1 or alls >= 8:
        return "tier2-solid"
    return "tier3-deepcut" if alls >= 3 else "tier4-rare"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", C.fold(s).lower()).strip("-")


def find():
    import film_stills as S
    os.makedirs(WORK, exist_ok=True)
    tiles = []
    for i, (name, *_ ) in enumerate(A):
        r = S.tmdb("/search/person", query=name)["results"]
        r = [x for x in r if x.get("known_for_department") == "Acting"] or r
        if not r:
            print("no match", name)
            continue
        profs = sorted(S.tmdb("/person/%d/images" % r[0]["id"])["profiles"], key=lambda p: -(p.get("vote_count") or 0))
        for k, p in enumerate(profs[:3]):
            local = os.path.join(WORK, "%d_%d.jpg" % (i, k))
            if not os.path.exists(local):
                open(local, "wb").write(urllib.request.urlopen("https://image.tmdb.org/t/p/w500" + p["file_path"], timeout=60).read())
            tiles.append(("A%d.%d %s" % (i, k, name), local))
        print(name, r[0]["id"], len(profs), flush=True)
    sys.path.insert(0, r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\4c6fe2ff-c3a6-47fb-8b54-226f916ad6af\scratchpad")
    import wm
    for s in range(0, len(tiles), 30):
        wm.sheet(tiles[s:s + 30], os.path.join(WORK, "sheet_%02d.jpg" % (s // 30)), cols=6, W=220)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:2] == ["find"]:
        find()
        sys.exit()
    ev = json.load(open(EVID, encoding="utf-8"))
    picks = json.load(open(PICKS, encoding="utf-8"))
    have = {C.fold(C.plain(n["fields"]["Title"]["value"])).lower()
            for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Film"'))}
    todo = []
    for i, (name, years, country, clue, works, notes) in enumerate(A):
        if C.fold(name).lower() in have:
            continue
        e = ev[name]
        t = tier(e["ans"], e["all"])
        f = {"Title": name, "Year": years, "Country": country, "Clue": clue, "Works": works, "Notes": notes, "Kind": "Actor"}
        fn = None
        if str(i) in picks:
            fn = "filmactor-%s-0929.jpg" % slug(name)
            f["Picture"] = '<img src="%s">' % fn
        todo.append((f, fn, os.path.join(WORK, "%d_%d.jpg" % (i, picks.get(str(i), 0))), t))
        print("%-20s ans %2d all %3d  %s  %s" % (name, e["ans"], e["all"], t, fn))
    if "--apply" in sys.argv:
        for f, fn, path, t in todo:
            if fn:
                C.anki("storeMediaFile", filename=fn, path=path)
            C.anki("addNote", note={"deckName": "Film", "modelName": "Film", "fields": f,
                                    "tags": ["Film::actor", "Film::actors_0929", "Film::tier::" + t],
                                    "options": {"allowDuplicate": False}})
        # only tier 1 is studied; tier-2 cards are suspended like the rest of the deck's
        cids = C.anki("findCards", query="tag:Film::actors_0929 -tag:Film::tier::tier1-core -is:suspended")
        if cids:
            C.anki("suspend", cards=cids)
        print("added", len(todo), "; suspended", len(cids), "tier-2 cards")
