"""MEISTER — a constructed display typeface for AKKI MEISTER.

Every glyph is a set of centre-lines on a 7-unit cap height, drawn with a constant stroke,
mitred joins and 45-degree chamfered corners, then sheared forward by the brand angle (15 deg).
Output is filled outlines only (no font files, no live text)."""
import math

ANGLE = 15.0
H = 7.0          # cap height in units
C = 1.6          # chamfer size


# ------------------------------------------------------------------ outline maths
def _isect(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-9:
        return p2
    a, b = x1 * y2 - y1 * x2, x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)


def _off(p, q, d):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * d, dx / L * d
    return (p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny)


def _area(poly):
    return sum(poly[i - 1][0] * poly[i][1] - poly[i][0] * poly[i - 1][1] for i in range(len(poly))) / 2


def _orient(poly, positive=True):
    return poly if (_area(poly) > 0) == positive else poly[::-1]


def stroke_open(pts, t):
    # square caps: push both ends out by t/2
    def ext(a, b):
        dx, dy = a[0] - b[0], a[1] - b[1]
        L = math.hypot(dx, dy)
        return (a[0] + dx / L * t / 2, a[1] + dy / L * t / 2)
    pts = [ext(pts[0], pts[1])] + pts[1:-1] + [ext(pts[-1], pts[-2])]
    sides = []
    for sgn in (1, -1):
        segs = [_off(pts[i], pts[i + 1], sgn * t / 2) for i in range(len(pts) - 1)]
        out = [segs[0][0]]
        for i in range(len(segs) - 1):
            out += _join(segs[i], segs[i + 1], pts[i + 1], t)
        out.append(segs[-1][1])
        sides.append(out)
    return [_orient(sides[0] + sides[1][::-1], True)]


def _join(s1, s2, v, t, limit=1.25):
    """mitre join, or a bevel when the mitre would spike out past limit*t from the vertex"""
    q = _isect(*s1, *s2)
    if math.hypot(q[0] - v[0], q[1] - v[1]) > limit * t:
        return [s1[1], s2[0]]
    return [q]


def stroke_closed(pts, t):
    rings = []
    n = len(pts)
    for sgn in (1, -1):
        segs = [_off(pts[i], pts[(i + 1) % n], sgn * t / 2) for i in range(n)]
        ring = []
        for i in range(n):
            ring += _join(segs[i - 1], segs[i], pts[i], t)
        rings.append(ring)
    a, b = rings
    outer, inner = (a, b) if abs(_area(a)) > abs(_area(b)) else (b, a)
    return [_orient(outer, True), _orient(inner, False)]


def clip(poly, x0, x1, y0, y1):
    def cl(pts, inside, cut):
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

    def at_x(x):
        return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]))

    def at_y(y):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y)

    e = 1e-9
    for inside, cut in ((lambda p: p[0] >= x0 - e, at_x(x0)), (lambda p: p[0] <= x1 + e, at_x(x1)),
                        (lambda p: p[1] >= y0 - e, at_y(y0)), (lambda p: p[1] <= y1 + e, at_y(y1))):
        poly = cl(poly, inside, cut)
        if not poly:
            return []
    return poly


# ------------------------------------------------------------------ glyphs
WIDTHS = {"·": None, "M": 7.6, "W": 8.6, "I": None, "1": 3.6, " ": 3.0, ".": None, ":": None, "-": 4.0, "'": None, "/": 4.4, "+": 5.0}


