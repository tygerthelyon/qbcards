# -*- coding: utf-8 -*-
"""cm_text_0929.py -- Carter's Classical Music notes of 2026-09-28/29.

1. "Listen for" never repeats the description beside it, and describes the passage actually playing (Carter:
   "Listen for should be specific to the passage (meant to actually help me get the famous music being played)";
   Gnossiennes and Danse macabre said the same thing twice). All 482 active pairs were read: where the Listen line
   was generic or restated the description, it is rewritten to name what you hear in that clip; where the
   description was only a restatement of the sound, the description (and an identical clue) takes other facts.
2. Clues that nearly name the answer are reworded (Woyzeck on Wozzeck, Kreisler on Kreisleriana, the Rhine gold
   on Das Rheingold, the Erlking on Erlkoenig, Caesar on Giulio Cesare, Bach on Bachianas brasileiras, Matthias
   on Mathis der Maler, Orfeo on L'Orfeo, "Der Tod und das Maedchen" on Death and the Maiden).
3. Titles of sung numbers in quotes (Carter: "Put aria titles in quotes"); instrumental movements stay italic;
   act labels one style ("Act III · ").
4. Italics: Holst's *Mars*, Wagner's *Ring*.
5. Concept cards whose "Heard in" example has a clip elsewhere in the deck now play it (Recitative had none).
6. Templates: DESCRIPTION to WORK asks "Title?" (was "Work?"), and the title sits further below the clip.

    py -3.9 cm_text_0929.py [--apply]
"""
import json
import os
import re
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))

LISTEN = {
    1787711405033: "A slow, sinuous oboe melody over a gently rocking accompaniment; the women's chorus then takes it up.",
    1787711405049: "The solo flute, alone and languid, sliding down and back up through a tritone before harp and horns enter.",
    1787711405062: "A slow, noble E-flat melody in the strings, hushed at first, swelling to one radiant climax and falling away.",
    1787711405096: "Strings and harp alone: a slow, yearning F-major melody that hangs on its suspensions and swells to one great climax.",
    1787711405101: "Swirling string runs, then trombones and tuba blast out a menacing theme over hammering timpani.",
    1787711405140: "A tender, gently swaying melody in the violins, then clarinet flourishes and a lilting dance tune over snare drum.",
    1787711405151: "Twelve soft harp strokes for midnight, then the violin's grating double-stopped tritones; the flute begins a ghostly waltz over pizzicato strings.",
    1787711405166: "A lilting Viennese waltz in the strings on the Act 2 duet tune “Du und du”, with a swaying, hesitating upbeat.",
    1787711405172: "A sombre, trudging B-flat-minor march in bassoons and violas that builds to a blaze of brass.",
    1787711405203: "The chorus's gentle processional in B-flat, “Treulich geführt”, the tune known in English as “Here Comes the Bride”.",
    1787711405204: "Whirling string figures, then trombones and horns blaze out a fanfare theme in G major.",
    1787711405306: "No violins at all, so the sound is dark and bottom-heavy; the chorus enters low and slow on “Selig sind”.",
    1787711405510: "A sweeping rising arpeggio from the piano, then rippling triplets and a warm violin theme in A major.",
    1787711405507: "Hushed, chorale-like chords in G minor, slow and even: the theme for five variations.",
    1787711405545: "A gentle C-major melody in the first violin, songlike and unhurried, over an even accompaniment.",
    1787711405464: "A few bars of piano introduction, then a sweeping, carefree waltz in D major.",
    1787711405722: "Low clarinets intone a bare, dark motto, then a limping E-minor Allegro in a dance-like 6/8.",
    1787711405834: "A slow, grave horn melody over plucked strings, stately and bare, in G major.",
    1787711406034: "Forceful D-major unison chords and rushing violin scales, with sudden quiet turns to the minor.",
    1787711406077: "Alternating loud, martial C-major chords and a quiet lyrical answer in the opening bars; trumpets and drums throughout.",
    1787792906309: "Solo harpsichord, thick with trills and mordents, in the gentle dance rhythms of the French court.",
    1787792906327: "Pentatonic melodies in delicate, chamber-like scoring for tenor or alto, coloured by flute, harp, and mandolin.",
    1787792906329: "Hushed, restrained choir with organ and low strings, gentle and consoling rather than dramatic.",
    1787792906330: "A tiny, gentle piano melody in A major, as simple as a folk song.",
    1787792906335: "A voice half-speaking, half-singing in Sprechstimme, with the instruments changing from poem to poem.",
    1787792906346: "A soprano's wordless, long-breathed vocalise high above a choir of cellos plucking like guitars.",
    1788199512173: "Organ and full double chorus blaze out “Veni, creator spiritus” from the very first bar, with no instrumental introduction.",
    1788199516836: "A slow piano melody winding around a few notes of a modal, vaguely Eastern scale, over a plain two-chord bass that never changes pace.",
    1788199516864: "Unaccompanied voices on a single held note that slowly spreads into soft, shimmering clusters.",
    1788489953189: "Suzel's short, simple soprano song offering a bunch of violets, over light woodwinds and strings.",
    1788489953262: "Plain hymn-and-march tunes, deliberately artless, with the singers chanting circular, nonsense-seeming words.",
    1788489953362: "Hard-edged chorus and blazing brass in jagged rhythms, broken by sudden hushed passages.",
}

