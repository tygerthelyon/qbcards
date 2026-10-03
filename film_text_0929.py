# -*- coding: utf-8 -*-
"""film_text_0929.py -- Film's clues, details, and movements rewritten, note by note.

Carter, 2026-09-28, on Film, Performing Arts, and Photography: "poorly written, poorly designed,
horrifically inconsistent and error-filled"; and on card design generally, "flashcards are supposed to
be FLASH cards." The main decks' description cards carry one short clue (Art: "Thirty-two canvases in a
grid, each showing a single tin ..."; Music: "Gives the harpsichord an enormous unaccompanied
cadenza ..."). Film's CLUE to TITLE fronts averaged 47 words, stacked three or four clues, and 247 of
250 named their own director. Each is now the one clue a question is likeliest to use, with no
director and no words from the title. The best second clue, where there is one, moves into Detail.

Movement had become a mix of movements, genres, and vague labels ("Art cinema" on 28 films, "Drama",
"Silent"). It now holds the movement or school a film belongs to, or else its specific genre or
tradition (Jidaigeki, Shomin-geki, Classic Hollywood, Disney animation), in one vocabulary.

House style throughout: Canadian spelling, the Oxford comma, italics for titles and foreign terms,
curly quotes, em dashes, and "Dr." and "St." with a period.

    T = {note id: {field: new value}}     (applied by film_apply_0929.py)
"""

