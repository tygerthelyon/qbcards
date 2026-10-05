# -*- coding: utf-8 -*-
"""cards_china_shang.py -- History v2 cards for China: the Shang dynasty.

From notes/03_shang_supplement_bonus.md (the qbreader sweep), with its correction applied: Erligang is
Zhengzhou, an early capital; Pan Geng moved the capital to Yin (Yinxu, near Anyang). All src="qb": tier 1-2
go into the queue, tier 3-4 are added suspended. Clues the old History Clue notes already give (Shang dynasty,
oracle bones, Yin, Fu Hao's tomb, taotie, Houmuwu ding, Muye, the Mandate of Heaven...) are left out, so this
adds only new angles. Don't run --supersede for this period: the old notes are the main cards.
Left out unless asked:  py -3.9 hist_qb_apply.py --include shang
No pictures yet (none downloaded at 1000 px or more).
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


Q, L, T = _wrap(base.Q, "shang"), _wrap(base.L, "shang"), _wrap(base.T, "shang")

# ---- the dynasty as an answer ----
T("Shang dynasty", 1, [
    "K. C. Chang argued that this dynasty overlapped its neighbours in the 'Three Dynasties' (<i>Sandai</i>) rather than simply following one.",
    "Max Loehr sorted the bronze décor of this dynasty into five styles; its <i>taotie</i> masks were cast in piece-moulds.",
    "Its consort Fu Hao led armies, and its king Wu Ding is named on most of its surviving divination records.",
    "Its last capital lay near Anyang, where its oracle bones were found."],
  "For 10 points, name this dynasty that followed the Xia and fell to the Zhou at Muye.",
  "<u>Shang</u> dynasty", "Yin dynasty")
Q("Zhengzhou", 3, "lead", "The Erligang culture is named for a site in this modern Henan capital, an early Shang capital (Ao).",
  "<u>Zhengzhou</u>", "Erligang; Ao", kind="place", conf="Not the last capital: that was Yin (Anyang).")

# ---- founding ----
Q("Xie", 3, "lead", "Jiandi swallowed an egg dropped by a black bird and bore this first ancestor of the Shang.",
  "<u>Xie</u>", "Qi (契)", extra="The egg story is the Shang's own origin myth.")
Q("Tang of Shang", 3, "lead", "During a years-long drought, this king offered himself as a sacrifice in the Mulberry Forest, and the rain came.",
  "<u>Tang</u> of Shang", "Cheng Tang")
Q("Tang of Shang", 2, "mid", "The <i>Great Learning</i> quotes this king's bathtub inscription, 'renew yourself daily', which Ezra Pound made 'Make It New'.",
  "<u>Tang</u> of Shang", "Cheng Tang", extra="苟日新，日日新，又日新.")
Q("Yi Yin", 3, "lead", "This minister of Tang, said to have been a cook, exiled Tang's grandson Tai Jia for three years to reform him.",
  "<u>Yi Yin</u>", "")

# ---- kings, Fu Hao, and the late Shang ----
Q("Fu Hao", 3, "lead", "Zheng Zhenxiang excavated this woman's tomb, which held over 1,600 objects, much jade, and 16 human sacrifices.",
  "<u>Fu Hao</u>", "Lady Hao")
Q("Zu Jia", 4, "lead", "This Shang king's ritual reforms are known only from the oracle bones; later texts don't mention them.",
  "<u>Zu Jia</u>", "")
Q("Wu Yi", 4, "lead", "This Shang king 'shot at Heaven' by firing arrows at a leather bag of blood, and was later killed by lightning.",
  "<u>Wu Yi</u> of Shang", "")
Q("Di Xin", 2, "mid", "After losing at Muye, this king burned himself to death on his Deer Terrace.",
  "<u>Di Xin</u>", "King Zhou of Shang")
Q("Bigan", 2, "mid", "Di Xin cut out the heart of this uncle to see whether a sage's heart really has seven openings.",
  "<u>Bigan</u>", "Bi Gan")
Q("Weizi", 3, "lead", "This half-brother of Di Xin went over to the Zhou and founded the state of Song, which carried on the Shang royal line.",
  "<u>Weizi</u>", "Weizi Qi; Viscount of Wei")
Q("Song (state)", 3, "lead", "The Shang royal line continued in this Zhou-era state, from which Confucius claimed descent.",
  "<u>Song</u>", "", kind="place")
Q("Jizi", 3, "lead", "This uncle of Di Xin is said to have gone east and founded Gija Joseon in Korea.",
  "<u>Jizi</u>", "Kija; Gija")

# ---- oracle bones ----
T("oracle bones", 1, [
    "David Keightley's <i>Sources of Shang History</i> showed that entries on these run preface, charge, prognostication, and verification.",
    "Dong Zuobin divided them into five periods, starting with Wu Ding; James Mellon Menzies collected thousands of them.",
    "Wang Yirong noticed writing on some sold as 'dragon bones' for his malaria in 1899.",
    "They were turtle plastrons and ox shoulder blades heated until they cracked."],
  "For 10 points, name these Shang divination objects that carry the earliest Chinese writing.",
  "<u>oracle bones</u>", "<i>jiaguwen</i>; oracle-bone script; dragon bones; plastrons; scapulae", src="qb")
Q("oracle bones", 3, "lead", "The character 卜 (<i>bu</i>, 'divine') pictures the crack made by heating these objects.",
  "<u>oracle bones</u>", "", kind="thing")
Q("Wang Yirong", 2, "mid", "In 1899 this scholar, taking 'dragon bones' for malaria, saw that they bore ancient characters.",
  "<u>Wang Yirong</u>", "")
Q("Luo Zhenyu", 4, "lead", "This scholar traced the oracle bones to their source at Anyang.", "<u>Luo Zhenyu</u>", "")
Q("Wang Guowei", 3, "lead", "This scholar used the oracle bones to confirm the Shang king list in Sima Qian's <i>Shiji</i>.",
  "<u>Wang Guowei</u>", "")
Q("Dong Zuobin", 4, "lead", "This archaeologist divided the oracle-bone inscriptions into five periods, from Wu Ding on.",
  "<u>Dong Zuobin</u>", "Tung Tso-pin")
Q("James Mellon Menzies", 4, "lead", "This Canadian missionary collected and reassembled thousands of oracle-bone fragments at Anyang.",
  "James Mellon <u>Menzies</u>", "")
Q("David Keightley", 4, "lead", "This historian's <i>Sources of Shang History</i> (1978) set out the parts of an oracle-bone inscription.",
  "David <u>Keightley</u>", "")
Q("Shangdi", 2, "mid", "The oracle bones name this supreme god of the Shang: 'If we build a settlement, he will not obstruct.'",
  "<u>Shangdi</u>", "Di; Lord on High", kind="concept")
L("oracle-bone inscription", 4, "The four parts of an oracle-bone inscription (Keightley)",
  [("preface", "the date and the diviner"), ("charge", "the question put"), ("prognostication", "the king's reading"),
   ("verification", "what happened")])

# ---- bronzes ----
Q("piece-mould casting", 3, "lead", "Shang bronzes were made by this method, not lost wax, which came later in the Zhou.",
  "<u>piece-mould</u> casting", "section-mould casting", kind="concept")
Q("Max Loehr", 4, "lead", "This art historian sorted the bronze décor of Anyang into five styles.", "Max <u>Loehr</u>", "")
Q("K. C. Chang", 4, "lead", "This archaeologist argued that the Xia, Shang, and Zhou (<i>Sandai</i>) partly overlapped.",
  "K. C. <u>Chang</u>", "Kwang-chih Chang; Zhang Guangzhi")
