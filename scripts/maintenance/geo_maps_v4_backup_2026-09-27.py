# -*- coding: utf-8 -*-
"""geo_maps_v4.py -- the Geography map standard, 2026-09-26.

Every map note gets three images:
  front   (Map)          the place in red with its surroundings named -- never the answer
  back    (Map Labeled)  the same frame: the answer, the capital starred clear of it, a country's main cities
  locator (Map Wide)     zoomed out, unlabelled: where in the world this is

THE STANDARD (Carter's review, three rounds)
  Projection   equal-area, centred on each map. The old flat lon/lat grid stretched everything big or
               far from the equator ("lots of the maps are warped").
  Colour       the place's own country cream, other land a light warm grey, water light blue, the place
               red. No dark fills ("too dark").
  Lines        international borders always. Internal borders only for the place's own country (a
               province against its sister provinces), and for a neighbouring country only when it is a
               big federal state whose states are asked about (US, Canada, Mexico, Brazil, Argentina,
               Australia, Russia, China, India). A country never shows its own subdivisions ("too many
               subdivisions" on Uruguay, Belize's neighbours).
  Labels       every label helps identify the place: first whatever borders or touches it (neighbouring
               countries or provinces, the waters it touches, rivers crossing or bounding it), then a few
               for orientation while a budget of about 11 lasts. No minor districts, no far-off names.
               Fewer labels, larger type: the smallest is readable at phone width.
  Zoom         the place fills about half the frame; tall places (the Nile, the Andes, Chile) portrait;
               anything too small to see ringed.
  Locator      a province, city, peak or feature inside one country: that whole country, centred. A
               country: its region (the continent when it fills its region). A sea, strait or feature
               across several countries: its continent-scale surroundings. Always at least twice the
               front map's extent, the place never on an edge.

    py -3.9 geo_maps_v4.py --names "Hunan|Belize" [--out renders/geo_v4]
    py -3.9 geo_maps_v4.py --kinds subdivision,country
"""
import argparse
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "archive", "scripts"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import concept_add as C
import ne_render as N
import ne_country as K
import ne_region as R
import ne_points as P
import ne_historical as H
import ne_fronts as NF

LADDER = (1.0, 1.4, 2.0, 3.0, 5.0)
COMPACT_LADDER = (1.4, 1.8, 2.6, 4.0, 6.0)   # a province, country or island: room around it
LONG_KINDS = {"river", "range", "desert"}     # long features fill the frame with a tighter margin
LOCATOR_MIN = 2.2          # the locator spans at least this many times the front map
LOCATOR_MIN_FREE = 4.0     # ... more when no country frames it (a lake, a strait, a sea)
LOCATOR_EDGE = 0.10        # the place stays at least this share of the frame away from every edge
REGION_KINDS = set(R.KINDS)
POINT_KINDS = set(P.KIND_LAYER)
BOX = {"United States of America": (-125, 24, -66, 50), "Canada": (-141, 41.5, -52, 72), "Russia": (27, 41, 180, 78),
       "France": (-5.2, 41.3, 9.6, 51.2), "Norway": (4.5, 57.8, 31.5, 71.3), "Netherlands": (3.3, 50.7, 7.3, 53.6),
       "Chile": (-76, -56, -66, -17.5), "New Zealand": (166, -47.5, 178.8, -34), "Denmark": (8, 54.5, 15.3, 57.8),
       "Spain": (-9.5, 35.8, 4.4, 43.9), "Portugal": (-9.6, 36.9, -6.1, 42.2), "Ecuador": (-81.1, -5.1, -75.1, 1.5)}
SUBREGION_BOX = {"Northern America": (-130, 20, -60, 62), "Western Europe": (-6, 41, 17, 56), "Northern Europe": (-25, 49, 33, 71),
                 "Eastern Europe": (12, 40, 60, 62), "Southern Europe": (-10, 34, 30, 48), "Western Asia": (25, 11, 63, 45),
                 "Southern Asia": (60, 5, 98, 39), "South-Eastern Asia": (92, -11, 142, 29), "Eastern Asia": (73, 18, 146, 54),
                 "Central Asia": (46, 34, 88, 56), "Northern Africa": (-18, 14, 38, 38), "Western Africa": (-18, 3, 17, 26),
                 "Middle Africa": (7, -19, 32, 24), "Eastern Africa": (21, -27, 52, 18), "Southern Africa": (10, -35, 34, -16),
                 "Central America": (-94, 6.5, -76, 22), "Caribbean": (-86, 9.5, -58, 27.5), "South America": (-82, -56, -34, 13),
                 "Australia and New Zealand": (111, -48, 179, -9), "Melanesia": (140, -23, 180, 0), "Micronesia": (130, -2, 180, 20),
                 "Polynesia": (-180, -25, -140, 0)}
CONTINENT_BOX = {"North America": (-140, 8, -52, 72), "South America": (-85, -56, -33, 13), "Europe": (-25, 34, 45, 71),
                 "Africa": (-19, -36, 52, 38), "Asia": (40, -10, 150, 60), "Oceania": (110, -48, 180, 0)}
REGION_GROUP = {"Canary Islands": ("Spain", "Canary Is.")}
# name -> (OSM boundary file, the country it lies inside)
SHAPE = {"Transnistria": (os.path.join(HERE, "data", "geo_shapes", "transnistria.geojson"), "Moldova")}
FORCE = {"Río de la Plata": ["Uruguay", "Paraná"]}
BOTH_HAND = {"Río de la Plata": [(-59.1, -33.95, "Paraná R."), (-58.0, -31.3, "Uruguay R.")]}
# hand-drawn polities over modern borders: name -> (outline, modern country whose states are drawn, caption)
HAND_HIST = {"Republic of Texas": (NF.TEXAS, "United States of America", "Claimed extent c. 1840 (approximate); modern states shown"),
             "Phoenicia": (NF.PHOENICIA, None, "Heartland c. 1000 BCE (approximate); modern countries shown")}
