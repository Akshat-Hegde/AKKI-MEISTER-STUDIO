"""AKKI MEISTER brand system (round 3). Writes ../round3/system.html: board panels (1600x1000) and
full-size social templates (1080x1350 posts, 1080x1920 stories). snap3.js screenshots every [data-snap]."""
import math, random, re, os
from mtype import text_svg, text_svg_path, H as CAP
from meister import NIGHT, CARBON, ICE, STEEL, RED, COBALT

R3 = "../round3/"
ASSET = "file:///C:/Users/admin/Akki-Portfolio-main/brag-output-2026-10-12-233528/work/assets/"
DIARY = "file:///" + os.environ["TEMP"].replace("\\", "/") + "/claude/c--Users-admin-Akki-Portfolio-main/30173890-75cd-439c-ae4d-37294cbc60ee/images/58.jpg"
NM = "file:///C:/Users/admin/Akki-Portfolio-main/3d_portfolio/node_modules"
NAVY = "#0B1030"
HEAVY, BOLD, LIGHT = 1.75, 1.35, 0.55


# ------------------------------------------------------------------ type + symbols
def T(s, h, w=BOLD, col=ICE, track=1.0, style=""):
    return text_svg(s, h, w, track, fill=col, style=style)


def sym_inner(name):
    s = open(R3 + name + ".svg").read()
    s = s[s.index("</title>") + 8: s.rindex("</svg>")]
    return re.sub(r'<rect width="256" height="256"[^>]*/>', "", s)


SYM = {k: sym_inner(k) for k in ("a-ligature-color", "a-ligature-black", "a-ligature-rev", "b-launch-color", "b-launch-rev", "b-launch-black", "c-box-color", "c-box-rev", "c-box-black")}


def sym(name, size, fg=None, acc=None, style=""):
    s = SYM[name]
    if fg:
        s = s.replace(f'fill="{NIGHT}"', f'fill="{fg}"').replace(f'fill="{ICE}"', f'fill="{fg}"')
    if acc:
        s = s.replace(f'fill="{RED}"', f'fill="{acc}"')
    return f'<svg viewBox="0 0 256 256" width="{size}" height="{size}" style="display:block;{style}">{s}</svg>'


def lockup(h, fg=ICE, acc=RED, sub=STEEL, symbol="a-ligature-color"):
    """symbol + wordmark + tagline in one row; h = symbol height"""
    s = sym(symbol, h * 1.25, fg=fg, acc=acc, style=f"margin:{-h * .125}px 0")
    return (f'<div style="display:flex;align-items:center;gap:{h * .32:.0f}px">{s}<div>{T("AKKI MEISTER", h * .42, HEAVY, fg, 1.1)}'
            f'<div style="display:flex;align-items:center;gap:{h * .12:.0f}px;margin-top:{h * .16:.0f}px"><span style="width:{h * .3:.0f}px;height:{max(2, h * .05):.0f}px;background:{acc}"></span>'
            f'{T("MOTORSPORT · PERFORMANCE", h * .11, LIGHT * 1.3, sub, 2.4)}</div></div></div>')


K = math.tan(math.radians(15))


# ------------------------------------------------------------------ patterns
def slipstream(w, h, col=RED, bg=NIGHT, seed=1, angle=-55, density=1.0):
    """parallelogram bands, each with pinstripes (after the red diagonal-stripe reference)"""
    rnd = random.Random(seed)
    D = int(math.hypot(w, h)) + 200
    g, y = "", -D / 2
    while y < D / 2:
        th = rnd.choice([14, 22, 36, 60, 90])
        x = -D / 2 + rnd.uniform(-200, 200)
        while x < D / 2:
            L = rnd.uniform(160, 700)
            if rnd.random() < 0.62 * density:
                op = rnd.choice([1, 1, 0.85, 0.6])
                g += f'<rect x="{x:.0f}" y="{y:.0f}" width="{L:.0f}" height="{th}" fill="{col}" opacity="{op}"/>'
                if th >= 36:
                    for k in (0.3, 0.62):
                        g += f'<rect x="{x:.0f}" y="{y + th * k:.0f}" width="{L:.0f}" height="3" fill="{bg}"/>'
            x += L + rnd.uniform(30, 260)
        y += th + rnd.choice([10, 16, 26, 40])
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{bg}"/><g transform="translate({w / 2} {h / 2}) rotate({angle})">{g}</g></svg>'


def interference(w, h, seed=4):
    """columns of hatch at different pitches, red and cobalt on navy"""
    rnd = random.Random(seed)
    defs, body, x = "", "", 0
    i = 0
    while x < w:
        cw = rnd.choice([28, 44, 60, 90])
        pitch = rnd.choice([6, 9, 12, 18])
        col = rnd.choice([RED, COBALT, COBALT, RED, "#1a2a9a"])
        sw = rnd.choice([2, 3, 4])
        defs += f'<pattern id="ih{i}" width="{pitch}" height="{pitch}" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><rect width="{sw}" height="{pitch}" fill="{col}"/></pattern>'
        y0 = rnd.choice([0, 0, rnd.uniform(0, h * 0.5)])
        body += f'<rect x="{x}" y="{y0:.0f}" width="{cw}" height="{h}" fill="url(#ih{i})"/>'
        if rnd.random() < 0.25:
            body += f'<rect x="{x}" y="{rnd.uniform(0, h):.0f}" width="{cw}" height="{rnd.uniform(40, 200):.0f}" fill="{col}" opacity="0.9"/>'
        x += cw + rnd.choice([0, 0, 4, 10])
        i += 1
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs><rect width="{w}" height="{h}" fill="{NAVY}"/>{body}</svg>'


