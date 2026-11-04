"""AKKI MEISTER launch kit v2: refined pattern system + teaser posts and story."""
import math, random, os, shutil
import launch as L
from launch import (mark, lockup, kicker, mono, frame, layer, roundel, NIGHT, ICE, BLUE, STEEL, DEEP, K, PHI,
                    p_bar_field, p_pinstripe, p_construction, p_rails, p_dots, p_monogram_tile, BODY_D, BARS_D, MW, MH)

OUT = L.OUT
SKY = "#5B7BFF"


def svgwrap(w, h, inner, bg=NIGHT, defs=""):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">'
            f'<defs>{defs}</defs><rect width="{w}" height="{h}" fill="{bg}"/>{inner}</svg>')


# ---------------------------------------------------------------- 03 GRID SLOTS v2: a waving chequered flag in perspective
def p_grid_slots(w, h, seed=0, rows=22, cols=26):
    def P(u, v):
        d = 1 + v * 3.2                                   # depth
        wave = math.sin(u * 7.5 + v * 3.2 + seed) * 0.9 + math.sin(u * 2.3 - v * 1.7) * 0.6
        sx = w * 0.45 + (u - 0.5) * w * 2.8 / d + v * w * 0.12
        sy = -h * 0.04 + h * 1.25 * (1 - 1 / d) - wave * 46 / d
        sx += (h - sy) * K * 0.6                          # lean 12° with the mark
        return sx, sy, wave

    cells, lines = "", ""
    for r in range(rows):
        v0, v1 = r / rows, (r + 1) / rows
        for c in range(cols):
            u0, u1 = c / cols, (c + 1) / cols
            a, b, cc, dd = P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)
            pts = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in (a, b, cc, dd))
            fade = (1 - v0) ** 0.7 * (0.35 + 0.65 * u0)
            shade = 0.55 + 0.45 * math.cos((a[2] - cc[2]) * 1.6)
            if (r + c + 1) % 2 == 0:
                op = max(0, fade * shade)
                col = BLUE if (r + c) % 7 else SKY
                cells += f'<polygon points="{pts}" fill="{col}" opacity="{op:.2f}"/>'
            else:
                cells += f'<polygon points="{pts}" fill="#0E1638" opacity="{max(0, fade * .6):.2f}"/>'
            lines += f'<polygon points="{pts}" fill="none" stroke="{ICE}" stroke-width=".45" opacity="{max(0, fade * .22):.2f}"/>'
    # specular sweep across the flag
    defs = (f'<linearGradient id="sp{seed}" x1="0" y1="0" x2="1" y2=".4"><stop offset=".3" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#9fb2ff" stop-opacity=".22"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="gl{seed}" cx=".75" cy=".15" r=".9"><stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient>')
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>'
            f'<rect width="{w}" height="{h}" fill="url(#gl{seed})"/>{cells}{lines}<rect width="{w}" height="{h}" fill="url(#sp{seed})"/></svg>')


# ---------------------------------------------------------------- 06 FLARES v2
def flare(x, y, s, col=ICE, op=1.0, uid="f"):
    t = s * 0.045
    rays = (f'<path d="M0 {-s} L{t} {-t} L{s} 0 L{t} {t} L0 {s} L{-t} {t} L{-s} 0 L{-t} {-t} Z" fill="{col}"/>'
            f'<path d="M0 {-s * .45} L{t * .6} 0 L0 {s * .45} L{-t * .6} 0 Z" fill="{col}" transform="rotate(45)" opacity=".55"/>')
    glow = f'<circle r="{s * .32:.1f}" fill="url(#{uid})"/>'
    return f'<g transform="translate({x:.0f} {y:.0f})" opacity="{op}">{glow}{rays}<circle r="{max(1.2, s * .05):.1f}" fill="#fff"/></g>'


