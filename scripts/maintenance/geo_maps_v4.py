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
import matplotlib.patches

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
REGION_GROUP = {"Canary Islands": ("Spain", "Canary Is."),
                # filed under Australia's "Indian Ocean Territories", not under Australia
                "Cocos (Keeling) Islands": ("Indian Ocean Territories", "Cocos (Keeling) Islands")}
# a former unit that is now part of a merged one: its own pieces, picked out by where they lie
# (Dadra and Nagar Haveli's card drew Daman and Diu too)
RING_PICK = {"Daman and Diu": ("India", "Dadra and Nagar Haveli and Daman and Diu", ((70.99, 20.73), (72.85, 20.42))),
             "Dadra and Nagar Haveli district": ("India", "Dadra and Nagar Haveli and Daman and Diu", ((73.04, 20.18),))}
# name -> (OSM boundary file, the country it lies inside)
SHAPE = {"Transnistria": (os.path.join(HERE, "data", "geo_shapes", "transnistria.geojson"), "Moldova"),
         "Xikang": (os.path.join(HERE, "data", "geo_shapes", "xikang.geojson"), "China"),
         # Antarctica between 45° and 160° E, less Adélie Land (136°–142° E)
         "Australian Antarctic Territory": (os.path.join(HERE, "data", "geo_shapes", "aat.geojson"), "Australia")}
# outlines drawn over their country's modern provinces, with a caption saying the outline is approximate
SHAPE_REGIONS = {"Xikang": "Xikang Province, 1939–1955 (approximate)"}
REGION_CAPTION = {"French Southern and Antarctic Lands": "Adélie Land, the territory's Antarctic claim, lies off this map",
                  "Tokyo": "The Ogasawara Islands, also part of Tokyo, lie off this map to the south"}
ALL_PARTS = {"French Southern and Antarctic Lands"}
FORCE = {"Río de la Plata": ["Uruguay", "Paraná"]}
BOTH_HAND = {"Río de la Plata": [(-59.1, -33.95, "Paraná R."), (-58.0, -31.3, "Uruguay R.")]}
# the Hawaiian islands: the state's name was printed on whichever island had room (on Maui for Lanai, on Oahu for
# Kauai) and read as that island's name; it is left off, and the Big Island is named where it is
HAWAII_ISLANDS = {"Kauai", "Oahu", "Molokai", "Lanai", "Maui", "Niihau", "Kahoolawe"}
for _i in HAWAII_ISLANDS:
    BOTH_HAND[_i] = [(-155.45, 19.6, "Hawaii")]
# hand-drawn polities over modern borders: name -> (outline, modern country whose states are drawn, caption)
HAND_HIST = {"Republic of Texas": (NF.TEXAS, "United States of America", "Claimed extent c. 1840 (approximate); modern states shown"),
             "Phoenicia": (NF.PHOENICIA, None, "Heartland c. 1000 BCE (approximate); modern countries shown")}
ASP = [4 / 3]
# a polity shown at its height inside a union the snapshots do not split: (year, union, clip polygon, the rest's name)
HIST_SPLIT = {"Grand Duchy of Lithuania": ("1400", ["Poland-Lithuania"],
                                           [(20.9, 56.3), (22.8, 54.3), (23.2, 52.3), (24.2, 51.0), (25.0, 50.0), (26.5, 49.0),
                                            (28.5, 47.8), (30.0, 46.2), (45.0, 46.2), (45.0, 60.0), (20.9, 60.0)], "Kingdom of Poland")}
HIST_EXTRA = {"French Indochina": ["Annam", "Cochin China"],    # the 1930 snapshot splits Vietnam off from "French Indo-China"
              "Weimar Republic": ["East Prussia"],   # a separate feature in the 1930 snapshot, but part of Germany
              "Spanish Empire": ["Luisiana"]}        # Spanish Louisiana (1762-1803), drawn as its own state in 1800
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
    N.NO_RING, N.SCATTER_DOTS, N.ALLOW_WIDE = False, False, False
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


# English names for Natural Earth's local or transliterated city names (Belarus's map said "Homyel", Denmark's
# named "Kobenhavn" beside its own capital Copenhagen)
CITY_EN = {"Ganca": "Ganja", "Sumqayt": "Sumgait", "Homyel": "Gomel", "Mahilyow": "Mogilev", "Vitsyebsk": "Vitebsk",
           "Antwerpen": "Antwerp", "Gent": "Ghent", "Lemosos": "Limassol", "Pizen": "Plzeň", "København": "Copenhagen",
           "Århus": "Aarhus", "Ismaïlia": "Ismailia", "Nazret": "Adama", "Ōsaka": "Osaka", "Az Zarqa": "Zarqa", "As Salt": "Salt",
           "Qaraghandy": "Karaganda", "Louangphrabang": "Luang Prabang", "Pakxe": "Pakse", "Ṭarābulus": "Tripoli",
           "Tarabulus": "Tripoli", "Saida": "Sidon","Banghazi": "Benghazi", "Tubruq": "Tobruk", "Kelang": "Klang", "Al Jahra": "Jahra",
           "Irbil": "Erbil", "Al Khalil": "Hebron", "Makkah": "Mecca", "Göteborg": "Gothenburg", "Zürich": "Zurich",
           "Fargona": "Fergana", "Daşoguz": "Dashoguz", "Kismaayo": "Kismayo", "Baydhabo": "Baidoa", "Al Hudaydah": "Hodeidah",
           "Taizz": "Taiz", "Al Ayn": "Al Ain", "Qurghonteppa": "Bokhtar", "Montréal": "Montreal", "Bobo Dioulasso": "Bobo-Dioulasso",
           "Gueckedou": "Guéckédou", "Nema": "Néma", "Odessa": "Odesa", "St.  Petersburg": "Saint Petersburg",
           "St. Petersburg": "Saint Petersburg", "Jalal Abad": "Jalal-Abad"}


# Natural Earth population figures that promote small towns over real cities
CITY_SKIP = {("Guatemala", "San Luis"), ("Guatemala", "El Progreso"), ("Chad", "Bongor")}