DESC = {
    1787711405036: "Written for the birth of a son to Bertha Faber, a singer Brahms had known in Hamburg; its accompaniment quietly quotes a Viennese song she used to sing to him.",
    1787711405043: "A study for the left hand, written in 1831 when Chopin heard in Stuttgart that the Russians had taken Warsaw; the Op. 10 set is dedicated to Liszt.",
    1787711405045: "Written for Martha Graham, who supplied the title from a Hart Crane poem after the music was finished; it won the 1945 Pulitzer Prize.",
    1787711405049: "After Stéphane Mallarmé's poem. Boulez said modern music begins with it, and Vaslav Nijinsky's 1912 ballet caused a scandal.",
    1787711405066: "Gershwin's tone poem of an American strolling through Paris, blending blues with a French promenade; later the basis of a Gene Kelly film.",
    1787711405083: "Written for George II's coronation in 1727 and sung at every British coronation since.",
    1787711405085: "The joke is said to have been aimed at dozing London audiences, hence the nickname. One of the twelve symphonies Haydn wrote for Johann Peter Salomon's concerts.",
    1787711405096: "Opens with a solo trumpet funeral march; the Adagietto was a love letter to Alma Mahler and became famous through Luchino Visconti's film <i>Death in Venice</i>.",
    1787711405127: "Pachelbel's only widely known work, long forgotten until a 1968 recording made it a wedding staple.",
    1787711405137: "Twenty-four variations for piano and orchestra on Paganini's 24th Caprice; the Dies irae chant also runs through it.",
    1787711405138: "Written as a ballet for Ida Rubinstein; Ravel called it “a piece for orchestra without music”.",
    1787711405147: "Rossini's last opera, written at thirty-seven; he wrote no more operas in the thirty-nine years he had left, and its final galop became the Lone Ranger theme.",
    1787711405151: "A tone poem after a poem by Henri Cazalis: Death calls the skeletons up at midnight, playing a fiddle with its E string tuned down to E-flat; the xylophone is their rattling bones, and a cockcrow ends it.",
    1787711405153: "Dedicated to the memory of Liszt, who died weeks after its 1886 London premiere. It is laid out in two large parts rather than four movements, and adds organ and piano four hands.",
    1787711405876: "Dedicated to the memory of Liszt, who died weeks after its 1886 London premiere. It is laid out in two large parts rather than four movements, and adds organ and piano four hands.",
    1787711405164: "Six tone poems on Bohemian history and landscape, from the castle of Vyšehrad to the Hussite mountain of Blaník; Smetana wrote them after going deaf.",
    1787711405167: "After Nietzsche's book, in nine sections; its sunrise opening became famous through <i>2001: A Space Odyssey</i>.",
    1787711405171: "Marks Napoleon's retreat from Moscow and is scored for cannon and church bells. Tchaikovsky himself thought it loud and insincere.",
    1787711405175: "Tchaikovsky's last ballet, from E. T. A. Hoffmann via Dumas: Clara's nutcracker becomes a prince and takes her to the Land of Sweets.",
    1787711405195: "Written for the anniversary of Alessandro Manzoni's death, and criticized as an opera in church dress; the Dies irae returns like a refrain.",
    1787711405776: "Written for the anniversary of Alessandro Manzoni's death, and criticized as an opera in church dress; the Dies irae returns like a refrain.",
    1787711405777: "Written for the anniversary of Alessandro Manzoni's death, and criticized as an opera in church dress; the Dies irae returns like a refrain.",
    1787711405208: "Its Toccata finale is the standard wedding recessional. Widor played at Saint-Sulpice for sixty-four years.",
    1787711405211: "After a George Meredith poem, begun in 1914 and revised after the war, and dedicated to the violinist Marie Hall.",
    1787711405213: "Its minuet is marked so fast it is really a scherzo, and the finale's theme is let out a few notes at a time in a teasing slow introduction.",
    1787711405214: "Its minuet is marked so fast it is really a scherzo, and the finale's theme is let out a few notes at a time in a teasing slow introduction.",
    1787711405225: "Schumann called it a slender Greek maiden between two Norse giants, the <i>Eroica</i> and the Fifth.",
    1787711405241: "Schumann called it a slender Greek maiden between two Norse giants, the <i>Eroica</i> and the Fifth.",
    1787711405018: "The four-note opening figure recurs across all four movements, and the scherzo runs without a break into the C-major finale.",
    1787711405246: "The four-note opening figure recurs across all four movements, and the scherzo runs without a break into the C-major finale.",
    1787711405235: "The shortest of his mature symphonies. Beethoven called it “my little symphony in F” and said it was less popular than the Seventh because it was so much better.",
    1787711405253: "The shortest of his mature symphonies. Beethoven called it “my little symphony in F” and said it was less popular than the Seventh because it was so much better.",
    1787711405276: "Written to thank Breslau for an honorary doctorate, and built from student drinking songs; Brahms called it a boisterous potpourri.",
    1787711405631: "Franck's only symphony, in three movements bound by cyclic themes; its slow movement doubles as the scherzo.",
    1787711405632: "Franck's only symphony, in three movements bound by cyclic themes; its slow movement doubles as the scherzo.",
    1787711405638: "Subtitled “The Poem of Fire”, it is scored for a colour organ (<i>luce</i>) meant to bathe the hall in coloured light.",
    1787711405601: "Grieg's only concerto, in A minor like Schumann's; Liszt played it at sight from the manuscript.",
    1787711405603: "Grieg's only concerto, in A minor like Schumann's; Liszt played it at sight from the manuscript.",
    1787711405613: "The third of Liszt's six Paganini studies, on the rondo of Paganini's Second Violin Concerto.",
    1787711405672: "Its cadenza comes before the recapitulation rather than after, and the three movements run without a break.",
    1787711405673: "Its cadenza comes before the recapitulation rather than after, and the three movements run without a break.",
    1787711405524: "Written at seventeen, a scene from Goethe's <i>Faust</i>; the spinning wheel stops when Gretchen remembers Faust's kiss.",
    1787711405440: "Commissioned by the French state; Berlioz said if he could burn all but one of his works, he would spare this.",
    1787711405442: "Commissioned by the French state; Berlioz said if he could burn all but one of his works, he would spare this.",
    1787711405488: "Grew out of a single-movement fantasy written for Clara Schumann, who premiered it; the whole first movement is built from the oboe's opening theme.",
    1787711405491: "Grew out of a single-movement fantasy written for Clara Schumann, who premiered it; the whole first movement is built from the oboe's opening theme.",
    1787711405715: "Dedicated to his patron Nadezhda von Meck, whom he never met; the third movement is played entirely <i>pizzicato</i>.",
    1787711405719: "Dedicated to his patron Nadezhda von Meck, whom he never met; the third movement is played entirely <i>pizzicato</i>.",
    1787711405785: "Six pieces with English titles for Debussy's daughter Chouchou, from “Doctor Gradus ad Parnassum” to “Golliwogg's Cakewalk”.",
    1787711405786: "Six pieces with English titles for Debussy's daughter Chouchou, from “Doctor Gradus ad Parnassum” to “Golliwogg's Cakewalk”.",
    1787711405902: "For piano, chorus, and orchestra, premiered in the four-hour, freezing 1808 concert that also gave the Fifth and Sixth symphonies.",
    1787711405914: "Written for Archduke Rudolph's installation as Archbishop of Olmütz, and finished three years too late. Beethoven headed the Kyrie “From the heart — may it go again to the heart!”",
    1787711405915: "Written for Archduke Rudolph's installation as Archbishop of Olmütz, and finished three years too late. Beethoven headed the Kyrie “From the heart — may it go again to the heart!”",
    1787711405936: "Beethoven's last piano concerto, written in 1809 while Vienna was under French bombardment; the nickname is not his, and he was too deaf to give the premiere.",
    1787711405937: "Beethoven's last piano concerto, written in 1809 while Vienna was under French bombardment; the nickname is not his, and he was too deaf to give the premiere.",
    1787711405999: "Haydn's last symphony, the final one of the twelve written for Johann Peter Salomon's London concerts; the finale is built on a tune said to be a Croatian folk song or a London street cry.",
    1787711406009: "A Singspiel in which Belmonte rescues Konstanze from the Pasha's harem, and the Pasha only speaks.",
    1787711406010: "A Singspiel in which Belmonte rescues Konstanze from the Pasha's harem, and the Pasha only speaks.",
    1787711406011: "A Singspiel with spoken dialogue, full of Masonic symbolism, premiered in a suburban Vienna theatre weeks before Mozart's death.",
    1787711406014: "A Singspiel with spoken dialogue, full of Masonic symbolism, premiered in a suburban Vienna theatre weeks before Mozart's death.",
    1787711406016: "A Singspiel with spoken dialogue, full of Masonic symbolism, premiered in a suburban Vienna theatre weeks before Mozart's death.",
    1787711406073: "One of only two symphonies he wrote in a minor key, both in G minor; he later revised it to add clarinets.",
    1787711406074: "One of only two symphonies he wrote in a minor key, both in G minor; he later revised it to add clarinets.",
    1787792906295: "A mass on the most-set secular tune of the Renaissance, a soldier's song used by more than forty composers.",
    1787792906297: "A motet for forty voices, probably written to answer an Italian forty-part work heard in London.",
    1787792906306: "Purcell's only true opera, with a libretto by Nahum Tate, perhaps first given at a girls' school in Chelsea.",
    1787792906308: "Twelve concertos published in 1714, after Corelli's death, that set the model for the concerto grosso; No. 8 is the “Christmas” Concerto.",
    1787792906335: "Twenty-one poems by Albert Giraud, in German translation, in three groups of seven; its ensemble of flute, clarinet, violin, cello, and piano is now called a “Pierrot ensemble”.",
    1787792906346: "Nine suites fusing Baroque counterpoint with Brazilian folk idiom; No. 5's Aria is the most famous thing Villa-Lobos wrote.",
    1787792906352: "Premiered in Cologne in 1958 under Stockhausen, Bruno Maderna, and Pierre Boulez; its tempi are derived from the overtone series.",
    1787792906356: "Commissioned by the New York Philharmonic for its 125th anniversary and premiered in 1967 under Seiji Ozawa.",
    1788199512131: "Mahler found its ending at Hans von Bülow's funeral on hearing Friedrich Klopstock's hymn “Aufersteh'n”. The first movement began as a separate tone poem, <i>Totenfeier</i>.",
    1788199512173: "Premiered in Munich in 1910 with over a thousand performers, hence its nickname; its second part sets the closing scene of Goethe's <i>Faust</i>.",
    1788199512174: "His last completed symphony, ending with an adagio that dies away to nothing; Alban Berg heard it as a farewell.",
    1788199512356: "Bruckner gave it its nickname himself, and the scherzo of the 1878 revision is a hunting scene.",
    1788199512401: "Bruckner called it the pride of his life and suggested it as a finale for his unfinished Ninth Symphony.",
    1788199512812: "Sibelius's only concerto, revised in 1905; Donald Tovey called its finale a “polonaise for polar bears”.",
    1788199512860: "One of the four Lemminkäinen Legends from the <i>Kalevala</i>: a swan glides on the black river around Tuonela, the land of the dead.",
    1788199513177: "Inspired by a black-and-white reproduction of Arnold Böcklin's painting; it quotes the Dies irae.",
    1788199513223: "Begun in Leningrad during the German siege; the score was microfilmed, flown out through Tehran, and played in the West as propaganda, and in 1942 the starving city's own orchestra performed it.",
    1788199513637: "Written for the Boston Symphony's fiftieth anniversary and dedicated “to the glory of God”; it sets Latin psalms.",
    1788199514200: "<i>Romeo and Juliet</i> moved to Manhattan gang turf, with lyrics by Stephen Sondheim and choreography by Jerome Robbins.",
    1788199514346: "Variations and fugue on a Purcell theme, written for an educational film; the closing fugue brings every instrument back in turn.",
    1788199514895: "Written in 1906 and subtitled “A Cosmic Landscape”; Leonard Bernstein borrowed its title for his Harvard lectures.",
    1788199514992: "Each movement portrays Concord Transcendentalists: “Emerson”, “Hawthorne”, “The Alcotts”, and “Thoreau”. One passage calls for a board to press down clusters.",
    1788199515115: "Vaughan Williams's first symphony, for soloists, chorus, and orchestra, on poems by Walt Whitman.",
    1788199515205: "An elegiac work written after the First World War; Jacqueline du Pré's 1965 recording made it famous.",
    1788199515350: "After Walter Scott: forced to marry another man, Lucia kills her husband on the wedding night and appears before the guests in her bloodstained nightgown.",
    1788199516179: "A guitar concerto named for a Bourbon palace garden; Rodrigo, blind from the age of three, wrote it in 1939.",
    1788199516364: "Modelled on the slow Spanish court dance, with an optional chorus added later on verses by Robert de Montesquiou.",
    1788199516592: "Poulenc's opera after Georges Bernanos on the sixteen Carmelite nuns of Compiègne guillotined in 1794; the fearful Blanche de la Force walks out to die last.",
    1788199516777: "A piano rondo Weber dedicated to his wife; Berlioz orchestrated it, and it became the music of the ballet <i>Le Spectre de la rose</i>.",
    1788199516836: "Written without bar lines or time signatures, with whimsical directions to the player such as <i>très luisant</i> (“very shiny”); the title is Satie's own coinage.",
    1788199516866: "A four-minute fanfare; Adams likened it to a ride in a terrific sports car that you wish you hadn't taken.",
    1788199516868: "A slow piece for violin (or cello) and piano in Pärt's tintinnabuli style, written in 1978 just before he left Estonia; the title means “mirror in the mirror”.",
    1788199516902: "A tintinnabuli piece of 1977 that Pärt has arranged for many ensembles, from string quartet to violin and piano; the title means “brothers”.",
    1788199516988: "A Romantic showpiece by a Polish virtuoso who wrote it for himself, dedicated to Pablo de Sarasate.",
    1788489953141: "A servant is condemned to death for a theft actually committed by a magpie.",
    1788489953149: "A girl raised by a regiment of French soldiers falls for a Tyrolean peasant, who joins the regiment to win her.",
    1788489953162: "Verdi's last opera, written at seventy-nine after Shakespeare's <i>The Merry Wives of Windsor</i> and <i>Henry IV</i>, and only his second comedy.",
    1788489953227: "Brecht and Weill's reworking of <i>The Beggar's Opera</i>, opening with the Ballad of Mack the Knife; it ran for years in Berlin until the Nazis banned it.",
    1788489953292: "After Henry James's ghost story: a governess fights the ghosts of Peter Quint and Miss Jessel for the two children in her care.",
    1788489953293: "Britten and Peter Pears cut Shakespeare's text to a libretto, keeping almost only his words; Puck is a speaking acrobat.",
    1788489953374: "A suite from Kodály's opera about a veteran hussar's tall tales, among them beating Napoleon single-handed.",
}

