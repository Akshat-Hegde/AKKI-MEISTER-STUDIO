"""AKKI MEISTER launch v3: final pattern set (kept + refined), transparent sticker pack, posts/stories, one showcase HTML."""
import math, random, os, shutil, re
import launch as L
import launch2 as L2
from launch import mark, lockup, kicker, mono, frame, layer, NIGHT, ICE, BLUE, STEEL, DEEP, K, BODY_D, BARS_D, MW, MH

ROOT = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/"
OUT = ROOT + "AKKI-MEISTER-LAUNCH/"
SKY, VIO = "#5B7BFF", "#7B5CFF"


def wrap(w, h, inner, defs="", bg=NIGHT):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{b}{inner}</svg>'


# ---------------------------------------------------------------- refined patterns
def p_shards(w, h, seed=4):
    """05 SHARDS: layered 12° aero planes with gradient fills, hairline edges and one hot edge."""
    rnd = random.Random(seed)
    defs = (f'<linearGradient id="sh1" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
            f'<linearGradient id="sh2" x1="0" x2="1"><stop offset="0" stop-color="{SKY}" stop-opacity=".5"/><stop offset="1" stop-color="{DEEP}" stop-opacity="0"/></linearGradient>')
    g = ""
    for i in range(16):
        y = rnd.uniform(-20, h)
        x = rnd.uniform(-w * .3, w * .8)
        L_, t = rnd.uniform(w * .25, w * .8), rnd.choice((8, 16, 28, 46))
        pts = [(x + t * K * 4, y), (x + L_, y), (x + L_ - t * K * 4 - t * 1.4, y + t), (x, y + t)]
        p = " ".join(f"{a:.0f},{b:.0f}" for a, b in pts)
        kind = rnd.random()
        if kind < .3:
            g += f'<polygon points="{p}" fill="url(#sh1)" opacity="{rnd.choice((.5, .8, 1))}"/>'
        elif kind < .5:
            g += f'<polygon points="{p}" fill="url(#sh2)"/>'
        g += f'<polygon points="{p}" fill="none" stroke="{ICE}" stroke-width=".8" opacity="{rnd.choice((.12, .22, .35))}"/>'
        if i % 5 == 0:
            g += f'<line x1="{pts[1][0]:.0f}" y1="{pts[1][1]:.0f}" x2="{pts[2][0]:.0f}" y2="{pts[2][1]:.0f}" stroke="{SKY}" stroke-width="2.4"/>'
    return wrap(w, h, g, defs)


def p_speedlines(w, h, seed=8):
    """10 SPEED LINES: gradient streaks with glow cores, φ lengths, densest through the centre band."""
    rnd = random.Random(seed)
    defs = (f'<linearGradient id="sl" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".8" stop-color="{SKY}"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            f'<linearGradient id="sli" x1="0" x2="1"><stop offset="0" stop-color="{ICE}" stop-opacity="0"/><stop offset="1" stop-color="{ICE}" stop-opacity=".9"/></linearGradient>'
            f'<filter id="slg" x="-20%" y="-300%" width="140%" height="700%"><feGaussianBlur stdDeviation="3"/></filter>')
    g = ""
    for _ in range(int(h / 4)):
        y = rnd.gauss(h / 2, h / 5)
        L_ = rnd.choice((40, 65, 105, 170, 275, 445))
        x = rnd.uniform(-L_, w)
        th = rnd.choice((1, 1, 1.5, 2.5, 4))
        fill = "url(#sl)" if rnd.random() < .5 else "url(#sli)"
        op = max(.05, 1 - abs(y - h / 2) / (h / 2)) * rnd.uniform(.4, 1)
        g += f'<rect x="{x:.0f}" y="{y:.0f}" width="{L_}" height="{th}" rx="{th / 2}" fill="{fill}" opacity="{op:.2f}"/>'
        if th >= 2.5:
            g += f'<rect x="{x:.0f}" y="{y - 2:.0f}" width="{L_}" height="{th + 4}" fill="{SKY}" opacity="{op * .4:.2f}" filter="url(#slg)"/>'
    return wrap(w, h, g, defs)


def p_rails(w, h):
    """12 RAILS: outlined 12° rails receding, gradient strokes, the racing line lit with a glow."""
    defs = (f'<linearGradient id="rl" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{ICE}" stop-opacity=".55"/><stop offset="1" stop-color="{ICE}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="rlb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{SKY}"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".2"/></linearGradient>'
            f'<filter id="rg" x="-50%" y="-10%" width="200%" height="120%"><feGaussianBlur stdDeviation="8"/></filter>')
    g = ""
    n = 11
    for i in range(n):
        x = w * .08 + i * (w * .84 / n)
        bw = w * .84 / n * .62
        p = f"{x + h * K:.0f},0 {x + bw + h * K:.0f},0 {x + bw:.0f},{h} {x:.0f},{h}"
        if i == 6:
            g += f'<polygon points="{p}" fill="{BLUE}" opacity=".35" filter="url(#rg)"/><polygon points="{p}" fill="none" stroke="url(#rlb)" stroke-width="3"/>'
        else:
            g += f'<polygon points="{p}" fill="none" stroke="url(#rl)" stroke-width="1" opacity="{.4 + .6 * (1 - abs(i - 6) / 6):.2f}"/>'
    return wrap(w, h, g, defs)


