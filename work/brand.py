"""AKKI MEISTER brand board: one HTML page, one <section> per board panel (screenshotted by snap.js)."""
import math, re
from gen import d_of, wordmark, ORANGE, INK, WHITE
import gen2

R2 = "../round2/"
FONT = "file:///C:/Users/admin/Akki-Portfolio-main/3d_portfolio/node_modules"


def inner(name):
    s = open(R2 + name + ".svg").read()
    s = s[s.index("</title>") + 8: s.rindex("</svg>")]
    return re.sub(r'<rect x="-9999"[^>]*/>', "", s)


SP_C, SP_W, SP_O, SP_K = inner("sliced-peaks-color"), inner("sliced-peaks-white"), inner("sliced-peaks-orange"), inner("sliced-peaks-black")
ST_K, ST_W, ST_O = inner("apex-star-black"), inner("apex-star-white"), inner("apex-star-orange")
SEAL_O, SEAL_K = inner("meister-seal-orange"), inner("meister-seal-black")
WM, WMW = wordmark("AKKI MEISTER", 64, 800, 125, 0.012)
TAG, TAGW = wordmark("MOTORSPORT  ·  PERFORMANCE", 16, 600, 125, 0.34, oblique=0)


def sym(content, size, extra=""):
    return f'<svg viewBox="0 0 256 256" width="{size}" height="{size}" style="{extra}">{content}</svg>'


def word(color, h=64, extra="", w=None):
    size = f'width="{w}"' if w else f'height="{h}"'
    return f'<svg viewBox="-4 -52 {WMW + 8:.0f} 60" {size} style="{extra};display:block"><path fill="{color}" d="{WM}"/></svg>'


def tag(color, h=16, extra=""):
    return f'<svg viewBox="0 -13 {TAGW + 2:.0f} 16" height="{h}" style="{extra}"><path fill="{color}" d="{TAG}"/></svg>'


def lean_lines(w, h, gap, color, width=1, k=math.tan(math.radians(20))):
    n = int((w + h * k) / gap) + 2
    return "".join(f'<line x1="{i * gap - h * k:.1f}" y1="{h}" x2="{i * gap:.1f}" y2="0" stroke="{color}" stroke-width="{width}"/>' for i in range(n))


# ------------------------------------------------------------------ patterns
def pat_slices(w, h, seed=3):
    import random
    rnd = random.Random(seed)
    k = math.tan(math.radians(20))
    out, y = [], 18
    while y < h - 10:
        th = rnd.choice([6, 10, 14, 22, 30])
        x = rnd.uniform(-200, w * 0.5)
        while x < w:
            L = rnd.uniform(60, 420)
            col = ORANGE if rnd.random() < 0.08 else ("#F4F2EE" if rnd.random() < 0.55 else "#3a3936")
            pts = [(x + th * k, y), (x + L + th * k, y), (x + L, y + th), (x, y + th)]
            out.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{col}"/>')
            x += L + rnd.uniform(20, 240)
        y += th + rnd.choice([8, 12, 18, 30])
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{INK}"/>'
            f'<g filter="url(#smear)">{"".join(out)}</g><g opacity="0.85">{"".join(out[::3])}</g></svg>')


def pat_construction(w, h):
    k = math.tan(math.radians(20))
    hz = "".join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}" stroke="#cfcac2" stroke-width="1"/>' for y in range(40, h, 64))
    dims = "".join(f'<g transform="translate({x} {h - 40})"><line x1="0" x2="64" y1="0" y2="0" stroke="{INK}" stroke-width="1"/><line x1="0" x2="0" y1="-5" y2="5" stroke="{INK}"/><line x1="64" x2="64" y1="-5" y2="5" stroke="{INK}"/><text x="32" y="-8" text-anchor="middle" font-family="Bai" font-weight="600" font-size="10" fill="{INK}">{v}</text></g>' for x, v in ((60, "20°"), (220, "9 U"), (380, "34 U")))
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="#F4F2EE"/>{hz}'
            f'{lean_lines(w, h, 32, "#d9d4cc")}{lean_lines(w, h, 192, ORANGE, 1.4)}{dims}</svg>')


