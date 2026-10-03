# -*- coding: utf-8 -*-
"""cm_sig_0928.py -- Music: signature works, longer and better clips, Mahler 1.

Carter, 2026-09-28: "ok, add the signature works. try to find longer clips. find better bitrate
clips. [Mahler 1] ok, fix this."

  Signature works. The audit listed composers asked about without their signature work. Most were
    in the deck already, suspended with a clip but no text: Pärt's Spiegel im Spiegel, Fratres,
    and Tabula Rasa; Poulenc's Gloria and Dialogues des Carmélites; Stockhausen's Gruppen;
    Telemann's Tafelmusik. They are written up (description, Listen line from the clip's
    spectrogram, clue) and made tier 1. Added: Palestrina's Missa Papae Marcelli and Byrd's
    Mass for Four Voices (Commons recordings); Haydn's Farewell Symphony, Reich's Music for 18
    Musicians, and Stockhausen's Gesang der Jünglinge have no free recording, so they get the
    WORK to COMPOSER and DESCRIPTION to WORK cards only until a clip is supplied.
  Longer clips: the sub-10-second clips of Vivaldi's Spring, Pachelbel's Canon, the Barber of
    Seville overture, Alla Turca, Mozart 40 (on Sonata form), the Anvil Chorus, and the Little
    Swans become 40-50 s excerpts of public-domain or Creative Commons recordings on Commons.
    Rejected: an organ transcription of The Sorcerer's Apprentice and a synthesized Barcarolle.
  Better bitrate: the Moonlight, Pathétique, and Eine kleine Nachtmusik first movements (79-93
    kbps) become 192 kbps excerpts of Commons recordings.
  Mahler 1: the only active clip was Blumine, the movement Mahler cut; Commons has only a
    second-movement excerpt (no free recording of the funeral march exists there), so the card
    moves to the Ländler, which is part of the symphony as played.
Every clip: leading silence cut, 40-50 s, loudness -17 LUFS, 192 kbps mp3. Sources and licences in
data/audio_sources_0928.json.

    py -3.9 cm_sig_0928.py [--apply]
"""
import json, os, re, subprocess, sys, time
import concept_add as C

BIN = r"C:\Users\carte\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
AUD = r"C:/Users/carte/AppData/Local/Temp/claude/c--QB/4c6fe2ff-c3a6-47fb-8b54-226f916ad6af/scratchpad/aud2/"
T1 = "Music::tier::tier1-core"

CLIP = {  # key: seconds
 "mahler1_ii": 40, "palestrina_kyrie": 40, "byrd_agnus": 40, "vivaldi_spring1": 50, "pachelbel": 45,
 "barber_toscanini": 45, "alla_turca": 40, "mozart40_i": 40, "anvil": 45, "moonlight_i": 40,
 "pathetique_i": 45, "little_swans": 40,
}
# key -> [(nid, old clip-name prefix or None to replace the whole Audio field)]
REPLACE = {
 "vivaldi_spring1": [(1787711405201, "Vivaldi (The Four Seasons - Spring)")],
 "pachelbel": [(1788585498436, "Pachelbel (Canon In D 1)")],
 "barber_toscanini": [(1787711405142, "Rossini (Barber of Seville 2)")],
 "alla_turca": [(1788585498250, "Mozart (Rondo Alla Turca 2)")],
 "mozart40_i": [(1788585498183, "Mozart (Symphony 40)")],
 "anvil": [(1787711405193, "Verdi (Il Trovatore - Anvil Chorus)")],
 "little_swans": [(1787711405185, "Tchaikovsky (Swan Lake - Dance of the Little Swans")],
 "moonlight_i": [(1787711405923, "Beethoven (P.Son. 14, mvI (Moonlight))")],
 "pathetique_i": [(1787711405920, "Beethoven (P.Son. 8, mvI (Pathetique))")],
 "mahler1_ii": [(1788199512089, None)],
}
# notes that already play a longer clip of the same passage: the short or low-bitrate one just goes
DROP = [(1787711405127, "Pachelbel (Canon In D 1)"), (1787711405115, "Mozart (Rondo Alla Turca 2)"),
        (1787711406023, "Mozart (Eine Kleine Nacthmusik mvI)")]
