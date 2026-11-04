"""Logo-creation breakdown post (1080x1350): golden-ratio construction over the ///AM."""
import math, os, shutil
import launch as L
from launch import mark, kicker, mono, NIGHT, ICE, BLUE, STEEL, K, MW, MH

SKY = "#5B7BFF"
GOLD = "#C8A96A"
PW, PH = 1080, 1350
PHI = (1 + 5 ** .5) / 2


def golden(x, y, w, h, steps=9):
    """golden-rectangle subdivision + spiral arcs (mark units)"""
    sq, arcs = [], []
    d = 0
    for _ in range(steps):
        if d == 0:     # square on the left
            s = h; sq.append((x, y, s)); arcs.append(f"M{x} {y + s} A{s} {s} 0 0 1 {x + s} {y}"); x += s; w -= s
        elif d == 1:   # square on the top
            s = w; sq.append((x, y, s)); arcs.append(f"M{x} {y} A{s} {s} 0 0 1 {x + s} {y + s}"); y += s; h -= s
        elif d == 2:   # square on the right
            s = h; sq.append((x + w - s, y, s)); arcs.append(f"M{x + w} {y} A{s} {s} 0 0 1 {x + w - s} {y + s}"); w -= s
        else:          # square on the bottom
            s = w; sq.append((x, y + h - s, s)); arcs.append(f"M{x + w} {y + h} A{s} {s} 0 0 1 {x} {y + h - s}"); h -= s
        d = (d + 1) % 4
    return sq, arcs