ASP = [4 / 3]
HIST_EXTRA = {"Weimar Republic": ["East Prussia"]}   # a separate feature in the 1930 snapshot, but part of Germany
_PLACES = []


def setup():
    N.FORCE_BY_NAME.update(FORCE)
    N.NO_INSET = True
    N.ADMIN1_LABELS = True
    N.NEIGHBOUR_ADMIN1_LINES = True
    N.RIVER_MAX = 4
    P.NO_INSET = True
    reset()


def reset():
    ASP[0] = 4 / 3
    N.ASPECT, N.W_PX, N.H_PX = 4 / 3, 1600, 1200
    N.MARGIN = 1.45
    N.OTHER_GREY = False
    N.GREY_EXCEPT = None
    N.REGION_NOLABEL = False
    N.EXTRA_WITH_REGIONS = False
    N.OVER_TARGET_COUNTRIES = False
    N.EXTRA_LABELS = []
    N.CITY_POINTS = ()
    N.VIEW_SCALE, N.TINY_LABELS = 1.0, False
    N.PROJ = None


# ---------------------------------------------------------------- geometry helpers (lon/lat unless noted)

def pad(b, f=0.06):
    dx, dy = (b[2] - b[0]) * f, (b[3] - b[1]) * f
    return (b[0] - dx, b[1] - dy, b[2] + dx, b[3] + dy)


