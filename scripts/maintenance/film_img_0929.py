# -*- coding: utf-8 -*-
"""film_img_0929.py -- Film's pictures: real stills on the fronts, the film in the gallery, captions fixed.

Carter, 2026-09-28, on Film: "poorly written, poorly designed, horrifically inconsistent and
error-filled." All 400 still slots were looked at on contact sheets (sheet numbers below are the
index in img/film/idx.json, one per Still / Still 2 / Still 3 slot).

  * 27 STILL to TITLE fronts were not stills from the film at all: a 2012 Disneyland photograph on
    Snow White, a Wynwood mural on Scarface, a plaque on Schindler's List, a photograph of a Focke-Wulf
    on Come and See, a press portrait on Oldboy, a museum costume on Gravity and Poor Things, filming
    locations photographed decades later on Shawshank, Roma, Parasite, Get Out, and more. Each gets a
    text-free TMDB backdrop, chosen by eye (REPLACE).
  * About 55 gallery pictures were not of the film either: locations today (Leeds Castle, Tikal, the
    Plaza de España, the UN), museum replicas (Easy Rider's bikes, Bonnie and Clyde's car), memorabilia
    (a boombox, a flag patch), and portraits taken years apart from it (Alec Guinness in 1972, Nora
    Gregor in 1932, Georges Auric). They are dropped (DROP). Production photographs stay.
  * A Trip to the Moon's front was a photograph of Méliès's studio; the moon's eye moves to the front.
    Modern Times's front was a portrait of Chaplin; the gears move to the front (SWAP).
  * Captions came from Wikipedia and read like it: cut off at "Dr." and "G." and "Michael J.", titles
    unitalicized, "[n 5]" footnote marks, critics' remarks where a description belongs. Each kept
    caption now says what the picture shows (CAP).

    py -3.9 film_img_0929.py find              TMDB candidates for REPLACE, onto a contact sheet
    py -3.9 film_img_0929.py apply PICKS.json  PICKS: {sheet index: candidate number}
"""
import json, os, re, sys, time, urllib.request
import concept_add as C

IDX = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\4c6fe2ff-c3a6-47fb-8b54-226f916ad6af\scratchpad\img\film\idx.json"
WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "film_stills_0929")
SLOTS = ["Still", "Still 2", "Still 3"]

REPLACE = [31, 70, 125, 131, 161, 169, 183, 187, 195, 247, 265, 275, 280, 281, 285, 293, 297, 300, 301, 304, 324,
           339, 361, 375, 380, 384, 395]
DROP = {2, 36, 39, 44, 63, 64, 94, 95, 113, 114, 116, 122, 128, 129, 133, 144, 147, 148, 152, 154, 155, 157, 160, 165,
        170, 171, 178, 184, 196, 197, 204, 234, 236, 237, 239, 242, 261, 268, 273, 282, 295, 298, 333, 334, 347, 350,
        351, 359, 372, 381, 382, 385, 390, 393}
