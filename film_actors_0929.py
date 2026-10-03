# -*- coding: utf-8 -*-
"""film_actors_0929.py -- step 1 of the Film actor cards: which of the greatest actors quizbowl asks.

Carter, 2026-10-01: "yes, do the actor card -- but use imdb or other established websites + qbreader
database to list only of the greatest actors ever". The candidates are the union of two established
rankings:
  * AFI's 100 Years...100 Stars (1999): the 25 male and 25 female screen legends;
  * Empire's 50 Greatest Actors of All Time (2022).
Each candidate is scored on qbreader (Fine Arts, answer lines and all mentions, retier2.py's name search),
and only the ones quizbowl actually asks become cards. Chaplin, Keaton, and Welles already have Film
director cards, and Fred Astaire, Gene Kelly, and Ginger Rogers have Performing Arts cards, so they are
left out; so are the Marx Brothers, a group.

    py -3.9 film_actors_0929.py            (writes data/film_actors_evidence_0929.json, resumable)
"""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
import retier2 as R

OUT = "data/film_actors_evidence_0929.json"

AFI = """Humphrey Bogart; Cary Grant; James Stewart; Marlon Brando; Henry Fonda; Clark Gable; James Cagney; Spencer Tracy;
Gary Cooper; Gregory Peck; John Wayne; Laurence Olivier; Kirk Douglas; James Dean; Burt Lancaster; Sidney Poitier;
Robert Mitchum; Edward G. Robinson; William Holden; Katharine Hepburn; Bette Davis; Audrey Hepburn; Ingrid Bergman;
Greta Garbo; Marilyn Monroe; Elizabeth Taylor; Judy Garland; Marlene Dietrich; Joan Crawford; Barbara Stanwyck;
Claudette Colbert; Grace Kelly; Mae West; Vivien Leigh; Lillian Gish; Shirley Temple; Rita Hayworth; Lauren Bacall;
Sophia Loren; Jean Harlow; Carole Lombard; Mary Pickford; Ava Gardner"""
EMPIRE = """Denzel Washington; Tom Hanks; Robert De Niro; Natalie Portman; Gene Hackman; Heath Ledger; Tom Cruise;
Leonardo DiCaprio; Tilda Swinton; Samuel L. Jackson; Toshiro Mifune; Nicolas Cage; Viola Davis; Cate Blanchett;
Alec Guinness; Michael Caine; Michelle Yeoh; Tom Hardy; Philip Seymour Hoffman; Jack Nicholson; Meryl Streep;
Christian Bale; Michelle Williams; Anthony Hopkins; Gary Oldman; Florence Pugh; Julianne Moore; Shah Rukh Khan;
Charlize Theron; Kate Winslet; Penélope Cruz; Al Pacino; Frances McDormand; Joaquin Phoenix; Morgan Freeman;
Paul Newman; Olivia Colman; Daniel Day-Lewis; Nicole Kidman"""
CANDIDATES = list(dict.fromkeys(c.strip() for c in (AFI + ";" + EMPIRE).replace("\n", " ").split(";") if c.strip()))


def score(name):
    a = R.ids_for(name, set(), "answer", True)
    m = R.ids_for(name, set(), "all", True)
    return {"name": name, "ans": len(a), "all": len(m), "afi": name in AFI, "empire": name in EMPIRE}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    done = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    todo = [c for c in CANDIDATES if c not in done]
    with ThreadPoolExecutor(2) as ex:
        for r in ex.map(score, todo):
            done[r["name"]] = r
            json.dump(done, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
            print("%-26s ans %3d all %4d" % (r["name"], r["ans"], r["all"]), flush=True)