def centre(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def bbox_of(feats):
    return (min(ft["_bbox"][0] for ft in feats), min(ft["_bbox"][1] for ft in feats),
            max(ft["_bbox"][2] for ft in feats), max(ft["_bbox"][3] for ft in feats))


def country_ft(admin):
    return N.country_index().get(N.norm(admin)) or K.target(admin)


def country_box(admin):
    if admin in BOX:
        return BOX[admin]
    ft = country_ft(admin)
    return pad(K.mainland(ft)["_bbox"], 0.02) if ft is not None else None


def box_proj(b):
    """a lon/lat box's extent in the current projection (its edges sampled, not just its corners)"""
    t = np.linspace(0, 1, 40)
    pts = np.vstack([np.column_stack([b[0] + (b[2] - b[0]) * t, np.full_like(t, b[1])]),
                     np.column_stack([b[0] + (b[2] - b[0]) * t, np.full_like(t, b[3])]),
                     np.column_stack([np.full_like(t, b[0]), b[1] + (b[3] - b[1]) * t]),
                     np.column_stack([np.full_like(t, b[2]), b[1] + (b[3] - b[1]) * t])])
    q = N.project(pts)
    return (q[:, 0].min(), q[:, 1].min(), q[:, 0].max(), q[:, 1].max())


# the Neo-Assyrian Empire at its height (c. 671 BCE, after Esarhaddon took Egypt): Mesopotamia with Babylonia, the
# Levant, Cilicia and south-east Anatolia, the western Zagros, Cyprus (tributary), and the Nile valley to Thebes --
# built from the modern units that cover it, so the outline follows real coasts and rivers
ASSYRIA_UNITS = {"Iraq": None, "Syria": None, "Lebanon": None, "Israel": None, "Palestine": None, "Jordan": None, "Cyprus": None,
                 "Egypt": ["Ad Daqahliyah", "Al Buhayrah", "Al Fayyum", "Al Gharbiyah", "Al Iskandariyah", "Al Isma`iliyah",
                           "Al Jizah", "Al Minufiyah", "Al Minya", "Al Qahirah", "Al Qalyubiyah", "As Suways", "Ash Sharqiyah",
                           "Asyut", "Bani Suwayf", "Bur Sa`id", "Dumyat", "Kafr ash Shaykh", "Luxor", "Qina", "Suhaj", "Shamal Sina'"],
                 "Turkey": ["Hatay", "Adana", "Mersin", "Osmaniye", "Gaziantep", "Kilis", "Sanliurfa", "Mardin", "Diyarbakir",
                            "Batman", "Siirt", "Sirnak", "Hakkari", "Adiyaman", "K. Maras", "Malatya"],
                 "Iran": ["Kermanshah", "Ilam", "Kordestan"]}
ASSYRIA_LABELS = [("Urartu", 43.6, 39.9), ("Phrygia", 31.2, 39.4), ("Lydia", 28.2, 38.6), ("Media", 49.4, 35.4),
                  ("Elam", 49.3, 31.0), ("Arabian tribes", 41.0, 28.5), ("Kush", 32.5, 21.0)]


def assyria_rings():
    rs = []
    a0 = N._layer_ll("ne_10m_admin_0_countries")
    a1 = R._admin1_ll()
    for c, units in ASSYRIA_UNITS.items():
        if units is None:
            rs += [r for f in a0 if f["_p"].get("admin") == c or f["_p"].get("name") == c for r in f["_rings"]]
        else:
            want = {N.norm(u) for u in units}
            rs += [r for f in a1 if f["_p"].get("admin") == c and N.norm(f["_p"].get("name") or "") in want for r in f["_rings"]]
    return N.dissolve(rs)


def shape_feat(nm):
    g = json.load(open(SHAPE[nm][0], encoding="utf-8"))
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    rings = [np.array(p[0]) for p in polys]
    a = np.vstack(rings)
    return {"geometry": {"type": "MultiPolygon"}, "_rings": rings, "_p": {"name": nm, "name_en": nm},
            "_bbox": (a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max())}


def main_cities(admin, capital, n=3):
    if not _PLACES:
        for ft in json.load(open(os.path.join(N.NE, "ne_10m_populated_places.geojson"), encoding="utf-8"))["features"]:
            p = ft["properties"]
            _PLACES.append((p.get("ADM0NAME"), p.get("POP_MAX") or 0, p.get("NAME"), ft["geometry"]["coordinates"]))
    rows = sorted((r for r in _PLACES if r[0] == admin and r[1] >= 100000), key=lambda r: -r[1])
    cap = N.norm(capital or "")
    return tuple((c[0], c[1], nm) for _, _, nm, c in rows if N.norm(nm) != cap and N.norm(nm) not in cap)[:n]


# ---------------------------------------------------------------- drawing

def set_aspect(tb):
    """tall, narrow places (the Nile, the Andes, Chile) portrait; everything else 4:3 landscape. tb projected."""
    w, h = tb[2] - tb[0], tb[3] - tb[1]
    ASP[0] = 3 / 4 if h > 1.6 * w else 4 / 3
    N.ASPECT = ASP[0]
    N.W_PX, N.H_PX = (1600, 1200) if ASP[0] > 1 else (1200, 1600)


def pair(fp, bp, draw, ladder=LADDER):
    """the labelled back first, widening until three neighbours are named; the front at that same rung"""
    ladder = tuple(ladder)
    for tight in (1.2, 1.0, 0.85):
        N.VIEW_SCALE = ladder[0]
        if draw(True, bp)[0]:
            break
        ladder = (tight,) + tuple(x for x in ladder if x > tight)   # too wide to draw (Greenland): tighter
    chosen = None
    for sc in ladder:
        N.VIEW_SCALE, N.TINY_LABELS = sc, sc > 1.4
        v, why = draw(True, bp)
        if not v:
            break
        chosen = sc
        if N.LAST_LABELS >= 3:
            break
    if chosen is None:
        return None, "no frame could be drawn"
    N.VIEW_SCALE, N.TINY_LABELS = chosen, chosen > 1.4
    v, _ = draw(True, bp)
    v2, why = draw(False, fp)
    return v, why


def locator(png, lon_lat_box, targets_ll, front_v, centred=True, mult=LOCATOR_MIN, admin=None, point=None,
            water=False, line=False, lines=False):
    """the zoomed-out map. The frame is the box given (a country, a region), centred on it; grown about its own
    centre until it is `mult` times the front map and the place sits clear of every edge."""
    cbox = lon_lat_box
    c_ll = centre(cbox) if centred else (centre(bbox_of(targets_ll)) if targets_ll else point)
    N.PROJ = (round(c_ll[0], 3), round(c_ll[1], 3))
    try:
        tgt = [N.proj_feat(ft) for ft in targets_ll]
        # the country's internal lines only when the place is one of its provinces (Hunan among China's);
        # for a city, a peak, a lake or Transnistria they were just clutter
        regions = [u for u in R.admin1() if u["_p"].get("admin") == admin] if (admin and lines) else []
        if admin:
            cf = country_ft(admin)      # admin-1 says "Czech Republic", admin-0 "Czechia": grey by the admin-0 name
            admin0 = cf["_p"].get("admin") if cf is not None else admin
        else:
            admin0 = None
        pt = N.project_pt(*point) if point else None
        b = box_proj(cbox)
        cx, cy = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) if centred else (0.0, 0.0)
        a = ASP[0]
        w, h = b[2] - b[0], b[3] - b[1]
        if not centred:
            w = h = 0.0
        # the place clear of the edges, the frame centred where it was asked to be
        tb = bbox_of(tgt) if tgt else (pt[0], pt[1], pt[0], pt[1])
        need_w = 2 * max(abs(tb[0] - cx), abs(tb[2] - cx)) / (1 - 2 * LOCATOR_EDGE)
        need_h = 2 * max(abs(tb[1] - cy), abs(tb[3] - cy)) / (1 - 2 * LOCATOR_EDGE)
        w, h = max(w, need_w), max(h, need_h)
        fh = (front_v[3] - front_v[2]) if front_v else 0
        fw = (front_v[1] - front_v[0]) if front_v else 0
        w, h = max(w, mult * fw), max(h, mult * fh)
        if w / max(h, 1e-9) < a:
            w = h * a
        else:
            h = w / a
        if h > 120:
            w, h = 120 * a, 120.0
        v = (cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2)
        fig = plt.figure(figsize=(N.W_PX / N.DPI, N.H_PX / N.DPI), dpi=N.DPI)
        fig.patch.set_facecolor(N.SEA)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(v[0], v[1])
        ax.set_ylim(v[2], v[3])
        ax.set_aspect(1, adjustable="datalim")
        ax.axis("off")
        N.OTHER_GREY = bool(admin)
        saved = N.NEIGHBOUR_ADMIN1_LINES
        N.NEIGHBOUR_ADMIN1_LINES = False
        try:
            N.base_map(ax, v, detail=True, labels=False, regions=regions, skip_admin=admin0)
        finally:
            N.OTHER_GREY = False
            N.NEIGHBOUR_ADMIN1_LINES = saved
        if tgt:
            if line:
                N.draw_lines(ax, tgt, v, colors="white", linewidths=6, zorder=5)
                N.draw_lines(ax, tgt, v, colors="#d62d20", linewidths=3.2, zorder=6)
            elif water:
                N.draw_polys(ax, tgt, v, facecolor="#3d8ee0", edgecolor="#d62d20", linewidth=2.6, zorder=5)
            else:
                N.draw_polys(ax, tgt, v, facecolor=(0.86, 0.24, 0.17, 0.55), edgecolor="#c0392b", linewidth=2.6, zorder=5)
            allp = np.vstack([r for ft in tgt for r in ft["_rings"] if len(r)])
            px = ax.transData.transform(allp)
            if (px[:, 0].max() - px[:, 0].min()) < 40 and (px[:, 1].max() - px[:, 1].min()) < 40:
                pt = (float(allp[:, 0].mean()), float(allp[:, 1].mean()))   # too small to see at this scale: ringed
        if pt:
            ax.plot([pt[0]], [pt[1]], marker="o", markersize=15, color="#d62d20", markeredgecolor="white",
                    markeredgewidth=2.5, zorder=9)
            ax.plot([pt[0]], [pt[1]], marker="o", markersize=40, markerfacecolor="none", markeredgecolor="#d62d20",
                    markeredgewidth=2.8, zorder=8)
        fig.savefig(png, dpi=N.DPI, facecolor=N.SEA)
        plt.close(fig)
    finally:
        N.PROJ = None