def p_dots(w, h):
    """13 SIGNAL DOTS: dot matrix, size and colour graded along the 12° diagonal (deep → cobalt → ice core)."""
    g = ""
    for y in range(0, h, 11):
        for x in range(0, w, 11):
            d = abs((x - (h - y) * K * 3.5) - w * .45) / w
            r = 3.4 * (1 - d * 2.2)
            if r > .35:
                col = ICE if d < .05 else SKY if d < .14 else BLUE
                g += f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{col}" opacity="{min(1, .3 + r / 3):.2f}"/>'
    defs = f'<radialGradient id="dg" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient>'
    return wrap(w, h, g, defs, "url(#dg)")


def p_construction(w, h):
    """11 CONSTRUCTION: refined blueprint — 12° rails, φ guides, dimension ticks, cobalt bars."""
    base = L.p_construction(w, h)
    ticks = "".join(f'<line x1="{x}" x2="{x}" y1="{h - 30}" y2="{h - (22 if x % 50 else 14)}" stroke="{ICE}" stroke-opacity=".35"/>' for x in range(0, w, 10))
    ticks += "".join(f'<line y1="{y}" y2="{y}" x1="12" x2="{20 if y % 50 else 28}" stroke="{ICE}" stroke-opacity=".35"/>' for y in range(0, h, 10))
    return base.replace("</svg>", ticks + "</svg>")


PATTERNS = [("01", "BAR FIELD", "The three bars as a running rhythm.", L.p_bar_field),
            ("02", "PINSTRIPE", "Hairlines broken by 13:8:5 cobalt runs.", L2.p_pinstripe),
            ("03", "SHARDS", "Layered 12° aero planes, gradient filled.", p_shards),
            ("04", "SPEED LINES", "Gradient streaks with glowing cores.", p_speedlines),
            ("05", "CONSTRUCTION", "The mark's blueprint: rails, φ guides, ticks.", p_construction),
            ("06", "RAILS", "Receding 12° rails, the racing line lit.", p_rails),
            ("07", "SIGNAL DOTS", "Dot matrix graded along the 12° diagonal.", p_dots)]


