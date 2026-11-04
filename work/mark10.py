"""AKKI MEISTER round 10: ///AM matrix. Rows = typeface the M comes from (and whose stem weight the
constructed square A matches); columns = A tip style. All upright glyphs sheared 12 degrees; the cut runs
through the speed bars only."""
import math, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity

OUT = "../round10/"
os.makedirs(OUT, exist_ok=True)
NM = r"C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/node_modules/"
NIGHT, ICE, RED = "#07080C", "#F3F4F6", "#E10A23"
ANG = 12
K = math.tan(math.radians(ANG))

FONTS = {
    "saira": ("Saira Expanded Bold", NM + "@fontsource-variable/saira/files/saira-latin-wdth-normal.woff2", {"wght": 750, "wdth": 125}),
    "chakra": ("Chakra Petch Bold", NM + "@fontsource/chakra-petch/files/chakra-petch-latin-700-normal.woff2", None),
    "titillium": ("Titillium Web Bold", NM + "@fontsource/titillium-web/files/titillium-web-latin-700-normal.woff2", None),
    "barlow": ("Barlow ExtraBold", NM + "@fontsource/barlow/files/barlow-latin-800-normal.woff2", None),
    "kanit": ("Kanit Bold", NM + "@fontsource/kanit/files/kanit-latin-700-normal.woff2", None),
    "oxanium": ("Oxanium ExtraBold", NM + "@fontsource/oxanium/files/oxanium-latin-800-normal.woff2", None),
}
TIPS = {"square": (0, 0), "chamfer-45": (0.20, 0.20), "chamfer-steep": (0.12, 0.30), "chamfer-shallow": (0.32, 0.12)}
_fc = {}


def load(key):
    if key not in _fc:
        _, path, axes = FONTS[key]
        f = TTFont(path)
        if axes:
            f = instantiateVariableFont(f, axes)
        _fc[key] = f
    return _fc[key]


