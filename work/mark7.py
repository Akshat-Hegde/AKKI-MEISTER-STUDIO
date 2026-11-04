"""AKKI MEISTER round 7: a constructed square-shouldered A (flat top, near-vertical legs, as in the diary
sketches), matched to Saira Bold Italic's M in stem weight, cap height and 12-degree italic."""
import math, os
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity
import mark6
from mark6 import Mark, clean, save as _save, K
from mark4 import glyph_poly

OUT = "../round7/"
os.makedirs(OUT, exist_ok=True)
mark6.OUT = OUT


def stem_width(M, y):
    seg = M.intersection(box(-1e5, y, 1e5, y + 0.5))
    gs = list(seg.geoms) if hasattr(seg, "geoms") else [seg]
    gs.sort(key=lambda g: g.bounds[0])
    return gs[0].bounds[2] - gs[0].bounds[0]


class SquareMark(Mark):
    def __init__(self, wght=700, gap=0.06, chamfer=0.0, width=0.80, bar=0.11):
        M, _ = glyph_poly("M", wght=wght)
        x0, y0, x1, y1 = M.bounds
        H = y1 - y0
        self.HT = H
        s = stem_width(M, y0 + H * 0.85)          # horizontal stem thickness incl. italic
        sh = s * 0.86                              # horizontal strokes slightly lighter
        W = H * width
        TH = H * 0.075
        YC = y0 + H * 0.60
        # upright construction, y0 = cap, y1 = baseline
        c = H * chamfer
        outer = Polygon([(0, y1), (0, y0 + c), (c, y0), (W, y0), (W, y1)]) if c else box(0, y0, W, y1)
        counter = box(s, y0 + sh, W - s, YC - TH / 2 - H * bar)
        legs = box(s, YC - TH / 2, W - s, y1 + 1)
        A = outer.difference(counter).difference(legs)
        A = affinity.skew(A, xs=-12, origin=(0, y1))   # lean like Saira italic (top moves right)
        # place M with an even gap
        lo, hi = -W, W * 3
        for _ in range(50):
            mid = (lo + hi) / 2
            Mt = affinity.translate(M, mid, 0)
            if A.intersects(Mt) or A.distance(Mt) < gap * H:
                lo = mid
            else:
                hi = mid
        M = affinity.translate(M, hi, 0)
        self.body = unary_union([A, M])
        self.X0, self.Y0, self.X1, self.Y1 = self.body.bounds
        self.YC, self.TH = YC, TH
        self.bars()


def save(name, parts, HT):
    _save(name, parts, HT)


if __name__ == "__main__":
    import mark6 as m6
    specs = {"sq": dict(chamfer=0.0), "ch": dict(chamfer=0.16)}
    for tag, kw in specs.items():
        m = SquareMark(**kw)
        save(f"{tag}-1-bars", [(m.barsam(), "main")], m.HT)
        save(f"{tag}-2-redline", m.redline(), m.HT)
        save(f"{tag}-3-plate", m6.f_split_plate(SquareMark(**kw)), m.HT)
        save(f"{tag}-4-pill", m6.f_pill_bars(SquareMark(**kw)), m.HT)
        save(f"{tag}-5-am", [(SquareMark(**kw).fusion(), "main")], m.HT)
    print("ok")
