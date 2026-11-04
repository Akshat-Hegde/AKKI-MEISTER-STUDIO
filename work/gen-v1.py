"""AKKI MEISTER logo concepts. Every mark is built from exact geometry (no fonts in the symbols),
then sheared 20 degrees forward, the same lean as Akshat's AH speed bars.

Writes black-on-white symbols, lockups with a constructed wordmark, and colour versions."""
import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ORANGE, INK, WHITE = "#FF5A1F", "#0B0B0C", "#FFFFFF"
LEAN = math.tan(math.radians(20))
T, B = 56.0, 200.0           # letter zone, pre-shear
H = B - T


# ---------------------------------------------------------------- geometry
def shear(pts, k=LEAN, base=B):
    return [(x + (base - y) * k, y) for x, y in pts]


def line_isect(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-9:
        return p2
    a, b = x1 * y2 - y1 * x2, x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)


def offset_seg(p, q, d):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * d, dx / L * d
    return (p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny)


def thick(points, t):
    """outline of a polyline of width t with mitred joins (butt ends, trimmed later by clip)"""
    sides = []
    for sgn in (1, -1):
        segs = [offset_seg(points[i], points[i + 1], sgn * t / 2) for i in range(len(points) - 1)]
        out = [segs[0][0]]
        for i in range(len(segs) - 1):
            out.append(line_isect(segs[i][0], segs[i][1], segs[i + 1][0], segs[i + 1][1]))
        out.append(segs[-1][1])
        sides.append(out)
    return sides[0] + sides[1][::-1]


def clip_y(poly, ymin, ymax):
    """Sutherland-Hodgman against two horizontal half-planes: flat tops and flat feet"""
    def clip(pts, inside, cut):
        out = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia:
                    out.append(cut(a, b))
                out.append(b)
            elif ia:
                out.append(cut(a, b))
        return out

    def at_y(y):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y)

    poly = clip(poly, lambda p: p[1] >= ymin - 1e-9, at_y(ymin))
    return clip(poly, lambda p: p[1] <= ymax + 1e-9, at_y(ymax))


def apex_y(t, half_angle):
    """centre-line apex height so the outer mitre point lands exactly on T"""
    return T + (t / 2) / math.sin(half_angle)


def d_of(poly):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in poly) + " Z"


# ---------------------------------------------------------------- concepts
# each returns a list of (path_d, role) with role in {"main", "accent", "tile"}; x pre-shear, y in [T, B]

def concept_a():
    """TWIN PEAKS: one mitred stroke draws two peaks, an M; only the first peak carries a crossbar, an A."""
    t, w = 30.0, 46.0
    ha = math.atan2(w, H)
    ty = apex_y(t, ha) - 1.5               # tiny overshoot above T
    V = T + 0.60 * H
    pts = [(0, B + 40), (w, ty), (2 * w, V), (3 * w, ty), (4 * w, B + 40)]
    # extend feet below B along the leg direction, then clip flat
    (x0, y0), (x1, y1) = pts[1], (0, B)
    pts[0] = (x1 - (x0 - x1) * 0.3, B + (B - y0) * 0.3)
    (x3, y3), (x4, y4) = pts[3], (4 * w, B)
    pts[4] = (x4 + (x4 - x3) * 0.3, B + (B - y3) * 0.3)
    body = clip_y(thick(pts, t), T - 1.5, B)
    # crossbar between the centre lines of peak 1, hidden ends inside the legs
    y1, y2 = T + 0.66 * H, T + 0.66 * H + 22
    xl = lambda y: w * (B - y) / (B - ty) * 1.0
    xr = lambda y: w + w * (y - ty) / (V - ty)
    bar = [(xl(y1), y1), (xr(y1), y1), (xr(y2), y2), (xl(y2), y2)]
    return [(body, "main"), (bar, "accent")]


def concept_b():
    """CUT BLOCK: a solid M block; the notch under its centre is an A, cut out of the M."""
    W0 = 176.0
    m = W0 / 2
    tv = T + 0.48 * H                       # bottom of the top V
    ta = tv + 22                            # apex of the A-shaped notch
    outline = [(0, T), (m - 30, T), (m, tv), (m + 30, T), (W0, T), (W0, B), (m + 46, B), (m, ta), (m - 46, B), (0, B)]
    # the A's crossbar, sitting inside the notch
    def nx(y, side):
        return m + side * 46 * (y - ta) / (B - ta)
    y1, y2 = B - 44, B - 28
    bar = [(nx(y1, -1) - 0.5, y1), (nx(y1, 1) + 0.5, y1), (nx(y2, 1) + 0.5, y2), (nx(y2, -1) - 0.5, y2)]
    return [(outline, "main"), (bar, "accent")]


def concept_c():
    """HAIRPIN: the A is a racing line through a hairpin (round apex); the line runs on and becomes the M.
    The A's crossbar is an orange kerb."""
    return "stroke"   # built as a stroked path below (round geometry), flagged in the audit