def pat_stars(w, h):
    out = []
    import random
    rnd = random.Random(7)
    for i in range(0, w, 90):
        for j in range(0, h, 90):
            s = rnd.choice([18, 26, 40])
            col = ORANGE if rnd.random() < 0.12 else "#F4F2EE"
            op = rnd.choice([0.25, 0.5, 1.0]) if col != ORANGE else 1
            out.append(f'<g transform="translate({i + rnd.uniform(-10, 10):.0f} {j + rnd.uniform(-10, 10):.0f}) scale({s / 256:.3f})" opacity="{op}">{ST_W if col != ORANGE else ST_O}</g>')
    dots = f'<pattern id="ht" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.2" fill="#2a2927"/></pattern>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>{dots}</defs><rect width="{w}" height="{h}" fill="{INK}"/><rect width="{w}" height="{h}" fill="url(#ht)"/>{"".join(out)}</svg>'


def pat_bands(w, h):
    k = math.tan(math.radians(20))
    bands = ""
    for i, (x, bw, col, op) in enumerate(((-60, 260, ORANGE, 1), (300, 90, ORANGE, 0.55), (430, 30, ORANGE, 0.35), (520, 340, "#1c1b1a", 1), (760, 14, "#F4F2EE", 0.8), (800, 6, "#F4F2EE", 0.5))):
        bands += f'<polygon points="{x + h * k:.0f},0 {x + bw + h * k:.0f},0 {x + bw:.0f},{h} {x:.0f},{h}" fill="{col}" opacity="{op}"/>'
    pin = "".join(f'<polygon points="{x + h * k:.0f},0 {x + 2 + h * k:.0f},0 {x + 2:.0f},{h} {x:.0f},{h}" fill="#F4F2EE" opacity="0.12"/>' for x in range(-100, w + 100, 24))
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{INK}"/>{pin}{bands}</svg>'


def pat_hud(w, h):
    rows = [("MODE", "PUSH"), ("LAP", "01 / 15"), ("SECTOR", "02"), ("DELTA", "-0.214"), ("THROTTLE", "100%"), ("BRAKE BIAS", "56.5"), ("TYRE", "SOFT"), ("STATUS", "ARMED")]
    txt = ""
    for i, (k, v) in enumerate(rows):
        x, y = 40 + (i % 2) * 220, 70 + (i // 2) * 44
        hot = k in ("DELTA", "STATUS")
        txt += (f'<text x="{x}" y="{y}" font-family="Bai" font-weight="600" font-size="9" letter-spacing="1.6" fill="#7d7973">{k}</text>'
                f'<text x="{x}" y="{y + 18}" font-family="Bai" font-weight="600" font-size="15" letter-spacing="1.2" fill="{ORANGE if hot else "#e9e6df"}">{v}</text>')
    trace = "M40 330 " + " ".join(f"L{40 + i * 8} {300 - 26 * math.sin(i * 0.5) - 10 * math.sin(i * 1.7):.1f}" for i in range(52))
    bars = "".join(f'<rect x="{w - 160 + i * 4}" y="{h - 64}" width="{(i * 7) % 3 + 1}" height="30" fill="#bdb8b0"/>' for i in range(30))
    cross = "".join(f'<g transform="translate({x} {y})" stroke="#bdb8b0" stroke-width="1"><line x1="-7" x2="7" y1="0" y2="0"/><line x1="0" x2="0" y1="-7" y2="7"/></g>' for x, y in ((24, 24), (w - 24, 24), (24, h - 24), (w - 24, h - 24)))
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="#151413"/>{txt}'
            f'<line x1="40" x2="{w - 40}" y1="250" y2="250" stroke="#3a3936"/><path d="{trace}" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>{bars}{cross}'
            f'<text x="40" y="{h - 40}" font-family="Bai" font-weight="600" font-size="9" letter-spacing="1.6" fill="#7d7973">AM-01 / LOADING...</text></svg>')


def pat_halftone(w, h):
    dots = ""
    for i in range(0, w + 12, 12):
        for j in range(0, h + 12, 12):
            d = math.hypot(i - w * 0.75, j - h * 0.3) / math.hypot(w, h)
            r = max(0, 5.4 * (1 - d * 1.6))
            if r > 0.4:
                dots += f'<circle cx="{i}" cy="{j}" r="{r:.2f}" fill="{ORANGE}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{INK}"/>{dots}</svg>'