# clues that nearly named their answer (the description on the back may name it)
CLUE = {
    1787711405480: "Eight fantasies named after E. T. A. Hoffmann's mad bandmaster and dedicated to Chopin; Schumann wrote them in a few days while in love with Clara Wieck.",
    1788199513969: "After an unfinished play by Georg Büchner: a poor soldier, bullied by his Captain and experimented on by a Doctor, murders his lover Marie. Every scene is built on a closed form, such as a passacaglia or a suite.",
    1787711405506: "Its slow movement is variations on one of Schubert's own songs, and all four movements are in minor keys. Written in 1824, after he knew his illness was serious.",
    1787711405521: "Schubert set Goethe's ballad at eighteen: one singer voices narrator, father, son, and a supernatural seducer over relentless piano triplets, which stop dead before the last line, “the child was dead”.",
    1787711405408: "The prologue to Wagner's <i>Ring</i>: Alberich steals the Rhinemaidens' treasure and forges the ring, which Wotan takes from him. It opens on an E-flat chord held for 136 bars.",
    1788489953353: "Hindemith's hero is the painter of the Isenheim Altarpiece, torn between art and the Peasants' War. The Nazis banned it, prompting Wilhelm Furtwängler's public defence and Hindemith's exile.",
    1788199511994: "Handel's most successful opera for London, on a Roman general and an Egyptian queen; the castrato Senesino created the title role, and the queen seduces him with the aria “V'adoro, pupille”.",
    1787792906346: "Nine suites fusing Baroque counterpoint with Brazilian folk idiom. No. 5 is for soprano and eight cellos, its wordless <i>vocalise</i> the most famous thing Villa-Lobos wrote.",
    1788199515491: "Among the first operas, premiered at the Mantuan court in 1607 with a libretto by Alessandro Striggio; it opens with a trumpet toccata, and the singer-hero's plea “Possente spirto” lulls the ferryman Charon.",
}

