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
    """TWIN PEAKS: two sharp peaks fused at a shared centre foot read as an M; only the first carries a crossbar, an A."""
    # horizontal stroke 34, legs rise 60 over 144; numbers worked out so both counters peak at the same height
    outline = [(0, B), (60, T), (108, 171), (156, T), (216, B), (182, B), (156, 137.6), (130, B), (86, B), (60, 137.6), (34, B)]
    y1, y2 = 166.0, 182.0
    cx = lambda y, side: 60 + side * (60 * (y - 137.6) / 144 * 2.4)   # inside the first counter
    lx = lambda y: 34 + 60 * (B - y) / 144
    rx = lambda y: 86 - 60 * (B - y) / 144
    bar = [(lx(y1), y1), (rx(y1), y1), (rx(y2), y2), (lx(y2), y2)]
    return [(outline, "main"), (bar, "accent")]


def concept_b():
    """CUT BLOCK: a solid M block; the notch under its centre is an A, cut out of the M."""
    W0 = 176.0
    m = W0 / 2
    tv = T + 0.38 * H                       # bottom of the top V
    ta = tv + 28                            # apex of the A-shaped notch
    outline = [(0, T), (m - 34, T), (m, tv), (m + 34, T), (W0, T), (W0, B), (m + 52, B), (m, ta), (m - 52, B), (0, B)]
    # the A's crossbar, sitting inside the notch
    def nx(y, side):
        return m + side * 52 * (y - ta) / (B - ta)
    y1, y2 = B - 52, B - 32
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
    w = LEAN * (H - 40)                     # right leg lands exactly vertical after the lean
    ha = math.atan2(w, H - 40)
    ex = 30 * w / (H - 40)
    a_pts = [(84 - w - ex, B - 18 + 30), (84, T + 22 + (t / 2) / math.sin(ha)), (84 + w + ex, B - 18 + 30)]
    a = clip_y(thick(a_pts, t), T + 22, B - 18)
    # M as |\/|
    mx0, mx1 = 128.0, 196.0
    vx = mx0 + t / 2 + LEAN * (T + 0.62 * H - (T + 22))   # first diagonal lands vertical after the lean
    m_pts = [(mx0 + t / 2, B + 30), (mx0 + t / 2, T + 22), (vx, T + 0.62 * H), (mx1 - t / 2, T + 22), (mx1 - t / 2, B + 30)]
    m = clip_y(thick(m_pts, t), T + 22, B - 18)
    bars = [[(x, T), (x + w, T), (x + w, B), (x, B)] for x, w in ((-34, 4), (-24, 7), (-11, 11))]
    return [(tile, "tile"), (a, "hole"), (m, "hole")] + [(b, "accent") for b in bars]


def concept_e():
    """SPEED-LINE A: an open A whose crossbar fires out to the left as a long speed line, then the M."""
    t = 28.0
    w = LEAN * H                            # right leg lands exactly vertical after the lean
    ha = math.atan2(w, H)
    ty = apex_y(t, ha) - 1.5
    a_pts = [(80 - w * 1.3, B + H * 0.3), (80, ty), (80 + w * 1.3, B + H * 0.3)]
    a = clip_y(thick(a_pts, t), T - 1.5, B)
    y1, y2 = T + 0.64 * H, T + 0.64 * H + 16
    xr = lambda y: 80 + w * (y - ty) / (B - ty)
    speed = [(-46, y1), (xr(y1), y1), (xr(y2), y2), (-46, y2)]
    mx0, mx1 = 132.0, 220.0
    vx = mx0 + t / 2 + LEAN * (0.66 * H)               # first diagonal lands vertical after the lean
    m_pts = [(mx0 + t / 2, B + 40), (mx0 + t / 2, T), (vx, T + 0.66 * H), (mx1 - t / 2, T), (mx1 - t / 2, B + 40)]
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
    """concept C, one stroked racing line: a tall round-apex A, then two lower round humps (an m).
    The A's crossbar is an orange kerb. Built pre-shear, then sheared like the others."""
    k = LEAN
    t = 26
    S = lambda x, y: (x + (B - y) * k, y)
    def P(x, y):
        X, Y = S(x, y)
        return f"{X:.2f} {Y:.2f}"
    def hump(x0, x1, ytop):
        # up the left side, round top (two cubic quarter-ish arcs), down to the baseline
        r = (x1 - x0) / 2
        cx = x0 + r
        return (f" L{P(x0, ytop + r)} C{P(x0, ytop + r * 0.45)} {P(cx - r * 0.55, ytop)} {P(cx, ytop)}"
                f" C{P(cx + r * 0.55, ytop)} {P(x1, ytop + r * 0.45)} {P(x1, ytop + r)} L{P(x1, B)}")
    # A: legs 0..64 tall to T; m: two humps 64..124 and 124..184 to T+54
    d = f"M{P(0, B)}" + hump(0, 64, T) + f" M{P(64, B)}" + hump(64, 124, T + 54)[0:0] + hump(64, 124, T + 54) + hump(124, 184, T + 54)
    d = d.replace(f" M{P(64, B)}", "")  # one continuous line: the A's right leg is the m's first stem
    kerb = f"M{P(-8, T + 0.66 * H)} L{P(72, T + 0.66 * H)}"
    bgr = f'<rect width="256" height="256" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>{title}</title>{bgr}'
            f'<g transform="translate(20 4)"><path d="{d}" fill="none" stroke="{color_main}" stroke-width="{t}" stroke-linejoin="round" stroke-linecap="butt"/>'
            f'<path d="{kerb}" fill="none" stroke="{color_accent}" stroke-width="15" stroke-linecap="butt"/></g></svg>')


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
