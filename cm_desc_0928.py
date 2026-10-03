# -*- coding: utf-8 -*-
"""cm_desc_0928.py -- Music descriptions and Listen lines, corrected after reading all 358 works.

Carter, 2026-09-28: the Waldstein "starts with 'The Waldstein'"; Stamitz's "listen for field calls
it an early Mannheim symphony, detail calls it a late Mannheim symphony"; tier-1 cards missing
their description. Every active work's Description and Listen line was then read against the
others and against what is known of the piece. Fixed here:

  * 27 descriptions that opened by restating the nickname ("The Pastoral, in five movements ...")
    now open with a fact; the nickname appears later only where it explains something.
  * Wrong facts: Chopin's Op. 10 No. 12 carried the Black Key étude's description (it is the
    Revolutionary, a left-hand study); Op. 64 No. 1 was called the posthumous "Farewell" waltz
    (it is the Minute Waltz, published 1847 for Countess Delfina Potocka); Schubert set Erlkönig
    at eighteen, not seventeen; Largo al factotum is Figaro's entrance, not the opera's opening;
    the Micrologus did not introduce ut-re-mi (Guido's letter Epistola de ignoto cantu did);
    Prokofiev's Romeo and Juliet was rejected by the Bolshoi; Strauss quoted Tod und Verklärung
    in Im Abendrot, not "on his deathbed"; Brahms 4's passacaglia is thirty variations; the
    Rosenkavalier trio is for three women's voices (Octavian is a mezzo); Fauré quoted someone
    else's "lullaby of death".
  * Unclear or overstated: Stamitz (late in his life, early in the Mannheim school), Brahms 1's
    unexplained "comparison", Beethoven 4's "slow introduction is in the dark", Beethoven 8 as
    "his own favourite", the Ninth as "the first symphony to use voices", Mahler 5's Death in
    Venice (the Visconti film, not Britten's opera, which is also in the deck).
  * Oxford commas (Debussy's Nocturnes, Peer Gynt, William Tell), and five notes whose sibling
    movement had a description while they had none.
  * Listen lines: Hamlet and Der Freischütz had none (identified from spectrograms: a coloratura
    soprano; the overture's slow horn chorale); La bohème and Madama Butterfly had one generic
    line pasted on both clips; the Verdi Requiem's Lacrymosa carried the Dies irae line; Scarpia
    is a baritone; the Mahler 1 clip is Blumine only.

    py -3.9 cm_desc_0928.py [--apply]
"""
import json, re, sys, time
import concept_add as C

