"""boheme_clips_1002.py -- the La bohème clips (Carter, 2026-10-02: "fix ... the la boheme clips").
Whisper (medium) showed that "Aria 2" (live), "Mimi 2", and "Mimi 3" were all further passages of "Sì. Mi chiamano Mimì"
(Mimi 2/Aria 2: "che parlano di sogni e di chimere"; Mimi 3: "ma quando vien lo sgelo, il primo sole è mio"), which the
"Mimi" note already covers, and two more notes held German documentary narration. They now carry five other numbers,
cut from public-domain Commons recordings (sources: data/boheme_clips_1002_sources.json; full files in scratchpad):
Gigli's "Che gelida manina", Chaliapin's "Vecchia zimarra", Gigli and De Luca's "O Mimì, tu più non torni", Caruso and
Melba's "O soave fanciulla" (1907), and Melba's "Donde lieta uscì" (1907). Each fixed note's AUDIO + WORK card is
unsuspended; AUDIO-only cards stay suspended as everywhere.        py -3.9 boheme_clips_1002.py [--apply]
"""
import base64, json, os, subprocess, sys, time
import concept_add as C

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\carte\AppData\Local\Temp\claude\c--QB\1d6bde35-08b4-4391-958b-52d033191c05\scratchpad\boheme"
FF = r"C:\Users\carte\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"
OUT = os.path.join(HERE, "renders", "boheme_1002")
PLAN = {
 1787711405681: ("gelida.flac", 1.5, "cmc5-boheme-che-gelida-manina.mp3", "Act I · “Che gelida manina”",
   "Rodolfo's “Che gelida manina, se la lasci riscaldar”: the tenor takes Mimì's cold hand in the dark garret in a tender, conversational line over hushed strings, here sung by Beniamino Gigli.",
   "Rodolfo takes a seamstress's cold hand in “Che gelida manina” after her candle goes out, and she answers with “Sì. Mi chiamano Mimì”; after Henri Murger's stories, the painter Marcello loves the flirt Musetta, who sings “Quando m'en vo'”, and the philosopher Colline bids farewell to his coat."),
 1787711405682: ("zimarra.ogg", 0.0, "cmc5-boheme-vecchia-zimarra.mp3", "Act IV · “Vecchia zimarra, senti”",
   "Colline's farewell to the old overcoat he will pawn for the dying Mimì, “Vecchia zimarra, senti”: a solemn bass melody over a slow orchestral tread, here sung by Feodor Chaliapin.", None),
 1787711405683: ("piu_non_torni.flac", 106.0, "cmc5-boheme-o-mimi-tu-piu-non-torni.mp3", "Act IV · “O Mimì, tu più non torni”",
   "The Act IV duet “O Mimì, tu più non torni”: the tenor mourns “o giorni belli, piccole mani, odorosi capelli”, then the baritone admits his brush still paints Musetta's face, here Beniamino Gigli and Giuseppe De Luca.", None),
 1787711405687: ("soave.ogg", 0.5, "cmc5-boheme-o-soave-fanciulla.mp3", "Act I · “O soave fanciulla”",
   "The Act I love duet “O soave fanciulla”: the tenor greets Mimì in the moonlight before the soprano joins him, here Enrico Caruso and Nellie Melba in 1907.", None),
 1787711405688: ("donde.ogg", 4.0, "cmc5-boheme-donde-lieta-usci.mp3", "Act III · “Donde lieta uscì”",
   "Mimì's quiet farewell to Rodolfo, “Donde lieta uscì al tuo grido d'amore, torna sola Mimì al solitario nido”, a resigned soprano line over muted strings, here sung by Nellie Melba in 1907.", None),
}


def cut(src, ss, out):
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(ss), "-t", "30", "-i", os.path.join(SRC, src),
                    "-af", "afade=t=in:d=0.4,afade=t=out:st=28.5:d=1.5,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2",
                    "-codec:a", "libmp3lame", "-b:a", "192k", out], check=True)


def main(apply):
    os.makedirs(OUT, exist_ok=True)
    notes = {n["noteId"]: n for n in C.anki("notesInfo", notes=list(PLAN))}
    backup = {}
    for nid, (src, ss, fn, mvt, listen, clue) in PLAN.items():
        out = os.path.join(OUT, fn)
        if not os.path.exists(out):
            cut(src, ss, out)
        new = {"Audio": "[sound:%s]" % fn, "Movement": mvt, "Listen": listen}
        if clue:
            new["Clue"] = clue
        print(nid, C.plain(notes[nid]["fields"]["Movement"]["value"]), "->", mvt)
        if apply:
            C.anki("storeMediaFile", filename=fn, data=base64.b64encode(open(out, "rb").read()).decode())
            backup[nid] = {k: notes[nid]["fields"][k]["value"] for k in new}
            C.anki("updateNoteFields", note={"id": nid, "fields": new})
            cards = C.anki("cardsInfo", cards=C.anki("findCards", query="nid:%d" % nid))
            C.anki("unsuspend", cards=[c["cardId"] for c in cards if c["ord"] == 1 and c["queue"] == -1])
    if apply:
        json.dump(backup, open(os.path.join(HERE, "backups", "boheme_clips_%s.json" % time.strftime("%Y%m%d_%H%M%S")), "w", encoding="utf-8"), ensure_ascii=False)
        print("applied")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main("--apply" in sys.argv)