def main_cities(admin, capital, n=3, within=None):
    """the country's biggest cities other than its capital; with `within` (a lon/lat feature), only those inside it
    (Scotland's map was given London, Birmingham, and Manchester, as the United Kingdom's biggest)"""
    if not _PLACES:
        for ft in json.load(open(os.path.join(N.NE, "ne_10m_populated_places.geojson"), encoding="utf-8"))["features"]:
            p = ft["properties"]
            nm0 = re.sub(r"\s+", " ", p.get("NAME") or "")
            _PLACES.append((p.get("ADM0NAME"), p.get("POP_MAX") or 0, CITY_EN.get(p.get("NAME"), CITY_EN.get(nm0, nm0)),
                            ft["geometry"]["coordinates"]))
    rows = sorted((r for r in _PLACES if r[0] == admin and r[1] >= 100000 and (admin, r[2]) not in CITY_SKIP),
                  key=lambda r: -r[1])
    if within is not None:
        from matplotlib.path import Path as _MP
        paths = [_MP(r) for r in within["_rings"] if len(r) >= 3]
        rows = [r for r in rows if any(pp.contains_point(r[3]) for pp in paths)]
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
            water=False, line=False, lines=False, polar=None, line_feats=None):
    """the zoomed-out map. The frame is the box given (a country, a region), centred on it; grown about its own
    centre until it is `mult` times the front map and the place sits clear of every edge. polar=(centre, half
    height) frames a view about a pole, which no lon/lat box can describe"""
    cbox = lon_lat_box
    if polar:
        c_ll = polar[0]
    else:
        c_ll = centre(cbox) if centred else (centre(bbox_of(targets_ll)) if targets_ll else point)
        if not centred and targets_ll and bbox_of(targets_ll)[2] - bbox_of(targets_ll)[0] > 180:
            # across the 180th meridian (Siberia's Chukotka): the middle measured in 0-360 longitudes
            allx = np.concatenate([r[:, 0] % 360 for ft in targets_ll for r in ft["_rings"] if len(r)])
            ally = np.concatenate([r[:, 1] for ft in targets_ll for r in ft["_rings"] if len(r)])
            cx0 = (allx.min() + allx.max()) / 2
            c_ll = (cx0 - 360 if cx0 > 180 else cx0, (ally.min() + ally.max()) / 2)
    N.PROJ = (round(c_ll[0], 3), round(c_ll[1], 3))
    try:
        tgt = [N.proj_feat(ft) for ft in targets_ll]
        # the country's internal lines only when the place is one of its provinces (Hunan among China's);
        # for a city, a peak, a lake or Transnistria they were just clutter
        regions = [u for u in R.admin1() if u["_p"].get("admin") == admin] if (admin and lines) else []
        if line_feats:
            regions = [N.proj_feat(x) for x in line_feats]     # the old provinces a pre-2016 French region sits among
        if admin:
            cf = country_ft(admin)      # admin-1 says "Czech Republic", admin-0 "Czechia": grey by the admin-0 name
            admin0 = cf["_p"].get("admin") if cf is not None else admin
        else:
            admin0 = None
        pt = N.project_pt(*point) if point else None
        b = box_proj(cbox) if not polar else (-polar[1] * ASP[0], -polar[1], polar[1] * ASP[0], polar[1])
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
        # the river's countries tinted afresh in this map's projection: the front map's tint, left in place, was
        # drawn here in the front's projection (a pale strip along Poland's eastern border on the Vistula's locator)
        saved_tint = N.TINT_FEATS
        N.TINT_FEATS = ([c for c in N.countries_crossed(tgt) if c["_p"].get("name") not in N.EXTRA_TINY]
                        if (saved_tint and tgt) else ())
        try:
            N.base_map(ax, v, detail=True, labels=False, regions=regions, skip_admin=admin0)
        finally:
            N.OTHER_GREY = False
            N.NEIGHBOUR_ADMIN1_LINES = saved
            N.TINT_FEATS = saved_tint
        if tgt:
            if line:
                N.draw_lines(ax, tgt, v, colors="white", linewidths=6, zorder=5)
                N.draw_lines(ax, tgt, v, colors="#d62d20", linewidths=3.2, zorder=6)
            elif water:
                N.draw_polys(ax, N.merged_water(tgt), v, facecolor="#3d8ee0", edgecolor="#d62d20", linewidth=2.6, zorder=5)
            else:
                N.draw_polys(ax, tgt, v, facecolor=(0.86, 0.24, 0.17, 0.55), edgecolor="#c0392b", linewidth=2.6, zorder=5)
            rs_ = [r for ft in tgt for r in ft["_rings"] if len(r)]
            allp = np.vstack(rs_) if rs_ else None
            px = ax.transData.transform(allp) if rs_ else None
            if rs_ and (px[:, 0].max() - px[:, 0].min()) < 40 and (px[:, 1].max() - px[:, 1].min()) < 40:
                pt = (float(allp[:, 0].mean()), float(allp[:, 1].mean()))   # too small to see at this scale: ringed
            elif rs_ and not line and max(max(np.ptp(q[:, 0]), np.ptp(q[:, 1])) for q in
                                          (ax.transData.transform(r) for r in rs_)) < 14:
                # a scatter of specks (Tuvalu, Kiribati): each too small to see, the whole group too wide for one
                # dot -- one ring drawn round the group
                cx_, cy_ = (px[:, 0].max() + px[:, 0].min()) / 2, (px[:, 1].max() + px[:, 1].min()) / 2
                rad = 0.5 * float(np.hypot(np.ptp(px[:, 0]), np.ptp(px[:, 1]))) + 22
                if rad < 0.18 * N.W_PX:
                    ax.add_patch(matplotlib.patches.Circle(ax.transData.inverted().transform((cx_, cy_)),
                                                           rad * (v[1] - v[0]) / N.W_PX, fill=False,
                                                           edgecolor="#d62d20", linewidth=2.8, zorder=8))
                else:
                    # a scatter across an ocean (Micronesia): a dot on each island, not one ring round half the map
                    for r in rs_:
                        ax.plot([float(r[:, 0].mean())], [float(r[:, 1].mean())], marker="o", markersize=6,
                                color="#d62d20", markeredgecolor="white", markeredgewidth=0.8, zorder=8)
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


# neighbours as they were called in the polity's own time (the snapshots carry some modern names)
HIST_RENAME = {"Rhodesia": {"Northern Rhodesia": "Zambia", "Namibia": "South West Africa", "Mozambique (Portugal)": "Mozambique",
                            "Angola (Portugal)": "Angola", "Nyasaland": "Malawi",
                            "Zaire": "Zaire", "Botswana": "Botswana", "Malawi": "Malawi", "Tanzania, United Republic of": "Tanzania"}}
HIST_RENAME["Dutch East Indies"] = {"Papua New Guinea": "Australian New Guinea"}
HIST_BORROW = {"Nazi Germany": [("1930", "East Prussia")]}
# snapshot polities out of date for the snapshot's own year (the Far Eastern Republic joined the USSR in 1922)
_COLONIAL_AFRICA = {"Botswana": "Bechuanaland", "Ghana": "Gold Coast", "Lesotho": "Basutoland", "Malawi": "Nyasaland",
                    "Namibia": "South West Africa", "Zambia": "Northern Rhodesia", "Zimbabwe": "Southern Rhodesia",
                    "Zaire": "Belgian Congo", "Zaire (Belgium)": "Belgian Congo", "Tanzania, United Republic of": "Tanganyika",
                    "Rwanda": "Ruanda-Urundi", "Rwanda (Belgium)": "Ruanda-Urundi", "Burundi": "Ruanda-Urundi",
                    "Mali": "French Sudan"}
HIST_YEAR_RENAME = {"1930": dict(_COLONIAL_AFRICA, **{"White Russia": "Soviet Union", "Far Eastern SSR": "Soviet Union", "USSR": "Soviet Union"}),
                    "1938": dict(_COLONIAL_AFRICA), "1945": dict(_COLONIAL_AFRICA)}
# the same borders held later, as the renamed neighbours say
HIST_CAPTION = {"Spanish Empire": "Borders c. 1800 (approximate); the Spanish Philippines lie off this map",
                "Rhodesia": "Borders c. 1970 (approximate)", "Republic of China": "Territory c. 1946, on modern borders (approximate)"}
MODERN_SAME = {"Ceylon": "Sri Lanka", "Burma": "Myanmar", "Siam": "Thailand", "Persia": "Iran", "Formosa": "Taiwan",
               "Zaire": "DR Congo", "Rhodesia": "Zimbabwe",
               # the mainland republic after 1945, with Manchuria and Taiwan back: today's China and Taiwan
               "Republic of China": ["China", "Taiwan"]}