# ---------------------------------------------------------------- STICKERS (transparent)
def sticker(w, h, inner, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{defs}</defs>{inner}</svg>'


GLOW = '<filter id="gw" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{s}"/></filter>'


def st_streak():
    d = (f'<linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".75" stop-color="{SKY}"/><stop offset="1" stop-color="#fff"/></linearGradient>' + GLOW.format(s=10))
    return sticker(1200, 120, f'<rect x="0" y="45" width="1200" height="30" rx="15" fill="{BLUE}" opacity=".6" filter="url(#gw)"/><rect x="0" y="56" width="1200" height="8" rx="4" fill="url(#a)"/>', d)


def st_beam():
    d = (f'<linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="{VIO}" stop-opacity="0"/><stop offset=".5" stop-color="{BLUE}" stop-opacity=".9"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/></linearGradient>' + GLOW.format(s=18))
    p = f"{900 * K:.0f},0 {180 + 900 * K:.0f},0 180,900 0,900"
    return sticker(520, 900, f'<g transform="translate(60 0)"><polygon points="{p}" fill="url(#a)" opacity=".5" filter="url(#gw)"/><polygon points="{p}" fill="url(#a)" opacity=".8"/></g>', d)


def st_bars():
    g = "".join(f'<polygon points="{x + 600 * K:.0f},0 {x + bw + 600 * K:.0f},0 {x + bw:.0f},600 {x:.0f},600" fill="url(#f{i})"/>' for i, (x, bw) in enumerate(((0, 50), (80, 80), (190, 130))))
    d = "".join(f'<linearGradient id="f{i}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{BLUE}" stop-opacity="{o}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>' for i, o in enumerate((.3, .6, 1)))
    return sticker(460, 600, g, d)


def st_chequer():
    sq, g = 28, ""
    for c in range(24):
        for r in range(2):
            if (c + r + 1) % 2 == 0:
                x, y = 10 + c * sq, r * sq
                g += (f'<polygon points="{x + sq * (2 - r) * K:.1f},{y} {x + sq + sq * (2 - r) * K:.1f},{y} {x + sq + sq * (1 - r) * K:.1f},{y + sq} '
                      f'{x + sq * (1 - r) * K:.1f},{y + sq}" fill="{ICE}" opacity="{(c + 1) / 24:.2f}"/>')
    return sticker(700, 60, g)


def st_flare():
    d = (f'<radialGradient id="a"><stop offset="0" stop-color="#cfd8ff" stop-opacity=".9"/><stop offset=".4" stop-color="{BLUE}" stop-opacity=".35"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="h" x1="0" x2="1"><stop offset="0" stop-color="{SKY}" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/></linearGradient>')
    s, t = 230, 9
    return sticker(600, 600, f'<g transform="translate(300 300)"><circle r="200" fill="url(#a)"/><rect x="-300" y="-1.5" width="600" height="3" fill="url(#h)"/>'
                   f'<path d="M0 {-s} L{t} {-t} L{s} 0 L{t} {t} L0 {s} L{-t} {t} L{-s} 0 L{-t} {-t} Z" fill="#fff"/><circle r="6" fill="#fff"/></g>', d)


def st_orb():
    d = (f'<radialGradient id="a" cx=".4" cy=".35"><stop offset="0" stop-color="{SKY}"/><stop offset=".5" stop-color="{BLUE}" stop-opacity=".6"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/></radialGradient>')
    return sticker(800, 800, f'<circle cx="400" cy="400" r="400" fill="url(#a)"/>', d)


def st_halftone():
    g = ""
    for y in range(0, 600, 14):
        for x in range(0, 900, 14):
            r = 6 * (1 - math.hypot((x - 450) / 450, (y - 300) / 300))
            if r > .4:
                g += f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{BLUE}"/>'
    return sticker(900, 600, g)


def st_brackets():
    s = f'stroke="{ICE}" stroke-width="4" fill="none"'
    return sticker(800, 500, f'<path d="M4 70 V4 H70 M730 4 H796 V70 M796 430 V496 H730 M70 496 H4 V430" {s}/><path d="M380 250 H420 M400 230 V270" stroke="{SKY}" stroke-width="3"/>')


def st_chevrons():
    g = "".join(f'<path d="M{i * 70} 0 L{i * 70 + 80} 100 L{i * 70} 200" fill="none" stroke="{BLUE}" stroke-width="22" opacity="{.15 + i * .2:.2f}"/>' for i in range(5))
    return sticker(440, 200, g)


def st_speed():
    rnd = random.Random(2)
    d = f'<linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="{ICE}" stop-opacity="0"/><stop offset="1" stop-color="{ICE}"/></linearGradient>'
    g = "".join(f'<rect x="{rnd.uniform(0, 400):.0f}" y="{y}" width="{rnd.choice((200, 320, 520, 700))}" height="{rnd.choice((2, 3, 5))}" rx="2" fill="url(#a)" opacity="{rnd.uniform(.3, 1):.2f}"/>' for y in range(0, 300, 14))
    return sticker(1100, 300, g, d)


def st_mark_glow():
    d = GLOW.format(s=14)
    b = "".join(f'<path fill="{BLUE}" fill-opacity="{o}" d="{p}"/>' for p, o in zip(BARS_D, (1, .58, .28)))
    inner = f'<path fill="{ICE}" fill-rule="evenodd" d="{BODY_D}"/>{b}'
    return sticker(int(MW + 60), int(MH + 60), f'<g transform="translate(30 30)"><g filter="url(#gw)" opacity=".7"><path fill="{BLUE}" d="{BODY_D}"/></g>{inner}</g>', d)


def st_rpm():
    g = "".join(f'<polygon points="{i * 46 + 30 * K:.0f},0 {i * 46 + 34 + 30 * K:.0f},0 {i * 46 + 34},30 {i * 46},30" fill="{BLUE if i < 10 else ICE if i < 13 else "#ff3b3b"}" opacity="{.35 + .65 * i / 14:.2f}"/>' for i in range(15))
    return sticker(700, 30, g)


STICKERS = [("glow-streak", st_streak), ("light-beam", st_beam), ("bar-fade", st_bars), ("chequer-fade", st_chequer), ("flare", st_flare),
            ("cobalt-orb", st_orb), ("halftone-glow", st_halftone), ("hud-brackets", st_brackets), ("chevrons", st_chevrons),
            ("speed-streaks", st_speed), ("mark-glow", st_mark_glow), ("rpm-strip", st_rpm)]


# ---------------------------------------------------------------- showcase
def standalone(fn, w=1600, h=1000):
    s = fn(w, h).replace('width="100%" height="100%"', f'width="{w}" height="{h}"', 1)
    return s.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)


