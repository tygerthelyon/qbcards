# -*- coding: utf-8 -*-
"""cards_china_zhou.py -- History v2 cards for China: the Zhou (Western Zhou, Spring and Autumn, Warring
States, and the Hundred Schools of Thought).

From notes/04_zhou_supplement.md (the qbreader sweep), with its corrections applied: hezong (vertical) was
against Qin, lianheng (horizontal) with Qin; the Three Guards rebelled against the Duke of Zhou's regency;
Spring and Autumn = 770-476 BC; Bai Qi served the state of Qin. All src="qb": tier 1-2 go into the queue,
tier 3-4 are added suspended. Left out unless asked:  py -3.9 hist_qb_apply.py --include zhou
Clues the old History Clue notes already give (the Duke of Zhou as regent, hezong/lianheng, Confucius,
Mencius's child at the well, the butterfly dream, wu wei, the white horse...) are left out, so this adds only
new angles. Don't run --supersede for this period: the old notes are the main cards.
Already in cards_china_myth_lit.py, so not repeated here: Houji, Jiang Ziya, the I Ching, the Spring and
Autumn Annals, the Classic of Poetry, Zisi, and the Queen Mother of the West.
"""
import cards_china_myth_lit as base

NOTES = []


def _wrap(fn, period):
    def inner(*a, **k):
        start = len(base.NOTES)
        k.setdefault("period", period)
        k.setdefault("src", "qb")
        fn(*a, **k)
        NOTES.extend(base.NOTES[start:])
        del base.NOTES[start:]
    return inner


Q, L, T = _wrap(base.Q, "zhou"), _wrap(base.L, "zhou"), _wrap(base.T, "zhou")
P = "zhou-philosophy"   # the Hundred Schools get their own period tag

# =====================================================================================
# WESTERN ZHOU
# =====================================================================================
T("Duke of Zhou", 1, [
    "In the 'Metal-Bound Coffer' chapter of the <i>Book of Documents</i>, this man offers his own life for his sick brother.",
    "He is credited with a ritual code of 360 offices and a popular dream-interpretation book, and built the eastern capital Chengzhou.",
    "Guanshu, Caishu, and Huoshu rebelled against his regency, and he crushed them.",
    "Confucius lamented that he no longer dreamed of this man."],
  "For 10 points, name this brother of King Wu who served as regent for the boy King Cheng, then stepped aside.",
  "Duke of <u>Zhou</u>", "Zhou Gong; Ji Dan")
Q("Rites of Zhou", 3, "lead", "This text, credited to the Duke of Zhou, lays out an ideal government of 360 posts under six offices.",
  "<i><u>Rites of Zhou</u></i>", "<i>Zhouli</i>; <i>Zhou guan</i>", kind="work")
Q("King Mu of Zhou", 3, "lead", "This king drove his eight steeds west to visit the Queen Mother of the West.",
  "King <u>Mu</u> of Zhou", "", extra="The story is told in the <i>Mu Tianzi Zhuan</i>.")
Q("King You of Zhou", 1, "give", "To make Bao Si laugh, this king lit the beacon fires as a false alarm, so no one came when the Quanrong attacked in 771 BC.",
  "King <u>You</u> of Zhou", "")
Q("Quanrong", 3, "lead", "With the Marquess of Shen, these people sacked the Western Zhou capital in 771 BC and killed King You.",
  "<u>Quanrong</u>", "Dog Rong", kind="group")
Q("Mao Gong ding", 4, "lead", "This Western Zhou tripod carries the longest known bronze inscription, about 500 characters.",
  "<u>Mao Gong</u> ding", "Duke Mao tripod", kind="thing")

# =====================================================================================
# SPRING AND AUTUMN (770-476 BC)
# =====================================================================================
Q("Spring and Autumn period", 2, "mid", "This period runs from the Zhou move east to Luoyang in 770 BC to 476 BC.",
  "<u>Spring and Autumn</u> period", "Chunqiu period", kind="period", extra="The <i>Annals</i> themselves cover 722–481 BC.")
Q("Guan Zhong", 2, "mid", "This chief minister of Duke Huan of Qi is credited with state salt and iron monopolies and a namesake book.",
  "<u>Guan Zhong</u>", "Guanzi; Guan Yiwu")