FRONT = {1: 0, 335: 333}      # this slot becomes the front; the old front (same film) moves into the gallery or is dropped
CAP = {
 0: "Georges Méliès (left) in his glass studio at Montreuil", 1: "The capsule lands in the eye of the Moon",
 3: "Lillian Gish, the woman who rocks the cradle", 4: "Mae Marsh in the modern story",
 5: "D. W. Griffith (left) and his crew during filming", 7: "A painted set: the town of Holstenwall",
 8: "Werner Krauss as Dr. Caligari", 10: "George O'Brien and Margaret Livingston, the woman from the city",
 11: "Brigitte Helm on set as the <i>Maschinenmensch</i>", 12: "The <i>Maschinenmensch</i> brought to life",
 13: "The <i>Maschinenmensch</i> on set", 15: "Renée Falconetti, shot from below; Dreyer dug holes in the set for the low angles",
 16: "Marlene Dietrich as Lola Lola", 17: "Marlene Dietrich in her cabaret pose", 20: "The Tramp meets the blind flower girl",
 22: "Groucho Marx and Margaret Dumont", 23: "Groucho Marx in one of his costumes from the war sequence",
 24: "Kong sets Ann Darrow (Fay Wray) in a tree before fighting a <i>Tyrannosaurus</i>",
 25: "A colour publicity image combining live actors with stop-motion animation",
 26: "The producer Merian C. Cooper with the full-size mechanical head used for close-ups",
 28: "Boris Karloff as the Monster", 29: "Elsa Lanchester as the Monster's mate",
 30: "Boris Karloff, James Whale, and the cinematographer John J. Mescall on set",
 32: "Judy Garland as Dorothy, with Terry as Toto", 33: "Judy Garland as Dorothy", 34: "Billie Burke as Glinda and Judy Garland as Dorothy",
 35: "Nora Gregor, Jean Renoir, Pierre Nay, and Pierre Magnier at the rabbit hunt",
 37: "Clark Gable and Vivien Leigh as Rhett and Scarlett", 38: "Hattie McDaniel, Olivia de Havilland, and Vivien Leigh",
 40: "Cary Grant, Rosalind Russell, and Ralph Bellamy in a publicity photograph", 41: "Cary Grant and Rosalind Russell (right)",
 42: "Cary Grant and Rosalind Russell, in a costume by Robert Kalloch",
 43: "Kane shouts down the stairs after the departing Boss Jim W. Gettys", 45: "Orson Welles and Ruth Warrick in the breakfast montage",
 46: "Humphrey Bogart in the airport scene", 47: "Paul Henreid, Ingrid Bergman, Claude Rains, and Humphrey Bogart",
 48: "Humphrey Bogart and Ingrid Bergman", 49: "Carole Lombard in a publicity still", 51: "Dana Andrews as Detective Mark McPherson",
 52: "Clifton Webb, Gene Tierney, and Vincent Price in the trailer", 53: "Gene Tierney in a publicity photograph",
 56: "Marius Goring, David Niven, Roger Livesey, Kim Hunter, and Robert Coote",
 57: "Marius Goring as Conductor 71 and David Niven as Peter Carter",
 58: "James Stewart and Gloria Grahame as George Bailey and Violet Bick", 59: "Lionel Barrymore as Henry Potter",
 60: "James Stewart, Donna Reed, and Karolyn Grimes as George, Mary, and Zuzu Bailey",
 62: "Alec Guinness in six of his eight roles, with Valerie Hobson (second from left)",
 68: "Gloria Swanson and William Holden", 69: "Gloria Swanson and Billy Wilder",
 71: "Robert Mitchum as the preacher Harry Powell, with Shelley Winters",
 72: "Stanley Cortez's expressionist lighting in the bedroom scene", 75: "Yasujirō Ozu (far right) on set",
 78: "Ogata, Yamada, an old fisherman, Emiko, and Professor Yamane", 79: "The monster, whose design drew on several dinosaurs",
 81: "Jim Stark (James Dean) in police custody", 82: "Jim confronts his father as his mother watches",
 84: "Apu and Durga run to see the train", 85: "A still shown in the MoMA's 1955 exhibition <i>The Family of Man</i>",
 86: "The apocalyptic final scene", 88: "Ethan (John Wayne) and his brother's wife, Martha", 89: "Captain Clayton and Ethan, caught in a trap",
 91: "The dance of death along the hilltop", 93: "Kim Novak as Madeleine, waking in Scottie's bed",
 97: "Tony Curtis and Jack Lemmon as Josephine and Daphne", 98: "Tony Curtis as “Shell Oil Junior” and Marilyn Monroe as Sugar",
 99: "Billy Wilder and Marilyn Monroe during filming", 103: "Jean Seberg and Jean-Paul Belmondo",
 105: "The formal garden, where the guests cast shadows and the trees do not",
 109: "General Buck Turgidson (George C. Scott) imitating a low-flying B-52", 110: "Wing Attack Plan R, fresh from the cockpit safe",
 111: "The War Room and its Big Board", 112: "Christopher Plummer and Julie Andrews on location in Salzburg",
 117: "Mary Woronov in the colour reel, beside a black-and-white one", 118: "Jacques Tati as Monsieur Hulot",
 119: "The office set, a maze of cubicles", 120: "The apartments: cubicles for living, seen from the street",
 124: "The zero-gravity effect", 126: "Sam Peckinpah sets up the final gunfight at “Agua Verde”",
 132: "Marlon Brando and Al Pacino as Vito and Michael Corleone", 136: "The red coat, a motif throughout",
 145: "Diane Keaton's Annie Hall look, which set a late-1970s fashion", 146: "Luke, Leia, and Han",
 150: "The crew: Ian Holm, Harry Dean Stanton, Sigourney Weaver, Yaphet Kotto, Tom Skerritt, Veronica Cartwright, and John Hurt",
 153: "The officers of <i>U-96</i>", 158: "A police spinner among the skyscrapers", 167: "Bruce Willis as the boxer Butch",
 175: "The Paul Bunyan statue made for the film by Rick Heinrichs",
 201: "Justus D. Barnes fires at the audience in the final shot",
 203: "May McAvoy and Al Jolson, in blackface, before the dress rehearsal", 205: "Jack Robin on stage in the final scene, in a publicity shot",
 206: "Max Schreck as Count Orlok", 207: "Max Schreck in a promotional still", 208: "Orlok's shadow climbs the staircase",
 210: "The ant-filled hand caught in the door", 211: "Johnny Eck and Angelo Rossitto", 212: "Among the circus performers",
 215: "Brigid O'Shaughnessy and Joel Cairo clash in front of the police", 216: "Veronica Lake and Joel McCrea",
 217: "Fred MacMurray and Barbara Stanwyck as Walter Neff and Phyllis Dietrichson", 218: "Edward G. Robinson as the claims man Barton Keyes",
 219: "Barbara Stanwyck in the blond wig Billy Wilder chose to look cheap", 220: "Maya Deren on the stairs",
 221: "Laura and Alec (Celia Johnson and Trevor Howard) part at the station", 223: "Marius Goring as the composer Julian Craster",
 224: "Moira Shearer in the Ballet of the Red Shoes", 225: "Bette Davis in a publicity still", 226: "George Sanders as Addison DeWitt",
 227: "Marilyn Monroe as Miss Casswell, with Anne Baxter, Bette Davis, and George Sanders",
 228: "Alfonso Mejía (right, behind) as Pedro", 229: "Roberto Cobo as El Jaibo", 230: "Mario Ramírez and Roberto Cobo (right)",
 232: "Anthony Quinn and Giulietta Masina", 233: "Giulietta Masina as Gelsomina",
 238: "Tony tells the bound César, “I liked you, Macaroni”", 243: "Orson Welles as Hank Quinlan", 244: "Janet Leigh and Charlton Heston",
 245: "Orson Welles, Victor Millan, Joseph Calleia, and Charlton Heston", 246: "Carl Boehm as Mark Lewis",
 248: "Anthony Perkins, Alfred Hitchcock, and Janet Leigh on set", 249: "The figure in the shower scene",
 250: "Deborah Kerr by candlelight; Freddie Francis darkened the edges of the frame", 251: "One of Jim Clark's layered dissolves",
 253: "Jose De Vega, Natalie Wood, and George Chakiris as Chino, Maria, and Bernardo", 254: "The Jets attack Anita at Doc's drugstore",
 257: "Talos seizes the <i>Argo</i>", 258: "Jason fights the Hydra", 259: "Jason and his companions fight the skeletons",
 264: "Liv Ullmann, who said she was cast for her face", 267: "Mia Farrow as Rosemary Woodhouse", 272: "Malcolm McDowell as Alex DeLarge",
 286: "The exploding-head effect in the tenement raid", 288: "Shot at magic hour, around dawn and dusk",
 289: "The locusts: peanut shells dropped from helicopters, run in reverse", 291: "Cathy Moriarty and Joe Pesci",
 292: "Robert De Niro training with the real Jake LaMotta", 294: "“Here's Johnny!”", 306: "The criminals' slow-motion walk in the opening",
 312: "Homayoun Ershadi as Mr. Badii", 316: "Betty (Naomi Watts) arrives in Los Angeles, with Irene (Jeanne Bates)",
 317: "Michael J. Anderson as Mr. Roque", 318: "Diane and Camilla", 329: "The miniature hotel built for the film",
 331: "Buster Keaton riding the cowcatcher", 332: "Buster Keaton with the Union mortar", 335: "The Tramp in the machine",
 336: "Katharine Hepburn as Susan Vance", 337: "Katharine Hepburn and Cary Grant",
 338: "Katharine Hepburn and the leopard Nissa in a publicity photograph", 340: "Grace Kelly as Lisa Fremont",
 341: "James Stewart as L. B. Jefferies", 342: "James Stewart, Grace Kelly, and Alfred Hitchcock on set",
 344: "Ingmar Bergman (left) and Victor Sjöström during filming in Solna", 345: "Cary Grant in a still from the film",
 346: "James Mason, Eva Marie Saint, and Cary Grant at Mount Rushmore during filming", 349: "Peter O'Toole as T. E. Lawrence",
 352: "Marcello Mastroianni as Guido Anselmi", 353: "Anouk Aimée as Luisa Anselmi",
 386: "The house, built on a set; everything above the ground floor was added digitally",
}


