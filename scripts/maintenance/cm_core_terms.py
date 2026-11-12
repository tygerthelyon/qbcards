# -*- coding: utf-8 -*-
"""cm_core_terms.py -- cards for the answers music tossups use most.

Audit 2026-09-26, 1.2: instruments answer over 600 of the 10,414 auditory and opera
tossups in the pool (flute 57, saxophone 26, clarinet 55, trumpet 54, violin 54, piano 41, cello 37,
viola 23, oboe 28, horn 22, trombone 21, bassoon 20, harp 19, guitar 17, harpsichord 14,
organ 13, double bass 12, timpani 9), and the plainest genres had no card at all
(string quartet 63, concerto about 50, waltz 44, mass 37, march 20, symphony 16,
ragtime 15, sonata 19, piano trio 12). Counts are answer lines in the pool, singular
and plural together.

Same shape as cm_terms_add.py: the definition clues the thing the way a tossup does
(construction first, then signature repertoire), "Heard in" names one piece, and
the Detail line carries the giveaway-level facts. concept_add.add() rejects any
definition containing its own answer. Tier1 at 10+ answer lines, tier2 below that.

    py -3.9 cm_core_terms.py --dry | --apply
"""
import sys

import concept_add as C

T = [
 # name, kind, tier, period, definition, heard in, detail
 ("Flute", "Instrument", 1, "",
  "A woodwind with no reed, held sideways and sounded by blowing across a hole; Theobald Boehm's keywork of 1847 set the modern metal form.",
  "Debussy &middot; <i>Syrinx</i>",
  "Its solo opens Debussy's <i>Prélude à l'après-midi d'un faune</i>, and it plays the bird in Prokofiev's <i>Peter and the Wolf</i>."),
 ("Clarinet", "Instrument", 1, "",
  "A single-reed woodwind with a cylindrical bore, so it overblows at the twelfth rather than the octave; its dark low register is the chalumeau.",
  "Mozart &middot; Concerto in A major, K. 622",
  "A glissando on it opens Gershwin's <i>Rhapsody in Blue</i>; it plays the cat in <i>Peter and the Wolf</i>; Mozart and Brahms wrote quintets for it."),
 ("Trumpet", "Instrument", 1, "",
  "The highest brass instrument, a narrow cylindrical tube with a cup mouthpiece and three piston valves; Baroque players had only the valveless natural form.",
  "Haydn &middot; Concerto in E-flat major",
  "It asks the question in Ives's <i>The Unanswered Question</i>; Louis Armstrong and Miles Davis played it."),
 ("Violin", "Instrument", 1, "",
  "The highest bowed string instrument, with four strings tuned in fifths (G, D, A, E), whose form was set by the Cremona workshops of Amati, Stradivari, and Guarneri.",
  "Vivaldi &middot; <i>The Four Seasons</i>",
  "Paganini's 24 Caprices are its virtuoso touchstone."),
 ("Piano", "Instrument", 1, "",
  "A keyboard instrument whose keys throw felt hammers at strings, invented by Bartolomeo Cristofori in Florence around 1700 and named for playing both soft and loud.",
  "Chopin &middot; <i>Nocturnes</i>",
  "The sustain pedal lifts all the dampers; John Cage \"prepared\" one with screws and bolts."),
 ("Cello", "Instrument", 1, "",
  "The bowed string instrument an octave below the viola, strung C, G, D, A, held between the knees and resting on an endpin.",
  "Bach &middot; six unaccompanied suites, BWV 1007–1012",
  "Pablo Casals revived Bach's suites; it plays \"The Swan\" in Saint-Saëns's <i>Carnival of the Animals</i>."),
 ("Saxophone", "Instrument", 1, "",
  "A single-reed woodwind with a conical brass body, patented in 1846 by a Belgian maker from Dinant who gave it his name.",
  "Ravel's orchestration of <i>Pictures at an Exhibition</i> &middot; \"The Old Castle\"",
  "Charlie Parker and John Coltrane made it the voice of jazz; Glazunov and Debussy wrote concert works for it."),
 ("Viola", "Instrument", 1, "",
  "The alto of the bowed string family, a fifth below the violin with a low C string, whose music is written in the alto clef.",
  "Berlioz &middot; <i>Harold en Italie</i>",
  "Paganini commissioned the Berlioz work and never played it; Walton and Bartók wrote concertos for it."),
 ("Oboe", "Instrument", 1, "",
  "A double-reed woodwind with a conical bore, which sounds the A the orchestra tunes to.",
  "Mozart &middot; Concerto in C major, K. 314",
  "It plays the duck in <i>Peter and the Wolf</i>; Richard Strauss wrote a concerto for it in 1945."),
 ("French horn", "Instrument", 1, "",
  "A coiled brass instrument with a wide flaring bell, played with one hand inside the bell; valves arrived in the 1810s, and before them it changed key with crooks.",
  "Mozart &middot; four concertos for Joseph Leutgeb",
  "Its call opens Strauss's <i>Till Eulenspiegel</i>, and three of them play the wolf in <i>Peter and the Wolf</i>."),
 ("Trombone", "Instrument", 1, "",
  "A brass instrument that changes pitch with a telescoping slide instead of valves, long tied to church music and to the supernatural in opera.",
  "Mozart &middot; <i>Requiem</i>, \"Tuba mirum\"",
  "Beethoven brought it into the symphony in the finale of his Fifth."),
 ("Bassoon", "Instrument", 1, "",
  "The bass of the double-reed woodwinds, its long tube folded back on itself, with the reed on a bent metal crook.",
  "Stravinsky &middot; <i>The Rite of Spring</i>, opening solo",
  "It plays the grandfather in <i>Peter and the Wolf</i> and the marching broom in Dukas's <i>The Sorcerer's Apprentice</i>."),
 ("Harp", "Instrument", 1, "",
  "A plucked instrument of 47 strings whose seven pedals each move one note name by a semitone in every octave, the double-action mechanism perfected by Sébastien Érard.",
  "Debussy &middot; <i>Danses sacrée et profane</i>",
  "Its cadenza opens the \"Waltz of the Flowers\" in <i>The Nutcracker</i>."),
 ("Guitar", "Instrument", 1, "",
  "A plucked, fretted instrument with six strings and a flat back, whose classical form was fixed by Antonio de Torres in 19th-century Spain.",
  "Rodrigo &middot; <i>Concierto de Aranjuez</i>",
  "Andrés Segovia built its concert repertoire; Villa-Lobos wrote twelve études for it."),
 ("Harpsichord", "Instrument", 1, "Baroque",
  "A keyboard instrument that plucks its strings with quills, so touch cannot change its loudness; players use a second manual or stops instead.",
  "Bach &middot; <i>Goldberg Variations</i>",
  "Domenico Scarlatti wrote 555 sonatas for it; Wanda Landowska revived it in the 20th century."),
 ("Organ", "Instrument", 1, "",
  "A keyboard instrument sounded by wind through ranks of pipes chosen by stops, usually with several manuals and a pedalboard for the feet.",
  "Bach &middot; Toccata and Fugue in D minor",
  "Saint-Saëns's Third Symphony features it; Widor and Vierne wrote \"symphonies\" for it alone."),
 ("Double bass", "Instrument", 1, "",
  "The largest and lowest bowed string instrument, tuned in fourths rather than fifths and sounding an octave below its written pitch.",
  "Saint-Saëns &middot; \"The Elephant\", <i>Carnival of the Animals</i>",
  "Plucked, it holds down the rhythm section in jazz; Giovanni Bottesini was its great virtuoso."),
 ("Timpani", "Instrument", 2, "",
  "Large tunable drums with copper bowls and a stretched head, pitched by pedals or screws and played in sets of two to five.",
  "Haydn &middot; Symphony No. 103, \"Drumroll\"",
  "Beethoven tuned them an octave apart in his Eighth and Ninth; they answer the brass in the opening of <i>Also sprach Zarathustra</i>."),
 ("String quartet", "Genre", 1, "Classical",
  "A chamber work, or the ensemble that plays it, for two violins, viola, and cello; Haydn wrote 68 and established it, and Beethoven's late set pushed it furthest.",
  "Beethoven &middot; Op. 131 in C-sharp minor",
  "Shostakovich wrote 15, as many as his symphonies; Haydn's Op. 76 No. 3 is the \"Emperor\"."),
 ("Concerto", "Genre", 1, "",
  "A work setting a soloist, or a small group, against an orchestra, usually fast–slow–fast, with a solo cadenza near the end of the first movement.",
  "Mendelssohn &middot; Violin, E minor, Op. 64",
  "Vivaldi wrote over 500; Beethoven's Fifth for piano is the \"Emperor\"."),
 ("Waltz", "Genre", 1, "Romantic",
  "A dance in triple time with a strong downbeat, which grew out of the Austrian Ländler to rule the Viennese ballrooms of the 19th century.",
  "Johann Strauss II &middot; <i>The Blue Danube</i>",
  "Chopin's Op. 64 No. 1 is the \"Minute\"; Ravel's <i>La valse</i> is its apotheosis and collapse."),
 ("Mass", "Genre", 1, "",
  "A setting of the central Catholic liturgy, above all its fixed Ordinary: Kyrie, Gloria, Credo, Sanctus, and Agnus Dei.",
  "Bach &middot; B minor, BWV 232",
  "Machaut's <i>Messe de Nostre Dame</i> is the first complete setting by one composer; Palestrina's for Pope Marcellus supposedly saved polyphony at Trent."),
 ("Symphony", "Genre", 1, "Classical",
  "A large orchestral work, usually in four movements with the first in sonata form, which grew out of the Italian opera overture; Haydn wrote 104.",
  "Beethoven &middot; No. 5 in C minor",
  "Mahler told Sibelius it \"must be like the world; it must embrace everything.\""),
 ("Sonata", "Genre", 1, "",
  "An instrumental work in several movements for one player, or one with piano, whose first movement usually runs exposition, development, and recapitulation.",
  "Beethoven &middot; \"Moonlight\", Op. 27 No. 2",
  "Beethoven wrote 32 for piano; Domenico Scarlatti's 555 are single movements."),
 ("March", "Genre", 1, "",
  "Music for soldiers and parades to step to, in duple time with a strong regular beat and a contrasting middle section called the trio; John Philip Sousa was its American master.",
  "Sousa &middot; <i>The Stars and Stripes Forever</i>",
  "Elgar's <i>Pomp and Circumstance</i> No. 1 is played at graduations."),
 ("Ragtime", "Genre", 1, "",
  "A syncopated American piano style of about 1895–1918: an off-beat right hand over a steady \"oom-pah\" left hand, in march-like strains.",
  "Scott Joplin &middot; <i>The Entertainer</i>",
  "The 1973 film <i>The Sting</i> revived it; Joplin also wrote an opera, <i>Treemonisha</i>."),
 ("Piano trio", "Genre", 2, "",
  "A chamber work, or the ensemble that plays it, for keyboard, violin, and cello.",
  "Beethoven &middot; \"Archduke\", Op. 97",
  "Tchaikovsky wrote his as an elegy for Nikolai Rubinstein."),
 ("Barcarolle", "Genre", 2, "",
  "A song or piece in a lilting 6/8 or 12/8 time imitating the songs of Venetian gondoliers.",
  "Offenbach &middot; <i>The Tales of Hoffmann</i>",
  "Chopin's Op. 60 is the great piano example."),
]
FIELDS = {"Work": "name", "Kind": "kind", "Description": "definition", "Composer": "heard",
          "Nickname": "detail", "Period": "period"}
TIER = {1: "tier1-core", 2: "tier2-solid", 3: "tier3-deepcut"}


def main():
    dry = "--apply" not in sys.argv
    for tier in (1, 2):
        rows = [dict(name=n, kind=k, period=p, definition=d, heard=h, detail=x)
                for n, k, t, p, d, h, x in T if t == tier]
        print("== %s" % TIER[tier])
        C.add("Classical Music", "Work", "Classical Music", rows, FIELDS, dry=dry,
              tags=("Music::concept", "Music::tier::" + TIER[tier], "Music::audit_2026-09-26"),
              concepts_only=True)
    if not dry:
        low = C.anki("findCards", query='note:"Classical Music" tag:Music::audit_2026-09-26 '
                                        '-tag:Music::tier::tier1-core -is:suspended')
        if low:
            C.anki("suspend", cards=low)
        print("suspended %d non-tier1 cards" % len(low))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
