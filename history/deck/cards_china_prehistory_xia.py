# -*- coding: utf-8 -*-
"""cards_china_prehistory_xia.py -- History v2 cards for China: Prehistory and the Xia.

From notes/02_prehistory_xia_writeup.md. Fact-checked 10-05 (web sources; qbreader was unreachable, so tiers
are unchanged). The apply script leaves it out unless asked:  py -3.9 hist_qb_apply.py --include prehistory
src="notes" = in my original notes (corrected); src="qb" = added from the qbreader sweep.
"""
import cards_china_myth_lit as base

NOTES = []
_Q, _L, _T = base.Q, base.L, base.T


def _wrap(fn, period):
    def inner(*a, **k):
        start = len(base.NOTES)
        k.setdefault("period", period)
        fn(*a, **k)
        NOTES.extend(base.NOTES[start:])
        del base.NOTES[start:]
    return inner


Q = _wrap(_Q, "prehistory")
L = _wrap(_L, "prehistory")

# ---- early humans ----
Q("Homo erectus", 1, "give", "Java Man and Peking Man belong to this hominin species, whose name means 'upright man'.",
  "<i>Homo <u>erectus</u></i>", "", kind="concept", src="qb")
Q("Peking Man", 1, "give", "Fossils of this <i>Homo erectus</i> population, about 780,000–400,000 years old, were found at Zhoukoudian near Beijing.",
  "<u>Peking Man</u>", "<i>Sinanthropus pekinensis</i>; <i>Homo erectus pekinensis</i>")
Q("Zhoukoudian", 2, "mid", "Peking Man was excavated in the 1920s–30s at this cave site southwest of Beijing, 'Dragon Bone Hill'.",
  "<u>Zhoukoudian</u>", "Chou-k'ou-tien", kind="place", src="qb")
Q("Teilhard de Chardin", 2, "mid", "This French Jesuit, who theorised the Omega Point and the noosphere, helped excavate Peking Man.",
  "Pierre <u>Teilhard de Chardin</u>", "", src="qb")
Q("Davidson Black", 3, "lead", "This Canadian anatomist directed the Peking Man excavations and named <i>Sinanthropus pekinensis</i>.",
  "Davidson <u>Black</u>", "", src="qb")
Q("Peking Man", 3, "lead", "The original fossils of this hominin vanished in 1941 while being shipped to the US; only Franz Weidenreich's casts survive.",
  "<u>Peking Man</u>", "", src="qb")
Q("Peking Man", 3, "lead", "In China this fossil population was cited for a multiregional, not 'out of Africa', origin of the Chinese.",
  "<u>Peking Man</u>", "")
Q("Yuanmou Man", 3, "lead", "Found in Yunnan and about 1.7 million years old, this is among the oldest <i>Homo erectus</i> finds in China.",
  "<u>Yuanmou</u> Man", "")
Q("Denisovans", 2, "mid", "First identified from a finger bone in a Siberian Altai cave, these archaic humans gave Tibetans a gene for living at altitude.",
  "<u>Denisovan</u>s", "Denisova hominins; <i>Homo longi</i>", kind="concept", src="qb",
  extra="In 2025 the Harbin 'Dragon Man' skull was shown to be Denisovan, so the species is now <i>Homo longi</i>.")
Q("Fuyan Cave", 4, "lead", "Teeth from this cave in Dao County, Hunan were claimed as modern humans 80,000–120,000 years old, a contested date.",
  "<u>Fuyan</u> Cave", "", kind="place")

# ---- Neolithic firsts ----
Q("Xianrendong", 2, "mid", "This 'Immortals' Cave' in Jiangxi holds the world's oldest pottery, about 20,000 years old.",
  "<u>Xianrendong</u>", "Xianren Cave", kind="place")
Q("Jiahu", 2, "give", "At this Peiligang-culture site in Henan, flutes carved from red-crowned crane wing bones are among the oldest playable instruments.",
  "<u>Jiahu</u>", "", kind="place")
Q("Jiahu", 2, "mid", "Symbols carved on tortoise shells at this Neolithic site may be the earliest Chinese proto-writing.",
  "<u>Jiahu</u>", "Jiahu symbols", kind="place")
Q("Jiahu", 3, "lead", "Residue in pots from this site is the oldest known fermented drink: rice, honey, and hawthorn.",
  "<u>Jiahu</u>", "", kind="place", src="qb")