MOVEMENT = {
    1787711405007: "“O Sacred Head, Now Wounded”",
    1787711405027: "“Habanera”",
    1787711405045: "<i>Simple Gifts</i>",
    1787711405052: "“Flower Duet”",
    1787711405097: "Act II · <i>Méditation</i>",
    1787711405125: "“Barcarolle”",
    1787711405132: "Act III · “Nessun dorma”",
    1787711405192: "Act II · Triumphal March",
    1787711405193: "Act II · “Anvil Chorus”",
    1787711405194: "Act I · “Libiamo ne' lieti calici”",
    1787711405196: "Act III · “La donna è mobile”",
    1787711405203: "Act III · “Bridal Chorus”",
    1787711405204: "Prelude to Act III",
    1787711405206: "Act III · “Liebestod”",
    1787711405409: "Act III · Dance of the Apprentices",
    1787711405411: "“Winterstürme wichen dem Wonnemond”",
    1787711405412: "“Steuermann, lass die Wacht”",
    1787711405415: "Act III · Siegfried's Funeral March",
    1787711405424: "“Hoho! Hoho! Hohei!”",
    1787711405429: "“Pilgrims' Chorus”",
    1787711405469: "“Ich grolle nicht”",
    1787711405470: "“Die alten, bösen Lieder”",
    1787711405517: "“Das Wandern”",
    1787711405518: "“Der Müller und der Bach”",
    1787711405554: "“Der Leiermann” (“The Hurdy-Gurdy Man”)",
    1787711405555: "“Der Lindenbaum” (“The Linden Tree”)",
    1787711405642: "“For the mountains shall depart”",
    1787711405691: "Act II · “Un bel dì, vedremo”",
    1787711405693: "Act I · Te Deum",
    1787711405694: "Act II · “Vissi d'arte”",
    1787711405696: "Act III · “E lucevan le stelle”",
    1787711405764: "Act III · “Fuggiam gli ardori inospiti”",
    1787711405766: "“La nuit calme”",
    1787711405773: "“Va, pensiero”",
    1787711405774: "Act II · “Credo in un Dio crudel”",
    1787711405780: "Act I · “Zitti, zitti”",
    1787711405912: "“Prisoners' Chorus”",
    1787711405960: "“By Thee with Bliss”",
    1787711406008: "Act I · “Un'aura amorosa”",
    1787711406009: "“Chorus of the Janissaries”",
    1787711406011: "“Der Vogelfänger bin ich ja”",
    1787711406016: "Act II · “Der Hölle Rache” (Queen of the Night)",
    1787711406019: "“Champagne Aria”",
    1787711406033: "Act II · “Fuor del mar”",
    1787711406036: "“Non più andrai”",
    1787711406083: "Act III · “Che farò senza Euridice?”",
    1787711406084: "Act III · “Che fiero momento”",
    1787792906306: "Act III · Dido's Lament, “When I am laid in earth”",
    1788199514251: "“Glitter and Be Gay”",
    1788199514801: "“Summertime”",
    1788199515350: "Mad Scene, “Il dolce suono”",
    1788199515398: "Act II · “Una furtiva lagrima”",
    1788199515443: "Act I · “Casta diva”",
    1788199515491: "Act III · “Possente spirto”",
    1788199515538: "Act III · “Pur ti miro”",
    1788199515912: "“Vesti la giubba”",
    1788199516865: "“News has a kind of mystery”",
    1788489953112: "Act I · “Parto, parto”",
    1788489953140: "Act II · “Non più mesta”",
    1788489953149: "“Ah! mes amis” (nine high Cs)",
    1788489953159: "Act III · “Eri tu”",
    1788489953161: "“Ella giammai m'amò”",
    1788489953162: "“Tutto nel mondo è burla”",
    1788489953168: "“Le veau d'or”",
    1788489953181: "“Song to the Moon”",
    1788489953197: "Act III · “Gavotte”",
    1788489953317: "Act I · “Must the Winter Come So Soon”",
    1788489953321: "“Hymn to the Sun”",
}