def apex_mesh(w, h, col=RED, bg=NIGHT, seed=2, corner=(1, 1)):
    """outlined triangle mesh that fades out from one corner"""
    rnd = random.Random(seed)
    s = 70
    hh = s * math.sqrt(3) / 2
    g = ""
    cx, cy = corner[0] * w, corner[1] * h
    for r in range(-1, int(h / hh) + 2):
        for q in range(-1, int(w / s) + 3):
            x0 = q * s + (r % 2) * s / 2
            y0 = r * hh
            for up in (True, False):
                pts = [(x0, y0 + hh), (x0 + s / 2, y0), (x0 + s, y0 + hh)] if up else [(x0 + s / 2, y0), (x0 + s, y0 + hh), (x0 + s * 1.5, y0)]
                mx, my = sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3
                dd = math.hypot(mx - cx, my - cy) / math.hypot(w, h)
                if rnd.random() < 1.15 - dd * 2.2:
                    g += f'<polygon points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="2" opacity="{max(0.15, 1 - dd * 1.6):.2f}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{bg}"/>{g}</svg>'


def kerb_rails(w, h, col=RED, bg=CARBON, angle=-28):
    """rounded rails, a solid block and tick marks (after the green rails reference)"""
    ticks = "".join(f'<rect x="{i * 26}" y="0" width="5" height="34" rx="2" fill="none" stroke="{ICE}" stroke-width="1.6"/>' for i in range(18))
    mini = "".join(f'<rect x="{i * 10}" y="0" width="3" height="44" fill="{col}"/>' for i in range(30))
    zig = "".join(f'<path d="M{x} {y} l40 -60 l40 60 l40 -60" fill="none" stroke="#2a2c34" stroke-width="16"/>' for x in range(-200, w + 200, 170) for y in range(0, h + 200, 120))
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{bg}"/>{zig}'
            f'<g transform="translate({w * 0.55} {h * 0.55}) rotate({angle})">'
            f'<rect x="-320" y="-120" width="900" height="900" rx="46" fill="none" stroke="{ICE}" stroke-width="5"/>'
            f'<rect x="-420" y="-60" width="900" height="900" rx="46" fill="none" stroke="{col}" stroke-width="5"/>'
            f'<rect x="-120" y="40" width="900" height="900" rx="40" fill="{col}"/>'
            f'<rect x="-60" y="120" width="900" height="900" rx="40" fill="none" stroke="{bg}" stroke-width="5"/>'
            f'<g transform="translate(-300 -40)">{ticks}</g><g transform="translate(-520 -230)">{mini}</g></g></svg>')


def flag_fade(w, h, col=ICE, bg=NIGHT):
    """a chequered flag lying in perspective, fading out (after the Mercedes livery shot)"""
    g = ""
    for r in range(14):
        for c in range(30):
            if (r + c) % 2:
                continue
            x, y = c * 48 - r * 30, r * 34
            op = max(0, 0.75 - c * 0.03 - r * 0.045)
            if op > 0.02:
                g += f'<rect x="{x}" y="{y}" width="48" height="34" fill="{col}" opacity="{op:.2f}"/>'
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs><radialGradient id="ff" cx="0.3" cy="0.3" r="0.9"><stop offset="0" stop-color="#1b2550"/><stop offset="1" stop-color="{bg}"/></radialGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#ff)"/><g transform="translate(-40 {h * 0.12}) skewX(-38) rotate(-12)">{g}</g></svg>')


def smear(w, h, seed=5, col=ICE, bg=NIGHT):
    rnd = random.Random(seed)
    g = ""
    y = 0
    while y < h:
        th = rnd.choice([3, 6, 10, 18, 30])
        g += f'<rect x="{rnd.uniform(-200, w * 0.4):.0f}" y="{y:.0f}" width="{rnd.uniform(200, w):.0f}" height="{th}" fill="{RED if rnd.random() < 0.12 else col}" opacity="{rnd.choice([0.2, 0.45, 0.8, 1])}"/>'
        y += th + rnd.choice([6, 14, 30, 60])
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs><filter id="sm{seed}" x="-30%" width="160%"><feGaussianBlur stdDeviation="22 0"/></filter></defs>'
            f'<rect width="{w}" height="{h}" fill="{bg}"/><g filter="url(#sm{seed})">{g}</g><g opacity=".9">{g}</g></svg>')


def chevrons(w, h, col=RED, bg=NIGHT):
    """nested outline chevrons — the overtake (after the Verstappen key art)"""
    g = ""
    for i in range(7):
        s = 160 + i * 140
        g += f'<path d="M{-s * 0.2} {-s} L{s * 0.55} 0 L{-s * 0.2} {s}" fill="none" stroke="{col if i % 3 == 0 else "#1c2a8a"}" stroke-width="{10 if i % 3 == 0 else 22}" opacity="{1 - i * 0.1:.2f}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{bg}"/><g transform="translate({w * 0.55} {h * 0.5})">{g}</g></svg>'


def halftone(w, h, col=RED, bg=NIGHT, fx=0.8, fy=0.25):
    g = ""
    for i in range(0, w + 14, 14):
        for j in range(0, h + 14, 14):
            d = math.hypot(i - w * fx, j - h * fy) / math.hypot(w, h)
            r = 6.2 * (1 - d * 1.5)
            if r > 0.5:
                g += f'<circle cx="{i}" cy="{j}" r="{r:.1f}" fill="{col}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{bg}"/>{g}</svg>'