HIST_ADD_A1 = {"Republic of Genoa": [("France", "Corse")],
               # Spanish Florida (1783-1821): the 1800 snapshot gives it to the United States
               "Spanish Empire": [("United States of America", "Florida")]}


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
            clip = None
            if nm in HIST_SPLIT:
                year, want, clip, rest_name = HIST_SPLIT[nm]
            want = list(want) + HIST_EXTRA.get(nm, [])
            feats = H.snapshot(year)
            if clip:
                # one union polity split in two: the named part highlighted, the rest labelled as its own state
                from shapely.geometry import Polygon as _SP
                cp = _SP(clip).buffer(0)
                split = []
                for x in feats:
                    if x["_raw"] not in want:
                        split.append(x)
                        continue
                    for part, raw, name in ((cp, x["_raw"], None), (None, x["_raw"] + "#rest", rest_name)):
                        rr = []
                        for r in x["_rings"]:
                            if len(r) < 4:
                                continue
                            g = _SP(r).buffer(0)
                            g = g.intersection(cp) if part is not None else g.difference(cp)
                            for q in (list(g.geoms) if hasattr(g, "geoms") else [g]):
                                if q.geom_type == "Polygon" and q.area > 0.01:
                                    rr.append(np.asarray(q.exterior.coords, dtype=float))
                        if rr:
                            aa = np.vstack(rr)
                            pp = dict(x["_p"])
                            if name:
                                pp["name"] = pp["name_en"] = name
                            split.append(dict(x, _rings=rr, _raw=raw, _p=pp,
                                              _bbox=(aa[:, 0].min(), aa[:, 1].min(), aa[:, 0].max(), aa[:, 1].max())))
                feats = split
            if nm == "Spanish Empire":
                # the snapshot's accented "Río de la Plata" does not always match the spec's spelling
                want += [x["_raw"] for x in feats if x["_raw"].startswith("Viceroyalty of the R")]
            tf = [x for x in feats if x["_raw"] in want]
            if not tf:
                return {"status": "no snapshot feature"}
            others = []
            for x in feats:
                g = dict(x)
                g["_p"] = dict(x["_p"])
                if x["_raw"] in want:
                    g["_p"]["_nolabel"] = True
                rn = HIST_RENAME.get(nm, {}).get(x["_raw"]) or HIST_YEAR_RENAME.get(year, {}).get(x["_raw"])
                if rn:
                    g["_p"]["name"] = g["_p"]["name_en"] = rn
                others.append(g)
            if nm == "Spanish Empire":
                # the 1800 snapshot draws sub-Saharan Africa as scattered, disconnected blobs that say nothing on
                # this card, a "Guanches" outline on the long-Spanish Canaries, and a Shuar ring inside New Granada
                def _keep(g):
                    b = g["_bbox"]
                    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
                    return g["_p"].get("_nolabel") or not ((-20 < cx < 60 and cy < 30) or g.get("_raw") in ("Guanches", "Shuar"))
                others = [g for g in others if _keep(g)]
            rs = [r for x in tf for r in x["_rings"]]
            for by_, braw in HIST_BORROW.get(nm, []):
                # a part the snapshot draws wrong, taken from another year's (1938 cut East Prussia to a sliver)
                rs += [r for x in H.snapshot(by_) if x["_raw"] == braw for r in x["_rings"]]
            if nm in HIST_BORROW:
                rs = N.dissolve(rs)      # one outline, no seam where the borrowed part overlaps
            for bx in H.EXCLUDE.get(nm, []):
                rs = [r for r in rs if not (r[:, 0].min() >= bx[0] and r[:, 1].min() >= bx[1] and r[:, 0].max() <= bx[2] and r[:, 1].max() <= bx[3])]
            if nm == "Spanish Empire":
                # the Americas and Iberia only: the Philippines and Guam put the shape across the 180th meridian and
                # no frame could be drawn (the caption says they lie off the map)
                rs = [r for r in rs if r[:, 0].min() > -130 and r[:, 0].max() < 15
                      and not (-58 < r[:, 0].mean() < -45 and -3 < r[:, 1].mean() < 7)]   # a stray New Granada ring at the Amazon mouth
                N.ALLOW_WIDE = True     # California to Spain is wider than the 180-unit guard (reset below)
            if nm == "Assyria":
                rs = assyria_rings()
                others = [{"geometry": x["geometry"], "_rings": x["_rings"], "_p": {"name": ""}, "_bbox": x["_bbox"]}
                          for x in N._layer_ll("ne_10m_land")]
            elif nm in H.MANUAL:
                rs = [np.array(H.MANUAL[nm], dtype=float)]
                others = [{"geometry": x["geometry"], "_rings": x["_rings"], "_p": {"name": ""}, "_bbox": x["_bbox"]}
                          for x in N.layer("ne_10m_land")]
            if nm == "Kingdom of Hawaii":
                # the kingdom was the eight main islands: today's state, cropped as on the state's own card (the
                # 1878 snapshot left Kauai and Molokai unshaded)
                hh, _, _ = R.find("Hawaii", "United States", "US state")
                cb_ = CROP["Hawaii"]
                rs = [r for h_ in hh for r in h_["_rings"] if cb_[0] <= r[:, 0].mean() <= cb_[2] and cb_[1] <= r[:, 1].mean() <= cb_[3]]
                ma = np.vstack(rs)
                for g in others:
                    if g["_p"].get("_nolabel"):
                        g["_rings"], g["_bbox"] = rs, (ma[:, 0].min(), ma[:, 1].min(), ma[:, 0].max(), ma[:, 1].max())
                N.AVOID_EXTRA = ("hawaii", "kauai", "lanai", "oahu", "maui", "molokai")
            for adm_, unit_ in HIST_ADD_A1.get(nm, []):
                # a possession the snapshot does not draw (Genoa's Corsica, held until 1768)
                rs += [r for u in R._admin1_ll() if u["_p"].get("admin") == adm_ and u["_p"].get("name") == unit_ for r in u["_rings"]]
            if nm in MODERN_SAME:
                # an old name for a country whose borders are today's: the modern outline, not the snapshot's
                # coarse one (Ceylon's showed slivers of coast outside its own edge)
                names_ = MODERN_SAME[nm] if isinstance(MODERN_SAME[nm], list) else [MODERN_SAME[nm]]
                fts_ = [K.target(x) for x in names_]
                mft = fts_[0] if all(x is not None for x in fts_) else None
                if mft is not None:
                    rs = [r for x in fts_ for r in K.mainland(x)["_rings"]]
                    ma = np.vstack(rs)
                    for g in others:
                        if g["_p"].get("_nolabel"):
                            g["_rings"], g["_bbox"] = rs, (ma[:, 0].min(), ma[:, 1].min(), ma[:, 0].max(), ma[:, 1].max())
            arr = np.vstack(rs)
            m = {"geometry": tf[0]["geometry"], "_rings": rs, "_p": tf[0]["_p"],
                 "_bbox": (arr[:, 0].min(), arr[:, 1].min(), arr[:, 0].max(), arr[:, 1].max())}
            yl = ("%d BCE" % int(year[2:])) if year.startswith("bc") else ("c. %s" % year)
            N.MAP_CAPTION = HIST_CAPTION.get(nm) or "Borders %s (approximate)" % yl
            if nm == "Assyria":
                N.MAP_CAPTION = "The Neo-Assyrian Empire at its height, c. 671 BCE (approximate)"
                N.CLIP_SEA = True
                N.EXTRA_LABELS = [(x, y, t) for t, x, y in ASSYRIA_LABELS]
            elif nm in H.MANUAL_LABELS:
                N.CLIP_SEA = True
                N.EXTRA_LABELS = [(x, y, t) for t, x, y in H.MANUAL_LABELS[nm][2]]
        hbox = H.SPEC[nm][2] if nm in H.SPEC and nm not in HAND_HIST else None
        # a polity reaching past the 180th meridian (the Russian Empire's Chukotka) has a lon/lat box spanning the
        # globe, and its map was centred on Greenwich: its own box, where the snapshot spec gives one
        N.PROJ = tuple(round(c, 3) for c in centre(hbox if hbox else m["_bbox"]))
        mp = N.proj_feat(m)
        if hbox:
            mp = dict(mp, _bbox=box_proj(hbox))
        if others is not None:
            N.COUNTRIES_OVERRIDE, N.NO_DETAIL = [N.proj_feat(x) for x in others], True
        regions = [u for u in R.admin1() if u["_p"].get("admin") == skip_admin] if skip_admin else []
        set_aspect(mp["_bbox"])
        N.MIN_SPAN["x"] = 4

        def draw(label, png):
            return N.render({"Name": nm, "Alternate": f["Alternate"]}, "x", [mp], png,
                            target_label=nm if label else None, regions=regions, skip_admin=skip_admin)
        v, why = pair(fp, bp, draw, FIXED_LADDER.get(nm, COMPACT_LADDER))
    finally:
        N.COUNTRIES_OVERRIDE, N.NO_DETAIL, N.MAP_CAPTION, N.CLIP_SEA, N.EXTRA_LABELS = saved
        N.OTHER_GREY = False
        N.PROJ = None
        N.ALLOW_WIDE = False
    N.AVOID_EXTRA = ()
    hbox_ = H.SPEC[nm][2] if nm in H.SPEC and nm not in HAND_HIST else None
    if nm in LOCATOR_BOX:
        locator(lp, LOCATOR_BOX[nm], [m], v)
    elif hbox_:
        locator(lp, hbox_, [m], v, mult=free_mult(v))
    else:
        locator(lp, m["_bbox"], [m], v, centred=False, mult=free_mult(v))
    return {"status": "rendered" if v else (why or "failed"), "front": fp, "back": bp, "locator": lp}