def p_flare(w, h, seed=3):
    rnd = random.Random(seed)
    defs = (f'<radialGradient id="fg{seed}"><stop offset="0" stop-color="#9fb2ff" stop-opacity=".55"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="bg{seed}" cx=".3" cy=".25" r=".9"><stop offset="0" stop-color="#0d1430"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient>')
    g = "".join(f'<line x1="{x}" y1="{h}" x2="{x + h * K:.0f}" y2="0" stroke="{ICE}" stroke-opacity=".045"/>' for x in range(-300, w + 300, 48))
    g += "".join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}" stroke="{ICE}" stroke-opacity=".035"/>' for y in range(0, h, 48))
    # one hero flare with a long horizontal anamorphic streak, then a scatter on grid crossings
    hx, hy = w * .76, h * .2
    g += f'<rect x="0" y="{hy - .6}" width="{w}" height="1.2" fill="{SKY}" opacity=".35"/>'
    g += flare(hx, hy, min(w, h) * .2, ICE, 1, f"fg{seed}")
    for _ in range(int(w * h / 26000)):
        gx = round(rnd.uniform(0, w) / 48) * 48
        gy = round(rnd.uniform(0, h) / 48) * 48
        s = rnd.choice((4, 6, 9, 14, 20))
        g += flare(gx + (h - gy) * K * 0, gy, s, BLUE if rnd.random() < .3 else ICE, rnd.choice((.35, .6, .9)), f"fg{seed}")
    return svgwrap(w, h, g, f"url(#bg{seed})", defs)


# ---------------------------------------------------------------- NEW PATTERNS
def p_chequer_lines(w, h, seed=2):
    """CHEQUER LINES: strips of fine chequer at 12°, different lengths, like timing loops across a track."""
    rnd = random.Random(seed)
    g, y = "", 10
    while y < h:
        sq = rnd.choice((5, 6, 8))
        x = rnd.uniform(-100, w * .5)
        n = rnd.randint(10, 60)
        for c in range(n):
            for r in range(2):
                if (c + r + 1) % 2 == 0:
                    xx, yy = x + c * sq, y + r * sq
                    op = (1 - c / n) * (1 if rnd.random() > .1 else .3)
                    g += (f'<polygon points="{xx + sq * (2 - r) * K:.1f},{yy} {xx + sq + sq * (2 - r) * K:.1f},{yy} {xx + sq + sq * (1 - r) * K:.1f},{yy + sq} '
                          f'{xx + sq * (1 - r) * K:.1f},{yy + sq}" fill="{BLUE if rnd.random() < .7 else ICE}" opacity="{op:.2f}"/>')
        g += f'<rect x="{x + n * sq + 8:.0f}" y="{y + sq - .4}" width="{rnd.uniform(40, 300):.0f}" height=".8" fill="{ICE}" opacity=".2"/>'
        y += sq * 2 + rnd.choice((14, 22, 40))
    return svgwrap(w, h, g)


def p_shards(w, h, seed=4):
    """SHARDS: angular 12° parallelograms and wedges, some solid cobalt, most outlined — aero surfaces."""
    rnd = random.Random(seed)
    g = ""
    for _ in range(24):
        x, y = rnd.uniform(-100, w), rnd.uniform(-50, h)
        L_, t = rnd.uniform(60, 360), rnd.uniform(10, 60)
        cut = rnd.uniform(.2, .8)
        pts = [(x + t * K * 4, y), (x + L_, y), (x + L_ - t * K * 4 - L_ * .18 * cut, y + t), (x, y + t)]
        p = " ".join(f"{a:.0f},{b:.0f}" for a, b in pts)
        if rnd.random() < .22:
            g += f'<polygon points="{p}" fill="{BLUE}" opacity="{rnd.choice((.5, .8, 1))}"/>'
        else:
            g += f'<polygon points="{p}" fill="none" stroke="{ICE if rnd.random() < .7 else BLUE}" stroke-width="1.2" opacity="{rnd.choice((.2, .35, .6))}"/>'
    return svgwrap(w, h, g)


def p_kerb(w, h):
    """KERB: a sweeping corner kerb in cobalt / ice blocks, with the apex flare."""
    g = ""
    cx, cy, R1, R2 = w * 1.05, h * 1.25, h * 1.05, h * .92
    n = 34
    for i in range(n):
        a0 = math.pi * (1.02 + i * .55 / n)
        a1 = math.pi * (1.02 + (i + 1) * .55 / n)
        pts = [(cx + R1 * math.cos(a0), cy + R1 * math.sin(a0)), (cx + R1 * math.cos(a1), cy + R1 * math.sin(a1)),
               (cx + R2 * math.cos(a1), cy + R2 * math.sin(a1)), (cx + R2 * math.cos(a0), cy + R2 * math.sin(a0))]
        g += f'<polygon points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="{BLUE if i % 2 else ICE}" opacity="{.35 + .65 * i / n:.2f}"/>'
    g += f'<path d="M{cx - R1 * 1.2:.0f} {cy - R1 * .2:.0f} A{R1 * 1.18:.0f} {R1 * 1.18:.0f} 0 0 1 {cx - R1 * .1:.0f} {cy - R1 * 1.17:.0f}" fill="none" stroke="{ICE}" stroke-opacity=".25" stroke-dasharray="2 8"/>'
    return svgwrap(w, h, g)