# ------------------------------------------------------------------ graphic devices
def bars(h, col=ICE, op=(0.35, 0.6, 1.0)):
    """/// speed bars on the 15-degree lean"""
    ws = (0.08, 0.14, 0.24)
    x, g = 0, ""
    for wd, o in zip(ws, op):
        bw = wd * h
        g += f'<polygon points="{x + h * K:.1f},0 {x + bw + h * K:.1f},0 {x + bw:.1f},{h} {x:.1f},{h}" fill="{col}" opacity="{o}"/>'
        x += bw + h * 0.09
    return f'<svg width="{x + h * K:.0f}" height="{h}" style="display:block">{g}</svg>'


def strike(w, h=10, col=RED):
    return f'<svg width="{w}" height="{h}" style="display:block"><polygon points="{h * K:.1f},0 {w},0 {w - h * K:.1f},{h} 0,{h}" fill="{col}"/></svg>'


def hud_corners(w, h, col=ICE, L=26, sw=2):
    p = f'M0 {L} V0 H{L} M{w - L} 0 H{w} V{L} M{w} {h - L} V{h} H{w - L} M{L} {h} H0 V{h - L}'
    return f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0;overflow:visible"><path d="{p}" fill="none" stroke="{col}" stroke-width="{sw}"/></svg>'


def pbadge(txt, h, bg=RED, fg=ICE):
    return (f'<div style="display:inline-flex;align-items:center;justify-content:center;height:{h}px;padding:0 {h * 0.35:.0f}px;background:{bg};'
            f'clip-path:polygon({h * 0.27:.0f}px 0,100% 0,calc(100% - {h * 0.27:.0f}px) 100%,0 100%)">{T(txt, h * 0.5, HEAVY, fg, 0.9)}</div>')


def label(s, col=STEEL, size=13, ls=0.24):
    return f'<span class="mono" style="color:{col};font-size:{size}px;letter-spacing:{ls}em">{s}</span>'


def photo(src, w, h, pos="50% 50%", tone="mono", extra=""):
    filt = {"mono": "grayscale(1) contrast(1.25) brightness(.82)", "warm": "grayscale(.2) contrast(1.15) brightness(.85) saturate(1.1)", "full": "contrast(1.08)"}[tone]
    return f'<div style="position:absolute;width:{w}px;height:{h}px;overflow:hidden;{extra}"><img src="{ASSET}{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};filter:{filt}"/></div>'


# ------------------------------------------------------------------ social templates (full size)
def post_raceday():
    W, Hh = 1080, 1350
    return f'''<div class="tpl" data-snap="post-race-day" style="width:{W}px;height:{Hh}px;background:{NIGHT}">
      {photo("williams.jpg", W, Hh, "48% 40%", "mono")}
      <div style="position:absolute;inset:0;background:linear-gradient(180deg,{NIGHT}e6 0%,transparent 34%,transparent 52%,{NIGHT} 92%)"></div>
      <div style="position:absolute;left:0;top:0;width:{W}px;height:{Hh}px;opacity:.92;mix-blend-mode:screen;clip-path:polygon(62% 0,100% 0,100% 58%,38% 100%,0 100%,0 92%)">{slipstream(W, Hh, RED, "#000", 3, -60, 0.5)}</div>
      <div style="position:absolute;left:72px;top:72px;display:flex;align-items:center;gap:22px">{sym("a-ligature-rev", 84)}{label("AKKI MEISTER · SIM RACING", ICE, 15)}</div>
      <div style="position:absolute;right:72px;top:96px">{label("ROUND 05 / 12", STEEL, 15)}</div>
      <div style="position:absolute;left:66px;top:880px">{T("RACE", 150, HEAVY, ICE, 0.8)}<div style="height:18px"></div>{T("DAY", 150, HEAVY, RED, 0.8)}</div>
      <div style="position:absolute;left:72px;bottom:84px;display:flex;align-items:center;gap:26px">{pbadge("SPA", 52, ICE, NIGHT)}{label("GT3 · 60 MIN · LIVE 20:30 IST", ICE, 17)}</div>
      <div style="position:absolute;right:72px;bottom:90px">{bars(46, RED)}</div>
    </div>'''


def post_result():
    W, Hh = 1080, 1350
    return f'''<div class="tpl" data-snap="post-result" style="width:{W}px;height:{Hh}px;background:{NIGHT}">
      <div style="position:absolute;inset:0">{apex_mesh(W, Hh, "#3a0a12", NIGHT, 9, (1, 0))}</div>
      {photo("podium-p1-jeddah.jpg", 560, 760, "50% 30%", "mono", f"right:0;top:150px;clip-path:polygon(18% 0,100% 0,100% 100%,0 100%)")}
      <div style="position:absolute;right:0;top:150px;width:560px;height:760px;background:linear-gradient(90deg,{NIGHT} 0%,transparent 40%)"></div>
      <div style="position:absolute;left:72px;top:72px">{lockup(64)}</div>
      <div style="position:absolute;left:58px;top:300px">{T("P1", 420, HEAVY, RED, 0.6)}</div>
      <div style="position:absolute;left:72px;top:760px">{label("RESULT · RACEATWILL F1 · JEDDAH", STEEL, 16)}</div>
      <div style="position:absolute;left:72px;top:808px">{T("WINNER", 92, HEAVY, ICE, 1)}</div>
      <div style="position:absolute;left:72px;top:1010px;right:72px;display:grid;grid-template-columns:repeat(3,1fr);border-top:2px solid #262833">
        {"".join(f'<div style="padding:26px 0 0">{label(k, STEEL, 14)}<div style="margin-top:14px">{T(v, 44, BOLD, ICE if i else RED, 1)}</div></div>' for i, (k, v) in enumerate((("BEST LAP", "1:26.004"), ("GAP", "+2.418"), ("POLE", "YES"))))}
      </div>
      <div style="position:absolute;left:72px;bottom:64px">{label("TEMPLATE · REPLACE THE NUMBERS", "#3b3e48", 12)}</div>
    </div>'''


