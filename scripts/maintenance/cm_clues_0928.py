# -*- coding: utf-8 -*-
"""cm_clues_0928.py -- DESCRIPTION to WORK clues for every active tier-1 Music work.

Carter asked (2026-09-28) what the "description to work" cards were. They show a description and
ask for the work, but only 190 active works had one, and the clue was the description with the
title's words blanked out ("The ____, begun during the siege..."), which reads as broken.

Now every active tier-1 work (358) has exactly one such card, on its lowest-id active note:
  * the clue is the work's Description (as corrected by cm_desc_0928.py) wherever that names
    nothing in the title or nickname (276 works);
  * 82 descriptions give the answer away; each gets its own clue below, written from the same
    facts without the title's distinctive words or the nickname.
No clue contains "____". Clues on any other note of a work are cleared, so a work never has two.

    py -3.9 cm_clues_0928.py [--apply]
"""
import json, re, sys, time
import concept_add as C
import qb_tier_model as T

CLUE = {
 1787711405014: "Beethoven marked this C-sharp-minor sonata <i>quasi una fantasia</i>: it opens with a slow movement of unbroken triplets instead of a fast one and ends with a furious <i>presto</i>. The critic Ludwig Rellstab gave it its nickname, five years after Beethoven's death.",
 1787711405037: "Chopin's B-flat-minor sonata of 1839, whose third movement is the most famous dirge ever written; the finale is a minute and a half of whispered unison that Schumann found baffling.",
 1787711405041: "A Chopin concert dance in A-flat major and triple time, from 1842, whose trio is built on thundering left-hand octaves; its nickname is not Chopin's.",
 1787711405046: "Written by Aaron Copland in 1942 for brass and percussion, after a wartime speech by Vice President Henry Wallace; Copland reused it in the finale of his Third Symphony.",
 1787711405055: "Paul Dukas's tone poem after Goethe's ballad about a boy who enchants a broom to fetch water and cannot stop it; Mickey Mouse plays the boy in Disney's <i>Fantasia</i>.",
 1787711405062: "Fourteen musical portraits of Edward Elgar's friends, each headed by initials; the ninth depicts his publisher August Jaeger, and Elgar claimed a larger unheard theme runs through the whole.",
 1787711405066: "George Gershwin's tone poem with real taxi horns, which he brought back from France, blending a blues with a French promenade; later the basis of a Gene Kelly film.",
 1787711405081: "Three suites played by an orchestra on a barge following George I up the Thames in 1717; the king is said to have had them repeated three times. Handel.",
 1787711405098: "Felix Mendelssohn's concert overture from a visit to the Scottish island of Staffa and its basalt sea grotto; he sent the opening bars home in a letter the same day.",
 1787711405648: "Eight books of short lyrical piano pieces by Felix Mendelssohn, each a melody over an accompaniment; he resisted attaching titles, insisting that music says things more precisely than language can.",
 1787711405115: "A Mozart sonata in which no movement is in sonata form: it opens with a theme and variations in siciliana rhythm and ends with a finale imitating a Turkish janissary band.",
 1787711405120: "Modest Mussorgsky's piano suite after a memorial show of Viktor Hartmann's drawings, with a recurring <i>Promenade</i> for the viewer walking between them; Ravel's orchestration is standard.",
 1787711405123: "Jacques Offenbach's parody of Greek myth and of Second Empire society, in which Public Opinion forces a musician to fetch back a wife he is glad to be rid of; its “Infernal Galop” is the tune of the can-can.",
 1787711405125: "Jacques Offenbach's last work, left unfinished at his death: a poet tells of three lost loves, the mechanical doll Olympia, the singer Antonia, and the courtesan Giulietta. Its <i>Barcarolle</i> is the best-known number.",
 1787711405127: "Johann Pachelbel's piece for three violins in strict imitation over a two-bar ground bass repeated twenty-eight times; long forgotten, it became a wedding staple after a 1968 recording.",
 1787711405137: "Sergei Rachmaninoff's twenty-four variations for piano and orchestra on the last of the Caprices for solo violin; the eighteenth turns the tune upside down into a lush D-flat melody.",
 1787711405139: "Ottorino Respighi's tone poem in four scenes of trees in the Italian capital: the third calls for a recording of a nightingale, and the last marches a legion up the Appian Way.",
 1787711405141: "Rimsky-Korsakov's opera after Pushkin's verse fairy story, in which Prince Gvidon is turned into a bumblebee to visit his father; that scene is “Flight of the Bumblebee”.",
 1787711405153: "Dedicated to the memory of Liszt, who died weeks after its 1886 London premiere, Saint-Saëns's C-minor symphony is laid out in two large parts and adds piano four hands and a keyboard instrument whose blazing C-major chord launches the finale.",
 1787711405206: "Opens with a chord that never resolves, often called the start of modern harmony, and ends with a <i>Liebestod</i>; the tenor who created the hero died weeks after the 1865 premiere. Wagner wrote it while in love with Mathilde Wesendonck.",
 1787711405306: "Brahms set scripture he chose himself, in his own language rather than Latin, and never mentions Christ; the fifth movement, for soprano, was added after the premiere, and the first has no violins.",
 1787711405381: "Dvořák wrote this F-major string quartet in three days in the Czech community of Spillville, Iowa; its tunes are pentatonic, and the third movement takes a birdcall from the scarlet tanager.",
 1787711405394: "Nikolai Rimsky-Korsakov's concert overture on Orthodox chants, moving from the solemnity of Holy Week to the bells and rejoicing of the resurrection morning.",
 1787711405421: "Wagner's last opera, a “festival play for the consecration of the stage”: an innocent fool heals the wounded Grail king Amfortas with the spear that wounded him. Bayreuth long kept it to itself.",
 1787711405423: "Wagner's early grand opera on a fourteenth-century Roman tribune; its 1842 success in Dresden launched his career, and its overture opens with a long, sustained trumpet note.",
 1787711405424: "The third part of Wagner's Ring: the hero reforges the sword Nothung, kills the dragon Fafner, understands the Woodbird's song, and wakes Brünnhilde on her fiery rock.",
 1787711405522: "Four linked movements for solo piano, all on a theme from one of Schubert's songs about a traveller; so difficult that Schubert broke down playing it and said the devil could play it.",
 1787711405524: "Schubert set this scene from Goethe's <i>Faust</i> at seventeen: the piano's whirring right hand is a spinning wheel, which stops when the heroine remembers Faust's kiss.",
 1787711405544: "The only one of Schubert's string quartets published in his lifetime; its A-minor first movement opens over a murmuring second violin, and its slow movement borrows an entr'acte from his incidental music to a play by Helmina von Chézy.",
 1787711405549: "Schumann found this C-major symphony among the papers of Schubert's brother Ferdinand ten years after Schubert's death; Mendelssohn premiered it, and Schumann praised its “heavenly length”. It opens with unaccompanied horns.",
 1787711405613: "Franz Liszt's study on the bell-rondo finale of a B-minor violin concerto by the Genoese virtuoso whose caprices he also transcribed; the right hand leaps constantly across more than two octaves.",
 1787711405690: "The 1904 La Scala premiere of this Puccini opera was a fiasco; revised, it became a staple. A Nagasaki geisha waits through the night, while an offstage chorus hums, for the American naval officer who married her.",
 1787711405693: "A Puccini melodrama set in real Roman locations: a singer stabs the police chief Scarpia, her lover's mock execution proves real, and she throws herself from the Castel Sant'Angelo.",
 1787711405734: "Tchaikovsky's opera after Pushkin's verse novel: a bored dandy rejects Tatiana's letter, kills his friend Lensky in a duel, and years later is rejected by her in turn.",
 1787711405801: "Debussy's only completed opera, an almost word-for-word setting of Maurice Maeterlinck's Symbolist play: Golaud finds a mysterious girl weeping by a spring in the forest, marries her, and kills his half-brother out of jealousy.",
 1787711405905: "A Viennese publisher sent his trivial waltz to fifty composers for one variation each; Beethoven refused, then wrote thirty-three, including a parody of Leporello's “Notte e giorno faticar” from <i>Don Giovanni</i>.",
 1787711405912: "Beethoven's only opera: Leonore disguises herself as a young man to rescue her husband Florestan from a political prison, and the prisoners' chorus greets the daylight. He wrote four overtures for it.",
 1787711405926: "Beethoven dedicated this C-major sonata to his first patron in Bonn. A short slow <i>Introduzione</i> leads into the finale; it replaced a longer middle movement, published separately as the <i>Andante favori</i>.",
 1787711405955: "Beethoven wrote this A-major sonata for the violinist George Bridgetower, then dedicated it to a French violinist who never played it; it gave Leo Tolstoy the title of a novella.",
 1787711405959: "Haydn's second great oratorio, after James Thomson's poem, following country life through the year from spring to winter; Haydn himself found some of its nature painting trivial.",
 1787711405999: "Haydn's last symphony, the final one of the twelve written for Johann Peter Salomon's concerts. It opens with a stern D-minor fanfare, and the finale is built on a tune said to be a Croatian folk song or a street cry.",
 1787711406070: "Made from a serenade Mozart wrote in 1782 for the ennoblement of a Salzburg family friend, then reworked for Vienna as a D-major symphony with flutes and clarinets added.",
 1787711406083: "Gluck's first “reform” opera, with the librettist Ranieri de' Calzabigi, stripping away <i>da capo</i> display in favour of drama; the hero, written for the castrato Gaetano Guadagni, sings the lament “Che farò”.",
 1787792906306: "Purcell's only true opera, with a libretto by Nahum Tate, perhaps first given at a girls' school in Chelsea; the Carthaginian queen's lament “When I am laid in earth” is sung over a descending chromatic ground bass.",
 1787792906308: "Twelve concertos by Arcangelo Corelli, published in 1714 after his death, that set a solo trio of two violins and cello against the full string band; No. 8 was written for Christmas night.",
 1787792906309: "Over two hundred works for harpsichord by François Couperin, grouped into <i>ordres</i> and given descriptive titles rather than dance names; Couperin was called <i>le Grand</i>.",
 1787792906326: "Four operas on the curse of a gold band forged from the Rhine gold, woven from leitmotifs; the whole tetralogy was first staged at Wagner's Bayreuth Festspielhaus in 1876.",
 1787792906335: "Twenty-one poems by Albert Giraud, in German translation, set by Schoenberg for a reciter in <i>Sprechstimme</i> and five players; its ensemble of flute, clarinet, violin, cello, and piano is named after the work.",
 1788199511863: "A comic secular cantata by Bach, first performed at Zimmermann's café in Leipzig: a father tries to cure his daughter Lieschen of her addiction to the drink.",
 1788199512089: "Mahler first called it a tone poem and briefly named it after a Jean Paul novel. Its third movement turns <i>Frère Jacques</i> into a minor-key funeral march led by a solo double bass; the gentle <i>Blumine</i> movement was cut after early performances.",
 1788199512173: "Mahler scored it for eight soloists, double chorus, boys' choir, and an enormous orchestra, and premiered it in Munich in 1910 with a vast array of performers. It sets the hymn <i>Veni creator spiritus</i> and the closing scene of Goethe's <i>Faust</i>.",
 1788199512401: "Bruckner called it the pride of his life and suggested it as a finale for his unfinished Ninth Symphony; it opens with a relentless C-major string figure under the choir's unison Latin hymn of praise.",
 1788199512490: "Richard Strauss's opera after Oscar Wilde, in which a princess performs the Dance of the Seven Veils and then sings to the Baptist's severed head; Mahler could not get it past the Vienna censor.",
 1788199512531: "Richard Strauss's first opera with Hugo von Hofmannsthal, after Sophocles: Agamemnon's daughter waits to avenge her father, and her recognition of her brother Orest is its emotional heart.",
 1788199512713: "Richard Strauss's tone poem in which a dying artist relives his life before his soul is released. Sixty years later he quoted its final theme at the close of “Im Abendrot”, the last of his <i>Four Last Songs</i>.",
 1788199512860: "One of Sibelius's four Lemminkäinen Legends from the <i>Kalevala</i>: a bird glides on the black river around the land of the dead, voiced by a <i>cor anglais</i>.",
 1788199513223: "Shostakovich began it during the German siege of his home city; the score was microfilmed, flown out through Tehran, and played in the West as propaganda. Its first movement builds an invasion theme over a snare-drum <i>ostinato</i>.",
 1788199513545: "Prokofiev's opera after Carlo Gozzi's fairy-tale play: a prince who cannot laugh is cursed to fall for three pieces of fruit and must find them. Its March became a concert favourite.",
 1788199513596: "Stravinsky's ballet in which a puppet comes to life at a Shrovetide fair in St Petersburg; its signature chord superimposes C major and F-sharp major, and it began as a concert piece for piano.",
 1788199513637: "Written for the Boston Symphony's fiftieth anniversary, Stravinsky's choral symphony sets Latin texts from the Vulgate for chorus and an orchestra with no violins, violas, or clarinets.",
 1788199513869: "Bartók's only opera: Judith opens seven doors in her new husband's home, each lit by its own orchestral colour; behind the seventh are his previous wives, alive.",
 1788199513970: "Alban Berg's last completed work, dedicated to Manon Gropius, the daughter of Alma Mahler, who died at eighteen; its tone row ends with the rising whole tones of Bach's chorale “Es ist genug”, which is quoted in the finale.",
 1788199513971: "Alban Berg's second opera, after Frank Wedekind's plays; he died leaving the third act unorchestrated, and Friedrich Cerha completed it in 1979. Its <i>femme fatale</i> ends murdered by Jack the Ripper.",
 1788199514610: "Aaron Copland's ballet for Lincoln Kirstein's Ballet Caravan, choreographed by Eugene Loring, on a young outlaw finally shot by Pat Garrett; it quotes cowboy songs such as “Git Along, Little Dogies”.",
 1788199514661: "A narrator reads from a president's speeches and letters, ending with the Gettysburg Address, over Aaron Copland's music quoting “Camptown Races” and the folk song “Springfield Mountain”.",
 1788199514801: "Gershwin's “American folk opera” after DuBose Heyward's novel, set in Catfish Row in Charleston with an all-Black cast; “Summertime” is Clara's lullaby.",
 1788199514895: "Charles Ives sets three layers at once: quiet strings for the silences of the druids, a trumpet posing the same atonal phrase seven times, and woodwinds growing more frantic in reply.",
 1788199514992: "Each movement of this Charles Ives piano sonata portrays a Transcendentalist of one Massachusetts town: “Emerson”, “Hawthorne”, “The Alcotts”, and “Thoreau”. One passage calls for a board to press down clusters.",
 1788199515071: "Ralph Vaughan Williams's work for a string quartet and two string orchestras of different sizes, on a psalm tune by a Tudor composer; it premiered in Gloucester Cathedral in 1910.",
 1788199515350: "Donizetti's opera after Walter Scott: the mad scene was written with glass harmonica, now usually played on flute, and ends with the heroine hallucinating her wedding after murdering her husband.",
 1788199515538: "Monteverdi's last opera, in which Nero's scheming mistress becomes empress while virtue goes unrewarded; its closing duet “Pur ti miro” may be by another composer.",
 1788199516746: "Edvard Grieg's suite for the bicentenary of the Danish-Norwegian playwright born in Bergen in 1684; it recasts Baroque dances, Praeludium, Sarabande, Gavotte, Air, and Rigaudon, in Romantic string writing.",
 1788199516865: "John Adams's opera on a president's 1972 visit to Mao, with a libretto by Alice Goodman and direction by Peter Sellars; the president sings “News has a kind of mystery” as he steps off Air Force One.",
 1788199516866: "A four-minute fanfare by John Adams over a relentless woodblock pulse; he likened it to being taken for a spin in a terrific sports car and wishing you hadn't.",
 1788199516961: "Samuel Barber's setting for soprano of James Agee's prose-poem about an evening in his Tennessee childhood, later the prologue to his novel <i>A Death in the Family</i>.",
 1788489953149: "Donizetti's comic opera about a girl raised by French soldiers, containing the tenor aria <i>Ah! mes amis</i> with nine high Cs, which made Pavarotti's reputation.",
 1788489953167: "Ambroise Thomas's French grand opera after Shakespeare, in which the Danish prince survives to be crowned; Ophelia's mad scene is its coloratura showpiece, and it was among the first operas to use a saxophone.",
 1788489953177: "Gilbert and Sullivan premiered it in New York to secure the American copyright, after <i>Pinafore</i> had been copied without payment; its Cornish hero is apprenticed to buccaneers by mistake.",
 1788489953262: "Virgil Thomson's opera to a Gertrude Stein libretto that makes little narrative sense, with more holy figures than its title promises; the 1934 premiere used an all-Black cast and cellophane sets.",
 1788489953292: "Britten's chamber opera after Henry James's ghost story, built as a theme and fifteen variations, one between each scene, rising a step at a time as the tension tightens.",
 1788489953295: "Britten's last opera, after Thomas Mann: Aschenbach's thoughts are set as accompanied recitative at the piano, and one baritone sings all seven figures who lure him toward his end.",
 1788489953334: "John Blow's masque for Charles II's court, usually called the first English opera, in which the king's mistress sang the goddess of love and their daughter played Cupid.",
}