LISTEN = {
 1787711405201: "The bright E-major ritornello for the full strings, then birdsong: solo violins trilling and chirping over a hushed accompaniment.",
 1787711405142: "The slow introduction: forceful chords, then a lyrical melody in the violins over a plucked accompaniment.",
 1787711405920: "Heavy dotted C-minor chords marked <i>Grave</i>, answered by hushed, questioning phrases: the slow introduction.",
 1788199512089: "A stamping Ländler in A major, the Austrian country dance, with heavy downbeats in the low strings and whooping horns.",
}
MAHLER_MV = "mvt. II · <i>Kräftig bewegt, doch nicht zu schnell</i>"

WAKE = {  # nid: (Description, Listen or None to keep, Clue or None for Description)
 1788199516868: ("A slow piece for violin (or cello) and piano in F major, in Pärt's tintinnabuli style: the piano repeats rising triads while the string instrument adds one scale note at a time, moving out from and back to a central A. The title means “mirror in the mirror”.",
                 "Gently rising three-note figures in the piano under long, slow notes in the strings, which step a little further from their home note each time.",
                 "A slow piece in F major for a string instrument and piano, written in 1978 just before Arvo Pärt left Estonia: the piano repeats rising triads while the melody adds one scale step at a time around a central A, in his tintinnabuli style."),
 1788199516902: ("A tintinnabuli piece of 1977 that Pärt has arranged for many ensembles: a chord sequence repeated in variations over an unchanging drone, each variation closed by a short percussion figure. The title means “brothers”.",
                 "Hushed, hymn-like chords repeated over a constant drone, each phrase closed by a quiet percussion stroke.",
                 "A 1977 piece in Arvo Pärt's tintinnabuli style, arranged for many ensembles, in which a chord sequence repeats in variations over an unchanging drone, each closed by a short percussion figure; its Latin title means “brothers”."),
 1788199516929: ("A double concerto for two violins, prepared piano, and string orchestra in two movements, the fast <i>Ludus</i> and the still <i>Silentium</i>; its 1984 recording, the first in ECM's New Series, brought Pärt to the West.",
                 "Bell-like prepared-piano notes scattered over two solo violins and slowly moving strings.",
                 "A double concerto for two violins, prepared piano, and strings in two movements, <i>Ludus</i> and <i>Silentium</i>, by Arvo Pärt; its 1984 recording launched ECM's New Series."),
 1788199516545: ("A setting of the Gloria for soprano, chorus, and orchestra, commissioned by the Koussevitzky Foundation and premiered in Boston in 1961; Poulenc said its irreverent angels came from Benozzo Gozzoli's frescoes and from Benedictine monks he had seen playing football.",
                 "A soprano soaring over chorus and a brightly coloured orchestra: liturgy set with music-hall brightness.",
                 "A setting of the Latin hymn of praise for soprano, chorus, and orchestra, premiered in Boston in 1961; Francis Poulenc said its irreverent angels came from Benozzo Gozzoli's frescoes and from Benedictine monks he had seen playing football."),
 1788199516592: ("Poulenc's opera after Georges Bernanos on the sixteen Carmelite nuns of Compiègne guillotined in 1794; it ends with the nuns singing the <i>Salve Regina</i> as the blade falls on each voice in turn, until the fearful Blanche de la Force walks out to die last.",
                 "The nuns' <i>Salve Regina</i>, cut off again and again by the fall of the guillotine as the chorus thins.",
                 "Francis Poulenc's opera after Georges Bernanos on sixteen nuns of Compiègne guillotined in 1794; the chorus thins as the blade falls on each singer during the <i>Salve Regina</i>, and the fearful Blanche de la Force walks out to die last."),
 1787792906352: (None, None, None),
 1787792906312: ("Three collections of “table music” published by subscription in 1733, each running from an overture-suite through quartet, concerto, trio, and solo sonata to a conclusion; Handel was among the subscribers.",
                 "Brisk Baroque ensemble music: strings and winds in lively counterpoint over harpsichord continuo.",
                 "Three collections published by subscription in 1733 by Georg Philipp Telemann, each running from an overture-suite through quartet, concerto, trio, and solo sonata to a conclusion, meant to accompany banquets; Handel subscribed."),
}