T = {
 1790240557767: {  # A Trip to the Moon
  "Clue": "A capsule fired from a giant cannon lands in the eye of a man's face in the sky.",
  "Notes": "The work of a stage magician turned filmmaker, shot in his glass studio at Montreuil; a hand-coloured print found in Barcelona in 1993 was restored in 2011.",
  "Movement": "Early cinema"},
 1790240557790: {  # Intolerance
  "Clue": "Four stories, from the fall of Babylon to a modern strike, are intercut and linked by a woman rocking a cradle.",
  "Notes": "Partly Griffith's answer to the outcry over <i>The Birth of a Nation</i>; it lost so much money that its Babylon set stood decaying beside Sunset Boulevard for years.",
  "Movement": "Silent epic"},
 1790240557822: {  # The Cabinet of Dr. Caligari
  "Clue": "A fairground showman exhibits a sleepwalker named Cesare and sends him out at night to murder."},
 1790240557865: {  # Battleship Potemkin
  "Clue": "Sailors mutiny over maggot-ridden meat, and the citizens who cheer them are cut down by troops on a long flight of steps.",
  "Notes": "The Odessa Steps massacre never happened, but the sequence is the standard demonstration of Eisenstein's theory of montage."},
 1790240557898: {  # Sunrise
  "Clue": "A farmer is talked by a woman from the city into drowning his wife, cannot go through with it, and falls in love with her again.",
  "Notes": "F. W. Murnau's first American film; it won the only Academy Award ever given for Unique and Artistic Production, at the first ceremony.",
  "Movement": "German Expressionism"},
 1790240557932: {  # Metropolis
  "Clue": "An inventor builds a robot double of the saintly Maria to incite the workers who toil beneath a city of the future.",
  "Notes": "Written by Thea von Harbou, it ends on the moral that the heart must mediate between the head and the hands; a nearly complete print was found in Buenos Aires in 2008."},
 1790240557964: {  # The Passion of Joan of Arc
  "Clue": "A trial and a burning are compressed into a single day, shot almost entirely in huge close-ups of faces against bare white walls.",
  "Notes": "Renée Falconetti's only film role; the original negative burned, and a complete print turned up in 1981 in a closet of a Norwegian mental hospital.",
  "Movement": "Silent era"},
 1790240557998: {  # The Blue Angel
  "Clue": "A respectable schoolmaster is ruined by his infatuation with a cabaret singer, and ends as a clown crowing like a rooster.",
  "Notes": "It made Marlene Dietrich a star with “Falling in Love Again”; it was shot twice, in German and in English."},
 1790240558029: {  # People on Sunday
  "Clue": "Four young Berliners with no acting experience spend their day off at the Wannsee lakes, and almost nothing happens.",
  "Notes": "Billy Wilder wrote it and Fred Zinnemann assisted on camera; nearly everyone involved had fled Germany within three years."},
 1790240558059: {  # City Lights
  "Clue": "The Tramp is mistaken for a millionaire by a blind flower girl, and pays for the operation that restores her sight.",
  "Notes": "Released without dialogue four years into the sound era; Chaplin shot the first meeting 342 times, and the closing close-up is often called the greatest in cinema."},
 1790240558098: {  # M
  "Clue": "A child murderer who whistles “In the Hall of the Mountain King” is hunted down and tried by the city's own criminals.",
  "Notes": "Peter Lorre's first major role, and Lang's first sound film; a beggar marks the killer with a chalk letter pressed onto his shoulder."},
 1790240558148: {  # Duck Soup
  "Clue": "Rufus T. Firefly becomes the leader of Freedonia and blunders into war with neighbouring Sylvania.",
  "Notes": "The Marx Brothers' last film for Paramount, and a flop; it contains the mirror scene, in which two men in identical nightshirts mimic each other.",
  "Movement": "Comedy"},
 1790240558182: {  # King Kong
  "Clue": "A giant ape is taken from Skull Island to New York, where he breaks his chains and climbs the Empire State Building.",
  "Notes": "Willis O'Brien animated him in stop motion; the closing line blames beauty for killing the beast.",
  "Movement": "Monster film"},
 1790240558214: {  # Zero for Conduct
  "Clue": "Boys at a repressive boarding school stage a revolt after a slow-motion pillow fight fills their dormitory with feathers.",
  "Notes": "Jean Vigo made it at 28, and France banned it until 1945; it was the direct model for Lindsay Anderson's <i>If....</i>"},
 1790240558253: {  # The Bride of Frankenstein
  "Clue": "Dr. Pretorius, who keeps homunculi in jars, forces his old colleague to build the monster a mate, who hisses at him.",
  "Notes": "Elsa Lanchester plays both the mate and Mary Shelley in the prologue; it is widely thought better than the 1931 original."},
 1790240558281: {  # Snow White and the Seven Dwarfs
  "Clue": "Disney's first feature film, known around Hollywood during production as “Disney's Folly.”",
  "Notes": "The first full-length cel-animated feature in English; its honorary Oscar was one full-size statuette and seven miniature ones.",
  "Movement": "Disney animation"},
 1790240558316: {  # The Wizard of Oz
  "Clue": "A Kansas farm girl is carried by a cyclone into a Technicolor land, where she follows a yellow brick road.",
  "Notes": "Victor Fleming took over from Richard Thorpe and George Cukor; “Over the Rainbow” was nearly cut, and the slippers were silver in L. Frank Baum's book.",
  "Movement": "MGM musical"},
 1790240558336: {  # The Rules of the Game
  "Clue": "A weekend shooting party at a country château tangles servants and aristocrats in the same adulteries, around a rabbit hunt filmed as a massacre.",
  "Notes": "Jean Renoir plays Octave, who says that everyone has their reasons; booed and cut in 1939, it was reconstructed in 1959 and now tops critics' polls."},
 1790240558368: {  # Gone with the Wind
  "Clue": "A plantation owner's daughter swears, clutching a radish in the ruins of Tara, that she will never be hungry again.",
  "Notes": "Hattie McDaniel became the first Black performer to win an Academy Award; adjusted for inflation, it is still the highest-grossing film ever made.",
  "Movement": "Classic Hollywood"},
 1790240558398: {  # His Girl Friday
  "Clue": "A newspaper editor schemes to keep his ex-wife, his star reporter, from remarrying by handing her one last story on the eve of an execution.",
  "Notes": "An adaptation of <i>The Front Page</i> with the reporter Hildy Johnson rewritten as a woman; the dialogue overlaps so fast that extra lines were written to be talked over."},
 1790240558430: {  # Citizen Kane
  "Clue": "A reporter tries to learn what a dying newspaper tycoon meant by his last word, “Rosebud.”",
  "Notes": "Gregg Toland shot it in deep focus for a 25-year-old first-time director; William Randolph Hearst tried to have the negative destroyed."},
 1790240558462: {  # Casablanca
  "Clue": "A cynical American nightclub owner in Vichy Morocco gives up two letters of transit to a Czech resistance leader and the woman they both love.",
  "Notes": "The script was still being written during shooting, and the last line about a beautiful friendship was dubbed in afterwards; “Play it again, Sam” is never said."},
 1790240558502: {  # To Be or Not to Be
  "Clue": "A Warsaw theatre troupe uses its costumes and its ham acting to outwit the Gestapo.",
  "Notes": "Carole Lombard was killed in a plane crash before its release, and in 1942 it was attacked for joking about the occupation."},
 1790240558559: {  # Ossessione
  "Clue": "A drifter and a roadhouse owner's wife murder her husband in the Po valley, in an unlicensed version of <i>The Postman Always Rings Twice</i>.",
  "Notes": "Luchino Visconti's first feature, usually counted the first Neorealist film; the rights problem kept it unseen in the United States until 1976."},
 1790240558615: {  # Laura
  "Clue": "A detective investigating a woman's murder falls in love with her portrait, and then she walks through the door alive.",
  "Notes": "David Raksin's theme became a standard; Clifton Webb's columnist Waldo Lydecker was modelled on Alexander Woollcott."},
 1790240558648: {  # Children of Paradise
  "Clue": "A mime, an actor, a criminal, and an aristocrat love the same woman along the Boulevard du Crime in 1830s Paris.",
  "Notes": "Shot in occupied France while its Jewish designer, Alexandre Trauner, and composer, Joseph Kosma, worked in hiding; often voted the greatest French film."},
 1790240558679: {  # Beauty and the Beast (1946)
  "Clue": "Living arms hold candelabra along the corridors of an enchanted castle, where stone faces follow the heroine with their eyes.",
  "Notes": "An opening title asks the audience for a child's simple faith; Jean Marais plays three roles.",
  "Movement": "Fantasy"},
 1790240558716: {  # A Matter of Life and Death
  "Clue": "An RAF pilot who bails out without a parachute survives through a clerical error in the afterlife, and must argue his case before a celestial court.",
  "Notes": "Earth is in Technicolor and the other world in monochrome; the Foreign Office asked for it, to improve Anglo-American relations."},
 1790240558749: {  # It's a Wonderful Life
  "Clue": "An apprentice angel shows a despairing building-and-loan manager what Bedford Falls would have become without him.",
  "Notes": "It flopped on release and became a Christmas fixture only after its copyright lapsed in 1974, letting television run it free."},
 1790240558780: {  # Bicycle Thieves
  "Clue": "A bill-poster has the means of transport his new job depends on stolen on his first morning, and searches Rome for it with his small son.",
  "Notes": "Vittorio De Sica cast non-professionals throughout, the lead a factory worker; it won an honorary Oscar before the foreign-language category existed."},
 1790240558806: {  # Kind Hearts and Coronets
  "Clue": "A draper's assistant murders his way through eight relatives, all played by Alec Guinness, to inherit a dukedom.",
  "Notes": "He narrates from the condemned cell; American censors demanded an added ending in which his memoirs are found."},
 1790240558840: {  # The Third Man
  "Clue": "A pulp novelist in occupied Vienna learns that his supposedly dead friend is alive and selling diluted penicillin.",
  "Notes": "Graham Greene wrote it and Anton Karas's zither scores it; Orson Welles added the speech about Switzerland and the cuckoo clock himself."},
 1790240558869: {  # Rashomon
  "Clue": "A bandit, a samurai's wife, the dead samurai speaking through a medium, and a woodcutter give incompatible accounts of the same killing.",
  "Movement": "<i>Jidaigeki</i>"},
 1790240558899: {  # Sunset Boulevard
  "Clue": "A screenwriter narrates his story while floating dead in the swimming pool of a forgotten silent star who is ready for her close-up.",
  "Notes": "Gloria Swanson really was a silent star, and Erich von Stroheim, who plays her butler, really had directed her."},
 1790240558933: {  # A Streetcar Named Desire
  "Clue": "A fading Southern belle moves in with her sister and her brutish brother-in-law in New Orleans, and is destroyed.",
  "Notes": "Elia Kazan had directed the play on Broadway; it was Marlon Brando's film breakthrough, and the Production Code cuts were restored only in 1993."},
 1790240558964: {  # The Night of the Hunter
  "Clue": "A murderous preacher with LOVE and HATE tattooed on his knuckles pursues two children down the Ohio River.",
  "Notes": "The only film the actor Charles Laughton directed; it failed so completely that he never directed again."},
 1790240558993: {  # Singin' in the Rain
  "Clue": "A studio's changeover to sound is nearly wrecked by its leading lady's voice, so a chorus girl secretly dubs her.",
  "Notes": "Built around Arthur Freed's back catalogue of songs; Debbie Reynolds, not a trained dancer, rehearsed until her feet bled."},
 1790240559057: {  # Tokyo Story
  "Clue": "An elderly couple visit their grown children in the capital, and only their widowed daughter-in-law makes time for them.",
  "Notes": "The camera sits at the height of someone kneeling on a tatami mat and hardly moves; Ozu's “pillow shots” of empty rooms punctuate it.",
  "Movement": "<i>Shomin-geki</i>"},
 1790240559114: {  # The Wages of Fear
  "Clue": "Four desperate men stranded in a Latin American oil town are hired to drive two trucks of nitroglycerine over broken roads to a burning well."},
 1790240559150: {  # Godzilla
  "Clue": "A creature woken by hydrogen-bomb testing comes ashore and levels Tokyo, until a scientist uses his oxygen destroyer and dies with its secret.",
  "Notes": "Released months after the Lucky Dragon No. 5 incident, with the monster played by a man in a suit; the American version cut the politics and added Raymond Burr.",
  "Movement": "<i>Kaiju</i>"},
 1790240692259: {  # All That Heaven Allows
  "Clue": "A well-off New England widow falls for her much younger gardener, and her grown children buy her a television set for company.",
  "Notes": "Rainer Werner Fassbinder remade it as <i>Ali: Fear Eats the Soul</i> and Todd Haynes reworked it as <i>Far from Heaven</i>; the studio-imposed happy ending is deliberately hollow."},
 1790240692323: {  # Rebel Without a Cause
  "Clue": "A new boy in town is goaded into a “chickie run” of stolen cars toward a cliff edge, and the night ends at the Griffith Observatory.",
  "Notes": "James Dean died in a car crash a month before its release; Sal Mineo's Plato is often read as the first gay teenager in American film."},
 1790240692356: {  # Pather Panchali
  "Clue": "A Bengali village boy and his sister run through a field of white <i>kaash</i> flowers to see a train go by.",
  "Notes": "The first part of the Apu Trilogy, shot on weekends over three years with an amateur crew; Ravi Shankar wrote the score in a single night."},
 1790240692387: {  # Kiss Me Deadly
  "Clue": "A thuggish private eye picks up a barefoot woman on a night road, and ends up chasing a glowing box that should never be opened.",
  "Notes": "The glowing box is the ancestor of the briefcase in <i>Pulp Fiction</i>; the apocalyptic ending was cut from prints for decades."},
 1790240692444: {  # The Searchers
  "Clue": "A Confederate veteran spends five years hunting for his niece, taken by Comanches, meaning to kill her for having lived among them.",
  "Notes": "The last shot frames him in a doorway that closes on him; his catchphrase, “That'll be the day,” became a Buddy Holly song."},
 1790240692485: {  # The Seventh Seal
  "Clue": "A knight back from the Crusades plays chess with Death on a stony beach to buy time.",
  "Notes": "It ends with Death leading a dance along a hilltop; Ingmar Bergman took the chess image from a medieval church painting.",
  "Movement": ""},
 1790240692506: {  # Vertigo
  "Clue": "A San Francisco detective with a fear of heights remakes a shopgirl in the image of the dead woman he was hired to follow.",
  "Notes": "Bernard Herrmann scored it, and the dolly zoom is often named after it; a flop in 1958, it displaced <i>Citizen Kane</i> atop the <i>Sight and Sound</i> poll in 2012."},
 1790240692549: {  # Ashes and Diamonds
  "Clue": "On the last day of the war, a young Home Army assassin in dark glasses is ordered to kill a Communist official.",
  "Notes": "Zbigniew Cybulski, called the Polish James Dean, died young like him, under a train in 1967."},
 1790240692610: {  # Some Like It Hot
  "Clue": "Two Chicago musicians witness the St. Valentine's Day Massacre and flee to Florida disguised in an all-female band.",
  "Notes": "The last line is “Nobody's perfect”; it was shot in black and white because the men's makeup looked ghastly in colour."},
 1790240692641: {  # The 400 Blows
  "Clue": "A neglected Paris schoolboy escapes from a reform school, runs to the sea, and turns to the camera in a freeze frame.",
  "Notes": "François Truffaut's first feature, which launched the New Wave at Cannes; Antoine Doinel returned in four more films with the same actor."},
 1790240692673: {  # La Dolce Vita
  "Clue": "A gossip journalist drifts through seven nights of Roman high life, one of them ending with a starlet wading in the Trevi Fountain.",
  "Notes": "Its photographer Paparazzo gave the world the word “paparazzi”; the Vatican newspaper denounced it.",
  "Movement": ""},
 1790240692695: {  # Breathless
  "Clue": "A petty thief who models himself on Humphrey Bogart shoots a policeman and hides out in Paris with an American girl who sells the <i>Herald Tribune</i>.",
  "Notes": "Shot handheld in four weeks from an outline by François Truffaut; the jump cuts began as a way to shorten an over-long rough cut."},
 1790240692731: {  # Saturday Night and Sunday Morning
  "Clue": "A Nottingham lathe operator drinks his wages and has an affair with a workmate's wife, insisting he won't let the bastards grind him down.",
  "Notes": "From Alan Sillitoe's novel; the first big hit of British kitchen-sink realism, and the film that made Albert Finney a star."},
 1790240692766: {  # Last Year at Marienbad
  "Clue": "In a baroque hotel of mirrors and clipped hedges, a man insists to a woman that they have met before, and she does not remember.",
  "Notes": "Written by Alain Robbe-Grillet; nobody involved agreed on whether the meeting happened, and the matchstick game the guests play is Nim."},
 1790240692787: {  # La Jetée
  "Clue": "Told almost entirely in still photographs, it follows a prisoner sent back in time because of a childhood memory of a woman's face on an airport pier.",
  "Notes": "It has exactly one moving shot, of a woman blinking; Terry Gilliam's <i>12 Monkeys</i> is built on it."},
 1790240692819: {  # The Umbrellas of Cherbourg
  "Clue": "Every line is sung as a shop girl's lover is conscripted to Algeria, and they meet again years later at a gas station.",
  "Notes": "Michel Legrand's score gave the song “I Will Wait for You”; Catherine Deneuve's singing is dubbed."},
 1790240692862: {  # Black God, White Devil
  "Clue": "A cowhand in the drought-stricken <i>sertão</i> kills his boss and follows first a messianic preacher and then a bandit.",
  "Notes": "Glauber Rocha called the movement's style an “aesthetic of hunger”; the bandit is a <i>cangaceiro</i> in the tradition of Lampião."},
 1790240692914: {  # Dr. Strangelove
  "Clue": "A general obsessed with precious bodily fluids launches a nuclear strike that cannot be recalled, and a major rides the bomb down waving his hat.",
  "Notes": "Peter Sellers plays three roles; a custard-pie fight in the War Room was shot and cut."},
 1790240692947: {  # The Sound of Music
  "Clue": "A postulant from a Salzburg abbey becomes governess to a widowed naval captain's seven children, and leads the family over the mountains after the Anschluss.",
  "Notes": "Robert Wise's Rodgers and Hammerstein adaptation rescued Twentieth Century-Fox after <i>Cleopatra</i>."},
 1790240692981: {  # The Battle of Algiers
  "Clue": "Shot in newsreel style with non-professionals, it reconstructs the FLN's bombing campaign in the Casbah and the French paratroopers' use of torture.",
  "Notes": "An opening title insists no documentary footage was used; it was banned in France for five years, and was screened at the Pentagon in 2003."},
 1790240693014: {  # Chelsea Girls
  "Clue": "Two reels are projected side by side for over three hours as Factory regulars talk, inject, and argue in hotel rooms.",
  "Notes": "The first underground film to play commercial cinemas; the sound switches between the reels at the projectionist's discretion, so no two screenings are alike."},
 1790240693044: {  # Playtime
  "Clue": "A bewildered man in a raincoat and a party of American tourists get lost in a Paris of glass partitions and identical cubicles.",
  "Notes": "Jacques Tati built a steel-and-glass city for it, nicknamed Tativille, and the cost bankrupted him; the gags are spread across a 70mm frame with no close-ups to point at them."},
 1790240693068: {  # Bonnie and Clyde
  "Clue": "Two Depression-era bank robbers rove across Texas and Oklahoma until they are cut down in slow motion at a roadside ambush.",
  "Notes": "Pauline Kael's long defence of it in <i>The New Yorker</i> is a landmark of criticism; its violence helped end the Production Code."},
 1790240693116: {  # 2001: A Space Odyssey
  "Clue": "A black monolith appears to apes at a waterhole, and a bone thrown into the air cuts to a satellite.",
  "Notes": "The soft-voiced computer HAL 9000 kills the crew and is dismantled singing “Daisy Bell”; Arthur C. Clarke co-wrote it."},
 1790240693148: {  # The Wild Bunch
  "Clue": "Aging outlaws in 1913 sell stolen rifles to a Mexican general, then walk four abreast into an unwinnable gunfight to rescue one of their own.",
  "Notes": "Its carnage is cut at several speeds at once; the opening has children feeding scorpions to ants."},
 1790240693184: {  # Easy Rider
  "Clue": "Two bikers hide their cocaine money in a fuel tank and ride from Los Angeles to Mardi Gras in New Orleans.",
  "Notes": "Made for about $400,000, it took some $60 million and convinced the studios to hand films to young directors; Jack Nicholson plays a drunken lawyer."},
 1790240693215: {  # Le Boucher
  "Clue": "A village schoolmistress befriends the local butcher, a veteran of Indochina and Algeria, while a murderer is at large.",
  "Notes": "Blood drips onto a schoolgirl's sandwich at a picnic; Claude Chabrol called it his most Hitchcockian film."},
 1790240693251: {  # The Godfather
  "Clue": "A Hollywood producer who refuses a favour wakes to find a severed horse's head in his bed.",
  "Notes": "Paramount wanted neither Marlon Brando nor Al Pacino nor the period setting; it became the highest-grossing film to that point."},
 1790240693282: {  # Aguirre, the Wrath of God
  "Clue": "A Spanish expedition searching the Amazon for El Dorado disintegrates under a mutinous lieutenant who declares himself emperor.",
  "Notes": "It ends circling a raft of corpses overrun by monkeys; Werner Herzog and Klaus Kinski threatened to kill each other during the shoot."},
 1790240693312: {  # The Discreet Charm of the Bourgeoisie
  "Clue": "Six well-bred friends try again and again to sit down to dinner, and are interrupted every time.",
  "Notes": "Between attempts they walk down an empty country road; it won Luis Buñuel the Oscar for Best Foreign Language Film."},
 1790240693346: {  # Don't Look Now
  "Clue": "A couple whose daughter drowned in a red coat keep glimpsing a small figure in red in wintry Venice."},
 1790240693378: {  # Chinatown
  "Clue": "A Los Angeles detective's fake adultery case leads him to a plot to divert the city's water, and to a far worse family secret.",
  "Notes": "Robert Towne wrote it and wanted a happier ending, but Roman Polanski overruled him; the water plot is loosely based on the Owens Valley aqueduct."},
 1790240693417: {  # Ali: Fear Eats the Soul
  "Clue": "A widowed Munich cleaning woman in her sixties marries a much younger Moroccan guest worker, and everyone around them punishes them for it.",
  "Notes": "A deliberate reworking of Douglas Sirk's <i>All That Heaven Allows</i>; Fassbinder shot it in about two weeks."},
 1790240705023: {  # The Spirit of the Beehive
  "Clue": "In a Castilian village in 1940, a small girl who has seen <i>Frankenstein</i> at a travelling cinema looks for the monster in an abandoned sheepfold, and finds a wounded fugitive.",
  "Movement": ""},
 1790240871057: {  # Jaws
  "Clue": "A resort island's police chief, a marine biologist, and an old fisherman who survived the USS <i>Indianapolis</i> go to sea after a great white shark.",
  "Notes": "The mechanical shark kept breaking down, so John Williams's two notes stand in for it; the first film to take $100 million, it created the summer blockbuster."},
 1790240871091: {  # Picnic at Hanging Rock
  "Clue": "On St. Valentine's Day 1900, three schoolgirls and a teacher vanish on a volcanic outcrop in Victoria, and nothing is explained.",
  "Notes": "The novel's final chapter, which offered an explanation, was published only after the author's death; many viewers still believe the story is true."},
 1790240871124: {  # Taxi Driver
  "Clue": "An insomniac Vietnam veteran who drives nights in New York shaves his head into a mohawk and shoots his way into a brothel to rescue a twelve-year-old.",
  "Notes": "Bernard Herrmann's last score; “You talkin' to me?” was improvised, and John Hinckley Jr. cited the film after shooting Ronald Reagan."},
 1790240871146: {  # Annie Hall
  "Clue": "A neurotic New York comedian looks back on his failed romance with a singer from Chippewa Falls, and pulls Marshall McLuhan from behind a cinema poster to win an argument.",
  "Movement": "Romantic comedy"},
 1790240871187: {  # Star Wars
  "Clue": "A farm boy on a desert planet finds a message hidden in a droid, and flies a trench run to destroy a moon-sized battle station.",
  "Notes": "Rescued in the edit by a team including Marcia Lucas, George Lucas's then wife; the merchandising rights the studio let him keep made him a fortune.",
  "Original title": "Star Wars: Episode IV – A New Hope"},
 1790240871245: {  # Alien
  "Clue": "Something attaches itself to a crewman's face on a distant moon, and later bursts out of his chest at dinner.",
  "Notes": "H. R. Giger designed the creature, and the tagline promised that in space no one can hear you scream; Ripley was written without a specified gender."},
 1790240871276: {  # Stalker
  "Clue": "A guide leads a writer and a scientist through a forbidden, guarded zone toward a room said to grant a person's deepest wish.",
  "Notes": "Sepia outside the zone and colour within; the first version was ruined in the lab and reshot from scratch.",
  "Movement": ""},
 1790240871308: {  # Das Boot
  "Clue": "A U-boat crew endures depth charges, survives being pinned on the sea floor below crush depth, and is destroyed in an air raid within sight of home.",
  "Notes": "Shot in a full-size hull on gimbals with the camera racing its length; the actors were kept out of daylight so they would look pale."},
 1790240871336: {  # Blade Runner
  "Clue": "In a rainy, neon Los Angeles of 2019, a burnt-out policeman hunts four escaped artificial humans with four-year lifespans.",
  "Notes": "Rutger Hauer largely wrote the tears-in-rain speech himself; Vangelis scored it, and later cuts dropped the studio's voiceover and happy ending."},
 1790240871373: {  # Blue Velvet
  "Clue": "A college student home in a picture-book American town finds a severed ear in a field.",
  "Notes": "Dennis Hopper plays a gas-huffing psychopath; Roger Ebert loathed the film and Pauline Kael championed it."},
 1790240871403: {  # Wings of Desire
  "Clue": "Angels in overcoats listen to the thoughts of Berliners, until one falls in love with a trapeze artist and chooses to become mortal.",
  "Notes": "The angels see in black and white; Peter Falk plays himself, a former angel, and Peter Handke wrote much of the text."},
 1790240871441: {  # Women on the Verge of a Nervous Breakdown
  "Clue": "A dubbing actress abandoned by her lover spikes a batch of gazpacho with sleeping pills while her flat fills with his son, his fiancée, and his mad ex-wife.",
  "Notes": "It made Pedro Almodóvar an international name and was nominated for the foreign-language Oscar; Antonio Banderas plays the son.",
  "Movement": "<i>La Movida</i>"},
 1790240871479: {  # Sex, Lies, and Videotape
  "Clue": "An impotent drifter who videotapes women talking about sex unsettles a Baton Rouge lawyer, his wife, and her sister.",
  "Notes": "Steven Soderbergh wrote it in eight days at 26; its Palme d'Or and box office started the independent boom of the 1990s and made Miramax."},
 1790240871510: {  # Do the Right Thing
  "Clue": "On the hottest day of the year in Bedford-Stuyvesant, a quarrel over whose photographs hang on a pizzeria wall ends in a riot.",
  "Notes": "Radio Raheem is killed in a police chokehold; it closes with quotations from Martin Luther King Jr. and Malcolm X."},
 1790240871543: {  # Pulp Fiction
  "Clue": "A hitman who quotes Ezekiel, a boxer who won't throw a fight, and a glowing briefcase share three stories told out of order.",
  "Notes": "Its Palme d'Or, and $200 million taken on an $8 million budget, reshaped American cinema in the 1990s and rebuilt John Travolta's career."},
 1790240871572: {  # Three Colours: Red
  "Clue": "A Geneva model runs over a dog and finds its owner, a retired judge who eavesdrops on his neighbours' telephone calls.",
  "Notes": "The last film Krzysztof Kieślowski completed; the trilogy follows the French flag and motto, and this one is fraternity.",
  "Movement": ""},
 1790240871609: {  # The Shawshank Redemption
  "Clue": "A banker wrongly convicted of murder spends nineteen years tunnelling out of prison behind a pin-up poster.",
  "Notes": "From a Stephen King novella; a box-office failure, it became through video the top-rated film on IMDb for over a decade."},
 1790240871637: {  # Toy Story
  "Clue": "A pull-string cowboy is displaced as a boy's favourite by a space ranger who does not know he is a toy.",
  "Notes": "The first feature made entirely with computer animation; Randy Newman wrote the songs.",
  "Movement": "Computer animation"},
 1790240871675: {  # La Haine
  "Clue": "Three friends, one Jewish, one Black, and one Arab, spend twenty-four hours in the Paris suburbs after a riot, one of them carrying a policeman's lost revolver.",
  "Notes": "Shot in black and white; its story of a man falling from a building and repeating “So far so good” is the film's own summary of itself."},
 1790240871705: {  # Fargo
  "Clue": "A Minneapolis car salesman has his own wife kidnapped for the ransom, and a heavily pregnant police chief politely works it out.",
  "Notes": "The opening claim that it is a true story is false; Frances McDormand won Best Actress, and there is a wood chipper."},
 1790240871742: {  # The Sweet Hereafter
  "Clue": "A lawyer arrives in a British Columbia town after a school bus crashes through the ice, hoping to organize a lawsuit.",
  "Notes": "From Russell Banks's novel, and structured around “The Pied Piper of Hamelin,” which a surviving girl reads aloud.",
  "Movement": ""},
 1790240871784: {  # Central Station
  "Clue": "A retired schoolteacher who writes letters for the illiterate at Rio's main railway terminus ends up escorting an orphaned boy across the northeast to find his father.",
  "Movement": "<i>Retomada</i>"},
 1790240871808: {  # Festen
  "Clue": "At a patriarch's sixtieth birthday party, his eldest son stands up to make a toast and accuses him of sexual abuse.",
  "Notes": "Dogme 95's certificate number one, made under the “vow of chastity” Thomas Vinterberg and Lars von Trier had signed, and shot on a handheld consumer camcorder."},
 1790240871842: {  # Ring
  "Clue": "A journalist investigates a cursed videotape that kills its viewers seven days after they watch it.",
  "Notes": "A drowned girl climbs out of a television set; it set off the J-horror wave and a Hollywood remake in 2002."},
 1790240871872: {  # Crouching Tiger, Hidden Dragon
  "Clue": "A warrior gives up his Green Destiny sword, a governor's daughter steals it, and they fight across the tops of a bamboo forest.",
  "Notes": "Yuen Woo-ping choreographed the wire work; it took over $200 million worldwide and won the foreign-language Oscar.",
  "Movement": "<i>Wuxia</i>"},
 1790240871903: {  # Spirited Away
  "Clue": "A sulky ten-year-old whose parents have been turned into pigs is put to work in a bathhouse for spirits.",
  "Movement": "Anime"},
 1790240871934: {  # Amélie
  "Clue": "A shy Montmartre waitress finds a boy's box of treasures behind a bathroom tile, and takes to secretly arranging other people's happiness.",
  "Notes": "Its Paris, all saturated green and gold, was criticized at home for being scrubbed of anything unpleasant; a garden gnome is sent travelling.",
  "Movement": "Romantic comedy"},
 1790240871963: {  # Lagaan
  "Clue": "In 1893, a drought-stricken village accepts a British officer's wager: beat his men at cricket and pay no tax for three years.",
  "Notes": "Nearly four hours long, with six songs and a final over that comes down to a no-ball; one of only three Indian films nominated for the foreign-language Oscar."},
 1790240871995: {  # City of God
  "Clue": "A boy with a camera narrates twenty years of a Rio housing project's slide into a drug war, beginning with a chicken running from a knife.",
  "Notes": "Most of the cast were untrained children from the favelas; it was nominated for four Oscars, though not for Best Foreign Language Film.",
  "Movement": "<i>Retomada</i>"},
 1790240872025: {  # Oldboy
  "Clue": "A man is imprisoned in a single room for fifteen years without being told why, and then given five days to find out.",
  "Notes": "He eats a live octopus and fights down a corridor with a hammer in one unbroken shot; the middle film of Park Chan-wook's Vengeance Trilogy."},
 1790240872062: {  # The Lives of Others
  "Clue": "A Stasi captain bugs a playwright's flat in 1984 East Berlin, and quietly begins protecting him instead.",
  "Notes": "Ulrich Mühe had himself been under Stasi surveillance; it won the foreign-language Oscar."},
 1790240872094: {  # Pan's Labyrinth
  "Clue": "In 1944 Spain, a girl whose mother has married a sadistic Falangist captain is told by a faun that she is a lost princess.",
  "Notes": "One of her three tasks brings her to the Pale Man, who has eyes in his palms; it won three Oscars for its craft."},
 1790240872123: {  # Slumdog Millionaire
  "Clue": "A Mumbai tea boy one question from the top prize on a television quiz is arrested for cheating, and each answer turns out to come from his own life.",
  "Notes": "A. R. Rahman scored it; it won eight Oscars, including Best Picture.",
  "Movement": ""},
 1790240872157: {  # The Hurt Locker
  "Clue": "A bomb-disposal sergeant in Iraq who has defused hundreds of devices cannot function at home, and goes back for another tour.",
  "Notes": "Kathryn Bigelow became the first woman to win the directing Oscar, beating her ex-husband James Cameron's <i>Avatar</i> for Best Picture."},
 1790240872197: {  # Man on Wire
  "Clue": "A documentary, structured like a heist film, about the Frenchman who in 1974 walked a cable strung between the World Trade Center towers.",
  "Notes": "It never mentions the towers' destruction; it won the documentary Oscar."},
 1790240872231: {  # The White Ribbon
  "Clue": "In a north German village just before the First World War, a doctor's horse is tripped by a wire, and children are beaten and worse.",
  "Notes": "Michael Haneke has said its children are the generation that would be adults under Nazism; shot in cold black and white, it won the Palme d'Or.",
  "Movement": ""},
 1790240872289: {  # Once Upon a Time in Anatolia
  "Clue": "Policemen, a prosecutor, a doctor, and a confessed killer drive around the steppe all night looking for a body the murderer cannot locate."},
 1790240872326: {  # Gravity
  "Clue": "A medical engineer on her first shuttle mission is left tumbling through orbit after debris destroys her craft.",
  "Notes": "It opens with an unbroken shot of about thirteen minutes, and most of it was shot inside an LED light box; it won seven Oscars, including Best Director."},
 1790240872351: {  # Boyhood
  "Clue": "A Texas boy and the actors around him were filmed a few days a year for twelve years, so that he grows from six to eighteen on screen."},
 1790240887962: {  # Raise the Red Lantern
  "Clue": "A university student becomes the fourth wife of a wealthy 1920s household, where the master's choice of wife for the night is announced outside her courtyard.",
  "Notes": "The master's face is never clearly shown; China banned it while it was nominated for an Oscar."},
 1790240888007: {  # The Lord of the Rings: The Fellowship of the Ring
  "Clue": "Nine companions set out from Rivendell to carry a small gold band toward a volcano, and a wizard falls with a Balrog at the bridge of Khazad-dûm.",
  "Notes": "Peter Jackson shot all three parts at once in New Zealand; the trilogy won 17 Academy Awards in all."},
 1790241046501: {  # The Great Train Robbery
  "Clue": "Bandits hold up a telegraph office and a locomotive's passengers, and in the last shot an outlaw fires straight at the audience.",
  "Notes": "Twelve minutes that helped establish cross-cutting, often called the first Western; exhibitors could show the close-up at either end.",
  "Movement": "Early cinema"},
 1790241046554: {  # Dr. Mabuse the Gambler
  "Clue": "A master of disguise and hypnosis manipulates the stock exchange and the card tables of inflation-era Berlin.",
  "Notes": "Over four hours in two parts; Fritz Lang returned to the character twice, and the Nazis banned the 1933 sequel."},
 1790241046585: {  # The Jazz Singer
  "Clue": "A cantor's son runs away to sing popular music, and returns to sing Kol Nidre in his dying father's place.",
  "Notes": "Mostly silent, with a few sung and spoken sequences on Vitaphone discs, it still ended the silent era; Al Jolson's blackface performance makes it hard to screen now.",
  "Movement": "Early sound film"},
 1790241046617: {  # Nosferatu
  "Clue": "An unlicensed version of <i>Dracula</i> brings a rat-toothed count to Wisborg on a plague ship, and sunlight destroys him.",
  "Notes": "Bram Stoker's widow won a court order to destroy every print; the film survives because copies had already gone abroad."},
 1790241046649: {  # Un Chien Andalou
  "Clue": "A cloud crosses the moon as a razor slices an eye.",
  "Notes": "Luis Buñuel and Salvador Dalí wrote it from their dreams; ants pour from a hole in a hand, and a man drags two pianos laden with dead donkeys."},
 1790241046682: {  # Freaks
  "Clue": "A trapeze artist marries a sideshow performer for his inheritance, and at the wedding banquet his friends chant that she is one of them.",
  "Notes": "Tod Browning cast real sideshow performers; MGM cut a third of it, Britain banned it for thirty years, and it effectively ended his career."},
 1790241046712: {  # The Grapes of Wrath
  "Clue": "An Oklahoma family driven off its land drives a loaded truck to California, and finds wage-cutting and a government camp.",
  "Notes": "Gregg Toland photographed it; Jane Darwell won Best Supporting Actress as Ma Joad, and John Steinbeck thought its ending improved on his."},
 1790241046743: {  # The Maltese Falcon
  "Clue": "A San Francisco private detective whose partner has been shot joins a hunt for a jewelled statuette that turns out to be lead.",
  "Notes": "John Huston's first film as director, and the one that made Humphrey Bogart a leading man; it closes on “the stuff that dreams are made of.”"},
 1790241046784: {  # Sullivan's Travels
  "Clue": "A director of profitable comedies sets out as a hobo to research a serious film, and learns on a chain gang that what prisoners want is a cartoon.",
  "Notes": "The serious film he means to make is <i>O Brother, Where Art Thou?</i>, a title the Coen brothers took for their own film in 2000."},
 1790241046809: {  # Double Indemnity
  "Clue": "An insurance salesman and a client's wife murder her husband and stage it as a fall from a train, to collect twice the payout.",
  "Notes": "Raymond Chandler co-wrote it with Billy Wilder, and they detested each other; the confession is dictated into a Dictaphone."},
 1790241046840: {  # Meshes of the Afternoon
  "Clue": "A woman follows a hooded figure with a mirror for a face into her own house again and again, until she multiplies into three versions of herself.",
  "Notes": "Made for about $250, it is the founding work of the American avant-garde; Teiji Ito's score was added in 1959."},
 1790241046871: {  # Brief Encounter
  "Clue": "A married suburban woman and a married doctor meet by chance in a railway refreshment room, fall in love over a few Thursdays, and part.",
  "Notes": "From a Noël Coward play, set to Rachmaninoff; it was shot partly at Carnforth station in Lancashire, far from the bombing.",
  "Movement": "Romantic drama"},
 1790241046903: {  # Murderers Among Us
  "Clue": "A drink-ruined army surgeon in the rubble of Berlin sets out to shoot his former captain, now prospering by making saucepans from old helmets.",
  "Notes": "The first German film made after the war, shot in the Soviet sector; the original ending, in which the killing happens, was changed.",
  "Movement": "<i>Trümmerfilm</i>"},
 1790241046933: {  # The Red Shoes
  "Clue": "A ballerina torn between an impresario who demands she dance and a composer who wants her to stop ends under a train in Monte Carlo.",
  "Notes": "Its seventeen-minute ballet takes over the film; Moira Shearer was a real ballerina, and Martin Scorsese funded its restoration."},
 1790241046964: {  # All About Eve
  "Clue": "An aging Broadway star takes on an adoring young fan as her assistant, and is systematically replaced by her.",
  "Notes": "The star tells her guests to fasten their seatbelts; its fourteen Oscar nominations were a record, since matched by <i>Titanic</i> and <i>La La Land</i>."},
 1790241047008: {  # Los Olvidados
  "Clue": "Boys in the slums of Mexico City knock a legless beggar off his cart, and one dreams in slow motion of his mother offering him raw meat.",
  "Notes": "Pulled from Mexican cinemas after four days, it won Best Director at Cannes and returned; it is on UNESCO's Memory of the World register.",
  "Movement": "Social realism"},
 1790241047039: {  # The Big Heat
  "Clue": "A police sergeant whose wife is killed by a car bomb meant for him goes after the city's syndicate alone.",
  "Notes": "A gangster's girlfriend has scalding coffee thrown in her face and returns the favour; the scene was cut in several countries."},
 1790241047070: {  # La Strada
  "Clue": "A brutish strongman buys a simple-minded girl from her mother to be his clown on the road, and abandons her when she breaks down.",
  "Notes": "Giulietta Masina, Federico Fellini's wife, plays her to Nino Rota's theme; it won the first competitive Oscar for Best Foreign Language Film."},
 1790241047101: {  # Seven Samurai
  "Clue": "A village pays masterless swordsmen in rice to defend it from bandits at harvest.",
  "Notes": "The final battle is fought in mud and rain, and the survivors are told the farmers have won, not them; remade as <i>The Magnificent Seven</i>.",
  "Movement": "<i>Jidaigeki</i>"},
 1790241047148: {  # Rififi
  "Clue": "Four men break into a Paris jeweller's through the ceiling in a half-hour heist with no dialogue and no music.",
  "Notes": "Jules Dassin, blacklisted out of Hollywood, made it in France and plays the safecracker under a pseudonym; several countries banned it as too instructive."},
 1790241047182: {  # Invasion of the Body Snatchers
  "Clue": "A small-town California doctor finds his patients' relatives being replaced by blank duplicates grown from pods.",
  "Notes": "Read at the time as being about McCarthyism or about Communism, depending on the reader; the studio added a framing story that softens the ending."},
 1790241047214: {  # Elevator to the Gallows
  "Clue": "A man who has murdered his lover's husband is trapped between floors of his office building overnight when the power is switched off.",
  "Notes": "Louis Malle directed it at 25; Miles Davis improvised the score in one night, watching the film on a loop."},
 1790241047248: {  # Touch of Evil
  "Clue": "A car bomb crosses the Mexican border in an unbroken opening crane shot of more than three minutes.",
  "Notes": "Orson Welles plays the corrupt captain who plants evidence; a 1998 restoration followed his 58-page memo protesting the studio's recut."},
 1790241047278: {  # Peeping Tom
  "Clue": "A focus puller kills women with a blade in his tripod leg while filming them watch their own deaths in a mirror.",
  "Notes": "Released weeks before <i>Psycho</i> and savaged as obscene, it wrecked Michael Powell's career until Martin Scorsese led its rehabilitation."},
 1790241047305: {  # Psycho
  "Clue": "A secretary who has stolen $40,000 stops at a motel run by a nervous young man with a taxidermy hobby and a mother.",
  "Notes": "She is killed forty minutes in, to Bernard Herrmann's strings; Hitchcock refused late admission to cinemas to protect the ending."},
 1790241047336: {  # The Innocents
  "Clue": "A governess at a remote country house becomes convinced that her two charges are possessed by the spirits of a dead valet and her predecessor.",
  "Notes": "From Henry James's <i>The Turn of the Screw</i>, with a script partly by Truman Capote; Freddie Francis darkened the edges of the frame."},
 1790241047370: {  # The Manchurian Candidate
  "Clue": "A brainwashed Korean War hero is triggered to kill by the queen of diamonds in a game of solitaire.",
  "Notes": "A garden-club meeting dissolves into a Communist demonstration in Manchuria; Angela Lansbury, who plays his mother, was three years older than Laurence Harvey."},
 1790241047402: {  # West Side Story
  "Clue": "<i>Romeo and Juliet</i> moves to 1950s Manhattan, with the Jets and the Sharks and a fire escape for a balcony.",
  "Notes": "Leonard Bernstein and Stephen Sondheim wrote the songs; it won ten Oscars, and Natalie Wood's singing is dubbed by Marni Nixon."},
 1790241047432: {  # Jules and Jim
  "Clue": "An Austrian and a Frenchman love the same wilful woman before and after the First World War, until she drives off a broken bridge with one of them.",
  "Notes": "From Henri-Pierre Roché's novel; Jeanne Moreau sings “Le Tourbillon,” about a whirlwind."},
 1790241047463: {  # Dry Summer
  "Clue": "A landowner in an Aegean village dams the spring on his land and refuses water to everyone downstream."},
 1790241047504: {  # Jason and the Argonauts
  "Clue": "Ray Harryhausen spent four and a half months animating its fight against seven sword-wielding skeletons.",
  "Notes": "The bronze giant Talos, harpies, and a hydra also appear; Bernard Herrmann wrote the score."},
 1790241047523: {  # Onibaba
  "Clue": "Two women in a sea of tall grass kill stray samurai and sell their armour, until one puts on a demon mask she cannot get off.",
  "Notes": "Kaneto Shindo said the mask was inspired by the keloid scars of atomic-bomb survivors; the grass was planted for the film."},
 1790241047558: {  # I Am Cuba
  "Clue": "A camera descends the side of a hotel into its swimming pool, and later floats out of a window above a funeral procession.",
  "Notes": "Shot on infrared film that turns palms white and skies black; disowned by both countries, it was forgotten until Martin Scorsese and Francis Ford Coppola presented a restoration in 1995.",
  "Movement": ""},
 1790241047587: {  # Persona
  "Clue": "An actress stops speaking in the middle of a performance of <i>Electra</i>, and is sent to a seaside cottage with a talkative nurse.",
  "Notes": "Partway through, the film seems to burn in the projector; later the two women's faces are printed over each other.",
  "Movement": ""},
 1790241047618: {  # The Graduate
  "Clue": "A young man home from college is given one word of advice, “plastics,” and is seduced by a family friend.",
  "Notes": "Simon and Garfunkel's songs score it; Anne Bancroft was only six years older than Dustin Hoffman."},
 1790241047651: {  # Belle de Jour
  "Clue": "A surgeon's wife secretly spends her afternoons working in a Paris brothel.",
  "Notes": "A client's lacquered box is never opened, and Luis Buñuel refused to say what was in it; it won the Golden Lion."},
 1790241047681: {  # Rosemary's Baby
  "Clue": "A young wife in a Gothic Manhattan apartment building is fed chocolate mousse with a chalky undertaste by her elderly neighbours."},
 1790241047715: {  # Salesman
  "Clue": "Four door-to-door Bible salesmen work Catholic neighbourhoods, and one of them, nicknamed the Badger, slowly stops being able to close.",
  "Notes": "Albert and David Maysles and Charlotte Zwerin made it as direct cinema, with no narration and no interviews."},
 1790241047741: {  # Midnight Cowboy
  "Clue": "A Texan dishwasher goes to New York to work as a gigolo, and teams up with a tubercular con man.",
  "Notes": "The only X-rated film to win Best Picture; Dustin Hoffman's “I'm walkin' here!” was reportedly a reaction to a real taxi."},
 1790241047774: {  # Once Upon a Time in the West
  "Clue": "Three gunmen wait at a railway halt for a harmonica player, who kills them instead.",
  "Notes": "Henry Fonda was cast against type as a man who shoots a child; Ennio Morricone's themes were written before shooting and played on set."},
 1790241047809: {  # A Clockwork Orange
  "Clue": "A gang leader who loves Beethoven is conditioned by the state with his eyelids clamped open.",
  "Notes": "From Anthony Burgess's novel; Stanley Kubrick withdrew it from British release in 1973, and it stayed unavailable there until after his death."},
 1790241047838: {  # Harold and Maude
  "Clue": "A rich young man who stages fake suicides and attends strangers' funerals falls in love with a 79-year-old woman.",
  "Notes": "Cat Stevens wrote the songs; a flop on release, it became a repertory fixture.",
  "Movement": "Black comedy"},
 1790241066275: {  # Closely Watched Trains
  "Clue": "A shy apprentice at a sleepy station in occupied Czechoslovakia worries over his impotence, and ends up blowing up a German munitions transport.",
  "Notes": "Jiří Menzel was 28 when it won the foreign-language Oscar in 1968; the Soviet invasion that August ended the Czech New Wave."},
 1790241066338: {  # Kes
  "Clue": "A bullied Barnsley schoolboy takes a young falcon from its nest and trains it.",
  "Notes": "From Barry Hines's novel; distributors thought the Yorkshire accents unintelligible and nearly shelved it."},
 1790241222341: {  # Land of Silence and Darkness
  "Clue": "A woman deaf and blind since adolescence travels Bavaria visiting others like her, signing into their palms.",
  "Notes": "Its opening image of ski jumpers is something Fini Straubinger said she remembered wanting to describe; Werner Herzog has admitted staging some moments."},
 1790241222368: {  # Walkabout
  "Clue": "A girl and her small brother, abandoned in the outback by their father, survive with the help of an Aboriginal boy on his initiation journey.",
  "Notes": "David Gulpilil's first film; Nicolas Roeg directed and shot it from a script of about fourteen pages."},
 1790241222399: {  # The Harder They Come
  "Clue": "A country boy comes to Kingston to cut a record, is cheated by the producer, and becomes an outlaw and folk hero with a hit on the charts.",
  "Notes": "Jimmy Cliff stars; its soundtrack did more than any other record to take reggae international."},
 1790241222433: {  # A Woman Under the Influence
  "Clue": "A construction foreman's wife, whose behaviour embarrasses everyone around her, is committed for six months.",
  "Notes": "John Cassavetes financed it himself; Gena Rowlands, his wife, plays her opposite Peter Falk."},
 1790241222462: {  # Sholay
  "Clue": "A retired policeman whose arms were cut off hires two petty crooks to capture the bandit who massacred his family.",
  "Notes": "The “curry Western” ran for five years at one Bombay cinema; a flop in its first fortnight, it became the highest-grossing Indian film for nineteen years."},
 1790241222496: {  # Xala
  "Clue": "A businessman in newly independent Senegal takes a third wife, and finds himself impotent.",
  "Notes": "To be cured he must let beggars spit on him; Ousmane Sembène, the father of African cinema, turned from novels to film to reach people who could not read.",
  "Movement": ""},
 1790241222528: {  # Eraserhead
  "Clue": "A man with towering hair in an industrial wasteland is left to care for a swaddled, bleating, skinless infant.",
  "Notes": "David Lynch shot it over five years, partly funded by a paper route; a woman in the radiator sings that in heaven everything is fine.",
  "Movement": "Midnight movie"},
 1790241222554: {  # Dawn of the Dead
  "Clue": "Four survivors take a traffic helicopter to a Pennsylvania shopping mall, and seal themselves in among wandering zombies.",
  "Notes": "George A. Romero's satire of consumerism; Tom Savini did the gore effects."},
 1790241222587: {  # Apocalypse Now
  "Clue": "A captain is sent up a river into Cambodia to terminate a renegade colonel's command “with extreme prejudice.”",
  "Notes": "A cavalry officer attacks a village to Wagner so his men can surf; the disastrous shoot is documented in <i>Hearts of Darkness</i>."},
 1790241222623: {  # Days of Heaven
  "Clue": "Migrant harvest workers pass off a couple as brother and sister so the woman can marry a dying Texas wheat farmer.",
  "Notes": "Shot largely at magic hour; Néstor Almendros won the cinematography Oscar, and Terrence Malick did not make another film for twenty years.",
  "Movement": ""},
 1790241222657: {  # Raging Bull
  "Clue": "A Bronx middleweight's jealousy destroys his marriage and his brother along with his career, and he ends reciting a speech from <i>On the Waterfront</i> in a nightclub.",
  "Notes": "Shot in black and white; Robert De Niro gained about sixty pounds for the later scenes, and Thelma Schoonmaker won her first Oscar for the editing."},
 1790241222694: {  # The Shining
  "Clue": "A writer takes a winter caretaking job at an empty Colorado hotel, where his son rides a tricycle down the corridors toward twin girls.",
  "Notes": "Stephen King disliked it; the manuscript turns out to be one sentence typed over and over, and Garrett Brown's early Steadicam follows the tricycle."},
 1790241222726: {  # E.T. the Extra-Terrestrial
  "Clue": "A suburban boy hides a stranded alien among his soft toys, and cycles him past a police roadblock into the sky.",
  "Notes": "John Williams scored it; it was the highest-grossing film in the world for eleven years, and M&amp;M's turned down the product placement that went to Reese's Pieces."},
 1790241222757: {  # Scarface
  "Clue": "A Cuban refugee from the Mariel boatlift rises through Miami's cocaine trade, and dies in his mansion behind a mounted machine gun.",
  "Notes": "Oliver Stone wrote it; mauled by critics in 1983, it later became a touchstone of hip hop."},
 1790241222795: {  # Blood Simple
  "Clue": "A Texas bar owner hires a sweaty private detective to kill his wife and her lover, and the detective double-crosses him.",
  "Notes": "The Coen brothers' first film, its title from Dashiell Hammett's <i>Red Harvest</i>; Frances McDormand made her debut."},
 1790241222855: {  # Come and See
  "Clue": "A Belarusian boy digs up a rifle to join the partisans, and watches an SS unit burn a village's people inside a barn.",
  "Notes": "His face ages visibly across the film, which ends running newsreel backward to Hitler as a baby; Elem Klimov never made another film."},
 1790241222886: {  # Paris, Texas
  "Clue": "A man walks out of the desert after four years of silence, reclaims his son, and finds his wife working behind one-way glass in a Houston peep show.",
  "Notes": "Sam Shepard wrote it and Ry Cooder's slide guitar scores it; it won the Palme d'Or.",
  "Movement": ""},
 1790241222916: {  # Brazil
  "Clue": "A dead fly in a printer causes the clerical error that sends the wrong man to be arrested, and a low-level functionary who dreams of flying is drawn into the machinery.",
  "Notes": "Universal tried to impose a happy ending, and Terry Gilliam took out a trade advertisement asking the studio head when he would release it.",
  "Movement": "Dystopian satire"},
 1790241222945: {  # Down by Law
  "Clue": "A disc jockey, a pimp, and a chattering Italian tourist share a New Orleans cell, and escape through the bayou.",
  "Notes": "Shot in black and white by Robby Müller; Roberto Benigni learned his English lines phonetically."},
 1790241222984: {  # Jesus of Montreal
  "Clue": "A young actor hired to modernize a shrine's Passion play finds his life repeating the story he is staging.",
  "Notes": "The cleansing of the temple happens at an advertising audition; it won the Jury Prize at Cannes.",
  "Movement": ""},
 1790241223012: {  # Hard Boiled
  "Clue": "A clarinet-playing Hong Kong policeman shoots his way through a hospital in a take of nearly three minutes, while babies are carried out of the maternity ward.",
  "Notes": "John Woo's last Hong Kong film before Hollywood; the “single take” hides several joins.",
  "Movement": "Heroic bloodshed"},
 1790241223046: {  # Reservoir Dogs
  "Clue": "Six criminals given colour-coded aliases argue about Madonna and tipping, and regroup in a warehouse after a diamond robbery that is never shown.",
  "Notes": "Quentin Tarantino's first film, much of its budget from Harvey Keitel; the ear-cutting scene, set to “Stuck in the Middle with You,” caused walkouts at Sundance."},
 1790241223077: {  # Naked
  "Clue": "A brilliant, vicious Mancunian talks his way across night-time London, delivering apocalyptic lectures to anyone who will listen.",
  "Notes": "Mike Leigh built it from months of improvisation; David Thewlis won Best Actor at Cannes, and Leigh Best Director."},
 1790241223115: {  # Short Cuts
  "Clue": "Twenty-two Los Angeles characters cross paths during a medfly spraying campaign, from fishermen who don't report a body to a phone-sex worker changing diapers.",
  "Notes": "From nine Raymond Carver stories and a poem, moved to Los Angeles; the whole cast shared a special award at Venice."},
 1790241223150: {  # Heavenly Creatures
  "Clue": "Two Christchurch schoolgirls build an imaginary kingdom, and when their families try to separate them they kill one of the mothers.",
  "Notes": "A true story, and Kate Winslet's first film; one of the real girls later became the crime novelist Anne Perry.",
  "Movement": "True crime"},
 1790241223192: {  # Drifting Clouds
  "Clue": "A tram driver and a restaurant head waiter both lose their jobs in the Finnish recession, and sink through debt and humiliation in perfect deadpan.",
  "Notes": "The first of Aki Kaurismäki's Finland trilogy; his usual lead, Matti Pellonpää, died before shooting and is honoured in a photograph.",
  "Movement": ""},
 1790241223212: {  # Breaking the Waves
  "Clue": "A devout young woman on a Scottish island marries an oil-rig worker who, paralyzed, asks her to take lovers and describe them to him.",
  "Notes": "Emily Watson's debut; bells ring over the sea at the end, and the handheld image was degraded through video on purpose.",
  "Movement": ""},
 1790241223248: {  # Taste of Cherry
  "Clue": "A man drives around the hills outside Tehran looking for someone willing to bury him after he kills himself.",
  "Notes": "It shared the Palme d'Or in 1997, and ends on video footage of the crew; a taxidermist talks him through mulberries."},
 1790241223280: {  # Werckmeister Harmonies
  "Clue": "A circus brings a stuffed whale to a freezing Hungarian town, and a mob forms and wrecks a hospital.",
  "Notes": "About 39 shots in 145 minutes, opening with a drunk demonstrating an eclipse in a bar; adapted from László Krasznahorkai's novel."},
 1790241223336: {  # Amores Perros
  "Clue": "A car crash in Mexico City connects a boy who enters his brother's dog in illegal fights, a model with a lapdog, and a homeless hitman surrounded by strays.",
  "Notes": "Alejandro González Iñárritu's first feature, and the first of his Death Trilogy with the writer Guillermo Arriaga.",
  "Movement": ""},
 1790241223402: {  # In the Mood for Love
  "Clue": "Two neighbours in 1962 Hong Kong discover that their spouses are having an affair with each other, and rehearse the confrontation themselves.",
  "Notes": "They pass on the stairs to the noodle stall in slow motion to a waltz; the secret is finally whispered into a hole at Angkor Wat.",
  "Movement": "Hong Kong Second Wave"},
 1790241223432: {  # Mulholland Drive
  "Clue": "An amnesiac car-crash survivor and an aspiring actress find a blue box and a blue key, and then everyone changes identity.",
  "Notes": "At the Club Silencio a singer collapses while her voice goes on; the film began as a rejected television pilot."},
 1790241223462: {  # Good Bye, Lenin!
  "Clue": "A committed East German socialist wakes from a coma after the Wall has fallen, and her son recreates the vanished country in her bedroom.",
  "Notes": "The biggest German hit of its year, it popularized the word <i>Ostalgie</i>; Yann Tiersen wrote the score."},
 1790241223496: {  # Tsotsi
  "Clue": "A Soweto gang leader shoots a woman for her car, and finds her baby on the back seat.",
  "Notes": "From Athol Fugard's 1960s novel, moved to the post-apartheid present; it won the foreign-language Oscar.",
  "Movement": ""},
 1790241223531: {  # Caché
  "Clue": "A Paris television presenter receives videotapes of his own front door, wrapped in childish drawings of a figure bleeding from the mouth.",
  "Notes": "The guilt they uncover goes back to an Algerian boy and the massacre of 17 October 1961; Michael Haneke has never said who sends the tapes.",
  "Movement": ""},
 1790241223552: {  # Times and Winds
  "Clue": "Three children in a mountain village live through the five daily calls to prayer that divide the film.",
  "Notes": "The Turkish title means “five times,” the prayer times; Reha Erdem set it to Arvo Pärt.",
  "Movement": ""},
 1790241223585: {  # Ten Canoes
  "Clue": "The first feature made entirely in an Australian Aboriginal language, in which a goose-egg hunt frames an older story about a man who covets his brother's wife.",
  "Notes": "Narrated in English by David Gulpilil, and built around Donald Thomson's 1930s photographs of the same swamp.",
  "Movement": ""},
 1790241223622: {  # There Will Be Blood
  "Clue": "A silver prospector turned oilman builds a California empire, and settles his score with a young preacher in a private bowling alley.",
  "Notes": "Loosely from Upton Sinclair's <i>Oil!</i>, to Jonny Greenwood's score; its first fifteen minutes have no dialogue.",
  "Movement": ""},
 1790241223662: {  # The Secret in Their Eyes
  "Clue": "A retired court investigator writing a novel reopens a 1974 rape and murder, whose suspect was found through his gaze in old photographs.",
  "Notes": "It won the foreign-language Oscar; its chase through a packed football stadium is a composite made to look like one shot."},
 1790241223713: {  # The Kid with a Bike
  "Clue": "An eleven-year-old in a children's home refuses to believe his father has abandoned him, and is taken in on weekends by a hairdresser.",
  "Notes": "Jean-Pierre and Luc Dardenne's first use of music, four short bursts of Beethoven; it shared the Grand Prix at Cannes."},
 1790241223749: {  # Holy Motors
  "Clue": "A man is driven around Paris in a white stretch limousine to nine appointments, at each of which he becomes someone else.",
  "Notes": "In one he is a sewer creature who eats flowers and abducts a model; the limousines talk to each other in the garage at the end.",
  "Movement": ""},
 1790241223772: {  # The Grand Budapest Hotel
  "Clue": "A concierge in a fictional interwar republic inherits a painting of a boy with an apple, is framed for murder, and is chased over the Alps on a sled.",
  "Notes": "Its nested time periods are shot in three aspect ratios; it won four Oscars for its craft, and credits Stefan Zweig as its inspiration."},
 1790241235206: {  # Hearts of Darkness
  "Clue": "A documentary built from the audio a director's wife secretly recorded during his disastrous shoot in the Philippines.",
  "Notes": "Eleanor Coppola's tapes record a typhoon, Martin Sheen's heart attack, and Francis Ford Coppola admitting he has no ending."},
 1790241347311: {  # The General
  "Clue": "A Confederate railway engineer rejected by the army chases his stolen locomotive north and back again, never once changing expression.",
  "Notes": "Based on the Andrews Raid of 1862; a real bridge collapses under a real train, and the film's failure ended Buster Keaton's independence."},
 1790241347336: {  # Modern Times
  "Clue": "A factory worker is fed by a malfunctioning automatic lunch machine, and tightens bolts until he is swallowed by the gears.",
  "Notes": "The Tramp's last appearance, and the only film in which his voice is heard, singing nonsense Italian; Chaplin was still refusing dialogue in 1936."},
 1790241347369: {  # Bringing Up Baby
  "Clue": "A paleontologist loses a prized bone to a dog, and is dragged around Connecticut by an heiress with a tame leopard.",
  "Notes": "A flop that got Katharine Hepburn labelled box-office poison; it is now the standard example of screwball comedy."},
 1790241347407: {  # Ugetsu
  "Clue": "In the sixteenth-century civil wars, a potter chasing profit is seduced by a noblewoman who turns out to be a ghost.",
  "Notes": "A boat glides out of the mist across Lake Biwa; it took the Silver Lion at Venice and, with <i>Rashomon</i>, opened Japanese cinema to the West.",
  "Movement": "<i>Jidaigeki</i>"},
 1790241347438: {  # Rear Window
  "Clue": "A photographer laid up with a broken leg watches his courtyard neighbours through a telephoto lens, and becomes convinced one has murdered his wife.",
  "Notes": "The whole film stays inside one apartment, looking out on a courtyard of 31 apartments built on a Paramount stage."},
 1790241347468: {  # Wild Strawberries
  "Clue": "An old professor driving to Lund for an honorary degree dreams of a clock without hands and of his own coffin.",
  "Notes": "Victor Sjöström, the silent director of <i>The Phantom Carriage</i>, plays him at 78.",
  "Movement": ""},
 1790241347491: {  # North by Northwest
  "Clue": "An advertising man mistaken for a spy who does not exist is attacked by a crop duster on an empty country road.",
  "Notes": "It ends on Mount Rushmore; Bernard Herrmann wrote the fandango, and Saul Bass designed the titles."},
 1790241347532: {  # Cléo from 5 to 7
  "Clue": "A pop singer waits ninety minutes, in near real time, for the result of a biopsy.",
  "Notes": "Chapter titles keep the clock; she finally meets a soldier on leave from Algeria in the Parc Montsouris."},
 1790241347562: {  # Lawrence of Arabia
  "Clue": "A misfit British officer crosses the Nefud Desert to take Aqaba from the landward side.",
  "Notes": "A match blown out cuts to a desert sunrise; shot in 70mm, it has no women in speaking parts, and Maurice Jarre wrote the score in six weeks.",
  "Movement": "Historical epic"},
 1790241347598: {  # 8½
  "Title": "8½",
  "Clue": "A film director with nothing to say hides at a spa from his producer, his wife, and his mistress.",
  "Notes": "It ends with everyone in his life joining a circus parade; the title counts Federico Fellini's previous films, and it inspired the musical <i>Nine</i>.",
  "Movement": ""},
 1790241347617: {  # Daisies
  "Clue": "Two young women decide that since the world is spoiled they will be spoiled too, and wreck a banquet laid for officials.",
  "Notes": "Banned at home for its food-wasting, not its politics; Věra Chytilová was forbidden to work for years afterward."},
 1790241347661: {  # The Conformist
  "Clue": "A man who wants above all to be normal joins Mussolini's secret police, and is sent to Paris to have his old professor killed.",
  "Notes": "Vittorio Storaro's photography slices light through Fascist architecture; Francis Ford Coppola and Martin Scorsese both cite it.",
  "Movement": ""},
 1790241347683: {  # Solaris
  "Clue": "A psychologist sent to a station orbiting a sentient ocean finds the crew haunted by physical copies of people from their memories, including his dead wife.",
  "Notes": "From Stanisław Lem, who disliked it; a five-minute drive on a Tokyo expressway stands in for the city of the future."},
 1790241347723: {  # Barry Lyndon
  "Clue": "An Irish adventurer duels, deserts from two armies, cheats at cards across Europe, and marries a countess.",
  "Notes": "From Thackeray; its interiors are lit by candles alone, shot with f/0.7 lenses made for NASA."},
 1790241347744: {  # Nashville
  "Clue": "Twenty-four characters converge on a country-music city during a populist presidential campaign whose candidate is heard only from a loudspeaker van.",
  "Notes": "It ends with a shooting at a rally and the crowd singing “It Don't Worry Me”; the cast wrote their own songs, and Keith Carradine's “I'm Easy” won the Oscar."},
 1790241347774: {  # Goodfellas
  "Clue": "A half-Irish boy from Brooklyn rises through a crew, narrating from his first line: as far back as he can remember, he always wanted to be a gangster.",
  "Notes": "A Steadicam takes a date in through the kitchen of the Copacabana; Joe Pesci won Best Supporting Actor for a “funny how?” scene he drew from life."},
 1790241347804: {  # Schindler's List
  "Clue": "A Sudeten German profiteer staffs his enamelware factory with Jewish workers, and ends up spending his fortune to save them.",
  "Notes": "The black and white is broken once by a small girl's red coat; Steven Spielberg took no salary and founded the Shoah Foundation with the profits."},
 1790241347845: {  # Beau Travail
  "Clue": "A Foreign Legion sergeant in Djibouti is consumed by jealousy of a new recruit.",
  "Notes": "Loosely from <i>Billy Budd</i>; it ends with the sergeant dancing alone to “The Rhythm of the Night.”",
  "Movement": ""},
 1790241347869: {  # Yi Yi
  "Clue": "A Taipei family's year runs from a wedding to a funeral, while the eight-year-old son photographs the backs of people's heads because they cannot see them.",
  "Notes": "It won Best Director at Cannes but was not released in Taiwan in Edward Yang's lifetime."},
 1790241347906: {  # Persepolis
  "Clue": "A girl grows up through the Iranian revolution and the war with Iraq, in stark hand-drawn black and white.",
  "Notes": "Marjane Satrapi adapted her own graphic novel; Iran protested its selection at Cannes, where it shared the Jury Prize."},
 1790241347937: {  # Grave of the Fireflies
  "Clue": "A teenage boy and his small sister, orphaned by the firebombing of Kobe, live in a hillside shelter until she dies of malnutrition.",
  "Notes": "Isao Takahata made it for Studio Ghibli, and it was released on a double bill with <i>My Neighbor Totoro</i>.",
  "Movement": "Anime"},
 1790241360307: {  # Andrei Rublev
  "Clue": "A fifteenth-century icon painter takes a vow of silence after killing a man in a Tatar raid, and a boy casts an enormous bell.",
  "Notes": "It opens with a peasant's hot-air balloon flight and ends in colour on the finished icons; the Soviet authorities shelved it for five years.",
  "Movement": ""},
 1790241461624: {  # Mad Max: Fury Road
  "Clue": "An imperator drives a war rig off its fuel run to smuggle five wives away from a warlord who rations water.",
  "Notes": "Almost the whole film is one chase out and back, with a flame-throwing guitarist on a truck of drummers; it won six Oscars, all for craft."},
 1790241461652: {  # Son of Saul
  "Clue": "A Sonderkommando prisoner at Auschwitz tries to find a rabbi to bury a boy he takes for his son.",
  "Notes": "The camera stays on his face in a shallow-focus, near-square frame while the horror happens out of focus; it won the foreign-language Oscar."},
 1790241461684: {  # Carol
  "Clue": "A Manhattan shopgirl in 1952 sells a train set to an elegant customer who leaves her gloves behind on purpose.",
  "Notes": "From Patricia Highsmith's <i>The Price of Salt</i>, published under a pseudonym because it did not punish its lovers; shot on 16mm.",
  "Movement": "Romantic drama"},
 1790241461720: {  # The Assassin
  "Clue": "A ninth-century killer trained by a nun is ordered to murder the cousin she was once betrothed to, and does not.",
  "Notes": "The fights last seconds and the takes last minutes; Hou Hsiao-hsien won Best Director at Cannes.",
  "Movement": "<i>Wuxia</i>"},
 1790241461782: {  # Moonlight
  "Clue": "Three chapters in the life of a boy growing up poor, Black, and gay in Miami, each with a different actor and a different name.",
  "Notes": "A drug dealer teaches him to swim; it won Best Picture after the envelope was misread on stage.",
  "Movement": ""},
 1790241461803: {  # Toni Erdmann
  "Clue": "A retired music teacher with joke false teeth turns up in Bucharest to pester his management-consultant daughter, disguised as a life coach.",
  "Notes": "Its Whitney Houston singalong is the heart of the film; it was the Cannes critics' clear favourite, and won nothing there."},
 1790241461838: {  # Arrival
  "Clue": "A linguist is brought in to learn the written language of aliens, circular ink marks with no direction in time.",
  "Notes": "From Ted Chiang's “Story of Your Life”; Max Richter's “On the Nature of Daylight” bookends it."},
 1790241461877: {  # Get Out
  "Clue": "A Black photographer visiting his white girlfriend's family is hypnotized with a teaspoon and a teacup into a paralyzed “sunken place.”",
  "Notes": "Made for about $4.5 million, it took over $250 million; Jordan Peele won the screenplay Oscar."},
 1790241461899: {  # Call Me by Your Name
  "Clue": "A seventeen-year-old and his father's American graduate student circle each other through a summer in northern Italy.",
  "Notes": "The father's speech about not killing feeling is its centre; James Ivory won the adapted-screenplay Oscar at 89."},
 1790241461943: {  # Lady Bird
  "Clue": "A Sacramento Catholic-school senior who insists on a name she gave herself throws herself out of a moving car during an argument with her mother."},
 1790241461962: {  # Phantom Thread
  "Clue": "A fastidious 1950s London couturier takes a waitress as his muse, and she learns to poison him with mushrooms.",
  "Notes": "Paul Thomas Anderson shot it himself, to Jonny Greenwood's score; it was announced as Daniel Day-Lewis's last film.",
  "Movement": ""},
 1790241461994: {  # Shoplifters
  "Clue": "A makeshift Tokyo household living off a grandmother's pension and petty theft takes in a neglected little girl.",
  "Movement": ""},
 1790241462029: {  # Roma
  "Clue": "A live-in housekeeper for a middle-class family in 1970s Mexico City loses her baby during the Corpus Christi massacre.",
  "Notes": "Shot in black and white, largely in slow lateral pans; Alfonso Cuarón wrote, shot, and edited it, and it was the first Netflix film nominated for Best Picture.",
  "Movement": ""},
 1790241462059: {  # Burning
  "Clue": "A would-be writer meets a woman who mimes peeling a tangerine, and her rich friend, who says he burns down a greenhouse every two months.",
  "Notes": "From Haruki Murakami's “Barn Burning,” which takes its title from William Faulkner; it topped <i>Screen</i>'s Cannes critics' grid and won nothing.",
  "Movement": ""},
 1790241462088: {  # Parasite
  "Clue": "A poor family living in a semi-basement cons its way, one member at a time, into jobs with a rich family."},
 1790241462121: {  # Nomadland
  "Clue": "A widow whose Nevada company town loses its ZIP code converts a van and follows seasonal work around the West, among real nomads playing themselves.",
  "Notes": "Chloé Zhao became the second woman, and the first woman of colour, to win the directing Oscar.",
  "Movement": ""},
 1790241462160: {  # The Power of the Dog
  "Clue": "A Montana rancher who castrates calves bare-handed torments his brother's new wife, until her delicate son befriends him.",
  "Notes": "The title comes from Psalm 22; Jane Campion became the first woman nominated twice for the directing Oscar, and won."},
 1790241462183: {  # Tár
  "Clue": "A celebrated conductor preparing Mahler's Fifth in Berlin humiliates a student in a Juilliard masterclass, and is undone by the suicide of a former protégée.",
  "Notes": "Cate Blanchett learned to conduct, play piano, and speak German for it; it ends with her conducting a video-game score in Southeast Asia.",
  "Movement": ""},
 1790241462223: {  # Oppenheimer
  "Clue": "A physicist's security-clearance hearing and a cabinet nominee's confirmation are cross-cut, in colour and in black and white, around the Trinity test.",
  "Notes": "Christopher Nolan shot it on IMAX film; it won seven Oscars, including Best Picture, and its joint release with <i>Barbie</i> became a cultural event."},
 1790241462245: {  # Anatomy of a Fall
  "Clue": "A German writer is tried in Grenoble for her husband's fatal plunge from their chalet window, with their partially sighted son as a witness.",
  "Notes": "It won the Palme d'Or and the screenplay Oscar; the dog, Messi, won the Palm Dog."},
 1790241462281: {  # The Zone of Interest
  "Clue": "The Auschwitz commandant and his wife tend their garden on the other side of the camp wall, while the atrocity exists only in the sound.",
  "Notes": "Jonathan Glazer used fixed cameras running unmanned through the house; it won the international-feature and sound Oscars."},
 1790241462311: {  # Poor Things
  "Clue": "A surgeon revives a drowned woman with her own unborn baby's brain, and she learns the world at speed in Lisbon, on a cruise ship, and in a Paris brothel.",
  "Notes": "From Alasdair Gray's novel; it won four Oscars, including Best Actress for Emma Stone."},
 1790254598581: {  # Everything Everywhere All at Once
  "Clue": "A laundromat owner in the middle of a tax audit borrows skills from her selves in other universes, including one where everyone has hot dogs for fingers.",
  "Notes": "It won seven Oscars, including Best Picture; the villain's weapon is a bagel with everything on it."},
 1790254598657: {  # Past Lives
  "Clue": "Two childhood friends separated when one family emigrates from Seoul reconnect twice across twenty-four years, the second time in New York, where she is married.",
  "Notes": "The Korean idea of <i>in-yun</i>, ties accumulated across past lives, is its argument; it was nominated for Best Picture.",
  "Movement": "Romantic drama"},
 1790254625911: {  # Portrait of a Lady on Fire
  "Clue": "A painter is sent to a Breton island in the 1770s to paint a woman in secret for her betrothal, memorizing her face on their walks.",
  "Notes": "It ends on a face across a concert hall during Vivaldi's “Summer”; it won the screenplay prize at Cannes.",
  "Movement": "Romantic drama"},
 1790254645378: {  # Drive My Car
  "Clue": "A stage director rehearsing <i>Uncle Vanya</i> in several languages at once is assigned a young woman as chauffeur for his red Saab.",
  "Notes": "From a Haruki Murakami story; the opening credits arrive forty minutes in, and it won the international-feature Oscar.",
  "Movement": ""},
 # the 38 director cards (FIGURE to NAME): one identifying trait each, no film titles on the front
 1790254934964: {"Clue": "A Bronx-born perfectionist who moved to England and made thirteen features in forty-six years, each researched to exhaustion and shot in endless takes."},
 1790254935084: {"Clue": "A Viennese-born master of Weimar cinema who left Germany in 1933 and made hard, fatalistic thrillers in Hollywood for twenty years."},
 1790254935180: {"Clue": "The English-born “master of suspense,” who appeared briefly in almost all of his own films and coined the term MacGuffin.",
  "Notes": "He moved to Hollywood in 1939 on a Selznick contract, and never won a competitive directing Oscar."},
 1790254935278: {"Clue": "An Aragonese Surrealist who made his first film with Salvador Dalí, spent two decades working in Mexico, and ended with elegant French satires of the bourgeoisie.",
  "Notes": "During the Civil War he worked for the Republic in Paris, and afterward for the MoMA in New York."},
 1790254935367: {"Clue": "The director half of the British partnership that signed its films “The Archers,” sharing one credit with a Hungarian émigré screenwriter.",
  "Notes": "His partner, Emeric Pressburger, wrote the scripts; <i>Peeping Tom</i> wrecked his career, and Thelma Schoonmaker, Martin Scorsese's editor, became his wife."},
 1790254935463: {"Clue": "A Viennese-born, Berlin-trained screenwriter who fled in 1933 and became Hollywood's sharpest cynic."},
 1790254935549: {"Clue": "A Swedish pastor's son who made about sixty films of faith, silence, and marriage, many of them on the island of Fårö with the cinematographer Sven Nykvist."},
 1790254935663: {"Clue": "A cartoonist from Rimini who began in neorealism and ended in circus, and gave the world its word for celebrity photographers.",
  "Notes": "He won four foreign-language Oscars and an honorary one; Giulietta Masina, his wife, starred in several of his films.",
  "Works": "<i>La Strada</i>; <u><i>La Dolce Vita</i></u>; <i>8½</i>"},
 1790254935765: {"Clue": "The most commercially successful director in history, who invented the summer blockbuster with a malfunctioning mechanical shark."},
 1790254935854: {"Clue": "A Little Italy asthmatic who nearly became a priest, and turned Catholic guilt into American crime cinema, nine times with Robert De Niro."},
 1790254935884: {"Clue": "A Russian who made only seven features, described his craft as “sculpting in time,” and died in exile in Paris in 1986."},
 1790254935981: {"Clue": "An Eagle Scout from Missoula whose films peel back the lawns of small-town America to show the beetles underneath.",
  "Notes": "He also co-created <i>Twin Peaks</i>, and practised Transcendental Meditation for decades."},
 1790254936090: {"Clue": "A German Expressionist who went to Hollywood and won a one-off Academy Award for Unique and Artistic Production."},
 1790254936182: {"Clue": "A London music-hall performer who became the most famous man on earth as a tramp in a bowler hat, and co-founded United Artists."},
 1790254936267: {"Clue": "An Indiana-born professional who worked in every genre without a signature visual style, and whose women give as good as they get."},
 1790254936368: {"Clue": "A prodigy who panicked radio listeners with a Martian invasion, and at twenty-five made a film that William Randolph Hearst tried to have destroyed."},
 1790254936464: {"Clue": "The Japanese director who opened his country's cinema to the West, and whose swordsmen were remade as cowboys in Hollywood and Italy.",
  "Notes": "He worked with Toshiro Mifune sixteen times; after a suicide attempt in 1971, his late films were funded from the Soviet Union, France, and America."},
 1790254936553: {"Clue": "A Maine-born son of Irish immigrants who won four directing Oscars, none of them for his Westerns, and shot nine films in Monument Valley."},
 1790254936667: {"Clue": "A <i>Cahiers du cinéma</i> critic who attacked French studio cinema in print, then launched the New Wave at Cannes with a semi-autobiographical first feature."},
 1790254936751: {"Clue": "A UCLA film graduate who won Best Picture twice in three years, for a mafia saga and its sequel.",
  "Notes": "He won five Oscars; his wineries paid off his debts, and his daughter Sofia and nephew Nicolas Cage also went into film."},
 1790254936851: {"Clue": "A Bavarian who dragged a steamship over a hill in Peru, and narrates his documentaries in a flat, doom-laden voice."},
 1790254936949: {"Clue": "A survivor of the Kraków ghetto who fled the United States in 1978 after pleading guilty to unlawful sex with a thirteen-year-old."},
 1790254937031: {"Clue": "A Tyneside-born maker of commercials whose two science-fiction films of 1979 and 1982 set the look of the genre for forty years."},
 1790254937139: {"Clue": "A leading figure of New German Cinema whose films are mostly journeys, and who also made a documentary about Cuban musicians."},
 1790254937235: {"Clue": "A former video-store clerk whose films scramble chronology, quote genre cinema constantly, and use old records instead of a score."},
 1790254937288: {"Clue": "Minnesota brothers who wrote, produced, and directed together for nearly forty years, and edited under the shared pseudonym Roderick Jaynes.",
  "Notes": "<i>No Country for Old Men</i> won them Best Picture in 2008."},
 1790254937390: {"Clue": "An Austrian who films violence as coldly as possible to deny the audience any pleasure in it, and has twice won the Palme d'Or."},
 1790254937475: {"Clue": "One of the three Mexican directors who dominated Hollywood's awards in the 2010s, and who wrote, photographed, and edited a film about his family's housekeeper."},
 1790254937585: {"Clue": "A New Zealander who began with splatter comedies made on weekends, and filmed a three-part fantasy epic back to back in his own country.",
  "Notes": "He later restored and colourized First World War footage for <i>They Shall Not Grow Old</i>; his effects house is Weta."},
 1790254937680: {"Clue": "An English editor turned director who made intimate British films in the 1940s, and then a run of enormous 70mm location epics."},
 1790254937773: {"Clue": "A Kansas City bomber pilot who came to features late, and filled them with overlapping multitrack dialogue, huge casts, and zoom lenses."},
 1790254937868: {"Clue": "A San Fernando Valley director who moved from sprawling ensembles to close studies of monstrous men, with Jonny Greenwood scoring most of his films since 2007.",
  "Notes": "<i>Boogie Nights</i> and <i>Magnolia</i> are the sprawling ensembles; <i>The Master</i> is his portrait of a cult leader."},
 1790254937937: {"Clue": "The most radical of the <i>Cahiers du cinéma</i> critics turned director, who invented the jump cut to shorten his first feature."},
 1790254938016: {"Clue": "A Belgian-born photographer called the grandmother of the New Wave, who in her seventies made a documentary about gleaners on a handheld camera.",
  "Notes": "She was married to Jacques Demy, and received an honorary Oscar in 2017."},
 1790254938070: {"Clue": "A Japanese director who returned throughout his career to parents, grown children, and a daughter who will not marry, filmed from the height of someone kneeling on a tatami mat."},
 1790254938165: {"Clue": "A South Korean who mixes genre and class satire without warning, and took four Oscars in one night in 2020.",
  "Notes": "Accepting a Golden Globe in 2020, he said that subtitles are a one-inch barrier worth getting over."},
 1790254938271: {"Clue": "The painter's son who made the two towering films of French poetic realism, and spent the war years in Hollywood."},
 1790254938368: {"Clue": "A Calcutta commercial artist who saw <i>Bicycle Thieves</i> in London, and sold his wife's jewellery to fund his first feature."},
}
