# -*- coding: utf-8 -*-
"""cm_add_1002.py -- the Classical Music gap: composers and works quizbowl asks that the deck did not cover.

Carter, 2026-10-02: "Do the music gap." Measured against the 10,414 auditory and opera tossups and checked on
qbreader (strict answer lines, Fine Arts), the deck's real gaps were composers with real volume and nothing (or
one work) in the deck, and a few heavily asked works:
  composers: John Cage 92 answer lines (only 4'33" in the deck), Sousa 52, Penderecki 35 (no active card),
             Honegger 30, William Grant Still 13, Ginastera 12, La Monte Young 9, Florence Price 7, Amy Beach 6
             (41 mentions), Lili Boulanger 5; Meredith Monk (3) is left out;
  works:     Haydn's "Farewell" (18 answer lines; the note existed, waiting on a clip, and gets one), Smetana's "From My Life" (9 / 71 mentions), The Stars and
             Stripes Forever (8 / 82), Pacific 231 (8 / 49), Sonatas and Interludes (2 / 52), St. Luke Passion (5).
Tiers on the Music scale (tier 1 at 10+ answer lines or 40+ mentions); a composer's signature work carries the
composer's own evidence, since the deck teaches composers through their works. Penderecki's Threnody, his
signature work, moves to tier 1. Each note has one Clue, a Description, and a 45-second clip normalised to
-17 LUFS; Sousa's is the U.S. Marine Band's public-domain recording on Commons, the rest personal-study excerpts
(no free recordings exist), as for Nixon in China. AUDIO to COMPOSER cards stay suspended, as across the deck.
Nickname is pre-formatted in qb-e9's 2026-10-02 style: a true nickname in curly quotes, a title in (<i>...</i>).

    py -3.9 cm_add_1002.py [--apply]
"""
import json, os, sys, time
import concept_add as C

CLIPS = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "cm_add_1002")
THRENODY = "<i>Threnody for the Victims of Hiroshima</i>"

