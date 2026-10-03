# -*- coding: utf-8 -*-
"""cm_audio_0928.py -- even out Music clip loudness and cut dead air at the start.

Carter, 2026-09-28: "Waldstein audio bad", and the audit's open item to review short clips. A scan
of every active clip (data/_cm_audio_quality.json) found the real problems were not length:
  * 35 clips begin with over a second of silence; the Queen of the Night clip starts with 10.6 s
    of nothing, Carmen's Toréadors with 5 s, La fanciulla del West with 3.4 s.
  * Loudness ran from -37 to -13 LUFS against a deck median of -17.2, so some clips (the Barber of
    Seville overture, Gluck, Rigoletto, Mazeppa, the Eroica excerpt) needed the volume turned up
    by 10 dB, and one (Hoedown) was clipping.
Each such clip is rewritten as a new file, "<name>_n.mp3" (the original stays in the media folder):
leading silence cut to 0.3 s, then two-pass EBU R128 loudness normalisation to -17 LUFS, true peak
-1.5 dBTP. Every note that plays the clip is pointed at the new file. Cage's 4'33" is left alone.

    py -3.9 cm_audio_0928.py [--apply]
"""
import json, os, re, subprocess, sys, time
import concept_add as C

BIN = r"C:\Users\carte\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
MED = os.path.join(os.environ["APPDATA"], "Anki2", "User 1", "collection.media")
TARGET, TP, TOL, LEAD = -17.0, -1.5, 4.0, 1.0


def todo():
    q = json.load(open("data/_cm_audio_quality.json", encoding="utf-8"))
    return {f: v for f, v in q.items() if "Cage" not in f and (abs(v["lufs"] - (-17.2)) > TOL or v["lead"] > LEAD)}


def process(f, v):
    src = os.path.join(MED, f)
    out = re.sub(r"\.[^.]+$", "", f) + "_n.mp3"
    pre = "atrim=start=%.2f,asetpts=PTS-STARTPTS," % (v["lead"] - 0.3) if v["lead"] > LEAD else ""
    e = subprocess.run([BIN + r"\ffmpeg.exe", "-hide_banner", "-nostats", "-i", src, "-af",
                        pre + "loudnorm=I=%s:TP=%s:LRA=11:print_format=json" % (TARGET, TP), "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(e[e.rindex("{"):e.rindex("}") + 1])
    ln = ("loudnorm=I=%s:TP=%s:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
          % (TARGET, TP, m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))
    r = subprocess.run([BIN + r"\ffmpeg.exe", "-hide_banner", "-nostats", "-y", "-i", src, "-af", pre + ln,
                        "-ar", "44100", "-b:a", "192k", os.path.join(MED, out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    fs = todo()
    print(len(fs), "clips")
    if "--apply" not in sys.argv:
        sys.exit()
    ns = C.anki("notesInfo", notes=C.anki("findNotes", query='"note:Classical Music"'))
    new = {}
    for i, (f, v) in enumerate(fs.items()):
        new[f] = process(f, v)
        print("%2d %s -> %s" % (i + 1, f[:60], new[f][:60]))
    ch = []
    for n in ns:
        a = n["fields"]["Audio"]["value"]
        b = a
        for f, g in new.items():
            b = b.replace("[sound:%s]" % f, "[sound:%s]" % g)
        if b != a:
            ch.append((n, a, b))
    json.dump([{"nid": n["noteId"], "Audio": a} for n, a, b in ch],
              open("backups/cm_audio_0928_%s.json" % time.strftime("%Y%m%d_%H%M"), "w", encoding="utf-8"), ensure_ascii=False)
    for n, a, b in ch:
        C.anki("updateNoteFields", note={"id": n["noteId"], "fields": {"Audio": b}})
    print("updated", len(ch), "notes")
