"""AKKI MEISTER round 4 marks. Letterforms come from Saira Expanded Black Italic (outlined),
then fused and cut with real boolean geometry (shapely)."""
import math
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from shapely import affinity
import saira

OUT = "../round4/"
NIGHT, INK, ICE, RED = "#06070B", "#0B0D14", "#F4F5F7", "#E10A23"


def glyph_poly(ch, size=1000, wght=900, wdth=125, italic=True):
    f = saira.font(wght, wdth, italic)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    sc = size / f["head"].unitsPerEm
    rp = RecordingPen()
    gs[cmap[ord(ch)]].draw(TransformPen(rp, (sc, 0, 0, -sc, 0, 0)))
    rings, cur = [], []
    for op, args in rp.value:
        if op == "moveTo":
            cur = [args[0]]
        elif op == "lineTo":
            cur.append(args[0])
        elif op in ("qCurveTo", "curveTo"):
            # flatten curves
            p0 = cur[-1]
            pts = list(args)
            if op == "qCurveTo":
                ctrl, end = pts[:-1], pts[-1]
                seq = [p0]
                for i, c in enumerate(ctrl):
                    e = end if i == len(ctrl) - 1 else ((c[0] + ctrl[i + 1][0]) / 2, (c[1] + ctrl[i + 1][1]) / 2)
                    for k in range(1, 9):
                        t = k / 8
                        x = (1 - t) ** 2 * seq[-1][0] + 2 * (1 - t) * t * c[0] + t * t * e[0]
                        y = (1 - t) ** 2 * seq[-1][1] + 2 * (1 - t) * t * c[1] + t * t * e[1]
                        cur.append((x, y))
                    seq.append(e)
            else:
                c1, c2, e = pts
                for k in range(1, 13):
                    t = k / 12
                    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * c1[0] + 3 * (1 - t) * t * t * c2[0] + t ** 3 * e[0]
                    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * c1[1] + 3 * (1 - t) * t * t * c2[1] + t ** 3 * e[1]
                    cur.append((x, y))
        elif op in ("closePath", "endPath"):
            if len(cur) > 2:
                rings.append(cur)
            cur = []
    # outer rings vs holes by orientation via containment
    polys = [Polygon(r).buffer(0) for r in rings]
    polys.sort(key=lambda p: -p.area)
    shape = None
    for p in polys:
        if shape is None:
            shape = p
        elif shape.contains(p.representative_point()) and shape.contains(p):
            shape = shape.difference(p)
        else:
            shape = shape.union(p)
    return shape, f["hmtx"][cmap[ord(ch)]][0] * sc


SLANT = None


def italic_angle():
    f = saira.font(900, 125, True)
    return -f["post"].italicAngle  # degrees, positive = leaning right


def to_d(geom, prec=2):
    def ring(c):
        pts = list(c.coords)[:-1]
        return "M" + " L".join(f"{x:.{prec}f} {y:.{prec}f}" for x, y in pts) + " Z"
    gs = geom.geoms if hasattr(geom, "geoms") else [geom]
    out = []
    for g in gs:
        if g.is_empty:
            continue
        out.append(ring(g.exterior))
        out += [ring(i) for i in g.interiors]
    return " ".join(out)


def fit(geoms, size=256, pad=24, cy_bias=-2):
    u = unary_union([g for g, _ in geoms])
    x0, y0, x1, y1 = u.bounds
    s = (size - 2 * pad) / max(x1 - x0, y1 - y0)
    ox = size / 2 - (x0 + x1) / 2 * s
    oy = size / 2 - (y0 + y1) / 2 * s + cy_bias
    return [(affinity.affine_transform(g, [s, 0, 0, s, ox, oy]), role) for g, role in geoms]


