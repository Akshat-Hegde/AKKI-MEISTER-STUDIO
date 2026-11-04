"""Bars as starting-grid slots: each bar piece becomes a ']' bracket (front line toward the AM, short ticks back)."""
from shapely import affinity
from shapely.geometry import box, Polygon
from shapely.ops import unary_union
import mark10 as m
from tune import NIGHT, ICE, RED, ORANGE, BLUE

OUT = "../FINAL-AM/tuning/"


def bracket(piece, w, tick):
    """']' bracket from a slanted parallelogram piece: front (right) edge + top/bottom ticks of length tick"""
    inner = piece.buffer(-w, join_style=2)
    if inner.is_empty:
        return piece
    hole = unary_union([inner, affinity.translate(inner, -10000, 0)]).convex_hull
    br = piece.difference(hole)
    x0, y0, x1, y1 = piece.bounds
    keep = affinity.translate(piece, (x1 - x0) * 0 + 0, 0)
    # keep only the right-most `tick` width of the piece (measured horizontally at each height)
    pw = piece.intersection(box(-1e5, (y0 + y1) / 2 - .01, 1e5, (y0 + y1) / 2 + .01)).bounds
    width = pw[2] - pw[0]
    right = piece.intersection(affinity.translate(piece, max(width - tick, 0), 0))
    return br.intersection(right)


def build(w_ratio, tick_ratio, stagger=False):
    body, bars, (yc, t, H) = m.build4(cutw=0.06, parts=True)
    pieces = []
    for i, b in enumerate(bars):
        ps = list(b.geoms) if hasattr(b, "geoms") else [b]
        if stagger and i == 1:
            # the middle column is cut at a different height: a staggered grid
            whole = unary_union(ps).convex_hull
            k = box(-1e5, yc - t / 2 - H * .22, 1e5, yc + t / 2 - H * .22)
            ps = list(whole.difference(k).geoms)
        for p in ps:
            pw = p.intersection(box(-1e5, p.centroid.y - .01, 1e5, p.centroid.y + .01)).bounds
            width = pw[2] - pw[0]
            pieces.append(bracket(p, H * w_ratio, width * tick_ratio))
    return body, unary_union(pieces)


def save(name, body, slots, fg, col, bg):
    allg = unary_union([body, slots])
    x0, y0, x1, y1 = allg.bounds
    s = 220 / max(x1 - x0, y1 - y0)
    T = lambda g: affinity.affine_transform(g, [s, 0, 0, s, 128 - (x0 + x1) / 2 * s, 128 - (y0 + y1) / 2 * s])
    open(OUT + name + ".svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><rect width="256" height="256" fill="{bg}"/>'
                                         f'<path fill="{fg}" fill-rule="evenodd" d="{m.d_of(T(body))}"/><path fill="{col}" d="{m.d_of(T(slots))}"/></svg>')


V = {"thin": (0.012, 0.55, False), "bold": (0.025, 0.55, False), "long": (0.014, 1.0, False), "stagger": (0.014, 0.55, True)}
for bg, tag, fg in ((ICE, "l", NIGHT), (NIGHT, "d", ICE)):
    for col, cn in ((ORANGE, "orange"), (RED, "red"), (BLUE, "cobalt"), (fg, "mono")):
        for k, (w, tk, st) in V.items():
            body, sl = build(w, tk, st)
            save(f"{tag}-slot-{k}-{cn}", body, sl, fg, col, bg)
print("ok")