NICK = {
    1788585500503: "Holst's <i>Mars</i> and Orff's “O Fortuna” both lean on one.",
    1788585501251: "Wagner's <i>Ring</i> is built from them; the parallel device in Hector Berlioz is the <i>idée fixe</i>.",
}

# concept note -> (clip taken from this note, new "Heard in" or None to keep it)
CONCEPT_AUDIO = {
    1790448081465: (1787711405812, None),                         # Flute: Debussy's Syrinx
    1790448081490: (1787711405103, None),                         # Clarinet: Mozart's Clarinet Concerto
    1790448081521: (1787711406001, None),                         # Trumpet: Haydn's Trumpet Concerto
    1790448081552: (1787711405201, None),                         # Violin: The Four Seasons
    1790448081583: (1787711405039, None),                         # Piano: Chopin's nocturnes
    1790448081614: (1787711405004, None),                         # Cello: Bach's cello suites
    1790448081654: (1787711405874, None),                         # Saxophone: "The Old Castle"
    1790448081685: (1787711405431, None),                         # Viola: Harold en Italie
    1790448081749: (1787711406031, None),                         # French horn: Mozart's horn concertos
    1790448081779: (1787711406059, None),                         # Trombone: "Tuba mirum"
    1790448081873: (1788199516179, None),                         # Guitar: Concierto de Aranjuez
    1790448081902: (1788199511656, None),                         # Harpsichord: Goldberg Variations
    1790448081933: (1787711405008, None),                         # Organ: Toccata and Fugue
    1790448081993: (1787792906322, None),                         # String quartet: Op. 131
    1790448082025: (1787711405672, None),                         # Concerto: Mendelssohn's Violin Concerto
    1790448082056: (1787711405165, None),                         # Waltz: The Blue Danube
    1790448082089: (1788199511557, None),                         # Mass: Mass in B minor
    1790448082118: (1787711405018, None),                         # Symphony: Beethoven's Fifth
    1790448082148: (1787711405923, None),                         # Sonata: Moonlight
    1790448082525: (1787711405998, None),                         # Timpani: the Drumroll
    1790448082588: (1787711405890, None),                         # Piano trio: the Archduke
    1790448082619: (1787711405125, None),                         # Barcarolle: The Tales of Hoffmann
    1790365377131: (1787711405679, None),                         # Aria: Gianni Schicchi
    1790365377157: (1787711405025, None),                         # Dies irae: Symphonie fantastique
    1790365377197: (1788489953164, None),                         # Tristan chord: the Prelude
    1790365377774: (1788489953211, None),                         # Operetta: The Merry Widow
    1790365377803: (1788489953338, None),                         # Intermezzo: La serva padrona
    1790365377834: (1787711405075, None),                         # Incidental music: Peer Gynt
    1790365377864: (1787711405081, None),                         # Suite: Water Music
    1790365377897: (1787711406023, None),                         # Serenade: Eine kleine Nachtmusik
    1790365378258: (1787711405365, None),                         # Cor anglais: Dvorak 9 Largo
    1790365378285: (1787711405175, None),                         # Celesta: the Sugar Plum Fairy
}

