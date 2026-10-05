# -*- coding: utf-8 -*-
"""cards_china_qin_han.py -- History v2 cards for China: the Qin, the Chu-Han contention, and the Han.

Written 10-05 in a cloud session that couldn't reach qbreader, from standard quizbowl clues and checked
against web sources. src="web": tier 1-2 go into the queue, tier 3-4 are added suspended. The tiers are
estimates; check them with  py -3.9 hist_tier_check.py --include qinhan  before trusting them.
Left out unless asked:  py -3.9 hist_qb_apply.py --include qinhan
Clues the old History Clue notes already give (the Terracotta Army, the book burning, Zhao Gao's fish cart,
Hong Gate, Gaixia, Empress Lu's 'human swine', Zhang Qian, salt and iron, Wang Mang, the Red Eyebrows, Cai Lun,
Zhang Heng, the Yellow Turbans, Dong Zhuo, Lelang, the King of Na seal...) are left out, so this adds only
new angles. Don't run --supersede for this period: the old notes are the main cards.
Already in cards_china_myth_lit.py: He Jin, the Ten Attendants, and Li Bing's Dujiangyan.
"""
import cards_china_myth_lit as base

NOTES = []


def _wrap(fn, period):
    def inner(*a, **k):
        start = len(base.NOTES)
        k.setdefault("period", period)
        k.setdefault("src", "web")
        fn(*a, **k)
        NOTES.extend(base.NOTES[start:])
        del base.NOTES[start:]
    return inner


Q, L, T = _wrap(base.Q, "qin"), _wrap(base.L, "qin"), _wrap(base.T, "qin")

# =====================================================================================
# QIN (221-206 BC)
# =====================================================================================
T("Qin Shi Huang", 1, [
    "Inscribed steles record this ruler's tours to Mount Tai, where he performed the <i>feng</i> and <i>shan</i> sacrifices, and to Langya.",
    "He standardized weights, measures, axle widths, and the round <i>banliang</i> coin.",
    "He replaced the Zhou fiefs with 36 commanderies run by appointed officials.",
    "He survived Jing Ke's attempt on his life and was buried under Mount Li."],
  "For 10 points, name this king of Qin who unified China in 221 BC.",
  "<u>Qin Shi Huang</u>", "Ying Zheng; Shi Huangdi; First Emperor of Qin")
Q("commanderies", 3, "lead", "Qin Shi Huang divided the empire into 36 of these units, each split into counties (<i>xian</i>), "
  "in place of hereditary fiefs.", "<u>commanderies</u>", "<i>jun</i>", kind="concept")
Q("banliang", 4, "lead", "The Qin standardized this round bronze coin with a square hole; its name means 'half an ounce'.",
  "<i><u>banliang</u></i>", "ban liang; half-<i>liang</i>", kind="thing")
Q("Mount Li", 3, "lead", "Qin Shi Huang's still-unopened burial mound lies at the foot of this mountain near Xi'an.",
  "Mount <u>Li</u>", "Lishan", kind="place")
Q("Epang Palace", 3, "lead", "This vast Qin palace, never finished and said to have been burned by Xiang Yu, is the subject of a "
  "rhapsody by the Tang poet Du Mu.", "<u>Epang</u> Palace", "Afang Palace; Ebang", kind="place")
Q("Lingqu Canal", 4, "lead", "Built in 214 BC to supply the Qin armies in the south, this canal in Guangxi joins the Xiang and Li "
  "rivers, linking the Yangtze and Pearl systems.", "<u>Lingqu</u> Canal", "Ling Canal", kind="place")
Q("Zhengguo Canal", 4, "lead", "The state of Han sent an engineer to Qin to build this canal and drain its treasury; instead it "
  "irrigated the Wei River plain and fed Qin's armies.", "<u>Zhengguo</u> Canal", "Cheng-kuo Canal", kind="place")
Q("Shuihudi Qin bamboo texts", 4, "lead", "Found in 1975 in Yunmeng, Hubei, in the tomb of a local official named Xi, these slips "
  "are the main surviving source for Qin law.", "the <u>Shuihudi</u> bamboo slips", "Yunmeng Qin slips", kind="work")