def glyph(ch, t):
    """returns (width, [open polylines], [closed polylines]) in units, y down, cap 0..H"""
    W = WIDTHS.get(ch, 6.0) or t
    L, R, T, B = t / 2, W - t / 2, t / 2, H - t / 2
    M = H * 0.52
    X = W / 2
    c = max(C, 1.1 * t)
    k = max(c * 0.6, 0.95 * t)
    o, cl = [], []
    if ch == "A":
        o = [[(L, B), (L, T + c), (L + c, T), (R - c, T), (R, T + c), (R, B)], [(L, M + 0.25), (R, M + 0.25)]]
    elif ch == "B":
        o = [[(L, B), (L, T), (R - c, T), (R, T + c), (R, B - c), (R - c, B), (L, B)], [(L, M), (R - 0.4, M)]]
    elif ch == "C":
        o = [[(R, T), (L + c, T), (L, T + c), (L, B - c), (L + c, B), (R, B)]]
    elif ch == "D":
        cl = [[(L, T), (R - c, T), (R, T + c), (R, B - c), (R - c, B), (L, B)]]
    elif ch == "E":
        o = [[(R, T), (L, T), (L, B), (R, B)], [(L, M), (R - 0.9, M)]]
    elif ch == "F":
        o = [[(R, T), (L, T), (L, B)], [(L, M), (R - 0.9, M)]]
    elif ch == "G":
        o = [[(R, T), (L + c, T), (L, T + c), (L, B - c), (L + c, B), (R, B), (R, M), (X, M)]]
    elif ch == "H":
        o = [[(L, T), (L, B)], [(R, T), (R, B)], [(L, M), (R, M)]]
    elif ch == "I":
        o = [[(L, T), (L, B)]]
    elif ch == "J":
        o = [[(R, T), (R, B - c), (R - c, B), (L, B), (L, B - 1.8)]]
    elif ch == "K":
        o = [[(L, T), (L, B)], [(R + 0.4, T - 0.3), (L + 0.2, M)], [(L + 1.2, M - 0.75), (R + 0.4, B + 0.4)]]
    elif ch == "L":
        o = [[(L, T), (L, B), (R, B)]]
    elif ch == "M":
        o = [[(L, B), (L, T), (X, M + 0.6), (R, T), (R, B)]]
    elif ch == "N":
        o = [[(L, B), (L, T), (R, B), (R, T)]]
    elif ch in "O0":
        cl = [[(L + c, T), (R - c, T), (R, T + c), (R, B - c), (R - c, B), (L + c, B), (L, B - c), (L, T + c)]]
    elif ch == "P":
        o = [[(L, B), (L, T), (R - c, T), (R, T + c), (R, M), (L, M)]]
    elif ch == "Q":
        cl = [[(L + c, T), (R - c, T), (R, T + c), (R, B - c), (R - c, B), (L + c, B), (L, B - c), (L, T + c)]]
        o = [[(X + 0.6, B - 1.4), (R + 0.6, B + 0.6)]]
    elif ch == "R":
        o = [[(L, B), (L, T), (R - c, T), (R, T + c), (R, M), (L, M)], [(R - 1.9, M), (R, M + 1.9), (R, B)]]
    elif ch == "S":
        o = [[(R, T), (L + c, T), (L, T + c), (L, M), (R, M), (R, B - c), (R - c, B), (L, B)]]
    elif ch == "T":
        o = [[(0 + t / 2, T), (W - t / 2, T)], [(X, T), (X, B)]]
    elif ch == "U":
        o = [[(L, T), (L, B - c), (L + c, B), (R - c, B), (R, B - c), (R, T)]]
    elif ch == "V":
        o = [[(L, T - 1), (L, T), (X, B + 0.8), (R, T), (R, T - 1)]]
    elif ch == "W":
        o = [[(L, T), (L, B), (X, M), (R, B), (R, T)]]
    elif ch == "X":
        o = [[(L - 0.3, T - 0.3), (R + 0.3, B + 0.3)], [(R + 0.3, T - 0.3), (L - 0.3, B + 0.3)]]
    elif ch == "Y":
        o = [[(L - 0.2, T - 0.4), (X, M), (R + 0.2, T - 0.4)], [(X, M), (X, B)]]
    elif ch == "Z":
        o = [[(L, T), (R, T), (L, B), (R, B)]]
    elif ch == "1":
        o = [[(R - 2.2, T + 1.2), (R - c * 0.3, T), (R, T), (R, B)]]
    elif ch == "2":
        o = [[(L, T), (R - c, T), (R, T + c), (R, M), (L, M), (L, B), (R, B)]]
    elif ch == "3":
        o = [[(L, T), (R - c, T), (R, T + c), (R, B - c), (R - c, B), (L, B)], [(L + 1.2, M), (R, M)]]
    elif ch == "4":
        o = [[(L, T), (L, M + 0.6), (R, M + 0.6)], [(R, T), (R, B)]]
    elif ch == "5":
        o = [[(R, T), (L, T), (L, M), (R, M), (R, B - c), (R - c, B), (L, B)]]
    elif ch == "6":
        o = [[(R, T), (L + c, T), (L, T + c), (L, B - c), (L + c, B), (R - c, B), (R, B - c), (R, M), (L, M)]]
    elif ch == "7":
        o = [[(L, T), (R, T), (R, T + 0.6), (X - 0.4, B + 0.6)]]
    elif ch == "8":
        cl = [[(L + c, T), (R - c, T), (R, T + c), (R, B - c), (R - c, B), (L + c, B), (L, B - c), (L, T + c)]]
        o = [[(L, M), (R, M)]]
    elif ch == "9":
        o = [[(L, B), (R - c, B), (R, B - c), (R, T + c), (R - c, T), (L + c, T), (L, T + c), (L, M), (R, M)]]
    elif ch == ".":
        o = [[(L, B - t / 2), (L, B)]]
    elif ch == ":":
        o = [[(L, B - t / 2), (L, B)], [(L, M - 0.9 - t / 2), (L, M - 0.9)]]
    elif ch == "·":
        o = [[(L, M - t / 4), (L, M + t / 4)]]
    elif ch == "-":
        o = [[(L, M), (R, M)]]
    elif ch == "+":
        o = [[(L, M), (R, M)], [(X, M - 2), (X, M + 2)]]
    elif ch == "/":
        o = [[(L - 0.3, B + 0.3), (R + 0.3, T - 0.3)]]
    elif ch == "'":
        o = [[(L, T), (L, T + 1.6)]]
    return W, o, cl


