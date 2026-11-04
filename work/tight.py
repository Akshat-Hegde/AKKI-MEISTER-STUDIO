"""Tighter chequer: smaller row/column gaps and a smaller gap to the A."""
import os, json, random
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
import mark10 as m
from mark10 import K, PHI
import iter2
from tune import NIGHT, ICE, RED

iter2.OUT = OUT = "../FINAL-AM/iter4/"
os.makedirs(OUT, exist_ok=True)


def build(rows=(4, 3), col_gap=0.06, row_gap=0.035, a_gap=0.06, widths=(0.13, 0.13 / PHI, 0.13 / PHI ** 2), phase=0, fade=(1, .58, .28), col=RED):
    body, _, (yc, t, H) = m.build4(cutw=0.035, parts=True)
    top, bot = yc - t / 2, yc + t / 2           # keep the crossbar alignment
    rg = row_gap * H
    def bands(a, b, n):
        h = (b - a - (n - 1) * rg) / n
        return [(a + i * (h + rg), a + i * (h + rg) + h) for i in range(n)]
    rws = bands(0, top, rows[0]) + bands(bot, H, rows[1])
    it, x = [], -a_gap * H
    for i, w in enumerate(widths):
        ww = H * w
        x -= ww
        bar = Polygon([(x + H * K, 0), (x + ww + H * K, 0), (x + ww, H), (x, H)])
        for j, (r0, r1) in enumerate(rws):
            if (i + j + phase) % 2 == 0:
                it.append((bar.intersection(box(-1e5, r0, 1e5, r1)), col[i] if isinstance(col, tuple) else col, fade[i]))
        x -= col_gap * H
    return body, it


V = [("00-current", "Current (7 rows)", {}),
     ("01-tight-a", "Tighter to the A", dict(a_gap=0.035)),
     ("02-tight-cols", "Tighter columns", dict(col_gap=0.03, a_gap=0.035)),
     ("03-tight-all", "Tight rows + columns", dict(col_gap=0.03, row_gap=0.02, a_gap=0.035)),
     ("04-touching", "Squares touch at corners", dict(col_gap=0.0, row_gap=0.0, a_gap=0.035)),
     ("05-wide-squares", "Wider squares, tight", dict(col_gap=0.025, row_gap=0.02, a_gap=0.035, widths=(0.15, 0.13, 0.11))),
     ("06-equal-squares", "Equal squares, tight", dict(col_gap=0.025, row_gap=0.02, a_gap=0.035, widths=(0.12, 0.12, 0.12))),
     ("07-touching-equal", "Equal + touching (true flag)", dict(col_gap=0.0, row_gap=0.0, a_gap=0.035, widths=(0.12, 0.12, 0.12)))]
for bg, tag, fg in ((NIGHT, "d", ICE), (ICE, "l", NIGHT)):
    for n, l, kw in V:
        body, it = build(**kw)
        iter2.write(f"{tag}-{n}", body, it, bg, fg)
json.dump([(n, l) for n, l, _ in V], open(OUT + "index.json", "w"))
print("ok")