Q("Fusu", 2, "mid", "Qin Shi Huang sent this eldest son to the northern frontier for objecting to the burial of scholars; a "
  "forged edict from Zhao Gao and Li Si ordered him to kill himself.", "<u>Fusu</u>", "Fu Su")
Q("Zhao Gao", 2, "mid", "To see which officials dared oppose him, this eunuch presented a deer at court and called it a horse.",
  "<u>Zhao Gao</u>", "", extra="The idiom 'point at a deer and call it a horse' (指鹿为马) means to misrepresent on purpose.")
Q("Chen Sheng", 2, "mid", "Late for garrison duty because of rain, and facing death for it, this conscript asked 'Are kings, "
  "nobles, generals, and ministers a breed apart?' and rose against the Qin.", "<u>Chen Sheng</u>", "Chen She",
  extra="He led the Dazexiang Uprising (209 BC) with Wu Guang and proclaimed the state of Zhang Chu.")
Q("Ziying", 3, "lead", "This last ruler of the Qin, who reigned only as 'King of Qin' for 46 days, surrendered to Liu Bang and "
  "was killed by Xiang Yu.", "<u>Ziying</u>", "Ziying of Qin")

# =====================================================================================
# CHU-HAN CONTENTION (206-202 BC)
# =====================================================================================
Q, L, T = _wrap(base.Q, "chu-han"), _wrap(base.L, "chu-han"), _wrap(base.T, "chu-han")
Q("Chu–Han Contention", 2, "mid", "The river line across the middle of a <i>xiangqi</i> board is labelled with the two sides of "
  "this 206–202 BC war.", "the <u>Chu–Han</u> Contention", "Chu–Han War", kind="event",
  extra="The board reads 'Chu River, Han Border' (楚河汉界).")
T("Xiang Yu", 1, [
    "His adviser Fan Zeng raised a jade <i>jue</i> three times as a signal to kill a guest, but this man did nothing.",
    "Before the Battle of Julu he ordered his men to break their cooking pots and sink their boats, so there could be no retreat.",
    "Hearing the songs of his homeland sung on all sides of his camp, he sang a farewell to his consort Yu.",
    "He killed himself on the bank of the Wu River."],
  "For 10 points, name this Chu general who destroyed the Qin and then lost China to Liu Bang.",
  "<u>Xiang Yu</u>", "Xiang Ji; Hegemon-King of Western Chu",
  extra="The farewell scene is the Peking opera and Chen Kaige's 1993 film <i>Farewell My Concubine</i>.")
Q("Fan Zeng", 3, "lead", "Xiang Yu called this adviser 'Second Father'; at Hong Gate he signalled three times for Liu Bang to be "
  "killed, and later left Xiang Yu in disgust.", "<u>Fan Zeng</u>", "Yafu")
Q("Consort Yu", 3, "lead", "This companion of Xiang Yu killed herself at Gaixia; she is the concubine of <i>Farewell My Concubine</i>.",
  "Consort <u>Yu</u>", "Yu Ji; Yu Meiren")
T("Han Xin", 2, [
    "A washerwoman fed this man when he was poor, and he once crawled between a bully's legs rather than fight.",
    "Xiao He chased after him by moonlight when he deserted, and talked Liu Bang into making him a general.",
    "At Jingxing he made his army fight with its back to a river, so it could not flee.",
    "Empress Lü had him killed in the Changle Palace in 196 BC."],
  "For 10 points, name this general who won the war for Liu Bang and became King of Chu.",
  "<u>Han Xin</u>", "Marquis of Huaiyin")
Q("Zhang Liang", 2, "mid", "This strategist hired a strongman to hit Qin Shi Huang's carriage with an iron mallet at Bolangsha; "
  "later he advised Liu Bang.", "<u>Zhang Liang</u>", "Zifang")
Q("Zhang Liang", 3, "lead", "After fetching an old man's shoe from under a bridge three times, this man was given a book of "
  "strategy by Huang Shigong.", "<u>Zhang Liang</u>", "Zifang")