def svg(geoms, colors, bg=None, title="AKKI MEISTER"):
    b = f'<rect width="256" height="256" fill="{bg}"/>' if bg else ""
    body = "".join(f'<path fill="{colors[r]}" fill-rule="evenodd" d="{to_d(g)}"/>' for g, r in geoms if not g.is_empty)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>{title}</title>{b}{body}</svg>'


# ------------------------------------------------------------------ the fusion monogram
def fusion(overlap=0.0, slit=True):
    A, aw = glyph_poly("A")
    M, mw = glyph_poly("M")
    a_bounds = A.bounds
    # slide M left until it touches the A's right leg, then a bit more so they share ink
    M = affinity.translate(M, aw * 0.80 + overlap, 0)
    body = unary_union([A, M])
    if not slit:
        return [(body, "main")]
    x0, y0, x1, y1 = body.bounds
    k = math.tan(math.radians(italic_angle()))
    # horizontal speed slit at the A's crossbar height: a sheared parallelogram knife cut that
    # exits through the right side of the M and tapers to a point
    hgt = y1 - y0
    yc = y0 + hgt * 0.60
    th = hgt * 0.085
    cut = Polygon([(x0 - 50, yc - th / 2), (x1 + 60, yc - th / 2 - th * 0.15), (x1 + 60, yc + th / 2 - th * 0.15), (x0 - 50, yc + th / 2)])
    return [(body.difference(cut), "main")]


def fusion_bar():
    """fusion with the slit filled red, carried out to the left as a speed line"""
    A, aw = glyph_poly("A")
    M, mw = glyph_poly("M")
    M = affinity.translate(M, aw * 0.80, 0)
    body = unary_union([A, M])
    x0, y0, x1, y1 = body.bounds
    hgt = y1 - y0
    yc = y0 + hgt * 0.60
    th = hgt * 0.085
    gap = th * 0.45
    cut = Polygon([(x0 - 600, yc - th / 2 - gap), (x1 + 80, yc - th / 2 - gap), (x1 + 80, yc + th / 2 + gap), (x0 - 600, yc + th / 2 + gap)])
    # tapered speed line: thin at the far left, full height under the A
    th2 = th * 1.25
    line = Polygon([(x0 - hgt * 0.75, yc + th2 / 2), (x0 - hgt * 0.62, yc - th2 / 2), (x1 - hgt * 0.30, yc - th2 / 2), (x1 - hgt * 0.30 - th2 * 0.25, yc + th2 / 2)])
    return [(body.difference(cut), "main"), (line, "accent")]


def crest():
    """a sharp visor-shaped team badge, the fusion knocked out of it"""
    inner = fusion(slit=True)[0][0]
    x0, y0, x1, y1 = inner.bounds
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    W2, H2 = w * 0.5 + h * 0.62, h * 0.5 + h * 0.62
    c = h * 0.55
    shape = Polygon([(cx - W2 + c, cy - H2), (cx + W2, cy - H2), (cx + W2, cy + H2 - c), (cx + W2 - c, cy + H2), (cx - W2, cy + H2), (cx - W2, cy - H2 + c)])
    shape = affinity.skew(shape, xs=-12, origin=(cx, cy))
    ring = shape.difference(shape.buffer(-h * 0.075, join_style=2))
    field = shape.buffer(-h * 0.15, join_style=2)
    return [(ring, "main"), (field.difference(inner), "main")]


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    print("italic angle", italic_angle())
    variants = {
        "m1-fusion": fusion(),
        "m2-fusion-bar": fusion_bar(),
        "m3-crest": crest(),
    }
    for k, g in variants.items():
        fg = fit(g)
        open(OUT + f"{k}-black.svg", "w").write(svg(fg, {"main": NIGHT, "accent": NIGHT}, title=k))
        open(OUT + f"{k}-color.svg", "w").write(svg(fg, {"main": NIGHT, "accent": RED}, title=k))
        open(OUT + f"{k}-rev.svg", "w").write(svg(fg, {"main": ICE, "accent": RED}, bg=NIGHT, title=k))
    print("ok")