_SPECIAL = {}
# a continent about a pole: (projection centre, front half-height, locator half-height) -- Antarctica was a sliver
# along the bottom of an Atlantic-centred globe
POLAR = {"Antarctica": ((0.0, -90.0), 30.0, 62.0), "Southern Ocean": ((0.0, -90.0), 38.0, 62.0)}
OCEAN_CENTRE = {"Pacific Ocean": (-165.0, 5.0), "Atlantic Ocean": (-30.0, 10.0), "Indian Ocean": (78.0, -18.0),
                "Southern Ocean": (0.0, -75.0), "Arctic Ocean": (0.0, 90.0)}


def special(nm):
    """places the general matcher cannot build, assembled the way ne_more.py and ne_more2.py do: France's old
    regions, the UK's nations, sets of countries (the Maghreb, the EU), continents, oceans, historical regions on
    modern borders, and hand or OpenStreetMap outlines. Returns a spec in lon/lat, or None."""
    import ne_more as M
    import ne_more2 as M2
    if nm in _SPECIAL:
        return _SPECIAL[nm]
    if nm in NO_SPECIAL:
        return None
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
        if nm in SET_CLIP:
            # the member states' European territory only: French Guiana and Reunion pulled the EU map out to a globe
            cb = SET_CLIP[nm]
            rs = [r for r in rs if cb[0] <= r[:, 0].mean() <= cb[2] and cb[1] <= r[:, 1].mean() <= cb[3]]
        for c, a in extra:
            rs += [r for f in a1 if f["_p"].get("admin") == c and f["_p"].get("name") == a for r in f["_rings"]]
        if nm == "Polynesia":
            # the Polynesian Triangle's corners, as the card describes it: Hawaii, New Zealand, Easter Island
            hh, _, _ = R.find("Hawaii", "United States", "US state")
            cb_ = CROP["Hawaii"]
            rs += [r for h_ in hh for r in h_["_rings"] if cb_[0] <= r[:, 0].mean() <= cb_[2] and cb_[1] <= r[:, 1].mean() <= cb_[3]]
            rs += [r for f_ in M.country("New Zealand") for r in f_["_rings"] if r[:, 0].mean() > 160 and r[:, 1].mean() < -33]
            t = np.linspace(0, 2 * np.pi, 24)
            rs.append(np.column_stack([-109.35 + 0.12 * np.cos(t), -27.12 + 0.1 * np.sin(t)]))
            box = (160.0, -50.0, 255.0, 25.0)       # across the 180th meridian, in 180+ longitudes
        if rs:
            sp = dict(feat=M.feat(rs, nm), box=box, multi=True, span=5)
    elif nm in M.CONT:
        cont, box = M.CONT[nm]
        rs = [r for f in N._layer_ll("ne_50m_admin_0_countries") if f["_p"].get("continent") == cont for r in f["_rings"]
              if box[0] <= r[:, 0].mean() <= box[2] and box[1] <= r[:, 1].mean() <= box[3]]
        if nm == "Europe":
            # European Russia, to the Urals (about 60 degrees E) and north of the Caucasus: its one big ring was left
            # out because its middle lies in Siberia
            from shapely.geometry import Polygon as _SP, box as _bx
            ru = [f for f in N._layer_ll("ne_50m_admin_0_countries") if f["_p"].get("admin") == "Russia"]
            cut = _bx(19.0, 41.5, 60.0, 82.0)
            for f in ru:
                for r in f["_rings"]:
                    if len(r) >= 4 and r[:, 0].mean() > 40:
                        g = _SP(r).buffer(0).intersection(cut)
                        for q in (list(g.geoms) if hasattr(g, "geoms") else [g]):
                            if q.geom_type == "Polygon" and q.area > 0.5:
                                rs.append(np.asarray(q.exterior.coords, dtype=float))
        if rs:
            sp = dict(feat=M.feat(rs, nm), box=box, span=20, world=True)
    elif nm == "Southern Ocean":
        # the water south of 60 deg S (the IHO limit), round the pole with the land drawn over it: Natural Earth's
        # polygon, cut at the 180th meridian, came out as scraps round Antarctica
        ring = np.array([(lon, -60.0) for lon in np.arange(-180.0, 180.0, 2.0)] + [(-180.0, -60.0)], dtype=float)
        sp = dict(feat={"geometry": {"type": "Polygon"}, "_rings": [ring],
                        "_p": {"name": nm, "label_x": 25.0, "label_y": -63.5},   # open water south of Africa
                        "_bbox": (-180.0, -90.0, 180.0, -60.0)},
                  kind="sea", over=True, span=60, world=True, noring=True)
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


REGION_HULL = {"Micronesia": 1.6, "Polynesia": 1.6}   # an ocean-wide scatter shown as a shaded area round its islands