# (Work, Composer) -> Description, written into every active note of the work
DESC = {
 ("Symphony No. 6", "Ludwig van Beethoven"): "Five movements with titles, including a brook scene whose birdcalls (nightingale, quail, and cuckoo) are named in the score, and a thunderstorm that runs straight into the finale. Beethoven called it “more the expression of feeling than painting”.",
 ("Étude, Op. 10 No. 12", "Frédéric Chopin"): "A study for the left hand, which storms through runs under heroic right-hand octaves. Chopin wrote it in 1831, on hearing in Stuttgart that the Russians had taken Warsaw; the Op. 10 set is dedicated to Liszt.",
 ("Symphony No. 9", "Antonín Dvořák"): "Written in New York while Dvořák ran the National Conservatory, drawing on spirituals and on Longfellow's <i>Hiawatha</i>. The <i>Largo</i>'s <i>cor anglais</i> melody was later given words as “Goin' Home” by his pupil William Arms Fisher.",
 ("Symphony No. 94", "Joseph Haydn"): "Its quiet slow-movement theme is cut off by a sudden <i>fortissimo</i> chord, said to have been aimed at dozing London audiences. One of the twelve symphonies Haydn wrote for Johann Peter Salomon's concerts.",
 ("Symphony No. 3", "Camille Saint-Saëns"): "Dedicated to the memory of Liszt, who died weeks after its 1886 London premiere. It is laid out in two large parts rather than four movements and adds organ and piano four hands; the organ's blazing C-major chord launches the finale.",
 ("Symphony No. 6", "Pyotr Ilyich Tchaikovsky"): "Tchaikovsky's last symphony ends with a slow movement that dies away into silence; he conducted the premiere nine days before his death. The first movement quotes the Russian Orthodox requiem chant, and the third is a march that audiences often applaud as if it were the end.",
 ("Symphony No. 3", "Ludwig van Beethoven"): "Beethoven dedicated it to Napoleon, then scratched out the title page when Napoleon crowned himself emperor. Twice the usual length, with a funeral march second and a finale of variations on a theme from his ballet <i>The Creatures of Prometheus</i>.",
 ("Symphony No. 1", "Robert Schumann"): "Sketched in four days in 1841, the first year of Schumann's marriage, after a poem by Adolf Böttger; Mendelssohn conducted the premiere in Leipzig. It opens with a trumpet call on the rhythm of the poem's last line.",
 ("Symphony No. 3", "Robert Schumann"): "In five movements, the extra one a solemn, archaic movement inspired by a cardinal's installation at Cologne Cathedral. Written after Schumann moved to Düsseldorf, it was the last of his symphonies to be composed.",
 ("String Quartet No. 12", "Antonín Dvořák"): "Written in three days in the Czech community of Spillville, Iowa, during Dvořák's American years; its tunes are pentatonic, and the third movement takes a birdcall from the scarlet tanager.",
 ("String Quartet No. 14", "Franz Schubert"): "Its slow movement is variations on Schubert's own song “Der Tod und das Mädchen”, and all four movements are in minor keys. Written in 1824, after he knew his illness was serious.",
 ("Symphony No. 8", "Franz Schubert"): "Two complete movements and a scherzo sketched for piano, left in 1822. The score lay with Schubert's friend Anselm Hüttenbrenner until 1865, and why Schubert abandoned it is unknown.",
 ("Symphony No. 3", "Felix Mendelssohn"): "Begun in 1829 after Mendelssohn saw the ruined chapel of Holyrood Palace in Edinburgh, and finished thirteen years later; its four movements run without a break.",
 ("Symphony No. 4", "Felix Mendelssohn"): "Begun on a tour of Italy. Its finale is a <i>saltarello</i>, a Roman dance, in the minor, so a major-key symphony ends in A minor. Mendelssohn never published it.",
 ("Piano Sonata No. 8", "Ludwig van Beethoven"): "One of the few nicknames Beethoven approved, from its first publisher. Its slow <i>Grave</i> introduction breaks back in during the first movement, and the <i>Adagio cantabile</i> melody is one of his best known.",
 ("Piano Sonata No. 21", "Ludwig van Beethoven"): "Dedicated to Count Ferdinand von Waldstein, Beethoven's first patron in Bonn. A short slow <i>Introduzione</i> leads into the finale; it replaced a longer middle movement, published separately as the <i>Andante favori</i>.",
 ("Piano Concerto No. 5", "Ludwig van Beethoven"): "Beethoven's last piano concerto, written in 1809 while Vienna was under French bombardment; the nickname is not his. The piano opens with cadenza-like flourishes instead of waiting through an orchestral exposition, and he was too deaf to give the premiere.",
 ("Violin Sonata No. 5", "Ludwig van Beethoven"): "The nickname was added after Beethoven's death. The violin opens with the main tune, unusual in a form still called a sonata for piano and violin, and in the minute-long scherzo the violin keeps landing a beat behind the piano.",
 ("Symphony No. 104", "Joseph Haydn"): "Haydn's last symphony, the final one of the twelve written for Johann Peter Salomon's London concerts. It opens with a stern D-minor fanfare, and the finale is built on a tune said to be a Croatian folk song or a London street cry.",
 ("Symphony No. 35", "Wolfgang Amadeus Mozart"): "Made from a serenade Mozart wrote in 1782 for the ennoblement of Sigmund Haffner the Younger in Salzburg, then reworked for Vienna with flutes and clarinets added.",
 ("Symphony No. 41", "Wolfgang Amadeus Mozart"): "Mozart's last symphony, the third he wrote in the summer of 1788. Its finale combines five themes in fugal counterpoint at once; the nickname probably came from Johann Peter Salomon.",
 ("Symphony No. 1", "Gustav Mahler"): "Mahler first called it a tone poem and briefly titled it after Jean Paul's novel <i>Titan</i>. Its third movement turns <i>Frère Jacques</i> into a minor-key funeral march led by a solo double bass, said to follow a woodcut of animals burying a hunter; the gentle <i>Blumine</i> movement was cut after early performances.",
 ("Symphony No. 2", "Gustav Mahler"): "Mahler found its ending at Hans von Bülow's funeral on hearing Friedrich Klopstock's hymn “Aufersteh'n”, and set it for soloists, chorus, organ, and offstage brass. The first movement began as a separate tone poem, <i>Totenfeier</i>.",
 ("Symphony No. 8", "Gustav Mahler"): "Scored for eight soloists, double chorus, boys' choir, and an enormous orchestra, and premiered in Munich in 1910 with over a thousand performers. It sets the Latin hymn <i>Veni creator spiritus</i> and the closing scene of Goethe's <i>Faust</i>.",
 ("Symphony No. 7", "Dmitri Shostakovich"): "Begun in Leningrad during the German siege; the score was microfilmed, flown out through Tehran, and played in the West as propaganda. Its first movement builds an invasion theme over a snare-drum <i>ostinato</i>, and in 1942 the starving city's own orchestra performed it.",
 ("Symphony No. 3", "Henryk Górecki"): "Three slow movements for soprano and orchestra on texts of separation between mother and child, one scratched on a Gestapo cell wall in Zakopane by an eighteen-year-old prisoner. A 1992 recording with Dawn Upshaw sold over a million copies.",
 ("Nocturnes", "Claude Debussy"): "Three orchestral pieces, <i>Nuages</i>, <i>Fêtes</i>, and <i>Sirènes</i>, the last adding a wordless female chorus.",
 ("Peer Gynt", "Edvard Grieg"): "Incidental music for Ibsen's play, containing <i>Morning Mood</i>, <i>Åse's Death</i>, <i>Anitra's Dance</i>, and <i>In the Hall of the Mountain King</i>.",
 ("Sonata", "Domenico Scarlatti"): "One of over 550 single-movement keyboard sonatas Domenico Scarlatti wrote in Spain for Queen Maria Barbara, full of hand-crossing and guitar imitations; Ralph Kirkpatrick catalogued them with K numbers.",
 ("Waltz, Op. 64 No. 1", "Frédéric Chopin"): "The nickname means “small”, not sixty seconds. Published in 1847 as the first of the three Op. 64 waltzes and dedicated to Countess Delfina Potocka; its spinning figure is said to be George Sand's little dog chasing its tail.",
 ("Requiem", "Gabriel Fauré"): "Omits the <i>Dies irae</i> except its closing <i>Pie Jesu</i>, and ends with <i>In Paradisum</i>. Fauré said he wrote it “for pleasure” and saw death as a happy deliverance rather than a terror; it has been called a lullaby of death.",
 ("Guillaume Tell", "Gioachino Rossini"): "Rossini's last opera, written at thirty-seven; he wrote no more operas in the thirty-nine years he had left. Its overture runs through a dawn for five cellos, a storm, a pastoral <i>cor anglais</i> tune, and the cavalry galop that became the <i>Lone Ranger</i> theme.",
 ("Il barbiere di Siviglia", "Gioachino Rossini"): "Written in about three weeks and hissed at its 1816 Rome premiere, partly by supporters of Giovanni Paisiello's older setting. Figaro makes his entrance with <i>Largo al factotum</i>, and the overture was borrowed from two earlier Rossini operas.",
 ("La forza del destino", "Giuseppe Verdi"): "The plot is set off by a pistol that fires by accident, killing the heroine's father, whose dying curse drives everything after; singers long thought the opera unlucky. Written for St Petersburg.",
 ("Micrologus", "Guido d'Arezzo"): "A treatise, not a piece: Guido's guide to teaching chant and composing <i>organum</i>, one of the most copied music textbooks of the Middle Ages. His letter <i>Epistola de ignoto cantu</i> introduced the syllables <i>ut</i>, <i>re</i>, <i>mi</i>, <i>fa</i>, <i>sol</i>, and <i>la</i>, taken from the hymn <i>Ut queant laxis</i>.",
 ("Symphony No. 5", "Gustav Mahler"): "Opens with a solo trumpet funeral march; the <i>Adagietto</i> for strings and harp was a love letter to Alma Mahler and became famous through Luchino Visconti's film <i>Death in Venice</i>.",
 ("Symphonie fantastique", "Hector Berlioz"): "A young artist, despairing of love, poisons himself with opium; his beloved recurs as an <i>idée fixe</i>, finally as a witch at a sabbath where the <i>Dies irae</i> tolls. Berlioz's own obsession was the actress Harriet Smithson, whom he later married.",
 ("Erlkönig", "Franz Schubert"): "Schubert set Goethe's ballad at eighteen: one singer voices narrator, father, son, and the Erlking over relentless piano triplets, which stop dead before the last line, “the child was dead”.",
 ("Toccata & Fugue", "Johann Sebastian Bach"): "The most famous organ piece ever written, though its attribution to Bach has been doubted for decades on stylistic grounds; Leopold Stokowski's orchestration opens Disney's <i>Fantasia</i>.",
 ("Symphony, Op. 11 No. 3", "Johann Stamitz"): "From the last years of Johann Stamitz, founder of the Mannheim school, whose orchestra was famous for the long <i>crescendo</i> and the rising “Mannheim rocket” that Mozart and Beethoven inherited.",
 ("Symphony No. 1", "Johannes Brahms"): "Took Brahms over twenty years, under the shadow of Beethoven; Hans von Bülow called it “Beethoven's Tenth”. Its finale's big tune resembles the <i>Ode to Joy</i>, and when this was pointed out Brahms said any fool could see that.",
 ("Symphony No. 4", "Johannes Brahms"): "Ends with a <i>passacaglia</i>, thirty variations and a coda on an eight-bar theme adapted from the closing chaconne of Bach's Cantata No. 150: an archaic form, used for a symphony's finale.",
 ("Lachrimae", "John Dowland"): "Seven pavans for five viols and lute, published in 1604, each beginning with the falling “tear” motif of Dowland's song “Flow, my tears”. He punned on his own name: <i>Semper Dowland semper dolens</i> (“always Dowland, always doleful”).",
 ("Missa Solemnis", "Ludwig van Beethoven"): "Written for Archduke Rudolph's installation as Archbishop of Olmütz, and finished three years too late. Beethoven headed the Kyrie “From the heart — may it go again to the heart!”, and the <i>Agnus Dei</i> is interrupted by distant military trumpets and drums.",
 ("Symphony No. 4", "Ludwig van Beethoven"): "Schumann called it a slender Greek maiden between two Norse giants, the <i>Eroica</i> and the Fifth. Its slow introduction gropes through B-flat minor before the <i>Allegro</i> bursts out.",
 ("Symphony No. 8", "Ludwig van Beethoven"): "The shortest of his mature symphonies, with a ticking second movement often linked to Johann Maelzel's metronome. Beethoven called it “my little symphony in F” and said it was less popular than the Seventh because it was so much better.",
 ("Symphony No. 9", "Ludwig van Beethoven"): "The first major symphony to use voices, setting Schiller's <i>Ode to Joy</i> in a finale that begins by rejecting the earlier movements' themes. Beethoven, completely deaf at the 1824 premiere, had to be turned round to see the applause.",
 ("Violin Concerto", "Pyotr Ilyich Tchaikovsky"): "Leopold Auer, its intended dedicatee, called it unplayable, and after the 1881 Vienna premiere Eduard Hanslick wrote that it “stinks to the ear”. It is now among the most performed violin concertos.",
 ("Der Rosenkavalier", "Richard Strauss"): "A Viennese comedy set in the 1740s with anachronistic waltzes, ending in a trio for three women's voices as the Marschallin gives up her young lover Octavian to Sophie.",
 ("Tod und Verklärung", "Richard Strauss"): "A dying artist relives his life before his soul is transfigured. Sixty years later Strauss quoted its transfiguration theme at the close of “Im Abendrot”, the last of his <i>Four Last Songs</i>; dying, he said it was just as he had composed it.",
 ("Romeo and Juliet", "Sergei Prokofiev"): "The Bolshoi rejected it as undanceable, and Prokofiev first gave it a happy ending, later dropped. <i>Dance of the Knights</i> is its best-known number.",
 ("Belshazzar's Feast", "William Walton"): "A cantata on the writing on the wall, with the chorus shouting “Slain!” at the king's death. Commissioned by the BBC for small forces, it grew into a Leeds Festival showpiece with two extra brass bands.",
 ("Lohengrin", "Richard Wagner"): "A swan knight who must never be asked his name. Its third-act prelude leads to the <i>Bridal Chorus</i>, universally used as the wedding processional.",
 ("Tannhäuser", "Richard Wagner"): "Its 1861 Paris revision put the ballet in Act I instead of Act II, so the Jockey Club members who came late rioted and closed it after three nights.",
 ("A Midsummer Night's Dream", "Felix Mendelssohn"): "Mendelssohn wrote the overture at seventeen and the rest of the incidental music sixteen years later. Its <i>Wedding March</i> became the standard recessional.",
 ("Le Sacre du printemps", "Igor Stravinsky"): "Its 1913 Paris premiere caused a riot, with Vaslav Nijinsky shouting counts from the wings. A pagan sacrifice, ending with the chosen maiden dancing herself to death.",
}