Q("Damaidi", 4, "lead", "This site in Zhongwei, Ningxia has thousands of petroglyphs, some argued to be the origin of Chinese characters.",
  "<u>Damaidi</u>", "", kind="place")
Q("rice", 2, "mid", "The earliest evidence of cultivating this crop comes from the Yangtze valley, about 9,000–10,000 years ago.",
  "<u>rice</u>", "", kind="thing")

# ---- Neolithic cultures ----
Q("Yangshao culture", 1, "give", "This painted-pottery culture of the middle Yellow River (c. 5000–3000 BC) has its type site at Banpo.",
  "<u>Yangshao</u> culture", "", kind="concept")
Q("Johan Gunnar Andersson", 2, "mid", "This Swedish geologist discovered the Yangshao culture in 1921 and sent the first excavator to Zhoukoudian.",
  "Johan Gunnar <u>Andersson</u>", "", src="notes")
Q("Banpo", 2, "mid", "This moated Yangshao village near Xi'an has round houses, pottery kilns, and children buried in urns.",
  "<u>Banpo</u>", "", kind="place", src="qb")
Q("Majiayao culture", 3, "lead", "This upper Yellow River culture (c. 3300–2000 BC), famous for painted pottery, made China's oldest bronze knife.",
  "<u>Majiayao</u> culture", "", kind="concept")
Q("Longshan culture", 1, "give", "This late Neolithic 'Dragon Mountain' culture made thin black eggshell pottery on the potter's wheel.",
  "<u>Longshan</u> culture", "", kind="concept", conf="Yangshao (painted pottery, no wheel)")
Q("Liangzhu culture", 1, "give", "This lower-Yangtze culture (c. 3300–2300 BC) carved jade <i>cong</i> and <i>bi</i>.",
  "<u>Liangzhu</u> culture", "", kind="concept", extra="My notes put it on the Yellow River; it was around Lake Tai, Zhejiang.")
Q("cong", 2, "mid", "Liangzhu jade carvers made these square tubes with a round hole, thought to stand for the earth.",
  "<i><u>cong</u></i>", "ts'ung", kind="thing", src="qb")
Q("jade", 1, "give", "The Liangzhu <i>cong</i> and <i>bi</i> and the Hongshan 'pig-dragons' are made of this stone.",
  "<u>jade</u>", "nephrite", kind="thing", src="qb")
Q("Hongshan culture", 2, "mid", "This Neolithic culture of the Liao River basin carved coiled jade 'pig-dragons'.",
  "<u>Hongshan</u> culture", "", kind="concept", src="qb")
Q("Qijia culture", 3, "lead", "This upper Yellow River culture (c. 2200–1600 BC) was one of China's first to work copper and bronze; "
  "its Lajia site preserved 4,000-year-old millet noodles.", "<u>Qijia</u> culture", "", kind="concept")
Q("Shimao", 4, "lead", "This Longshan stone city in Shaanxi had jade embedded in its walls.", "<u>Shimao</u>", "", kind="place", src="qb")
Q("Taosi", 4, "lead", "This walled Longshan city in Shanxi may contain the earliest astronomical observatory, and is linked to the legendary Yao.",
  "<u>Taosi</u>", "", kind="place", src="qb")
Q("Hemudu", 3, "lead", "This Neolithic culture south of Hangzhou Bay built stilt houses and grew wet rice.", "<u>Hemudu</u>", "", kind="concept", src="qb")
Q("Sanxingdui", 1, "give", "This 'Three Star Mound' site in Sichuan, tied to the ancient kingdom of Shu, yielded bronze masks with protruding eyes.",
  "<u>Sanxingdui</u>", "Three Star Mound", kind="place")
Q("Shu", 2, "mid", "Sanxingdui and its successor Jinsha belonged to this ancient kingdom of the Chengdu plain, said to be founded by Cancong.",
  "<u>Shu</u>", "", kind="place", src="qb", conf="Shu Han of the Three Kingdoms (named after it)")
Q("Jinsha", 3, "lead", "This site in Chengdu, successor to Sanxingdui, produced the Golden Sun Bird disc.", "<u>Jinsha</u>", "", kind="place", src="qb")
Q("Zhangzhung", 3, "lead", "This ancient kingdom of western Tibet, cradle of the Bon religion, was conquered in the 7th century by Songtsen Gampo.",
  "<u>Zhangzhung</u>", "Zhang Zhung", kind="place")