def post_teaser():
    W, Hh = 1080, 1350
    flare = (f'<svg width="900" height="900" viewBox="-450 -450 900 900" style="position:absolute;left:90px;top:220px">'
             f'<defs><radialGradient id="gl"><stop offset="0" stop-color="{RED}" stop-opacity=".55"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient></defs>'
             f'<circle r="330" fill="url(#gl)"/><path d="M0 -420 L10 -10 L420 0 L10 10 L0 420 L-10 10 L-420 0 L-10 -10 Z" fill="{ICE}"/>'
             f'<path d="M-260 -430 Q-120 0 -260 430" fill="none" stroke="{ICE}" stroke-opacity=".35" stroke-width="1.5"/></svg>')
    return f'''<div class="tpl" data-snap="post-teaser" style="width:{W}px;height:{Hh}px;background:#0d0e13">
      <div style="position:absolute;inset:0;background-image:url(&quot;data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='.22'/></svg>&quot;)"></div>
      {flare}
      <div style="position:absolute;left:96px;top:150px">{T("SOMETHING NEW", 64, LIGHT * 1.6, ICE, 1.8)}<div style="height:22px"></div>{T("IS COMING.", 64, LIGHT * 1.6, ICE, 1.8)}</div>
      <div style="position:absolute;left:96px;top:1080px;display:flex;gap:120px">{label("FASTER.", STEEL, 18, .5)}{label("SHARPER.", STEEL, 18, .5)}{label("CLOSER.", STEEL, 18, .5)}</div>
      <div style="position:absolute;left:96px;bottom:90px;display:flex;align-items:center;gap:22px">{sym("a-ligature-rev", 64)}{label("01 · 11 · 2026", ICE, 15)}</div>
    </div>'''


def post_data():
    W, Hh = 1080, 1350
    rnd = random.Random(3)
    pts = " ".join(f"{60 + i * 13.8:.0f},{360 - (120 + 90 * math.sin(i * 0.11) + 40 * math.sin(i * 0.37)):.0f}" for i in range(70))
    pts2 = " ".join(f"{60 + i * 13.8:.0f},{360 - (110 + 90 * math.sin(i * 0.11 - 0.15) + 38 * math.sin(i * 0.37 - 0.2)):.0f}" for i in range(70))
    stats = (("TOP SPEED", "287", "KM/H"), ("BRAKE POINT", "112", "M"), ("THROTTLE", "68", "%"), ("DELTA", "-0.21", "S"))
    return f'''<div class="tpl" data-snap="post-data" style="width:{W}px;height:{Hh}px;background:{CARBON}">
      <div style="position:absolute;left:0;top:0;width:{W}px;height:260px;opacity:.6">{interference(W, 260, 12)}</div>
      <div style="position:absolute;left:0;top:0;width:{W}px;height:260px;background:linear-gradient(180deg,transparent,{CARBON})"></div>
      <div style="position:absolute;left:72px;top:72px;display:flex;align-items:center;gap:20px">{sym("a-ligature-rev", 70)}{label("DATA DROP · 07", ICE, 15)}</div>
      <div style="position:absolute;left:66px;top:300px">{T("SECTOR 2", 104, HEAVY, ICE, 0.9)}<div style="height:20px"></div>{T("BREAKDOWN", 104, HEAVY, COBALT, 0.9)}</div>
      <div style="position:absolute;left:72px;top:560px;width:936px;height:380px;border:2px solid #262833;background:#0e1016">
        {hud_corners(936, 380, RED, 22, 3)}
        <svg width="936" height="380" style="position:absolute;left:0;top:0">
          {"".join(f'<line x1="0" x2="936" y1="{y}" y2="{y}" stroke="#20232c"/>' for y in (95, 190, 285))}
          <polyline points="{pts2}" fill="none" stroke="{STEEL}" stroke-width="2" stroke-dasharray="7 7"/>
          <polyline points="{pts}" fill="none" stroke="{RED}" stroke-width="4"/></svg>
        <div style="position:absolute;left:20px;top:16px">{label("SPEED · ME vs REFERENCE", STEEL, 12)}</div></div>
      <div style="position:absolute;left:72px;top:990px;right:72px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px">
        {"".join(f'<div style="border-top:3px solid {RED if i == 0 else "#2a2d38"};padding-top:20px">{label(k, STEEL, 12)}<div style="display:flex;align-items:flex-end;gap:8px;margin-top:14px">{T(v, 46, BOLD, ICE, 0.9)}{label(u, STEEL, 13)}</div></div>' for i, (k, v, u) in enumerate(stats))}
      </div>
      <div style="position:absolute;left:72px;bottom:64px">{label("TEMPLATE · ILLUSTRATIVE NUMBERS", "#3b3e48", 12)}</div>
    </div>'''