def tmdb_candidates(nid, title, orig, year, director):
    import film_stills as S
    directors = [S.surname(d) for d in re.split(r",| and |;|&", director) if S.surname(d)]
    hit = None
    for q in [title, orig]:
        if not q or hit:
            continue
        for yr in ([year] if year else []) + [None]:
            for r in S.tmdb("/search/movie", query=q, **({"year": yr} if yr else {}))["results"][:5]:
                crew = S.tmdb("/movie/%d/credits" % r["id"])["crew"]
                dirs = " ".join(C.fold(c["name"]) for c in crew if c.get("job") == "Director")
                if not directors or any(d in dirs for d in directors):
                    hit = r
                    break
            if hit:
                break
    if not hit:
        return None, []
    imgs = [b for b in S.tmdb("/movie/%d/images" % hit["id"])["backdrops"] if not b.get("iso_639_1")]
    imgs.sort(key=lambda b: (-(b.get("vote_count") or 0) * (b.get("vote_average") or 0), -b["width"]))
    out = []
    for k, b in enumerate(imgs[:4]):
        local = os.path.join(WORK, "%d_%d.jpg" % (nid, k))
        if not os.path.exists(local):
            open(local, "wb").write(urllib.request.urlopen("https://image.tmdb.org/t/p/w1280" + b["file_path"], timeout=60).read())
            time.sleep(0.2)
        out.append(local)
    return hit["id"], out