def close_seams(mp, eps=0.08):
    """an ocean's polygons merged after projection: cut at the 180th meridian in lon/lat, the Arctic and the
    Pacific each showed a seam line through the highlight (the two sides of the cut project onto one line)"""
    from shapely.geometry import Polygon as _SP
    from shapely.ops import unary_union as _UU
    try:
        g = _UU([_SP(r).buffer(0) for r in mp["_rings"] if len(r) >= 4]).buffer(eps).buffer(-eps)
        rs = [np.asarray(q.exterior.coords, dtype=float) for q in (list(g.geoms) if hasattr(g, "geoms") else [g])
              if q.geom_type == "Polygon" and q.area > 0.01]
        return dict(mp, _rings=rs) if rs else mp
    except Exception as e:
        print("   seam closing failed:", e)
        return mp


def island_hull(m, d):
    from shapely.geometry import Polygon as _SP
    from shapely.ops import unary_union as _UU
    g = _UU([_SP(r).buffer(0).buffer(d) for r in m["_rings"] if len(r) >= 4]).buffer(0.6).buffer(-0.6).simplify(0.1)
    rs = [np.asarray(q.exterior.coords, dtype=float) for q in (list(g.geoms) if hasattr(g, "geoms") else [g])
          if q.geom_type == "Polygon"]
    a = np.vstack(rs)
    return dict(m, _rings=rs, geometry={"type": "MultiPolygon"}, _bbox=(a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()))


def do_special(f, nm, sp, fp, bp, lp):
    m = sp["feat"]
    if nm in REGION_HULL:
        m = island_hull(m, REGION_HULL[nm])
    kind = sp.get("kind", "x")
    saved = (N.MAP_CAPTION, N.LAND_OVER, N.CLIP_SEA, N.NO_RING, N.OVER_TARGET_COUNTRIES)
    try:
        cb = sp.get("box") or m["_bbox"]
        N.PROJ = (POLAR[nm][0] if nm in POLAR else None) or OCEAN_CENTRE.get(nm) or tuple(round(c, 3) for c in centre(cb))
        mp = N.proj_feat(m)
        if nm in POLAR:
            h = POLAR[nm][1]
            mp = dict(mp, _bbox=(-h * 4 / 3, -h, h * 4 / 3, h))
        elif nm in OCEAN_CENTRE:
            # the Arctic is small: a hemisphere left it a speck (34, not 26, now that its marginal seas are in it)
            h = 34.0 if nm == "Arctic Ocean" else 52.0
            mp = dict(close_seams(mp), _bbox=(-h * 4 / 3, -h, h * 4 / 3, h))
        elif sp.get("box"):
            mp = dict(mp, _bbox=box_proj(sp["box"]))
        regions = [N.proj_feat(x) for x in sp.get("sisters", [])]
        admin = sp.get("admin")
        set_aspect(mp["_bbox"])
        N.MIN_SPAN[kind] = sp.get("span", 5)
        N.MAP_CAPTION, N.LAND_OVER, N.CLIP_SEA, N.NO_RING = sp.get("cap", ""), sp.get("over", False), sp.get("clip", False), sp.get("noring", False)
        N.NO_RING = N.NO_RING or len(m["_rings"]) >= 8     # scattered islands: no ring round each (Micronesia)
        N.SCATTER_DOTS = len(m["_rings"]) >= 8
        N.OVER_TARGET_COUNTRIES = bool(sp.get("multi"))
        N.ALLOW_WIDE = bool(sp.get("world"))
        if kind in LONG_KINDS:
            N.MARGIN = 1.12

        # a region drawn among its country's other regions (Franche-Comté among France's old provinces): that
        # country cream, the rest grey, as on the locator
        grey_admin = None
        if regions and admin and not sp.get("multi"):
            cf_ = country_ft(admin)
            grey_admin = cf_["_p"].get("admin") if cf_ is not None else admin

        def draw(label, png):
            saved_g = N.GREY_EXCEPT
            if grey_admin:
                N.GREY_EXCEPT = grey_admin
            try:
                return N.render({"Name": nm, "Alternate": f["Alternate"]}, kind, [mp], png,
                                target_label=nm if label else None, regions=regions, skip_admin=admin if regions else None)
            finally:
                N.GREY_EXCEPT = saved_g
        ladder = FIXED_LADDER.get(nm) or ((1.0,) if nm in OCEAN_CENTRE else (0.75, 1.0, 1.4) if sp.get("world") else COMPACT_LADDER)
        v, why = pair(fp, bp, draw, ladder)
    finally:
        N.MAP_CAPTION, N.LAND_OVER, N.CLIP_SEA, N.NO_RING, N.OVER_TARGET_COUNTRIES = saved
        N.ALLOW_WIDE = False
        N.SCATTER_DOTS = False
        N.PROJ = None
    tb = m["_bbox"]
    owner = sp.get("owner") or admin
    cbox = country_box(owner) if owner else None
    water = kind in N.WATER or kind == "sea"
    if nm in LOCATOR_BOX:
        locator(lp, LOCATOR_BOX[nm], [m], v, water=water)
    elif cbox and cbox[0] <= tb[0] and cbox[1] <= tb[1] and cbox[2] >= tb[2] and cbox[3] >= tb[3]:
        # its sister regions outlined on the locator too (Carter: Franche-Comté's locator "doesnt show the outlines
        # of france's provinces at all")
        locator(lp, cbox, [m], v, admin=owner, water=water, line_feats=sp.get("sisters") or None)
    elif cbox:
        far_place_locator(lp, m, cbox, v, owner, water=water)
    elif nm in POLAR:
        locator(lp, None, [m], None, polar=(POLAR[nm][0], POLAR[nm][2]))
    elif nm in OCEAN_CENTRE:
        c = OCEAN_CENTRE[nm]
        locator(lp, (c[0] - 60, c[1] - 45, c[0] + 60, c[1] + 45), [m], None, water=True)   # the ocean on the globe
    else:
        # a set with its own box is centred on the box: Melanesia's bounding box, Fiji astride the 180th meridian,
        # ran round the globe and centred the view on Africa, where every island fell on the far side
        locator(lp, sp.get("box") or tb, [m], v, centred=bool(sp.get("box")), mult=free_mult(v), water=water)
    return {"status": "rendered" if v else (why or "failed"), "front": fp, "back": bp, "locator": lp}


_GL = []


def minus_great_lakes(m):
    """Natural Earth's states and provinces run out to the international line in the Great Lakes: Illinois and
    Indiana were drawn with a slice of Lake Michigan shaded as land"""
    from shapely.geometry import Polygon as _SP
    from shapely.ops import unary_union as _UU
    if not _GL:
        big = {"lake superior", "lake michigan", "lake huron", "lake erie", "lake ontario", "georgian bay", "lake st clair"}
        _GL.append(_UU([_SP(r).buffer(0) for f in N._layer_ll("ne_10m_lakes") if N.norm(f["_p"].get("name")) in big
                        for r in f["_rings"] if len(r) >= 4]))
    lakes = _GL[0]
    b = m["_bbox"]
    if lakes.is_empty or not lakes.intersects(_SP([(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])])):
        return m
    rs = []
    for r in m["_rings"]:
        if len(r) < 4:
            continue
        g = _SP(r).buffer(0).difference(lakes)
        for q in (list(g.geoms) if hasattr(g, "geoms") else [g]):
            if q.geom_type == "Polygon" and q.area > 1e-4:
                rs.append(np.asarray(q.exterior.coords, dtype=float))
    if not rs:
        return m
    a = np.vstack(rs)
    return dict(m, _rings=rs, _bbox=(a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()))