def story_countdown():
    W, Hh = 1080, 1920
    lights = "".join(f'<div style="width:118px;height:118px;border-radius:50%;background:{RED if i < 3 else "#2a1015"};box-shadow:{"0 0 60px " + RED if i < 3 else "none"};border:6px solid #000"></div>' for i in range(5))
    return f'''<div class="tpl" data-snap="story-lights-out" style="width:{W}px;height:{Hh}px;background:{NIGHT}">
      <div style="position:absolute;inset:0;opacity:.85">{chevrons(W, Hh)}</div>
      <div style="position:absolute;left:0;right:0;top:120px;display:flex;justify-content:center">{sym("a-ligature-rev", 110)}</div>
      <div style="position:absolute;left:90px;top:520px;padding:34px 40px;background:#111;display:flex;gap:26px;border-radius:26px;border:4px solid #222">{lights}</div>
      <div style="position:absolute;left:0;right:0;top:820px;display:flex;flex-direction:column;align-items:center;gap:30px">{label("LIGHTS OUT IN", ICE, 22, .6)}{T("02:14:09", 170, HEAVY, ICE, 0.8)}</div>
      <div style="position:absolute;left:0;right:0;top:1180px;display:flex;justify-content:center">{pbadge("SPA · GT3", 70, RED, ICE)}</div>
      <div style="position:absolute;left:0;right:0;bottom:180px;display:flex;justify-content:center">{label("TAP TO SET A REMINDER", STEEL, 18)}</div>
    </div>'''


def story_onboard():
    W, Hh = 1080, 1920
    return f'''<div class="tpl" data-snap="story-on-board" style="width:{W}px;height:{Hh}px;background:{NIGHT}">
      {photo("fs-bw.jpg", W, Hh, "50% 55%", "mono")}
      <div style="position:absolute;inset:0;background:linear-gradient(180deg,{NIGHT}cc 0%,transparent 25%,transparent 60%,{NIGHT} 95%)"></div>
      <div style="position:absolute;left:60px;top:200px;width:960px;height:1300px">{hud_corners(960, 1300, ICE, 46, 3)}</div>
      <div style="position:absolute;left:96px;top:236px">{label("ON BOARD · CAR 10", ICE, 18)}</div>
      <div style="position:absolute;right:96px;top:236px">{label("● REC", RED, 18)}</div>
      <div style="position:absolute;left:0;top:930px;width:{W}px;display:flex;justify-content:center">{strike(560, 8, RED)}</div>
      <div style="position:absolute;left:84px;top:1560px">{T("FROM CAD", 108, HEAVY, ICE, 0.8)}<div style="height:16px"></div>{T("TO CURBS.", 108, HEAVY, RED, 0.8)}</div>
      <div style="position:absolute;left:90px;bottom:120px;display:flex;align-items:center;gap:20px">{sym("a-ligature-rev", 60)}{label("FORMULA STUDENT · DSCE", STEEL, 15)}</div>
    </div>'''


def story_schedule():
    W, Hh = 1080, 1920
    rows = (("FRI", "PRACTICE", "18:00"), ("SAT", "QUALIFYING", "19:30"), ("SUN", "RACE", "20:30"), ("SUN", "DEBRIEF", "22:00"))
    r = "".join(f'''<div style="display:grid;grid-template-columns:150px 1fr auto;align-items:center;padding:40px 0;border-bottom:2px solid #262833">
        {label(d, RED if i == 2 else STEEL, 20)}{T(n, 54, HEAVY if i == 2 else BOLD, ICE, 0.9)}{T(t, 46, LIGHT * 1.7, ICE, 1.2)}</div>''' for i, (d, n, t) in enumerate(rows))
    return f'''<div class="tpl" data-snap="story-schedule" style="width:{W}px;height:{Hh}px;background:{NIGHT}">
      <div style="position:absolute;left:0;top:0;width:{W}px;height:720px">{slipstream(W, 720, RED, NIGHT, 7, -58, 0.7)}</div>
      <div style="position:absolute;left:0;top:300px;width:{W}px;height:420px;background:linear-gradient(180deg,transparent,{NIGHT})"></div>
      <div style="position:absolute;left:84px;top:140px">{sym("b-launch-rev", 150, style="margin-left:-20px")}</div>
      <div style="position:absolute;left:84px;top:560px">{label("RACE WEEKEND · ROUND 05", STEEL, 20)}</div>
      <div style="position:absolute;left:78px;top:620px">{T("SCHEDULE", 128, HEAVY, ICE, 0.8)}</div>
      <div style="position:absolute;left:84px;right:84px;top:880px">{r}</div>
      <div style="position:absolute;left:84px;bottom:130px">{label("ALL TIMES IST · AKKI MEISTER", STEEL, 16)}</div>
    </div>'''


ICONS = {
    "SIM": '<rect x="-30" y="-24" width="60" height="34" /><path d="M-22 26 A24 24 0 0 1 22 26"/><line x1="0" y1="10" x2="0" y2="18"/>',
    "KART": '<circle r="28"/><circle r="10"/><line x1="10" y1="0" x2="28" y2="0"/><line x1="-6" y1="8" x2="-16" y2="23"/><line x1="-6" y1="-8" x2="-16" y2="-23"/>',
    "DATA": '<polyline points="-32,16 -18,16 -10,-18 0,12 8,-4 16,8 22,-26 32,-26"/>',
    "BUILD": '<polygon points="0,-30 26,-15 26,15 0,30 -26,15 -26,-15"/><circle r="10"/>',
    "COACH": '<polyline points="-24,10 0,-12 24,10"/><polyline points="-24,28 0,6 24,28"/><line x1="-28" x2="28" y1="-28" y2="-28"/>',
    "PODIUM": '<rect x="-12" y="-22" width="24" height="50"/><rect x="-36" y="-4" width="24" height="32"/><rect x="12" y="6" width="24" height="22"/>',
}