def free_mult(front_v):
    """how far a locator with no country to frame it zooms out: a lot for a small place, less for a big one --
    the Sahara at four times its front map was a whole hemisphere"""
    fh = (front_v[3] - front_v[2]) if front_v else 10
    return 6.0 if fh < 10 else 3.0 if fh < 25 else 2.0


def far_place_locator(lp, m, cbox, front_v, admin, water=False, line=False):
    """a region away from its country's mainland (the Canaries, Madeira, Greenland, Réunion): centred on the place.
    The country is brought into the frame, and drawn cream against grey, only when it is near enough to share one
    readable view; otherwise the place is shown in its own surroundings"""
    targets = m if isinstance(m, list) else [m]
    tb = bbox_of(targets)
    cx, cy = centre(tb)
    reach_x = max(abs(cbox[0] - cx), abs(cbox[2] - cx))
    reach_y = max(abs(cbox[1] - cy), abs(cbox[3] - cy))
    k = math.cos(math.radians(max(-70.0, min(70.0, cy))))
    if max(reach_x * k, reach_y) <= 24:
        box = (cx - reach_x, cy - reach_y, cx + reach_x, cy + reach_y)
        locator(lp, box, targets, front_v, admin=admin, mult=1.0, water=water, line=line)
    else:
        locator(lp, tb, targets, front_v, centred=False, mult=free_mult(front_v), water=water, line=line)


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", N.norm(s)).strip("_")


def do_hist(f, nm, fp, bp, lp):
    """a historical polity: against its contemporaries when a border snapshot exists, else a hand-drawn outline
    over modern borders; the locator is a modern map with the extent in red"""
    saved = (N.COUNTRIES_OVERRIDE, N.NO_DETAIL, N.MAP_CAPTION, N.CLIP_SEA, N.EXTRA_LABELS)
    skip_admin, others = None, None
    try:
        if nm in HAND_HIST:
            pts, admin, cap = HAND_HIST[nm]
            a = np.array(pts, dtype=float)
            m = {"geometry": {"type": "Polygon"}, "_rings": [a], "_p": {"name": nm},
                 "_bbox": (a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max())}
            skip_admin = admin
            N.MAP_CAPTION, N.CLIP_SEA = cap, True
        else:
            year, want, box = H.SPEC[nm]
            want = list(want) + HIST_EXTRA.get(nm, [])
            feats = H.snapshot(year)
            tf = [x for x in feats if x["_raw"] in want]
            if not tf:
                return {"status": "no snapshot feature"}
            others = []
            for x in feats:
                g = dict(x)
                g["_p"] = dict(x["_p"])
                if x["_raw"] in want:
                    g["_p"]["_nolabel"] = True
                others.append(g)
            rs = [r for x in tf for r in x["_rings"]]
            for bx in H.EXCLUDE.get(nm, []):
                rs = [r for r in rs if not (r[:, 0].min() >= bx[0] and r[:, 1].min() >= bx[1] and r[:, 0].max() <= bx[2] and r[:, 1].max() <= bx[3])]
            if nm == "Assyria":
                rs = assyria_rings()
                others = [{"geometry": x["geometry"], "_rings": x["_rings"], "_p": {"name": ""}, "_bbox": x["_bbox"]}
                          for x in N._layer_ll("ne_10m_land")]
            elif nm in H.MANUAL:
                rs = [np.array(H.MANUAL[nm], dtype=float)]
                others = [{"geometry": x["geometry"], "_rings": x["_rings"], "_p": {"name": ""}, "_bbox": x["_bbox"]}
                          for x in N.layer("ne_10m_land")]
            arr = np.vstack(rs)
            m = {"geometry": tf[0]["geometry"], "_rings": rs, "_p": tf[0]["_p"],
                 "_bbox": (arr[:, 0].min(), arr[:, 1].min(), arr[:, 0].max(), arr[:, 1].max())}
            yl = ("%d BCE" % int(year[2:])) if year.startswith("bc") else ("c. %s" % year)
            N.MAP_CAPTION = "Borders %s (approximate)" % yl
            if nm == "Assyria":
                N.MAP_CAPTION = "The Neo-Assyrian Empire at its height, c. 671 BCE (approximate)"
                N.CLIP_SEA = True
                N.EXTRA_LABELS = [(x, y, t) for t, x, y in ASSYRIA_LABELS]
            elif nm in H.MANUAL_LABELS:
                N.CLIP_SEA = True
                N.EXTRA_LABELS = [(x, y, t) for t, x, y in H.MANUAL_LABELS[nm][2]]
        N.PROJ = tuple(round(c, 3) for c in centre(m["_bbox"]))
        mp = N.proj_feat(m)
        if others is not None:
            N.COUNTRIES_OVERRIDE, N.NO_DETAIL = [N.proj_feat(x) for x in others], True
        regions = [u for u in R.admin1() if u["_p"].get("admin") == skip_admin] if skip_admin else []
        set_aspect(mp["_bbox"])
        N.MIN_SPAN["x"] = 4

        def draw(label, png):
            return N.render({"Name": nm, "Alternate": f["Alternate"]}, "x", [mp], png,
                            target_label=nm if label else None, regions=regions, skip_admin=skip_admin)
        v, why = pair(fp, bp, draw, COMPACT_LADDER)
    finally:
        N.COUNTRIES_OVERRIDE, N.NO_DETAIL, N.MAP_CAPTION, N.CLIP_SEA, N.EXTRA_LABELS = saved
        N.OTHER_GREY = False
        N.PROJ = None
    locator(lp, m["_bbox"], [m], v, centred=False, mult=free_mult(v))
    return {"status": "rendered" if v else (why or "failed"), "front": fp, "back": bp, "locator": lp}