TPL_FRONT_OLD = '<div class="cm2-eyebrow">Work</div>\n<div class="cm2-def">{{Clue}}</div>\n<div class="cm2-ask">Work?</div>'
TPL_FRONT_NEW = '<div class="cm2-eyebrow">Piece</div>\n<div class="cm2-def">{{Clue}}</div>\n<div class="cm2-ask">Title?</div>'
TPL_BACK_OLD = '{{#Clue}}<div class="cm2">\n<div class="cm2-eyebrow">Work</div>'
TPL_BACK_NEW = '{{#Clue}}<div class="cm2">\n<div class="cm2-eyebrow">Piece</div>'
CSS_ADD = """
/* 2026-09-29: more room between the clip (or its Listen box) and the title under it (Carter, Beethoven 9 scherzo) */
.cm2 .cm2-audio + .cm2-work, .cm2 .cm2-listen + .cm2-work { margin-top: 36px; }
"""


def ring_italics(s):
    s = re.sub(r"(?<![>\w])Ring(?=[:,.;\s])(?![^<]*</i>)", "<i>Ring</i>", s)
    return s


def main(apply):
    ids = C.anki("findNotes", query='note:"Classical Music"')
    notes = {}
    for i in range(0, len(ids), 400):
        for n in C.anki("notesInfo", notes=ids[i:i + 400]):
            notes[n["noteId"]] = n
    changes, backup = {}, {}

    def put(nid, field, val):
        n = notes[nid]
        if n["fields"][field]["value"] != val:
            changes.setdefault(nid, {})[field] = val

    for nid, v in LISTEN.items():
        put(nid, "Listen", v)
    for nid, v in DESC.items():
        f = notes[nid]["fields"]
        if f["Clue"]["value"].strip() and f["Clue"]["value"] == f["Description"]["value"] and nid not in CLUE:
            put(nid, "Clue", v)
        put(nid, "Description", v)
    for nid, v in CLUE.items():
        put(nid, "Clue", v)
    for nid, v in MOVEMENT.items():
        put(nid, "Movement", v)
    for nid, v in NICK.items():
        put(nid, "Nickname", v)
    col = notes[1788585501777]["fields"]["Nickname"]["value"]
    put(1788585501777, "Nickname", col.replace("Holst's Mars", "Holst's <i>Mars</i>"))
    # the Ring in Wagner notes
    for nid, n in notes.items():
        if "Wagner" not in n["fields"]["Composer"]["value"]:
            continue
        for field in ("Description", "Clue"):
            cur = changes.get(nid, {}).get(field, n["fields"][field]["value"])
            new = ring_italics(cur)
            if new != cur:
                put(nid, field, new)
    for nid, (src, heard) in CONCEPT_AUDIO.items():
        au = notes[src]["fields"]["Audio"]["value"]
        m = re.search(r"\[sound:[^\]]+\]", au)
        assert m, (nid, src)
        if not notes[nid]["fields"]["Audio"]["value"].strip():
            put(nid, "Audio", m.group(0))
        if heard:
            put(nid, "Composer", heard)
    for nid, fields in changes.items():
        backup[nid] = {k: notes[nid]["fields"][k]["value"] for k in fields}
    print(len(changes), "notes,", sum(len(v) for v in changes.values()), "fields")
    for nid, fields in list(changes.items()):
        for k, v in fields.items():
            print("  %s %-14s %-10s %s" % (nid, C.plain(notes[nid]["fields"]["Work"]["value"])[:14], k, C.plain(v)[:110]))
    t = C.anki("modelTemplates", modelName="Classical Music")
    tpl = t["DESCRIPTION to WORK"]
    new_tpl = {"Front": tpl["Front"].replace(TPL_FRONT_OLD, TPL_FRONT_NEW), "Back": tpl["Back"].replace(TPL_BACK_OLD, TPL_BACK_NEW)}
    print("template front changed:", new_tpl["Front"] != tpl["Front"], "| back changed:", new_tpl["Back"] != tpl["Back"])
    css = C.anki("modelStyling", modelName="Classical Music")["css"]
    if not apply:
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump(backup, open(os.path.join(HERE, "backups", "cm_text_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"templates": t, "css": css}, open(os.path.join(HERE, "templates_backup", "cm_before_%s.json" % stamp), "w", encoding="utf-8"),
              ensure_ascii=False)
    for nid, fields in changes.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": fields})
    if new_tpl != {"Front": tpl["Front"], "Back": tpl["Back"]}:
        C.anki("updateModelTemplates", model={"name": "Classical Music", "templates": {"DESCRIPTION to WORK": new_tpl}})
    if "cm2-listen + .cm2-work" not in css:
        C.anki("updateModelStyling", model={"name": "Classical Music", "css": css + CSS_ADD})
    print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