def concept_d():
    """GRID SLOT: an orange tile cut like a grid-box marker; A and M knocked out, speed bars trailing."""
    tile = [(18, T), (220, T), (220, B), (18, B)]
    t = 22.0
    # A (open, no bar) inside the tile
    ha = math.atan2(30, H - 44)
    a_pts = [(52, B - 18 + 30), (82, T + 22 + (t / 2) / math.sin(ha)), (112, B - 18 + 30)]
    a = clip_y(thick(a_pts, t), T + 22, B - 18)
    # M as |\/|
    mx0, mx1 = 128.0, 196.0
    m_pts = [(mx0 + t / 2, B + 30), (mx0 + t / 2, T + 22), ((mx0 + mx1) / 2, T + 0.62 * H), (mx1 - t / 2, T + 22), (mx1 - t / 2, B + 30)]
    m = clip_y(thick(m_pts, t), T + 22, B - 18)
    bars = [[(x, T), (x + w, T), (x + w, B), (x, B)] for x, w in ((-34, 4), (-24, 7), (-11, 11))]
    return [(tile, "tile"), (a, "hole"), (m, "hole")] + [(b, "accent") for b in bars]


def concept_e():
    """SPEED-LINE A: an open A whose crossbar fires out to the left as a long speed line, then the M."""
    t = 28.0
    ha = math.atan2(40, H)
    ty = apex_y(t, ha) - 1.5
    a_pts = [(40 - 40 * 0.3, B + H * 0.3), (80, ty), (120 + 40 * 0.3, B + H * 0.3)]
    a = clip_y(thick(a_pts, t), T - 1.5, B)
    y1, y2 = T + 0.64 * H, T + 0.64 * H + 16
    xr = lambda y: 80 + 40 * (y - ty) / (B - ty)
    speed = [(-46, y1), (xr(y1), y1), (xr(y2), y2), (-46, y2)]
    mx0, mx1 = 132.0, 220.0
    m_pts = [(mx0 + t / 2, B + 40), (mx0 + t / 2, T), ((mx0 + mx1) / 2, T + 0.66 * H), (mx1 - t / 2, T), (mx1 - t / 2, B + 40)]
    m = clip_y(thick(m_pts, t), T, B)
    return [(a, "main"), (m, "main"), (speed, "accent")]


# ---------------------------------------------------------------- SVG writers
def fit(parts, box=212.0, cx=128.0, cy=126.0):
    """shear, then scale/centre the whole mark into the 256 canvas (centred slightly above middle)"""
    sh = [(shear(p), r) for p, r in parts]
    xs = [x for p, _ in sh for x, _ in p]
    ys = [y for p, _ in sh for _, y in p]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = box / max(w, h)
    ox, oy = cx - (min(xs) + w / 2) * s, cy - (min(ys) + h / 2) * s
    return [([(x * s + ox, y * s + oy) for x, y in p], r) for p, r in sh], s, (ox, oy)


def svg_symbol(parts, colors, title):
    """colors: role -> fill. 'hole' polygons are cut out of the preceding 'tile' with evenodd."""
    body = []
    tile = [p for p, r in parts if r == "tile"]
    holes = [p for p, r in parts if r == "hole"]
    if tile:
        body.append(f'<path fill="{colors["tile"]}" fill-rule="evenodd" d="{" ".join(d_of(p) for p in tile + holes)}"/>')
    for role in ("main", "accent"):
        ps = [p for p, r in parts if r == role]
        if ps:
            body.append(f'<path fill="{colors[role]}" d="{" ".join(d_of(p) for p in ps)}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>{title}</title>{"".join(body)}</svg>'


def hairpin_svg(color_main, color_accent, title, bg=None):
    """concept C, drawn as a stroked path: tall round-apex A, then a lower round M hump; orange kerb."""
    # pre-shear centre line (stroke width 28): A up to a round apex, down, into a lower hump, down
    k = LEAN
    S = lambda x, y: (x + (B - y) * k, y)
    t = 28
    r1, r2 = 30, 24
    # points before shear
    p = [(0, B), (48 - r1, T + r1), (48 + r1, T + r1), (110, B - 10), (150 - r2, T + 52 + r2), (150 + r2, T + 52 + r2), (196, B)]
    # build path with straight legs and round tops (arcs approximated by cubic after shear)
    def P(x, y):
        X, Y = S(x, y)
        return f"{X:.2f} {Y:.2f}"
    a1 = (48, T + r1)
    a2 = (150, T + 52 + r2)
    d = (f"M{P(0 + 12, B)} L{P(a1[0] - r1, a1[1])} C{P(a1[0] - r1, a1[1] - r1 * 0.552)} {P(a1[0] - r1 * 0.552, a1[1] - r1)} {P(a1[0], a1[1] - r1)} "
         f"C{P(a1[0] + r1 * 0.552, a1[1] - r1)} {P(a1[0] + r1, a1[1] - r1 * 0.552)} {P(a1[0] + r1, a1[1])} "
         f"L{P(a1[0] + r1, B - 34)} C{P(a1[0] + r1, B - 34 + 30)} {P(a2[0] - r2, B - 34 + 30)} {P(a2[0] - r2, B - 40)} "
         f"L{P(a2[0] - r2, a2[1])} C{P(a2[0] - r2, a2[1] - r2 * 0.552)} {P(a2[0] - r2 * 0.552, a2[1] - r2)} {P(a2[0], a2[1] - r2)} "
         f"C{P(a2[0] + r2 * 0.552, a2[1] - r2)} {P(a2[0] + r2, a2[1] - r2 * 0.552)} {P(a2[0] + r2, a2[1])} L{P(a2[0] + r2, B)}")
    kerb = f"M{P(a1[0] - r1 - 6, T + 0.62 * H)} L{P(a1[0] + r1 + 6, T + 0.62 * H)}"
    # centre into the canvas: shear width ≈ 200+52; translate
    g = '<g transform="translate(6 2)">'
    bgr = f'<rect width="256" height="256" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>{title}</title>{bgr}{g}'
            f'<path d="{d}" fill="none" stroke="{color_main}" stroke-width="{t}" stroke-linejoin="round" stroke-linecap="butt"/>'
            f'<path d="{kerb}" fill="none" stroke="{color_accent}" stroke-width="16" stroke-linecap="butt"/></g></svg>')