L("Five Hegemons", 2, "The Five Hegemons of the Spring and Autumn period (the usual list)",
  [("Duke Huan of Qi", "the first; Guan Zhong"), ("Duke Wen of Jin", "Chengpu"), ("King Zhuang of Chu", ""),
   ("Duke Mu of Qin", ""), ("Duke Xiang of Song", "")], ordered=False,
  extra="Some lists swap in Goujian of Yue and Fuchai of Wu.")
Q("Jie Zhitui", 2, "mid", "This follower cut flesh from his own thigh to feed the exiled Duke Wen of Jin, and burned to death when the duke set fire to the forest to bring him out.",
  "<u>Jie Zhitui</u>", "Jie Zitui", extra="He is the origin of the Cold Food Festival.")
Q("Cold Food Festival", 3, "lead", "No fires are lit at this festival, just before Qingming, in memory of Jie Zhitui.",
  "<u>Cold Food</u> Festival", "Hanshi", kind="thing")
Q("Battle of Chengpu", 3, "lead", "At this battle in 632 BC, Duke Wen of Jin beat Chu.", "Battle of <u>Chengpu</u>", "", kind="event")
Q("Wu Zixu", 1, "give", "Ordered to kill himself by King Fuchai of Wu, this man asked for his eyes to be hung on the city gate to watch Yue conquer Wu.",
  "<u>Wu Zixu</u>", "Wu Yun")
Q("Fuchai", 3, "lead", "This king of Wu, who forced Wu Zixu's suicide, lost his state to Goujian in 473 BC.", "<u>Fuchai</u>", "")
Q("Fan Li", 3, "lead", "This minister of Goujian sent Xi Shi to King Fuchai, then retired with her and became a model merchant.",
  "<u>Fan Li</u>", "Tao Zhu Gong")
Q("Zuo zhuan", 1, "give", "Credited to Zuo Qiuming, this narrative commentary on the <i>Spring and Autumn Annals</i> is the source of many proverbs.",
  "<i><u>Zuo zhuan</u></i>", "<i>Commentary of Zuo</i>; <i>Zuoshi Chunqiu</i>", kind="work")
Q("Dong Zhongshu", 2, "mid", "This Han scholar of the Gongyang commentary wrote <i>Luxuriant Dew of the Spring and Autumn Annals</i>, joining Confucianism to five-phase cosmology.",
  "<u>Dong Zhongshu</u>", "")

# =====================================================================================
# WARRING STATES (475-221 BC)
# =====================================================================================
L("Seven Warring States", 2, "The seven powers of the Warring States period",
  [("Qin", ""), ("Chu", ""), ("Qi", ""), ("Yan", ""), ("Han", ""), ("Zhao", ""), ("Wei", "")], ordered=False)
Q("Shang Yang", 2, "mid", "After his patron Duke Xiao died, this reformer was torn apart by chariots.", "<u>Shang Yang</u>", "Lord Shang")
Q("Jixia Academy", 2, "mid", "This state-funded gathering of scholars from the Hundred Schools met in Linzi, the capital of Qi.",
  "<u>Jixia</u> Academy", "", kind="place")
L("Four Lords", 4, "The Four Lords of the Warring States",
  [("Lord Mengchang", "Qi"), ("Lord Pingyuan", "Zhao"), ("Lord Xinling", "Wei"), ("Lord Chunshen", "Chu")], ordered=False,
  extra="Each kept thousands of retainers.")
T("Qu Yuan", 1, [
    "This man wrote 'Heavenly Questions', a list of riddles about myth and the cosmos.",
    "He is the main poet of the <i>Chu Ci</i> (<i>Songs of the South</i>).",
    "Slandered and exiled, this minister of Chu wrote <i>Li Sao</i> ('Encountering Sorrow').",
    "He drowned himself in the Miluo River."],
  "For 10 points, name this poet whose death is remembered with the Dragon Boat Festival and <i>zongzi</i>.",
  "<u>Qu Yuan</u>", "")
Q("Zhao Kuo", 3, "lead", "This Zhao general who lost at Changping is the proverbial strategist who only knew war from books.",
  "<u>Zhao Kuo</u>", "", extra="The idiom is 纸上谈兵, 'fighting on paper'.")
Q("Marquis Yi of Zeng", 3, "lead", "This ruler's tomb, about 433 BC, held a set of 65 bronze bells (<i>bianzhong</i>).",
  "Marquis <u>Yi</u> of Zeng", "Zeng Hou Yi")

