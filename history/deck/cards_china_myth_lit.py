# -*- coding: utf-8 -*-
"""cards_china_myth_lit.py -- History v2 cards for China: Mythology and Literature.

Sources: my notes (World Hist pp. 1-9, the part I have checked and studied), corrected where they were
wrong, plus the qbreader supplement (notes/01_supplement_mythology_literature.md).
src="notes" cards are active. src="qb" cards are active at tier 1-2 and suspended at tier 3-4.

Q(...)  QB Clue: one clue -> one answer (pic= adds a PICTURE card when the picture is the clue)
L(...)  QB List: a closed set, one card per item, the other items hidden on the front
T(...)  QB Tossup: lead-in -> giveaway, graded by where you could have buzzed

pos: lead (hard, early in a tossup) / mid / give (the giveaway). Images are keys into IMAGES
(images.py); the picture always shows the card's answer.
"""

NOTES = []
P = "mythology"


def Q(entity, tier, pos, prompt, answer, accept="", extra="", img="", conf="", src="notes", pic="",
      picq="", kind="figure", period=None):
    NOTES.append(dict(model="QB Clue", entity=entity, tier=tier, pos=pos, src=src, kind=kind,
                      period=period or P, fields=dict(Prompt=prompt, Answer=answer, Accept=accept,
                      Extra=extra, Confusable=conf, Entity=entity), img=img, pic=pic, picq=picq))


def L(entity, tier, title, items, extra="", img="", src="notes", ordered=True, period=None):
    tag = "ol" if ordered else "ul"
    lis = "".join("<li>{{c%d::%s}}%s</li>" % (i + 1, a, (" — " + cue) if cue else "")
                  for i, (a, cue) in enumerate(items))
    NOTES.append(dict(model="QB List", entity=entity, tier=tier, pos="mid", src=src, kind="set",
                      period=period or P, fields=dict(Text="<%s>%s</%s>" % (tag, lis, tag), Title=title,
                      Extra=extra, Entity=entity), img=img))


def T(entity, tier, clues, give, answer, accept="", extra="", img="", src="qb", period=None):
    c = list(clues) + [""] * (4 - len(clues))
    NOTES.append(dict(model="QB Tossup", entity=entity, tier=tier, pos="mid", src=src, kind="tossup",
                      period=period or P, fields=dict(Clue1=c[0], Clue2=c[1], Clue3=c[2], Clue4=c[3],
                      Giveaway=give, Answer=answer, Accept=accept, Extra=extra, Entity=entity), img=img))


# =====================================================================================
# MYTHOLOGY - creation
# =====================================================================================
E = "Pangu"
Q(E, 1, "give", "This primordial giant hatched from a cosmic egg; when he split it with an axe, the halves became "
  "earth (<i>yin</i>) and heaven (<i>yang</i>).", "<u>Pangu</u>", "Pan Gu; P'an Ku", img="pangu",
  extra="He held the two apart for 18,000 years as he grew; the first written account is Xu Zheng's 3rd-century <i>Sanwu Liji</i>.")
Q(E, 2, "mid", "When this creator giant died, his breath became the wind, his eyes the sun and moon, and his body "
  "the mountains and seas.", "<u>Pangu</u>", "Pan Gu", img="pangu")
Q(E, 2, "lead", "Humans arose from the parasites on this hairy, horned giant's body, blown by the wind after his death.",
  "<u>Pangu</u>", "Pan Gu", src="notes")
Q(E, 3, "lead", "This giant made an ox from clay and saliva to hold up the earth, and is one of the few beings who can "
  "make rain without the Jade Emperor's permission.", "<u>Pangu</u>", "Pan Gu")
Q("cosmic egg", 2, "mid", "In Chinese creation myth, Pangu grew for 18,000 years inside one of these objects before breaking out.",
  "an <u>egg</u>", "cosmic egg", kind="thing", src="qb")

E = "Nüwa"
Q(E, 1, "give", "This goddess made the first humans out of yellow clay.", "<u>Nüwa</u>",
  "Nügua; Nu Wa; Nu Gua", img="nuwa_fuxi", conf="Jingwei (the Yan Emperor's drowned daughter, also read Nüwa)")
Q(E, 2, "mid", "Tired of shaping people by hand, this goddess dipped a rope in mud and flung the drops, which became "
  "the poor while the hand-made became nobles.", "<u>Nüwa</u>", "Nügua", src="qb",
  extra="This version is in Ying Shao's <i>Fengsu Tongyi</i>.")
Q(E, 1, "give", "This goddess melted five-coloured stones to patch the broken sky.", "<u>Nüwa</u>", "Nügua",
  extra="The story is known as 'mending the heavens' and is in the <i>Huainanzi</i>.", img="nuwa_mend")
Q("turtle", 1, "mid", "Nüwa cut the legs off a giant one of these animals, named Ao, to prop up the four corners of the sky.",
  "a <u>turtle</u>", "tortoise; Ao", kind="thing", extra="Quizbowl often asks this as a common-link answer, with the Hindu world-turtle and the Black Tortoise.")
Q("Gonggong", 2, "mid", "After losing a battle to Zhuanxu, this water god butted Mount Buzhou, a pillar of heaven, and "
  "broke the sky.", "<u>Gonggong</u>", "Gong Gong", extra="In other versions he fights the fire god Zhurong. The sky tilted "
  "northwest and the earth sank southeast, which is why China's rivers flow east.")
Q("Mount Buzhou", 3, "lead", "Gonggong headbutted this mountain, one of the pillars holding up heaven, forcing Nüwa to repair the sky.",
  "Mount <u>Buzhou</u>", "Buzhou Shan", kind="place")
Q("Zhurong", 3, "lead", "In some versions, the water god Gonggong fought this god of fire before breaking the pillar of heaven; "
  "the same god executed Gun on Feather Mountain.", "<u>Zhurong</u>", "Chu Jung", src="qb")
Q(E, 2, "mid", "In <i>Investiture of the Gods</i>, this goddess sent a fox spirit to possess Daji and corrupt King "
  "Zhou of Shang for writing a lustful poem on her temple wall.", "<u>Nüwa</u>", "Nügua")
Q(E, 2, "mid", "This goddess and her brother-husband are drawn with intertwined snake tails, holding a compass and a set square.",
  "<u>Nüwa</u> (and Fuxi)", "Nügua", pic="nuwa_fuxi", picq="Which pair of deities?", img="nuwa_fuxi")
Q("snake", 2, "mid", "Nüwa and Fuxi have the lower bodies of this kind of creature, and in some stories mate to repopulate the "
  "world after a flood.", "a <u>snake</u>", "serpent", kind="thing")
Q("Jingwei", 3, "lead", "The Yan Emperor's daughter drowned in the Eastern Sea and became this bird, which tries to fill the sea "
  "with twigs and pebbles.", "<u>Jingwei</u>", "", src="qb", conf="Nüwa the creator goddess")

E = "Fuxi"
Q(E, 2, "give", "After studying the markings on a tortoise shell, this culture hero created the Eight Trigrams.",
  "<u>Fuxi</u>", "Fu Hsi; Fu Xi", extra="King Wen of Zhou later doubled the trigrams into the 64 hexagrams of the <i>I Ching</i>.")
Q("Ba Gua", 3, "lead", "Fuxi placed the eight trigrams around the <i>tajitu</i> (yin and yang) to make this symbol.",
  "the <u>Ba Gua</u>", "Bagua; Pa Kua; eight trigrams", kind="thing")
Q(E, 3, "lead", "This brother-husband of Nüwa taught humans to fish with nets; the Yellow River Map was revealed to him by a dragon-horse.",
  "<u>Fuxi</u>", "Fu Hsi", src="qb")

# =====================================================================================
# The sage kings
# =====================================================================================
L("Three Sovereigns", 2, "The Three Sovereigns (the common list)",
  [("Fuxi", "the most ancient; trigrams"), ("Shennong", "farming; herbs; tea"), ("Huangdi", "the Yellow Emperor")],
  extra="Sources differ; Nüwa, Suiren, or Zhurong appear in other lists. They come before the Five Emperors.")