NEW = [
 dict(Work="<i>Missa Papae Marcelli</i>", Composer="Giovanni Pierluigi da Palestrina", Movement="Kyrie", Nickname="Pope Marcellus Mass",
      Date="c. 1562", Period="Renaissance", Genre="Mass", clip="palestrina_kyrie", tags=["sacred", "renaissance"],
      Description="A six-voice mass dedicated to Pope Marcellus II, long said to have persuaded the Council of Trent not to ban polyphony because its words stay audible; Hans Pfitzner's opera <i>Palestrina</i> dramatizes the legend.",
      Listen="Six unaccompanied voices in smooth, overlapping lines, with the words of the Kyrie kept clear.",
      Clue="A six-voice mass named for a pope who reigned three weeks, long credited with saving church polyphony at the Council of Trent by keeping its text intelligible; Hans Pfitzner built an opera on the legend."),
 dict(Work="<i>Mass for Four Voices</i>", Composer="William Byrd", Movement="Agnus Dei", Date="c. 1592–1593", Period="Renaissance",
      Genre="Mass", clip="byrd_agnus", tags=["sacred", "renaissance"],
      Description="One of three Latin masses the Catholic Byrd published in Protestant England without title pages, for services in recusant households; its Agnus Dei builds to an intense plea for peace.",
      Listen="Unaccompanied voices entering one after another in slow, overlapping imitation.",
      Clue="A Latin mass for a quartet of singers, published around 1593 without a title page by a Catholic composer in Elizabeth I's Protestant England, for secret services in recusant households."),
 dict(Work="<i>Symphony No. 45</i>", Composer="Joseph Haydn", Nickname="Farewell", Catalogue="Hob. I:45", Key="F-sharp minor",
      Date="1772", Period="Classical", Genre="Symphony", clip=None, tags=["symphony", "classical"],
      Description="Written at Eszterháza when Prince Nikolaus Esterházy kept his musicians away from their families too long: in the finale the players stop one by one, snuff their candles, and leave, until two muted violins remain. The prince took the hint.",
      Clue="In the finale of this F-sharp-minor symphony of 1772 the players stop one by one, snuff their candles, and walk out until two muted violins remain: Haydn's hint to Prince Nikolaus Esterházy that his musicians wanted to go home."),
 dict(Work="<i>Music for 18 Musicians</i>", Composer="Steve Reich", Date="1974–1976", Period="Contemporary", Genre="Chamber",
      clip=None, tags=["chamber", "contemporary"],
      Description="Built on a cycle of eleven chords, each stretched into a section of pulsing repeated patterns for pianos, marimbas, women's voices, clarinets, violin, and cello, with the changes cued by the vibraphone; about an hour long.",
      Clue="Steve Reich's hour-long piece built on a cycle of eleven chords, each stretched into a section of pulsing patterns for pianos, marimbas, women's voices, and clarinets, the changes cued by the vibraphone."),
 dict(Work="<i>Gesang der Jünglinge</i>", Composer="Karlheinz Stockhausen", Nickname="Song of the Youths", Date="1955–1956",
      Period="Modern", Genre="Electronic", clip=None, tags=["electronic", "modern"],
      Description="An electronic work that splices a boy's recorded voice singing the <i>Benedicite</i> from the Book of Daniel, the song of the three youths in the fiery furnace, into synthesized tones, first projected from five groups of loudspeakers.",
      Clue="Karlheinz Stockhausen's electronic landmark of 1956, which splices a boy's recorded voice singing the <i>Benedicite</i>, the canticle of the three young men in Nebuchadnezzar's fiery furnace, into synthesized sound."),
]