def text_polys(s, t=1.35, track=1.0, angle=ANGLE, size=None):
    """polygons for a string, sheared, in units (origin at cap-top-left). returns (polys, width, height)"""
    k = math.tan(math.radians(angle))
    x, polys = 0.0, []
    for i, ch in enumerate(s.upper()):
        W, o, cl = glyph(ch, t)
        for p in o:
            for poly in stroke_open(p, t):
                poly = clip(poly, 0, W, 0, H)
                if poly:
                    polys.append([(px + x + (H - py) * k, py) for px, py in poly])
        for p in cl:
            for poly in stroke_closed(p, t):
                polys.append([(px + x + (H - py) * k, py) for px, py in poly])
        x += W + (track if ch != " " else 0)
    return polys, x - track + H * k, H


def to_d(polys, s=1.0, ox=0.0, oy=0.0):
    return " ".join("M" + " L".join(f"{px * s + ox:.2f} {py * s + oy:.2f}" for px, py in p) + " Z" for p in polys)


def text_svg_path(s, height, t=1.35, track=1.0, angle=ANGLE, x=0.0, y=0.0, fill="#fff", extra=""):
    """an SVG <path> of the text with its cap height = height px, top-left at (x, y)"""
    polys, w, _ = text_polys(s, t, track, angle)
    sc = height / H
    return f'<path fill="{fill}" {extra} d="{to_d(polys, sc, x, y)}"/>', w * sc


def text_svg(s, height, t=1.35, track=1.0, angle=ANGLE, fill="#fff", pad=0.0, style=""):
    """a standalone inline <svg> of the text, sized to its own width"""
    path, w = text_svg_path(s, height, t, track, angle, pad, pad, fill)
    return f'<svg width="{w + 2 * pad:.1f}" height="{height + 2 * pad:.1f}" viewBox="0 0 {w + 2 * pad:.1f} {height + 2 * pad:.1f}" style="overflow:visible;display:block;{style}">{path}</svg>'


if __name__ == "__main__":
    rows = [("AKKI MEISTER", 1.35, 1.0), ("ABCDEFGHIJKLM", 1.35, 1.0), ("NOPQRSTUVWXYZ", 1.35, 1.0), ("0123456789 P1 1:26.004", 1.35, 1.0),
            ("LIGHTS OUT - RACE DAY", 1.7, 0.8), ("MOTORSPORT PERFORMANCE", 0.55, 2.2)]
    body, y = "", 30
    for s, t, tr in rows:
        p, w = text_svg_path(s, 70, t, tr, x=30, y=y, fill="#111")
        body += p
        y += 110
    open("../round3/type-test.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1700 {y}" width="1700" height="{y}"><rect width="1700" height="{y}" fill="#f2f2f2"/>{body}</svg>')
    print("ok")