# ------------------------------------------------------------------ icons (thin line, in rings)
def icon(kind):
    s = 'fill="none" stroke="#F4F2EE" stroke-width="3" stroke-linejoin="miter" stroke-linecap="square"'
    k = {
        "Sim": f'<rect x="-26" y="-22" width="52" height="30" {s}/><path d="M-18 22 A20 20 0 0 1 18 22" {s}/><line x1="0" y1="8" x2="0" y2="16" {s}/>',
        "Kart": f'<circle r="24" {s}/><circle r="9" {s}/>' + "".join(f'<line x1="{9 * math.cos(a):.1f}" y1="{9 * math.sin(a):.1f}" x2="{24 * math.cos(a):.1f}" y2="{24 * math.sin(a):.1f}" {s}/>' for a in (0.3, 2.4, 4.5)),
        "Data": f'<polyline points="-28,14 -16,14 -10,-16 -2,10 6,-4 12,6 18,-22 28,-22" {s}/><line x1="-28" x2="28" y1="22" y2="22" {s} stroke-dasharray="3 5"/>',
        "Build": f'<polygon points="0,-26 22.5,-13 22.5,13 0,26 -22.5,13 -22.5,-13" {s}/><circle r="9" {s}/>',
        "Coach": f'<polyline points="-20,8 0,-10 20,8" {s}/><polyline points="-20,24 0,6 20,24" {s}/><line x1="-24" x2="24" y1="-24" y2="-24" {s}/>',
        "Move": f'<g transform="scale(0.24) translate(-128 -128)">{ST_W.replace("#FFFFFF", "#F4F2EE")}</g>',
    }[kind]
    return (f'<svg viewBox="-60 -60 120 120" width="150" height="150"><circle r="56" fill="none" stroke="#4a4844" stroke-width="5"/>'
            f'<circle r="47" fill="#121110"/><g transform="skewX(-20)">{k}</g></svg>')


# ------------------------------------------------------------------ page
CSS = f"""
@font-face {{ font-family: Archivo; src: url({FONT}/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2) format('woff2'); font-weight: 100 900; font-stretch: 62% 125%; }}
@font-face {{ font-family: Bai; src: url({FONT}/@fontsource/bai-jamjuree/files/bai-jamjuree-latin-600-normal.woff2) format('woff2'); font-weight: 600; }}
@font-face {{ font-family: Bai; src: url({FONT}/@fontsource/bai-jamjuree/files/bai-jamjuree-latin-500-normal.woff2) format('woff2'); font-weight: 500; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #2a2927; width: 1600px; }}
section {{ position: relative; width: 1600px; height: 1000px; overflow: hidden; }}
.mono {{ font-family: Bai; font-weight: 600; text-transform: uppercase; letter-spacing: .22em; font-size: 13px; }}
.disp {{ font-family: Archivo; font-variation-settings: 'wdth' 125; font-weight: 800; text-transform: uppercase; line-height: .9; }}
.lbl {{ position: absolute; left: 64px; top: 52px; display: flex; gap: 22px; align-items: center; }}
.tile {{ position: absolute; display: flex; align-items: center; justify-content: center; }}
.cap {{ position: absolute; left: 20px; bottom: 16px; }}
.chamfer {{ clip-path: polygon(0 0, calc(100% - 26px) 0, 100% 26px, 100% 100%, 26px 100%, 0 calc(100% - 26px)); }}
"""


def header(n, title, dark=True):
    c = "#F4F2EE" if dark else INK
    return (f'<div class="lbl"><span class="mono" style="color:{ORANGE}">{n}</span><span class="mono" style="color:{c}">{title}</span>'
            f'<span style="width:120px;height:1px;background:{c};opacity:.3"></span><span class="mono" style="color:{c};opacity:.5">AKKI MEISTER · BRAND ASSETS · R2</span></div>')


