"""AKKI MEISTER launch v4: 3 teaser posts (intro / logo breakdown / follow the line) + story tweaks + dither pattern."""
import math, os, shutil, re
import launch as L
import launch2 as L2
import launch3 as L3
from launch import mark, lockup, kicker, mono, frame, layer, NIGHT, ICE, BLUE, STEEL, DEEP, K, MW, MH

OUT = L3.OUT
SKY = L3.SKY
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def p_dither(w, h, cell=7, fx=.78, fy=.18, col=BLUE, bg=NIGHT, hot=False):
    """DITHER GRADIENT: ordered (Bayer 4×4) dither of a radial cobalt glow; brightest cells turn ice."""
    g = []
    R = math.hypot(w, h) * .62
    for j in range(0, h, cell):
        for i in range(0, w, cell):
            v = max(0, 1 - math.hypot(i - w * fx, j - h * fy) / R) ** 1.25
            t = (BAYER[(j // cell) % 4][(i // cell) % 4] + .5) / 16
            if v > t:
                c = ICE if (hot and v > .86) else SKY if v > .72 else col
                g.append(f'<rect x="{i}" y="{j}" width="{cell - 1.5}" height="{cell - 1.5}" fill="{c}"/>')
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{"".join(g)}</svg>')


PW, PH = 1080, 1350
PILLARS = [("01", "SIM RACING", "rigs · grids · racecraft"), ("02", "MOTORSPORT", "karts · Formula Student · track days"), ("03", "BEHIND THE SCENES", "the people, the prep, the process")]


def post_intro():
    cols = "".join(f'<div style="flex:1;border-top:2px solid {BLUE if i == 0 else "#2a3150"};padding-top:18px">{mono(n, BLUE, 15)}'
                   f'<div class="k" style="color:{ICE};font-size:21px;letter-spacing:.14em;margin-top:10px">{t}</div>'
                   f'<div class="b" style="font-size:16px;margin-top:8px;color:{STEEL}">{s}</div></div>' for i, (n, t, s) in enumerate(PILLARS))
    return frame("post-01-introducing", PW, PH,
                 layer(p_dither(PW, PH, 8, .85, .08)) +
                 layer("", f"background:linear-gradient(180deg,{NIGHT}00 0%,{NIGHT}aa 40%,{NIGHT} 70%)") +
                 f'<div style="position:absolute;left:90px;top:90px">{kicker("INTRODUCING", STEEL, 18)}</div>'
                 f'<div style="position:absolute;left:90px;top:200px" class="h" ><span style="font-size:96px">SAME PASSION.<br/>SAME VISION.<br/><span style="color:{BLUE}">NEW IDENTITY.</span></span></div>'
                 f'<div style="position:absolute;left:90px;top:690px">{lockup(560)}</div>'
                 f'<div style="position:absolute;left:90px;right:90px;bottom:150px;display:flex;gap:30px">{cols}</div>'
                 f'<div style="position:absolute;left:90px;right:90px;bottom:70px;display:flex;justify-content:space-between">{mono("AKKI MEISTER", STEEL, 15)}{mono("@AKKKKKI_45", ICE, 15)}</div>')


def post_breakdown():
    s = 860 / MW
    mx, my = 110, 520
    X = lambda u: mx + u * s
    Y = lambda v: my + v * s
    mh = MH * s
    k = math.tan(math.radians(12))
    # outlined mark with partial cobalt fill + guides
    body = L.BODY_D
    guides = (f'<line x1="0" x2="{PW}" y1="{Y(0)}" y2="{Y(0)}" class="g"/><line x1="0" x2="{PW}" y1="{Y(100)}" y2="{Y(100)}" class="g"/>'
              f'<line x1="0" x2="{PW}" y1="{Y(61.8)}" y2="{Y(61.8)}" class="gb"/><line x1="0" x2="{PW}" y1="{Y(38.2)}" y2="{Y(38.2)}" class="gd"/>'
              f'<line x1="{X(261.8)}" y1="{Y(100)}" x2="{X(261.8) + 100 * s * k}" y2="{Y(0)}" class="gb"/>'
              f'<path d="M{X(261.8) - 40} {Y(100)} A40 40 0 0 1 {X(261.8) - 40 * math.cos(math.radians(78)) - 0} {Y(100) - 40 * math.sin(math.radians(78))}" class="g" fill="none"/>'
              # width dimension
              f'<line x1="{X(0)}" x2="{X(261.8)}" y1="{Y(100) + 60}" y2="{Y(100) + 60}" class="gd2"/>'
              f'<line x1="{X(0)}" x2="{X(0)}" y1="{Y(100) + 50}" y2="{Y(100) + 70}" class="gd2"/><line x1="{X(261.8)}" x2="{X(261.8)}" y1="{Y(100) + 50}" y2="{Y(100) + 70}" class="gd2"/>'
              # height dimension
              '')
    bars = "".join(f'<path d="{d}" fill="{BLUE}" fill-opacity="{o}" stroke="{SKY}" stroke-width="{1 / s:.3f}"/>' for d, o in zip(L.BARS_D, (1, .58, .28)))
    svg = (f'<svg width="{PW}" height="{PH}" style="position:absolute;left:0;top:0"><style>.g{{stroke:#F3F4F6;stroke-opacity:.18}}.gb{{stroke:{SKY};stroke-dasharray:6 6}}'
           f'.gd{{stroke:#F3F4F6;stroke-opacity:.12;stroke-dasharray:3 6}}.gd2{{stroke:#F3F4F6;stroke-opacity:.5}}</style>{guides}'
           f'<g transform="translate({mx} {my}) scale({s})"><path d="{body}" fill="{ICE}" fill-opacity=".06" stroke="{ICE}" stroke-width="{1.4 / s:.3f}" fill-rule="evenodd"/>{bars}</g></svg>')
    lab = lambda x, y, t, c=STEEL, a="left": f'<div class="m" style="position:absolute;left:{x}px;top:{y}px;color:{c};font-size:15px;text-align:{a}">{t}</div>'
    callouts = (lab(X(261.8) - 40, Y(0) - 44, "12° LEAN", SKY)
                + lab(14, Y(61.8) - 24, "1/φ · 0.618", SKY)
                + lab(14, Y(38.2) - 24, "1/φ² · 0.382")
                + lab(X(130) - 80, Y(100) + 72, "W : H = 2.618 · φ²", ICE)
                
                + lab(X(0), Y(0) - 44, "13 : 8 : 5 · EACH ÷ φ", SKY))
    strip = ""
    for i, (name, fn) in enumerate((("BAR FIELD", L.p_bar_field), ("RAILS", L3.p_rails), ("DITHER", p_dither))):
        x = 90 + i * 310
        strip += (f'<div style="position:absolute;left:{x}px;top:1010px;width:290px;height:190px;overflow:hidden;border:1px solid #1d2230">{fn(290, 190)}</div>'
                  f'<div style="position:absolute;left:{x}px;top:1212px">{kicker(name, ICE, 12)}</div>')
    return frame("post-02-logo-breakdown", PW, PH,
                 layer(f'<svg width="{PW}" height="{PH}"><rect width="{PW}" height="{PH}" fill="{NIGHT}"/>' + "".join(f'<line x1="{x}" y1="{PH}" x2="{x + PH * k:.0f}" y2="0" stroke="#F3F4F6" stroke-opacity=".05"/>' for x in range(-300, PW + 300, 36)) + "".join(f'<line x1="{x}" x2="{x}" y1="{PH - 26}" y2="{PH - (20 if x % 50 else 12)}" stroke="#F3F4F6" stroke-opacity=".3"/>' for x in range(0, PW, 10)) + '</svg>') + svg + callouts + strip +
                 f'<div style="position:absolute;left:90px;top:90px">{kicker("THE MARK · BREAKDOWN", BLUE, 18)}</div>'
                 f'<div style="position:absolute;left:90px;top:150px" class="h" ><span style="font-size:96px">BUILT ON<br/><span style="color:{BLUE}">GEOMETRY.</span></span></div>'
                 f'<div style="position:absolute;right:90px;top:96px">{mark(150)}</div>'
                 f'<div style="position:absolute;left:90px;top:985px">{mono("DERIVED PATTERNS", STEEL, 13)}</div>')


def post_follow():
    return frame("post-03-follow-the-line", PW, PH,
                 layer(L3.p_rails(PW, PH)) +
                 f'<div style="position:absolute;left:90px;top:200px" class="h">FOLLOW<br/>THE <span style="color:{BLUE}">LINE.</span></div>'
                 f'<div style="position:absolute;left:90px;right:90px;top:620px;padding:34px 40px;background:{BLUE};display:flex;justify-content:space-between;align-items:center">'
                 f'<span class="k" style="color:{ICE};font-size:30px;letter-spacing:.12em">@AKKKKKI_45</span><span class="k" style="color:{ICE};font-size:22px">FOLLOW →</span></div>'
                 f'<div style="position:absolute;left:0;right:0;bottom:200px;display:flex;justify-content:center">{mark(360)}</div>'
                 f'<div style="position:absolute;left:90px;right:90px;bottom:70px;display:flex;justify-content:space-between">{mono("SIM RACING · MOTORSPORT · BEHIND THE SCENES", STEEL, 15)}{mono("2026", ICE, 15)}</div>')


def stories():
    L2.p_grid_slots = lambda w, h, seed=0: p_dither(w, h, 9, .5, .95)   # no chequer behind the reveal
    out = []
    for s in L2.stories():
        s = (s.replace("THREE BARS", "THREE LANES").replace("BAR 0", "LANE 0").replace(">LIFESTYLE<", ">BEHIND THE SCENES<")
              .replace("SIM RACING · MOTORSPORT · TECH · LIFESTYLE", "SIM RACING · MOTORSPORT · BEHIND THE SCENES"))
        out.append(s)
    return out


if __name__ == "__main__":
    L3.build()
    for d in ("posts", "story"):
        shutil.rmtree(OUT + d, ignore_errors=True)
        os.makedirs(OUT + d)
    open(OUT + "patterns/08-dither-gradient.svg", "w").write(
        p_dither(1600, 1000).replace('width="100%" height="100%"', 'width="1600" height="1000"').replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
    body = [post_intro(), post_breakdown(), post_follow()] + stories()
    open(OUT + "launch-kit.html", "w", encoding="utf-8").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{L.CSS}</style></head><body>{"".join(body)}</body></html>')
    print("ok")