Q("Xiao He", 3, "lead", "This first chancellor of the Han kept Liu Bang's armies supplied and drafted the Han law code from the Qin one.",
  "<u>Xiao He</u>", "")
L("Three Heroes of the early Han", 3, "The Three Heroes of the early Han (Liu Bang's men)",
  [("Zhang Liang", "strategy"), ("Xiao He", "supply and administration"), ("Han Xin", "command in the field")], ordered=False)

# =====================================================================================
# WESTERN HAN (202 BC-9 AD)
# =====================================================================================
Q, L, T = _wrap(base.Q, "han"), _wrap(base.L, "han"), _wrap(base.T, "han")
Q("Rule of Wen and Jing", 3, "lead", "This name for the reigns of two early Han emperors (180–141 BC) stands for light taxes, "
  "frugal government, and Huang–Lao Daoism.", "the <u>Rule of Wen and Jing</u>", "Wen–Jing era", kind="event")
Q("Chao Cuo", 3, "lead", "This adviser to Emperor Jing urged him to cut down the kingdoms; when the Seven States revolted, he "
  "was cut in half in his court robes to appease them.", "<u>Chao Cuo</u>", "")
Q("Huo Qubing", 2, "mid", "This nephew of Wei Qing beat the Xiongnu in the Hexi Corridor and died at 23; his tomb has a stone "
  "horse trampling a Xiongnu warrior.", "<u>Huo Qubing</u>", "",
  extra="He refused a mansion: 'The Xiongnu are not yet destroyed; what use is a home?'")
Q("Wei Qing", 3, "lead", "Once a horseman in Princess Pingyang's household, this brother of Emperor Wu's empress became Emperor Wu's "
  "commander against the Xiongnu.", "<u>Wei Qing</u>", "")
Q("Li Guang", 3, "lead", "The Xiongnu called this Han archer the 'Flying General'; he once shot an arrow deep into a rock he "
  "took for a tiger.", "<u>Li Guang</u>", "")
Q("Li Ling", 2, "mid", "When this general surrendered to the Xiongnu in 99 BC, Sima Qian defended him and was castrated for it.",
  "<u>Li Ling</u>", "", extra="He was Li Guang's grandson.")
Q("Su Wu", 3, "lead", "Held by the Xiongnu for 19 years, this Han envoy herded sheep by Lake Baikal and would not give up his "
  "envoy's staff.", "<u>Su Wu</u>", "")
Q("Yuezhi", 2, "mid", "Zhang Qian was sent west to ally with this people, whom the Xiongnu had driven out of Gansu; they later "
  "founded the Kushan Empire.", "the <u>Yuezhi</u>", "Rouzhi; Yüeh-chih", kind="concept")
Q("Dayuan", 3, "lead", "Emperor Wu sent Li Guangli to conquer this Central Asian kingdom to get its 'heavenly horses'.",
  "<u>Dayuan</u>", "Ferghana; Ta-yuan", kind="place", extra="The 'War of the Heavenly Horses', 104–101 BC.")
Q("Zhao Tuo", 3, "lead", "This Qin general founded Nanyue, with its capital at Panyu (Guangzhou); the Han conquered his kingdom in "
  "111 BC.", "<u>Zhao Tuo</u>", "Triệu Đà", extra="Vietnam's Triệu dynasty is named after him.")
Q("Huainanzi", 2, "mid", "Presented to Emperor Wu in 139 BC, this Daoist-leaning compendium was compiled at the court of his "
  "uncle Liu An.", "the <i><u>Huainanzi</u></i>", "", kind="work")
Q("Music Bureau", 3, "lead", "Emperor Wu expanded this office, which collected folk songs; its name became the name of a verse form.",
  "the <u>Music Bureau</u>", "<i>Yuefu</i>", kind="concept")
Q("Sima Xiangru", 3, "lead", "This court poet of Emperor Wu wrote the 'Rhapsody on the Shanglin Park' and eloped with the young "
  "widow Zhuo Wenjun.", "<u>Sima Xiangru</u>", "")