# =====================================================================================
# THE HUNDRED SCHOOLS
# =====================================================================================
# ---- Confucius ----
T("Confucius", 1, [
    "Herbert Fingarette wrote that this thinker saw 'the secular as sacred'. Red Guards smashed his family cemetery in 1966.",
    "He condemned the Ji family for having eight rows of dancers perform in their courtyard.",
    "He called for the 'rectification of names': let the ruler be a ruler, the subject a subject.",
    "His sayings, including 'Do not impose on others what you do not desire', are collected in the <i>Analects</i>."],
  "For 10 points, name this teacher from Qufu in the state of Lu.",
  "<u>Confucius</u>", "Kongzi; Kong Qiu; Kong Fuzi; Zhongni", period=P)
Q("ren", 2, "mid", "Confucius defined this virtue, usually translated 'humaneness', as restraining yourself and returning to the rites.",
  "<i><u>ren</u></i>", "humaneness; benevolence", kind="concept", period=P)
Q("Qufu", 2, "mid", "Confucius's home town, in the state of Lu, holds his temple, with the Hall of Great Perfection and the Apricot Platform.",
  "<u>Qufu</u>", "", kind="place", period=P)
Q("Criticize Lin, Criticize Confucius", 3, "lead", "This 1973–74 campaign attacked Mao's dead heir and an ancient sage together.",
  "<u>Criticize Lin, Criticize Confucius</u>", "Pi Lin Pi Kong", kind="event", period=P)

# ---- Mencius and Xunzi ----
Q("Mencius", 3, "lead", "This thinker told a king who had spared an ox from sacrifice to extend that compassion to his people.",
  "<u>Mencius</u>", "Mengzi", period=P)
Q("Mencius", 3, "lead", "This thinker compared seeking conquest by force to 'climbing a tree to look for fish'.",
  "<u>Mencius</u>", "Mengzi", period=P)
Q("Mencius", 3, "lead", "This thinker's Ox Mountain parable says the mountain's nature was forested even after it was stripped bare.",
  "<u>Mencius</u>", "Mengzi", period=P)
Q("Mencius", 2, "mid", "This thinker's mother moved house three times for his education.", "<u>Mencius</u>", "Mengzi", period=P)
L("four sprouts", 3, "Mencius's four sprouts and the virtues they grow into",
  [("compassion", "<i>ren</i>, humaneness"), ("shame", "<i>yi</i>, righteousness"), ("deference", "<i>li</i>, propriety"),
   ("approving and disapproving", "<i>zhi</i>, wisdom")], period=P)
Q("Xunzi", 2, "mid", "This Confucian taught both Han Fei and Li Si.", "<u>Xunzi</u>", "Xun Kuang", period=P)

# ---- Laozi and Daoism ----
T("Laozi", 1, [
    "Deified as Taishang Laojun, this man cooks Sun Wukong in his furnace in <i>Journey to the West</i>.",
    "He is the smiling one in the 'Vinegar Tasters' painting.",
    "This Zhou archivist rode west on a water buffalo, and the gatekeeper Yin Xi made him write down his teaching.",
    "The resulting 81 chapters open 'The Dao that can be told is not the eternal Dao.'"],
  "For 10 points, name this founder of Daoism, credited with the <i>Daodejing</i>.",
  "<u>Laozi</u>", "Lao-tzu; Lao Tse; Li Er", period=P)
Q("Daodejing", 3, "lead", "The 1973 Mawangdui silk copies of this text put its two parts in reverse order.",
  "<i><u>Daodejing</u></i>", "<i>Tao Te Ching</i>", kind="work", period=P)
Q("pu (uncarved block)", 3, "lead", "The <i>Daodejing</i> uses this image of the 'uncarved block' for the simple, natural state.",
  "<i><u>pu</u></i>", "uncarved block", kind="concept", period=P)
Q("Daodejing", 3, "lead", "This text says heaven and earth treat creatures as 'straw dogs', and that a wheel's use lies in its empty hub.",
  "<i><u>Daodejing</u></i>", "<i>Tao Te Ching</i>", kind="work", period=P)
Q("Wang Bi", 4, "lead", "This 3rd-century scholar of 'Mysterious Learning' (<i>Xuanxue</i>) wrote the classic commentary on the <i>Daodejing</i>.",
  "<u>Wang Bi</u>", "", period=P)

