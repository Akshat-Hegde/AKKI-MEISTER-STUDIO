"""Teaser story v3 (1080x1920), matching the three posts. Patterns / dither / glass kept subtle."""
import math, os, shutil
import launch as L, launch2 as L2, launch3 as L3, launch4 as L4
from launch import ICE, BLUE, NIGHT, STEEL, DEEP, K, MW, MH, mark, lockup, mono, kicker, frame, layer

SW, SH = 1080, 1920
SKY = "#5B7BFF"


def dim(html, o=.35):
    """pattern at low strength under a night veil"""
    return layer(html, f"opacity:{o}")


def glass(x, y, w, h, inner="", lean=True, uid="g"):
    off = h * K * 2 if lean else 0
    pts = f"{off:.0f},0 {w},0 {w - off:.0f},{h} 0,{h}"
    clip = f"polygon({off:.0f}px 0,100% 0,calc(100% - {off:.0f}px) 100%,0 100%)"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div style="position:absolute;inset:0;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);clip-path:{clip}"></div>'
            f'<svg width="{w}" height="{h}" style="position:absolute;inset:0;overflow:visible"><defs>'
            f'<linearGradient id="{uid}a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SKY}" stop-opacity=".32"/><stop offset=".6" stop-color="{BLUE}" stop-opacity=".12"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".04"/></linearGradient>'
            f'<linearGradient id="{uid}b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="{uid}c" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></linearGradient></defs>'
            f'<polygon points="{pts}" fill="url(#{uid}a)"/><polygon points="{pts}" fill="url(#{uid}b)"/><polygon points="{pts}" fill="none" stroke="url(#{uid}c)" stroke-width="1.5"/></svg>'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;padding:0 {40 + off:.0f}px">{inner}</div></div>')


