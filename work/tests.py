"""Final ///AM tests: tight master SVGs + a golden-ratio construction overlay."""
import math, re
from shapely import affinity
import mark10 as m

OUT = "../final/"
import os
os.makedirs(OUT, exist_ok=True)
PHI = m.PHI

g, _ = m.build3()
x0, y0, x1, y1 = g.bounds
W, H = x1 - x0, y1 - y0
# master: tight viewBox, height 100 units
s = 100 / H
G = affinity.affine_transform(g, [s, 0, 0, s, -x0 * s, -y0 * s])
vw = W * s
for name, fg, bg in (("am-black", m.NIGHT, None), ("am-white", m.ICE, None), ("am-red", m.RED, None), ("am-on-night", m.ICE, m.NIGHT)):
    b = f'<rect x="-10" y="-10" width="{vw + 20:.1f}" height="120" fill="{bg}"/>' if bg else ""
    open(OUT + name + ".svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 {vw + 20:.1f} 120"><title>AKKI MEISTER</title>{b}<path fill="{fg}" fill-rule="evenodd" d="{m.d_of(G)}"/></svg>')
# square icon (mark centred in 256 with clear space = crossbar band height)
open(OUT + "am-icon.svg", "w").write(open(m.OUT + "final-1-golden-rev.svg").read())

# ---- golden overlay (in master units, height 100) -------------------------------------
M = m.glyph("titillium", "M")
mx0, my0, mx1, my1 = M.bounds
Hu = my1 - my0
sc = 100 / Hu
stem = m.stem(affinity.translate(M, -mx0, -my0)) * sc
sh = stem * 0.86
cb = 61.8 - sh / 2
lines = []
def hl(y, label, col="#E10A23", dash=""):
    lines.append(f'<line x1="-40" x2="{vw + 40:.0f}" y1="{y:.2f}" y2="{y:.2f}" stroke="{col}" stroke-width="0.35" stroke-dasharray="{dash}"/>'
                 f'<text x="{vw + 44:.0f}" y="{y + 1.4:.2f}" font-size="3.6" fill="{col}" font-family="Arial">{label}</text>')
hl(0, "cap · 0")
hl(100, "baseline · 1")
hl(61.8, "crossbar centre · 1/φ = 0.618", dash="1.2 1")
hl(38.2, "0.382 = 1/φ²", "#2440FF", "1.2 1")
hl(cb, "crossbar top", "#888", "0.6 0.8")
hl(cb + sh, "crossbar bottom = bar cut", "#888", "0.6 0.8")
# golden rectangle on the whole lockup width
gr = []
x, y, w, h = -10, -10, vw + 20, (vw + 20) / PHI
gr.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="#2440FF" stroke-width="0.3"/>')
for i in range(6):                         # nested squares + quarter arcs (golden spiral)
    if i % 4 == 0:
        sq = h; gr.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{sq:.1f}" height="{sq:.1f}" fill="none" stroke="#2440FF" stroke-width="0.25"/>')
        gr.append(f'<path d="M{x:.1f} {y + sq:.1f} A{sq:.1f} {sq:.1f} 0 0 1 {x + sq:.1f} {y:.1f}" fill="none" stroke="#2440FF" stroke-width="0.4"/>')
        x, w = x + sq, w - sq
    elif i % 4 == 1:
        sq = w; gr.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{sq:.1f}" height="{sq:.1f}" fill="none" stroke="#2440FF" stroke-width="0.25"/>')
        gr.append(f'<path d="M{x:.1f} {y:.1f} A{sq:.1f} {sq:.1f} 0 0 1 {x + sq:.1f} {y + sq:.1f}" fill="none" stroke="#2440FF" stroke-width="0.4"/>')
        y, h = y + sq, h - sq
    elif i % 4 == 2:
        sq = h; gr.append(f'<rect x="{x + w - sq:.1f}" y="{y:.1f}" width="{sq:.1f}" height="{sq:.1f}" fill="none" stroke="#2440FF" stroke-width="0.25"/>')
        gr.append(f'<path d="M{x + w:.1f} {y:.1f} A{sq:.1f} {sq:.1f} 0 0 1 {x + w - sq:.1f} {y + sq:.1f}" fill="none" stroke="#2440FF" stroke-width="0.4"/>')
        w = w - sq
    else:
        sq = w; gr.append(f'<rect x="{x:.1f}" y="{y + h - sq:.1f}" width="{sq:.1f}" height="{sq:.1f}" fill="none" stroke="#2440FF" stroke-width="0.25"/>')
        gr.append(f'<path d="M{x + sq:.1f} {y + h:.1f} A{sq:.1f} {sq:.1f} 0 0 1 {x:.1f} {y + h - sq:.1f}" fill="none" stroke="#2440FF" stroke-width="0.4"/>')
        h = h - sq
ratio = (vw + 20) / 120
notes = (f'<text x="-40" y="128" font-size="4" font-family="Arial" fill="#111">Bars: 13.0 : 8.0 : 5.0 (each = previous ÷ φ) · bar spacing = A–M gap = 6% of cap · '
         f'crossbar centred at 1/φ of cap height · bar cut = crossbar band · lean 12° · overall ratio {vw / 100:.3f} : 1 (φ = 1.618 × {vw / 100 / PHI:.2f})</text>')
open(OUT + "golden-overlay.svg", "w", encoding="utf-8").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-45 -20 {vw + 130:.0f} 155" width="1800"><rect x="-45" y="-20" width="{vw + 130:.0f}" height="155" fill="#fff"/>'
    f'<path fill="#07080C" fill-opacity=".9" fill-rule="evenodd" d="{m.d_of(G)}"/>{"".join(gr)}{"".join(lines)}{notes}</svg>')
print("vw", round(vw, 2), "ratio w/h", round(vw / 100, 3))