def p_hud(w, h, seed=6):
    """HUD: sim-racing telemetry overlay: speed trace vs reference, delta bar, gear, rpm ticks."""
    rnd = random.Random(seed)
    g = ""
    for y in range(int(h * .3), int(h * .8), 30):
        g += f'<line x1="40" x2="{w - 40}" y1="{y}" y2="{y}" stroke="{ICE}" stroke-opacity=".07"/>'
    pts = lambda ph, a: " ".join(f"{40 + i * (w - 80) / 160:.1f},{h * .55 - a * (math.sin(i * .09 + ph) * 60 + math.sin(i * .31) * 20):.1f}" for i in range(161))
    g += f'<polyline points="{pts(.3, 1)}" fill="none" stroke="{STEEL}" stroke-width="1.2" stroke-dasharray="4 4"/>'
    g += f'<polyline points="{pts(0, 1.05)}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
    g += "".join(f'<rect x="{40 + i * 14}" y="{h * .14}" width="10" height="16" fill="{BLUE if i < 14 else "#1a2350"}"/>' for i in range(20))
    g += f'<text x="40" y="{h * .12}" font-family="JBM" font-size="12" fill="{STEEL}">RPM</text>'
    g += (f'<text x="{w - 40}" y="{h * .2}" text-anchor="end" font-family="JBM" font-size="38" fill="{ICE}">1:26.004</text>'
          f'<text x="{w - 40}" y="{h * .26}" text-anchor="end" font-family="JBM" font-size="18" fill="{BLUE}">−0.214</text>'
          f'<text x="40" y="{h * .9}" font-family="JBM" font-size="12" fill="{STEEL}">S1   S2   S3   ·   GEAR 6   ·   ABS 3   ·   TC 2</text>')
    g += f'<rect x="{w / 2 - 160}" y="{h * .66}" width="320" height="10" fill="#1a2350"/><rect x="{w / 2}" y="{h * .66}" width="110" height="10" fill="{BLUE}"/><line x1="{w / 2}" x2="{w / 2}" y1="{h * .65}" y2="{h * .68}" stroke="{ICE}"/>'
    g += "".join(f'<rect x="{40 + i * ((w - 80) / 3)}" y="{h * .74}" width="{(w - 80) / 3 - 8:.0f}" height="34" fill="{c}" opacity=".85"/><text x="{50 + i * ((w - 80) / 3)}" y="{h * .74 + 23}" font-family="JBM" font-size="14" fill="{ICE}">S{i + 1}  {t}</text>' for i, (c, t) in enumerate(((BLUE, "28.114"), ("#1a2350", "31.420"), (BLUE, "26.470"))))
    g += f'<text x="{w / 2}" y="{h * .62}" text-anchor="middle" font-family="JBM" font-size="64" fill="{ICE}">6</text>'
    g += "".join(f'<g transform="translate({x} {y})" stroke="{ICE}" stroke-opacity=".5"><line x1="-8" x2="8"/><line y1="-8" y2="8"/></g>' for x, y in ((24, 24), (w - 24, 24), (24, h - 24), (w - 24, h - 24)))
    return svgwrap(w, h, g)


def p_track(w, h):
    """TRACK MAP: a circuit drawn as a single cobalt line with sector ticks and the start/finish chequer."""
    pts = [(0.12, .62), (.3, .64), (.42, .58), (.48, .4), (.62, .3), (.82, .34), (.88, .48), (.74, .58), (.64, .74), (.4, .82), (.18, .78), (.1, .7), (0.12, .62)]
    P = [(x * w, y * h) for x, y in pts]
    d = "M" + " ".join(f"{(P[i][0] + P[i + 1][0]) / 2:.0f},{(P[i][1] + P[i + 1][1]) / 2:.0f} Q" if False else "" for i in range(0))
    path = f"M{P[0][0]:.0f},{P[0][1]:.0f} " + " ".join(f"Q{P[i][0]:.0f},{P[i][1]:.0f} {(P[i][0] + P[i + 1][0]) / 2:.0f},{(P[i][1] + P[i + 1][1]) / 2:.0f}" for i in range(1, len(P) - 1)) + f" T{P[-1][0]:.0f},{P[-1][1]:.0f}"
    g = f'<path d="{path}" fill="none" stroke="#141c3c" stroke-width="22" stroke-linejoin="round"/><path d="{path}" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    g += "".join(f'<circle cx="{P[i][0]:.0f}" cy="{P[i][1]:.0f}" r="5" fill="{NIGHT}" stroke="{ICE}" stroke-width="1.5"/><text x="{P[i][0] + 10:.0f}" y="{P[i][1] - 10:.0f}" font-family="JBM" font-size="11" fill="{STEEL}">T{n}</text>'
                for n, i in enumerate((2, 4, 6, 8, 10), 1))
    return svgwrap(w, h, g)


