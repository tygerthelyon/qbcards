# -*- coding: utf-8 -*-
"""crop_match_1002.py -- where a small deck picture is a crop of a larger photograph, the same crop cut from the original.

Some deck pictures are tight crops of a group photograph (Twyla Tharp from a photo with George and Laura Bush).
Matching the crop against the full photograph finds it, but the full photograph shows other people too, which
would make a "who is this?" card ambiguous. This finds where the old picture sits inside the candidate (the ORB/
RANSAC homography maps the old picture's corners into the candidate) and records that box as fractions, so
img_replace_1002.py cuts the same crop from the full-size original: the same picture, larger, and the caption
stays true.

    py -3.9 crop_match_1002.py JOBS.json KEY:INDEX ...      (prints picks with crop boxes to merge into a pick file)
"""
import json, os, sys
import cv2
import numpy as np
import img_upgrade_1002 as U


def box(old_path, cand):
    a, b = U.gray(old_path, 800), U.gray(U.thumb(cand), 800)
    big = U.gray(U.thumb(cand), 800)
    o = cv2.ORB_create(4000)
    ka, da = o.detectAndCompute(a, None)
    kb, db = o.detectAndCompute(b, None)
    good = [m[0] for m in cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da, db, k=2) if len(m) == 2 and m[0].distance < 0.75 * m[1].distance]
    H, mask = cv2.findHomography(np.float32([ka[m.queryIdx].pt for m in good]), np.float32([kb[m.trainIdx].pt for m in good]), cv2.RANSAC, 5.0)
    h, w = a.shape
    pts = cv2.perspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2), H).reshape(-1, 2)
    bh, bw = b.shape
    x0, y0 = max(0, pts[:, 0].min() / bw), max(0, pts[:, 1].min() / bh)
    x1, y1 = min(1, pts[:, 0].max() / bw), min(1, pts[:, 1].max() / bh)
    return [round(float(v), 4) for v in (x0, y0, x1, y1)], int(mask.sum())


if __name__ == "__main__":
    jobs = {j["key"]: j for j in json.load(open(sys.argv[1], encoding="utf-8"))}
    cands = json.load(open(sys.argv[1].replace(".json", "_cands.json"), encoding="utf-8"))
    for arg in sys.argv[2:]:
        key, idx = arg.rsplit(":", 1)
        c = cands[key][int(idx)]
        b, n = box(os.path.join(U.MEDIA, jobs[key]["file"]), c)
        px = ((b[2] - b[0]) * c["w"], (b[3] - b[1]) * c["h"])
        print(json.dumps({key: [int(idx), None, b]}, ensure_ascii=False), "inliers", n, "crop px %dx%d" % px)