_SPECIAL = {}
OCEAN_CENTRE = {"Pacific Ocean": (-165.0, 5.0), "Atlantic Ocean": (-30.0, 10.0), "Indian Ocean": (78.0, -18.0),
                "Southern Ocean": (0.0, -75.0), "Arctic Ocean": (0.0, 85.0)}


def special(nm):
    """places the general matcher cannot build, assembled the way ne_more.py and ne_more2.py do: France's old
    regions, the UK's nations, sets of countries (the Maghreb, the EU), continents, oceans, historical regions on
    modern borders, and hand or OpenStreetMap outlines. Returns a spec in lon/lat, or None."""
    import ne_more as M
    import ne_more2 as M2
    if nm in _SPECIAL:
        return _SPECIAL[nm]
    sp = None
    a1 = M2.A1
    if nm in M.FR_OLD:
        fr = [f for f in a1 if f["_p"].get("admin") == "France"]
        by = {N.norm(f["_p"]["name"]): f for f in fr}
        def old(reg):
            fs = [by[N.norm(d)] for d in M.FR_OLD[reg] if N.norm(d) in by]
            return M.feat([r for f in fs for r in f["_rings"]], reg, "France") if fs else None
        m = old(nm)
        sis = [x for x in (old(k) for k in M.FR_OLD if k != nm) if x]
        sp = dict(feat=m, admin="France", sisters=sis, span=3)
    elif nm in M.UK or nm == "England":
        uk = [f for f in a1 if f["_p"].get("admin") == "United Kingdom"]
        nat = {k: M.feat([r for f in uk if f["_p"].get("region") in regs for r in f["_rings"]], k, "United Kingdom") for k, regs in M.UK.items()}
        used = {r for regs in M.UK.values() for r in regs}
        nat["England"] = M.feat([r for f in uk if f["_p"].get("region") not in used for r in f["_rings"]], "England", "United Kingdom")
        sp = dict(feat=K.mainland(nat[nm]), admin="United Kingdom", sisters=[o for k, o in nat.items() if k != nm], span=5)
    elif nm == "French Guiana":
        hits = [f for f in a1 if f["_p"].get("admin") == "France" and f["_p"].get("name") == "Guyane française"]
        if hits:
            sp = dict(feat=K.mainland(M.feat(hits[0]["_rings"], nm)), span=4, owner="France")
    elif nm in M.SETS:
        members, extra, box = M.SETS[nm]
        rs = [r for mb in members for f in M.country(mb) for r in f["_rings"]]
        for c, a in extra:
            rs += [r for f in a1 if f["_p"].get("admin") == c and f["_p"].get("name") == a for r in f["_rings"]]
        if rs:
            sp = dict(feat=M.feat(rs, nm), box=box, multi=True, span=5)
    elif nm in M.CONT:
        cont, box = M.CONT[nm]
        rs = [r for f in N._layer_ll("ne_50m_admin_0_countries") if f["_p"].get("continent") == cont for r in f["_rings"]
              if box[0] <= r[:, 0].mean() <= box[2] and box[1] <= r[:, 1].mean() <= box[3]]
        if rs:
            sp = dict(feat=M.feat(rs, nm), box=box, span=20, world=True)
    elif nm in M2.OCEAN:
        fs = M2.marine(*M2.OCEAN[nm])
        if fs:
            rs = [r for f in fs for r in f["_rings"]]
            if len(fs) > 1:
                rs = N.dissolve(rs)      # the North and South Pacific polygons, without the seam between them
            a = np.vstack(rs)
            sp = dict(feat={"geometry": {"type": "Polygon"}, "_rings": rs, "_p": {"name": nm},
                            "_bbox": (a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max())},
                      kind="sea", over=True, span=60, world=True, noring=True)
    elif nm in M2.S:
        d = M2.S[nm]
        try:
            fs = d["feats"]()
        except Exception as e:
            print("   special failed", nm, e)
            fs = []
        if fs:
            rs = [r for f in fs for r in f["_rings"]]
            over = d.get("over", False)
            a = np.vstack(rs)
            m = M.feat(rs, nm) if not over else {"geometry": {"type": "Polygon"}, "_rings": rs, "_p": {"name": nm},
                                                  "_bbox": (a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max())}
            admins = {f["_p"].get("admin") for f in fs if f.get("_p")}
            admin = next(iter(admins)) if len(admins) == 1 and None not in admins and not any(
                N.norm(f["_p"].get("admin") or "") == N.norm(f["_p"].get("name") or "") for f in fs) else None
            sis = [M.feat([r for f in M2.S[sb]["feats"]() for r in f["_rings"]], sb) for sb in M2.SISTER.get(nm, []) if sb in M2.S]
            sp = dict(feat=m, cap=d.get("cap", ""), kind=d.get("kind", "x"), over=over, clip=d.get("clip", False),
                      span=d.get("span", 5), box=d.get("box"), multi=nm in M2.MULTI_COUNTRY, admin=admin, sisters=sis,
                      noring=d.get("noring", False), world=d.get("wide", False))
    _SPECIAL[nm] = sp
    return sp