def highlight(name, size=150, ring=RED):
    return (f'<svg viewBox="-60 -60 120 120" width="{size}" height="{size}" style="display:block"><circle r="57" fill="none" stroke="{ring}" stroke-width="3"/>'
            f'<circle r="50" fill="{CARBON}"/><g transform="skewX(-15)" fill="none" stroke="{ICE}" stroke-width="3.2" stroke-linejoin="miter">{ICONS[name]}</g></svg>')


# ------------------------------------------------------------------ board panels
def head(n, title, dark=True):
    c = ICE if dark else NIGHT
    return (f'<div style="position:absolute;left:64px;top:50px;display:flex;align-items:center;gap:22px;z-index:5">{label(n, RED, 13)}{label(title, c, 13)}'
            f'<span style="width:120px;height:1px;background:{c};opacity:.25"></span>{label("AKKI MEISTER · BRAND SYSTEM · R3", c if dark else "#666", 13)}</div>')


def panel(pid, inner, bg=NIGHT):
    return f'<section data-snap="{pid}" style="width:1600px;height:1000px;background:{bg}">{inner}</section>'


def scaled(html, w, h, s, left, top, extra=""):
    return f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w * s:.0f}px;height:{h * s:.0f}px;overflow:hidden;{extra}"><div style="transform:scale({s});transform-origin:0 0;width:{w}px;height:{h}px">{html}</div></div>'