def glyph(key, ch, size=1000):
    f = load(key)
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
        elif op == "qCurveTo":
            ctrl, end = list(args[:-1]), args[-1]
            p0 = cur[-1]
            for i, c in enumerate(ctrl):
                e = end if i == len(ctrl) - 1 else ((c[0] + ctrl[i + 1][0]) / 2, (c[1] + ctrl[i + 1][1]) / 2)
                for k in range(1, 9):
                    t = k / 8
                    cur.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * e[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * e[1]))
                p0 = e
        elif op == "curveTo":
            c1, c2, e = args
            p0 = cur[-1]
            for k in range(1, 13):
                t = k / 12
                cur.append(((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * c1[0] + 3 * (1 - t) * t * t * c2[0] + t ** 3 * e[0],
                            (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * c1[1] + 3 * (1 - t) * t * t * c2[1] + t ** 3 * e[1]))
        elif op in ("closePath", "endPath"):
            if len(cur) > 2:
                rings.append(cur)
            cur = []
    polys = sorted([Polygon(r).buffer(0) for r in rings], key=lambda p: -p.area)
    shape = None
    for p in polys:
        if shape is None:
            shape = p
        elif shape.contains(p):
            shape = shape.difference(p)
        else:
            shape = shape.union(p)
    return shape


def stem(M):
    x0, y0, x1, y1 = M.bounds
    seg = M.intersection(box(-1e5, y0 + (y1 - y0) * 0.85, 1e5, y0 + (y1 - y0) * 0.85 + 0.5))
    gs = sorted(list(seg.geoms) if hasattr(seg, "geoms") else [seg], key=lambda g: g.bounds[0])
    return gs[0].bounds[2] - gs[0].bounds[0]


def build(fkey, tip, gap=0.06, full=False):
    M = glyph(fkey, "M")
    x0, y0, x1, y1 = M.bounds
    M = affinity.translate(M, -x0, -y0)
    H = y1 - y0
    s = stem(M)
    sh = s * 0.86
    W = H * 0.80
    cb = H * 0.56                       # crossbar top
    cx, cy = TIPS[tip]
    c1, c2 = W * cx, H * cy
    outer = Polygon([(0, H), (0, c2), (c1, 0), (W, 0), (W, H)]) if c1 else box(0, 0, W, H)
    A = outer.difference(box(s, sh, W - s, cb)).difference(box(s, cb + sh, W - s, H + 1))
    if c1:   # keep the stroke weight even along the chamfer
        inner_cut = Polygon([(s, c2 + sh * 0.8), (c1 + s * 0.4, sh), (s, sh)])
        A = A.difference(inner_cut) if False else A
    A = affinity.skew(A, xs=-ANG, origin=(0, H))
    M = affinity.skew(M, xs=-ANG, origin=(0, H))
    # gap between A and M
    lo, hi = -W, W * 3
    for _ in range(50):
        mid = (lo + hi) / 2
        Mt = affinity.translate(M, mid, 0)
        if A.intersects(Mt) or A.distance(Mt) < gap * H:
            lo = mid
        else:
            hi = mid
    body = unary_union([A, affinity.translate(M, hi, 0)])
    # speed bars, cut at crossbar height
    bars, x = [], -H * 0.07
    for w in (0.13, 0.09, 0.06):
        ww = H * w
        x -= ww
        bars.append(Polygon([(x + H * K, 0), (x + ww + H * K, 0), (x + ww, H), (x, H)]))
        x -= H * 0.07
    yc, th = cb + sh / 2, H * 0.075
    knife = box(-1e5, yc - th / 2, 1e5, yc + th / 2)
    if full == "parts":
        return body, bars, yc, th, H
    if full:   # one uniform line through bars, A and M
        return unary_union([body, unary_union(bars)]).difference(knife)
    bars = unary_union(bars).difference(knife)
    return unary_union([body, bars])


def d_of(g):
    def ring(c):
        return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in list(c.coords)[:-1]) + " Z"
    gs = g.geoms if hasattr(g, "geoms") else [g]
    return " ".join(ring(p.exterior) + " " + " ".join(ring(i) for i in p.interiors) for p in gs if not p.is_empty)


def save(name, g, fg=NIGHT, bg=None):
    x0, y0, x1, y1 = g.bounds
    s = 220 / max(x1 - x0, y1 - y0)
    g = affinity.affine_transform(g, [s, 0, 0, s, 128 - (x0 + x1) / 2 * s, 128 - (y0 + y1) / 2 * s])
    b = f'<rect width="256" height="256" fill="{bg}"/>' if bg else ""
    open(OUT + name + ".svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>AKKI MEISTER {name}</title>{b}<path fill="{fg}" fill-rule="evenodd" d="{d_of(g)}"/></svg>')


if __name__ == "__main__":
    import sys
    if "partial" in sys.argv:
        for fk in ("barlow", "saira", "chakra"):
            for md in "abc":
                g = partial(fk, md)
                save(f"partial-{fk}-{md}", g)
                save(f"partial-{fk}-{md}-rev", g, ICE, NIGHT)
        print("partial ok")
        raise SystemExit
    if "full" in sys.argv:
        for fk in ("saira", "chakra", "titillium", "barlow"):
            g = build(fk, "square", full=True)
            save(f"full-{fk}", g)
            save(f"full-{fk}-rev", g, ICE, NIGHT)
        print("full ok")
        raise SystemExit
    for fk in FONTS:
        for tk in TIPS:
            save(f"{fk}-{tk}", build(fk, tk))
    print("ok", len(FONTS) * len(TIPS))


def bar_x(b, yc):
    seg = b.intersection(box(-1e5, yc - 0.1, 1e5, yc + 0.1)).bounds
    return seg[0], seg[2]


def partial(fkey, mode):
    """mode a: line starts halfway into the first bar. b: as a, and the bar next to the A is only half cut.
    c: line starts halfway into the second bar (first bar whole)."""
    body, bars, yc, th, H = build(fkey, "square", full="parts")
    thick, mid, thin = bars            # created right to left: thick (next to A), middle, thin (leftmost)
    kn = lambda x0, x1: box(x0, yc - th / 2, x1, yc + th / 2)
    t0, t1 = bar_x(thin, yc)
    m0, m1 = bar_x(mid, yc)
    k0, k1 = bar_x(thick, yc)
    allg = unary_union([body] + bars)
    if mode == "a":
        return allg.difference(kn((t0 + t1) / 2, 1e5))
    if mode == "b":
        return allg.difference(kn((t0 + t1) / 2, k0)).difference(kn((k0 + k1) / 2, k1 + 0.01)).difference(kn(k1, 1e5))
    if mode == "c":
        return allg.difference(kn((m0 + m1) / 2, 1e5))


def equal(fkey, ratio, gap=0.06):
    """A with top bar = upper crossbar = cut = lower crossbar, all thickness v; cut starts halfway into bar 1."""
    M = glyph(fkey, "M")
    x0, y0, x1, y1 = M.bounds
    M = affinity.translate(M, -x0, -y0)
    H = y1 - y0
    s = stem(M)
    v = s * ratio
    W = H * 0.80
    cb = H * 0.56 - 1.5 * v                      # crossbar block (3 bands) centred on 0.56 H
    A = box(0, 0, W, H).difference(box(s, v, W - s, cb)).difference(box(s, cb + 3 * v, W - s, H + 1))
    A = affinity.skew(A, xs=-ANG, origin=(0, H))
    M = affinity.skew(M, xs=-ANG, origin=(0, H))
    lo, hi = -W, W * 3
    for _ in range(50):
        mid = (lo + hi) / 2
        Mt = affinity.translate(M, mid, 0)
        if A.intersects(Mt) or A.distance(Mt) < gap * H:
            lo = mid
        else:
            hi = mid
    body = unary_union([A, affinity.translate(M, hi, 0)])
    bars, x = [], -H * 0.07
    for w in (0.13, 0.09, 0.06):
        ww = H * w
        x -= ww
        bars.append(Polygon([(x + H * K, 0), (x + ww + H * K, 0), (x + ww, H), (x, H)]))
        x -= H * 0.07
    yt, yb = cb + v, cb + 2 * v                   # the cut sits exactly in the middle band
    t0, t1 = bar_x(bars[2], (yt + yb) / 2)
    return unary_union([body] + bars).difference(box((t0 + t1) / 2, yt, 1e5, yb))


def build2(fkey, tip, gap=0.06):
    """consistent version: inner chamfer parallel to the outer one at even stroke weight, and the bar cut is
    exactly the A's crossbar band (same top and bottom), so the crossbar continues back through the bars."""
    M = glyph(fkey, "M")
    x0, y0, x1, y1 = M.bounds
    M = affinity.translate(M, -x0, -y0)
    H = y1 - y0
    s = stem(M)
    sh = s * 0.86
    W = H * 0.80
    cb = H * 0.56
    cx, cy = TIPS[tip]
    c1, c2 = W * cx, H * cy
    outer = Polygon([(0, H), (0, c2), (c1, 0), (W, 0), (W, H)]) if c1 else box(0, 0, W, H)
    counter = box(s, sh, W - s, cb)
    if c1:
        L = math.hypot(c1, c2)
        n = (c2 / L, c1 / L)                      # inward normal of the chamfer edge
        d = (s * c1 + sh * c2) / L * 0.98         # stroke across the chamfer, blended from stem and bar weights
        px, py = n[0] * d, c2 + n[1] * d
        ux, uy = c1 / L, -c2 / L                  # direction along the chamfer
        big = H * 10
        a = (px - ux * big, py - uy * big)
        b = (px + ux * big, py + uy * big)
        half = Polygon([a, b, (b[0] - n[0] * big, b[1] - n[1] * big), (a[0] - n[0] * big, a[1] - n[1] * big)])
        counter = counter.difference(half)
    A = outer.difference(counter).difference(box(s, cb + sh, W - s, H + 1))
    A = affinity.skew(A, xs=-ANG, origin=(0, H))
    M = affinity.skew(M, xs=-ANG, origin=(0, H))
    lo, hi = -W, W * 3
    for _ in range(50):
        mid = (lo + hi) / 2
        Mt = affinity.translate(M, mid, 0)
        if A.intersects(Mt) or A.distance(Mt) < gap * H:
            lo = mid
        else:
            hi = mid
    body = unary_union([A, affinity.translate(M, hi, 0)])
    bars, x = [], -H * 0.07
    for w in (0.13, 0.09, 0.06):
        ww = H * w
        x -= ww
        bars.append(Polygon([(x + H * K, 0), (x + ww + H * K, 0), (x + ww, H), (x, H)]))
        x -= H * 0.07
    bars = unary_union(bars).difference(box(-1e5, cb, 1e5, cb + sh))   # cut = crossbar band
    return unary_union([body, bars])


PHI = (1 + 5 ** 0.5) / 2


def build3(fkey="titillium", gap=0.06, bar_gap=None, widths=(0.13, 0.13 / PHI, 0.13 / PHI ** 2), cbar=0.618,
           aw=0.86002, chamfer=None, inktrap=False, red=False):
    """final family. crossbar band centred at cbar*H (golden section), bars in golden progression,
    bar spacing = A-M gap by default, bar cut = crossbar band."""
    M = glyph(fkey, "M")
    x0, y0, x1, y1 = M.bounds
    M = affinity.translate(M, -x0, -y0)
    H = y1 - y0
    s = stem(M)
    sh = s * 0.86
    W = H * aw
    cb = H * cbar - sh / 2
    if chamfer:
        c1, c2 = W * chamfer[0], H * chamfer[1]
        outer = Polygon([(0, H), (0, c2), (c1, 0), (W, 0), (W, H)])
    else:
        outer = box(0, 0, W, H)
    counter = box(s, sh, W - s, cb)
    if chamfer:
        L = math.hypot(c1, c2); n = (c2 / L, c1 / L); d = (s * c1 + sh * c2) / L * 0.98
        px, py = n[0] * d, c2 + n[1] * d; ux, uy = c1 / L, -c2 / L; big = H * 10
        a = (px - ux * big, py - uy * big); b = (px + ux * big, py + uy * big)
        counter = counter.difference(Polygon([a, b, (b[0] - n[0] * big, b[1] - n[1] * big), (a[0] - n[0] * big, a[1] - n[1] * big)]))
    A = outer.difference(counter).difference(box(s, cb + sh, W - s, H + 1))
    if inktrap:   # small notches where M's diagonals meet the stems, opened for small sizes
        pass
    A = affinity.skew(A, xs=-ANG, origin=(0, H))
    M = affinity.skew(M, xs=-ANG, origin=(0, H))
    lo, hi = -W, W * 3
    for _ in range(50):
        mid = (lo + hi) / 2
        Mt = affinity.translate(M, mid, 0)
        if A.intersects(Mt) or A.distance(Mt) < gap * H:
            lo = mid
        else:
            hi = mid
    Mf = affinity.translate(M, hi, 0)
    if inktrap:
        # a thin wedge into the M's inner V vertex
        mx0, my0, mx1, my1 = Mf.bounds
        seg = Mf.intersection(box(-1e5, H * 0.995, 1e5, H)).bounds
    body = unary_union([A, Mf])
    bg = (bar_gap if bar_gap is not None else gap) * H
    bars, x = [], -bg
    for w in widths:
        ww = H * w
        x -= ww
        bars.append(Polygon([(x + H * K, 0), (x + ww + H * K, 0), (x + ww, H), (x, H)]))
        x -= bg
    band = box(-1e5, cb, 1e5, cb + sh)
    bars = unary_union(bars).difference(band)
    g = unary_union([body, bars])
    if red:
        bx = min(b.bounds[0] for b in [bars] )
        return g, box(bx - H * 0.0, cb + sh * 0.25, -bg * 0.5, cb + sh * 0.75)
    return g, None


def custom_M(H, s, Wm, vy=0.80, vb=None):
    """M built from two stems and two diagonals, every stroke the same horizontal width s; flat-bottomed V."""
    vb = s if vb is None else vb
    xc = Wm / 2
    L = box(0, 0, s, H)
    R = box(Wm - s, 0, Wm, H)
    dl = Polygon([(0, 0), (s, 0), (xc + vb / 2, H * vy), (xc - vb / 2, H * vy)])
    dr = Polygon([(Wm - s, 0), (Wm, 0), (xc + vb / 2, H * vy), (xc - vb / 2, H * vy)])
    return unary_union([L, R, dl, dr])


def build4(fkey="titillium", gap=0.06, widths=(0.13, 0.13 / PHI, 0.13 / PHI ** 2), cbar=0.618, aw=0.86, vy=0.80, mw=None, chamfer=None, cutw=None, parts=False, bar_gap=None):
    """as build3, but the M is constructed: stems and diagonals equal width, solid joins (no slivers)."""
    Mg = glyph(fkey, "M")
    x0, y0, x1, y1 = Mg.bounds
    H = y1 - y0
    s = stem(affinity.translate(Mg, -x0, -y0))
    Wm = mw * H if mw else (x1 - x0)
    M = custom_M(H, s, Wm, vy)
    sh = s * 0.86
    W = H * aw
    cb = H * cbar - sh / 2
    if chamfer:
        c1, c2 = W * chamfer[0], H * chamfer[1]
        outer = Polygon([(0, H), (0, c2), (c1, 0), (W, 0), (W, H)])
    else:
        outer = box(0, 0, W, H)
    counter = box(s, sh, W - s, cb)
    if chamfer:
        Lh = math.hypot(c1, c2); n = (c2 / Lh, c1 / Lh); d = (s * c1 + sh * c2) / Lh * 0.98
        px, py = n[0] * d, c2 + n[1] * d; ux, uy = c1 / Lh, -c2 / Lh; big = H * 10
        a = (px - ux * big, py - uy * big); b = (px + ux * big, py + uy * big)
        counter = counter.difference(Polygon([a, b, (b[0] - n[0] * big, b[1] - n[1] * big), (a[0] - n[0] * big, a[1] - n[1] * big)]))
    A = outer.difference(counter).difference(box(s, cb + sh, W - s, H + 1))
    A = affinity.skew(A, xs=-ANG, origin=(0, H))
    M = affinity.skew(M, xs=-ANG, origin=(0, H))
    lo, hi = -W, W * 3
    for _ in range(50):
        mid = (lo + hi) / 2
        Mt = affinity.translate(M, mid, 0)
        if A.intersects(Mt) or A.distance(Mt) < gap * H:
            lo = mid
        else:
            hi = mid
    body = unary_union([A, affinity.translate(M, hi, 0)])
    bg = gap * H
    bars, x = [], -(bar_gap * H if bar_gap is not None else bg)
    for w in widths:
        ww = H * w
        x -= ww
        bars.append(Polygon([(x + H * K, 0), (x + ww + H * K, 0), (x + ww, H), (x, H)]))
        x -= bg
    if parts:
        yc, t = cb + sh / 2, (cutw or 0.035) * H
        knife = box(-1e5, yc - t / 2, 1e5, yc + t / 2)
        return body, [bb.difference(knife) for bb in bars], (yc, t, H)
    if cutw is None:
        bars = unary_union(bars).difference(box(-1e5, cb, 1e5, cb + sh))
    else:
        yc, t = cb + sh / 2, cutw * H
        bars = unary_union(bars).difference(box(-1e5, yc - t / 2, 1e5, yc + t / 2))
    return unary_union([body, bars])