def flat_panel(x0, y0, w, t, handle="@akki_meister"):
    off = t * K * 2.2
    x1 = x0 + w
    pts = f"{x0 + off:.0f},{y0} {x1:.0f},{y0} {x1 - off:.0f},{y0 + t} {x0},{y0 + t}"
    hatch = "".join(f'<line x1="{x:.0f}" y1="{y0 + t}" x2="{x + t * K * 2.2:.0f}" y2="{y0}" stroke="#F3F4F6" stroke-width="1.2"/>' for x in range(x0 - 40, x1 + 40, 14))
    dots = "".join(f'<rect x="{x0 + i}" y="{y0 + j}" width="5" height="5" fill="#5B7BFF"/>' for j in range(0, t, 8) for i in range(int(w * .55), w, 8)
                   if (i - w * .55) / (w * .45) > ((j // 8 * 3 + i // 8) % 5 + .5) / 5 * .9)
    svg = (f'<svg width="{SW}" height="{SH}" style="position:absolute;left:0;top:0"><defs>'
           f'<linearGradient id="pf" x1="0" x2="1"><stop offset="0" stop-color="#2440FF"/><stop offset=".55" stop-color="#2440FF" stop-opacity=".45"/><stop offset="1" stop-color="#2440FF" stop-opacity="0"/></linearGradient>'
           f'<linearGradient id="pm" x1="0" x2="1"><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>'
           f'<mask id="mk"><rect width="{SW}" height="{SH}" fill="url(#pm)"/></mask><clipPath id="pc"><polygon points="{pts}"/></clipPath></defs>'
           f'<polygon points="{pts}" fill="url(#pf)"/><g clip-path="url(#pc)"><g opacity=".14">{hatch}</g><g mask="url(#mk)" opacity=".55">{dots}</g></g>'
           f'<polygon points="{x0 + off:.0f},{y0} {x0 + off + 10:.0f},{y0} {x0 + 10},{y0 + t} {x0},{y0 + t}" fill="#F3F4F6"/></svg>')
    txt = (f'<div style="position:absolute;left:{x0 + off + 40:.0f}px;width:{w - off - 80:.0f}px;top:{y0}px;height:{t}px;display:flex;justify-content:space-between;align-items:center">'
           f'<span class="k" style="color:#F3F4F6;font-size:36px;letter-spacing:.12em;text-transform:none">{handle}</span>'
           f'<svg width="70" height="30" viewBox="0 0 64 28"><path d="M0 14 H58 M44 2 L60 14 L44 26" fill="none" stroke="#F3F4F6" stroke-width="3"/></svg></div>')
    return svg + txt


def fade_lines():
    lines = "".join(f'<line x1="{x}" y1="{SH}" x2="{x + SH * K:.0f}" y2="0" stroke="#F3F4F6" stroke-width="{1.4 if n % 6 == 0 else .8}"/>' for n, x in enumerate(range(-500, SW + 200, 22)))
    cob = "".join(f'<line x1="{x}" y1="{SH}" x2="{x + SH * K:.0f}" y2="0" stroke="#5B7BFF" stroke-width="1.6"/>' for x in (560, 680, 800))
    return (f'<svg width="{SW}" height="{SH}" style="position:absolute;left:0;top:0"><defs>'
            f'<radialGradient id="fm" cx=".85" cy=".95" r="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".55" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="fmk"><rect width="{SW}" height="{SH}" fill="url(#fm)"/></mask>'
            f'<linearGradient id="cm" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="cmk"><rect width="{SW}" height="{SH}" fill="url(#cm)"/></mask></defs>'
            f'<g mask="url(#fmk)" opacity=".28">{lines}</g><g mask="url(#cmk)" opacity=".5">{cob}</g></svg>')


def chequer_band(y0, sq=18, rows=4):
    cells = ""
    for c in range(-3, int(SW / sq) + 6):
        for r in range(rows):
            if (c + r) % 2:
                continue
            x, y = c * sq, y0 + r * sq
            d = min(1, abs((x + sq / 2) - SW / 2) / (SW / 2))
            op = (1 - d) ** 1.6 * (1 - r / rows * .75)
            if op < .02:
                continue
            dy = (rows - r) * sq
            cells += f'<polygon points="{x + dy * K:.1f},{y} {x + sq + dy * K:.1f},{y} {x + sq + (dy - sq) * K:.1f},{y + sq} {x + (dy - sq) * K:.1f},{y + sq}" fill="#F3F4F6" opacity="{op * .55:.2f}"/>'
    return f'<svg width="{SW}" height="{SH}" style="position:absolute;left:0;top:0">{cells}</svg>'


def dither_beam(w, h, cell=8):
    """ordered dither of a 12-degree light beam rising from the bottom, plus a soft horizon under the logo"""
    B8 = [[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
          [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25], [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]
    g = []
    for j in range(0, h, cell):
        for i in range(0, w, cell):
            u = (i - (h - j) * K) / w                       # position across the leaning beam
            beam = math.exp(-((u - .32) / .16) ** 2) * (j / h) ** 1.4
            horizon = math.exp(-((j - h * .71) / (h * .035)) ** 2) * .5
            v = min(1, beam + horizon)
            t = (B8[(j // cell) % 8][(i // cell) % 8] + .5) / 64
            if v > t:
                c = SKY if v > .7 else BLUE
                g.append(f'<rect x="{i}" y="{j}" width="{cell - 2}" height="{cell - 2}" fill="{c}"/>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{"".join(g)}</svg>'


def pulse_frames(w, h, cx=540, cy=900):
    """nested 12-degree parallelogram outlines around the logo, fading outward; every 4th in cobalt"""
    g = ""
    for n in range(1, 22):
        hw, hh = 300 + n * 46, 170 + n * 46
        sk = hh * K
        pts = f"{cx - hw + sk:.0f},{cy - hh:.0f} {cx + hw + sk:.0f},{cy - hh:.0f} {cx + hw - sk:.0f},{cy + hh:.0f} {cx - hw - sk:.0f},{cy + hh:.0f}"
        cob = n % 4 == 0
        op = max(0, 1 - n / 22) ** 1.3 * (.9 if cob else .45)
        g += f'<polygon points="{pts}" fill="none" stroke="{SKY if cob else ICE}" stroke-width="{1.6 if cob else .8}" opacity="{op:.2f}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%"><rect width="{w}" height="{h}" fill="{NIGHT}"/>{g}</svg>'


def foot():
    return f'<div style="position:absolute;left:90px;right:90px;bottom:120px;display:flex;justify-content:space-between">{mono("AKKI MEISTER", STEEL, 18)}{mono("2026", STEEL, 18)}</div>'


def st(n, inner):
    return frame(f"story-{n:02d}", SW, SH, f'<div style="position:absolute;inset:0;background:{NIGHT}"></div>' + inner)


def frames():
    F = []
    # 01 teaser
    F.append(st(1, dim(L2.p_flare(SW, SH, 9), .55) +
                f'<div style="position:absolute;left:90px;top:300px">{kicker("COMING SOON", BLUE, 22)}</div>'
                f'<div style="position:absolute;left:90px;bottom:560px" class="h">SOMETHING<br/>IS <span style="color:{BLUE}">COMING.</span></div>' + foot()))
    # 02 same passion
    F.append(st(2, dim(L4.p_dither(SW, SH, 9, .85, .05), .45) +
                layer("", f"background:linear-gradient(180deg,{NIGHT}00 0%,{NIGHT} 55%)") +
                f'<div style="position:absolute;left:90px;top:640px" class="h"><span style="font-size:112px">SAME PASSION.<br/>SAME VISION.<br/><span style="color:{BLUE}">NEW IDENTITY.</span></span></div>' + foot()))
    # 03 three lanes (glass cards)
    lanes = [("01", "SIM RACING", "rigs · grids · racecraft"), ("02", "MOTORSPORT", "karts · Formula Student · track days"), ("03", "BEHIND THE SCENES", "the people, the prep, the process")]
    cards = "".join(glass(90, 600 + i * 250, 900, 190,
                          f'<div>{mono(n, SKY, 18)}<div class="k" style="color:{ICE};font-size:34px;letter-spacing:.12em;margin-top:12px">{t}</div>'
                          f'<div class="b" style="font-size:20px;margin-top:8px;color:{STEEL}">{s}</div></div>', uid=f"l{i}") for i, (n, t, s) in enumerate(lanes))
    F.append(st(3, dim(L.p_bar_field(SW, SH), .22) +
                f'<div style="position:absolute;left:90px;top:300px">{kicker("THREE LANES", BLUE, 22)}</div>'
                f'<div style="position:absolute;left:90px;top:380px" class="h"><span style="font-size:100px">ONE <span style="color:{BLUE}">DRIVE.</span></span></div>' + cards + foot()))
    # 04 on the rig
    F.append(st(4, dim(L2.p_hud(SW, SH), .6) + layer("", f"background:linear-gradient(0deg,{NIGHT} 0%,{NIGHT}ee 22%,{NIGHT}00 40%)") +
                f'<div style="position:absolute;left:90px;bottom:560px">{kicker("SIM RACING", BLUE, 22)}</div>'
                f'<div style="position:absolute;left:90px;bottom:420px" class="h">ON THE <span style="color:{BLUE}">RIG.</span></div>'
                f'<div style="position:absolute;left:90px;bottom:330px;width:860px" class="b">Real racecraft, one lap at a time.</div>' + foot()))
    # 05 every line has a reason (mini construction)
    s = 900 / MW
    mx, my = 90, 820
    sw = 1 / s
    g = (f'<svg width="{SW}" height="{SH}" style="position:absolute;inset:0">'
         + "".join(f'<line x1="0" x2="{SW}" y1="{my + v * s:.0f}" y2="{my + v * s:.0f}" stroke="{c}" stroke-opacity="{o}" stroke-dasharray="{d}"/>'
                   for v, c, o, d in ((0, ICE, .18, ""), (100, ICE, .18, ""), (61.8, SKY, .6, "6 6")))
         + f'<g transform="translate({mx} {my}) scale({s})"><rect x="0" y="0" width="100" height="100" fill="none" stroke="#C8A96A" stroke-opacity=".18" stroke-width="{sw}"/>'
         + "".join(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c:.2f}" height="{c:.2f}" fill="none" stroke="#C8A96A" stroke-opacity=".14" stroke-width="{sw}"/>' for a, b, c in __import__("breakdown").golden(100, 0, 161.8, 100)[0])
         + f'<path d="{" ".join(__import__("breakdown").golden(100, 0, 161.8, 100)[1])}" fill="none" stroke="#C8A96A" stroke-opacity=".4" stroke-width="{1.2 * sw}"/>'
         + f'<path d="{L.BODY_D}" fill="{ICE}" fill-opacity=".06" stroke="{ICE}" stroke-width="{1.4 * sw}" fill-rule="evenodd"/>'
         + "".join(f'<path d="{d}" fill="{BLUE}" fill-opacity="{o}" stroke="{SKY}" stroke-width="{sw}"/>' for d, o in zip(L.BARS_D, (1, .58, .28))) + "</g></svg>")
    specs = "".join(f'<div style="flex:1;border-top:2px solid {BLUE if i == 0 else "#2a3150"};padding-top:16px"><div class="h" style="font-size:52px;text-transform:none">{a}</div>'
                    f'<div class="b" style="font-size:17px;margin-top:8px;color:{STEEL}">{b}</div></div>'
                    for i, (a, b) in enumerate((("13:8:5", "bars ÷ φ"), ("12°", "one lean"), ("φ²", "2.618 : 1"))))
    F.append(st(5, g + f'<div style="position:absolute;left:90px;top:300px">{kicker("THE MARK", BLUE, 22)}</div>'
                f'<div style="position:absolute;left:90px;top:380px" class="h"><span style="font-size:104px">EVERY LINE<br/>HAS A <span style="color:{BLUE}">REASON.</span></span></div>'
                f'<div style="position:absolute;left:90px;right:90px;top:1300px;display:flex;gap:28px">{specs}</div>' + foot()))
    # 06 built to move
    F.append(st(6, dim(L3.p_speedlines(SW, SH), .55) +
                f'<div style="position:absolute;left:90px;right:90px;top:780px">{mark(900)}</div>'
                f'<div style="position:absolute;left:90px;bottom:460px" class="h">BUILT<br/>TO <span style="color:{BLUE}">MOVE.</span></div>' + foot()))
    # 07 reveal
    F.append(st(7, dim(pulse_frames(SW, SH), .7) +
                f'<div style="position:absolute;left:90px;right:90px;top:640px">{lockup(900)}</div>'
                f'<div style="position:absolute;left:0;right:0;top:1180px;text-align:center">{mono("SIM RACING · MOTORSPORT · BEHIND THE SCENES", ICE, 20)}</div>'))
    # 08 follow the journey: flat panel, fading lines, full lockup, fading chequer
    F.append(st(8, fade_lines() +
                f'<div style="position:absolute;left:90px;top:360px" class="h">FOLLOW<br/>THE <span style="color:{BLUE}">JOURNEY.</span></div>'
                + flat_panel(90, 780, 900, 130, handle="") +
                f'<div style="position:absolute;left:0;right:0;top:1080px;display:flex;justify-content:center">{lockup(640)}</div>'
                + chequer_band(1560) + foot()))
    return F


if __name__ == "__main__":
    open("stories.html", "w", encoding="utf-8").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{L.CSS}</style></head><body>{"".join(frames())}</body></html>')
    print("ok")
