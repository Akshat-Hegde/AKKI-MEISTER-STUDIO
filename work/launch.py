"""AKKI MEISTER launch kit: pattern system, launch posts, launch story. One HTML; snap.js shoots every [data-snap]."""
import re, math, random, os

ROOT = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/"
OUT = ROOT + "AKKI-MEISTER-FINAL/"
FONTS = "file:///C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/"
NIGHT, ICE, BLUE, STEEL, DEEP = "#07080C", "#F3F4F6", "#2440FF", "#8C93A3", "#0B1440"
K = math.tan(math.radians(12))
PHI = (1 + 5 ** .5) / 2

# ---------------------------------------------------------------- the mark (paths from the locked master)
src = open(OUT + "logo/lockup-dark.svg").read()
paths = re.findall(r'<path ([^>]*)/>', src)
BODY_D = re.search(r'd="([^"]+)"', paths[0]).group(1)
BARS_D = [re.search(r'd="([^"]+)"', p).group(1) for p in paths[1:4]]
MW, MH = 261.8, 100.0
LOCKUP_INNER = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
LOCKUP_INNER = re.sub(r'<rect x="-14"[^>]*/>', "", LOCKUP_INNER, count=1)
LVB = re.search(r'viewBox="([^"]+)"', src).group(1)


def mark(w, fg=ICE, bars=(BLUE, BLUE, BLUE), ops=(1, .58, .28), style=""):
    b = "".join(f'<path fill="{c}" fill-opacity="{o}" d="{d}"/>' for d, c, o in zip(BARS_D, bars, ops))
    return f'<svg viewBox="0 0 {MW} {MH}" width="{w}" style="display:block;overflow:visible;{style}"><path fill="{fg}" fill-rule="evenodd" d="{BODY_D}"/>{b}</svg>'


def lockup(w, fg=ICE, style=""):
    inner = LOCKUP_INNER if fg == ICE else LOCKUP_INNER.replace(ICE, NIGHT)
    return f'<svg viewBox="{LVB}" width="{w}" style="display:block;{style}">{inner}</svg>'


# ---------------------------------------------------------------- PATTERN SYSTEM (all derived from the mark)
def p_bar_field(w, h, seed=1):
    """01 BAR FIELD: the three bars (13:8:5, 12° lean, cobalt fade) repeated as a rhythm across the frame."""
    g, x, i = "", -h * K, 0
    widths = (13, 8, 5)
    while x < w + 60:
        for j, (ww, op) in enumerate(zip(widths, (1, .58, .28))):
            g += f'<polygon points="{x + h * K:.1f},0 {x + ww + h * K:.1f},0 {x + ww:.1f},{h} {x:.1f},{h}" fill="{BLUE}" opacity="{op * (0.25 + 0.75 * (1 - x / w)) :.2f}"/>'
            x += ww + 6
        x += 34
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{g}</svg>'


def p_pinstripe(w, h, seed=5):
    """02 PINSTRIPE: the crossbar slit as a horizontal system: hairlines broken by cobalt runs in 13:8:5."""
    rnd = random.Random(seed)
    g, y = "", 14
    while y < h:
        g += f'<rect x="0" y="{y}" width="{w}" height="1" fill="{ICE}" opacity=".07"/>'
        x = rnd.uniform(-200, w * .3)
        while x < w:
            u = rnd.choice((6, 9, 14))
            for L, op in ((13 * u, 1), (8 * u, .58), (5 * u, .28)):
                g += f'<rect x="{x:.0f}" y="{y - 1.5}" width="{L:.0f}" height="3" fill="{BLUE}" opacity="{op}"/>'
                x += L + 6
            x += rnd.uniform(160, 520)
        y += rnd.choice((18, 18, 30, 44))
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{g}</svg>'