L("Five Emperors", 2, "The Five Emperors (Sima Qian's <i>Shiji</i>)",
  [("the Yellow Emperor", "Huangdi"), ("Zhuanxu", "astronomy and the calendar"), ("Di Ku", ""),
   ("Yao", "the model benevolent ruler"), ("Shun", "passed the throne to Yu")],
  extra="Other lists put Shaohao among them, as my notes did; quizbowl follows the <i>Shiji</i>.")

E = "Shennong"
Q(E, 1, "give", "This god of agriculture discovered tea when burning leaves blew into his pot.", "<u>Shennong</u>",
  "Shen Nung; Divine Farmer", img="shennong")
Q(E, 2, "mid", "Called the 'First Deity of the Five Grains', this ox-headed sage is often merged with Yan Di, the Flame Emperor.",
  "<u>Shennong</u>", "Divine Farmer")
Q(E, 2, "mid", "This 'Divine Farmer' tasted a hundred herbs to test them for poison, helped by a transparent stomach.",
  "<u>Shennong</u>", "Shen Nung", src="qb", extra="His name is on the <i>Divine Farmer's Materia Medica</i> (<i>Shennong Bencao Jing</i>).")
Q("tea", 2, "mid", "Shennong supposedly discovered this drink when leaves fell into his boiling water.", "<u>tea</u>", "cha",
  kind="thing")

E = "Yellow Emperor"
Q(E, 1, "give", "Regarded as the initiator of Chinese culture, this sovereign is credited with the calendar, carts, boats, "
  "the compass needle, and the ball game <i>cuju</i>.", "the <u>Yellow</u> Emperor", "Huangdi; Huang Di; Xuanyuan",
  img="huangdi", conf="the Jade Emperor (ruler of heaven)")
Q(E, 2, "mid", "Born from lightning out of the Big Dipper, this sovereign ascended to heaven as a dragon; a founding text of "
  "Chinese medicine bears his name.", "the <u>Yellow</u> Emperor", "Huangdi",
  extra="The text is <i>The Yellow Emperor's Inner Canon</i> (<i>Huangdi Neijing</i>).")
Q("Huangdi Neijing", 2, "mid", "This foundational text of Chinese medicine and acupuncture is named after the Yellow Emperor.",
  "<i><u>Huangdi Neijing</u></i>", "<i>Yellow Emperor's Inner Canon</i>; <i>Inner Classic</i>", kind="work")
Q(E, 2, "mid", "This sovereign defeated the bronze-headed Chiyou at the Battle of Zhuolu.", "the <u>Yellow</u> Emperor",
  "Huangdi", extra="He avenged the Yan Emperor, whom Chiyou's Nine Li tribes had beaten.")
Q("Chiyou", 2, "mid", "This four-eyed, bronze-headed tyrant led the Nine Li and could darken the sky by breathing out fog.",
  "<u>Chiyou</u>", "Chi You; Ch'ih-yu", conf="Gonggong")
Q("Battle of Zhuolu", 2, "mid", "At this battle the Yellow Emperor called on the drought demon Nüba to dispel Chiyou's storm.",
  "Battle of <u>Zhuolu</u>", "Zhuolu", kind="event", extra="My notes call it the second recorded battle in Chinese history. "
  "The first is Banquan, where the Yellow Emperor beat the Yan Emperor.")
Q("south-pointing chariot", 2, "mid", "To find his way through Chiyou's fog at Zhuolu, the Yellow Emperor built this vehicle.",
  "the <u>south-pointing chariot</u>", "compass chariot", kind="thing", src="qb")
Q("Battle of Banquan", 3, "lead", "At this first battle of Chinese legend, the Yellow Emperor defeated the Flame Emperor and "
  "merged their clans into the Huaxia.", "Battle of <u>Banquan</u>", "", kind="event", src="qb")
Q("Cangjie", 2, "mid", "This four-eyed scribe of the Yellow Emperor invented writing; millet rained from the sky and ghosts wailed.",
  "<u>Cangjie</u>", "Ts'ang Chieh", src="notes", extra="The rain of millet and wailing ghosts are from the qbreader clues.")
Q("Leizu", 2, "mid", "This consort of the Yellow Emperor invented sericulture after a silkworm cocoon fell into her tea.",
  "<u>Leizu</u>", "Lei Zu; Xiling", src="notes")
Q("silk", 2, "mid", "Leizu, the Yellow Emperor's wife, is credited with inventing the making of this material.",
  "<u>silk</u>", "sericulture", kind="thing")
Q("Huaxia", 3, "lead", "The Yellow Emperor is considered the father of these tribes, the most ancient ancestors of the Chinese.",
  "the <u>Huaxia</u>", "Hua-Hsia", kind="concept")
Q("Xingtian", 4, "lead", "Beheaded by the Yellow Emperor, this giant fights on with his nipples for eyes and his navel for a mouth.",
  "<u>Xingtian</u>", "Hsing-t'ien", src="qb")

E = "Five Emperors"
Q("Shaohao", 4, "lead", "In some lists, this son of the Yellow Emperor is the first of the Five Emperors.", "<u>Shaohao</u>", "Shao Hao",
  conf="Shiji's list, which has the Yellow Emperor himself")
Q("Zhuanxu", 3, "lead", "This second of the Five Emperors improved astronomy and the calendar, and was succeeded by Di Ku.",
  "<u>Zhuanxu</u>", "Chuan-hsü")
Q("Yao", 1, "give", "Confucius considered this sage king the ultimate benevolent ruler; he passed the throne to Shun.",
  "<u>Yao</u>", "Emperor Yao; Tang Yao", extra="He passed over his own son Danzhu, and gave Shun his daughters Ehuang and Nüying.")
Q("Shun", 1, "give", "This last of the Five Emperors handed his title to Yu the Great.", "<u>Shun</u>", "Emperor Shun",
  extra="This kind of handover by merit is called abdication (<i>shanrang</i>).")
Q("Shun", 2, "mid", "Famed for filial piety toward a father and stepbrother who tried to kill him, this sage king banished the "
  "Four Perils.", "<u>Shun</u>", "", src="qb")
Q("Ehuang and Nüying", 3, "lead", "Yao's two daughters married Shun; their tears for him made the spotted bamboo of this river, "
  "whose goddesses they became.", "the <u>Xiang</u> River", "Xiang; Xiangjiang", kind="place", src="qb")

E = "Great Flood"
Q("Gun", 2, "mid", "Appointed to stop the Great Flood, this man stole the self-expanding soil <i>xirang</i> from heaven and was "
  "executed on Feather Mountain.", "<u>Gun</u>", "Kun; Count of Chong", src="qb",
  extra="Yu was born from his corpse, which did not rot for three years.")
Q("xirang", 3, "lead", "Gun built dams out of this magical self-expanding soil, which he stole from heaven.",
  "<u>xirang</u>", "breathing soil", kind="thing", src="qb")
Q("Yu the Great", 1, "give", "This founder of the Xia dynasty ended the Great Flood by dredging channels instead of building dams.",
  "<u>Yu</u> the Great", "Da Yu; Yu the Engineer", img="yu", src="qb",
  extra="He worked for 13 years and passed his own door three times without going in.")
Q("Yu the Great", 2, "mid", "This flood-tamer killed Gonggong's nine-headed minister Xiangliu and cast the Nine Tripods for the "
  "nine provinces.", "<u>Yu</u> the Great", "Da Yu", src="qb")
Q("Nine Tripods", 2, "mid", "Yu the Great cast these bronze vessels, one for each province, which later became symbols of the right to rule.",
  "the <u>Nine Tripods</u>", "Jiuding; nine cauldrons", kind="thing", src="qb")
Q("Dragon Gate", 2, "mid", "A carp that leaps this waterfall on the Yellow River, cut by Yu, becomes a dragon — an idiom said to exam candidates.",
  "the <u>Dragon Gate</u>", "Longmen", kind="place", src="qb")
Q("Four Mountains", 4, "lead", "On the advice of these advisors, Emperor Yao appointed Gun to stop the flood.",
  "the <u>Four Mountains</u>", "Siyue", kind="concept", src="qb")

