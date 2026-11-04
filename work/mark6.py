"""AKKI MEISTER round 6: lighter weight, a gap between A and M, a flat (rectangular) A tip,
and fusions of the round-5 favourites (///AM, red line, brackets, race plate, pill)."""
import math, os
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity
from mark4 import glyph_poly, fit, svg, NIGHT, ICE, RED

OUT = "../round6/"
os.makedirs(OUT, exist_ok=True)
K = math.tan(math.radians(12))


class Mark:
    def __init__(self, wght=800, gap=0.05, tip="flat", tipw=0.40):
        A, aw = glyph_poly("A", wght=wght)
        M, _ = glyph_poly("M", wght=wght)
        x0, y0, x1, y1 = A.bounds
        self.HT = y1 - y0
        if tip == "flat":
            A = self.flatten(A, y0, tipw)
        # place M so the closest distance to A is exactly gap*HT (0 = fused)
        lo, hi = -aw, aw * 2
        target = gap * self.HT
        for _ in range(50):
            mid = (lo + hi) / 2
            d = A.distance(affinity.translate(M, mid, 0))
            inter = A.intersects(affinity.translate(M, mid, 0))
            if inter or d < target:
                lo = mid
            else:
                hi = mid
        M = affinity.translate(M, hi if gap > 0 else lo + aw * 0.02, 0)
        self.body = unary_union([A, M])
        self.X0, self.Y0, self.X1, self.Y1 = self.body.bounds
        self.YC = self.Y0 + self.HT * 0.60
        self.TH = self.HT * 0.075

    def flatten(self, A, top, tipw):
        """cut the pointed apex off and rebuild it as a flat italic block: a rectangular tip"""
        h = self.HT
        cut_y = top + h * 0.30
        low = A.intersection(box(-1e5, cut_y, 1e5, 1e5))
        # width of the A at the cut line
        seg = A.intersection(box(-1e5, cut_y, 1e5, cut_y + 0.5)).bounds
        xl, xr = seg[0], seg[2]
        w = max(xr - xl, h * tipw)
        cx = (xl + xr) / 2
        dy = cut_y - top
        cap = Polygon([(cx - w / 2 + dy * K, top), (cx + w / 2 + dy * K, top), (cx + w / 2, cut_y + 1), (cx - w / 2, cut_y + 1)])
        return unary_union([low, cap])

    def slant(self, xb, w, y0=None, y1=None):
        y0 = self.Y0 if y0 is None else y0
        y1 = self.Y1 if y1 is None else y1
        return Polygon([(xb + (y1 - y0) * K, y0), (xb + w + (y1 - y0) * K, y0), (xb + w, y1), (xb, y1)])

    def slit(self, a, b, th=None, yc=None):
        th = th or self.TH
        yc = yc or self.YC
        return Polygon([(a, yc - th / 2), (b, yc - th / 2), (b, yc + th / 2), (a, yc + th / 2)])

    def bars(self, gap=0.07, widths=(0.06, 0.09, 0.13)):
        polys, x = [], self.X0 - self.HT * gap
        for w in reversed(widths):
            ww = self.HT * w
            x -= ww
            polys.append(self.slant(x, ww))
            x -= self.HT * gap
        self.BX0 = x
        return unary_union(polys)

    def ibox(self, x0, y0, x1, y1):
        h = y1 - y0
        return Polygon([(x0 + h * K, y0), (x1 + h * K, y0), (x1, y1), (x0, y1)])

    # ---- building blocks
    def fusion(self, th=None):
        return self.body.difference(self.slit(self.X0 - 1e4, self.X1 + 1e4, th))

    def barsam(self, th=None):
        return unary_union([self.body, self.bars()]).difference(self.slit(-1e5, 1e5, th))

    def redline(self):
        g = unary_union([self.body, self.bars()]).difference(self.slit(-1e5, 1e5, self.TH * 1.9))
        return [(g, "main"), (self.slit(self.BX0 + self.HT * 0.1, self.X1 - self.HT * 0.15, self.TH * 0.9), "accent")]


def clean(parts, HT):
    out = []
    for g, r in parts:
        e = HT * 0.004
        g = g.buffer(-e, join_style=2).buffer(e, join_style=2)
        gs = list(g.geoms) if hasattr(g, "geoms") else [g]
        tot = g.area
        out.append((unary_union([p for p in gs if p.area > tot * 0.004]), r))
    return out


def save(name, parts, HT, pad=26):
    g = fit(clean(parts, HT), pad=pad)
    open(OUT + f"{name}.svg", "w").write(svg(g, {"main": NIGHT, "accent": RED}, title=f"AKKI MEISTER {name}"))
    open(OUT + f"{name}-rev.svg", "w").write(svg(g, {"main": ICE, "accent": RED}, bg=NIGHT, title=f"AKKI MEISTER {name} reversed"))


