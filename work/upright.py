"""Upright wordmarks + separator band under the final cobalt ///AM."""
import os, json, math
from typeiter import font, setline, body, bars, W, FADE
import mark10 as m
from tune import NIGHT, ICE, BLUE

OUT = "../FINAL-AM/upright/"
os.makedirs(OUT, exist_ok=True)
WN = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/node_modules/@fontsource/"
FS = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/fonts/"


def f_(n, w):
    return WN + f"{n}/files/{n}-latin-{w}-normal.woff2"


FONTS = [
    ("clash", "Clash Grotesk 600", FS + "clash-grotesk.woff2"),
    ("clashd", "Clash Display 600", FS + "clash-display.woff2"),
    ("bai", "Bai Jamjuree 600", f_("bai-jamjuree", 600)),
    ("panchang", "Panchang 600", FS + "panchang.woff2"),
    ("unbounded", "Unbounded 600", f_("unbounded", 600)),
    ("syne", "Syne 700", f_("syne", 700)),
    ("cabinet", "Cabinet Grotesk 700", FS + "cabinet-grotesk.woff2"),
    ("satoshi", "Satoshi 700", FS + "satoshi.woff2"),
    ("general", "General Sans 600", FS + "general-sans.woff2"),
    ("michroma", "Michroma", f_("michroma", 400)),
    ("tomorrow", "Tomorrow 600", f_("tomorrow", 600)),
    ("spacegrotesk", "Space Grotesk 600", f_("space-grotesk", 600)),
    ("orbitron", "Orbitron 700", f_("orbitron", 700)),
    ("chakra", "Chakra Petch 600", f_("chakra-petch", 600)),
    ("sora", "Sora 600", f_("sora", 600)),
]
CAP, PAD = 15.0, 14
G1, BAND, G2 = 13.0, 4.0, 11.0          # gap, separator band, gap
from shapely.geometry import box as _box
from shapely.ops import unary_union as _uu
_foot = _uu([body] + bars).intersection(_box(-1e4, 99.5, 1e4, 100.5)).bounds
XL, XR = _foot[0], _foot[2]              # baseline extents: foot of first bar -> foot of the M
SW = XR - XL
K = math.tan(math.radians(12))


def separator(kind, fg, y):
    return f'<g transform="translate({XL:.3f} 0)">' + _sep(kind, fg, y) + "</g>"


