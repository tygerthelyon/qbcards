# -*- coding: utf-8 -*-
"""director_add_1001.py -- 53 director cards from the critical canon, chosen on academic quizbowl evidence.

Carter, 2026-10-01: "add the director cards. ... do a search of a couple of well established lists and critic
reviews; i want to cover the real world canon of famous directors that could come up in quiz."

The canon: They Shoot Pictures, Don't They?'s Top 250 Directors (2026 edition), an aggregate of thousands of
critics' and filmmakers' lists, checked against Sight & Sound's directors ranked by votes in its 2022 polls.
47 of the 249 already had cards. The other 202 were scored on qbreader, Fine Arts only
(director_evidence_1001.py): strict answer lines (the name is the main answer) and all mentions. Kept:
  * every director with three or more strict answer lines (45), and
  * the TSPDT top 60 with any evidence below that (Mizoguchi, Akerman, Resnais, Donen, Vigo, Tati, Hou
    Hsiao-hsien, Claire Denis), so the core of the canon is covered;
  * not Andy Warhol (his answer lines are for his visual art) or Bob Fosse (a Performing Arts card).
Written like the existing director cards: one clue that never names the director, key films with the
signature one underlined, a detail, a TMDB portrait looked at on a contact sheet. Tiers by the History rule
on the strict count and mentions; only tier 1 is studied. film_order_1001.py puts each intro card first.

    py -3.9 director_add_1001.py find        (TMDB portraits and contact sheets)
    py -3.9 director_add_1001.py [--apply]   (with data/director_picks_portraits_1001.json)
"""
import json, os, re, sys, urllib.request
import concept_add as C

WORK = os.path.join(os.environ["LOCALAPPDATA"], "QB_caches", "directors_1001")
EVID = "data/director_evidence_1001.json"
PICKS = "data/director_picks_portraits_1001.json"
SP = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\4c6fe2ff-c3a6-47fb-8b54-226f916ad6af\scratchpad"