def p_grid_slots(w, h):
    """03 GRID SLOTS: the inverted, leaning chequer from the lockup, laid in perspective and fading — the finish line."""
    g = ""
    for r in range(18):
        sq = 18 + r * 3.2
        y = h * 0.18 + sum(18 + i * 3.2 for i in range(r))
        if y > h:
            break
        n = int(w / sq) + 4
        for c in range(n):
            if (c + r + 1) % 2 == 0:
                x = c * sq - r * sq * .5
                op = max(0, 0.9 - r * 0.05) * (0.25 + 0.75 * c / n)
                g += (f'<polygon points="{x + sq * K:.1f},{y:.1f} {x + sq + sq * K:.1f},{y:.1f} {x + sq:.1f},{y + sq:.1f} {x:.1f},{y + sq:.1f}" '
                      f'fill="{BLUE}" opacity="{op:.2f}"/>')
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">'
            f'<defs><radialGradient id="gs" cx=".7" cy=".2" r="1"><stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#gs)"/><g transform="skewY(-8) translate(0 {h * .1})">{g}</g></svg>')


def p_smear(w, h):
    """04 SMEAR: the mark itself streaked horizontally — a motion study, like a long exposure at the apex."""
    m = mark(w * .8)
    layers = "".join(f'<div style="position:absolute;left:{w * .1 + i * 26}px;top:{h * .5 - w * .8 * MH / MW / 2}px;opacity:{0.5 - i * 0.07:.2f};filter:blur({i * 3}px)">{m}</div>' for i in range(7, 0, -1))
    return (f'<div style="position:absolute;inset:0;background:{NIGHT};overflow:hidden">{layers}'
            f'<div style="position:absolute;left:{w * .1}px;top:{h * .5 - w * .8 * MH / MW / 2}px">{m}</div></div>')


