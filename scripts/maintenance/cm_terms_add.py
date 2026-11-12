# -*- coding: utf-8 -*-
"""cm_terms_add.py -- term cards for words the Classical Music text already uses.

Carter (2026-09-25): "can you make cards for some of the other common terms used
in the deck if they arent already there, like opera-comique or masque-opera,
etc...?" and, on key names, "i should learn what the symbols mean anyhow".

Each term below occurs in the deck's own Description / Listen text (counted
first) and had no card among the 106 existing ones. Same shape as those:
definition on the front, name as the answer, an example in "Heard in", a Detail
line only where it adds a fact. concept_add.add() refuses a definition that
contains its answer and skips anything already present.

Tiers are tight (W97): tier1 only for the six a listener meets constantly;
tier3 for the specialist items; the rest tier2. Per the tier gate, cards not on
a tier1 note are suspended after adding.

    py -3.9 cm_terms_add.py --dry | --apply
"""
import sys

import concept_add as C

T = [
 # name, kind, tier, period, definition, heard in, detail
 ("Recitative", "Form", 1, "Baroque",
  "Speech-like singing that follows the rhythm of the words and carries an opera's plot between the arias; <i>secco</i> when only the continuo accompanies it.",
  "Mozart &middot; <i>Don Giovanni</i>", "It arrived with the first operas, in Florence around 1600."),
 ("Aria", "Form", 1, "",
  "A self-contained solo song in an opera, oratorio, or cantata, where the action stops and a character reflects; the Baroque type repeats its first section <i>da capo</i>.",
  "Puccini &middot; <i>Gianni Schicchi</i>", ""),
 ("Opéra comique", "Genre", 2, "",
  "French opera with spoken dialogue between the musical numbers, whatever its mood; named after the Paris theatre that staged it.",
  "Bizet &middot; <i>Carmen</i>", "The label means spoken dialogue, not comedy: <i>Carmen</i> ends in a murder."),
 ("Grand opera", "Genre", 2, "Romantic",
  "The Paris spectacle of the 1830s to 1860s: five acts, a historical subject, massed choruses, a ballet, and lavish staging.",
  "Meyerbeer &middot; <i>Les Huguenots</i>",
  "The Paris Opéra required a ballet in Act II, which is why the Jockey Club wrecked Wagner's 1861 <i>Tannhäuser</i> when he put it in Act I."),
 ("Masque", "Genre", 2, "Baroque",
  "An English court entertainment of the 16th and 17th centuries combining poetry, song, dance, and elaborate scenery, in which courtiers themselves performed.",
  "John Blow &middot; <i>Venus and Adonis</i>", "Ben Jonson wrote the texts and Inigo Jones the designs for the Stuart ones."),
 ("Semi-opera", "Genre", 3, "Baroque",
  "An English Restoration hybrid in which a spoken play carries the plot and the music comes in separate episodes, usually sung by minor or supernatural characters.",
  "Purcell &middot; <i>The Fairy-Queen</i>", ""),
 ("Ballad opera", "Genre", 2, "Baroque",
  "An 18th-century English stage work of spoken dialogue broken by new words set to popular tunes, usually satirical.",
  "John Gay &middot; <i>The Beggar's Opera</i>", ""),
 ("Tragédie en musique", "Genre", 3, "Baroque",
  "The serious French opera of Lully and Rameau: five acts on myth or chivalric romance, a prologue praising the king, and dances throughout.",
  "Lully &middot; <i>Armide</i>", ""),
 ("Opéra-ballet", "Genre", 3, "Baroque",
  "An 18th-century French stage genre of loosely linked acts, each with its own story, in which dance matters as much as singing.",
  "Rameau &middot; <i>Les Indes galantes</i>", ""),
 ("Operetta", "Genre", 2, "Romantic",
  "A light stage work with spoken dialogue, catchy songs, and dances, usually comic and sentimental; Jacques Offenbach in Paris, Johann Strauss II and Franz Lehár in Vienna.",
  "Lehár &middot; <i>The Merry Widow</i>", ""),
 ("Intermezzo", "Form", 2, "",
  "A short piece set between larger ones: in the 18th century, a comic opera played between the acts of a serious one; later, an orchestral interlude inside an opera or a short piano piece.",
  "Pergolesi &middot; <i>La serva padrona</i>", ""),
 ("Melodrama", "Technique", 3, "",
  "Spoken words delivered over or between passages of music.",
  "Weber &middot; <i>Der Freischütz</i>", "The Wolf's Glen scene and the dungeon scene of Beethoven's <i>Fidelio</i> are the standard examples."),
 ("Incidental music", "Genre", 2, "",
  "Music written for a spoken play (overtures, entr'actes, songs, and underscoring), often gathered afterwards into a concert suite.",
  "Grieg &middot; <i>Peer Gynt</i>", ""),
 ("Suite", "Form", 2, "Baroque",
  "A set of instrumental movements played as one work: in the Baroque, stylised dances (allemande, courante, sarabande, gigue); later, any sequence drawn from a ballet, opera, or play.",
  "Handel &middot; <i>Water Music</i>", ""),
 ("Serenade", "Genre", 2, "Classical",
  "Originally a song sung at evening beneath a lover's window; in the Classical period, a light piece in several movements for an outdoor or social occasion.",
  "Mozart &middot; <i>Eine kleine Nachtmusik</i>", ""),
 ("Character piece", "Genre", 2, "Romantic",
  "A short Romantic piano work that captures one mood or scene, often under a fanciful title.",
  "Schumann &middot; <i>Kinderszenen</i>", ""),
 ("Dies irae", "Concept", 1, "",
  "The medieval chant on the Day of Judgement from the Requiem Mass, whose four-note falling opening composers quote to mean death.",
  "Berlioz &middot; <i>Symphonie fantastique</i>",
  "Also quoted by Liszt (<i>Totentanz</i>), Saint-Saëns (<i>Danse macabre</i>), and Rachmaninoff (<i>Rhapsody on a Theme of Paganini</i>)."),
 ("Tristan chord", "Concept", 1, "Romantic",
  "The unresolved half-diminished chord F, B, D-sharp, G-sharp in the second bar of a Wagner prelude, often called the start of modern harmony.",
  "Wagner &middot; <i>Tristan und Isolde</i>", ""),
 ("Mad scene", "Concept", 2, "Romantic",
  "An operatic set piece in which a heroine loses her reason, sung in dazzling coloratura, often with a solo flute echoing her.",
  "Donizetti &middot; <i>Lucia di Lammermoor</i>", ""),
 ("Trouser role", "Concept", 2, "",
  "A male character written for a woman's voice, usually a mezzo-soprano playing a youth.",
  "Richard Strauss &middot; <i>Der Rosenkavalier</i>", "Cherubino in <i>The Marriage of Figaro</i> and Octavian are the standard examples."),
 ("Countertenor", "Voice", 2, "",
  "A male singer using a developed head voice to sing in the alto or even soprano range.",
  "Britten &middot; <i>A Midsummer Night's Dream</i>", "Britten wrote Oberon for Alfred Deller."),
 ("Mannheim rocket", "Technique", 2, "Classical",
  "A rapidly rising arpeggio over a crescendo, the trademark of the Elector Palatine's court orchestra under Johann Stamitz in the 1750s.",
  "Mozart &middot; <i>Symphony No. 40</i>", "It opens the finale of Mozart's Symphony No. 40."),
 ("Sturm und Drang", "Style", 2, "Classical",
  "A German movement of the 1760s and 1770s, named after a play, prizing turbulent emotion; in music, restless minor-key symphonies.",
  "Haydn &middot; <i>Farewell Symphony</i>", ""),
 ("Tone cluster", "Technique", 2, "20th century",
  "A chord of adjacent notes sounded together, such as a whole row of piano keys pressed with the forearm.",
  "Henry Cowell &middot; <i>The Tides of Manaunaun</i>", ""),
 ("Microtonality", "Technique", 3, "20th century",
  "Music using intervals smaller than a semitone, such as quarter tones.",
  "Aribert Reimann &middot; <i>Lear</i>", ""),
 ("Querelle des Bouffons", "Concept", 3, "Baroque",
  "The 1752 to 1754 Paris pamphlet war over whether French or Italian opera was better, set off by an Italian comic intermezzo.",
  "Pergolesi &middot; <i>La serva padrona</i>", "Jean-Jacques Rousseau took the Italian side."),
 ("Paraphrase mass", "Form", 3, "Renaissance",
  "A Renaissance mass built on a plainchant melody that is embellished and passed through every voice rather than held in one.",
  "Josquin &middot; <i>Missa Pange lingua</i>", ""),
 ("Solmization", "Concept", 3, "Medieval",
  "Naming the steps of a scale by syllables (<i>ut, re, mi, fa, sol, la</i>) to teach sight-singing, credited to Guido of Arezzo.",
  "Guido of Arezzo &middot; <i>Ut queant laxis</i>", ""),
 ("Quodlibet", "Form", 3, "",
  "A piece that combines several well-known tunes at once or in quick succession, usually for humour.",
  "Bach &middot; <i>Goldberg Variations</i>", ""),
 ("Church parable", "Genre", 3, "20th century",
  "A small-scale sacred opera for an all-male cast and a chamber ensemble, staged in a religious building without a conductor, modelled on Japanese Noh.",
  "Britten &middot; <i>Curlew River</i>", ""),
 ("Gamelan", "Ensemble", 2, "",
  "An Indonesian ensemble of tuned gongs, metallophones, and drums from Java and Bali, whose interlocking patterns influenced Debussy and Britten.",
  "Colin McPhee &middot; <i>Tabuh-Tabuhan</i>", ""),
 ("Cor anglais", "Instrument", 2, "",
  "An alto oboe pitched a fifth below the oboe, with a bulb-shaped bell and a darker, melancholy tone; called the English horn in America.",
  "Dvořák &middot; <i>Symphony No. 9</i>", ""),
 ("Celesta", "Instrument", 2, "",
  "A keyboard instrument whose hammers strike metal plates, giving a soft, bell-like sound.",
  "Tchaikovsky &middot; <i>The Nutcracker</i>", "Invented by Auguste Mustel in Paris in 1886."),
 ("Ondes Martenot", "Instrument", 3, "20th century",
  "An early electronic instrument of 1928, played from a keyboard or a ring on a wire, producing gliding, wavering tones.",
  "Messiaen &middot; <i>Turangalîla-Symphonie</i>", ""),
 ("Cimbalom", "Instrument", 3, "",
  "The Hungarian concert hammered dulcimer, its strings struck with small beaters.",
  "Kodály &middot; <i>Háry János</i>", ""),
 ("Glass harmonica", "Instrument", 3, "Classical",
  "Nested spinning crystal bowls played with wet fingers, invented by Benjamin Franklin in 1761.",
  "Donizetti &middot; <i>Lucia di Lammermoor</i>", "The mad scene was first scored for it."),
 ("Basset horn", "Instrument", 3, "Classical",
  "A tenor clarinet with an extended low range and a bent neck, favoured by Mozart in his Masonic music.",
  "Mozart &middot; <i>Requiem</i>", ""),
 ("Flat", "Notation", 1, "",
  "The sign ♭, which lowers a note by a semitone; its opposite raises one.",
  "", "Written after the letter in names: B-flat, E-flat major."),
 ("Sharp", "Notation", 1, "",
  "The sign ♯, which raises a note by a semitone; its opposite lowers one.",
  "", "Written after the letter in names: C-sharp minor, F-sharp major."),
]
FIELDS = {"Work": "name", "Kind": "kind", "Description": "definition", "Composer": "heard",
          "Nickname": "detail", "Period": "period"}
TIER = {1: "tier1-core", 2: "tier2-solid", 3: "tier3-deepcut"}


def main():
    dry = "--apply" not in sys.argv
    for tier in (1, 2, 3):
        rows = [dict(name=n, kind=k, period=p, definition=d, heard=h, detail=x)
                for n, k, t, p, d, h, x in T if t == tier]
        print("== %s" % TIER[tier])
        C.add("Classical Music", "Work", "Classical Music", rows, FIELDS, dry=dry,
              tags=("Music::concept", "Music::tier::" + TIER[tier]), concepts_only=True)
    if not dry:
        # tier gate: only tier1 cards in the queue
        low = C.anki("findCards", query='note:"Classical Music" tag:Music::concept '
                                        '-tag:Music::tier::tier1-core -is:suspended added:1')
        if low:
            C.anki("suspend", cards=low)
        print("suspended %d non-tier1 cards" % len(low))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