Q("Bon", 2, "mid", "This indigenous Tibetan religion, from the kingdom of Zhangzhung, influenced Tibetan Buddhism.", "<u>Bon</u>", "", kind="concept")
L("Neolithic cultures", 2, "Neolithic culture — known for",
  [("Yangshao", "painted pottery; Banpo"), ("Longshan", "black eggshell pottery; potter's wheel"),
   ("Liangzhu", "jade <i>cong</i> and <i>bi</i>; lower Yangtze"), ("Hongshan", "jade pig-dragons; Liao River"),
   ("Majiayao", "painted pottery; first bronze knife")], ordered=False, src="notes")

# ---- Xia ----
Q = _wrap(_Q, "xia")
Q("Xia dynasty", 1, "give", "Founded by Yu the Great and ended by Jie, this semi-legendary dynasty is traditionally dated 2070–1600 BC.",
  "<u>Xia</u> dynasty", "Hsia", kind="concept")
Q("Xia dynasty", 2, "mid", "This first dynasty in Sima Qian's <i>Records of the Grand Historian</i> and the <i>Bamboo Annals</i> has left no writing of its own.",
  "<u>Xia</u> dynasty", "", kind="concept")
Q("Erlitou culture", 1, "give", "This Bronze Age site near the Luo River in Henan, with China's earliest ritual bronzes, is the main candidate for the Xia.",
  "<u>Erlitou</u> culture", "", kind="place")
Q("Bamboo Annals", 2, "mid", "This chronicle, found in 279 AD in the tomb of a Warring States king of Wei, is one of the two main sources on the Xia.",
  "the <i><u>Bamboo Annals</u></i>", "<i>Zhushu Jinian</i>", kind="work", src="notes")
Q("Records of the Grand Historian", 1, "give", "Sima Qian's history, whose Shang king list was confirmed by the oracle bones.",
  "<i><u>Records of the Grand Historian</u></i>", "<i>Shiji</i>", kind="work", src="qb")
Q("Yu the Great", 1, "give", "This first king of the Xia drained the waters of the Great Flood.", "<u>Yu</u> the Great", "Da Yu")
Q("Qi of Xia", 3, "lead", "By succeeding his father Yu, this king replaced abdication by merit with hereditary succession.",
  "<u>Qi</u> of Xia", "", src="qb")
Q("Shaokang", 4, "lead", "After the usurper archer Yi of Youqiong seized the throne from Taikang, this king restored the Xia line.",
  "<u>Shaokang</u>", "", src="qb", conf="Hou Yi the sun-shooter")
Q("Jie of Xia", 1, "give", "This last king of the Xia, the model tyrant, fell in love with a beautiful but cruel woman.",
  "<u>Jie</u> of Xia", "Lü Gui", extra="The woman was Mo Xi, who loved the sound of tearing silk.")
Q("Battle of Mingtiao", 2, "mid", "At this battle, around 1600 BC, Tang of Shang defeated Jie and ended the Xia.",
  "Battle of <u>Mingtiao</u>", "", kind="event")
Q("Tang of Shang", 2, "mid", "This founder of the Shang (also Zi Lü or Cheng Tang) overthrew Jie of Xia at Mingtiao.",
  "<u>Tang</u> of Shang", "Cheng Tang; Zi Lü", src="notes")
Q("rammed earth", 2, "mid", "This building technique pounds layers of earth in wooden frames; it built Longshan and Erlitou walls.",
  "<u>rammed earth</u>", "<i>hangtu</i>; pisé", kind="thing")
Q("Xia–Shang–Zhou Chronology Project", 3, "lead", "This 1996–2000 state project produced the standard dates of 2070–1600 BC for the Xia.",
  "the <u>Xia–Shang–Zhou Chronology</u> Project", "", kind="event", src="qb")
L("Contemporaries of the Xia", 3, "Contemporaries of the Xia (c. 2070–1600 BC)",
  [("the Minoans", "Crete"), ("the Indus Valley Civilisation", ""), ("Egypt's Middle Kingdom", ""),
   ("<i>Epic of Gilgamesh</i>", "written down")], ordered=False)