# =====================================================================================
# Legends
# =====================================================================================
E = "White Snake"
Q(E, 2, "give", "In this legend, the snake spirit Bai Suzhen takes human form and falls in love with Xu Xian.",
  "the Legend of the <u>White Snake</u>", "<i>Baishe Zhuan</i>; Madame White Snake")
Q("Leifeng Pagoda", 3, "lead", "At the end of the White Snake legend, the monk Fahai imprisons Bai Suzhen under this pagoda on West Lake.",
  "<u>Leifeng</u> Pagoda", "", kind="place", src="qb")
L("Four Great Folktales", 3, "The Four Great Folktales of China",
  [("the Cowherd and the Weaver Girl", "the magpie bridge"), ("the White Snake", "Bai Suzhen and Xu Xian"),
   ("Lady Meng Jiang", "wept down the Great Wall"), ("the Butterfly Lovers", "Liang Shanbo and Zhu Yingtai")],
  ordered=False, src="qb")

E = "Jade Emperor"
Q(E, 1, "give", "This primordial god heads the celestial bureaucracy of Chinese heaven.", "the <u>Jade</u> Emperor",
  "Yu Huang; Yudi; Tian Gong", img="jade_emperor", conf="the Yellow Emperor")
Q(E, 3, "lead", "In Daoist theology, this ruler of heaven assists Yuanshi Tianzun, one of the Three Pure Ones; he gained Golden "
  "Immortality after aeons of helping the needy.", "the <u>Jade</u> Emperor", "Yu Huang")
L("Three Pure Ones", 3, "The Three Pure Ones (<i>Sanqing</i>), the highest Daoist gods",
  [("Yuanshi Tianzun", "Jade Purity"), ("Lingbao Tianzun", "Supreme Purity"),
   ("Daode Tianzun", "= Taishang Laojun, the deified Laozi")], src="qb")
Q(E, 1, "give", "This ruler of heaven held the Great Race that decided the order of the zodiac.", "the <u>Jade</u> Emperor",
  "Yu Huang", src="notes")

E = "Cowherd and Weaver Girl"
Q("Zhinü", 1, "give", "This daughter of the Jade Emperor, linked with the star Vega, was separated from her cowherd husband by "
  "the Milky Way.", "the <u>Weaver Girl</u>", "Zhinü; Zhi Nu", img="cowherd")
Q("Niulang", 2, "mid", "This lonely cowherd, linked with the star Altair, stole a heavenly maiden's robe while she bathed.",
  "the <u>Cowherd</u>", "Niulang; Niu Lang", extra="In the qbreader version, his talking ox told him where she bathed.")
Q("magpies", 1, "give", "Once a year these birds form a bridge across the Milky Way so the Cowherd and the Weaver Girl can meet.",
  "<u>magpies</u>", "", kind="thing")
Q("Qixi", 2, "mid", "This festival, 'Chinese Valentine's Day' on the 7th day of the 7th month, celebrates the Cowherd and the "
  "Weaver Girl's yearly reunion.", "<u>Qixi</u>", "Double Seventh; Chilseok (Korea); Tanabata (Japan)", kind="event")
Q("Milky Way", 2, "mid", "The Jade Emperor — or the Queen Mother of the West, with her hairpin — created this to separate two lovers.",
  "the <u>Milky Way</u>", "Silver River", kind="thing")

E = "Four dragons"
Q(E, 3, "lead", "The Jade Emperor trapped four dragons under mountains for bringing rain without permission; they became the "
  "Yellow, Amur (Black), and Pearl rivers and this one.", "the <u>Yangtze</u>", "Chang Jiang; Long River", kind="place")

E = "Chang'e"
Q(E, 1, "give", "This goddess of the moon was the wife of the great archer Hou Yi.", "<u>Chang'e</u>", "Heng'e; Chang-O",
  img="change")
Q(E, 1, "give", "To keep the elixir of immortality from Feng Meng, this woman swallowed it herself and floated up to the moon.",
  "<u>Chang'e</u>", "Heng'e", extra="She lives there with the Jade Rabbit.")
Q("Hou Yi", 1, "give", "This archer shot down nine of the ten suns, leaving one to give light.", "Hou <u>Yi</u>",
  "Houyi; Yi; Shen Yi", img="houyi", conf="Yi of Youqiong, who usurped the Xia throne")
Q("three-legged crow", 2, "mid", "The ten suns that Hou Yi shot down, born to the goddess Xihe, are often depicted as these "
  "three-legged animals.", "<u>crow</u>s", "three-legged crows; sanzuwu; ravens", kind="thing")
Q("Queen Mother of the West", 1, "give", "This goddess gave Hou Yi an elixir of immortality made from her peaches, which Chang'e drank.",
  "Queen Mother of the <u>West</u>", "Xiwangmu", img="xiwangmu")
Q("Feng Meng", 2, "mid", "This apprentice of Hou Yi tried to steal his master's elixir and later killed him with a peach-wood club.",
  "<u>Feng</u> Meng", "Peng Meng; Beng Meng")
Q("Jade Rabbit", 1, "give", "This animal lives with Chang'e on the moon, pounding the elixir of life with a mortar and pestle.",
  "the <u>Jade Rabbit</u>", "Yutu; Moon Rabbit; Tu'er Ye", kind="figure")
Q("moon", 1, "give", "Chang'e, Wu Gang, and the Jade Rabbit all live on this celestial body.", "the <u>moon</u>", "",
  kind="thing", extra="Quizbowl's common link pairs it with Tsukuyomi, Chandra, Selene, and Artemis.")
Q("Mid-Autumn Festival", 1, "give", "On the 15th day of the 8th lunar month, this harvest festival offers mooncakes and "
  "lanterns to Chang'e.", "<u>Mid-Autumn</u> Festival", "Moon Festival; Zhongqiu; Chuseok (Korea)", kind="event")
Q("Wu Gang", 2, "mid", "This 'Chinese Sisyphus' endlessly chops at a self-healing osmanthus tree on the moon, punished for "
  "abandoning his pursuit of immortality.", "<u>Wu</u> Gang", "Wu Kang")
Q("Fusang", 3, "lead", "Ten sun-crows roosted in this world tree in the far east; nine rested while the tenth carried the sun.",
  "<u>Fusang</u>", "", kind="place")
Q("Kuafu", 3, "lead", "This giant chased the sun and died of thirst after draining the Yellow and Wei rivers.", "<u>Kuafu</u>",
  "Kua Fu")
Q("Suiren", 3, "lead", "This culture hero is credited with bringing fire to humanity by drilling wood.", "<u>Suiren</u>",
  "Suirenshi")
Q("Diyu", 2, "give", "Guarded by Ox-Head and Horse-Face, this is the Chinese underworld, also called the Yellow Springs.",
  "<u>Diyu</u>", "Chinese hell; Huangquan", kind="place")
Q("Diyu", 3, "lead", "This 18-level underworld, worst level Avici, is overseen by Yama; joss-paper money is burned for those who live there.",
  "<u>Diyu</u>", "", kind="place")
Q("Tian", 3, "lead", "This Chinese word for 'heaven' or 'sky' names the heavenly realm; the Zhou made it their supreme power.",
  "<i><u>Tian</u></i>", "", kind="concept")
Q("Houji", 3, "lead", "This hero gave millet to humanity, helped Yu control the flood, and founded the Ji clan of the Zhou kings.",
  "<u>Houji</u>", "Hou Ji; Lord Millet", extra="Agriculturalism actually claimed Shennong, not Houji, as my notes had it.")
L("Wu Xing", 2, "The Five Phases (<i>Wu Xing</i>): colour — direction",
  [("wood", "green, east"), ("fire", "red, south"), ("earth", "yellow, centre"), ("metal", "white, west"),
   ("water", "black, north")], extra="This is also the generating order: wood feeds fire, fire makes earth (ash), earth bears metal, metal carries water, water nourishes wood.")
L("Four Symbols", 2, "The Four Symbols — direction",
  [("Azure Dragon", "east"), ("Vermilion Bird", "south"), ("White Tiger", "west"), ("Black Tortoise", "north")],
  extra="The Black Tortoise (Xuanwu) is drawn with a snake coiled around it. Japan calls them Seiryū, Suzaku, Byakko, and Genbu.",
  img="four_symbols", ordered=False)