# ---------------------------------------------------------------- wordmark from Archivo outlines
_font = None


def wordmark(text, size, wght=800, wdth=125, track=0.0, oblique=12.0):
    """returns (path_d, width) for text set in Archivo, outlined, with an oblique shear"""
    global _font
    key = (wght, wdth)
    if _font is None:
        _font = {}
    if key not in _font:
        f = TTFont(r"C:/Users/admin/Akki-Portfolio-main/3d_portfolio/node_modules/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2")
        _font[key] = instantiateVariableFont(f, {"wght": wght, "wdth": wdth})
    f = _font[key]
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    sc = size / upm
    k = math.tan(math.radians(oblique))
    pen = SVGPathPen(gs)
    x = 0.0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        tp = TransformPen(pen, (sc, 0, k * sc, -sc, x, 0))  # flip y, shear forward
        gs[g].draw(tp)
        x += hmtx[g][0] * sc + track * size
    return pen.getCommands(), x - track * size


def lockup(symbol_inner, title, color_word=INK, color_tag="#6B6762", accent=ORANGE):
    """horizontal lockup: symbol (256) + wordmark; height 256"""
    w1, w1w = wordmark("AKKI MEISTER", 62, 800, 125, 0.01)
    w2, w2w = wordmark("MOTORSPORT & PERFORMANCE", 17.5, 600, 125, 0.22, oblique=0)
    x0 = 286
    width = x0 + max(w1w, w2w) + 24
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} 256"><title>{title}</title>'
            f'<g>{symbol_inner}</g>'
            f'<path fill="{color_word}" transform="translate({x0} 142)" d="{w1}"/>'
            f'<rect x="{x0 + 4}" y="160" width="40" height="5" fill="{accent}"/>'
            f'<path fill="{color_tag}" transform="translate({x0 + 54} 168)" d="{w2}"/></svg>')


def inner(svg):
    return svg[svg.index("</title>") + 8: svg.rindex("</svg>")]


if __name__ == "__main__":
    import os
    os.makedirs("../concepts", exist_ok=True)
    out = "../concepts/"
    CONCEPTS = {"a": concept_a(), "b": concept_b(), "d": concept_d(), "e": concept_e()}
    names = {"a": "Twin Peaks", "b": "Cut Block", "c": "Hairpin", "d": "Grid Slot", "e": "Speed-Line A"}
    for k, parts in CONCEPTS.items():
        fp, _, _ = fit(parts)
        black = svg_symbol(fp, {"main": INK, "accent": INK, "tile": INK}, f"AKKI MEISTER {names[k]}")
        color = svg_symbol(fp, {"main": INK, "accent": ORANGE, "tile": ORANGE}, f"AKKI MEISTER {names[k]} colour")
        open(out + f"{k}-symbol.svg", "w").write(black)
        open(out + f"{k}-symbol-color.svg", "w").write(color)
        open(out + f"{k}-lockup.svg", "w").write(lockup(inner(black), f"AKKI MEISTER {names[k]} lockup", accent=INK))
        open(out + f"{k}-lockup-color.svg", "w").write(lockup(inner(color), f"AKKI MEISTER {names[k]} lockup colour"))
    c_black = hairpin_svg(INK, INK, "AKKI MEISTER Hairpin")
    c_color = hairpin_svg(INK, ORANGE, "AKKI MEISTER Hairpin colour")
    open(out + "c-symbol.svg", "w").write(c_black)
    open(out + "c-symbol-color.svg", "w").write(c_color)
    open(out + "c-lockup.svg", "w").write(lockup(inner(c_black), "AKKI MEISTER Hairpin lockup", accent=INK))
    open(out + "c-lockup-color.svg", "w").write(lockup(inner(c_color), "AKKI MEISTER Hairpin lockup colour"))
    print("written")