N = [
    dict(clip="haydn45-iv", tier=1, style=None,
         Work="<i>Symphony No. 45</i>", Composer="Joseph Haydn", **{"Composer Dates": "1732–1809"}, Nationality="Austrian",
         Movement="mvt. IV · <i>Finale: Presto – Adagio</i>", Catalogue="Hob. I:45", Key="F-sharp minor", Nickname="“Farewell”",
         Date="1772", Period="Classical", Genre="Symphony",
         Clue="Its finale slows into an Adagio in which the players snuff their candles and leave one by one until two violins remain, a hint to Prince Esterházy that the musicians wanted to go home.",
         Description="Written at Eszterháza in 1772, when the prince had kept the orchestra from their families too long; he took the hint and let them leave the next day. A rare symphony in F-sharp minor, from Haydn's <i>Sturm und Drang</i> years.",
         Listen="The finale's slow coda: a gentle Adagio whose texture thins and quietens as the instruments fall silent one after another."),
    dict(clip="smetana-q1", tier=1, style="nationalist",
         Work="<i>String Quartet No. 1</i>", Composer="Bedřich Smetana", **{"Composer Dates": "1824–1884"}, Nationality="Czech",
         Movement="mvt. I · <i>Allegro vivo appassionato</i>", Catalogue="JB 1:105", Key="E minor", Nickname="(<i>From My Life</i>)",
         Date="1876", Period="Romantic", Genre="String quartet",
         Clue="An autobiographical string quartet whose finale is cut short by a long, piercing high E in the first violin, the ringing in its composer's ear that came before his deafness.",
         Description="Smetana's account of his life, from youthful romance to the tinnitus and deafness that struck him in 1874; he gave the viola the passionate opening theme.",
         Listen="Over agitated tremolo in the other strings, the viola launches a passionate, surging E-minor theme."),
    dict(clip="sousa-stars", tier=1, style=None,
         Work="<i>The Stars and Stripes Forever</i>", Composer="John Philip Sousa", **{"Composer Dates": "1854–1932"}, Nationality="American",
         Date="1896", Period="Romantic", Genre="March",
         Clue="A march written on a ship home from Europe in 1896, whose final strain adds a famous piccolo obbligato; Congress made it the national march of the United States in 1987.",
         Description="By the “March King”, who led the U.S. Marine Band before touring the world with his own; the recording is the Marine Band's.",
         Listen="A brisk introduction for full band, then the first strain of the march over an oom-pah bass."),
    dict(clip="honegger-pacific", tier=1, style=None,
         Work="<i>Pacific 231</i>", Composer="Arthur Honegger", **{"Composer Dates": "1892–1955"}, Nationality="Swiss",
         Catalogue="H. 53", Date="1923", Period="Modern", Genre="Orchestral",
         Clue="An orchestral “symphonic movement” of a steam locomotive starting up and thundering along, named for a type of engine with a 2-3-1 wheel arrangement.",
         Description="By a member of Les Six, who said he loved locomotives as others love women or horses; he called the piece a study in mounting speed while the actual tempo slows.",
         Listen="Low strings hiss and sigh like escaping steam, then the orchestra begins to churn as the engine pulls away."),
    dict(clip="cage-sonata5", tier=1, style="avant-garde",
         Work="<i>Sonatas and Interludes</i>", Composer="John Cage", **{"Composer Dates": "1912–1992"}, Nationality="American",
         Movement="Sonata V", Date="1946–1948", Period="Modern", Genre="Solo piano",
         Clue="Sixteen sonatas and four interludes for a piano “prepared” with screws, bolts, and rubber between its strings, meant to express the permanent emotions of Indian aesthetics.",
         Description="The largest work for the prepared piano, which Cage invented for a 1940 dance by Syvilla Fort; the preparations turn the piano into something like a gamelan.",
         Listen="Muted, woody, and gong-like tones from the prepared piano in a lilting, dance-like rhythm."),
    dict(clip="penderecki-luke", tier=2, style="avant-garde",
         Work="<i>St. Luke Passion</i>", Composer="Krzysztof Penderecki", **{"Composer Dates": "1933–2020"}, Nationality="Polish",
         Movement="Part I · <i>O Crux ave</i>", Date="1966", Period="Modern", Genre="Oratorio",
         Clue="A Latin Passion written for the 700th anniversary of Münster Cathedral, whose music spells out B-A-C-H and ends on a blazing E-major chord.",
         Description="One of the first major sacred works from behind the Iron Curtain, mixing tone clusters and twelve-tone rows with Gregorian chant.",
         Listen="The opening hymn: dense choral clusters and swelling cries of “O crux” over a dark, low orchestra."),
    dict(clip="beach-gaelic", tier=1, style="late-romantic",
         Work="<i>Symphony in E minor</i>", Composer="Amy Beach", **{"Composer Dates": "1867–1944"}, Nationality="American",
         Movement="mvt. I · <i>Allegro con fuoco</i>", Catalogue="Op. 32", Key="E minor", Nickname="“Gaelic”",
         Date="1896", Period="Romantic", Genre="Symphony",
         Clue="Built on Irish folk tunes, it was the first symphony composed and published by an American woman, premiered by the Boston Symphony Orchestra in 1896.",
         Description="Beach, largely self-taught, belonged to the Second New England School; she wrote it partly in answer to Dvořák's call for an American music drawn from folk song.",
         Listen="A stormy, surging opening in the full orchestra, like a gale at sea, before a bold theme emerges."),
    dict(clip="still-afro", tier=1, style="nationalist",
         Work="<i>Afro-American Symphony</i>", Composer="William Grant Still", **{"Composer Dates": "1895–1978"}, Nationality="American",
         Movement="mvt. I · <i>Moderato assai</i>", Date="1930", Period="Modern", Genre="Symphony",
         Clue="The first symphony by a Black American composer played by a major orchestra, the Rochester Philharmonic in 1931; it adds a banjo and builds its themes on the blues.",
         Description="Still, later the first Black American to conduct a major U.S. orchestra, prefaced each movement with lines by Paul Laurence Dunbar.",
         Listen="A plaintive solo in the English horn, bending its notes in the inflections of the blues."),
    dict(clip="ginastera-malambo", tier=1, style="nationalist",
         Work="<i>Estancia</i>", Composer="Alberto Ginastera", **{"Composer Dates": "1916–1983"}, Nationality="Argentine",
         Movement="<i>Danza final (Malambo)</i>", Catalogue="Op. 8", Date="1941", Period="Modern", Genre="Ballet",
         Clue="A ballet of a day on an Argentine cattle ranch, whose suite ends with a malambo, the gauchos' competitive foot-stamping dance.",
         Description="Commissioned by Lincoln Kirstein's American Ballet Caravan, which broke up before staging it; the suite was heard in 1943, the full ballet only in 1952.",
         Listen="Driving, syncopated rhythms hammered out by brass, xylophone, and percussion, building relentlessly."),
    dict(clip="young-wtp", tier=2, style="minimalist",
         Work="<i>The Well-Tuned Piano</i>", Composer="La Monte Young", **{"Composer Dates": "born 1935"}, Nationality="American",
         Date="1964–", Period="Modern", Genre="Solo piano",
         Clue="A minimalist improvisation of five hours or more on a piano retuned in just intonation, performed in the composer's Dream House under Marian Zazeela's lights.",
         Description="By a founder of minimalism, who also wrote <i>Composition 1960 #7</i>: a perfect fifth, B and F-sharp, “to be held for a long time”.",
         Listen="Slow, resonating piano figures in a pure, unfamiliar tuning, blurring into a shimmering haze."),
    dict(clip="price-juba", tier=2, style="nationalist",
         Work="<i>Symphony No. 1</i>", Composer="Florence Price", **{"Composer Dates": "1887–1953"}, Nationality="American",
         Movement="mvt. III · <i>Juba Dance</i>", Key="E minor", Date="1932", Period="Modern", Genre="Symphony",
         Clue="Its third movement is a Juba dance; in 1933 it became the first symphony by a Black woman played by a major American orchestra, the Chicago Symphony.",
         Description="It won the 1932 Wanamaker Prize; Price's reputation revived after a trove of her manuscripts turned up in an abandoned house in Illinois in 2009.",
         Listen="A syncopated, ragtime-flavoured dance tune, bright and bouncing in the strings."),
    dict(clip="boulanger-faust", tier=2, style="impressionist",
         Work="<i>Faust et Hélène</i>", Composer="Lili Boulanger", **{"Composer Dates": "1893–1918"}, Nationality="French",
         Date="1913", Period="Modern", Genre="Cantata",
         Clue="A cantata on Goethe's <i>Faust</i> that made its nineteen-year-old composer the first woman to win the Prix de Rome in composition.",
         Description="Lili Boulanger, younger sister of the teacher Nadia Boulanger, died at twenty-four in 1918.",
         Listen="A hushed orchestral introduction of murmuring strings and woodwind."),
]

