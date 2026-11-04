"""AKKI MEISTER round 9: modular block monograms (Studio Loom-like) and single-stroke app marks (Grid Atlas-like)."""
import math, os
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
from shapely import affinity
import saira

OUT = "../round9/"
os.makedirs(OUT, exist_ok=True)
NIGHT, ICE, RED, STEEL, PAPER = "#07080C", "#F3F4F6", "#E10A23", "#8C93A3", "#ECEBE7"


def d_of(g):
    def ring(c):
        return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in list(c.coords)[:-1]) + " Z"
    gs = g.geoms if hasattr(g, "geoms") else [g]
    return " ".join(ring(p.exterior) + " " + " ".join(ring(i) for i in p.interiors) for p in gs if not p.is_empty)


def disc(cx, cy, r):
    return Point(cx, cy).buffer(r, 128)


# ------------------------------------------------------------------ modular letters in a 100x100 cell
def L_A(u=100, w=None):
    """arch A: a block with fully rounded top corners, a rounded counter and a gap between the legs"""
    w = w or u
    r = min(u, w) * 0.5
    outer = box(0, r, w, u).union(box(r, 0, w - r, u)).union(disc(r, r, r)).union(disc(w - r, r, r))
    cw, ch = min(w * 0.36, u * 0.40), u * 0.30
    cr = cw / 2
    counter = box(w / 2 - cw / 2, u * 0.26 + cr, w / 2 + cw / 2, u * 0.26 + ch).union(disc(w / 2, u * 0.26 + cr, cr))
    legs = box(w / 2 - cw / 2, u * 0.70, w / 2 + cw / 2, u + 1)
    return outer.difference(counter).difference(legs)


def L_m(u=100, w=None):
    """lowercase m from two humps with arched counters"""
    w = w or u
    r = w / 4
    g = unary_union([disc(r, r, r), disc(3 * r, r, r), box(0, r, w, u)])
    g = g.intersection(box(0, 0, w, u))
    for cx in (r, 3 * r):
        g = g.difference(unary_union([disc(cx, r * 1.05, r * .42), box(cx - r * .42, r * 1.05, cx + r * .42, u + 1)]))
    return g


def L_K(u=100):
    return box(0, 0, u, u).difference(Polygon([(u * .38, u * .5), (u + 1, -1), (u + 1, u + 1)])).difference(Polygon([(u * .42, -1), (u * .78, -1), (u * .40, u * .36)])).difference(Polygon([(u * .42, u + 1), (u * .78, u + 1), (u * .40, u * .64)]))


def L_I(u=100):
    return box(u * .30, 0, u * .70, u)


def L_M(u=100):
    return box(0, 0, u, u).difference(Polygon([(u * .26, -1), (u * .74, -1), (u * .5, u * .5)])).difference(box(u * .26, u * .62, u * .74, u + 1)).union(Polygon([(u * .26, u * .62), (u * .5, u * .5), (u * .74, u * .62)]).difference(box(-1, -1, u + 1, u * .62)))


def cell(g, x, y):
    return affinity.translate(g, x, y)


def svg_wrap(body, vb, bg=None, w=600):
    b = f'<rect x="-999" y="-999" width="9999" height="9999" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}">{b}{body}</svg>'


def label(text, x, y, h, col, wght=600, track=0.18, anchor_w=None):
    d, w, cap = saira.outline(text, 100, wght, 125, False, track)
    s = h / cap
    return f'<path fill="{col}" transform="translate({x} {y}) scale({s:.4f})" d="{d}"/>', w * s


# ---- Block series ------------------------------------------------------
def block_am(fg, bg, frame=True, gap=8):
    """A over m in a square, a thin frame on top/right with MEISTER above"""
    u = 100
    A = L_A(u, 2 * u)
    m = cell(L_m(u, 2 * u), 0, u + gap)
    g = unary_union([A, m])
    body = f'<path fill="{fg}" fill-rule="evenodd" d="{d_of(g)}"/>'
    if frame:
        body += f'<path d="M -22 -26 H 222 V 222" fill="none" stroke="{fg}" stroke-width="2.4"/>'
        p, w = label("AKKI MEISTER", -22, -38, 13, fg)
        body += p
    return svg_wrap(body, "-40 -70 280 310", bg)


def block_akki(fg, bg):
    """AK / KI in a 2x2 grid; MEISTER set wide below"""
    u, gap = 100, 10
    g = unary_union([cell(L_A(u), 0, 0), cell(L_K(u), u + gap, 0), cell(L_K(u), 0, u + gap), cell(L_I(u), u + gap, u + gap)])
    body = f'<path fill="{fg}" fill-rule="evenodd" d="{d_of(g)}"/>'
    body += f'<path d="M -20 -20 H 230 V 230" fill="none" stroke="{fg}" stroke-width="2.4"/>'
    p, w = label("MEISTER", 0, 268, 22, fg, 700, 0.38)
    body += p
    return svg_wrap(body, "-40 -40 290 330", bg)