LISTEN = {
 1788489953167: "A coloratura soprano over a lilting, dance-like accompaniment, with long trills and runs high in the voice.",
 1787792906321: "The overture's slow introduction: four horns sing a hushed, hymn-like chorale over quiet strings.",
 1787711405681: "A soprano melody rising in long arcs over warm strings, with the full orchestra surging up beneath its climaxes.",
 1787711405684: "Mimì's soprano: plain, conversational phrases on repeated notes that blossom into a soaring climax over warm strings.",
 1787711405690: "Butterfly's final scene: the soprano line straining high over a full, surging orchestra.",
 1787711405691: "“Un bel dì, vedremo”: the soprano floats a hushed, suspended opening line before the orchestra swells beneath her.",
 1787711405195: "Bass-drum blows on the off-beats, a shrieking full chorus, and shattering brass: the loudest music Verdi wrote, and it returns through the work.",
 1787711405776: "A slow, sighing B-flat-minor lament, begun by the mezzo-soprano and taken up by the other soloists and the chorus over throbbing strings.",
 1787711405693: "Scarpia's scheming baritone monologue over tolling bells and organ, set against a church procession and a full chorus singing the <i>Te Deum</i>.",
 1787711405440: "Four brass bands placed at the corners of the hall, with sixteen timpani, blaze out at the <i>Tuba mirum</i>.",
 1788199512089: "A gentle trumpet serenade over soft, rippling strings: the <i>Blumine</i> movement Mahler later cut.",
 1787792906315: "A long orchestral <i>crescendo</i>, <i>tremolo</i> strings, abrupt loud–soft contrasts, and independent wind writing: the machinery of the Classical symphony being assembled.",
 1787711405220: "Two blunt E-flat chords, then a cello theme that stumbles onto a foreign C-sharp. Enormous: this movement alone outlasts a whole Haydn symphony. Listen for the horn entering with the theme a few bars early, over the wrong chord, just before the recapitulation.",
 1787711406016: "Furious D-minor <i>coloratura</i>, <i>staccato</i> leaps climbing twice to a high F, among the highest notes in the standard repertory.",
}