# ------------------------------------------------------------------ fusions of B / C / E / F / H
def f_plate_red(m):
    """F + C: race plate, ///AM knocked out, red line running through the plate"""
    g = unary_union([m.body, m.bars()])
    pad = m.HT * 0.38
    o = m.ibox(m.BX0 - pad * 0.5, m.Y0 - pad, m.X1 + pad * 0.3, m.Y1 + pad)
    inner = o.buffer(-m.HT * 0.045, join_style=2)
    hair = inner.difference(inner.buffer(-m.HT * 0.03, join_style=2))
    solid = o.difference(hair).difference(g).difference(m.slit(-1e5, 1e5, m.TH * 1.9))
    return [(solid, "main"), (m.slit(o.bounds[0] - 10, o.bounds[2] + 10, m.TH * 0.9).intersection(o), "accent")]


def f_brackets_bars(m):
    """E + B: ///AM inside two corner brackets"""
    g = m.barsam()
    pad = m.HT * 0.36
    o = m.ibox(m.BX0 - pad * 0.6, m.Y0 - pad, m.X1 + pad * 0.25, m.Y1 + pad)
    ring = o.difference(o.buffer(-m.HT * 0.05, join_style=2))
    xa, ya, xb, yb = o.bounds
    keep = unary_union([box(xa - 10, ya - 10, xa + (xb - xa) * .24, ya + (yb - ya) * .45), box(xa + (xb - xa) * .76, ya + (yb - ya) * .55, xb + 10, yb + 10)])
    return [(g, "main"), (ring.intersection(keep), "main")]


def f_pill_bars(m):
    """H + B: rounded tile, ///AM knocked out, the slit exits the tile on the left"""
    g = m.barsam()
    pad = m.HT * 0.34
    o = m.ibox(m.BX0 - pad * 0.5, m.Y0 - pad * .9, m.X1 + pad * 0.3, m.Y1 + pad * .9)
    r = m.HT * 0.24
    o = o.buffer(-r, join_style=2).buffer(r, join_style=1)
    return [(o.difference(unary_union([m.body, m.bars()])).difference(m.slit(-1e5, 1e5)), "main")]


def f_split_plate(m):
    """F + D: plate split by the slit, top half nudged forward"""
    pad = m.HT * 0.36
    o = m.ibox(m.BX0 - pad * 0.5, m.Y0 - pad, m.X1 + pad * 0.3, m.Y1 + pad)
    k = o.difference(unary_union([m.body, m.bars()]))
    top = k.intersection(box(-1e5, -1e5, 1e5, m.YC - m.TH / 2))
    bot = k.intersection(box(-1e5, m.YC + m.TH / 2, 1e5, 1e5))
    return [(affinity.translate(top, m.HT * .05, 0), "main"), (bot, "main")]


def f_brackets_red(m):
    """E + C: brackets + ///AM + red line"""
    parts = m.redline()
    pad = m.HT * 0.36
    o = m.ibox(m.BX0 - pad * 0.6, m.Y0 - pad, m.X1 + pad * 0.25, m.Y1 + pad)
    ring = o.difference(o.buffer(-m.HT * 0.05, join_style=2))
    xa, ya, xb, yb = o.bounds
    keep = unary_union([box(xa - 10, ya - 10, xa + (xb - xa) * .24, ya + (yb - ya) * .45), box(xa + (xb - xa) * .76, ya + (yb - ya) * .55, xb + 10, yb + 10)])
    return parts + [(ring.intersection(keep), "main")]


if __name__ == "__main__":
    # 1. weight / gap / tip study on plain ///AM
    study = []
    for wg in (900, 800, 700):
        for gap, tip in ((0.0, "point"), (0.05, "point"), (0.05, "flat")):
            m = Mark(wg, gap, tip)
            n = f"s-{wg}-{'gap' if gap else 'fused'}-{tip}"
            save(n, [(m.barsam(), "main")], m.HT)
            study.append(n)
    # 2. fusions at the chosen spec (800, gap, flat)
    m = Mark(700, 0.05, "flat")
    fus = {"f1-bars": [(m.barsam(), "main")], "f2-redline": m.redline(), "f3-plate-red": f_plate_red(m), "f4-brackets-bars": f_brackets_bars(m),
           "f5-pill-bars": f_pill_bars(m), "f6-split-plate": f_split_plate(m), "f7-brackets-red": f_brackets_red(Mark(700, 0.05, "flat")),
           "f8-fusion-small": [(m.fusion(), "main")]}
    for k, v in fus.items():
        save(k, v, m.HT)
    print("ok", len(study), len(fus))