STOP = set("the and for with from der die das des dem den von und les del della di da la le el los las une op no in of on a an to at".split())


def words(s):
    out = set()
    for t in re.split(r"[^\w'’-]+", C.plain(s)):
        f = C.fold(t)
        if len(f) > 3 and f not in T.GENERIC_MUSIC and f not in STOP and not f.isdigit():
            out.add(f)
    return out


def leak(work, nick, text):
    t = C.fold(C.plain(text))
    hits = [w for w in words(work) | words(nick) if re.search(r"\b%s" % re.escape(w[:-1] if w.endswith("s") else w), t)]
    if nick and C.fold(C.plain(nick)) in t:
        hits.append(nick)
    return hits


def P(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").strip()


def plan():
    ids = C.anki("findNotes", query='"note:Classical Music" -Kind:_*')
    ns = C.anki("notesInfo", notes=ids)
    q = {c["cardId"]: c["queue"] for c in C.anki("cardsInfo", cards=[c for n in ns for c in n["cards"]])}
    works = {}
    for n in ns:
        works.setdefault((P(n["fields"]["Work"]["value"]), n["fields"]["Composer"]["value"]), []).append(n)
    ch, bad = [], []
    for key, lst in works.items():
        cand = sorted([n for n in lst if "Music::tier::tier1-core" in n["tags"] and any(q[c] != -1 for c in n["cards"])],
                      key=lambda n: n["noteId"])
        keep = cand[0]["noteId"] if cand else None
        for n in lst:
            cur = n["fields"]["Clue"]["value"]
            if n["noteId"] != keep:
                if cur:
                    ch.append((n, ""))
                continue
            clue = CLUE.get(keep) or n["fields"]["Description"]["value"]
            h = leak(key[0], n["fields"]["Nickname"]["value"], clue)
            if h or "____" in clue or not clue.strip():
                bad.append((keep, key, h))
                continue
            if cur != clue:
                ch.append((n, clue))
    return ch, bad


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch, bad = plan()
    for b in bad:
        print("LEAK/EMPTY", b)
    print("set", sum(1 for n, c in ch if c), "| cleared", sum(1 for n, c in ch if not c), "| unresolved", len(bad))
    if "--apply" in sys.argv and not bad:
        json.dump([{"nid": n["noteId"], "Clue": n["fields"]["Clue"]["value"]} for n, c in ch],
                  open("backups/cm_clues_0928_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, c in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": {"Clue": c}})
        print("applied")