def do_special(f, nm, sp, fp, bp, lp):
    m = sp["feat"]
    kind = sp.get("kind", "x")
    saved = (N.MAP_CAPTION, N.LAND_OVER, N.CLIP_SEA, N.NO_RING, N.OVER_TARGET_COUNTRIES)
    try:
        cb = sp.get("box") or m["_bbox"]
        N.PROJ = OCEAN_CENTRE.get(nm) or tuple(round(c, 3) for c in centre(cb))
        mp = N.proj_feat(m)
        if nm in OCEAN_CENTRE:
            h = 26.0 if nm == "Arctic Ocean" else 52.0      # the Arctic is small: a hemisphere left it a speck
            mp = dict(mp, _bbox=(-h * 4 / 3, -h, h * 4 / 3, h))
        elif sp.get("box"):
            mp = dict(mp, _bbox=box_proj(sp["box"]))
        regions = [N.proj_feat(x) for x in sp.get("sisters", [])]
        admin = sp.get("admin")
        set_aspect(mp["_bbox"])
        N.MIN_SPAN[kind] = sp.get("span", 5)
        N.MAP_CAPTION, N.LAND_OVER, N.CLIP_SEA, N.NO_RING = sp.get("cap", ""), sp.get("over", False), sp.get("clip", False), sp.get("noring", False)
        N.OVER_TARGET_COUNTRIES = bool(sp.get("multi"))
        N.ALLOW_WIDE = bool(sp.get("world"))
        if kind in LONG_KINDS:
            N.MARGIN = 1.12

        def draw(label, png):
            return N.render({"Name": nm, "Alternate": f["Alternate"]}, kind, [mp], png,
                            target_label=nm if label else None, regions=regions, skip_admin=admin if regions else None)
        ladder = (1.0,) if nm in OCEAN_CENTRE else (0.75, 1.0, 1.4) if sp.get("world") else COMPACT_LADDER
        v, why = pair(fp, bp, draw, ladder)
    finally:
        N.MAP_CAPTION, N.LAND_OVER, N.CLIP_SEA, N.NO_RING, N.OVER_TARGET_COUNTRIES = saved
        N.ALLOW_WIDE = False
        N.PROJ = None
    tb = m["_bbox"]
    owner = sp.get("owner") or admin
    cbox = country_box(owner) if owner else None
    water = kind in N.WATER or kind == "sea"
    if cbox and cbox[0] <= tb[0] and cbox[1] <= tb[1] and cbox[2] >= tb[2] and cbox[3] >= tb[3]:
        locator(lp, cbox, [m], v, admin=owner, water=water)
    elif cbox:
        far_place_locator(lp, m, cbox, v, owner, water=water)
    elif nm in OCEAN_CENTRE:
        c = OCEAN_CENTRE[nm]
        locator(lp, (c[0] - 60, c[1] - 45, c[0] + 60, c[1] + 45), [m], None, water=True)   # the ocean on the globe
    else:
        locator(lp, sp.get("box") or tb, [m], v, centred=False, mult=free_mult(v), water=water)
    return {"status": "rendered" if v else (why or "failed"), "front": fp, "back": bp, "locator": lp}