def P(s):
    return re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").replace("&amp;", "&").strip()


def plan():
    ids = C.anki("findNotes", query='"note:Classical Music" -Kind:_*')
    ns = C.anki("notesInfo", notes=ids)
    info = {c["cardId"]: c["queue"] for c in C.anki("cardsInfo", cards=[c for n in ns for c in n["cards"]])}
    ch, seen = {}, set()
    for n in ns:
        if all(info[c] == -1 for c in n["cards"]):
            continue
        key = (P(n["fields"]["Work"]["value"]), n["fields"]["Composer"]["value"])
        if key in DESC:
            seen.add(key)
            if n["fields"]["Description"]["value"] != DESC[key]:
                ch.setdefault(n["noteId"], (n, {}))[1]["Description"] = DESC[key]
        if n["noteId"] in LISTEN and n["fields"]["Listen"]["value"] != LISTEN[n["noteId"]]:
            ch.setdefault(n["noteId"], (n, {}))[1]["Listen"] = LISTEN[n["noteId"]]
    missing = set(DESC) - seen
    assert not missing, missing
    return list(ch.values())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ch = plan()
    nd = sum("Description" in f for n, f in ch); nl = sum("Listen" in f for n, f in ch)
    print("notes:", len(ch), "| descriptions:", nd, "| listen lines:", nl)
    if "--apply" in sys.argv:
        json.dump([{"nid": n["noteId"], **{k: n["fields"][k]["value"] for k in f}} for n, f in ch],
                  open("backups/cm_desc_0928_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
        for n, f in ch:
            C.anki("updateNoteFields", note={"id": n["noteId"], "fields": f})
        print("applied")