def block_knock(fg, bg):
    """solid square, AM knocked out as the modular A and m, a red notch at the m's foot"""
    u = 100
    sq = box(-20, -20, 220, 2 * u + 30)
    A = L_A(u, 2 * u)
    m = cell(L_m(u, 2 * u), 0, u + 10)
    g = sq.difference(unary_union([A, m]))
    body = f'<path fill="{fg}" fill-rule="evenodd" d="{d_of(g)}"/><rect x="200" y="{2 * u + 22}" width="20" height="8" fill="{RED}"/>'
    return svg_wrap(body, "-40 -40 280 290", bg)


# ---- Stroke / app-tile series ----------------------------------------------
def checker(x, y, s, cols, rows, col, fade=True):
    out = ""
    for c in range(cols):
        for r in range(rows):
            if (c + r) % 2 == 0:
                op = 1 - c / (cols + .5) if fade else 1
                out += f'<rect x="{x + c * s:.1f}" y="{y + r * s:.1f}" width="{s}" height="{s}" fill="{col}" opacity="{op:.2f}" transform="skewX(-12)"/>'
    return out


def tile(inner, size=160, r=36, bg="#14161E"):
    return (f'<rect x="0" y="0" width="{size}" height="{size}" rx="{r}" fill="{bg}"/>'
            f'<rect x="0.5" y="0.5" width="{size - 1}" height="{size - 1}" rx="{r}" fill="none" stroke="rgba(255,255,255,.08)"/>{inner}')


def stroke_a(col, acc):
    """one thick italic stroke draws a flat-topped A; its red crossbar runs out the right side into a chequered trail"""
    p = "M40 122 L58 42 L98 42 L80 122"
    return (f'<path d="{p}" fill="none" stroke="{col}" stroke-width="16" stroke-linejoin="miter" stroke-linecap="butt"/>'
            f'<path d="M50 92 L112 92" fill="none" stroke="{acc}" stroke-width="12"/>' + checker(134, 86, 8, 3, 2, acc))


def stroke_am(col, acc):
    """flat-topped A and M drawn in the same thick stroke; red crossbar into a chequered trail"""
    a = "M20 122 L36 42 L66 42 L50 122"
    m = "M66 122 L82 42 L96 42 L106 84 L126 42 L140 42 L124 122"
    return (f'<path d="{a}" fill="none" stroke="{col}" stroke-width="13" stroke-linejoin="miter" stroke-linecap="butt"/>'
            f'<path d="{m}" fill="none" stroke="{col}" stroke-width="13" stroke-linejoin="miter" stroke-miterlimit="3" stroke-linecap="butt"/>'
            f'<path d="M28 96 L58 96" stroke="{acc}" stroke-width="10"/>' + checker(146, 102, 6, 2, 2, acc, False))


def app_lockup(mark, title_lines, fg, bg, sub=None):
    t1, w1 = label(title_lines[0], 0, 0, 34, fg, 300, 0.20)
    t2, w2 = label(title_lines[1], 0, 0, 34, fg, 300, 0.20)
    ws = label(sub, 0, 0, 10, STEEL, 600, 0.42)[1] if sub else 0
    W = max(w1, w2, ws)
    body = f'<g transform="translate({(W - 160) / 2:.1f} 0)">{tile(mark)}</g>'
    body += f'<g transform="translate({(W - w1) / 2:.1f} 210)">{t1}</g><g transform="translate({(W - w2) / 2:.1f} 262)">{t2}</g>'
    if sub:
        s, ws = label(sub, 0, 0, 10, STEEL, 600, 0.42)
        body += f'<g transform="translate({(W - ws) / 2:.1f} 300)">{s}</g>'
    return svg_wrap(body, f"-40 -30 {W + 80:.0f} 360", bg)


if __name__ == "__main__":
    files = {
        "b1-block-am-light": block_am(NIGHT, PAPER),
        "b2-block-am-dark": block_am(ICE, NIGHT),
        "b3-block-akki": block_akki(NIGHT, PAPER),
        "b4-block-knock": block_knock(NIGHT, PAPER),
        "g1-stroke-a": app_lockup(stroke_a(ICE, RED), ("AKKI", "MEISTER"), ICE, "#000", "MOTORSPORT · PERFORMANCE"),
        "g2-stroke-am": app_lockup(stroke_am(ICE, RED), ("AKKI", "MEISTER"), ICE, "#000", "MOTORSPORT · PERFORMANCE"),
        "g3-stroke-a-red": app_lockup(stroke_a(ICE, "#07080C").replace('fill="#07080C"', 'fill="#07080C"'), ("AKKI", "MEISTER"), ICE, "#000", "MOTORSPORT · PERFORMANCE").replace('fill="#14161E"', f'fill="{RED}"'),
    }
    for k, v in files.items():
        open(OUT + k + ".svg", "w").write(v)
    print("ok")