Q("Four Symbols", 2, "mid", "These four creatures are shown on Han roof-tile ends, one for each of the cardinal directions.",
  "the <u>Four Symbols</u>", "Sixiang; Four Benevolent Animals", pic="four_symbols",
  picq="What set of creatures? Name the one at top left.", kind="concept",
  extra="Top left: the Black Tortoise, with its snake (north). Top right: the Azure Dragon (east). Bottom left: the "
  "White Tiger (west). Bottom right: the Vermilion Bird (south).")
L("Chinese zodiac", 1, "The Chinese zodiac, in order",
  [("rat", "rode the ox, jumped first"), ("ox", ""), ("tiger", ""), ("rabbit", ""), ("dragon", "the only mythical one"),
   ("snake", ""), ("horse", ""), ("goat", ""), ("monkey", ""), ("rooster", ""), ("dog", ""), ("pig", "last")],
  extra="The order was set by the Jade Emperor's Great Race.")
Q("rat", 1, "give", "This animal won the Jade Emperor's Great Race by riding on the ox's back across the river and jumping off first.",
  "the <u>rat</u>", "", kind="thing")
Q("Great Race", 2, "mid", "The cat lost its place in the zodiac when the rat pushed it off the ox during this contest.",
  "the <u>Great Race</u>", "", kind="event", src="qb")

E = "Daoism"
Q("Eight Immortals", 1, "give", "This Daoist group lives on Mount Penglai, on an island in the Bohai Sea.",
  "the <u>Eight Immortals</u>", "Baxian; Pa Hsien", img="eight_immortals")
Q("Zhang Guolao", 2, "mid", "This one of the Eight Immortals rides a white donkey, which he folds up and puts in his pocket.",
  "<u>Zhang Guolao</u>", "Zhang Guo; Elder Zhang Guo")
Q("Li Tieguai", 2, "mid", "While this immortal's soul was away visiting Laozi, his body was cremated, so his soul had to enter "
  "a lame beggar's body and walk with an iron crutch.", "<u>Li Tieguai</u>", "Iron-Crutch Li")
Q("Lü Dongbin", 1, "give", "This leader of the Eight Immortals dreamed a whole life of exile and loss while waiting for yellow millet to cook.",
  "<u>Lü Dongbin</u>", "Lu Dongbin", extra="The episode is the Yellow Millet Dream.")
Q("He Xiangu", 2, "mid", "This only woman of the Eight Immortals became immortal after eating powdered mica (mother-of-pearl).",
  "<u>He Xiangu</u>", "Ho Hsien-ku")
Q("Han Xiangzi", 3, "lead", "Usually shown with a flute, this one of the Eight Immortals was the nephew of the Tang writer Han Yu.",
  "<u>Han Xiangzi</u>", "", src="qb")
Q("Lan Caihe", 3, "lead", "This gender-ambiguous member of the Eight Immortals carries a flower basket.", "<u>Lan Caihe</u>", "", src="qb")
Q("Penglai", 2, "mid", "Qin Shi Huang sent the alchemist Xu Fu across the sea to find this island of the immortals.",
  "<u>Penglai</u>", "Mount Penglai", kind="place", src="qb", extra="Legend says Xu Fu landed in Japan.")
E = "Kitchen God"
Q(E, 1, "give", "Every year just before Chinese New Year, this god returns to heaven to report on each household to the Jade Emperor.",
  "the <u>Kitchen</u> God", "Zao Jun; Zao Shen; Stove God", img="kitchen_god")
Q(E, 1, "give", "Honey is smeared on the lips of a paper effigy of this god, and firecrackers set off on 'Little New Year', to sweeten his report.",
  "the <u>Kitchen</u> God", "Zao Jun")
Q(E, 3, "lead", "In one story this god was blinded by heaven for leaving his wife for a younger woman, and regained his sight when he returned to her.",
  "the <u>Kitchen</u> God", "Zao Jun; Zhang Lang", extra="In the qbreader version, Zhang Lang recognises his ex-wife and throws himself into the hearth.")

L("Buddhist figures", 3, "Chinese Buddhist figures — role",
  [("Guanyin", "bodhisattva of compassion; Avalokiteśvara"), ("Ksitigarbha", "Dizang; vowed to empty the hells"),
   ("Four Heavenly Kings", "guardians of the four directions"), ("Budai", "the Laughing Buddha; Maitreya")], ordered=False,
  extra="These are the headings in my notes that have no text yet; the facts are in the supplement.")

# =====================================================================================
# LITERATURE - Four Great Classical Novels
# =====================================================================================
P = "literature"
L("Four Great Classical Novels", 1, "The Four Great Classical Novels — author",
  [("<i>Romance of the Three Kingdoms</i>", "Luo Guanzhong"), ("<i>Water Margin</i>", "Shi Nai'an"),
   ("<i>Journey to the West</i>", "Wu Cheng'en"), ("<i>Dream of the Red Chamber</i>", "Cao Xueqin")], ordered=False)
L("Four Great Classical Novels (authors)", 1, "Author — novel",
  [("Luo Guanzhong", "<i>Romance of the Three Kingdoms</i>"), ("Shi Nai'an", "<i>Water Margin</i>"),
   ("Wu Cheng'en", "<i>Journey to the West</i>"), ("Cao Xueqin", "<i>Dream of the Red Chamber</i>")], ordered=False)

E = "Romance of the Three Kingdoms"
Q(E, 1, "give", "This 14th-century novel by Luo Guanzhong opens: 'The empire, long divided, must unite; long united, must divide.'",
  "<i><u>Romance of the Three Kingdoms</u></i>", "<i>Sanguo Yanyi</i>",
  conf="<i>Records of the Three Kingdoms</i> (<i>Sanguozhi</i>, Chen Shou's history)", kind="work",
  extra="That opening line was added in Mao Zonggang's 1679 edition.")
Q(E, 1, "give", "This novel centres on Liu Bei and Shu Han in the conflict between the Wu, Shu, and Wei.",
  "<i><u>Romance of the Three Kingdoms</u></i>", "<i>Sanguo Yanyi</i>", kind="work")
Q("Luo Guanzhong", 1, "give", "This author wrote <i>Romance of the Three Kingdoms</i>.", "<u>Luo Guanzhong</u>", "Lo Kuan-chung")
Q("Yellow Turban Rebellion", 1, "give", "The <i>Romance of the Three Kingdoms</i> opens with this late-Han rebellion under Emperor Ling.",
  "the <u>Yellow Turban</u> Rebellion", "", kind="event", extra="Its leader was Zhang Jue (Way of Supreme Peace).")
Q("He Jin", 3, "lead", "This general put Emperor Shao on the throne; the eunuch Ten Attendants killed him, and his supporters "
  "under Dong Zhuo seized Luoyang.", "<u>He Jin</u>", "Ho Chin")
Q("Ten Attendants", 2, "mid", "This group of court eunuchs assassinated He Jin under Emperor Ling.", "the <u>Ten Attendants</u>",
  "Ten Eunuchs; Shichangshi", kind="concept")
Q("Seven-Star Sword", 3, "lead", "Cao Cao borrowed this blade in a failed attempt to assassinate Dong Zhuo.",
  "the <u>Seven-Star Sword</u>", "Seven Treasures Sword", kind="thing")
Q("Diaochan", 2, "mid", "Wang Yun used this dancing maid, his adopted daughter, in a seduction plot to make Lü Bu kill Dong Zhuo.",
  "<u>Diaochan</u>", "Diao Chan")
Q("Lü Bu", 1, "give", "Driven by jealousy over Diaochan, this warrior murdered his adoptive father Dong Zhuo in Chang'an.",
  "<u>Lü Bu</u>", "Lu Bu", conf="Lü Buwei (Qin merchant-chancellor); Lü Meng (Wu general)",
  extra="'Among men, Lü Bu; among horses, Red Hare.'")