def build():
    for d in ("logo", "patterns", "stickers", "posts", "story"):
        os.makedirs(OUT + d, exist_ok=True)
    for f in os.listdir(L.OUT + "logo"):
        shutil.copy(L.OUT + "logo/" + f, OUT + "logo/" + f)
    for n, name, _, fn in PATTERNS:
        open(OUT + f"patterns/{n}-{name.lower().replace(' ', '-')}.svg", "w", encoding="utf-8").write(standalone(fn))
    for n, fn in STICKERS:
        open(OUT + f"stickers/{n}.svg", "w", encoding="utf-8").write(fn())
    # posts + stories from v2 (teaser)
    for d in ("posts", "story"):
        for f in os.listdir(L.OUT + d):
            shutil.copy(L.OUT + d + "/" + f, OUT + d + "/" + f)

    def sec(title, sub, body):
        return f'<section><div class="sh"><h2>{title}</h2><p>{sub}</p></div>{body}</section>'

    logo = ('<div class="row">' + "".join(f'<div class="card"><img src="logo/{f}"/><span>{f}</span></div>' for f in ("lockup-dark.svg", "lockup-light.svg")) + "</div>")
    pats = '<div class="grid3">' + "".join(
        f'<div class="card"><img src="patterns/{n}-{name.lower().replace(" ", "-")}.svg"/><span><b>{n}</b> {name} · {note}</span></div>' for n, name, note, _ in PATTERNS) + "</div>"
    stk = '<div class="grid4">' + "".join(f'<div class="card chk"><img src="stickers/{n}.svg"/><span>{n}.svg · .png</span></div>' for n, _ in STICKERS) + "</div>"
    posts = '<div class="grid3">' + "".join(f'<div class="card"><img src="posts/{f}"/><span>{f}</span></div>' for f in sorted(os.listdir(OUT + "posts"))) + "</div>"
    story = '<div class="grid6">' + "".join(f'<div class="card"><img src="story/{f}"/><span>{f}</span></div>' for f in sorted(os.listdir(OUT + "story"))) + "</div>"
    css = f"""*{{margin:0;padding:0;box-sizing:border-box}} body{{background:{NIGHT};color:{ICE};font-family:'Clash',Arial,sans-serif;padding:60px 64px;max-width:1800px;margin:auto}}
@font-face{{font-family:Clash;src:url(../work/fonts/clash-grotesk.woff2)}}
header{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1d2230;padding-bottom:40px}} header img{{width:420px}}
header p{{color:{STEEL};letter-spacing:.3em;font-size:13px;text-transform:uppercase}}
section{{margin-top:70px}} .sh{{display:flex;align-items:baseline;gap:20px;border-top:2px solid {BLUE};padding-top:16px;margin-bottom:24px}}
h2{{font-size:26px;letter-spacing:.2em;text-transform:uppercase}} .sh p{{color:{STEEL};font-size:15px}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:20px}} .grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}} .grid6{{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}}
.card{{background:#0e1118;border:1px solid #1d2230;border-radius:10px;overflow:hidden}} .card img{{width:100%;display:block}}
.card span{{display:block;padding:10px 12px;color:{STEEL};font-size:13px}} .card b{{color:{BLUE}}}
.chk img{{height:200px;object-fit:contain;padding:18px;background:repeating-conic-gradient(#151925 0 25%,#0b0e15 0 50%) 0 0/22px 22px}}"""
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>AKKI MEISTER · launch kit</title><style>{css}</style></head><body>'
            f'<header><img src="logo/lockup-dark.svg"/><p>Identity · patterns · stickers · launch posts · launch story</p></header>'
            + sec("Logo", "cobalt ///AM · Clash Grotesk · inverted chequer finish", logo)
            + sec("Pattern system", "seven patterns, all derived from the mark · SVG in patterns/", pats)
            + sec("Stickers", "transparent SVG + PNG · drop on any Instagram post or story", stk)
            + sec("Teaser posts", "1080 × 1350", posts)
            + sec("Teaser story", "1080 × 1920 · post in order", story)
            + "</body></html>")
    open(OUT + "index.html", "w", encoding="utf-8").write(html)
    open(OUT + "README.md", "w", encoding="utf-8").write(
        "# AKKI MEISTER · launch kit\n\nOpen `index.html` to see everything.\n\n"
        "- `logo/`: final lockup, dark and light (SVG + PNG)\n- `patterns/`: 7 patterns as SVG (+ PNG)\n"
        "- `stickers/`: 12 transparent stickers as SVG + PNG for Instagram posts and stories\n"
        "- `posts/`: 6 teaser posts, 1080×1350\n- `story/`: 6-frame teaser story, 1080×1920\n")


if __name__ == "__main__":
    build()
    print("ok")