def p_construction(w, h, dark=True):
    """05 CONSTRUCTION: the mark's own build — 12° rails, φ guides, measurements (after technical drawings)."""
    fg = ICE if dark else NIGHT
    bg = NIGHT if dark else ICE
    g = "".join(f'<line x1="{x}" y1="{h}" x2="{x + h * K}" y2="0" stroke="{fg}" stroke-opacity=".1"/>' for x in range(-200, w + 200, 36))
    g += "".join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}" stroke="{fg}" stroke-opacity="{.25 if i in (1, 3) else .08}" stroke-dasharray="{"" if i in (1, 3) else "3 5"}"/>' for i, y in enumerate((h * .2, h * .3, h * .52, h * .7, h * .85)))
    s = w * .62 / MW
    ox, oy = w * .19, h * .3
    m = (f'<g transform="translate({ox} {oy}) scale({s})"><path d="{BODY_D}" fill="none" stroke="{fg}" stroke-width="{1.2 / s}"/>'
         + "".join(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="{1.2 / s}"/>' for d in BARS_D) + "</g>")
    dims = (f'<g font-family="JBM" font-size="11" fill="{fg}" opacity=".7">'
            f'<line x1="{ox}" x2="{ox + MW * s}" y1="{oy + MH * s + 26}" y2="{oy + MH * s + 26}" stroke="{fg}" stroke-opacity=".5"/>'
            f'<text x="{ox + MW * s / 2}" y="{oy + MH * s + 44}" text-anchor="middle">2.618 : 1  ·  φ²</text>'
            f'<text x="{ox - 8}" y="{oy + MH * s * .618 + 4}" text-anchor="end">1/φ</text>'
            f'<text x="{ox + MW * s + 10}" y="{oy - 10}">12°</text></g>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{bg}"/>{g}{m}{dims}</svg>'


def p_flare(w, h, seed=3):
    """06 FLARES: four-point apex flares at the crossings of a 12° grid (after starburst highlights)."""
    rnd = random.Random(seed)
    g = "".join(f'<line x1="{x}" y1="{h}" x2="{x + h * K}" y2="0" stroke="{ICE}" stroke-opacity=".05"/>' for x in range(-200, w + 200, 60))
    g += "".join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}" stroke="{ICE}" stroke-opacity=".05"/>' for y in range(0, h, 60))
    for _ in range(14):
        x, y, s = rnd.uniform(0, w), rnd.uniform(0, h), rnd.choice((6, 10, 18, 30))
        c = BLUE if rnd.random() < .35 else ICE
        g += (f'<g transform="translate({x:.0f} {y:.0f})" opacity="{rnd.choice((.4, .7, 1))}"><path d="M0 {-s} L{s * .08} {-s * .08} L{s} 0 L{s * .08} {s * .08} L0 {s} L{-s * .08} {s * .08} L{-s} 0 L{-s * .08} {-s * .08} Z" fill="{c}"/></g>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{g}</svg>'


def p_rails(w, h):
    """07 RAILS: outlined parallelograms stacked like the bars, drawn as the racing line through a corner."""
    g = ""
    for i in range(7):
        x = w * .15 + i * 46
        g += (f'<polygon points="{x + h * K:.0f},0 {x + 30 + h * K:.0f},0 {x + 30:.0f},{h} {x:.0f},{h}" fill="none" '
              f'stroke="{BLUE if i == 3 else ICE}" stroke-width="{3 if i == 3 else 1.2}" opacity="{1 if i == 3 else .25 + i * .05:.2f}"/>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{g}</svg>'


def p_dots(w, h):
    """08 SIGNAL DOTS: a cobalt dot matrix, brightest along the 12° diagonal (a telemetry heat strip)."""
    g = ""
    for y in range(0, h, 12):
        for x in range(0, w, 12):
            d = abs((x - (h - y) * K * 3.5) - w * .45) / w
            r = max(0, 3.2 * (1 - d * 2.4))
            if r > .3:
                g += f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{BLUE}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{g}</svg>'


def p_monogram_tile(w, h):
    """09 MONOGRAM TILE: the mark repeated on a 12° offset grid, every 5th in cobalt — merch / backdrop."""
    g, s = "", 70 / MW
    for r in range(int(h / 50) + 2):
        for c in range(int(w / 110) + 2):
            x = c * 110 - (r % 2) * 55 + r * 50 * K
            y = r * 50
            col = BLUE if (r * 3 + c) % 5 == 0 else ICE
            op = 1 if col == BLUE else .12
            g += f'<g transform="translate({x:.0f} {y}) scale({s:.4f})" opacity="{op}"><path d="{BODY_D}" fill="{col}"/>{"".join(f"<path d={chr(34)}{d}{chr(34)} fill={chr(34)}{col}{chr(34)}/>" for d in BARS_D)}</g>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{g}</svg>'


def roundel(kind, size=140):
    """10 ROUNDEL ICONS: line icons on a cobalt disc in a steel ring (after team highlight covers), drawn on the 12° grid."""
    s = 'fill="none" stroke="#F3F4F6" stroke-width="3" stroke-linecap="square"'
    icon = {
        "flare": "".join(f'<line x1="0" y1="0" x2="{30 * math.cos(a):.1f}" y2="{30 * math.sin(a):.1f}" {s}/>' for a in [i * math.pi / 8 for i in range(16)]),
        "bars": "".join(f'<polygon points="{x + 40 * K:.1f},-20 {x + w_ + 40 * K:.1f},-20 {x + w_:.1f},20 {x:.1f},20" fill="#F3F4F6" opacity="{o}"/>' for x, w_, o in ((-26, 6, .4), (-16, 9, .7), (-3, 13, 1))),
        "flag": "".join(f'<rect x="{-24 + c * 12}" y="{-12 + r * 12}" width="12" height="12" fill="#F3F4F6" transform="skewX(-12)"/>' for c in range(4) for r in range(2) if (c + r + 1) % 2 == 0),
        "apex": f'<path d="M-30 20 C -10 20 0 -24 30 -24" {s}/><circle cx="2" cy="-6" r="4" fill="#F3F4F6"/>',
        "trace": f'<polyline points="-32,10 -18,10 -10,-18 0,12 8,-4 16,6 22,-22 32,-22" {s}/>',
        "wheel": f'<circle r="28" {s}/><circle r="7" {s}/><line x1="-28" y1="0" x2="-7" y2="0" {s}/><line x1="28" y1="0" x2="7" y2="0" {s}/><line x1="0" y1="7" x2="0" y2="28" {s}/>',
    }[kind]
    return (f'<svg viewBox="-60 -60 120 120" width="{size}" height="{size}"><defs><radialGradient id="rd{kind}" cx=".35" cy=".3"><stop offset="0" stop-color="#3355ff"/>'
            f'<stop offset="1" stop-color="#0d1a7a"/></radialGradient></defs><circle r="56" fill="none" stroke="#4a5263" stroke-width="7"/>'
            f'<circle r="48" fill="url(#rd{kind})"/>{icon}</svg>')


PATTERNS = [
    ("01", "BAR FIELD", "The three bars (13:8:5, 12°, cobalt fade) as a running rhythm.", p_bar_field),
    ("02", "PINSTRIPE", "The crossbar slit as a horizontal system, punctuated by 12° bars.", p_pinstripe),
    ("03", "GRID SLOTS", "The lockup's inverted chequer laid in perspective: the finish line.", p_grid_slots),
    ("04", "SMEAR", "The mark streaked like a long exposure through the apex.", p_smear),
    ("05", "CONSTRUCTION", "The mark's build exposed: 12° rails, φ guides, ratios.", p_construction),
    ("06", "FLARES", "Four-point apex flares on a 12° grid.", p_flare),
    ("07", "RAILS", "Outlined bars as rails, one lit cobalt: the racing line.", p_rails),
    ("08", "SIGNAL DOTS", "Cobalt dot matrix, brightest along the 12° diagonal.", p_dots),
    ("09", "MONOGRAM TILE", "The mark on an offset 12° grid, every fifth in cobalt.", p_monogram_tile),
]


# ---------------------------------------------------------------- shared bits
def kicker(t, col=STEEL, size=14):
    return f'<div class="k" style="color:{col};font-size:{size}px">{t}</div>'


def mono(t, col=STEEL, size=16):
    return f'<div class="m" style="color:{col};font-size:{size}px">{t}</div>'


def flag_rule(w, col=ICE):
    sq = 7
    f = "".join(f'<polygon points="{w - 8 * sq + c * sq + (sq * (2 - r)) * K:.1f},{r * sq} {w - 8 * sq + (c + 1) * sq + (sq * (2 - r)) * K:.1f},{r * sq} '
                f'{w - 8 * sq + (c + 1) * sq + sq * (1 - r) * K:.1f},{(r + 1) * sq} {w - 8 * sq + c * sq + sq * (1 - r) * K:.1f},{(r + 1) * sq}" fill="{col}"/>'
                for c in range(8) for r in range(2) if (c + r + 1) % 2 == 0)
    return f'<svg width="{w}" height="{2 * sq}" style="display:block;overflow:visible"><rect x="0" y="{sq - .6}" width="{w - 8 * sq - 6}" height="1.2" fill="{col}" opacity=".4"/>{f}</svg>'


def frame(snap, w, h, inner, bg=NIGHT):
    return f'<section data-snap="{snap}" style="width:{w}px;height:{h}px;background:{bg}">{inner}</section>'


def layer(html, extra=""):
    return f'<div style="position:absolute;inset:0;{extra}">{html}</div>'


# ---------------------------------------------------------------- PATTERN SHEET
def pattern_sheet():
    tiles = ""
    for i, (n, name, note, fn) in enumerate(PATTERNS):
        x, y = 64 + (i % 3) * 496, 150 + (i // 3) * 360
        tiles += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:480px;height:300px;overflow:hidden;border:1px solid #1d2230">{fn(480, 300)}</div>'
                  f'<div style="position:absolute;left:{x}px;top:{y + 312}px;width:480px">{kicker(n + " · " + name, BLUE, 13)}<div class="b" style="font-size:14px;margin-top:6px">{note}</div></div>')
    head = (f'<div style="position:absolute;left:64px;top:56px;right:64px;display:flex;justify-content:space-between;align-items:center">'
            f'{kicker("AKKI MEISTER · PATTERN SYSTEM", ICE, 15)}{mark(120)}</div>')
    return frame("pattern-system", 1600, 1250, head + tiles)


def roundel_sheet():
    names = ["bars", "flag", "apex", "trace", "wheel", "flare"]
    labels = ["MARK", "FINISH", "APEX", "DATA", "SIM", "LAUNCH"]
    row = "".join(f'<div style="text-align:center">{roundel(k, 170)}<div style="margin-top:16px">{kicker(l, ICE, 13)}</div></div>' for k, l in zip(names, labels))
    return frame("highlight-roundels", 1600, 520,
                 f'<div style="position:absolute;left:64px;top:50px">{kicker("10 · ROUNDEL ICONS · INSTAGRAM HIGHLIGHTS", BLUE, 13)}</div>'
                 f'<div style="position:absolute;left:64px;right:64px;top:130px;display:flex;justify-content:space-between">{row}</div>')


# ---------------------------------------------------------------- POSTS (1080 x 1350)
PW, PH = 1080, 1350


def post_launch():
    return frame("post-01-launch", PW, PH,
                 layer(p_grid_slots(PW, PH)) +
                 layer("", f"background:linear-gradient(180deg,{NIGHT} 0%,{NIGHT}00 40%,{NIGHT}00 60%,{NIGHT} 100%)") +
                 f'<div style="position:absolute;left:90px;top:90px">{kicker("INTRODUCING", STEEL, 18)}</div>'
                 f'<div style="position:absolute;left:90px;right:90px;top:430px">{lockup(900)}</div>'
                 f'<div style="position:absolute;left:90px;bottom:90px;right:90px;display:flex;justify-content:space-between">{mono("MOTORSPORT · PERFORMANCE", STEEL, 16)}{mono("2026", ICE, 16)}</div>')


def post_mark():
    return frame("post-02-the-mark", PW, PH,
                 layer(p_construction(PW, PH)) +
                 f'<div style="position:absolute;left:90px;top:90px">{kicker("THE MARK", BLUE, 18)}</div>'
                 f'<div style="position:absolute;left:90px;bottom:250px;width:880px" class="h">THREE BARS.<br/><span style="color:{BLUE}">ONE LINE.</span></div>'
                 f'<div style="position:absolute;left:90px;bottom:110px;width:820px" class="b">Speed bars from a 2026 diary sketch, in a 13 : 8 : 5 golden progression. '
                 f'A pinstripe at 1/φ. Everything leans 12°.</div>')


def post_bars():
    return frame("post-03-meaning", PW, PH,
                 layer(p_bar_field(PW, PH)) + layer("", f"background:linear-gradient(90deg,{NIGHT}00 0%,{NIGHT} 70%)") +
                 f'<div style="position:absolute;right:90px;top:90px">{kicker("/// MEANS", STEEL, 18)}</div>'
                 + "".join(f'<div style="position:absolute;right:90px;top:{330 + i * 270}px;text-align:right">'
                           f'<div class="h" style="font-size:96px;color:{c}">{t}</div><div class="b" style="margin-top:10px">{s}</div></div>'
                           for i, (t, s, c) in enumerate((("SIM", "where it started, 2020", "rgba(36,64,255,.45)"),
                                                          ("TRACK", "karts, Formula Student", "rgba(36,64,255,.72)"),
                                                          ("DATA", "the line between them", BLUE))))
                 + f'<div style="position:absolute;right:90px;bottom:90px">{mark(220)}</div>')


def post_lights():
    lights = "".join(f'<div style="width:120px;height:120px;border-radius:50%;background:{BLUE if i < 4 else "#141a33"};box-shadow:{"0 0 60px " + BLUE if i < 4 else "none"}"></div>' for i in range(5))
    return frame("post-04-lights-out", PW, PH,
                 layer(p_flare(PW, PH)) +
                 f'<div style="position:absolute;left:0;right:0;top:300px;display:flex;justify-content:center;gap:34px">{lights}</div>'
                 f'<div style="position:absolute;left:0;right:0;top:560px;text-align:center" class="h">LIGHTS OUT<br/><span style="color:{BLUE}">SOON.</span></div>'
                 f'<div style="position:absolute;left:0;right:0;bottom:120px;display:flex;justify-content:center">{mark(260)}</div>')


def post_tile():
    return frame("post-05-pattern", PW, PH, layer(p_monogram_tile(PW, PH)) +
                 f'<div style="position:absolute;left:90px;right:90px;bottom:90px;padding:40px;background:{NIGHT}">{lockup(560)}'
                 f'<div style="margin-top:22px">{mono("NEW IDENTITY · OUT NOW · @AKKKKKI_45", STEEL, 16)}</div></div>')


# ---------------------------------------------------------------- LAUNCH STORY (1080 x 1920)
SW, SH = 1080, 1920


def story(n, inner):
    return frame(f"story-{n:02d}", SW, SH, inner)


def stories():
    S = []
    S.append(story(1, layer(p_flare(SW, SH, 9)) +
                   f'<div style="position:absolute;left:0;right:0;top:820px;text-align:center" class="h">SOMETHING<br/>IS COMING.</div>'
                   f'<div style="position:absolute;left:0;right:0;bottom:200px;text-align:center">{mono("01 / 06", STEEL, 18)}</div>'))
    S.append(story(2, layer(p_bar_field(SW, SH)) + layer("", f"background:linear-gradient(0deg,{NIGHT} 0%,{NIGHT}ee 30%,{NIGHT}00 60%)") +
                   f'<div style="position:absolute;left:90px;bottom:420px" class="h">THREE<br/>BARS.</div>'
                   f'<div style="position:absolute;left:90px;bottom:300px" class="b">13 : 8 : 5. Each one ÷ φ.</div>'
                   f'<div style="position:absolute;left:0;right:0;bottom:200px;text-align:center">{mono("02 / 06", STEEL, 18)}</div>'))
    S.append(story(3, layer(p_pinstripe(SW, SH)) +
                   f'<div style="position:absolute;left:90px;top:300px" class="h">ONE<br/><span style="color:{BLUE}">LINE.</span></div>'
                   f'<div style="position:absolute;left:90px;top:620px;width:780px" class="b">A pinstripe at 1/φ runs through the bars: the racing line through the mark.</div>'
                   f'<div style="position:absolute;left:0;right:0;bottom:200px;text-align:center">{mono("03 / 06", STEEL, 18)}</div>'))
    S.append(story(4, layer(p_smear(SW, SH)) +
                   f'<div style="position:absolute;left:90px;top:300px">{kicker("12° FORWARD", BLUE, 22)}</div>'
                   f'<div style="position:absolute;left:90px;bottom:400px" class="h">BUILT<br/>TO <span style="color:{BLUE}">MOVE.</span></div>'
                   f'<div style="position:absolute;left:0;right:0;bottom:200px;text-align:center">{mono("04 / 06", STEEL, 18)}</div>'))
    S.append(story(5, layer(p_grid_slots(SW, SH)) + layer("", f"background:linear-gradient(180deg,{NIGHT} 20%,{NIGHT}00 60%)") +
                   f'<div style="position:absolute;left:90px;right:90px;top:520px">{lockup(900)}</div>'
                   f'<div style="position:absolute;left:0;right:0;bottom:200px;text-align:center">{mono("05 / 06", STEEL, 18)}</div>'))
    S.append(story(6, layer(p_rails(SW, SH)) +
                   f'<div style="position:absolute;left:90px;top:300px" class="h">FOLLOW<br/>THE <span style="color:{BLUE}">LINE.</span></div>'
                   f'<div style="position:absolute;left:90px;right:90px;top:760px;padding:34px 40px;background:{BLUE};display:flex;justify-content:space-between;align-items:center">'
                   f'<span class="k" style="color:{ICE};font-size:30px;letter-spacing:.12em">@AKKKKKI_45</span><span class="k" style="color:{ICE};font-size:22px">FOLLOW →</span></div>'
                   f'<div style="position:absolute;left:0;right:0;bottom:300px;display:flex;justify-content:center">{mark(300)}</div>'
                   f'<div style="position:absolute;left:0;right:0;bottom:200px;text-align:center">{mono("06 / 06", STEEL, 18)}</div>'))
    return S


CSS = f"""
@font-face {{ font-family: Clash; src: url({FONTS}fonts/clash-grotesk.woff2) format('woff2'); font-weight: 600; }}
@font-face {{ font-family: ClashD; src: url({FONTS}fonts/clash-display.woff2) format('woff2'); font-weight: 600; }}
@font-face {{ font-family: JBM; src: url({FONTS}node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2) format('woff2'); font-weight: 100 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#000; }}
section {{ position:relative; overflow:hidden; margin-bottom:40px; }}
.k {{ font-family: Clash; font-weight:600; text-transform:uppercase; letter-spacing:.32em; white-space:nowrap; }}
.m {{ font-family: JBM; font-weight:500; letter-spacing:.08em; white-space:nowrap; }}
.h {{ font-family: ClashD; font-weight:600; font-size:130px; line-height:.92; letter-spacing:-.01em; color:{ICE}; text-transform:uppercase; }}
.b {{ font-family: Clash; font-weight:600; font-size:28px; line-height:1.35; color:#A9B0C0; }}
"""

if __name__ == "__main__":
    body = "".join([pattern_sheet(), roundel_sheet(), post_launch(), post_mark(), post_bars(), post_lights(), post_tile()] + stories())
    open(OUT + "launch-kit.html", "w", encoding="utf-8").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
    print("ok")