D = [
    ("Robert Bresson", "1901–1999", "France",
     "The French director who called his non-professional actors “models” and set down his method in <i>Notes on the Cinematograph</i>.",
     "<i>A Man Escaped</i>; <i>Pickpocket</i>; <u><i>Au Hasard Balthazar</i></u>; <i>Mouchette</i>",
     "<i>Au Hasard Balthazar</i> follows a donkey through a string of owners; his last film was <i>L'Argent</i> (1983)."),
    ("Carl Theodor Dreyer", "1889–1968", "Denmark",
     "The Danish director who filmed Renée Falconetti in close-up after close-up as Joan of Arc on trial.",
     "<u><i>The Passion of Joan of Arc</i></u>; <i>Vampyr</i>; <i>Day of Wrath</i>; <i>Ordet</i>",
     "<i>Ordet</i> ends with a woman raised from the dead in her coffin; <i>Gertrud</i> (1964) was his last film."),
    ("Kenji Mizoguchi", "1898–1956", "Japan",
     "The Japanese director of long single takes whose films return again and again to women sold or ruined by men.",
     "<i>The Life of Oharu</i>; <u><i>Ugetsu</i></u>; <i>Sansho the Bailiff</i>; <i>Street of Shame</i>",
     "<i>Ugetsu</i>, in which a potter is seduced by a ghostly noblewoman, and <i>Sansho the Bailiff</i> won Silver Lions at Venice in successive years."),
    ("Roberto Rossellini", "1906–1977", "Italy",
     "His <i>Rome, Open City</i>, shot in a city just freed from German occupation, launched Italian Neorealism.",
     "<u><i>Rome, Open City</i></u>; <i>Paisan</i>; <i>Germany, Year Zero</i>; <i>Journey to Italy</i>",
     "He made five films with Ingrid Bergman, beginning with <i>Stromboli</i>, during an affair that scandalized Hollywood; Isabella Rossellini is their daughter."),
    ("Chantal Akerman", "1950–2015", "Belgium",
     "The Belgian director whose three-hour study of a widow's household routine topped the 2022 <i>Sight and Sound</i> critics' poll.",
     "<i>Je, tu, il, elle</i>; <u><i>Jeanne Dielman, 23 quai du Commerce, 1080 Bruxelles</i></u>; <i>News from Home</i>; <i>No Home Movie</i>",
     "Delphine Seyrig plays Jeanne Dielman, whose days of cooking, cleaning, and sex work slowly unravel; Akerman made it in her mid-twenties."),
    ("Sergei Eisenstein", "1898–1948", "Soviet Union",
     "The Soviet director and theorist of montage who staged a massacre on the Odessa Steps.",
     "<i>Strike</i>; <u><i>Battleship Potemkin</i></u>; <i>October</i>; <i>Alexander Nevsky</i>; <i>Ivan the Terrible</i>",
     "Prokofiev scored <i>Alexander Nevsky</i> and <i>Ivan the Terrible</i>; Stalin banned Part II of <i>Ivan</i>."),
    ("Wong Kar-wai", "born 1958", "Hong Kong",
     "The Hong Kong director, never without dark glasses, of slow-motion longing in neon-lit apartments and noodle stalls.",
     "<i>Chungking Express</i>; <i>Fallen Angels</i>; <i>Happy Together</i>; <u><i>In the Mood for Love</i></u>",
     "Christopher Doyle shot most of his films; Tony Leung and Maggie Cheung play the neighbours of <i>In the Mood for Love</i>."),
    ("Abbas Kiarostami", "1940–2016", "Iran",
     "The Iranian director of zigzag mountain roads, whose Koker trilogy began with a boy trying to return a classmate's notebook.",
     "<i>Where Is the Friend's House?</i>; <i>Close-Up</i>; <u><i>Taste of Cherry</i></u>; <i>Certified Copy</i>",
     "<i>Taste of Cherry</i>, about a man looking for someone to bury him after his suicide, shared the 1997 Palme d'Or."),
    ("Vittorio De Sica", "1901–1974", "Italy",
     "The Italian actor-director who cast a factory worker as the bill-poster searching Rome for his stolen bicycle.",
     "<i>Shoeshine</i>; <u><i>Bicycle Thieves</i></u>; <i>Umberto D.</i>; <i>Two Women</i>",
     "Four of his films won the Academy Award for foreign-language film; Sophia Loren won Best Actress for <i>Two Women</i>."),
    ("John Cassavetes", "1929–1989", "United States",
     "The actor who financed his own raw, improvised-seeming films, beginning with <i>Shadows</i>, often starring his wife, Gena Rowlands.",
     "<i>Shadows</i>; <i>Faces</i>; <u><i>A Woman Under the Influence</i></u>; <i>Opening Night</i>",
     "Called the father of American independent film; he paid for his work by acting, as in <i>Rosemary's Baby</i> and <i>The Dirty Dozen</i>."),
    ("Luchino Visconti", "1906–1976", "Italy",
     "The aristocratic Marxist director whose <i>The Leopard</i> follows a Sicilian prince through the Risorgimento.",
     "<i>Ossessione</i>; <i>La Terra Trema</i>; <i>Rocco and His Brothers</i>; <u><i>The Leopard</i></u>; <i>Death in Venice</i>",
     "<i>Ossessione</i>, an unauthorized <i>The Postman Always Rings Twice</i>, anticipated Neorealism; Burt Lancaster plays the prince in <i>The Leopard</i>."),
    ("Ernst Lubitsch", "1892–1947", "Germany",
     "The Berlin-born Hollywood director whose sly, suggestive comedies gave rise to a “touch” named after him.",
     "<i>Trouble in Paradise</i>; <i>Ninotchka</i>; <i>The Shop Around the Corner</i>; <u><i>To Be or Not to Be</i></u>",
     "<i>To Be or Not to Be</i>, a comedy of Polish actors fooling the Nazis, outraged audiences in 1942; Billy Wilder kept a sign asking “How would Lubitsch do it?”"),
    ("Woody Allen", "born 1935", "United States",
     "The New York comic who won Best Director for a romance with Diane Keaton that ends with her moving to Los Angeles.",
     "<u><i>Annie Hall</i></u>; <i>Manhattan</i>; <i>Hannah and Her Sisters</i>; <i>Crimes and Misdemeanors</i>",
     "He holds the record of sixteen nominations for the screenwriting Academy Award."),
    ("Alain Resnais", "1922–2014", "France",
     "The French Left Bank director who intercut an actress's wartime memories with her affair with a Japanese architect.",
     "<i>Night and Fog</i>; <u><i>Hiroshima mon amour</i></u>; <i>Last Year at Marienbad</i>; <i>Providence</i>",
     "Marguerite Duras wrote <i>Hiroshima mon amour</i> and Alain Robbe-Grillet <i>Last Year at Marienbad</i>."),
    ("Sergio Leone", "1929–1989", "Italy",
     "The Italian director of spaghetti westerns who made Clint Eastwood the Man with No Name.",
     "<i>A Fistful of Dollars</i>; <u><i>The Good, the Bad and the Ugly</i></u>; <i>Once Upon a Time in the West</i>; <i>Once Upon a Time in America</i>",
     "Ennio Morricone scored all his westerns; <i>A Fistful of Dollars</i> remade Kurosawa's <i>Yojimbo</i> without permission."),
    ("Stanley Donen", "1924–2019", "United States",
     "He co-directed <i>Singin' in the Rain</i> with its star, Gene Kelly.",
     "<i>On the Town</i>; <u><i>Singin' in the Rain</i></u>; <i>Funny Face</i>; <i>Charade</i>",
     "A former Broadway dancer; <i>Charade</i>, with Cary Grant and Audrey Hepburn, is often called the best Hitchcock film Hitchcock didn't make."),
    ("Jean Vigo", "1905–1934", "France",
     "The French director who died of tuberculosis at twenty-nine, leaving a featurette of a boarding-school revolt and a feature set on a barge.",
     "<i>À propos de Nice</i>; <i>Zero for Conduct</i>; <u><i>L'Atalante</i></u>",
     "<i>Zero for Conduct</i> was banned in France until 1945; the Prix Jean Vigo is named after him."),
    ("Rainer Werner Fassbinder", "1945–1982", "West Germany",
     "The New German Cinema director who reworked Sirk's <i>All That Heaven Allows</i> as a romance between a cleaning woman and a Moroccan worker.",
     "<u><i>Ali: Fear Eats the Soul</i></u>; <i>The Bitter Tears of Petra von Kant</i>; <i>The Marriage of Maria Braun</i>; <i>Berlin Alexanderplatz</i>",
     "He made more than forty films in about fifteen years before dying at thirty-seven."),
    ("Terrence Malick", "born 1943", "United States",
     "The former philosophy lecturer who shot <i>Days of Heaven</i> almost entirely at magic hour, then made no film for twenty years.",
     "<i>Badlands</i>; <u><i>Days of Heaven</i></u>; <i>The Thin Red Line</i>; <i>The Tree of Life</i>",
     "He translated Heidegger before turning to film; <i>The Tree of Life</i> won the 2011 Palme d'Or."),
    ("Jacques Tati", "1907–1982", "France",
     "The French comic who played the pipe-smoking, raincoated Monsieur Hulot.",
     "<i>Jour de fête</i>; <i>Monsieur Hulot's Holiday</i>; <i>Mon Oncle</i>; <u><i>Playtime</i></u>",
     "He built a glass-and-steel city set for <i>Playtime</i>, nicknamed Tativille; its cost bankrupted him."),
    ("Chris Marker", "1921–2012", "France",
     "The French essay filmmaker whose short science-fiction film is told almost entirely in still photographs.",
     "<u><i>La Jetée</i></u>; <i>Sans Soleil</i>; <i>A Grin Without a Cat</i>",
     "He avoided being photographed, usually sending a picture of a cat instead; <i>La Jetée</i> inspired <i>12 Monkeys</i>."),
    ("Dziga Vertov", "1896–1954", "Soviet Union",
     "The Soviet documentarist of the “kino-eye”, whose city symphony keeps showing its own cameraman and editor at work.",
     "<i>Kino-Pravda</i>; <u><i>Man with a Movie Camera</i></u>; <i>Enthusiasm</i>; <i>Three Songs About Lenin</i>",
     "Born David Kaufman; his brother Mikhail shot <i>Man with a Movie Camera</i>, and his wife, Elizaveta Svilova, edited it."),
    ("Hou Hsiao-hsien", "born 1947", "Taiwan",
     "The Taiwanese New Wave director whose <i>A City of Sadness</i> broke the silence about the 228 Incident.",
     "<i>The Time to Live and the Time to Die</i>; <u><i>A City of Sadness</i></u>; <i>The Puppetmaster</i>; <i>The Assassin</i>",
     "<i>A City of Sadness</i> won the Golden Lion in 1989; <i>The Assassin</i> won him Best Director at Cannes in 2015."),
    ("Krzysztof Kieślowski", "1941–1996", "Poland",
     "The Polish director of ten television films on the Ten Commandments, set in one Warsaw housing estate.",
     "<i>Dekalog</i>; <i>The Double Life of Véronique</i>; <i>Three Colours: Blue</i>; <u><i>Three Colours: Red</i></u>",
     "The Three Colours trilogy takes the French flag's liberty, equality, and fraternity; Irène Jacob stars in <i>Véronique</i> and <i>Red</i>."),
    ("Claire Denis", "born 1946", "France",
     "The French director, raised in colonial Africa, who restaged <i>Billy Budd</i> among Foreign Legionnaires in Djibouti.",
     "<i>Chocolat</i>; <u><i>Beau Travail</i></u>; <i>35 Shots of Rum</i>; <i>High Life</i>",
     "<i>Beau Travail</i> ends with Denis Lavant dancing alone to “The Rhythm of the Night”."),
    ("D. W. Griffith", "1875–1948", "United States",
     "The pioneer of the close-up and cross-cutting whose Civil War epic glorified the Ku Klux Klan.",
     "<u><i>The Birth of a Nation</i></u>; <i>Intolerance</i>; <i>Broken Blossoms</i>; <i>Way Down East</i>",
     "He co-founded United Artists with Chaplin, Mary Pickford, and Douglas Fairbanks; Lillian Gish starred in many of his films."),
    ("Frank Capra", "1897–1991", "United States",
     "The Sicilian-born director of populist fables, from a naive senator's filibuster to a small-town banker saved by an angel.",
     "<i>It Happened One Night</i>; <i>Mr. Deeds Goes to Town</i>; <i>Mr. Smith Goes to Washington</i>; <u><i>It's a Wonderful Life</i></u>",
     "He won Best Director three times in the 1930s, and made the <i>Why We Fight</i> series in the Second World War."),
    ("Hayao Miyazaki", "born 1941", "Japan",
     "The co-founder of Studio Ghibli who directed a girl's year working in a bathhouse for spirits.",
     "<i>My Neighbor Totoro</i>; <i>Princess Mononoke</i>; <u><i>Spirited Away</i></u>; <i>The Boy and the Heron</i>",
     "<i>Spirited Away</i> and <i>The Boy and the Heron</i> both won the Academy Award for Animated Feature."),
    ("Sam Peckinpah", "1925–1984", "United States",
     "The director nicknamed “Bloody Sam” for the slow-motion gunfights of his westerns.",
     "<i>Ride the High Country</i>; <u><i>The Wild Bunch</i></u>; <i>Straw Dogs</i>; <i>Pat Garrett and Billy the Kid</i>",
     "<i>The Wild Bunch</i> ends in a massacre in a Mexican town; Bob Dylan wrote “Knockin' on Heaven's Door” for <i>Pat Garrett</i>."),
    ("Douglas Sirk", "1897–1987", "Germany",
     "The German émigré whose lush Universal melodramas, often with Rock Hudson, were later read as critiques of American life.",
     "<i>Magnificent Obsession</i>; <u><i>All That Heaven Allows</i></u>; <i>Written on the Wind</i>; <i>Imitation of Life</i>",
     "Born Hans Detlef Sierck; Fassbinder (<i>Ali: Fear Eats the Soul</i>) and Todd Haynes (<i>Far from Heaven</i>) reworked <i>All That Heaven Allows</i>."),
    ("Spike Lee", "born 1957", "United States",
     "The Brooklyn director who played Mookie, the pizza delivery man who throws a trash can through Sal's window.",
     "<i>She's Gotta Have It</i>; <u><i>Do the Right Thing</i></u>; <i>Malcolm X</i>; <i>BlacKkKlansman</i>",
     "His company is 40 Acres and a Mule Filmworks; he won the adapted-screenplay Academy Award for <i>BlacKkKlansman</i>."),
    ("Lars von Trier", "born 1956", "Denmark",
     "The Danish co-founder of the Dogme 95 movement, whose <i>Breaking the Waves</i> made Emily Watson a star.",
     "<u><i>Breaking the Waves</i></u>; <i>Dancer in the Dark</i>; <i>Dogville</i>; <i>Melancholia</i>",
     "<i>Dancer in the Dark</i>, with Björk, won the 2000 Palme d'Or; Cannes declared him persona non grata in 2011."),
    ("Miloš Forman", "1932–2018", "Czechoslovakia",
     "The Czech New Wave director who emigrated and won Best Director for Ken Kesey's novel of a mental hospital.",
     "<i>The Firemen's Ball</i>; <u><i>One Flew Over the Cuckoo's Nest</i></u>; <i>Hair</i>; <i>Amadeus</i>",
     "Both <i>One Flew Over the Cuckoo's Nest</i> and <i>Amadeus</i> won Best Picture and Best Director."),
    ("Jane Campion", "born 1954", "New Zealand",
     "The New Zealand director of a mute Scottish pianist who arrives in the colony with her daughter.",
     "<i>An Angel at My Table</i>; <u><i>The Piano</i></u>; <i>Bright Star</i>; <i>The Power of the Dog</i>",
     "The first woman to win the Palme d'Or, for <i>The Piano</i> (1993); she won Best Director for <i>The Power of the Dog</i>."),
    ("Preston Sturges", "1898–1959", "United States",
     "The screenwriter who became one of the first to direct his own scripts, satirizing a comedy director who sets out to suffer like the poor.",
     "<i>The Lady Eve</i>; <u><i>Sullivan's Travels</i></u>; <i>The Palm Beach Story</i>; <i>The Miracle of Morgan's Creek</i>",
     "He won the first Academy Award for Original Screenplay, for <i>The Great McGinty</i> (1940)."),
    ("Elia Kazan", "1909–2003", "United States",
     "The director who named names to the House Un-American Activities Committee, then made a film about a dockworker who informs.",
     "<i>A Streetcar Named Desire</i>; <u><i>On the Waterfront</i></u>; <i>East of Eden</i>; <i>A Face in the Crowd</i>",
     "He co-founded the Actors Studio; his 1999 honorary Academy Award drew protests inside and outside the hall."),
    ("Jean-Pierre Melville", "1917–1973", "France",
     "The French director of laconic gangster films whose hitman keeps a caged bullfinch in <i>Le Samouraï</i>.",
     "<i>Bob le flambeur</i>; <u><i>Le Samouraï</i></u>; <i>Army of Shadows</i>; <i>Le Cercle Rouge</i>",
     "Born Jean-Pierre Grumbach, he took his name from the author of <i>Moby-Dick</i>; the New Wave treated him as a model."),
    ("Pedro Almodóvar", "born 1949", "Spain",
     "The Spanish director who came out of Madrid's post-Franco Movida, with melodramas in saturated colour.",
     "<u><i>Women on the Verge of a Nervous Breakdown</i></u>; <i>All About My Mother</i>; <i>Talk to Her</i>; <i>Volver</i>",
     "<i>All About My Mother</i> won the foreign-language Academy Award and <i>Talk to Her</i> the original-screenplay award; Penélope Cruz and Antonio Banderas are frequent stars."),
    ("Brian De Palma", "born 1940", "United States",
     "The New Hollywood director of split screens and Hitchcock homages, from a telekinetic prom queen to Tony Montana.",
     "<i>Carrie</i>; <i>Dressed to Kill</i>; <u><i>Scarface</i></u>; <i>The Untouchables</i>",
     "<i>The Untouchables</i> restages the Odessa Steps sequence of <i>Battleship Potemkin</i> with a baby carriage in Union Station."),
    ("Sidney Lumet", "1924–2011", "United States",
     "The director of a jury room in which one holdout talks eleven others out of a guilty verdict.",
     "<u><i>12 Angry Men</i></u>; <i>Serpico</i>; <i>Dog Day Afternoon</i>; <i>Network</i>",
     "<i>Network</i> gave Peter Finch “I'm as mad as hell, and I'm not going to take this anymore!”; he received an honorary Academy Award in 2005."),
    ("John Carpenter", "born 1948", "United States",
     "The director, who composes his own scores, of a masked killer stalking babysitters in Haddonfield, Illinois.",
     "<i>Assault on Precinct 13</i>; <u><i>Halloween</i></u>; <i>The Thing</i>; <i>They Live</i>",
     "<i>The Thing</i>, his remake of a 1951 film, flopped on release and became a classic."),
    ("Ousmane Sembène", "1923–2007", "Senegal",
     "The Senegalese novelist and director called the father of African cinema.",
     "<u><i>Black Girl</i></u>; <i>Mandabi</i>; <i>Xala</i>; <i>Moolaadé</i>",
     "<i>Black Girl</i> (1966), about a Senegalese maid in France, is often called the first sub-Saharan African feature; he had worked as a docker in Marseille."),
    ("George Lucas", "born 1944", "United States",
     "The director of <i>American Graffiti</i>, who founded Industrial Light & Magic to make his space opera.",
     "<i>THX 1138</i>; <i>American Graffiti</i>; <u><i>Star Wars</i></u>",
     "Joseph Campbell's <i>The Hero with a Thousand Faces</i> shaped <i>Star Wars</i>; he sold Lucasfilm to Disney in 2012."),
    ("Jean Cocteau", "1889–1963", "France",
     "The French poet and artist who directed Jean Marais as the Beast and as a poet led through a mirror into the underworld.",
     "<i>The Blood of a Poet</i>; <u><i>Beauty and the Beast</i></u>; <i>Orpheus</i>; <i>Testament of Orpheus</i>",
     "He wrote <i>Les Enfants Terribles</i> and the scenario for the ballet <i>Parade</i>."),
    ("Mike Nichols", "1931–2014", "United States",
     "The improv comedian, partner of Elaine May, who directed Dustin Hoffman's affair with Mrs. Robinson.",
     "<i>Who's Afraid of Virginia Woolf?</i>; <u><i>The Graduate</i></u>; <i>Carnal Knowledge</i>; <i>Working Girl</i>",
     "One of the few to win an Emmy, a Grammy, an Oscar, and a Tony; the Oscar was Best Director for <i>The Graduate</i>."),
    ("Ang Lee", "born 1954", "Taiwan",
     "The Taiwanese director of swordfights on bamboo treetops and of two cowboys' secret love.",
     "<i>Sense and Sensibility</i>; <u><i>Crouching Tiger, Hidden Dragon</i></u>; <i>Brokeback Mountain</i>; <i>Life of Pi</i>",
     "He won Best Director twice, for <i>Brokeback Mountain</i> and <i>Life of Pi</i>."),
    ("Wes Anderson", "born 1969", "United States",
     "The director of symmetrical pastel tableaux, from a family of fallen prodigies to a concierge at a mountain hotel.",
     "<i>Rushmore</i>; <i>The Royal Tenenbaums</i>; <i>Fantastic Mr. Fox</i>; <u><i>The Grand Budapest Hotel</i></u>",
     "Bill Murray appears in nearly all his films; his first Academy Award was for the short <i>The Wonderful Story of Henry Sugar</i>."),
    ("Maya Deren", "1917–1961", "United States",
     "The avant-garde filmmaker who, with her husband Alexander Hammid, made a dream film of keys, knives, and a hooded figure with a mirror for a face.",
     "<u><i>Meshes of the Afternoon</i></u>; <i>At Land</i>; <i>Ritual in Transfigured Time</i>",
     "Born in Kyiv; she studied Vodou in Haiti for <i>Divine Horsemen</i>."),
    ("Louis Malle", "1932–1995", "France",
     "The French director whose <i>Au revoir les enfants</i> recalls a Jewish boy hidden at his Catholic boarding school.",
     "<i>Elevator to the Gallows</i>; <i>The Lovers</i>; <u><i>Au revoir les enfants</i></u>; <i>My Dinner with Andre</i>",
     "Miles Davis improvised the score of <i>Elevator to the Gallows</i>; he married Candice Bergen."),
    ("Kelly Reichardt", "born 1964", "United States",
     "The American independent director of the Oregon frontier, from a lost wagon train to two men stealing milk for oily cakes.",
     "<i>Old Joy</i>; <i>Wendy and Lucy</i>; <i>Meek's Cutoff</i>; <u><i>First Cow</i></u>",
     "Jon Raymond co-writes most of her films; Michelle Williams has starred in four of them."),
    ("Sofia Coppola", "born 1971", "United States",
     "The director who paired Bill Murray and Scarlett Johansson in a Tokyo hotel.",
     "<i>The Virgin Suicides</i>; <u><i>Lost in Translation</i></u>; <i>Marie Antoinette</i>; <i>The Beguiled</i>",
     "Francis Ford Coppola's daughter, she played the baby in the christening scene of <i>The Godfather</i>; she won the original-screenplay Academy Award for <i>Lost in Translation</i>."),
    ("Derek Jarman", "1942–1994", "United Kingdom",
     "The English director whose last film is a single blue screen with voices, made as he went blind with AIDS.",
     "<i>Sebastiane</i>; <i>Jubilee</i>; <u><i>Caravaggio</i></u>; <i>Blue</i>",
     "A painter and set designer too; he made a celebrated garden of shingle and driftwood at Prospect Cottage, Dungeness."),
    ("Guillermo del Toro", "born 1964", "Mexico",
     "The Mexican director of a girl who meets a faun in the woods in Franco's Spain.",
     "<i>The Devil's Backbone</i>; <u><i>Pan's Labyrinth</i></u>; <i>The Shape of Water</i>; <i>Pinocchio</i>",
     "<i>The Shape of Water</i> won Best Picture and Best Director; his <i>Pinocchio</i> won the animated-feature Academy Award."),
]