# ---- Zhuangzi ----
T("Zhuangzi", 1, [
    "In this thinker's book, Hundun (Chaos) dies after friends drill seven holes in him.",
    "He drummed on a basin and sang when his wife died, and preferred to be a turtle dragging its tail in the mud.",
    "Arguing with Huizi on a bridge, he claimed to know the happiness of fish, and Cook Ding's knife stays sharp for 19 years.",
    "He dreamed he was a butterfly, and woke unsure whether he was a butterfly dreaming he was a man."],
  "For 10 points, name this Daoist thinker, second only to Laozi.",
  "<u>Zhuangzi</u>", "Chuang-tzu; Zhuang Zhou", period=P)
Q("Cook Ding", 2, "mid", "In the <i>Zhuangzi</i>, this butcher's knife hasn't dulled in 19 years because he cuts between the joints.",
  "<u>Cook Ding</u>", "Butcher Ding; Pao Ding", period=P)
Q("Hui Shi", 2, "mid", "Zhuangzi argued with this logician about the happiness of fish, on a bridge over the Hao River.",
  "<u>Hui Shi</u>", "Huizi", period=P)

# ---- Mozi and the Logicians ----
Q("Mozi", 2, "mid", "This thinker, who held only defensive war just, outwitted Lu Ban's siege engines to save a small state.",
  "<u>Mozi</u>", "Mo Di", period=P)
Q("Mohism", 3, "lead", "This school's Ten Doctrines include 'against music', 'moderation in funerals', and 'against fatalism'.",
  "<u>Mohism</u>", "Mohists; Mojia", kind="concept", period=P)
Q("Mohism", 4, "lead", "This school judged doctrines by 'three tests' (basis, verifiability, applicability), an early consequentialism.",
  "<u>Mohism</u>", "Mohists; Mojia", kind="concept", period=P)
Q("Hui Shi", 3, "lead", "This logician's paradoxes include 'I set off for Yue today and arrived yesterday.'",
  "<u>Hui Shi</u>", "Huizi", period=P)

# ---- Legalism ----
Q("Han Fei", 2, "mid", "This Legalist called reward and punishment the ruler's 'two handles', and listed 'Five Vermin' of the state.",
  "<u>Han Fei</u>", "Han Feizi", period=P)
Q("Han Fei", 3, "lead", "This writer mocked the farmer who waited by a stump for another hare to break its neck on it.",
  "<u>Han Fei</u>", "Han Feizi", period=P)
Q("maodun", 3, "lead", "From Han Fei's story of a seller of an unbeatable spear and an impenetrable shield comes this Chinese word for 'contradiction'.",
  "<i><u>maodun</u></i>", "矛盾", kind="concept", period=P)
Q("Shen Buhai", 4, "lead", "This Legalist minister of Han stressed <i>shu</i>, the ruler's administrative technique.",
  "<u>Shen Buhai</u>", "", period=P)
Q("Shen Dao", 4, "lead", "This Legalist stressed <i>shi</i>, the power that comes from the ruler's position.", "<u>Shen Dao</u>", "", period=P)
Q("Yang Zhu", 3, "lead", "Mencius attacked this egoist, who would not pluck out one hair to benefit the world.", "<u>Yang Zhu</u>", "", period=P)
Q("Zou Yan", 4, "lead", "This Naturalist of the Yin-Yang school tied the rise and fall of dynasties to the cycle of the five phases.",
  "<u>Zou Yan</u>", "", period=P)

# ---- Sun Tzu ----
T("The Art of War", 1, [
    "A 1972 tomb find at Yinqueshan also yielded a namesake work by Sun Bin, settling an authorship dispute about this text.",
    "Cao Cao annotated it, and the Jesuit Jean-Joseph Amiot translated it into French in 1772.",
    "Its 13 chapters end with one on the five kinds of spies.",
    "It says 'All warfare is based on deception' and 'Know the enemy and know yourself.'"],
  "For 10 points, name this military treatise by Sun Tzu.",
  "<i>The <u>Art of War</u></i>", "<i>Sunzi bingfa</i>; <i>Sun Tzu</i>", period=P)
Q("Sun Tzu", 2, "mid", "To train the King of Wu's palace women, this general beheaded the two royal concubines who led them.",
  "<u>Sun Tzu</u>", "Sunzi; Sun Wu", period=P)