Q("Oath of the Peach Garden", 1, "give", "In this pledge, Zhang Fei, Guan Yu, and Liu Bei swear to die together in loyalty to the Han.",
  "the <u>Oath of the Peach Garden</u>", "Peach Garden Oath", kind="event", img="peach_garden",
  extra="They sacrificed a black ox and a white horse.")
Q("Zhuge Liang", 1, "give", "Liu Bei visited this 'Sleeping Dragon' three times at his thatched cottage to recruit him.",
  "<u>Zhuge Liang</u>", "Kongming; Chu-ko Liang; Crouching Dragon; Wolong", img="zhuge")
Q("Three Visits to the Thatched Cottage", 3, "lead", "Liu Bei's repeated recruitment of Zhuge Liang became a classic story under this title.",
  "<i>The <u>Three Visits</u> to the Thatched Cottage</i>", "", kind="work")
Q("Red Cliffs", 1, "give", "Liu Bei and Sun Quan allied to defeat Cao Cao at this battle.", "<u>Red Cliffs</u>", "Chibi",
  kind="event", img="red_cliffs")
Q("Zhuge Liang", 1, "give", "At Red Cliffs, this strategist sent straw-covered boats through the fog to 'borrow' 100,000 arrows from Cao Cao.",
  "<u>Zhuge Liang</u>", "Kongming")
Q("Lady Sun", 3, "lead", "Sun Quan tried to lure Liu Bei to Wu with a marriage to his sister, hoping to take Jing Province; "
  "Zhuge Liang foiled the plot. Name the sister.", "Lady <u>Sun</u>", "Sun Shangxiang")
Q("Guan Yu", 1, "give", "Leaving Cao Cao's service to rejoin Liu Bei, this general 'crossed five passes and slew six generals'.",
  "<u>Guan Yu</u>", "Guan Gong; Guandi; Yunchang", img="guanyu", pic="guanyu", picq="Who? (red face, long beard, halberd)")
Q("Guan Yu", 1, "give", "This general calmly played Go while the physician Hua Tuo scraped poison from his arm, wounded at Fan Castle.",
  "<u>Guan Yu</u>", "Guan Gong")
Q("Hua Tuo", 2, "mid", "This physician scraped the poisoned flesh from Guan Yu's arm while Guan played Go.", "<u>Hua Tuo</u>", "")
Q("Lu Xun (Three Kingdoms)", 3, "lead", "This Wu general defeated Liu Bei's revenge campaign for Guan Yu, but was trapped by Zhuge Liang's Stone Sentinel Maze.",
  "<u>Lu Xun</u>", "", conf="Lu Xun the 20th-century writer")
Q("Stone Sentinel Maze", 3, "lead", "Zhuge Liang's array of rocks that trapped the pursuing Lu Xun.", "the <u>Stone Sentinel Maze</u>",
  "", kind="thing")
Q("Zhuge Liang", 2, "mid", "This strategist tried to add twelve years to his life with a lamp ritual before the Big Dipper, "
  "but Wei Yan knocked out the main lamp.", "<u>Zhuge Liang</u>", "Kongming")
Q("Red Hare", 2, "mid", "This famous red horse belonged to Lü Bu and was later given to Guan Yu.", "<u>Red Hare</u>", "Chitu",
  kind="thing")
Q("Dilu", 3, "lead", "Thought to bring misfortune because of a white mark on its face, this horse saved Liu Bei by leaping a stream.",
  "<u>Dilu</u>", "Hex Mark", kind="thing")
Q("Pang Tong", 3, "lead", "This 'Young Phoenix' was killed after being mistaken for Liu Bei, because he was riding Liu Bei's distinctive horse.",
  "<u>Pang Tong</u>", "Fledgling Phoenix; Fengchu", extra="He had suggested the chained ships to Cao Cao before Red Cliffs.")

Q("Cao Cao", 1, "give", "This warlord, the villain of <i>Romance of the Three Kingdoms</i>, lost the Battle of Red Cliffs.",
  "<u>Cao Cao</u>", "Mengde; Ts'ao Ts'ao", src="qb", img="caocao")
Q("Cao Cao", 2, "mid", "This warlord said, 'I would rather betray the world than let the world betray me.'", "<u>Cao Cao</u>", "", src="qb")
Q("Cao Cao", 2, "mid", "This man told Liu Bei, 'The only heroes in the world are you and I'; Liu Bei dropped his chopsticks and "
  "blamed the thunder.", "<u>Cao Cao</u>", "", src="qb")
Q("Cao Cao", 3, "lead", "This warlord refused Hua Tuo's offer to open his skull to cure his headaches; he built the Bronze Sparrow Terrace.",
  "<u>Cao Cao</u>", "", src="qb")
Q("Liu Bei", 1, "give", "This founder of Shu Han swore the Peach Garden Oath and recruited Zhuge Liang.", "<u>Liu Bei</u>",
  "Xuande; Liu Pei", src="qb")
Q("Zhou Yu", 3, "lead", "This Wu commander planned the fire attack at Red Cliffs and is shown as jealous of Zhuge Liang.",
  "<u>Zhou Yu</u>", "", src="qb")
Q("Huang Gai", 3, "lead", "This Wu general had himself flogged, faked a defection, and sent fire ships into Cao Cao's chained fleet.",
  "<u>Huang Gai</u>", "", src="qb", extra="The trick is the 'self-injury ruse'.")
Q("Empty Fort Strategy", 2, "mid", "Zhuge Liang opened a city's gates and played the zither on its walls, scaring off Sima Yi with this ruse.",
  "the <u>Empty Fort</u> Strategy", "", kind="concept", src="qb")
Q("Meng Huo", 3, "lead", "On his southern campaign, Zhuge Liang captured and released this Nanman chief seven times.", "<u>Meng Huo</u>", "", src="qb")
Q("Sanguozhi", 2, "mid", "Chen Shou's 3rd-century history behind Luo Guanzhong's novel — also the first record of the Japanese queen Himiko.",
  "<i><u>Records of the Three Kingdoms</u></i>", "<i>Sanguozhi</i>", kind="work", src="qb",
  conf="<i>Romance of the Three Kingdoms</i> (<i>Sanguo Yanyi</i>)")
Q("Five Tiger Generals", 3, "lead", "Liu Bei's Five Tiger Generals were Guan Yu, Zhang Fei, Ma Chao, Huang Zhong, and this rescuer of "
  "the infant Liu Shan at Changban.", "<u>Zhao Yun</u>", "Zilong", src="qb")
Q("Guan Yu", 2, "mid", "After death, this general was deified as a god of war, worshipped by police and triads alike.",
  "<u>Guan Yu</u>", "Guandi; Guan Gong", src="qb")
Q("Green Dragon Crescent Blade", 2, "mid", "Guan Yu wielded this halberd.", "the <u>Green Dragon Crescent Blade</u>", "",
  kind="thing", src="qb")
Q("Cao Zhi", 3, "lead", "Ordered to compose a poem in seven steps, this son of Cao Cao compared brothers to beans boiled over their own stalks.",
  "<u>Cao Zhi</u>", "", src="qb", conf="Cao Pi (his brother, founder of Wei)")
T("Romance of the Three Kingdoms", 1, [
    "In this novel, troops are told of imaginary sour plums to make them salivate, and a man interprets the password 'chicken ribs' too well.",
    "A strategist in it captures and releases a southern chief seven times, and later scares off Sima Yi by playing a zither on an open city wall.",
    "Before its great naval battle, a general is flogged in a 'self-injury ruse', and straw boats are used to 'borrow' arrows.",
    "It begins with the Yellow Turban Rebellion and the Oath of the Peach Garden."],
  "For 10 points, name this novel by Luo Guanzhong about the conflict between Wei, Shu, and Wu.",
  "<i><u>Romance of the Three Kingdoms</u></i>", "<i>Sanguo Yanyi</i>", img="peach_garden")

E = "Water Margin"
Q(E, 1, "give", "This Yuan–Ming novel by Shi Nai'an follows 108 outlaws — 36 Heavenly Spirits and 72 Earthly Fiends — at Mount Liang.",
  "<i><u>Water Margin</u></i>", "<i>Outlaws of the Marsh</i>; <i>All Men Are Brothers</i>; <i>Shuihu Zhuan</i>",
  kind="work", img="wusong")