def find():
    sys.path.insert(0, os.path.dirname(IDX) + r"\..\..")
    import wm
    os.makedirs(WORK, exist_ok=True)
    idx = json.load(open(IDX, encoding="utf-8"))
    plan, tiles = {}, []
    for i in REPLACE:
        r = idx[i]
        f = C.anki("notesInfo", notes=[r["nid"]])[0]["fields"]
        year = (re.findall(r"\d{4}", f["Year"]["value"]) or [""])[0]
        tid, cands = tmdb_candidates(r["nid"], C.plain(f["Title"]["value"]), C.plain(f["Original title"]["value"]), year,
                                     C.plain(f["Director"]["value"]))
        plan[i] = {"nid": r["nid"], "title": r["title"], "tmdb": tid, "cands": cands}
        tiles += [("%d.%d %s" % (i, k, r["title"][:30]), p) for k, p in enumerate(cands)]
        print(i, r["title"], tid, len(cands), flush=True)
    json.dump(plan, open(os.path.join(WORK, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    out = os.path.dirname(IDX)
    for s in range(0, len(tiles), 24):
        wm.sheet(tiles[s:s + 24], os.path.join(out, "repl_%02d.jpg" % (s // 24)), cols=4, W=300)


def apply(picks_path):
    idx = json.load(open(IDX, encoding="utf-8"))
    plan = json.load(open(os.path.join(WORK, "plan.json"), encoding="utf-8"))
    picks = {int(k): v for k, v in json.load(open(picks_path, encoding="utf-8")).items()}
    by_note = {}
    for i, r in enumerate(idx):
        by_note.setdefault(r["nid"], []).append(i)
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(by_note))}
    changes, stored = {}, []
    for nid, slots in by_note.items():
        n = ns[nid]
        cur = {idx[i]["field"]: i for i in slots}
        # build the new ordered list of (image html, caption) for the three slots
        order = [cur[s] for s in SLOTS if s in cur]
        front = next((a for a, b in FRONT.items() if b in order), None)
        if front is not None:
            order.remove(front)
            order.insert(0, front)
        new = []
        for i in order:
            if i in DROP and i not in FRONT:
                continue
            if i in picks or (i in REPLACE and i not in picks):
                continue
            new.append(('<img src="%s">' % idx[i]["file"], CAP.get(i, idx[i]["cap"])))
        front_repl = next((i for i in order if i in picks), None)
        if front_repl is not None:
            p = plan[str(front_repl)]
            fn = "film-tmdb-%d-0929.jpg" % p["tmdb"]
            stored.append((fn, p["cands"][picks[front_repl]]))
            new.insert(0, ('<img src="%s">' % fn, ""))
        f = {}
        for k, s in enumerate(SLOTS):
            img, cap = new[k] if k < len(new) else ("", "")
            if n["fields"][s]["value"] != img:
                f[s] = img
            if n["fields"][s + " caption"]["value"] != cap:
                f[s + " caption"] = cap
        if f:
            changes[nid] = f
    for nid, f in changes.items():
        print(C.plain(ns[nid]["fields"]["Title"]["value"])[:34], {k: C.plain(v)[:50] or re.sub(r'.*src="([^"]+)".*', r"\1", v) for k, v in f.items()})
    print(len(changes), "notes;", len(stored), "new stills")
    if "--apply" in sys.argv:
        json.dump({str(nid): {k: ns[nid]["fields"][k]["value"] for k in f} for nid, f in changes.items()},
                  open("backups/film_img_0929_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for fn, path in stored:
            C.anki("storeMediaFile", filename=fn, path=path)
        for nid, f in changes.items():
            C.anki("updateNoteFields", note={"id": nid, "fields": f})
        print("applied")


def extras():
    """The posters and director pictures, looked at the same way (all 250 posters, all 38 directors).

    Murderers Among Us (1946) carried the poster of the 1989 Simon Wiesenthal television film with Ben
    Kingsley, which shares its English title; it now has the 1946 poster. Two "Release poster" captions
    were on pictures that are not posters: Méliès's title card and a frame of Meshes of the Afternoon.
    Andrei Tarkovsky had no picture; no free photograph of him exists, and every Wikipedia uses the 2007
    Russian stamp, so that is what he gets, captioned as such.
    """
    W = WORK
    fx = {1790241046903: {"Poster": ("filmposter-murderers-among-us-1946.jpg", os.path.join(W, "murderers_poster_0.jpg")),
                          "Poster caption": "Release poster &middot; Wolfgang Staudte, 1946"},
          1790240557767: {"Poster caption": "Title card &middot; Georges Méliès, 1902"},
          1790241046840: {"Poster caption": "Maya Deren at the window"},
          1790254935884: {"Picture": ("filmdir-andrei-tarkovsky-stamp.jpg", os.path.join(W, "tarkovsky.jpg")),
                          "Caption": "On a Russian stamp of 2007"}}
    ns = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(fx))}
    for nid, f in fx.items():
        print(C.plain(ns[nid]["fields"]["Title"]["value"]), {k: (v[0] if isinstance(v, tuple) else v) for k, v in f.items()})
    if "--apply" in sys.argv:
        json.dump({str(nid): {k: ns[nid]["fields"][k]["value"] for k in f} for nid, f in fx.items()},
                  open("backups/film_img_extras_0929_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for nid, f in fx.items():
            out = {}
            for k, v in f.items():
                if isinstance(v, tuple):
                    C.anki("storeMediaFile", filename=v[0], path=v[1])
                    out[k] = '<img src="%s">' % v[0]
                else:
                    out[k] = v
            C.anki("updateNoteFields", note={"id": nid, "fields": out})
        print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1] == "find":
        find()
    elif sys.argv[1] == "extras":
        extras()
    else:
        apply(sys.argv[2])