Q("jade burial suit", 2, "mid", "Liu Sheng, Prince of Zhongshan, and his wife Dou Wan were found at Mancheng in 1968 wearing these, "
  "made of jade plaques sewn with gold wire.", "<u>jade burial suit</u>s", "jade suit; jade clothes", kind="thing")
Q("Changxin Palace Lamp", 3, "lead", "From Dou Wan's tomb at Mancheng, this gilt-bronze lamp shows a kneeling servant whose sleeve "
  "carries the smoke away.", "the <u>Changxin Palace Lamp</u>", "Changxin lamp", kind="thing")
Q("Lady Dai", 3, "lead", "A T-shaped silk banner covered the coffin of this wife of Li Cang, chancellor of Changsha; her body was "
  "found intact at Mawangdui.", "<u>Lady Dai</u>", "Xin Zhui; Marquise of Dai", kind="figure")
Q("Huo Guang", 3, "lead", "This regent deposed Liu He after 27 days on the throne, charging him with over a thousand misdeeds.",
  "<u>Huo Guang</u>", "")
Q("Haihun tomb", 4, "lead", "The tomb of Liu He, the deposed emperor, found near Nanchang, held about 10 tonnes of coins and a "
  "lost version of the <i>Analects</i>.", "the tomb of the Marquis of <u>Haihun</u>", "Haihun Marquis tomb", kind="place")

# =====================================================================================
# WANG MANG AND THE EASTERN HAN (9-220)
# =====================================================================================
Q("Wang Mang", 2, "mid", "This ruler nationalized land as 'king's fields' in an attempt to revive the well-field system, and "
  "banned the sale of slaves.", "<u>Wang Mang</u>", "")
Q("Battle of Kunyang", 3, "lead", "At this battle in 23 AD, Liu Xiu beat a far larger army of Wang Mang's during a storm.",
  "Battle of <u>Kunyang</u>", "", kind="event")
Q("Flying Horse of Gansu", 2, "mid", "Found in 1969 in a tomb at Wuwei, this Eastern Han bronze horse, one hoof resting on a bird in "
  "flight, is China's tourism emblem.", "the <u>Flying Horse of Gansu</u>", "Galloping Horse Treading on a Flying Swallow",
  kind="thing")
Q("Wang Chong", 3, "lead", "This Eastern Han sceptic argued against ghosts and omens in his <i>Lunheng</i> ('Balanced Discourses').",
  "<u>Wang Chong</u>", "")
Q("Shuowen Jiezi", 2, "mid", "Xu Shen's dictionary of about 100 AD sorted 9,353 characters under 540 radicals.",
  "the <i><u>Shuowen Jiezi</u></i>", "<i>Shuowen</i>", kind="work")
Q("The Nine Chapters on the Mathematical Art", 3, "lead", "This Han mathematics book uses negative numbers and solves systems of "
  "equations; Liu Hui wrote a commentary on it in 263.", "<i>The <u>Nine Chapters</u> on the Mathematical Art</i>",
  "<i>Jiuzhang Suanshu</i>", kind="work")
Q("Zhang Zhongjing", 3, "lead", "Called the 'Medical Sage', this Eastern Han doctor wrote the <i>Treatise on Cold Damage Disorders</i>.",
  "<u>Zhang Zhongjing</u>", "Zhang Ji")
Q("Partisan Prohibitions", 3, "lead", "In 166 and 169, the eunuchs had hundreds of Confucian officials barred from office or "
  "killed in these purges.", "the <u>Partisan Prohibitions</u>", "Disasters of the Partisan Prohibitions; <i>danggu</i>",
  kind="event")
Q("Cai Wenji", 3, "lead", "Captured by the Xiongnu and ransomed by Cao Cao, this poet is credited with 'Eighteen Songs of a "
  "Nomad Flute'.", "<u>Cai Wenji</u>", "Cai Yan")
Q("Emperor Xian of Han", 2, "mid", "Held at Xuchang by Cao Cao, this last Han emperor abdicated to Cao Pi in 220.",
  "Emperor <u>Xian</u> of Han", "Liu Xie")