def post():
    s = 880 / MW
    mx, my = 100, 500
    X = lambda u: mx + u * s
    Y = lambda v: my + v * s
    sw = 1 / s
    # 1) the mark = one 100×100 square + a golden rectangle (161.8×100)
    sq0 = f'<rect x="0" y="0" width="100" height="100" fill="none" stroke="{GOLD}" stroke-width="{sw}" stroke-opacity=".2"/>'
    circ0 = f'<circle cx="50" cy="50" r="50" fill="none" stroke="{GOLD}" stroke-width="{sw}" stroke-opacity=".12"/>'
    sqs, arcs = golden(100, 0, 161.8, 100)
    gq = "".join(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c:.2f}" height="{c:.2f}" fill="none" stroke="{GOLD}" stroke-width="{sw}" stroke-opacity=".16"/>' for a, b, c in sqs)
    spiral = f'<path d="{" ".join(arcs)}" fill="none" stroke="{GOLD}" stroke-width="{1.3 * sw}" stroke-opacity=".45"/>'
    circles = "".join(f'<circle cx="{a + c / 2:.2f}" cy="{b + c / 2:.2f}" r="{c / 2:.2f}" fill="none" stroke="{SKY}" stroke-width="{sw}" stroke-opacity=".1"/>' for a, b, c in sqs[:3])
    diag = (f'<line x1="0" y1="100" x2="261.8" y2="0" stroke="{GOLD}" stroke-width="{sw}" stroke-opacity=".14" stroke-dasharray="{4 * sw} {4 * sw}"/>'
            f'<line x1="100" y1="100" x2="261.8" y2="0" stroke="{GOLD}" stroke-width="{sw}" stroke-opacity=".14" stroke-dasharray="{4 * sw} {4 * sw}"/>')
    bars = "".join(f'<path d="{d}" fill="{BLUE}" fill-opacity="{o}" stroke="{SKY}" stroke-width="{sw}"/>' for d, o in zip(L.BARS_D, (1, .58, .28)))
    body = f'<path d="{L.BODY_D}" fill="{ICE}" fill-opacity=".08" stroke="{ICE}" stroke-width="{1.5 * sw}" fill-rule="evenodd"/>'
    markg = f'<g transform="translate({mx} {my}) scale({s})">{sq0}{circ0}{gq}{circles}{diag}{body}{bars}{spiral}</g>'
    # page guides
    hl = lambda v, c, o, dash="": f'<line x1="0" x2="{PW}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{c}" stroke-opacity="{o}" stroke-dasharray="{dash}"/>'
    guides = hl(0, ICE, .2) + hl(100, ICE, .2) + hl(61.8, SKY, .7, "6 6")
    lean = f'<line x1="{X(261.8)}" y1="{Y(100)}" x2="{X(261.8) + 100 * s * K}" y2="{Y(0)}" stroke="{SKY}" stroke-dasharray="6 6"/>'
    dims = (f'<line x1="{X(0)}" x2="{X(100)}" y1="{Y(100) + 46}" y2="{Y(100) + 46}" stroke="{GOLD}" stroke-opacity=".8"/>'
            f'<line x1="{X(100)}" x2="{X(261.8)}" y1="{Y(100) + 46}" y2="{Y(100) + 46}" stroke="{GOLD}" stroke-opacity=".8"/>'
            + "".join(f'<line x1="{X(u)}" x2="{X(u)}" y1="{Y(100) + 38}" y2="{Y(100) + 54}" stroke="{GOLD}"/>' for u in (0, 100, 261.8)))
    grid = "".join(f'<line x1="{x}" y1="{PH}" x2="{x + PH * K:.0f}" y2="0" stroke="{ICE}" stroke-opacity=".04"/>' for x in range(-300, PW + 300, 36))
    ticks = "".join(f'<line x1="{x}" x2="{x}" y1="{PH - 26}" y2="{PH - (20 if x % 50 else 12)}" stroke="{ICE}" stroke-opacity=".3"/>' for x in range(0, PW, 10))
    svg = f'<svg width="{PW}" height="{PH}" style="position:absolute;left:0;top:0"><rect width="{PW}" height="{PH}" fill="{NIGHT}"/>{grid}{ticks}{guides}{lean}{dims}{markg}</svg>'
    lab = lambda x, y, t, c=STEEL: f'<div class="m" style="position:absolute;left:{x}px;top:{y}px;color:{c};font-size:15px">{t}</div>'
    labels = (lab(14, Y(61.8) - 24, "1/φ · 0.618", SKY)
              + lab(X(200), Y(0) - 32, "12° LEAN", SKY)
              + lab(X(30), Y(100) + 62, "1", GOLD) + lab(X(170), Y(100) + 62, "φ", GOLD)
              + lab(X(0), Y(0) - 32, "1 : φ  ·  SQUARE + GOLDEN RECTANGLE", GOLD))
    specs = [("13 : 8 : 5", "speed bars, each ÷ φ"), ("12°", "one lean, every edge"), ("1/φ", "the line through the bars"), ("φ²", "width : height · 2.618")]
    row = "".join(f'<div style="flex:1;border-top:2px solid {BLUE if i == 0 else "#2a3150"};padding-top:16px">'
                  f'<div class="h" style="font-size:44px;color:{ICE};text-transform:none">{a}</div><div class="b" style="font-size:15px;margin-top:8px;color:{STEEL}">{b}</div></div>'
                  for i, (a, b) in enumerate(specs))
    html = (svg
            + f'<div style="position:absolute;left:90px;top:90px">{kicker("THE MARK · CONSTRUCTION", BLUE, 18)}</div>'
            + f'<div style="position:absolute;right:90px;top:84px">{mark(150)}</div>'
            + f'<div style="position:absolute;left:90px;top:160px" class="h"><span style="font-size:92px">EVERY LINE<br/>HAS A <span style="color:{BLUE}">REASON.</span></span></div>'
            + labels
            + f'<div style="position:absolute;left:90px;right:90px;top:1060px;display:flex;gap:28px">{row}</div>'
            + f'<div style="position:absolute;left:90px;right:90px;bottom:60px;display:flex;justify-content:space-between">{mono("AKKI MEISTER · LOGO BREAKDOWN", STEEL, 14)}{mono("@AKKKKKI_45", ICE, 14)}</div>')
    return f'<section data-snap="post-02-logo-breakdown" style="width:{PW}px;height:{PH}px;background:{NIGHT}">{html}</section>'


if __name__ == "__main__":
    out = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/breakdown.html"
    open(out, "w", encoding="utf-8").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{L.CSS}</style></head><body>{post()}</body></html>')
    print("ok")