def p_speedlines(w, h, seed=8):
    """SPEED LINES: horizontal streaks in φ lengths, densest at the centre band, fading out."""
    rnd = random.Random(seed)
    g = ""
    for _ in range(int(h / 3)):
        y = rnd.gauss(h / 2, h / 5)
        L_ = rnd.choice((40, 65, 105, 170, 275))
        x = rnd.uniform(-L_, w)
        col = BLUE if rnd.random() < .4 else ICE
        g += f'<rect x="{x:.0f}" y="{y:.0f}" width="{L_}" height="{rnd.choice((1, 1, 2, 3))}" fill="{col}" opacity="{max(.05, 1 - abs(y - h / 2) / (h / 2)) * rnd.uniform(.3, 1):.2f}"/>'
    return svgwrap(w, h, g)


PATTERNS = [
    ("01", "BAR FIELD", "The three bars as a running rhythm.", p_bar_field),
    ("02", "PINSTRIPE", "Hairlines broken by 13:8:5 cobalt runs.", p_pinstripe),
    ("03", "GRID SLOTS", "A waving chequered flag in perspective, leaning 12°.", p_grid_slots),
    ("04", "CHEQUER LINES", "Fine 12° chequer strips, like timing loops.", p_chequer_lines),
    ("05", "SHARDS", "Angular 12° aero surfaces, solid and outlined.", p_shards),
    ("06", "FLARES", "Apex flares with glow on a 12° grid.", p_flare),
    ("07", "KERB", "A sweeping corner kerb in cobalt and ice.", p_kerb),
    ("08", "HUD", "Sim-racing telemetry overlay.", p_hud),
    ("09", "TRACK MAP", "A circuit drawn as one cobalt line.", p_track),
    ("10", "SPEED LINES", "φ-length streaks, densest in the centre.", p_speedlines),
    ("11", "CONSTRUCTION", "The mark's build: 12° rails, φ guides.", p_construction),
    ("12", "RAILS", "Outlined bars, one lit: the racing line.", p_rails),
    ("13", "SIGNAL DOTS", "Dot matrix along the 12° diagonal.", p_dots),
    ("14", "MONOGRAM TILE", "The mark on an offset grid.", p_monogram_tile),
]


def pattern_sheet():
    tiles = ""
    for i, (n, name, note, fn) in enumerate(PATTERNS):
        x, y = 64 + (i % 3) * 496, 150 + (i // 3) * 380
        tiles += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:480px;height:300px;overflow:hidden;border:1px solid #1d2230">{fn(480, 300)}</div>'
                  f'<div style="position:absolute;left:{x}px;top:{y + 312}px;width:480px">{kicker(n + " · " + name, BLUE, 13)}<div class="b" style="font-size:14px;margin-top:6px">{note}</div></div>')
    head = (f'<div style="position:absolute;left:64px;top:56px;right:64px;display:flex;justify-content:space-between;align-items:center">'
            f'{kicker("AKKI MEISTER · PATTERN SYSTEM", ICE, 15)}{mark(120)}</div>')
    return frame("pattern-system", 1600, 150 + 5 * 380 + 20, head + tiles)


def big_pattern(fn, name, w=1600, h=1000):
    return frame(f"pattern-{name}", w, h, layer(fn(w, h)))


# ---------------------------------------------------------------- POSTS (teaser)
PW, PH = 1080, 1350
PILLARS = [("SIM RACING", "rigs, grids, racecraft"), ("MOTORSPORT", "karts, Formula Student, track days"),
           ("TECH", "data, telemetry, builds"), ("LIFESTYLE", "the people, the places, the drive")]


def foot(txt="@AKKKKKI_45"):
    return f'<div style="position:absolute;left:90px;right:90px;bottom:80px;display:flex;justify-content:space-between">{mono("AKKI MEISTER", STEEL, 16)}{mono(txt, ICE, 16)}</div>'