NAMES = {1: "tier1-core", 2: "tier2-solid"}


def slug(s):
    return C.fold(s).lower().replace(" ", "-")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    have = {(C.plain(n["fields"]["Work"]["value"]), C.plain(n["fields"]["Composer"]["value"]))
            for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Classical Music"'))}
    todo = [d for d in N if (C.plain(d["Work"]), d["Composer"]) not in have]
    for d in todo:
        assert os.path.getsize(os.path.join(CLIPS, "cmc4-%s.mp3" % d["clip"])) > 100000, d["clip"]
        print("%-36s %-22s tier %d" % (C.plain(d["Work"]), d["Composer"], d["tier"]))
    thr = C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Classical Music" "Work:%s"' % THRENODY))
    print("Threnody notes:", [(n["noteId"], [t for t in n["tags"] if "::tier::" in t]) for n in thr])
    if "--apply" in sys.argv:
        tm = list(C.anki("modelTemplates", modelName="Classical Music"))
        for d in todo:
            fn = "cmc4-%s.mp3" % d["clip"]
            C.anki("storeMediaFile", filename=fn, path=os.path.join(CLIPS, fn))
            f = {k: v for k, v in d.items() if k not in ("clip", "tier", "style")}
            f["Audio"] = "[sound:%s]" % fn
            f["Hint"] = "Period=%s|Genre=%s|Composed=%s" % (d["Period"], d["Genre"], d["Date"])
            tags = ["Music::genre::" + slug(d["Genre"]), "Music::period::" + slug(d["Period"]), "Music::tier::" + NAMES[d["tier"]], "Music::gap_1002"]
            if d["style"]:
                tags.append("Music::style::" + d["style"])
            nid = C.anki("addNote", note={"deckName": "Classical Music", "modelName": "Classical Music", "fields": f, "tags": tags,
                                          "options": {"allowDuplicate": True}})   # same title, other composer ("String Quartet No. 1")
            cards = C.anki("cardsInfo", cards=C.anki("findCards", query="nid:%d" % nid))
            sus = [c["cardId"] for c in cards if d["tier"] != 1 or tm[c["ord"]] == "AUDIO to COMPOSER"]
            if sus:
                C.anki("suspend", cards=sus)
        # Haydn 45 was already in the deck (added 2026-09-28), waiting on a clip: fill it rather than duplicate it
        hd = [d for d in N if d["clip"] == "haydn45-iv"][0]
        for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Classical Music" Composer:*Haydn* "Work:<i>Symphony No. 45</i>"')):
            if n["fields"]["Audio"]["value"]:
                continue
            C.anki("storeMediaFile", filename="cmc4-haydn45-iv.mp3", path=os.path.join(CLIPS, "cmc4-haydn45-iv.mp3"))
            json.dump({"nid": n["noteId"], "fields": {k: n["fields"][k]["value"] for k in ("Audio", "Movement", "Listen")}},
                      open("backups/cm_add_1002_haydn45_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": {"Audio": "[sound:cmc4-haydn45-iv.mp3]",
                                                                         "Movement": hd["Movement"], "Listen": hd["Listen"]}})
            cards = C.anki("cardsInfo", cards=C.anki("findCards", query="nid:%d" % n["noteId"]))
            C.anki("suspend", cards=[c["cardId"] for c in cards if tm[c["ord"]] == "AUDIO to COMPOSER"])
        for n in thr:
            if "Music::tier::tier1-core" in n["tags"]:
                continue
            json.dump({"nid": n["noteId"], "tags": n["tags"]}, open("backups/cm_add_1002_threnody_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"))
            for t in [t for t in n["tags"] if "::tier::" in t]:
                C.anki("removeTags", notes=[n["noteId"]], tags=t)
            C.anki("addTags", notes=[n["noteId"]], tags="Music::tier::tier1-core Music::retier_2026-10-02")
            cards = C.anki("cardsInfo", cards=n["cards"])
            C.anki("unsuspend", cards=[c["cardId"] for c in cards if tm[c["ord"]] != "AUDIO to COMPOSER"])
        print("added", len(todo), "; Threnody promoted")