def build():
    k = math.tan(math.radians(20))
    S = []
    # 01 COVER
    S.append(f'''<section id="cover" style="background:{INK}">
      <svg class="tile" style="left:0;top:0" width="1600" height="1000">{lean_lines(1600, 1000, 46, "rgba(244,242,238,0.05)")}{lean_lines(1600, 1000, 276, "rgba(255,90,31,0.22)")}</svg>
      <div class="tile" style="left:120px;top:150px;width:640px;height:640px">{sym(SP_W, 640)}</div>
      <div style="position:absolute;left:820px;top:420px">{word("#F4F2EE", w=700)}<div style="display:flex;align-items:center;gap:18px;margin-top:22px"><span style="width:60px;height:5px;background:{ORANGE}"></span>{tag("#9A968F", 17)}</div></div>
      <div class="tile" style="left:1440px;top:80px">{sym(ST_O, 70)}</div>
      <div class="mono" style="position:absolute;left:64px;bottom:48px;color:#6d6a65;font-size:11px">AM-01 / PRIMARY MARK &nbsp;·&nbsp; LEAN 20° &nbsp;·&nbsp; SLICE 9U</div>
      <div class="mono" style="position:absolute;right:64px;bottom:48px;color:#6d6a65;font-size:11px">BLACK #0B0B0C &nbsp;·&nbsp; WHITE #F4F2EE &nbsp;·&nbsp; RACING ORANGE #FF5A1F</div>
      {header("01", "Identity")}
    </section>''')
    # 02 SYMBOL FAMILY
    tiles = [
        ("Primary · colour", "#F4F2EE", sym(SP_C, 250)), ("Primary · reversed", INK, sym(SP_W, 250)), ("Primary · on orange", ORANGE, sym(SP_O, 250)),
        ("Apex Star · secondary", INK, sym(ST_O, 230)), ("Meister Seal · tags & patches", "#F4F2EE", sym(SEAL_O, 190, "margin-top:-24px")), ("Primary · one colour", "#F4F2EE", sym(SP_K, 250)),
    ]
    g = ""
    for i, (cap, bg, art) in enumerate(tiles):
        x, y = 64 + (i % 3) * 496, 120 + (i // 3) * 300
        capc = INK if bg != INK else "#F4F2EE"
        g += f'<div class="tile chamfer" style="left:{x}px;top:{y}px;width:480px;height:284px;background:{bg}">{art}<span class="mono cap" style="color:{capc};opacity:.7;font-size:11px">{cap}</span></div>'
    lock = open(R2 + "lockup-horizontal.svg").read().replace("<svg ", '<svg height="150" ', 1)
    lock_r = open(R2 + "lockup-horizontal-reversed.svg").read().replace("<svg ", '<svg height="150" ', 1)
    g += f'<div class="tile chamfer" style="left:64px;top:730px;width:728px;height:220px;background:#F4F2EE">{lock}<span class="mono cap" style="color:{INK};opacity:.7;font-size:11px">Horizontal lockup</span></div>'
    g += f'<div class="tile chamfer" style="left:808px;top:730px;width:728px;height:220px;background:{INK}">{lock_r}<span class="mono cap" style="color:#F4F2EE;opacity:.7;font-size:11px">Horizontal · reversed</span></div>'
    S.append(f'<section id="family" style="background:#1a1918">{g}{header("02", "Symbol family")}</section>')
    # 03 CONSTRUCTION
    S.append(f'''<section id="construction" style="background:#F4F2EE">
      <svg class="tile" style="left:0;top:0" width="1600" height="1000">{lean_lines(1600, 1000, 40, "#e2ddd5")}
        {"".join(f'<line x1="0" x2="1600" y1="{y}" y2="{y}" stroke="#cfc9bf"/>' for y in (308, 436, 690))}</svg>
      <div class="tile" style="left:520px;top:150px;width:700px;height:700px">{sym(SP_K, 700, "opacity:.14;position:absolute")}<svg viewBox="0 0 256 256" width="700" height="700" style="position:absolute">{SP_K.replace('fill="#0B0B0C"', 'fill="none" stroke="#0B0B0C" stroke-width="0.6"').replace('fill="#0B0B0C" ', 'fill="none" stroke="#0B0B0C" stroke-width="0.6" ')}</svg></div>
      <div style="position:absolute;left:96px;top:240px;width:360px">
        <div class="mono" style="color:{ORANGE}">01 · Two peaks</div><p style="font-family:Bai;font-weight:500;font-size:17px;line-height:1.5;color:#3a3936;margin:8px 0 26px">Two sharp peaks share one centre foot: an M. Only the first has a crossbar, so it is also an A.</p>
        <div class="mono" style="color:{ORANGE}">02 · The lean</div><p style="font-family:Bai;font-weight:500;font-size:17px;line-height:1.5;color:#3a3936;margin:8px 0 26px">Everything leans 20°, the angle of the AH speed bars. Every right leg lands dead vertical.</p>
        <div class="mono" style="color:{ORANGE}">03 · The slice</div><p style="font-family:Bai;font-weight:500;font-size:17px;line-height:1.5;color:#3a3936;margin:8px 0 26px">One 9-unit cut through the peaks; the body trails 8 units behind. Speed, without drawing a speed line.</p>
      </div>
      <div class="mono" style="position:absolute;right:80px;top:286px;color:#8d877e;font-size:11px">CAP LINE</div>
      <div class="mono" style="position:absolute;right:80px;top:414px;color:#8d877e;font-size:11px">SLICE</div>
      <div class="mono" style="position:absolute;right:80px;top:668px;color:#8d877e;font-size:11px">BASELINE</div>
      {header("03", "Construction", dark=False)}
    </section>''')
    # 04 PATTERNS
    pats = [("Slice field", pat_slices(500, 400)), ("Construction grid", pat_construction(500, 400)), ("Apex stars", pat_stars(500, 400)),
            ("Diagonal bands", pat_bands(500, 400)), ("Data HUD", pat_hud(500, 400)), ("Halftone heat", pat_halftone(500, 400))]
    g = ""
    for i, (cap, art) in enumerate(pats):
        x, y = 64 + (i % 3) * 496, 120 + (i // 3) * 430
        capc = INK if "Construction" in cap else "#F4F2EE"
        g += f'<div class="tile chamfer" style="left:{x}px;top:{y}px;width:480px;height:410px;overflow:hidden">{art}<span class="mono cap" style="color:{capc};font-size:11px;background:{"#F4F2EE" if capc == INK else INK};padding:4px 8px">{cap}</span></div>'
    S.append(f'<section id="patterns" style="background:#1a1918"><svg width="0" height="0" style="position:absolute"><filter id="smear" x="-20%" width="140%"><feGaussianBlur stdDeviation="14 0"/></filter></svg>{g}{header("04", "Patterns")}</section>')
    # 05 ICONS
    names = ["Sim", "Kart", "Data", "Build", "Coach", "Move"]
    g = "".join(f'<div style="position:absolute;left:{110 + i * 236}px;top:330px;width:200px;text-align:center">{icon(n)}<div class="mono" style="color:#F4F2EE;margin-top:22px">{n}</div></div>' for i, n in enumerate(names))
    S.append(f'''<section id="icons" style="background:#0d0c0c">
      <svg class="tile" style="left:0;top:0" width="1600" height="1000">{lean_lines(1600, 1000, 46, "rgba(244,242,238,0.035)")}</svg>{g}
      <div class="mono" style="position:absolute;left:110px;top:640px;color:#6d6a65;width:1380px;line-height:1.8;font-size:12px">Thin 3-unit line · square caps · drawn on the same 20° lean · always inside a dark disc with a grey ring. For highlights, story covers and section markers.</div>
      {header("05", "Icon set")}</section>''')
    # 06 APPLICATIONS
    post = f'''<div class="chamfer" style="position:absolute;left:64px;top:110px;width:520px;height:520px;background:{INK};overflow:hidden">
        <div style="position:absolute;inset:0">{pat_bands(520, 520)}</div>
        <div class="disp" style="position:absolute;left:34px;top:46px;font-size:76px;color:#F4F2EE;font-style:italic">Lights<br/><span style="color:transparent;-webkit-text-stroke:2px #F4F2EE">out.</span></div>
        <div class="mono" style="position:absolute;left:36px;top:226px;color:#F4F2EE;background:{INK};padding:5px 9px;font-size:12px">Session 01 · Keep moving</div>
        <div style="position:absolute;right:30px;bottom:26px">{sym(SP_W, 110)}</div>
        <div style="position:absolute;left:34px;bottom:34px">{word("#F4F2EE", 24)}</div></div>'''
    story = f'''<div class="chamfer" style="position:absolute;left:610px;top:110px;width:292px;height:520px;background:{ORANGE};overflow:hidden">
        <svg style="position:absolute;inset:0" width="292" height="520">{lean_lines(292, 520, 22, "rgba(11,11,12,0.12)")}</svg>
        <div style="position:absolute;left:30px;top:60px">{sym(SP_K, 230)}</div>
        <div class="disp" style="position:absolute;left:26px;top:330px;font-size:40px;color:{INK};font-style:italic">Keep<br/>moving.</div>
        <div class="mono" style="position:absolute;left:28px;bottom:30px;color:{INK};font-size:10px">AKKI MEISTER · LAP 01</div></div>'''
    av = ""
    for i, (bg, art) in enumerate(((ORANGE, sym(SP_K, 120)), (INK, sym(SP_W, 120)), ("#F4F2EE", sym(SP_C, 120)))):
        av += f'<div style="position:absolute;left:{930 + i * 210}px;top:110px;width:180px;height:180px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 6px #3a3936">{art}</div>'
    av += f'<div class="mono" style="position:absolute;left:930px;top:312px;color:#9A968F;font-size:11px">Social avatars</div>'
    decal = f'''<div style="position:absolute;left:930px;top:350px;width:606px;height:280px;background:#d9d6d0;overflow:hidden" class="chamfer">
        <div style="position:absolute;left:24px;top:30px">{sym(SP_C, 120)}</div><div style="position:absolute;left:170px;top:40px">{sym(ST_K, 90)}</div>
        <div style="position:absolute;left:290px;top:30px">{sym(SEAL_O, 110)}</div><div style="position:absolute;left:420px;top:44px">{sym(SP_O, 100, "background:" + ORANGE)}</div>
        <div style="position:absolute;left:28px;top:180px">{word(INK, 44)}</div>
        <div class="mono" style="position:absolute;left:24px;bottom:14px;color:#6d6a65;font-size:10px">Decal sheet · helmet, rig, laptop</div></div>'''
    card = f'''<div style="position:absolute;left:64px;top:660px;width:520px;height:300px;background:{INK}" class="chamfer">
        <div style="position:absolute;inset:0">{pat_slices(520, 300, 5)}</div><div style="position:absolute;inset:0;background:linear-gradient(90deg,{INK} 45%,transparent)"></div>
        <div style="position:absolute;left:36px;top:40px">{sym(SP_W, 90)}</div>
        <div class="disp" style="position:absolute;left:40px;top:160px;font-size:28px;color:#F4F2EE;font-style:italic">Akshat Hegde</div>
        <div class="mono" style="position:absolute;left:42px;top:200px;color:{ORANGE};font-size:11px">Driver · Engineer · Builder</div>
        <div class="mono" style="position:absolute;left:42px;top:236px;color:#9A968F;font-size:10px;text-transform:none;letter-spacing:.1em">akshathegde.vercel.app</div></div>'''
    cap_patch = f'''<div style="position:absolute;left:610px;top:660px;width:292px;height:300px;background:#2b2a28" class="chamfer">
        <div style="position:absolute;left:66px;top:46px;transform:rotate(-4deg);filter:drop-shadow(0 6px 8px rgba(0,0,0,.5))">{sym(SEAL_O, 160)}</div>
        <div class="mono" style="position:absolute;left:24px;bottom:18px;color:#9A968F;font-size:10px">Woven patch · cap, jacket</div></div>'''
    jersey = f'''<div style="position:absolute;left:930px;top:660px;width:606px;height:300px;background:#F4F2EE;overflow:hidden" class="chamfer">
        <div style="position:absolute;inset:0;opacity:.9">{pat_construction(606, 300)}</div>
        <div style="position:absolute;left:40px;top:50px">{sym(SP_C, 150)}</div>
        <div style="position:absolute;left:216px;top:104px">{word(INK, w=350)}<div style="margin-top:12px">{tag("#6B6762", 11)}</div></div>
        <div class="mono" style="position:absolute;left:24px;bottom:14px;color:#6d6a65;font-size:10px">Website header · on the construction grid</div></div>'''
    S.append(f'<section id="applications" style="background:#1a1918">{post}{story}{av}{decal}{card}{cap_patch}{jersey}{header("06", "Applications")}</section>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(S)}</body></html>'


if __name__ == "__main__":
    open("../round2/brand-board.html", "w", encoding="utf-8").write(build())
    print("board written")