def state_ring(ring, xy, pf):
    """a place in a country too big to frame whole is framed on its state or province, and the locator shows the
    country: Mount Rainier's "close-up" was half of North America, the same frame as its locator"""
    if ring is None:
        return ring
    k = math.cos(math.radians(max(-70.0, min(70.0, xy[1]))))
    if np.ptp(ring[:, 1]) * 1.2 <= 30 and np.ptp(ring[:, 0]) * k * 1.2 <= 40:
        return ring
    from matplotlib.path import Path as _MP
    # the state is looked for in the country whose outline framed the place (Niagara Falls: New York, not Ontario)
    owner = [ft["_p"].get("admin") for ft in pf if any(r is ring for r in ft["_rings"])]
    admins = set(owner) or {ft["_p"].get("admin") for ft in pf}
    best = None
    for u in R._admin1_ll():
        if u["_p"].get("admin") not in admins:
            continue
        b = u["_bbox"]
        if not (b[0] - 0.3 <= xy[0] <= b[2] + 0.3 and b[1] - 0.3 <= xy[1] <= b[3] + 0.3):
            continue
        for r in u["_rings"]:
            if len(r) < 3:
                continue
            inside = _MP(r).contains_point(xy)
            if inside or np.min(((r - np.array(xy)) ** 2).sum(axis=1)) < 0.3 ** 2:
                a_ = np.ptp(r[:, 0]) * np.ptp(r[:, 1])
                # the unit holding the point, and on a border the smaller one (Niagara Falls: New York, not Ontario)
                key = (0 if inside else 1, a_)
                if best is None or key < best[0]:
                    best = (key, r)
    return best[1] if best else ring


# isolated island units: the main islands only, at one fixed zoom
CROP = {"Hawaii": (-160.6, 18.7, -154.6, 22.4),
        # the metropolis and the Izu Islands: with the Ogasawara Islands 1,000 km south the city was a speck and
        # its name floated in open ocean
        "Tokyo": (138.0, 32.0, 140.6, 36.2)}
SET_CLIP = {"European Union": (-32.0, 27.0, 35.0, 72.0)}
FIXED_LADDER = {"Great Salt Lake": (2.0,),   # the ladder ran out to the whole continent looking for three names
                "Nunavut": (1.05,),           # at 1.4 the frame reached Sweden
                "Spanish Empire": (0.85,),"Canada": (0.85,),"United States of America": (0.9,), "Russia": (0.9,), "Russian Empire": (1.0,), "Soviet Union": (1.0,), "Siberia": (1.0,), "European Union": (0.9,), "Hawaii": (1.25,), "Kingdom of Hawaii": (1.25,), "Easter Island": (0.35,), "Madeira": (0.6,), "Antarctica": (1.0,)}
# island countries that straddle the 180th meridian, and the locator box for each (longitudes past 180 as 180+)
ACROSS_180 = {"Kiribati": (140.0, -35.0, 225.0, 25.0), "Fiji": (145.0, -48.0, 200.0, 0.0)}
# locators framed by hand: Australia's Indian Ocean islands with Australia and Java in view, not open ocean
LOCATOR_BOX = {"Cocos (Keeling) Islands": (90.0, -36.0, 135.0, 2.0), "Christmas Island": (90.0, -36.0, 135.0, 2.0),
               "French Southern and Antarctic Lands": (15.0, -60.0, 95.0, 0.0),   # with Africa and Madagascar
               "Hawaii": (-165.0, 8.0, -110.0, 50.0), "Kingdom of Hawaii": (-165.0, 8.0, -110.0, 50.0),
               # Pacific islands with Australia and New Zealand in view: the open-ocean locator showed only specks
               "American Samoa": (150.0, -48.0, 215.0, 8.0), "Wallis and Futuna": (150.0, -48.0, 215.0, 8.0),
               "French Polynesia": (165.0, -50.0, 240.0, 8.0),
               "Easter Island": (-112.0, -45.0, -66.0, -10.0),
               # South Pacific states: Australia and New Zealand in view (the Cook Islands' locator showed open sea)
               "Cook Islands": (150.0, -50.0, 220.0, 5.0), "Niue": (150.0, -50.0, 215.0, 5.0),
               "Tonga": (145.0, -50.0, 210.0, 5.0), "Samoa": (145.0, -50.0, 210.0, 5.0)}


# Natural Earth calls it "Red", like the Red River of the North
MATCH_AS = {"Red River of the South": ("Red", (-104.0, -91.0, 30.0, 36.0))}


def islands_in(ft):
    """an island group's own islands: Natural Earth gives the group as a hull over the sea, and the Azores were
    drawn as a shaded pentagon of ocean"""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    hull = unary_union([Polygon(r).buffer(0) for r in ft["_rings"] if len(r) >= 4]).buffer(0.05)
    b = hull.bounds
    rs = []
    for lname in ("ne_10m_land", "ne_10m_minor_islands"):
        for g in N._layer_ll(lname):
            gb = g["_bbox"]
            if gb[2] < b[0] or gb[0] > b[2] or gb[3] < b[1] or gb[1] > b[3]:
                continue
            for r in g["_rings"]:
                if len(r) >= 4 and hull.contains(Polygon(r).buffer(0).representative_point()):
                    rs.append(r)
    if not rs:
        return ft
    a = np.vstack(rs)
    return dict(ft, _rings=rs, geometry={"type": "MultiPolygon"}, _bbox=(a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()))


# small Hawaiian islands Natural Earth names nowhere: the land polygon under a point on each
ISLAND_AT = {"Molokai": (-157.0, 21.13), "Niihau": (-160.15, 21.9), "Kahoolawe": (-156.61, 20.55)}


def island_at(nm):
    from shapely.geometry import Point, Polygon
    pt = Point(*ISLAND_AT[nm])
    for lname in ("ne_10m_minor_islands", "ne_10m_land"):
        for ft in N._layer_ll(lname):
            if not (ft["_bbox"][0] <= pt.x <= ft["_bbox"][2] and ft["_bbox"][1] <= pt.y <= ft["_bbox"][3]):
                continue
            for r in ft["_rings"]:
                if len(r) >= 4 and Polygon(r).buffer(0).contains(pt):
                    return [{"geometry": {"type": "Polygon"}, "_rings": [r], "_p": {"name": nm, "featurecla": "Island"},
                             "_bbox": (r[:, 0].min(), r[:, 1].min(), r[:, 0].max(), r[:, 1].max())}]
    return []


# hand specials now worse than the plain path: the Northern Marianas special drew the whole Mariana chain's sea
# hull (Guam included); Natural Earth's own admin-0 outline has the islands themselves
NO_SPECIAL = {"Northern Mariana Islands"}
# the Parent field names a region, not countries, where the renderer needs countries
PARENT_FIX = {"Rub' al-Khali": "Saudi Arabia, Oman, Yemen, United Arab Emirates",
              "Limpopo": "South Africa, Botswana, Zimbabwe, Mozambique", "Okavango": "Angola, Namibia, Botswana",
              "Gulf of Aqaba": "Egypt, Israel, Jordan, Saudi Arabia", "Bight of Biafra": "Nigeria, Cameroon, Equatorial Guinea, Gabon",
              "Rhine": "Switzerland, Liechtenstein, Austria, Germany, France, Netherlands", "Tagus": "Spain, Portugal",
              "Oder": "Czech Republic, Poland, Germany", "Red River of the South": "United States",
              "Caribbean Sea": "Mexico, Cuba, Jamaica, Haiti, Dominican Republic, Puerto Rico, Colombia, Venezuela, Panama, Costa Rica, Nicaragua, Honduras, Guatemala, Belize",
              "Mediterranean Sea": "Spain, France, Italy, Greece, Turkey, Cyprus, Syria, Lebanon, Israel, Egypt, Libya, Tunisia, Algeria, Morocco"}