def _sep(kind, fg, y):
    W = SW
    h = BAND
    if kind == "hairline":
        return f'<rect x="0" y="{y + h / 2 - .45:.2f}" width="{W:.2f}" height=".9" fill="{fg}" opacity=".35"/>'
    if kind == "cobalt":
        return (f'<defs><linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".25"/>'
                f'<stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient></defs>'
                f'<rect x="0" y="{y + h / 2 - 1:.2f}" width="{W:.2f}" height="2" fill="url(#cg)"/>')
    if kind == "ticks":
        out = ""
        for j in range(61):
            x = j * W / 60
            big = j % 5 == 0
            out += (f'<rect x="{x - .35:.2f}" y="{y + (0 if big else h * .45):.2f}" width=".7" height="{h if big else h * .55:.2f}" '
                    f'fill="{fg}" opacity="{.7 if big else .35}"/>')
        return out
    if kind == "hatch":
        out, x = "", 0.0
        while x < W - 2:
            op = 1 - x / W * .85
            out += f'<polygon points="{x + h * K:.2f},{y} {x + 1.6 + h * K:.2f},{y} {x + 1.6:.2f},{y + h} {x:.2f},{y + h}" fill="{BLUE}" opacity="{op:.2f}"/>'
            x += 4.2
        return out
    if kind == "chequer":
        s, out = h / 2, ""
        n = int(W / s)
        for c in range(n):
            for r in range(2):
                if (c + r) % 2 == 0:
                    out += f'<rect x="{c * s:.2f}" y="{y + r * s:.2f}" width="{s:.2f}" height="{s:.2f}" fill="{fg}" opacity="{max(.08, 1 - c / n):.2f}"/>'
        return out
    if kind == "bars":
        segs = [(0, .14, .28), (.15, .22, .58), (.23, 1, 1)]
        return "".join(f'<rect x="{a * W:.2f}" y="{y + h / 2 - 1:.2f}" width="{(b - a) * W - .8:.2f}" height="2" fill="{BLUE}" opacity="{o}"/>' for a, b, o in segs)
    import math as _m
    PHI = (1 + 5 ** .5) / 2
    mid = y + h / 2
    def line(x0, x1, t=.9, col=None, op=1):
        return f'<rect x="{x0:.2f}" y="{mid - t / 2:.2f}" width="{x1 - x0:.2f}" height="{t}" fill="{col or fg}" opacity="{op}"/>'
    if kind == "double":
        return f'<rect x="0" y="{y + .6:.2f}" width="{W:.2f}" height=".7" fill="{fg}" opacity=".4"/><rect x="0" y="{y + h - 1.3:.2f}" width="{W:.2f}" height=".7" fill="{fg}" opacity=".4"/>'
    if kind == "lead":
        return line(0, W * .22, 2.4, BLUE) + line(W * .22 + 2, W, .8, fg, .35)
    if kind == "caps":
        return line(0, W, .8, fg, .4) + f'<rect x="0" y="{y:.2f}" width=".9" height="{h}" fill="{fg}"/><rect x="{W - .9:.2f}" y="{y:.2f}" width=".9" height="{h}" fill="{fg}"/>'
    if kind == "dashed":
        out, x = "", 0.0
        while x < W:
            out += line(x, min(x + 6, W), 1.2, fg, .55); x += 9
        return out
    if kind == "dots":
        n = 64
        return "".join(f'<circle cx="{i * W / (n - 1):.2f}" cy="{mid:.2f}" r=".75" fill="{fg}" opacity="{.25 + .65 * (1 - i / n):.2f}"/>' for i in range(n))
    if kind == "fade":
        return (f'<defs><linearGradient id="fg" x1="0" x2="1"><stop offset="0" stop-color="{fg}" stop-opacity="0"/><stop offset=".5" stop-color="{fg}" stop-opacity=".8"/>'
                f'<stop offset="1" stop-color="{fg}" stop-opacity="0"/></linearGradient></defs><rect x="0" y="{mid - .5:.2f}" width="{W:.2f}" height="1" fill="url(#fg)"/>')
    if kind == "cobalt-ice":
        return (f'<defs><linearGradient id="ci" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{fg}" stop-opacity=".25"/></linearGradient></defs>'
                f'<rect x="0" y="{mid - .9:.2f}" width="{W:.2f}" height="1.8" fill="url(#ci)"/>')
    if kind == "phi":
        a, b, c = 13, 8, 5
        tot = a + b + c; gap = 2.5; u = (W - 2 * gap) / tot
        return line(0, a * u, 2, BLUE) + line(a * u + gap, (a + b) * u + gap, 2, BLUE, .58) + line((a + b) * u + 2 * gap, W, 2, BLUE, .28)
    if kind == "speed":
        out, x, L = "", 0.0, 40.0
        while x < W and L > 1:
            out += line(x, x + L, 1.6, BLUE, max(.25, L / 40)); x += L + 3; L *= .78
        return out + line(x, W, .7, fg, .25)
    if kind == "trace":
        pts = " ".join(f"{i * W / 120:.2f},{mid - 1.6 * _m.sin(i / 120 * 2 * _m.pi * 3) * (0.4 + .6 * _m.sin(i / 120 * _m.pi)):.2f}" for i in range(121))
        return f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width=".9"/>' + line(0, W, .4, fg, .25)
    if kind == "finish":
        sq = h / 2
        cq = "".join(f'<rect x="{W - 8 * sq + c * sq:.2f}" y="{y + r * sq:.2f}" width="{sq:.2f}" height="{sq:.2f}" fill="{fg}"/>' for c in range(8) for r in range(2) if (c + r) % 2 == 0)
        return line(0, W - 8 * sq - 2, .8, fg, .4) + cq
    if kind == "led":
        n = 48; out = ""
        for i in range(n):
            x = i * W / n
            out += f'<rect x="{x:.2f}" y="{y + .4:.2f}" width="{W / n - 1.2:.2f}" height="{h - .8:.2f}" fill="{BLUE}" opacity="{1 if i < n * .6 else .18}"/>'
        return out
    if kind == "hatch-ice":
        out, x = "", 0.0
        while x < W - 2:
            out += f'<polygon points="{x + h * K:.2f},{y} {x + 1 + h * K:.2f},{y} {x + 1:.2f},{y + h} {x:.2f},{y + h}" fill="{fg}" opacity=".45"/>'
            x += 3.2
        return out
    if kind == "bracket":
        return line(0, W * .45, .8, fg, .4) + line(W * .55, W, .8, fg, .4) + line(W * .47, W * .53, 2.4, BLUE)
    return ""


def lockup(name, path, sep):
    f = font(path, None)
    lo, hi = -0.1, 1.5
    for _ in range(60):
        mid = (lo + hi) / 2
        _, b, cap = setline(f, mid, 0)
        (lo, hi) = (mid, hi) if (b[2] - b[0]) * CAP / cap < SW else (lo, mid)
    d, b, cap = setline(f, (lo + hi) / 2, 0)
    sc = CAP / cap
    ysep = 100 + G1
    ty = ysep + BAND + G2 + CAP
    H = ty + max(0, -b[1]) * sc + PAD
    for tag, fg, bg in (("d", ICE, NIGHT), ("l", NIGHT, ICE)):
        bar_p = "".join(f'<path fill="{BLUE}" fill-opacity="{FADE[i]}" d="{m.d_of(bb)}"/>' for i, bb in enumerate(bars))
        open(OUT + f"{tag}-{name}.svg", "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-PAD} {-PAD} {W + 2 * PAD:.2f} {H + PAD:.2f}">'
            f'<rect x="{-PAD}" y="{-PAD}" width="{W + 2 * PAD:.2f}" height="{H + PAD:.2f}" fill="{bg}"/>'
            f'<path fill="{fg}" fill-rule="evenodd" d="{m.d_of(body)}"/>{bar_p}{separator(sep, fg, ysep)}'
            f'<path fill="{fg}" transform="translate({XL - b[0] * sc:.3f} {ty:.3f}) scale({sc:.6f})" d="{d}"/></svg>')


