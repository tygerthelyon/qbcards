# -*- coding: utf-8 -*-
"""hist_qb_models.py -- the three note types of History v2 (see DESIGN.md).

    QB Clue    one tossup-style clue -> one answer; optional PICTURE card when a picture is the clue
    QB List    a closed set (Five Classics, zodiac...): one card per item, the other items hidden
    QB Tossup  a pyramid of clues revealed one at a time, graded by where you could have buzzed

House look (Art/History palette): paper #f7f3ea, ink #2b2b2b, accent #6b4c3b, Optima text, serif
answer; night mode via .night_mode / html:has(> body.night_mode), never :root:not(...).
Imported by hist_qb_apply.py and render_previews.py; nothing here talks to Anki.
"""

CSS = r"""
/* ---- History v2 (hist_qb_models.py) ---- */
.card { --paper:#f7f3ea; --ink:#2b2b2b; --muted:#706a61; --rule:#d8d0c0; --accent:#6b4c3b;
  --tint:#efe8d8; --plate:#fffdf8;
  background:var(--paper) !important; color:var(--ink);
  font-family: Optima, "Century Gothic", "Segoe UI", sans-serif; font-size:19px; line-height:1.5;
  text-align:center; margin:0; padding:0; }
html:has(> body.night_mode) .card, .night_mode .card, .nightMode .card {
  --paper:#1b1a18; --ink:#e6dfd3; --muted:#a39a8c; --rule:#3a3631; --accent:#d2ab8f;
  --tint:#26241f; --plate:#22201c; }
html:has(> body.night_mode), .night_mode, .nightMode { background:#1b1a18 !important; }
.qb { max-width:640px; margin:0 auto; padding:22px 18px 110px; }
.qb-kicker { font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted);
  margin-bottom:14px; }
.qb-prompt { font-size:21px; line-height:1.5; text-align:left; display:inline-block; max-width:600px; }
.qb-back .qb-prompt { font-size:16px; color:var(--muted); }
.qb-rule { border:0; border-top:1px solid var(--rule); width:60%; margin:20px auto; }
.qb-answer { font-family: "Iowan Old Style", Palatino, "Palatino Linotype", Georgia, serif;
  font-size:30px; font-weight:600; color:var(--accent); line-height:1.25; }
.qb-answer u { text-decoration-thickness:2px; text-underline-offset:4px; }
.qb-accept { font-size:15px; color:var(--muted); margin-top:6px; }
.qb-accept:before { content:"accept: "; font-style:italic; }
.qb-extra { text-align:left; background:var(--tint); border-left:3px solid var(--accent);
  padding:10px 14px; margin:18px auto 0; max-width:600px; font-size:17px; border-radius:2px; }
.qb-conf { font-size:15px; color:var(--muted); margin-top:12px; }
.qb-conf:before { content:"not to be confused with "; font-style:italic; }
.qb-fig { margin:20px auto 0; display:inline-block; max-width:100%; }
.qb-fig img { max-width:100%; max-height:46vh; height:auto; background:var(--plate);
  padding:6px; border:1px solid var(--rule); box-shadow:0 1px 3px rgba(0,0,0,.12); cursor:zoom-in; }
.qb-fig figcaption { font-size:13.5px; color:var(--muted); margin-top:6px; max-width:560px; }
.qb-qpic img { max-height:58vh; }
.qb-cap { font-size:13.5px; color:var(--muted); margin-top:10px; }
.qb-question { font-size:22px; margin-top:14px; }
.qb-foot { margin-top:22px; display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }
.qb-pill { font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted);
  border:1px solid var(--rule); border-radius:999px; padding:3px 10px; }
.qb-pill:empty { display:none; }
/* QB List: the other items stay hidden on the front */
.qb-list { text-align:left; display:inline-block; max-width:600px; }
.qb-list ol, .qb-list ul { padding-left:1.4em; margin:8px 0; }
.qb-list li { margin:4px 0; }
.qb-title { font-size:20px; font-weight:600; margin-bottom:6px; }
.qb-front .cloze-inactive { color:transparent !important; background:var(--rule); border-radius:3px; }
.qb-front .cloze-inactive * { color:transparent !important; }
.cloze { font-weight:700; color:var(--accent); }
/* QB Tossup */
.qb-tu { text-align:left; display:inline-block; max-width:600px; }
.qb-tu p { margin:0 0 10px; }
.qb-front .qb-tu p.later { display:none; }
.qb-next { margin-top:10px; font:inherit; font-size:14px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--accent); background:none; border:1px solid var(--accent); border-radius:999px;
  padding:6px 16px; cursor:pointer; }
.qb-back .qb-next { display:none; }
.qb-grade { font-size:13px; color:var(--muted); margin-top:16px; }
"""

TIER_JS = r"""<script>(function(){var t="{{Tags}}".split(" "),m={"tier1-core":"Tier 1 · Core",
"tier2-solid":"Tier 2 · Solid","tier3-deepcut":"Tier 3 · Deep cut","tier4-rare":"Tier 4 · Rare"},o="";
t.forEach(function(x){var k=x.split("::").pop();if(m[k])o=m[k];});
var e=document.getElementById("qb-tier");if(e)e.textContent=o;})();</script>"""

