"""AKKI MEISTER round 5: refine the Fusion AM. Negative-space speed bars (from the ///AM diary sketch)
and a set of box styles. Every edge keeps Saira's 12-degree italic."""
import math, os
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity
from mark4 import glyph_poly, fit, svg, NIGHT, ICE, RED

OUT = "../round5/"
os.makedirs(OUT, exist_ok=True)
K = math.tan(math.radians(12))


def base():
    A, aw = glyph_poly("A")
    M, _ = glyph_poly("M")
    M = affinity.translate(M, aw * 0.80, 0)
    body = unary_union([A, M])
    x0, y0, x1, y1 = body.bounds
    return body, (x0, y0, x1, y1)


BODY, (X0, Y0, X1, Y1) = base()
HT = Y1 - Y0
YC = Y0 + HT * 0.60          # slit centre (A crossbar height)
TH = HT * 0.085              # slit thickness


def slant(xb, w, y0=Y0, y1=Y1):
    """parallelogram leaning with the italic; xb = left edge at the baseline (y1)"""
    return Polygon([(xb + (y1 - y0) * K, y0), (xb + w + (y1 - y0) * K, y0), (xb + w, y1), (xb, y1)])


def slit_poly(x_from, x_to, th=TH, yc=YC):
    return Polygon([(x_from, yc - th / 2), (x_to, yc - th / 2), (x_to, yc + th / 2), (x_from, yc + th / 2)])


def fusion(th=TH):
    return BODY.difference(slit_poly(X0 - 300, X1 + 300, th))


def bars(gap=HT * 0.07, widths=(0.07, 0.11, 0.16)):
    """three speed bars, thin to thick, sitting left of the A"""
    out, x = [], X0 - gap
    polys = []
    for w in reversed(widths):
        ww = HT * w
        x -= ww
        polys.append(slant(x - HT * K * 0, ww))
        x -= gap
    return unary_union(polys)


# ------------------------------------------------------------------ variants
def v_fusion():
    return [(fusion(), "main")]


def v_speedbars():
    """///AM: speed bars launch into the fusion, the slit runs through bars and letters alike"""
    g = unary_union([BODY, bars()])
    return [(g.difference(slit_poly(X0 - 2000, X1 + 300)), "main")]


def v_cut_leg():
    """negative-space speed: the A's left leg is sliced into three by parallel italic cuts"""
    cuts = unary_union([slant(X0 + HT * 0.10 + i * HT * 0.105, HT * 0.032, Y0 + HT * 0.30, Y1) for i in range(2)])
    g = fusion().difference(cuts)
    return [(g, "main")]


def v_twin_slit():
    """two slits: a hairline above the main cut, like a speed line and its shadow"""
    g = BODY.difference(slit_poly(X0 - 300, X1 + 300)).difference(slit_poly(X0 - 300, X1 + 300, TH * 0.32, YC - TH * 1.35))
    return [(g, "main")]


def v_red_slit_bars():
    """speed bars in Ice, the slit filled red: the overtaking line"""
    g = unary_union([BODY, bars()]).difference(slit_poly(X0 - 2000, X1 + 300, TH * 1.9))
    red = slit_poly(X0 - HT * 0.45, X1 - HT * 0.2, TH * 0.9)
    return [(g, "main"), (red, "accent")]


# ---- box styles -----------------------------------------------------
PAD = HT * 0.42


def italic_box(x0, y0, x1, y1, ch=0.0):
    """parallelogram box leaning with the italic, optional chamfer on top-right/bottom-left"""
    h = y1 - y0
    pts = [(x0 + h * K, y0), (x1 + h * K - ch, y0), (x1 + h * K - ch * (1 - K), y0 + ch), (x1, y1), (x0 + ch, y1), (x0 + ch * K, y1 - ch)] if ch else \
          [(x0 + h * K, y0), (x1 + h * K, y0), (x1, y1), (x0, y1)]
    return Polygon(pts)


def b_tile_split():
    """solid italic tile, AM knocked out; the slit splits the whole tile, top half pushed ahead"""
    t = italic_box(X0 - PAD, Y0 - PAD, X1 + PAD * 0.3, Y1 + PAD)
    knock = t.difference(BODY)
    top = knock.intersection(box(-1e4, -1e4, 1e4, YC - TH / 2))
    bot = knock.intersection(box(-1e4, YC + TH / 2, 1e4, 1e4))
    return [(affinity.translate(top, HT * 0.06, 0), "main"), (bot, "main")]