def build():
    P = []
    # 01 cover
    P.append(panel("01-cover", f'''
      <div style="position:absolute;inset:0;opacity:.95;clip-path:polygon(64% 0,100% 0,100% 100%,40% 100%)">{slipstream(1600, 1000, RED, NIGHT, 11, -58)}</div>
      <div style="position:absolute;left:110px;top:250px">{sym("a-ligature-rev", 440)}</div>
      <div style="position:absolute;left:120px;top:690px">{T("AKKI MEISTER", 56, HEAVY, ICE, 1.1)}<div style="display:flex;align-items:center;gap:16px;margin-top:20px"><span style="width:44px;height:4px;background:{RED}"></span>{T("MOTORSPORT · PERFORMANCE", 14, LIGHT * 1.3, STEEL, 2.4)}</div></div>
      <div style="position:absolute;left:64px;bottom:44px">{label("AM-01 · LIGATURE MARK · LEAN 15° · NIGHT / SIGNAL RED / ICE", STEEL, 11)}</div>
      {head("01", "IDENTITY")}'''))
    # 02 origin: from the diary to the mark
    steps = [("SKETCH", "Your diary: flat-topped A, ///AM, the box."), ("SQUARE", "Square it up: 7-unit cap, 45° chamfers, one stroke weight."), ("SHARE", "A's right leg becomes M's left stem: one ligature."), ("LEAN", "Lean 15°. Cut the V at exactly 60° and 45°.")]
    sk = "".join(f'<div style="position:absolute;left:{700 + (i % 2) * 450}px;top:{150 + (i // 2) * 170}px;width:420px">{label(f"0{i + 1} · {a}", RED, 13)}<p class="body">{b}</p></div>' for i, (a, b) in enumerate(steps))
    lig_open = (f'<svg viewBox="0 0 256 256" width="260" height="260" style="position:absolute;left:820px;top:520px">'
                f'{SYM["a-ligature-black"].replace(f"fill={chr(34)}{NIGHT}{chr(34)}", "fill=" + chr(34) + "none" + chr(34) + " stroke=" + chr(34) + ICE + chr(34) + " stroke-width=" + chr(34) + "1.5" + chr(34))}</svg>')
    P.append(panel("02-origin", f'''
      <div style="position:absolute;left:64px;top:120px;width:560px;height:820px;overflow:hidden;clip-path:polygon(0 0,calc(100% - 40px) 0,100% 40px,100% 100%,0 100%)"><img src="{DIARY}" style="width:100%;height:100%;object-fit:cover;object-position:50% 38%;filter:grayscale(1) contrast(1.2) brightness(.9)"/></div>
      <div style="position:absolute;left:84px;top:140px">{label("31 JAN · THE ORIGINAL BRIEF", ICE, 12)}</div>
      {sk}
      <div style="position:absolute;left:700px;top:520px;width:860px;height:400px;border:1px solid #23252e">{hud_corners(860, 400, RED, 20, 2)}
        <svg width="860" height="400" style="position:absolute">{"".join(f'<line x1="0" x2="860" y1="{y}" y2="{y}" stroke="#1b1d25"/>' for y in range(40, 400, 40))}</svg></div>
      <div style="position:absolute;left:740px;top:560px">{sym("a-ligature-rev", 320)}</div>
      <div style="position:absolute;left:1120px;top:600px">{sym("b-launch-color", 210, fg=ICE)}</div>
      <div style="position:absolute;left:1360px;top:640px">{sym("c-box-rev", 160)}</div>
      {head("02", "ORIGIN")}'''))
    # 03 logo system
    tiles = [("PRIMARY · LIGATURE", ICE, sym("a-ligature-color", 230)), ("REVERSED", NIGHT, sym("a-ligature-rev", 230)), ("ON SIGNAL RED", RED, sym("a-ligature-rev", 230, fg=ICE, acc=NIGHT)),
             ("EXTENDED · ///AM", NIGHT, sym("b-launch-rev", 240)), ("BADGE · GRID BOX", ICE, sym("c-box-color", 220)), ("ONE COLOUR", "#D9DBE0", sym("a-ligature-black", 230))]
    g = ""
    for i, (cap, bg, art) in enumerate(tiles):
        x, y = 64 + (i % 3) * 496, 110 + (i // 3) * 290
        cc = NIGHT if bg in (ICE, "#D9DBE0") else ICE
        g += f'<div class="tile" style="left:{x}px;top:{y}px;width:480px;height:274px;background:{bg}">{art}<div style="position:absolute;left:20px;bottom:16px">{label(cap, cc, 11)}</div></div>'
    g += f'<div class="tile" style="left:64px;top:700px;width:728px;height:250px;background:{ICE}">{lockup(110, NIGHT, RED, "#6d717c")}<div style="position:absolute;left:20px;bottom:16px">{label("HORIZONTAL LOCKUP", NIGHT, 11)}</div></div>'
    g += f'<div class="tile" style="left:808px;top:700px;width:728px;height:250px;background:{NIGHT};border:1px solid #1f2129">{lockup(110)}<div style="position:absolute;left:20px;bottom:16px">{label("HORIZONTAL · REVERSED", ICE, 11)}</div></div>'
    P.append(panel("03-logo-system", g + head("03", "LOGO SYSTEM"), "#101117"))
    # 04 typeface
    P.append(panel("04-typeface", f'''
      <div style="position:absolute;left:64px;top:120px">{label("DISPLAY · MEISTER (CONSTRUCTED)", RED, 13)}</div>
      <div style="position:absolute;left:60px;top:160px">{T("MEISTER", 190, HEAVY, ICE, 1.0)}</div>
      <div style="position:absolute;left:64px;top:400px">{T("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 56, BOLD, ICE, 1.0)}</div>
      <div style="position:absolute;left:64px;top:490px">{T("0123456789 P1 1:26.004 +0.214", 56, BOLD, STEEL, 1.0)}</div>
      <div style="position:absolute;left:64px;top:600px;display:flex;gap:70px;align-items:flex-end">
        <div>{label("HEAVY", STEEL, 11)}<div style="margin-top:12px">{T("LIGHTS OUT", 54, HEAVY, ICE, .9)}</div></div>
        <div>{label("BOLD", STEEL, 11)}<div style="margin-top:12px">{T("RACE DAY", 54, BOLD, ICE, 1)}</div></div>
        <div>{label("LIGHT · WIDE TRACKING", STEEL, 11)}<div style="margin-top:12px">{T("PERFORMANCE", 40, LIGHT, ICE, 2.0)}</div></div></div>
      <div style="position:absolute;left:64px;top:780px;width:720px">{label("TEXT · BAI JAMJUREE", RED, 13)}<p class="body" style="font-size:22px;color:{ICE}">Labels, captions and data in Bai Jamjuree, a free Google font with a technical, Thai-engineered feel. Uppercase with wide tracking for labels; sentence case for body copy.</p></div>
      <div style="position:absolute;left:900px;top:780px;width:620px">{label("RULES", RED, 13)}<p class="body">Every letter: 7-unit cap, one stroke weight, 45° chamfers, 15° lean. Headlines in Heavy, numbers in Bold, taglines in Light with wide tracking. Never stretch, never outline-stroke, never set it upright.</p></div>
      {head("04", "TYPEFACE")}'''))
    # 05 colour
    sw = [("NIGHT", NIGHT, "8 9 13", "62%"), ("CARBON", CARBON, "20 22 29", "14%"), ("SIGNAL RED", RED, "232 17 45", "12%"), ("ICE", ICE, "242 243 245", "8%"), ("COBALT", COBALT, "36 64 255", "3%"), ("STEEL", STEEL, "138 143 153", "1%")]
    g = ""
    for i, (n, hx, rgb, pct) in enumerate(sw):
        x = 64 + i * 248
        fg = NIGHT if n in ("ICE", "STEEL") else ICE
        g += (f'<div style="position:absolute;left:{x}px;top:120px;width:232px;height:560px;background:{hx};border:1px solid #20222a">'
              f'<div style="position:absolute;left:22px;top:24px">{T(n, 20, BOLD, fg, 1)}</div>'
              f'<div style="position:absolute;left:22px;bottom:70px">{label(hx.upper(), fg, 13)}</div><div style="position:absolute;left:22px;bottom:44px">{label("RGB " + rgb, fg, 11)}</div>'
              f'<div style="position:absolute;left:22px;bottom:18px">{label("USE " + pct, fg, 11)}</div></div>')
    bar = "".join(f'<div style="height:40px;flex:{p.strip("%")};background:{hx}"></div>' for _, hx, _, p in sw)
    g += f'<div style="position:absolute;left:64px;top:720px;width:1472px;display:flex;border:1px solid #20222a">{bar}</div>'
    g += f'<div style="position:absolute;left:64px;top:800px;width:1100px">{label("PROPORTION", RED, 13)}<p class="body">Mostly Night. Signal Red is the voice: one red thing per frame, usually the strike, the crossbar or the result. Cobalt only for sim racing and data, never next to red as equals.</p></div>'
    P.append(panel("05-colour", g + head("05", "COLOUR"), "#0d0e13"))
    # 06 patterns
    pats = [("SLIPSTREAM", slipstream(480, 360, RED, NIGHT, 21, -58)), ("INTERFERENCE", interference(480, 360, 31)), ("APEX MESH", apex_mesh(480, 360, RED, NIGHT, 4, (1, 1))),
            ("KERB RAILS", kerb_rails(480, 360)), ("FLAG FADE", flag_fade(480, 360)), ("OVERTAKE", chevrons(480, 360)),
            ("SMEAR", smear(480, 360, 8)), ("HEAT", halftone(480, 360)), ("SLIPSTREAM · COBALT", slipstream(480, 360, COBALT, NAVY, 13, -58))]
    g = ""
    for i, (n, art) in enumerate(pats):
        x, y = 64 + (i % 3) * 496, 104 + (i // 3) * 296
        g += f'<div class="tile" style="left:{x}px;top:{y}px;width:480px;height:280px;overflow:hidden">{art}<div style="position:absolute;left:14px;bottom:12px;background:{NIGHT};padding:4px 8px">{label(n, ICE, 11)}</div></div>'
    P.append(panel("06-patterns", g + head("06", "PATTERNS"), "#101117"))
    # 07 devices + highlights
    hl = "".join(f'<div style="text-align:center">{highlight(n, 150)}<div style="margin-top:12px">{label(n, ICE, 11)}</div></div>' for n in ICONS)
    P.append(panel("07-devices", f'''
      <div style="position:absolute;left:64px;top:120px">{label("THE STRIKE", RED, 13)}<div style="margin-top:26px">{strike(620, 16)}</div><p class="body" style="width:620px">One red strike per layout. It underlines the headline, splits the frame, or fires out of the ligature.</p></div>
      <div style="position:absolute;left:820px;top:120px">{label("SPEED BARS", RED, 13)}<div style="margin-top:26px;display:flex;gap:28px;align-items:flex-end">{bars(90, ICE)}{bars(60, RED, (1, 1, 1))}{bars(40, STEEL)}</div></div>
      <div style="position:absolute;left:64px;top:390px;width:440px;height:200px">{hud_corners(440, 200, ICE, 22, 2)}<div style="position:absolute;left:24px;top:22px">{label("HUD FRAME", RED, 13)}</div><div style="position:absolute;left:24px;bottom:22px">{label("AM-01 / LAP 05 / S2", STEEL, 12)}</div></div>
      <div style="position:absolute;left:560px;top:390px">{label("RESULT BADGES", RED, 13)}<div style="margin-top:26px;display:flex;gap:18px">{pbadge("P1", 70)}{pbadge("P2", 70, ICE, NIGHT)}{pbadge("P3", 70, CARBON, ICE)}{pbadge("POLE", 70, COBALT, ICE)}</div></div>
      <div style="position:absolute;left:64px;top:650px">{label("HIGHLIGHT COVERS · INSTAGRAM", RED, 13)}</div>
      <div style="position:absolute;left:64px;top:700px;display:flex;gap:70px">{hl}</div>
      <div style="position:absolute;left:1180px;top:390px;display:flex;flex-direction:column;gap:22px">{label("AVATARS", RED, 13)}<div style="display:flex;gap:22px">
        <div style="width:150px;height:150px;border-radius:50%;background:{RED};display:flex;align-items:center;justify-content:center">{sym("a-ligature-rev", 120, fg=ICE, acc=NIGHT)}</div>
        <div style="width:150px;height:150px;border-radius:50%;background:{NIGHT};border:3px solid #2a2c34;display:flex;align-items:center;justify-content:center">{sym("a-ligature-rev", 120)}</div></div></div>
      {head("07", "DEVICES & ICONS")}'''))
    # 08 social overview (scaled templates)
    posts = [post_raceday(), post_result(), post_teaser(), post_data()]
    g = "".join(scaled(p, 1080, 1350, 0.3, 64 + i * 340, 110) for i, p in enumerate(posts))
    stories = [story_countdown(), story_onboard(), story_schedule()]
    g += "".join(scaled(s, 1080, 1920, 0.218, 1424 - (2 - i) * 0, 0) for i, s in enumerate([]))
    g += f'<div style="position:absolute;left:64px;top:540px">{label("POSTS · 1080 × 1350", RED, 12)}</div>'
    g += "".join(scaled(s, 1080, 1920, 0.2, 64 + i * 236, 580) for i, s in enumerate(stories))
    g += f'<div style="position:absolute;left:780px;top:600px;width:760px">{label("STORIES · 1080 × 1920", RED, 12)}<p class="body">Every template uses the same grid: logo top-left, one headline in MEISTER Heavy, one red strike or badge, labels in Bai. Photos go monochrome so the red always wins.</p></div>'
    g += f'<div style="position:absolute;left:780px;top:800px;display:flex;gap:20px">{"".join(f"<div>{highlight(n, 96)}</div>" for n in list(ICONS)[:6])}</div>'
    P.append(panel("08-social", g + head("08", "SOCIAL TEMPLATES"), "#101117"))
    return P, posts + stories


CSS = f"""
@font-face {{ font-family: Bai; src: url({NM}/@fontsource/bai-jamjuree/files/bai-jamjuree-latin-600-normal.woff2) format('woff2'); font-weight: 600; }}
@font-face {{ font-family: Bai; src: url({NM}/@fontsource/bai-jamjuree/files/bai-jamjuree-latin-500-normal.woff2) format('woff2'); font-weight: 500; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; }}
section, .tpl {{ position: relative; overflow: hidden; margin-bottom: 40px; }}
.mono {{ font-family: Bai; font-weight: 600; text-transform: uppercase; white-space: nowrap; }}
.body {{ font-family: Bai; font-weight: 500; font-size: 18px; line-height: 1.5; color: #b7bac2; margin-top: 12px; }}
.tile {{ position: absolute; display: flex; align-items: center; justify-content: center; clip-path: polygon(0 0, calc(100% - 26px) 0, 100% 26px, 100% 100%, 26px 100%, 0 calc(100% - 26px)); }}
"""

if __name__ == "__main__":
    panels, tpls = build()
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(panels)}{"".join(tpls)}</body></html>'
    open(R3 + "system.html", "w", encoding="utf-8").write(html)
    print("system.html written", len(html) // 1024, "KB")