def post_launch():
    return frame("post-01-introducing", PW, PH, layer(p_grid_slots(PW, PH, 1)) +
                 layer("", f"background:linear-gradient(180deg,{NIGHT} 0%,{NIGHT}00 34%,{NIGHT}00 62%,{NIGHT} 100%)") +
                 f'<div style="position:absolute;left:90px;top:90px">{kicker("INTRODUCING", STEEL, 18)}</div>'
                 f'<div style="position:absolute;left:90px;right:90px;top:430px">{lockup(900)}</div>'
                 f'<div style="position:absolute;left:90px;right:90px;bottom:80px;display:flex;justify-content:space-between">{mono("SIM RACING · MOTORSPORT · TECH · LIFESTYLE", STEEL, 15)}{mono("2026", ICE, 15)}</div>')


def post_pillars():
    rows = "".join(f'<div style="border-top:1px solid #2a3150;padding:26px 0;display:flex;justify-content:space-between;align-items:baseline">'
                   f'<div class="h" style="font-size:92px;color:{BLUE if i == 0 else ICE}">{t}</div><div class="m" style="color:{STEEL};font-size:15px">0{i + 1}</div></div>'
                   for i, (t, s) in enumerate(PILLARS))
    return frame("post-02-pillars", PW, PH, layer(p_chequer_lines(PW, PH)) + layer("", f"background:{NIGHT};opacity:.78") +
                 f'<div style="position:absolute;left:90px;top:90px">{mark(170)}</div>'
                 f'<div style="position:absolute;left:90px;right:90px;top:330px">{rows}</div>' + foot())


def post_bars():
    labels = [("SIM RACING", "rgba(36,64,255,.45)"), ("MOTORSPORT", "rgba(36,64,255,.72)"), ("LIFESTYLE", BLUE)]
    big = (f'<svg viewBox="0 0 520 900" width="520" height="900" style="position:absolute;left:40px;top:220px;overflow:visible;transform:scale(.62);transform-origin:0 0">'
           + "".join(f'<polygon points="{x + 900 * K:.0f},0 {x + bw + 900 * K:.0f},0 {x + bw:.0f},900 {x:.0f},900" fill="{BLUE}" opacity="{o}"/>'
                     for x, bw, o in ((0, 60, .28), (90, 96, .58), (216, 156, 1))) + "</svg>")
    txt = "".join(f'<div style="position:absolute;right:90px;top:{330 + i * 250}px;text-align:right"><div class="m" style="color:{STEEL};font-size:15px">BAR 0{i + 1}</div>'
                  f'<div class="h" style="font-size:84px;color:{c};margin-top:8px">{t}</div></div>' for i, (t, c) in enumerate(labels))
    return frame("post-03-three-bars", PW, PH, big + txt +
                 f'<div style="position:absolute;left:90px;top:90px">{kicker("/// THREE BARS", BLUE, 18)}</div>' + foot())


def post_sim():
    return frame("post-04-on-the-rig", PW, PH, layer(p_hud(PW, PH)) +
                 f'<div style="position:absolute;left:90px;top:90px">{kicker("SIM RACING", BLUE, 18)}</div>' +
                 layer("", f"background:linear-gradient(0deg,{NIGHT} 0%,{NIGHT} 22%,{NIGHT}00 34%)") +
                 f'<div style="position:absolute;left:90px;bottom:150px" class="h" >ON THE <span style="color:{BLUE}">RIG.</span></div>' + foot())


def post_lights():
    lights = "".join(f'<div style="width:120px;height:120px;border-radius:50%;background:{BLUE if i < 4 else "#141a33"};box-shadow:{"0 0 60px " + BLUE if i < 4 else "none"}"></div>' for i in range(5))
    return frame("post-05-lights-out", PW, PH, layer(p_flare(PW, PH, 11)) +
                 f'<div style="position:absolute;left:0;right:0;top:300px;display:flex;justify-content:center;gap:34px">{lights}</div>'
                 f'<div style="position:absolute;left:0;right:0;top:760px;text-align:center" class="h">LIGHTS OUT<br/><span style="color:{BLUE}">SOON.</span></div>'
                 f'<div style="position:absolute;left:0;right:0;bottom:110px;display:flex;justify-content:center">{mark(240)}</div>')