def tier(strict, alls):   # the History rule, as for the actors and the 2026-09-29 Film additions
    if strict >= 5 or (strict >= 3 and alls >= 12) or alls >= 40:
        return "tier1-core"
    if strict >= 1 or alls >= 8:
        return "tier2-solid"
    return "tier3-deepcut" if alls >= 3 else "tier4-rare"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", C.fold(s).lower()).strip("-")


def find():
    import film_stills as S
    os.makedirs(WORK, exist_ok=True)
    tiles = []
    for i, d in enumerate(D):
        name = d[0]
        r = S.tmdb("/search/person", query=name)["results"]
        r = [x for x in r if x.get("known_for_department") == "Directing"] or r
        if not r:
            print("no TMDB match:", name)
            continue
        profs = sorted(S.tmdb("/person/%d/images" % r[0]["id"])["profiles"], key=lambda p: -(p.get("vote_count") or 0))
        for k, p in enumerate(profs[:3]):
            local = os.path.join(WORK, "%d_%d.jpg" % (i, k))
            if not os.path.exists(local):
                open(local, "wb").write(urllib.request.urlopen("https://image.tmdb.org/t/p/w500" + p["file_path"], timeout=60).read())
            tiles.append(("%d.%d %s" % (i, k, name), local))
        if not profs:
            print("no portrait:", name)
    sys.path.insert(0, SP)
    import wm
    for s in range(0, len(tiles), 36):
        wm.sheet(tiles[s:s + 36], os.path.join(WORK, "sheet_%02d.jpg" % (s // 36)), cols=9, W=170)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:2] == ["find"]:
        find()
        sys.exit()
    ev = json.load(open(EVID, encoding="utf-8"))
    picks = json.load(open(PICKS, encoding="utf-8"))
    have = {C.fold(C.plain(n["fields"]["Title"]["value"])).lower()
            for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Film" Kind:Director'))}
    key = {"D. W. Griffith": "D.W. Griffith"}
    todo = []
    from collections import Counter
    for i, (name, years, country, clue, works, notes) in enumerate(D):
        if C.fold(name).lower() in have:
            continue
        e = ev[key.get(name, name)]
        t = tier(e["strict"], e["all"])
        f = {"Title": name, "Year": years, "Country": country, "Clue": clue, "Works": works, "Notes": notes, "Kind": "Director"}
        fn, path = None, None
        if str(i) in picks:
            fn = "filmdir-%s-1001.jpg" % slug(name)
            path = os.path.join(WORK, "%d_%d.jpg" % (i, picks[str(i)]))
            f["Picture"] = '<img src="%s">' % fn
        todo.append((f, fn, path, t))
    print(len(todo), "directors;", Counter(t for *_, t in todo))
    for f, fn, path, t in todo:
        print("  %-26s %s %s" % (f["Title"], t, "" if fn else "(no portrait)"))
    if "--apply" in sys.argv:
        for f, fn, path, t in todo:
            if fn:
                C.anki("storeMediaFile", filename=fn, path=path)
            nid = C.anki("addNote", note={"deckName": "Film", "modelName": "Film", "fields": f,
                                          "tags": ["Film::director", "Film::directors_1001", "Film::tier::" + t],
                                          "options": {"allowDuplicate": False}})
            if t != "tier1-core":
                C.anki("suspend", cards=C.anki("findCards", query="nid:%d" % nid))
        print("added", len(todo))