def do_note(n, out):
    f = {k: C.plain(v["value"]).strip() for k, v in n["fields"].items()}
    f["Alternate"] = n["fields"]["Alternate"]["value"]
    nm, kind = f["Name"], f["Kind"]
    s = slug(nm + " " + kind)
    fp, bp, lp = (os.path.join(out, "%s-%s.png" % (pre, s)) for pre in ("g4front", "g4lab", "g4loc"))
    N.PLACED_NAMES.clear()
    reset()
    if nm in H.SPEC or nm in HAND_HIST:
        return do_hist(f, nm, fp, bp, lp)
    sp = special(nm)
    if sp:
        return do_special(f, nm, sp, fp, bp, lp)

    if nm in SHAPE or kind in REGION_KINDS or nm in REGION_GROUP:
        # ---- a province, state, dependency, territory
        if nm in SHAPE:
            m, hits, is_a1 = shape_feat(nm), [], False
            pass
        elif nm in REGION_GROUP:
            m = K.mainland(next(u for u in R.admin1() if u["_p"].get("name") == REGION_GROUP[nm][1]
                                and u["_p"].get("admin") == REGION_GROUP[nm][0]))
            hits, is_a1 = [m], True
        else:
            hits, is_a1, admins = R.find(nm, f["Parent"], kind)
            if not hits:
                return {"status": "no Natural Earth match"}
            m = K.mainland(R.merge(hits))
        skip_admin = hits[0]["_p"].get("admin") if is_a1 else None
        hit_ids = {id(h) for h in hits}
        span = max(m["_bbox"][2] - m["_bbox"][0], m["_bbox"][3] - m["_bbox"][1])
        N.PROJ = tuple(round(c, 3) for c in centre(m["_bbox"]))
        mp = N.proj_feat(m)
        hit_p = {id(N.proj_feat(h)) for h in hits}
        regions = [u for u in R.admin1() if skip_admin and u["_p"].get("admin") == skip_admin and id(u) not in hit_p]
        set_aspect(mp["_bbox"])
        N.MIN_SPAN["x"] = 3 if span < 1.5 else 5

        def draw(label, png):
            N.EXTRA_LABELS = list(N.HAND_LABELS.get(nm, [])) if label else []
            return N.render({"Name": nm, "Alternate": f["Alternate"]}, "x", [mp], png,
                            target_label=nm if label else None, regions=regions, skip_admin=skip_admin)
        v, why = pair(fp, bp, draw, COMPACT_LADDER)
        N.OTHER_GREY, N.GREY_EXCEPT, N.PROJ = False, None, None
        tb = m["_bbox"]
        if is_a1:
            box = country_box(skip_admin) or pad(tb, 1.5)
            if box[0] <= tb[0] and box[1] <= tb[1] and box[2] >= tb[2] and box[3] >= tb[3]:
                locator(lp, box, [m], v, admin=skip_admin, lines=True)   # the whole country, centred
            else:
                far_place_locator(lp, m, box, v, skip_admin)
        elif len(N.parent_features(f["Parent"])) == 1 and N.norm(N.parent_features(f["Parent"])[0]["_p"].get("admin") or "") != N.norm(nm):
            padm = N.parent_features(f["Parent"])[0]["_p"].get("admin")
            cb = country_box(padm)
            if cb and cb[0] <= tb[0] and cb[1] <= tb[1] and cb[2] >= tb[2] and cb[3] >= tb[3]:
                locator(lp, cb, [m], v, admin=padm)
            else:
                far_place_locator(lp, m, cb or pad(tb, 1.5), v, padm)
        else:
            parent = SHAPE.get(nm, (None, None))[1]
            sub = (hits[0]["_p"].get("subregion") or "") if hits else ""
            box = (country_box(parent) if parent else None) or SUBREGION_BOX.get(sub)
            if box and box[0] <= tb[0] and box[1] <= tb[1] and box[2] >= tb[2] and box[3] >= tb[3]:
                locator(lp, box, [m], v)
            else:
                locator(lp, tb, [m], v, centred=False, mult=free_mult(v))

    elif kind == "country":
        ft = K.target(nm)
        if ft is None:
            return {"status": "no Natural Earth country"}
        m = K.mainland(ft)
        if nm in ("United States of America", "United States"):
            m["_bbox"] = (-125, 25, -67, 49)
        if nm == "Canada":
            m["_bbox"] = (-130, 43, -55, 66)
        if nm == "Russia":
            m["_bbox"] = (30, 44, 100, 70)
        admin = ft["_p"].get("admin")
        N.MIN_SPAN["country"] = 3 if max(m["_bbox"][2] - m["_bbox"][0], m["_bbox"][3] - m["_bbox"][1]) < 1.0 else 6
        cap = (N.CAPITALS.get(nm) or [None, None, ""])[2]
        N.CITY_POINTS = main_cities(admin, cap)
        N.PROJ = tuple(round(c, 3) for c in centre(m["_bbox"]))
        mp = N.proj_feat(m)
        set_aspect(mp["_bbox"])

        def draw(label, png):
            return N.render({"Name": nm, "Alternate": f["Alternate"]}, "country", [mp], png, target_label=nm if label else None)
        v, why = pair(fp, bp, draw, COMPACT_LADDER)
        N.PROJ, N.CITY_POINTS = None, ()
        sub = ft["_p"].get("subregion") or ""
        box = SUBREGION_BOX.get(sub)
        tb = m["_bbox"]
        if not box or (tb[2] - tb[0]) > 0.5 * (box[2] - box[0]) or (tb[3] - tb[1]) > 0.5 * (box[3] - box[1]):
            box = CONTINENT_BOX.get(ft["_p"].get("continent") or "") or box   # Brazil fills South America's box
        if box and box[0] <= tb[0] and box[1] <= tb[1] and box[2] >= tb[2] and box[3] >= tb[3]:
            locator(lp, box, [m], v)
        else:
            locator(lp, tb, [m], v, centred=False, mult=free_mult(v))   # Greenland: framed on itself

    elif kind in POINT_KINDS:
        # ---- a city, peak or waterfall: a marker; the locator is its whole country, centred
        pf = N.parent_features(f["Parent"])
        if not pf:
            return {"status": "no Parent country"}
        xy, src = P.locate(f, kind, pf)
        if not xy:
            return {"status": "not located"}
        ring = P.inside(pf, xy, 0.5 if kind == "peak" else 0.15)
        N.PROJ = (round(xy[0], 3), round(xy[1], 3))
        xyp = N.project_pt(*xy)
        ringp = N.project(np.asarray(ring, dtype=float)) if ring is not None else None
        pfp = [N.proj_feat(x) for x in pf]
        N.LAST_LABELS = 0
        v = P.render(f, kind, xyp, ringp, bp, pfp, named=True)
        N.LAST_LABELS = 0     # the points renderer does not reset it: the front inherited the back's count
        P.render(f, kind, xyp, ringp, fp, pfp, named=False)
        N.PROJ = None
        admin = pf[0]["_p"].get("admin")
        box = country_box(admin) or (xy[0] - 12, xy[1] - 9, xy[0] + 12, xy[1] + 9)
        locator(lp, box, [], v, point=xy, admin=admin)
        why = ""

    elif kind in N.KIND_LAYERS:
        # ---- a river, lake, sea, range, desert, island, strait ...
        feats, why = N.match(f, kind)
        if not feats:
            return {"status": why or "no Natural Earth feature"}
        tb = bbox_of(feats)
        N.PROJ = tuple(round(c, 3) for c in centre(tb))
        fpj = [N.proj_feat(x) for x in feats]
        set_aspect(bbox_of(fpj))
        if kind in LONG_KINDS:
            N.MARGIN = 1.12   # the Nile and the Andes filled a frame half again their size

        def draw(label, png):
            # names placed by hand, on both sides: a river's tributaries are not answers (the Uruguay R. at the
            # head of the Río de la Plata went unnamed because the river pass skips a river-shaped target)
            N.EXTRA_LABELS = list(BOTH_HAND.get(nm, [])) or (list(N.HAND_LABELS.get(nm, [])) if label else [])
            return N.render(f, kind, fpj, png, target_label=nm if label else None)
        v, why = pair(fp, bp, draw, LADDER if kind in LONG_KINDS or kind in N.WATER else COMPACT_LADDER)
        N.PROJ = None
        pf = N.parent_features(f["Parent"]) if f.get("Parent") else []
        admin, box = None, None
        if len(pf) == 1:
            cb = country_box(pf[0]["_p"].get("admin"))
            if cb and cb[0] <= tb[0] and cb[1] <= tb[1] and cb[2] >= tb[2] and cb[3] >= tb[3]:
                admin, box = pf[0]["_p"].get("admin"), cb      # Tasmania: all of Australia, centred
            elif cb and kind not in N.WATER and kind != "river":
                far_place_locator(lp, feats, cb, v, pf[0]["_p"].get("admin"))   # Madeira, like the Canaries
                reset()
                return {"status": "rendered" if v else (why or "failed"), "front": fp, "back": bp, "locator": lp}
        if box:
            locator(lp, box, feats, v, admin=admin, water=kind in N.WATER, line=kind == "river")
        else:
            locator(lp, tb, feats, v, centred=False, mult=free_mult(v), water=kind in N.WATER, line=kind == "river")
    else:
        return {"status": "kind not handled yet: %s" % kind}
    reset()
    return {"status": "rendered" if v else (why or "failed"), "front": fp, "back": bp, "locator": lp}