def post_kerb():
    return frame("post-06-out-now", PW, PH, layer(p_kerb(PW, PH)) +
                 f'<div style="position:absolute;left:90px;top:780px" class="h" >OUT<br/><span style="color:{BLUE}">NOW.</span></div>'
                 f'<div style="position:absolute;left:90px;top:1090px">{lockup(380)}</div>' + foot())


# ---------------------------------------------------------------- STORY (teaser, no counters)
SW, SH = 1080, 1920


def st(n, inner):
    return frame(f"story-{n:02d}", SW, SH, inner)


def stories():
    S = []
    S.append(st(1, layer(p_flare(SW, SH, 9)) +
                f'<div style="position:absolute;left:90px;bottom:520px" class="h">SOMETHING<br/>IS <span style="color:{BLUE}">COMING.</span></div>'))
    bars = (f'<svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;left:0;top:0">'
            + "".join(f'<polygon points="{x + 1920 * K:.0f},0 {x + bw + 1920 * K:.0f},0 {x + bw:.0f},1920 {x:.0f},1920" fill="{BLUE}" opacity="{o}"/>'
                      for x, bw, o in ((-420, 50, .28), (-340, 80, .58), (-225, 130, 1))) + "</svg>")
    lab = "".join(f'<div style="position:absolute;right:90px;top:{560 + i * 300}px;text-align:right"><div class="m" style="color:{STEEL};font-size:18px">BAR 0{i + 1}</div>'
                  f'<div class="h" style="font-size:96px;margin-top:10px;color:{c}">{t}</div></div>'
                  for i, (t, c) in enumerate((("SIM RACING", "rgba(36,64,255,.55)"), ("MOTORSPORT", "rgba(91,123,255,.9)"), ("LIFESTYLE", ICE))))
    bars = bars.replace('style="position:absolute;left:0;top:0"', 'style="position:absolute;left:120px;top:0"')
    S.append(st(2, bars + f'<div style="position:absolute;right:90px;top:300px">{kicker("THREE BARS", BLUE, 24)}</div>' + lab))
    S.append(st(3, layer(p_hud(SW, SH)) +
                f'<div style="position:absolute;left:90px;top:640px" class="h">ON THE<br/><span style="color:{BLUE}">RIG.</span></div>'
                f'<div style="position:absolute;left:90px;top:920px;width:820px" class="b">Sim racing first. Real racecraft, one lap at a time.</div>'))
    S.append(st(4, layer(p_speedlines(SW, SH)) +
                f'<div style="position:absolute;left:90px;right:90px;top:820px">{mark(900)}</div>'
                f'<div style="position:absolute;left:90px;bottom:420px" class="h">BUILT<br/>TO <span style="color:{BLUE}">MOVE.</span></div>'))
    S.append(st(5, layer(p_grid_slots(SW, SH, 2)) + layer("", f"background:linear-gradient(180deg,{NIGHT} 18%,{NIGHT}00 58%)") +
                f'<div style="position:absolute;left:90px;right:90px;top:520px">{lockup(900)}</div>'
                f'<div style="position:absolute;left:90px;right:90px;top:1140px;text-align:center">{mono("SIM RACING · MOTORSPORT · TECH · LIFESTYLE", ICE, 20)}</div>'))
    S.append(st(6, layer(p_rails(SW, SH)) +
                f'<div style="position:absolute;left:90px;top:300px" class="h">FOLLOW<br/>THE <span style="color:{BLUE}">LINE.</span></div>'
                f'<div style="position:absolute;left:90px;right:90px;top:760px;padding:34px 40px;background:{BLUE};display:flex;justify-content:space-between;align-items:center">'
                f'<span class="k" style="color:{ICE};font-size:30px;letter-spacing:.12em">@AKKKKKI_45</span><span class="k" style="color:{ICE};font-size:22px">FOLLOW →</span></div>'
                f'<div style="position:absolute;left:0;right:0;bottom:300px;display:flex;justify-content:center">{mark(300)}</div>'))
    return S


if __name__ == "__main__":
    for d in ("posts", "story", "patterns"):
        shutil.rmtree(OUT + d, ignore_errors=True)
    body = [pattern_sheet(), L.roundel_sheet(), big_pattern(p_grid_slots, "grid-slots"), big_pattern(p_flare, "flares"),
            post_launch(), post_pillars(), post_bars(), post_sim(), post_lights(), post_kerb()] + stories()
    open(OUT + "launch-kit.html", "w", encoding="utf-8").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{L.CSS}</style></head><body>{"".join(body)}</body></html>')
    print("ok")