def do_note(n, out):
    f = {k: C.plain(v["value"]).strip() for k, v in n["fields"].items()}
    f["Alternate"] = n["fields"]["Alternate"]["value"]
    nm, kind = f["Name"], f["Kind"]
    f["Parent"] = PARENT_FIX.get(nm, f["Parent"])
    kind = {"canal": "river"}.get(kind, kind)      # the Suez Canal is drawn from its centreline, like a river
    s = slug(nm + " " + kind)
    fp, bp, lp = (os.path.join(out, "%s-%s.png" % (pre, s)) for pre in ("g4front", "g4lab", "g4loc"))
    N.PLACED_NAMES.clear()
    reset()
    # a "region" card describes today's extent (Bengal: "divided between Bangladesh and West Bengal"), so where a
    # modern outline exists it is used, not a snapshot of a medieval kingdom
    # a modern province is never a snapshot: Sindh, filed in the historical table for an older card, was drawn as
    # the 900 CE state with "Borders c. 900"
    if (nm in H.SPEC or nm in HAND_HIST) and kind != "subdivision" and not (kind == "region" and special(nm)):
        return do_hist(f, nm, fp, bp, lp)
    sp = special(nm)
    if sp:
        return do_special(f, nm, sp, fp, bp, lp)

    if nm in SHAPE or kind in REGION_KINDS or nm in REGION_GROUP or nm in RING_PICK:
        # ---- a province, state, dependency, territory
        if nm in SHAPE:
            m, hits, is_a1 = shape_feat(nm), [], False
        elif nm in RING_PICK:
            adm, unit, pts = RING_PICK[nm]
            u = next(x for x in R._admin1_ll() if x["_p"].get("name") == unit and x["_p"].get("admin") == adm)
            rs = [min(u["_rings"], key=lambda r: (r[:, 0].mean() - px) ** 2 + (r[:, 1].mean() - py) ** 2) for px, py in pts]
            a_ = np.vstack(rs)
            m = {"geometry": {"type": "MultiPolygon"}, "_rings": rs, "_p": dict(u["_p"], name=nm, name_en=nm),
                 "_bbox": (a_[:, 0].min(), a_[:, 1].min(), a_[:, 0].max(), a_[:, 1].max())}
            hits, is_a1 = [m], True
        elif nm in REGION_GROUP:
            m = K.mainland(next(u for u in R.admin1() if u["_p"].get("name") == REGION_GROUP[nm][1]
                                and u["_p"].get("admin") == REGION_GROUP[nm][0]))
            hits, is_a1 = [m], True
        else:
            hits, is_a1, admins = R.find(nm, f["Parent"], kind)
            if not hits:
                return {"status": "no Natural Earth match"}
            # a territory that is only scattered parts keeps them all (the TAAF map showed Kerguelen alone)
            m = R.merge(hits) if nm in ALL_PARTS else K.mainland(R.merge(hits))
        if nm in CROP:
            # an island state far from any neighbour: the frame kept widening in search of names to print, and
            # Hawaii became eight specks in open ocean
            cb_ = CROP[nm]
            rs_ = [r for r in m["_rings"] if cb_[0] <= r[:, 0].mean() <= cb_[2] and cb_[1] <= r[:, 1].mean() <= cb_[3]]
            a_ = np.vstack(rs_)
            m = dict(m, _rings=rs_, _bbox=(a_[:, 0].min(), a_[:, 1].min(), a_[:, 0].max(), a_[:, 1].max()))
        skip_admin = hits[0]["_p"].get("admin") if is_a1 else (SHAPE[nm][1] if nm in SHAPE_REGIONS else None)
        if skip_admin in ("United States of America", "Canada"):
            m = minus_great_lakes(m)
        hit_ids = {id(h) for h in hits}
        span = max(m["_bbox"][2] - m["_bbox"][0], m["_bbox"][3] - m["_bbox"][1])
        N.PROJ = tuple(round(c, 3) for c in centre(m["_bbox"]))
        mp = N.proj_feat(m)
        hit_p = {id(N.proj_feat(h)) for h in hits}
        # the place's own unit left out of its sisters by name, not object: the projection cache is cleared when a
        # new note's projection comes in, so on every note after a batch's first the projected copy differed and
        # the place itself was drawn and treated as one of its own neighbours (Beijing went unnamed in Hebei's hole)
        hit_keys = {(h["_p"].get("admin"), h["_p"].get("name")) for h in hits}
        regions = [u for u in R.admin1() if skip_admin and u["_p"].get("admin") == skip_admin and id(u) not in hit_p
                   and (u["_p"].get("admin"), u["_p"].get("name")) not in hit_keys]
        if kind == "partially recognised state":
            regions = []      # Abkhazia's map named every Georgian region; the country around it is what matters
        set_aspect(mp["_bbox"])
        N.MIN_SPAN["x"] = 3 if span < 1.5 else 5

        # a small island territory's neighbours are small islands too: named at their label points (Saint
        # Barthélemy's map named Guadeloupe and the Virgin Islands, not Saint Martin or Saint Kitts beside it)
        small_isl = (not is_a1 and (m["_bbox"][2] - m["_bbox"][0]) * (m["_bbox"][3] - m["_bbox"][1]) < 6.0)
        # a province's own country cream and every other grey on the close-up too, as on its locator (Carter:
        # Franche-Comté's first map "doesnt put the non-france countries in grey")
        grey_admin = None
        if is_a1 and skip_admin and kind != "partially recognised state" and not N.GREY_EXCEPT:
            cf_ = country_ft(skip_admin)
            grey_admin = cf_["_p"].get("admin") if cf_ is not None else skip_admin

        def draw(label, png):
            N.EXTRA_LABELS = list(N.HAND_LABELS.get(nm, [])) if label else []
            N.MAP_CAPTION = (SHAPE_REGIONS.get(nm) or REGION_CAPTION.get(nm, "")) if label else ""
            saved_t = N.TINY_LABELS
            N.TINY_LABELS = N.TINY_LABELS or small_isl
            if grey_admin:
                N.GREY_EXCEPT = grey_admin
            try:
                return N.render({"Name": nm, "Alternate": f["Alternate"]}, "x", [mp], png,
                                target_label=nm if label else None, regions=regions,
                                # a breakaway state keeps its country named (Abkhazia's map never said "Georgia")
                                skip_admin=None if kind == "partially recognised state" else skip_admin)
            finally:
                N.TINY_LABELS = saved_t
        # a territory of many scattered islands (French Polynesia, American Samoa) gets one ring on the locator,
        # not a ring round every speck on the close-up
        saved_nr = N.NO_RING
        N.NO_RING = N.NO_RING or len(m["_rings"]) >= 4
        N.SCATTER_DOTS = N.NO_RING
        try:
            v, why = pair(fp, bp, draw, FIXED_LADDER.get(nm, COMPACT_LADDER))
        finally:
            N.NO_RING, N.SCATTER_DOTS = saved_nr, False
        N.OTHER_GREY, N.GREY_EXCEPT, N.PROJ, N.MAP_CAPTION = False, None, None, ""
        tb = m["_bbox"]
        if nm in LOCATOR_BOX:
            locator(lp, LOCATOR_BOX[nm], [m], v)
        elif is_a1:
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
            m["_bbox"] = (-141, 42, -52, 80)
        if nm == "Russia":
            m["_bbox"] = (30, 44, 100, 70)
        if nm in ACROSS_180:
            # every island group, the frame centred across the 180th meridian (Kiribati showed only its
            # Line Islands, without Tarawa and the capital); longitudes past 180 are written as 180+
            lo = [np.column_stack([np.where(r[:, 0] < 0, r[:, 0] + 360, r[:, 0]), r[:, 1]]) for r in ft["_rings"]]
            a_ = np.vstack(lo)
            m = dict(ft, _rings=ft["_rings"], _bbox=(a_[:, 0].min(), a_[:, 1].min(), a_[:, 0].max(), a_[:, 1].max()))
        admin = ft["_p"].get("admin")
        N.MIN_SPAN["country"] = 3 if max(m["_bbox"][2] - m["_bbox"][0], m["_bbox"][3] - m["_bbox"][1]) < 1.0 else 6
        cap = (N.CAPITALS.get(nm) or [None, None, ""])[2]
        N.CITY_POINTS = main_cities(admin, cap, within=m)
        N.PROJ = tuple(round(c, 3) for c in centre(m["_bbox"]))
        mp = N.proj_feat(m)
        set_aspect(mp["_bbox"])

        def draw(label, png):
            # a small island state's neighbours are small islands too: named at their label points (Antigua's
            # map named Guadeloupe and nothing else)
            small = (m["_bbox"][2] - m["_bbox"][0]) * (m["_bbox"][3] - m["_bbox"][1]) < 6.0
            # a state of many specks (Micronesia, the Marshall Islands) gets no ring round each one
            scatter = len(m["_rings"]) >= 6 and max(np.ptp(r[:, 0]) * np.ptp(r[:, 1]) for r in m["_rings"]) < 0.5
            saved_t, saved_nr = N.TINY_LABELS, N.NO_RING
            N.TINY_LABELS = N.TINY_LABELS or small
            N.NO_RING = N.NO_RING or scatter
            N.SCATTER_DOTS = scatter
            try:
                return N.render({"Name": nm, "Alternate": f["Alternate"]}, "country", [mp], png, target_label=nm if label else None)
            finally:
                N.TINY_LABELS, N.NO_RING, N.SCATTER_DOTS = saved_t, saved_nr, False
        v, why = pair(fp, bp, draw, FIXED_LADDER.get(nm, COMPACT_LADDER))
        N.PROJ, N.CITY_POINTS = None, ()
        sub = ft["_p"].get("subregion") or ""
        box = SUBREGION_BOX.get(sub)
        tb = m["_bbox"]
        if not box or (tb[2] - tb[0]) > 0.5 * (box[2] - box[0]) or (tb[3] - tb[1]) > 0.5 * (box[3] - box[1]):
            box = CONTINENT_BOX.get(ft["_p"].get("continent") or "") or box   # Brazil fills South America's box
        if nm in ACROSS_180:
            locator(lp, ACROSS_180[nm], [m], v)
        elif nm in LOCATOR_BOX:
            locator(lp, LOCATOR_BOX[nm], [m], v)
        elif box and box[0] <= tb[0] and box[1] <= tb[1] and box[2] >= tb[2] and box[3] >= tb[3]:
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
        ring = state_ring(ring, xy, pf)
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
        if nm in MATCH_AS:
            # matched under Natural Earth's own name, inside a box that keeps its namesakes out
            mn, mbox = MATCH_AS[nm]
            N.NOTE_BOX[mn] = mbox
            feats, why = N.match(dict(f, Name=mn, Alternate=""), kind)
        else:
            feats, why = (island_at(nm), "") if nm in ISLAND_AT else N.match(f, kind)
        if not feats:
            return {"status": why or "no Natural Earth feature"}
        group = any("group" in (ft["_p"].get("featurecla") or "").lower() for ft in feats)
        feats = [islands_in(ft) if "group" in (ft["_p"].get("featurecla") or "").lower() else ft for ft in feats]
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
        # an island group is shown close up, its islands visible, with no ring round each speck (the Azores and
        # the Galapagos were rings in open ocean); the locator gives the wider view
        saved_nr = N.NO_RING
        N.NO_RING = N.NO_RING or group
        N.SCATTER_DOTS = bool(group)
        try:
            N.AVOID_EXTRA = ("hawaii",) if nm in HAWAII_ISLANDS else ()
            v, why = pair(fp, bp, draw, FIXED_LADDER.get(nm) or ((1.3,) if group else LADDER if kind in LONG_KINDS or kind in N.WATER else COMPACT_LADDER))
        finally:
            N.NO_RING, N.SCATTER_DOTS = saved_nr, False
            N.AVOID_EXTRA = ()
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
    ap.add_argument("--skip-kinds", default="")   # the last batch of a split run: every kind the others did not take
    ap.add_argument("--out", default=os.path.join(HERE, "renders", "geo_v4"))
    a = ap.parse_args()
    setup()
    os.makedirs(a.out, exist_ok=True)
    names = [x.strip() for x in a.names.split("|") if x.strip()]
    kinds = {x.strip() for x in a.kinds.split(",") if x.strip()}
    skip_kinds = {x.strip() for x in a.skip_kinds.split(",") if x.strip()}
    ids = C.anki("findNotes", query='note:"Geography"')
    notes = []
    for i in range(0, len(ids), 500):
        notes += C.anki("notesInfo", notes=ids[i:i + 500])
    order = {nm: i for i, nm in enumerate(names)}
    sel = [n for n in notes if (not names or C.plain(n["fields"]["Name"]["value"]).strip() in order)
           and (not kinds or C.plain(n["fields"]["Kind"]["value"]).strip() in kinds)
           and C.plain(n["fields"]["Kind"]["value"]).strip() not in skip_kinds]
    sel.sort(key=lambda n: order.get(C.plain(n["fields"]["Name"]["value"]).strip(), 0))
    # resumable: a note whose three maps are already on disk is not drawn again (unless --names asks for it),
    # and the manifest is written after every note, so a batch killed mid-run loses nothing
    mpath = os.path.join(a.out, "manifest.json")
    man, rows = {}, []
    for n in sel:
        nm = C.plain(n["fields"]["Name"]["value"]).strip()
        kd = C.plain(n["fields"]["Kind"]["value"]).strip()
        s_ = slug(nm + " " + {"canal": "river"}.get(kd, kd))
        paths = {k: os.path.join(a.out, "%s-%s.png" % (pre, s_)) for k, pre in (("front", "g4front"), ("back", "g4lab"), ("locator", "g4loc"))}
        if not names and all(os.path.exists(p) for p in paths.values()):
            r = dict(paths, status="rendered")
        else:
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
        json.dump(man, open(mpath + ".part", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(man, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sheet(rows, a.out)
    print(len(rows), "rendered of", len(man))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
