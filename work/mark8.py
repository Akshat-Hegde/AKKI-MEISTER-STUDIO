"""AKKI MEISTER round 8: iterations on the horizontal cut (where it cuts, how, and what the bars do)."""
import os
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity
import mark6
from mark6 import clean, K
from mark7 import SquareMark

OUT = "../round8/"
os.makedirs(OUT, exist_ok=True)
mark6.OUT = OUT

m = SquareMark(chamfer=0.16)
HT, X0, X1, Y0, Y1, YC, TH = m.HT, m.X0, m.X1, m.Y0, m.Y1, m.YC, m.TH
AM = m.body
BARS = m.bars()
BX0 = m.BX0
ALLX = (-1e5, 1e5)


def cut(x0, x1, th=TH, yc=YC):
    return Polygon([(x0, yc - th / 2), (x1, yc - th / 2), (x1, yc + th / 2), (x0, yc + th / 2)])


def bar_list(widths=(0.06, 0.09, 0.13), gap=0.07, tops=(0, 0, 0)):
    """individual bars, thin to thick, optional top offsets (fraction of HT, 0 = full height)"""
    out, x = [], X0 - HT * gap
    for w, t in zip(reversed(widths), reversed(tops)):
        ww = HT * w
        x -= ww
        out.insert(0, m.slant(x, ww, Y0 + HT * t, Y1))
        x -= HT * gap
    return out


V = {}
# 01 · cut through everything (reference)
V["01-all"] = ("Full cut", "One line through bars and letters: the reference.",
               [(unary_union([AM, BARS]).difference(cut(*ALLX)), "main")])
# 02 · cut only the AM, bars untouched
V["02-am-only"] = ("AM cut", "Bars stay whole; only the letters are split, so the motion sits inside the name.",
                   [(unary_union([AM.difference(cut(X0 - 1, X1 + 1)), BARS]), "main")])
# 03 · cut only the bars, AM untouched
V["03-bars-only"] = ("Bar cut", "The letters stay whole; the cut lives in the bars, like exhaust or a timing beam.",
                     [(unary_union([AM, BARS.difference(cut(*ALLX))]), "main")])
# 04 · tapered wedge: thick through the bars, closing to a hairline at the M
wedge = Polygon([(BX0 - 50, YC - TH * 0.95), (X1 + HT * 0.05, YC - TH * 0.06), (X1 + HT * 0.05, YC + TH * 0.06), (BX0 - 50, YC + TH * 0.95)])
V["04-wedge"] = ("Wedge", "The cut tapers from wide in the bars to a hairline at the M: speed fading forward.",
                 [(unary_union([AM, BARS]).difference(wedge), "main")])
# 05 · shift: everything above the cut nudged forward (overtake)
whole = unary_union([AM, BARS]).difference(cut(*ALLX))
top = whole.intersection(box(-1e5, -1e5, 1e5, YC))
bot = whole.intersection(box(-1e5, YC, 1e5, 1e5))
V["05-shift"] = ("Overtake", "The top half slides ahead of the bottom: the moment of the pass.",
                 [(affinity.translate(top, HT * 0.13, 0), "main"), (bot, "main")])
# 06 · rev bars: bars rise from short to full height, then the AM (a rev counter / launch)
rev = unary_union(bar_list(tops=(0.55, 0.30, 0.0)))
V["06-rev"] = ("Rev bars", "Bars rise short to tall into the A: a launch, a rev counter, a podium.",
               [(unary_union([AM, rev]).difference(cut(*ALLX)), "main")])
# 07 · dashed bars: each bar broken into three by two thin cuts, AM cut once
dash = unary_union([BARS]).difference(cut(*ALLX, TH * 0.6, Y0 + HT * 0.32)).difference(cut(*ALLX, TH * 0.6, Y0 + HT * 0.68))
V["07-dashed"] = ("Data bars", "The bars break into segments like a telemetry strip; the AM keeps the single cut.",
                  [(unary_union([AM.difference(cut(X0 - 1, X1 + 1)), dash]), "main")])
# 08 · staggered: each element cut a little lower than the one before (a falling line)
st = []
els = bar_list() + [AM]
for i, e in enumerate(els):
    st.append(e.difference(cut(*ALLX, TH, YC - HT * 0.24 + i * HT * 0.08)))
V["08-stagger"] = ("Stagger", "The cut steps down element by element, like a car braking into a corner.",
                   [(unary_union(st), "main")])
# 09 · red cut, bars only (accent lives in the bars)
V["09-red-bars"] = ("Red exhaust", "The AM stays clean; a red line runs through the bars only.",
                    [(unary_union([AM, BARS.difference(cut(*ALLX, TH * 1.8))]), "main"), (cut(BX0 - HT * 0.15, X0 - HT * 0.02, TH * 0.8), "accent")])
# 10 · red cut that stops at the M's last stem (enters, does not leave)
V["10-red-enter"] = ("Red entry", "A red line enters from the bars and stops inside the M: the mark is the finish line.",
                     [(unary_union([AM, BARS]).difference(cut(*ALLX, TH * 1.8)), "main"), (cut(BX0 - HT * 0.35, X1 - HT * 0.35, TH * 0.8), "accent")])
# 11 · single thick bar as a negative: bars removed, a block left of A with the three bars knocked out of it
blk = m.slant(BX0 - HT * 0.05, (X0 - HT * 0.075) - (BX0 - HT * 0.05))
V["11-block"] = ("Bar block", "The bars become negative space inside a solid block that leads the AM.",
                 [(unary_union([AM.difference(cut(X0 - 1, X1 + 1)), blk.difference(BARS).difference(cut(*ALLX))]), "main")])
# 12 · the cut runs through the bars and the A, then stops: the M stays whole (the line ends at the M)
mx = min(x for x, y in AM.exterior.coords) if hasattr(AM, "exterior") else None
Mpart = max(AM.geoms, key=lambda g: g.bounds[2]) if hasattr(AM, "geoms") else AM
Apart = min(AM.geoms, key=lambda g: g.bounds[0]) if hasattr(AM, "geoms") else AM
V["12-a-cut"] = ("A cut", "The line runs through the bars and the A, then stops: the M is the wall it hits.",
                 [(unary_union([unary_union([Apart, BARS]).difference(cut(*ALLX)), Mpart]), "main")])

if __name__ == "__main__":
    for k, (_, _, parts) in V.items():
        mark6.save(k, parts, HT)
    print("ok", len(V))