ZOOM_JS = r"""<script>(function(){document.querySelectorAll(".qb-fig img").forEach(function(i){
i.onclick=function(){var f=i.closest("figure");if(f.dataset.big){i.style.maxHeight="";delete f.dataset.big;}
else{i.style.maxHeight="none";f.dataset.big=1;}};});})();</script>"""

FOOT = ('<div class="qb-foot"><span class="qb-pill" id="qb-tier"></span>'
        '{{#Entity}}<span class="qb-pill">{{Entity}}</span>{{/Entity}}</div>' + TIER_JS)

FIG = ('{{#Image}}<figure class="qb-fig">{{Image}}{{#Caption}}<figcaption>{{Caption}}</figcaption>'
       '{{/Caption}}</figure>{{/Image}}')

ANSWER = ('<div class="qb-answer">{{Answer}}</div>'
          '{{#Accept}}<div class="qb-accept">{{Accept}}</div>{{/Accept}}')

CLUE = dict(
    name="QB Clue",
    fields=["Prompt", "Answer", "Accept", "Extra", "Image", "Caption", "Picture", "PictureQuestion",
            "Confusable", "Entity", "Sources"],
    templates=[
        dict(Name="CLUE to ANSWER",
             Front='<div class="qb qb-front"><div class="qb-prompt">{{Prompt}}</div></div>',
             Back=('<div class="qb qb-back"><div class="qb-prompt">{{Prompt}}</div><hr class="qb-rule">'
                   + ANSWER + '{{#Extra}}<div class="qb-extra">{{Extra}}</div>{{/Extra}}'
                   '{{#Confusable}}<div class="qb-conf">{{Confusable}}</div>{{/Confusable}}'
                   + FIG + FOOT + '</div>' + ZOOM_JS)),
        dict(Name="PICTURE to ANSWER",
             Front=('{{#Picture}}<div class="qb qb-front"><figure class="qb-fig qb-qpic">{{Picture}}</figure>'
                    '<div class="qb-question">{{PictureQuestion}}</div></div>{{/Picture}}'),
             Back=('{{#Picture}}<div class="qb qb-back"><figure class="qb-fig qb-qpic">{{Picture}}</figure>'
                   '<div class="qb-question" style="color:var(--muted);font-size:16px">{{PictureQuestion}}</div>'
                   '<hr class="qb-rule">' + ANSWER +
                   '{{#Caption}}<div class="qb-cap">{{Caption}}</div>{{/Caption}}'
                   '{{#Extra}}<div class="qb-extra">{{Extra}}</div>{{/Extra}}' + FOOT + '</div>{{/Picture}}'
                   + ZOOM_JS)),
    ])

LIST = dict(
    name="QB List",
    is_cloze=True,
    fields=["Text", "Title", "Extra", "Image", "Caption", "Entity", "Sources"],
    templates=[
        dict(Name="LIST ITEM",
             Front=('<div class="qb qb-front"><div class="qb-kicker">name the hidden one</div>'
                    '<div class="qb-list"><div class="qb-title">{{Title}}</div>{{cloze:Text}}</div></div>'),
             Back=('<div class="qb qb-back"><div class="qb-list"><div class="qb-title">{{Title}}</div>'
                   '{{cloze:Text}}</div>{{#Extra}}<div class="qb-extra">{{Extra}}</div>{{/Extra}}'
                   + FIG + FOOT + '</div>' + ZOOM_JS)),
    ])

TOSSUP = dict(
    name="QB Tossup",
    fields=["Clue1", "Clue2", "Clue3", "Clue4", "Giveaway", "Answer", "Accept", "Extra", "Image",
            "Caption", "Entity", "Sources"],
    templates=[
        dict(Name="PYRAMID",
             Front=('<div class="qb qb-front"><div class="qb-kicker">buzz as early as you can</div>'
                    '<div class="qb-tu" id="qb-tu"><p>{{Clue1}}</p>{{#Clue2}}<p class="later">{{Clue2}}</p>{{/Clue2}}'
                    '{{#Clue3}}<p class="later">{{Clue3}}</p>{{/Clue3}}{{#Clue4}}<p class="later">{{Clue4}}</p>{{/Clue4}}'
                    '<p class="later"><b>{{Giveaway}}</b></p></div><br>'
                    '<button class="qb-next" onclick="var p=document.querySelector(\'#qb-tu p.later\');'
                    'if(p){p.classList.remove(\'later\');}if(!document.querySelector(\'#qb-tu p.later\'))'
                    '{this.style.display=\'none\';}">next clue</button></div>'),
             Back=('<div class="qb qb-back"><div class="qb-tu"><p>{{Clue1}}</p>{{#Clue2}}<p>{{Clue2}}</p>{{/Clue2}}'
                   '{{#Clue3}}<p>{{Clue3}}</p>{{/Clue3}}{{#Clue4}}<p>{{Clue4}}</p>{{/Clue4}}'
                   '<p><b>{{Giveaway}}</b></p></div><hr class="qb-rule">' + ANSWER +
                   '{{#Extra}}<div class="qb-extra">{{Extra}}</div>{{/Extra}}' + FIG +
                   '<div class="qb-grade">Easy = first clue · Good = mid-question · Hard = giveaway · '
                   'Again = missed</div>' + FOOT + '</div>' + ZOOM_JS)),
    ])

MODELS = [CLUE, LIST, TOSSUP]