Q(E, 2, "mid", "Sidney Shapiro translated this novel as <i>Outlaws of the Marsh</i>, and Pearl S. Buck as <i>All Men Are Brothers</i>.",
  "<i><u>Water Margin</u></i>", "<i>Shuihu Zhuan</i>", kind="work")
Q("Shi Nai'an", 1, "give", "This author wrote <i>Water Margin</i>.", "<u>Shi Nai'an</u>", "Shih Nai-an")
Q("Suikoden", 3, "lead", "Woodblock illustrations of <i>Water Margin</i> by Kuniyoshi and Hokusai started this Japanese craze for full-body pictorial tattoos.",
  "the <u>Suikoden</u> craze", "Suikoden", kind="concept")
Q(E, 2, "mid", "This novel opens when Marshal Hong moves a tortoise and frees 108 demonic spirits from under a stele.",
  "<i><u>Water Margin</u></i>", "", kind="work")
Q("Gao Qiu", 2, "mid", "This former street urchin rose to Grand Marshal by impressing the future Emperor Huizong at <i>cuju</i>, "
  "and is the chief villain of <i>Water Margin</i>.", "<u>Gao Qiu</u>", "Kao Ch'iu")
Q("Fang La", 3, "lead", "The outlaws of <i>Water Margin</i>, after accepting amnesty, are sent to crush this rebel leader; most of them die.",
  "<u>Fang La</u>", "")
Q("Chao Gai", 3, "lead", "This leader of the 'Original Seven' robbed a convoy of birthday gifts by drugging the escorts' wine.",
  "<u>Chao Gai</u>", "")
Q("Song Jiang", 1, "give", "This outlaw leader of <i>Water Margin</i> is tattooed on the face after he is convicted of murdering his concubine Yan Poxi.",
  "<u>Song Jiang</u>", "Sung Chiang; Timely Rain")
Q("Li Kui", 2, "mid", "This fierce outlaw, the 'Black Whirlwind', fights with two axes.", "<u>Li Kui</u>", "Black Whirlwind; Iron Ox")
Q("Wu Song", 1, "give", "This outlaw drinks 18 bowls of wine and then kills a man-eating tiger with his bare hands.",
  "<u>Wu Song</u>", "Wu Sung", img="wusong", pic="wusong", picq="Which <i>Water Margin</i> hero?")
Q("Jin Ping Mei", 1, "give", "Wu Song's story with his sister-in-law Pan Jinlian was expanded into this late-Ming erotic novel.",
  "<i>The <u>Plum in the Golden Vase</u></i>", "<i>Jin Ping Mei</i>; <i>The Golden Lotus</i>", kind="work",
  extra="It was written by the pseudonymous 'Scoffing Scholar of Lanling'. Its hero, Ximen Qing, dies of an aphrodisiac overdose.")
Q("Shi Jin", 3, "lead", "This outlaw has his torso covered in tattoos of nine dragons.", "<u>Shi Jin</u>", "Nine Dragons")
Q("Loyalty Hall", 4, "lead", "This is the outlaws' central meeting place at Liangshan Marsh.", "the <u>Loyalty</u> Hall",
  "Hall of Loyalty and Righteousness", kind="place")
Q("Lin Chong", 3, "lead", "This drill instructor, 'Panther Head', was framed by Gao Qiu for carrying a sword into the White Tiger Hall.",
  "<u>Lin Chong</u>", "", src="qb")
Q("Lu Zhishen", 3, "lead", "This tattooed 'Flowery Monk' killed a butcher with three punches and uprooted a willow tree.",
  "<u>Lu Zhishen</u>", "Sagacious Lu", src="qb")
Q("Sun Erniang", 3, "lead", "This 'Ogress' and her husband run an inn at Cross Slope that serves buns of human flesh.",
  "<u>Sun Erniang</u>", "", src="qb")
T("Water Margin", 1, [
    "In this novel, a couple run an inn at Cross Slope where they drug their guests and serve their flesh in buns.",
    "A former street urchin in it becomes Grand Marshal after impressing a prince at football.",
    "It opens when a stone tortoise is moved and a black cloud of spirits bursts out; one of its heroes drinks 18 bowls of wine and kills a tiger.",
    "Its Heavenly Spirits and Earthly Fiends gather at Mount Liang under Song Jiang."],
  "For 10 points, name this novel by Shi Nai'an about 108 outlaws.",
  "<i><u>Water Margin</u></i>", "<i>Outlaws of the Marsh</i>; <i>All Men Are Brothers</i>", img="wusong")

E = "Journey to the West"
Q(E, 1, "give", "This Ming novel by Wu Cheng'en fictionalises the monk Xuanzang's pilgrimage to India for Buddhist sutras.",
  "<i><u>Journey to the West</u></i>", "<i>Xiyouji</i>; <i>Monkey</i>", kind="work", img="jttw")
Q(E, 2, "mid", "Arthur Waley's abridged translation of this novel is titled <i>Monkey</i>.", "<i><u>Journey to the West</u></i>",
  "<i>Xiyouji</i>", kind="work")
Q("Wu Cheng'en", 1, "give", "This author wrote <i>Journey to the West</i>.", "<u>Wu Cheng'en</u>", "Wu Ch'eng-en")
Q("Xuanzang", 2, "mid", "In a past life, the pilgrim monk of <i>Journey to the West</i> was a disciple of the Buddha called "
  "'Golden Cicada'. Name the monk.", "<u>Xuanzang</u>", "Tang Sanzang; Tang Seng; Tripitaka",
  conf="Emperor Xuanzong of Tang")
Q("Sun Wukong", 1, "give", "This monkey, born from a stone egg on Flower Fruit Mountain, called himself 'Great Sage Equal to Heaven'.",
  "<u>Sun Wukong</u>", "the Monkey King; Qitian Dasheng", img="wukong", pic="wukong", picq="Who?")
Q("Sun Wukong", 1, "give", "This character masters 72 transformations and the secrets of immortality.", "<u>Sun Wukong</u>", "Monkey King")
Q("Sun Wukong", 2, "mid", "This monkey earned the title 'Handsome Monkey King' by bravely entering the Water Curtain Cave.",
  "<u>Sun Wukong</u>", "")
Q("Sun Wukong", 1, "give", "Set to guard the Peach Garden of Immortality, this character ate the ripe peaches, then lost a bet "
  "that he could somersault out of the Buddha's hand.", "<u>Sun Wukong</u>", "")
Q("Five Elements Mountain", 2, "mid", "After losing his bet with the Buddha, Sun Wukong is trapped under a mountain for this long.",
  "<u>500</u> years", "five hundred", kind="thing")
Q("Ruyi Jingu Bang", 1, "give", "Sun Wukong's staff, which can shrink to a needle in his ear or grow huge.", "the <u>Ruyi Jingu Bang</u>",
  "Ruyi Bang; Jingu Bang; golden-banded staff", kind="thing")
Q("Ruyi Jingu Bang", 2, "mid", "Yu the Great once used this rod to measure the depth of the flood; it later held up the Dragon King "
  "of the East Sea's palace.", "the <u>Ruyi Jingu Bang</u>", "Sun Wukong's staff", kind="thing")
Q("Guanyin", 2, "mid", "This bodhisattva frees Sun Wukong from under the mountain to join Tang Sanzang, and gives the monk the headband to control him.",
  "<u>Guanyin</u>", "Avalokiteśvara; Kannon")
Q("Zhu Bajie", 1, "give", "This second disciple of Tang Sanzang, 'Pigsy', was banished to earth for harassing Chang'e; he fights "
  "with a nine-toothed iron rake.", "<u>Zhu Bajie</u>", "Pigsy; Zhu Wuneng",
  extra="'Bajie' means 'Eight Precepts'. His dharma name, Zhu Wuneng, means 'Pig Awakened to Power'.")
Q("Zhu Bajie", 2, "mid", "At the end of the journey this lazy glutton is made Cleanser of the Altars, so he can eat the leftover offerings.",
  "<u>Zhu Bajie</u>", "Pigsy")
