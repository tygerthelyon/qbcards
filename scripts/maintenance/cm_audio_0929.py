# -*- coding: utf-8 -*-
"""cm_audio_0929.py -- Carter, 2026-09-28: "Bad audio: Cavalleria rusticana, Norma, Fort denn eile"; "No example for
recitative upon reveal"; "I don't hear the word news referred to in News has a kind of mystery clip".

- Cavalleria rusticana, Norma: the old clips were hiss-heavy transfers (10-20 dB more noise above 9 kHz than a clean
  recording). Replaced by a modern Intermezzo and by Justina Didyk's "Casta diva", from the soprano's entry.
- The Ring Cycle: "Fort denn eile" exists free only in Johanna Gadski's acoustic-era recording, the source of the bad
  clip, so the card now plays the Ring's best-known music, the Ride of the Valkyries.
- Recitative: a secco example, the tenor recitative from Bach's Cantata No. 140.
- Nixon in China: the clip began just after the stuttered "News, news, news"; recut from the opening of the aria
  (checked with speech recognition: "News ... has a kind of mystery" at 0-15 s).

Clips cut and normalised to -17 LUFS / TP -1.5, 192 kbps (scratchpad make_clips.py); sources in
data/audio_sources_0929.json. AUDIO to COMPOSER cards stay suspended.

    py -3.9 cm_audio_0929.py <clip dir> [--apply]
"""
import base64
import json
import os
import sys
import time

import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
UPDATES = {
    1788199515855: {"Audio": "[sound:cmc3-cavalleria-intermezzo.mp3]"},
    1788199515443: {"Audio": "[sound:cmc3-norma-casta-diva.mp3]"},
    1787792906326: {"Audio": "[sound:cmc3-ride-of-the-valkyries.mp3]",
                    "Movement": "<i>Die Walküre</i>, Act III · <i>Ride of the Valkyries</i>",
                    "Listen": "Swirling strings and shrieking woodwind trills, then horns and trombones hammer out the galloping Valkyrie theme."},
    1790365377103: {"Audio": "[sound:cmc3-recitative-bach-140.mp3]",
                    "Composer": "Bach's Cantata No. 140, <i>Wachet auf</i>"},
    1788199516865: {"Audio": "[sound:cmc3-nixon-news.mp3]"},
}
SOURCES = {
    "cmc3-cavalleria-intermezzo.mp3": {"title": "File:Pietro Mascagni - Cavalleria Rusticana - Intermezzo Sinfonico.ogg", "license": "EEF OAL-1", "excerpt": "46-91 s"},
    "cmc3-norma-casta-diva.mp3": {"title": "File:Каватина Норми з опери Норма Белліні - вик. ЮстинаДідик Norma -CastaDiva - V. Bellini -JustinaDidyk.ogg",
                                  "license": "CC BY-SA 4.0", "performer": "Justina Didyk", "excerpt": "86-131 s"},
    "cmc3-ride-of-the-valkyries.mp3": {"title": "File:Ride of the Valkyries.ogg", "license": "CC BY 3.0", "excerpt": "0-45 s"},
    "cmc3-recitative-bach-140.mp3": {"title": "File:Bach - cantata 140. 2. recitative.ogg", "license": "CC BY-SA 2.0", "excerpt": "0-45 s"},
    "cmc3-nixon-news.mp3": {"source": "Nonesuch recording (Edo de Waart, James Maddalena), YouTube OAv4GxkhqzE", "excerpt": "0-40 s",
                            "note": "personal study excerpt; no free recording exists"},
}


def main(clipdir, apply):
    notes = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(UPDATES))}
    backup = {nid: {k: notes[nid]["fields"][k]["value"] for k in f} for nid, f in UPDATES.items()}
    for nid, f in UPDATES.items():
        print(nid, C.plain(notes[nid]["fields"]["Work"]["value"]), {k: v[:60] for k, v in f.items()})
    if not apply:
        return
    for fn in SOURCES:
        data = open(os.path.join(clipdir, fn), "rb").read()
        C.anki("storeMediaFile", filename=fn, data=base64.b64encode(data).decode())
    stamp = time.strftime("%Y%m%d_%H%M%S")
    json.dump(backup, open(os.path.join(HERE, "backups", "cm_audio_before_%s.json" % stamp), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(SOURCES, open(os.path.join(HERE, "data", "audio_sources_0929.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for nid, f in UPDATES.items():
        C.anki("updateNoteFields", note={"id": nid, "fields": f})
    # AUDIO to COMPOSER stays suspended by Carter's policy
    cards = C.anki("findCards", query="nid:%s card:1" % ",".join(str(x) for x in UPDATES))
    info = C.anki("cardsInfo", cards=cards) if cards else []
    live = [c["cardId"] for c in info if c["queue"] != -1]
    if live:
        C.anki("suspend", cards=live)
    print("applied; re-suspended", len(live), "AUDIO to COMPOSER cards")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main(sys.argv[1], "--apply" in sys.argv)
