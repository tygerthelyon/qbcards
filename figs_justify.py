# -*- coding: utf-8 -*-
"""figs_justify.py -- pictures in a row share one height (Architecture and Art).

Carter (2026-09-25): the Ospedale degli Innocenti back "moves the two images onto
separate rows", and the Heydar Aliyev Center "has two images of different
sizes". A fixed height wraps wide pictures onto separate rows; equal-width cells
give pictures of different shapes different heights. Neither can be fixed in CSS,
which does not know each picture's proportions.

So a small script lays each picture block out as justified rows: 2 or 3 pictures
in one row (3 only while each stays 170px
tall, else 1 + 2), 4 as two rows of two. Each picture's width is its aspect ratio times
the row height, and the row height is whatever makes the row fill the card, capped
at 300px (a lone picture is left to the stylesheet). Pictures are never cropped
or stretched. It runs again when images load and when the window resizes.

    py -3.9 figs_justify.py --dry | --apply
"""
import json
import sys
import time

import concept_add as C

SCRIPT = r"""<script id="qb-justify">
(function () {
  var SEL = ".arch-figs, .arch-concept-figs, .cap-figs, .art-figs, .art-concept-figure";
  var MAXH = 300, GAP = 10;
  function kids(box) {
    return Array.prototype.filter.call(box.children, function (k) {
      return k.className !== "qb-jbreak" && (k.tagName === "IMG" || (k.querySelector && k.querySelector("img")));
    });
  }
  function img(k) { return k.tagName === "IMG" ? k : k.querySelector("img"); }
  function imp(el, p, v) { el.style.setProperty(p, v, "important"); }
  function lay(box) {
    var ks = kids(box);
    if (ks.length < 2) { return; }
    for (var i = 0; i < ks.length; i++) {
      var m = img(ks[i]);
      if (!m.complete || !m.naturalWidth) { return; }
    }
    var W = box.clientWidth;
    if (!W) { return; }
    // three in a row is too small on a phone: keep one row only while the
    // pictures stay at least MINH tall, else the first alone and two below
    var MINH = 170;
    function rowH(row) {
      var sum = 0;
      row.forEach(function (k) { var m = img(k); sum += m.naturalWidth / m.naturalHeight; });
      return (W - GAP * (row.length - 1) - 2) / sum;
    }
    var rows = ks.length === 4 ? [ks.slice(0, 2), ks.slice(2)] : [ks];
    if (ks.length === 3 && rowH(ks) < MINH) { rows = [ks.slice(0, 1), ks.slice(1)]; }
    if (ks.length > 4 && rowH(ks) < MINH) {
      rows = []; for (var r = 0; r < ks.length; r += 2) { rows.push(ks.slice(r, r + 2)); }
    }
    imp(box, "display", "flex"); imp(box, "flex-wrap", "wrap"); imp(box, "flex-direction", "row");
    imp(box, "width", "100%");
    imp(box, "justify-content", "center"); imp(box, "align-items", "flex-start");
    imp(box, "gap", "8px " + GAP + "px");
    var brs = box.querySelectorAll(".qb-jbreak"), ok = brs.length === rows.length - 1;
    for (var bi = 0; ok && bi < brs.length; bi++) { ok = brs[bi].nextElementSibling === rows[bi + 1][0]; }
    if (!ok) { Array.prototype.forEach.call(brs, function (x) { x.remove(); }); }
    rows.forEach(function (row, ri) {
      if (ri > 0 && !ok) {
        // force the next row: a zero-height, full-width flex item before it
        var br = document.createElement("div");
        br.className = "qb-jbreak";
        br.style.cssText = "flex:0 0 100% !important;height:0;margin:0;padding:0;";
        box.insertBefore(br, row[0]);
      }
      var sum = 0;
      row.forEach(function (k) { var m = img(k); sum += m.naturalWidth / m.naturalHeight; });
      var h = Math.min(MAXH, (W - GAP * (row.length - 1) - 2) / sum);
      row.forEach(function (k) {
        var m = img(k), w = Math.floor(h * m.naturalWidth / m.naturalHeight);
        imp(k, "flex", "0 0 " + w + "px"); imp(k, "width", w + "px"); imp(k, "max-width", "none");
        imp(k, "min-width", "0"); imp(k, "margin", "0");
        if (k !== m) { imp(m, "width", "100%"); }
        else { imp(m, "width", w + "px"); }
        imp(m, "height", "auto"); imp(m, "max-height", "none"); imp(m, "max-width", "100%");
        imp(m, "background", "none");
      });
    });
  }
  function all() { Array.prototype.forEach.call(document.querySelectorAll(SEL), lay); }
  all();
  Array.prototype.forEach.call(document.querySelectorAll(SEL + " img"), function (m) {
    if (!m.complete) { m.addEventListener("load", all); }
  });
  window.addEventListener("resize", all);
  // the Art caption script rebuilds the figures after load, wiping these widths:
  // lay out again whenever a picture block gains new children (not our breaks)
  var pend = null;
  new MutationObserver(function (ms) {
    for (var i = 0; i < ms.length; i++) {
      for (var j = 0; j < ms[i].addedNodes.length; j++) {
        var n = ms[i].addedNodes[j];
        if (n.nodeType === 1 && n.className !== "qb-jbreak") {
          clearTimeout(pend); pend = setTimeout(all, 30); return;
        }
      }
    }
  }).observe(document.body, { childList: true, subtree: true });
  [60, 300, 900, 1600].forEach(function (t) { setTimeout(all, t); });
})();
</script>
"""


def main():
    apply = "--apply" in sys.argv
    stamp = time.strftime("%Y%m%d_%H%M")
    for model in ("Architecture", "Art"):
        t = C.anki("modelTemplates", modelName=model)
        upd = {}
        for k, v in t.items():
            sides = {}
            for side in ("Front", "Back"):
                s = v[side]
                if 'id="qb-justify"' in s:
                    continue
                if not any(c in s for c in ("arch-figs", "arch-concept-figs", "cap-figs", "art-figs", "art-concept-figure")):
                    continue
                sides[side] = s + "\n" + SCRIPT
            if sides:
                upd[k] = sides
                print(model, "|", k, "|", ", ".join(sides))
        if apply and upd:
            json.dump(t, open("templates_backup/%s_before_justify_%s.json" % (model.lower(), stamp), "w",
                              encoding="utf-8"), ensure_ascii=False)
            C.anki("updateModelTemplates", model={"name": model, "templates": upd})
    print("applied" if apply else "dry run")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