Q("Zhu Bajie", 3, "lead", "Posing as a handsome young man, this pilgrim married a maiden at Gao Family Village, but his appetite and true form gave him away.",
  "<u>Zhu Bajie</u>", "Pigsy")
Q("Sha Wujing", 2, "mid", "This third disciple, 'Sandy', was banished for dropping the Queen Mother of the West's crystal goblet.",
  "<u>Sha Wujing</u>", "Sandy; Friar Sand; Sha Seng")
Q("White Dragon Horse", 3, "lead", "The fourth disciple, a son of the Dragon King of the West Sea, becomes the monk's mount.",
  "the <u>White Dragon Horse</u>", "Bailongma")
Q("Vulture Peak", 3, "lead", "After 81 tribulations, the pilgrims receive the scriptures from the Buddha at this mountain in India.",
  "<u>Vulture Peak</u>", "Gridhrakuta", kind="place")
Q("Sun Wukong", 2, "mid", "Made 'Keeper of the Heavenly Horses', this character was furious at the lowly post and freed the horses.",
  "<u>Sun Wukong</u>", "", src="qb")
Q("Sun Wukong", 2, "mid", "Forty-nine days in Laozi's Eight Trigrams Furnace gave this character 'fiery eyes and golden pupils' "
  "that see through disguises.", "<u>Sun Wukong</u>", "", src="qb")
Q("Sun Wukong", 2, "mid", "Thinking he had reached the edge of the world, this character wrote his name on a pillar and urinated on "
  "it — but it was the Buddha's finger.", "<u>Sun Wukong</u>", "", src="qb")
Q("Sun Wukong", 3, "lead", "This character erased his own name and others' from the Book of Life and Death.", "<u>Sun Wukong</u>", "", src="qb")
Q("White Bone Demon", 2, "mid", "This shapeshifter of <i>Journey to the West</i> disguises herself as a girl, her mother, and her "
  "father to get at Tang Sanzang.", "the <u>White Bone Demon</u>", "Baigujing", src="qb")
Q("Princess Iron Fan", 2, "mid", "Her banana-leaf fan is the only thing that can put out the Flaming Mountains.",
  "<u>Princess Iron Fan</u>", "Tieshan Gongzhu; Rakshasi", src="qb", extra="Her husband is the Bull Demon King, and their son is Red Boy.")
Q("headband", 2, "mid", "Tang Sanzang controls Sun Wukong by chanting a spell that tightens this object.", "the <u>headband</u>",
  "golden fillet; circlet; Tightening-Crown Spell", kind="thing", src="qb")
Q("Kingdom of Women", 3, "lead", "In this kingdom of <i>Journey to the West</i>, drinking from a river makes the pilgrims pregnant.",
  "the <u>Kingdom of Women</u>", "Nüerguo", kind="place", src="qb")
Q("Erlang Shen", 3, "lead", "This three-eyed god, with his Howling Celestial Dog, captured the rebellious Sun Wukong.",
  "<u>Erlang</u> Shen", "Lord Erlang", src="qb")
T("Journey to the West", 1, [
    "In a supplement to this novel, a character is trapped in a fish demon's dream world; in the novel, an old turtle dumps the scriptures in a river.",
    "A man in it, once Marshal Tianpeng, was banished for flirting with the moon goddess and later carries a nine-toothed rake.",
    "A character in it urinates on five pillars that turn out to be the Buddha's fingers, and is sealed under a mountain for 500 years.",
    "Pigsy and Sandy join a monkey in protecting a monk on his way to Vulture Peak."],
  "For 10 points, name this novel by Wu Cheng'en in which Sun Wukong accompanies Xuanzang to India.",
  "<i><u>Journey to the West</u></i>", "<i>Xiyouji</i>; <i>Monkey</i> before mention", img="jttw")
T("Sun Wukong", 1, [
    "This figure defeats a six-eared macaque double that is identical to him.",
    "He is cooked for 49 days in Laozi's furnace, gaining eyes that see through disguises, and is captured by Erlang Shen.",
    "Insulted by the post of Keeper of the Heavenly Horses, he declares himself 'Great Sage Equal to Heaven'.",
    "Born from a stone egg, he wields a size-changing staff."],
  "For 10 points, name this Monkey King of <i>Journey to the West</i>.", "<u>Sun Wukong</u>", "the Monkey King", img="wukong")

E = "Dream of the Red Chamber"
Q(E, 1, "give", "This 18th-century novel by Cao Xueqin observes aristocratic life in the High Qing through the Jia clan.",
  "<i><u>Dream of the Red Chamber</u></i>", "<i>Story of the Stone</i>; <i>Honglou Meng</i>", kind="work", img="daiyu")
Q("Cao Xueqin", 1, "give", "This author wrote <i>Dream of the Red Chamber</i>.", "<u>Cao Xueqin</u>", "Ts'ao Hsüeh-ch'in")
Q("Redology", 2, "mid", "This is the name of the scholarly field devoted entirely to <i>Dream of the Red Chamber</i>.",
  "<u>Redology</u>", "hongxue", kind="concept")
Q("Gao E", 3, "lead", "First written as eighty chapters, <i>Dream of the Red Chamber</i> was published in the 1790s with forty "
  "added chapters by Cheng Weiyuan and this man.", "<u>Gao E</u>", "Gao O")
Q("Zhiyanzhai", 3, "lead", "The 'Rouge' (Red Inkstone) manuscripts of <i>Dream of the Red Chamber</i> carry commentary by this writer.",
  "<u>Zhiyanzhai</u>", "Red Inkstone; Rouge Inkstone")
Q("David Hawkes", 3, "lead", "This translator of <i>The Story of the Stone</i> gave characters Latinate names like Sapientia and Adamantina.",
  "David <u>Hawkes</u>", "")
Q(E, 2, "mid", "This novel's first chapter opens with a couplet: 'Truth becomes fiction when the fiction's true.'",
  "<i><u>Dream of the Red Chamber</u></i>", "<i>Story of the Stone</i>", kind="work")
Q("Jia Baoyu", 1, "give", "In this novel's frame story, a sentient stone left over when Nüwa mended the heavens is born as this "
  "character, 'Precious Jade', with a jade in his mouth.", "<u>Jia Baoyu</u>", "Pao-yu; Baoyu")
Q("Prospect Garden", 2, "mid", "Inside the Rongguo mansion of the Jia clan lies this huge garden, the Daguanyuan.",
  "the <u>Prospect</u> Garden", "Grand View Garden; Daguanyuan", kind="place")
Q("Lin Daiyu", 1, "give", "Baoyu loves this sickly, melancholy cousin, but is forced to marry another cousin, Xue Baochai.",
  "<u>Lin Daiyu</u>", "Black Jade; Tai-yu", img="daiyu", pic="daiyu", picq="Who is burying the flowers?")
Q("Lin Daiyu", 2, "mid", "This cousin of Baoyu is the reincarnation of the Crimson Pearl Flower, which he watered in a past life; "
  "she repays him with tears.", "<u>Lin Daiyu</u>", "")
Q("Xue Baochai", 2, "mid", "Baoyu is tricked into marrying this cousin, whose golden locket matches his jade.", "<u>Xue Baochai</u>",
  "Precious Clasp", src="notes")
Q("Twelve Beauties of Jinling", 3, "lead", "The main female characters of <i>Dream of the Red Chamber</i> are known by this collective name.",
  "the <u>Twelve Beauties of Jinling</u>", "", kind="concept")
Q("Lin Daiyu", 2, "mid", "This woman buries fallen flower petals and writes a poem asking 'who will bury me?'", "<u>Lin Daiyu</u>", "", src="qb")
Q("Wang Xifeng", 3, "lead", "This scheming manager of the Jia household, 'Phoenix', engineers the switch that marries Baoyu to Baochai.",
  "<u>Wang Xifeng</u>", "Phoenix; Sister Feng", src="qb")