def make_clip(key, secs):
    src = [f for f in os.listdir(AUD) if f.startswith(key + ".") and os.path.getsize(AUD + f) > 0]
    if not src:
        return None
    src = AUD + src[0]
    out = "cmc2-%s.mp3" % key.replace("_", "-")
    pre = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.3,atrim=duration=%d,afade=t=out:st=%d:d=2," % (secs, secs - 2)
    e = subprocess.run([BIN + r"\ffmpeg.exe", "-hide_banner", "-nostats", "-i", src, "-af", pre + "loudnorm=I=-17:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    m = json.loads(e[e.rindex("{"):e.rindex("}") + 1])
    ln = "loudnorm=I=-17:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true" % (
        m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"])
    r = subprocess.run([BIN + r"\ffmpeg.exe", "-hide_banner", "-nostats", "-y", "-i", src, "-af", pre + ln, "-ac", "2", "-ar", "44100",
                        "-b:a", "192k", os.path.join(MED, out)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, r.stderr[-400:]
    return out


def composer_fields(name):
    for n in C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Classical Music" "Composer:%s"' % name)):
        if n["fields"]["Composer Image"]["value"]:
            return {k: n["fields"][k]["value"] for k in ("Composer Image", "Composer Dates", "Nationality")}
    n = C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Classical Music" "Composer:%s"' % name)[:1])[0]
    return {k: n["fields"][k]["value"] for k in ("Composer Image", "Composer Dates", "Nationality")}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    apply = "--apply" in sys.argv
    only_clips = "--clips-only" in sys.argv          # rerun for downloads that arrived late
    avail = {k for k in CLIP if any(f.startswith(k + ".") and os.path.getsize(AUD + f) > 0 for f in os.listdir(AUD))}
    print("recordings available:", sorted(avail), "| missing:", sorted(set(CLIP) - avail))
    if not apply:
        sys.exit()
    done = {k: "cmc2-%s.mp3" % k.replace("_", "-") for k in avail if os.path.exists(os.path.join(MED, "cmc2-%s.mp3" % k.replace("_", "-")))}
    made = {k: (done[k] if (only_clips and k in done) else make_clip(k, CLIP[k])) for k in sorted(avail)}
    backup = []
    # clip replacements
    for k, targets in REPLACE.items():
        if not made.get(k):
            continue
        for nid, old in targets:
            n = C.anki("notesInfo", notes=[nid])[0]
            a = n["fields"]["Audio"]["value"]
            if "cmc2-" in a and made[k] in a:
                continue
            if old is None:
                new = "[sound:%s]" % made[k]
            else:
                new, cnt = re.subn(r"\[sound:%s[^\]]*\]" % re.escape(old), "[sound:%s]" % made[k], a, count=1)
                assert cnt == 1, (nid, old, a)
            f = {"Audio": new}
            if nid in LISTEN:
                f["Listen"] = LISTEN[nid]
            if nid == 1788199512089:
                f["Movement"] = MAHLER_MV
            backup.append({"nid": nid, **{x: n["fields"][x]["value"] for x in f}})
            C.anki("updateNoteFields", note={"id": nid, "fields": f})
            print("clip", k, "->", nid)
    for nid, old in DROP:
        n = C.anki("notesInfo", notes=[nid])[0]
        a = n["fields"]["Audio"]["value"]
        new, cnt = re.subn(r"\[sound:%s[^\]]*\]" % re.escape(old), "", a, count=1)
        if cnt and "[sound:" in new:
            backup.append({"nid": nid, "Audio": a})
            C.anki("updateNoteFields", note={"id": nid, "fields": {"Audio": new}})
            print("dropped short clip", nid)
    if not only_clips:
        # wake and write up
        for nid, (d, l, c) in WAKE.items():
            n = C.anki("notesInfo", notes=[nid])[0]
            f = {}
            if d: f["Description"] = d
            if l: f["Listen"] = l
            f["Clue"] = c or d or n["fields"]["Description"]["value"]
            backup.append({"nid": nid, "tags": n["tags"], **{x: n["fields"][x]["value"] for x in f}})
            C.anki("updateNoteFields", note={"id": nid, "fields": f})
            old = [t for t in n["tags"] if "::tier::" in t and t != T1]
            if old:
                C.anki("removeTags", notes=[nid], tags=" ".join(old))
            C.anki("addTags", notes=[nid], tags=T1 + " Music::retier_2026-09-28")
            C.anki("unsuspend", cards=[c for c in n["cards"] if c])
            print("woke", C.plain(n["fields"]["Work"]["value"]))
        # new works
        added = []
        for w in NEW:
            f = {k: w.get(k, "") for k in ("Work", "Composer", "Movement", "Catalogue", "Key", "Nickname", "Date", "Period", "Genre",
                                            "Description", "Listen", "Clue")}
            f.update(composer_fields(w["Composer"]))
            if w["clip"] and made.get(w["clip"]):
                f["Audio"] = "[sound:%s]" % made[w["clip"]]
            tags = [T1, "Music::genre::" + w["tags"][0], "Music::period::" + w["tags"][1], "Music::added_2026-09-28"]
            nid = C.anki("addNote", note={"deckName": "Classical Music", "modelName": "Classical Music", "fields": f, "tags": tags,
                                          "options": {"allowDuplicate": False}})
            added.append(nid); print("added", C.plain(w["Work"]), nid)
        backup.append({"added": added})
    json.dump(backup, open("backups/cm_sig_0928_%s.json" % time.strftime("%Y%m%d_%H%M%S"), "w", encoding="utf-8"), ensure_ascii=False)
    meta = json.load(open(AUD + "meta.json", encoding="utf-8"))
    src = {made[k]: {x: meta[k][x] for x in ("title", "page", "license")} for k in made if made[k] and k in meta}
    old = json.load(open("data/audio_sources_0928.json", encoding="utf-8")) if os.path.exists("data/audio_sources_0928.json") else {}
    old.update(src)
    json.dump(old, open("data/audio_sources_0928.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("done")