def sheet(rows, out):
    from PIL import Image, ImageDraw, ImageFont
    try:
        font, small = ImageFont.truetype("segoeui.ttf", 26), ImageFont.truetype("segoeui.ttf", 20)
    except Exception:
        font = small = None
    tiles = []
    for nm, r in rows:
        t = Image.new("RGB", (1840, 500), "white")
        for i, key in enumerate(("front", "locator", "back")):
            try:
                im = Image.open(r[key]).convert("RGB")
                im.thumbnail((600, 450))
                t.paste(im, (10 + i * 610 + (600 - im.width) // 2, 42))
            except Exception:
                pass
        d = ImageDraw.Draw(t)
        d.text((12, 6), nm, fill="black", font=font)
        for i, lab in enumerate(("FRONT (question)", "LOCATOR (both sides)", "BACK (answer)")):
            d.text((10 + i * 610 + 420, 10), lab, fill="#666", font=small)
        tiles.append(t)
    os.makedirs(os.path.join(out, "review"), exist_ok=True)
    for f_ in os.listdir(os.path.join(out, "review")):
        os.remove(os.path.join(out, "review", f_))
    for s in range(0, len(tiles), 4):
        part = tiles[s:s + 4]
        sh = Image.new("RGB", (1840, 500 * len(part)), "white")
        for i, t in enumerate(part):
            sh.paste(t, (0, i * 500))
        sh.save(os.path.join(out, "review", "samples_%02d.jpg" % (s // 4 + 1)), quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--names", default="")
    ap.add_argument("--kinds", default="")
    ap.add_argument("--out", default=os.path.join(HERE, "renders", "geo_v4"))
    a = ap.parse_args()
    setup()
    os.makedirs(a.out, exist_ok=True)
    names = [x.strip() for x in a.names.split("|") if x.strip()]
    kinds = {x.strip() for x in a.kinds.split(",") if x.strip()}
    ids = C.anki("findNotes", query='note:"Geography"')
    notes = []
    for i in range(0, len(ids), 500):
        notes += C.anki("notesInfo", notes=ids[i:i + 500])
    order = {nm: i for i, nm in enumerate(names)}
    sel = [n for n in notes if (not names or C.plain(n["fields"]["Name"]["value"]).strip() in order)
           and (not kinds or C.plain(n["fields"]["Kind"]["value"]).strip() in kinds)]
    sel.sort(key=lambda n: order.get(C.plain(n["fields"]["Name"]["value"]).strip(), 0))
    man, rows = {}, []
    for n in sel:
        nm = C.plain(n["fields"]["Name"]["value"]).strip()
        try:
            r = do_note(n, a.out)
        except Exception as e:
            import traceback
            traceback.print_exc()
            reset()
            r = {"status": "error: %s" % e}
        man[n["noteId"]] = dict(r, name=nm)
        print("  %-28s %s" % (nm[:28], r["status"]), flush=True)
        if r.get("status") == "rendered":
            rows.append((nm, r))
    json.dump(man, open(os.path.join(a.out, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sheet(rows, a.out)
    print(len(rows), "rendered of", len(man))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