T("Dream of the Red Chamber", 1, [
    "An early commentator on this novel used the pen name 'Red Inkstone'; its namesake '-ology' disputes its last forty chapters.",
    "Its characters form a Crab-Flower Poetry Club, and a begonia blooming out of season is a bad omen.",
    "A sickly woman in it writes an elegy for flower petals she buries.",
    "Its hero, born with a piece of jade in his mouth, loves Lin Daiyu but marries Xue Baochai."],
  "For 10 points, name this novel by Cao Xueqin about Jia Baoyu.",
  "<i><u>Dream of the Red Chamber</u></i>", "<i>Story of the Stone</i>; <i>Honglou Meng</i>", img="daiyu")

# =====================================================================================
# The Classics
# =====================================================================================
L("Five Classics", 1, "The Five Classics — what it is",
  [("<i>Classic of Poetry</i>", "poems and folk songs (<i>Shijing</i>)"),
   ("<i>Book of Documents</i>", "speeches of early Zhou and older rulers; the first Chinese narrative"),
   ("<i>Book of Rites</i>", "ancient rites and ceremonies"), ("<i>I Ching</i>", "a divination system"),
   ("<i>Spring and Autumn Annals</i>", "the state of Lu's chronicle, attributed to Confucius")], ordered=False,
  extra="They were the Western Han curriculum: Emperor Wu gave each a chair of erudites in 136 BC.")
L("Four Books", 1, "The Four Books (chosen by Zhu Xi) — what it is",
  [("<i>Great Learning</i>", "a chapter of the <i>Book of Rites</i>; Confucius and Zengzi"),
   ("<i>Doctrine of the Mean</i>", "from the <i>Book of Rites</i>; by Zisi, Confucius's grandson"),
   ("<i>Analects</i>", "sayings of Confucius"), ("<i>Mencius</i>", "dialogues of Mencius")], ordered=False,
  extra="They were the imperial-exam syllabus from 1313 (Yuan) until 1905.")
Q("Zhu Xi", 1, "give", "This Song Neo-Confucian chose the Four Books.", "<u>Zhu Xi</u>", "Chu Hsi")
Q("Zisi", 3, "lead", "This grandson of Confucius is credited with the <i>Doctrine of the Mean</i>.", "<u>Zisi</u>", "Kong Ji", src="notes")
Q("I Ching", 1, "give", "This classic of divination has 64 hexagrams, built from Fuxi's eight trigrams.", "the <i><u>I Ching</u></i>",
  "<i>Yijing</i>; <i>Book of Changes</i>; <i>Zhouyi</i>", kind="work", extra="John Cage used it to compose by chance in "
  "<i>Music of Changes</i>; Jung wrote the foreword to the Wilhelm translation.")
Q("Spring and Autumn Annals", 1, "give", "This chronicle of the state of Lu, traditionally by Confucius, names a period of Chinese history.",
  "<i><u>Spring and Autumn Annals</u></i>", "<i>Chunqiu</i>", kind="work", extra="Three commentaries explain it: the Zuo, the Gongyang, and the Guliang.")
Q("Classic of Poetry", 1, "give", "This collection of 305 poems and folk songs opens with 'Guanju' (the ospreys).",
  "<i><u>Classic of Poetry</u></i>", "<i>Book of Songs</i>; <i>Shijing</i>; <i>Book of Odes</i>", kind="work", src="qb")
Q("Liu Xiang", 3, "lead", "This Han scholar compiled the imperial library catalogue and the <i>Strategies of the Warring States</i>.",
  "<u>Liu Xiang</u>", "Liu Hsiang", extra="My notes say he edited the <i>Mountains and Seas</i>; that was his son, Liu Xin.")
Q("Classic of Mountains and Seas", 2, "mid", "This mythic geography and bestiary describes Xingtian, the nine-tailed fox, and "
  "the Queen Mother of the West.", "<i><u>Classic of Mountains and Seas</u></i>", "<i>Shanhaijing</i>", kind="work", src="qb")
Q("Thirteen Classics", 3, "lead", "This expanded canon — the Five Classics, plus texts such as the <i>Erya</i> and the "
  "<i>Classic of Filial Piety</i> — was settled under the Song.", "the <u>Thirteen Classics</u>", "", kind="concept",
  extra="My notes credit it to the Ming exams; those were set on the Four Books and Five Classics.")

# =====================================================================================
# Supplement-only mythology (qbreader gaps), active at tier 1-2
# =====================================================================================
P = "mythology"
Q("Mazu", 2, "give", "This sea goddess from Meizhou Island, Fujian, born Lin Moniang, protects sailors and is called Tianhou.",
  "<u>Mazu</u>", "Lin Moniang; Tianhou; Tianfei; Tin Hau", src="qb", img="mazu")
Q("Nezha", 2, "mid", "Born from a ball of flesh after a 42-month pregnancy, this boy god rides Wind Fire Wheels and killed the "
  "Dragon King's third son.", "<u>Nezha</u>", "Third Lotus Prince", src="qb")
Q("Ao Guang", 2, "mid", "This Dragon King of the East Sea gave Sun Wukong his staff.", "<u>Ao Guang</u>", "Dragon King of the East Sea", src="qb")
Q("Investiture of the Gods", 2, "mid", "In this Ming 'gods and demons' novel, Jiang Ziya helps the Zhou overthrow King Zhou of Shang "
  "and his fox-possessed consort Daji.", "<i><u>Investiture of the Gods</u></i>", "<i>Fengshen Yanyi</i>", kind="work", src="qb")
Q("Daji", 2, "mid", "Possessed by a fox spirit, this consort of King Zhou of Shang invented the <i>paolao</i>, a heated bronze pillar used for torture.",
  "<u>Daji</u>", "Da Ji", src="qb")
Q("huli jing", 2, "mid", "These Chinese spirits, often nine-tailed, match the Japanese kitsune and Korean kumiho.",
  "<u>fox spirits</u>", "huli jing; nine-tailed foxes", kind="thing", src="qb")
Q("Queen Mother of the West", 2, "mid", "Her immortality peaches on Mount Kunlun ripen every 3,000 years; Sun Wukong ruins her Peach Banquet.",
  "Queen Mother of the <u>West</u>", "Xiwangmu", src="qb")
Q("Kunlun", 2, "mid", "This mountain, an axis mundi of Chinese myth, is home to the Queen Mother of the West.", "<u>Kunlun</u>",
  "Mount Kunlun", kind="place", src="qb")
Q("peaches", 1, "give", "The Queen Mother of the West grows these fruits of immortality, which Sun Wukong steals.", "<u>peach</u>es",
  "peaches of immortality; pantao", kind="thing", src="qb")
Q("Nian", 2, "mid", "This beast came each New Year until people learned it feared red, noise, and fire — the origin of firecrackers and red couplets.",
  "<u>Nian</u>", "Nian shou", src="qb")
Q("Yinglong", 3, "lead", "This winged dragon fought for the Yellow Emperor at Zhuolu and helped Yu the Great dig channels with his tail.",
  "<u>Yinglong</u>", "Ying Long", src="qb")
Q("Xiangliu", 3, "lead", "Yu the Great killed this nine-headed serpent minister of Gonggong.", "<u>Xiangliu</u>", "", src="qb")
Q("Di Jun", 3, "lead", "With the goddess Xihe, this god fathered the ten sun-crows that Hou Yi shot down.", "<u>Di Jun</u>", "Emperor Jun", src="qb")
Q("Zhong Kui", 3, "lead", "Refused office for his ugliness after topping the imperial exam, this man killed himself and became a demon-queller painted on doors.",
  "<u>Zhong Kui</u>", "", src="qb")
Q("Meng Po", 3, "lead", "In Diyu, this old woman serves the Soup of Forgetfulness to souls before they are reborn.", "<u>Meng Po</u>", "", src="qb")
Q("Erlang Shen", 4, "lead", "This god's Howling Celestial Dog bit Sun Wukong's calf; he is linked to Li Bing of the Dujiangyan.",
  "<u>Erlang</u> Shen", "", src="qb")
Q("Jiang Ziya", 3, "lead", "This strategist fished with a straight hook until King Wen hired him; in <i>Investiture of the Gods</i> "
  "he holds the List of Investiture.", "<u>Jiang Ziya</u>", "Jiang Taigong; Taigong Wang", src="qb")