def b_brackets():
    """open frame: only two chamfered corner brackets, top-left and bottom-right"""
    f = fusion()
    o = italic_box(X0 - PAD, Y0 - PAD * 0.85, X1 + PAD * 0.25, Y1 + PAD * 0.85)
    i = o.buffer(-HT * 0.065, join_style=2)
    ring = o.difference(i)
    xa, ya, xb, yb = o.bounds
    keep = unary_union([box(xa - 10, ya - 10, xa + (xb - xa) * 0.30, ya + (yb - ya) * 0.42), box(xa + (xb - xa) * 0.70, ya + (yb - ya) * 0.58, xb + 10, yb + 10)])
    return [(f, "main"), (ring.intersection(keep), "main")]


def b_plate():
    """number-plate: tile with the ///AM knocked out and a hairline inset frame"""
    g = unary_union([BODY, bars()])
    xa = X0 - HT * 0.55
    o = italic_box(xa - PAD * 0.6, Y0 - PAD * 0.7, X1 + PAD * 0.35, Y1 + PAD * 0.7)
    inner = o.buffer(-HT * 0.05, join_style=2)
    frame_gap = inner.difference(inner.buffer(-HT * 0.035, join_style=2))
    solid = o.difference(frame_gap).difference(g.difference(slit_poly(X0 - 2000, X1 + 300)))
    return [(solid, "main")]


def b_visor_thin():
    """refined visor crest: thinner ring, tighter field, the slit exits through the ring on the right"""
    f = fusion()
    xa, ya, xb, yb = X0, Y0, X1, Y1
    cx, cy = (xa + xb) / 2, (ya + yb) / 2
    W2, H2, c = (xb - xa) / 2 + HT * 0.55, HT / 2 + HT * 0.5, HT * 0.5
    shape = Polygon([(cx - W2 + c, cy - H2), (cx + W2, cy - H2), (cx + W2, cy + H2 - c), (cx + W2 - c, cy + H2), (cx - W2, cy + H2), (cx - W2, cy - H2 + c)])
    shape = affinity.skew(shape, xs=-12, origin=(cx, cy))
    ring = shape.difference(shape.buffer(-HT * 0.045, join_style=2))
    field = shape.buffer(-HT * 0.11, join_style=2)
    solid = unary_union([ring, field.difference(BODY)])
    return [(solid, "main")]


def b_pill():
    """tall-radius tile (rounded parallelogram) with the fusion knocked out"""
    o = italic_box(X0 - PAD, Y0 - PAD * 0.8, X1 + PAD * 0.3, Y1 + PAD * 0.8)
    r = HT * 0.28
    o = o.buffer(-r, join_style=2).buffer(r, join_style=1)
    return [(o.difference(fusion()).difference(slit_poly(X0 - 2000, X0 + HT * 0.1)), "main")]


VARIANTS = {
    "01-fusion": ("Fusion", "The refined base: one silhouette, one slit.", v_fusion),
    "02-speedbars": ("///AM", "Your diary sketch: three bars launch into the AM; the slit cuts bars and letters alike.", v_speedbars),
    "05-red-line": ("Red line", "Bars and letters split wide; a red overtaking line runs through the gap.", v_red_slit_bars),
    "06-tile-split": ("Split tile", "Solid italic tile, AM knocked out; the slit splits the tile and the top half surges ahead.", b_tile_split),
    "07-brackets": ("Brackets", "Open frame: two chamfered corner brackets, the mark breathing in between.", b_brackets),
    "08-plate": ("Race plate", "///AM knocked out of a number-plate tile with a hairline inset.", b_plate),
    "09-visor": ("Visor", "A thinner visor crest: a team badge for avatars, patches and kit.", b_visor_thin),
    "10-pill": ("Pill", "Rounded italic tile, softer and more product-like.", b_pill),
}

def clean(parts):
    """drop slivers left where glyph overlaps meet a cut, then square up with a tiny open"""
    out = []
    for g, r in parts:
        e = HT * 0.004
        g = g.buffer(-e, join_style=2).buffer(e, join_style=2)
        tot = g.area
        gs = list(g.geoms) if hasattr(g, "geoms") else [g]
        g = unary_union([p for p in gs if p.area > tot * 0.004])
        out.append((g, r))
    return out


if __name__ == "__main__":
    for k, (_, _, fn) in VARIANTS.items():
        g = fit(clean(fn()), pad=26)
        open(OUT + f"{k}.svg", "w").write(svg(g, {"main": NIGHT, "accent": RED}, title=f"AKKI MEISTER {k}"))
        open(OUT + f"{k}-rev.svg", "w").write(svg(g, {"main": ICE, "accent": RED}, bg=NIGHT, title=f"AKKI MEISTER {k} reversed"))
    print("ok")