import sys
class _Stop(Exception): pass
if "noop" in sys.argv:
    pass
elif "more" in sys.argv:
    C = []
    MORE = [("hairline", "Hairline (current)"), ("hatch", "12° hatch (current)"), ("double", "Double rule"), ("lead", "Cobalt lead + rule"),
            ("caps", "Rule with end caps"), ("dashed", "Dashed"), ("dots", "Dotted, fading"), ("fade", "Centre-fade rule"),
            ("cobalt-ice", "Cobalt to ice gradient"), ("phi", "φ segments 13:8:5"), ("speed", "Speed dashes"), ("trace", "Telemetry trace"),
            ("finish", "Rule + chequered finish"), ("led", "LED shift lights"), ("hatch-ice", "Fine hatch, mono"), ("bracket", "Split rule, cobalt centre")]
    p = FONTS[0][2]
    for k, l in MORE:
        lockup(f"m-{k}", p, k)
        C.append((f"m-{k}", l))
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:2000px;background:#111;color:#eee;font-family:Arial;padding:56px}}
h1{{font-size:42px}} .lead{{color:#999;margin:10px 0 36px;font-size:17px}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
figure{{background:#1b1b1d;border-radius:10px;overflow:hidden}} .pair{{display:grid;grid-template-rows:1fr 1fr}} .pair img{{width:100%;display:block}}
figcaption{{padding:12px 14px;font-size:15px}} b{{color:#2440FF;margin-right:8px}}</style></head><body>
<h1>AKKI MEISTER — separator line iterations</h1><p class="lead">16 lines above the wordmark · Clash Grotesk · aligned to the mark's baseline</p>
<div class="grid">{"".join(f'<figure><div class="pair"><img src="upright/d-{n}.svg"/><img src="upright/l-{n}.svg"/></div><figcaption><b>{i + 1:02d}</b> {l}</figcaption></figure>' for i, (n, l) in enumerate(C))}</div></body></html>"""
    open("../FINAL-AM/separator-iterations.html", "w", encoding="utf-8").write(html)
    print(len(C)); raise SystemExit
if "noop" not in sys.argv:
  A, B = [], []
  for k, label, p in FONTS:
      lockup(f"f-{k}", p, "hairline")
      A.append((f"f-{k}", label))
  SEPS = [("hairline", "Hairline"), ("cobalt", "Cobalt glow line"), ("bars", "Three-bar line"),
          ("ticks", "Timing ticks"), ("hatch", "12° hatch strip"), ("chequer", "Chequer strip")]
  for k, label, p in FONTS[:3]:
      for s, sl in SEPS:
          lockup(f"s-{k}-{s}", p, s)
          B.append((f"s-{k}-{s}", f"{label} · {sl}"))
  json.dump({"fonts": A, "seps": B}, open(OUT + "index.json", "w"))

  D = "../FINAL-AM/"


  def grid(items):
      return '<div class="grid">' + "".join(
          f'<figure><div class="pair"><img src="upright/d-{n}.svg"/><img src="upright/l-{n}.svg"/></div>'
          f'<figcaption><b>{i + 1:02d}</b> {l}</figcaption></figure>' for i, (n, l) in enumerate(items)) + "</div>"


  html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
  *{{margin:0;padding:0;box-sizing:border-box}} body{{width:2000px;background:#111;color:#eee;font-family:Arial;padding:56px}}
  h1{{font-size:42px}} h2{{font-size:24px;border-top:2px solid #2440FF;padding-top:14px;margin:44px 0 18px}}
  .lead{{color:#999;margin:10px 0;font-size:17px}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
  figure{{background:#1b1b1d;border-radius:10px;overflow:hidden}} .pair{{display:grid;grid-template-columns:1fr 1fr}} .pair img{{width:100%;display:block}}
  figcaption{{padding:12px 14px;font-size:15px}} b{{color:#2440FF;margin-right:8px}}
  </style></head><body><h1>AKKI MEISTER — upright wordmark + separator</h1>
  <p class="lead">Upright futuristic typefaces, tracked to the mark's baseline width (foot of the first bar to the foot of the M), with a gap and a separator band between mark and name.</p>
  <h2>A · Typefaces (hairline separator)</h2>{grid(A)}<h2>B · Separators (Clash Grotesk, Clash Display, Bai Jamjuree)</h2>{grid(B)}</body></html>"""
  open(D + "upright-iterations.html", "w", encoding="utf-8").write(html)
  print(len(A), len(B))
