"""FINAL-AM: master files + the logo-story poster for the locked ///AM mark (line-2-thin)."""
import os, re, math, shutil
from shapely import affinity
import mark10 as m
import saira

ROOT = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/"
OUT = ROOT + "FINAL-AM/"
os.makedirs(OUT + "svg", exist_ok=True)
NIGHT, ICE, RED, NAVY, STEEL = m.NIGHT, m.ICE, m.RED, "#0C1530", "#8C93A3"
SPEC = dict(cutw=0.035)

# ---------------------------------------------------------------- masters
g = m.build4(**SPEC)
x0, y0, x1, y1 = g.bounds
H = y1 - y0
s = 100 / H
G = affinity.affine_transform(g, [s, 0, 0, s, -x0 * s, -y0 * s])
VW = (x1 - x0) * s
D = m.d_of(G)
PAD = 12


def master(name, fg, bg=None):
    b = f'<rect x="{-PAD}" y="{-PAD}" width="{VW + 2 * PAD:.2f}" height="{100 + 2 * PAD}" fill="{bg}"/>' if bg else ""
    open(OUT + f"svg/{name}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-PAD} {-PAD} {VW + 2 * PAD:.2f} {100 + 2 * PAD}"><title>AKKI MEISTER ///AM</title>{b}<path fill="{fg}" fill-rule="evenodd" d="{D}"/></svg>')


for n, fg, bg in (("am-black", NIGHT, None), ("am-white", ICE, None), ("am-red", RED, None), ("am-on-night", ICE, NIGHT), ("am-on-red", ICE, RED), ("am-on-ice", NIGHT, ICE)):
    master(n, fg, bg)
# square icon: mark centred, clear space
sc = 180 / VW
open(OUT + "svg/am-icon-night.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><rect width="256" height="256" rx="56" fill="{NIGHT}"/><path fill="{ICE}" fill-rule="evenodd" transform="translate({128 - VW * sc / 2:.2f} {128 - 50 * sc:.2f}) scale({sc:.4f})" d="{D}"/></svg>')
open(OUT + "svg/am-icon-red.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><rect width="256" height="256" rx="56" fill="{RED}"/><path fill="{ICE}" fill-rule="evenodd" transform="translate({128 - VW * sc / 2:.2f} {128 - 50 * sc:.2f}) scale({sc:.4f})" d="{D}"/></svg>')
# small-size cut: AM only (bars removed) for 16-24 px
bars_x = None
gs = list(G.geoms)
tot = sum(p.area for p in gs)
am_only = [p for p in gs if p.area > tot * 0.08]
from shapely.ops import unary_union
AMO = unary_union(am_only)
ax0, ay0, ax1, ay1 = AMO.bounds
open(OUT + "svg/am-small.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ax0 - 8:.1f} -8 {ax1 - ax0 + 16:.1f} 116"><title>AKKI MEISTER small</title><path fill="{NIGHT}" fill-rule="evenodd" d="{m.d_of(AMO)}"/></svg>')
# wordmark lockup
wd, ww, cap = saira.outline("AKKI MEISTER", 100, 700, 125, True, 0.02)
td, tw, tcap = saira.outline("MOTORSPORT · PERFORMANCE", 100, 500, 125, False, 0.32)
wsc, tsc = 38 / cap, 11 / tcap
LW = VW + 40 + max(ww * wsc, tw * tsc)
for n, fg, sub, bg in (("lockup-night", ICE, STEEL, NIGHT), ("lockup-ice", NIGHT, "#5c6270", None)):
    b = f'<rect x="-14" y="-14" width="{LW + 28:.1f}" height="128" fill="{bg}"/>' if bg else ""
    open(OUT + f"svg/{n}.svg", "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-14 -14 {LW + 28:.1f} 128">{b}<path fill="{fg}" fill-rule="evenodd" d="{D}"/>'
        f'<path fill="{fg}" transform="translate({VW + 40:.1f} 56) scale({wsc:.4f})" d="{wd}"/>'
        f'<rect x="{VW + 42:.1f}" y="68" width="26" height="3" fill="{RED}"/>'
        f'<path fill="{sub}" transform="translate({VW + 76:.1f} 80) scale({tsc:.4f})" d="{td}"/></svg>')

# ---------------------------------------------------------------- poster
IMG = "file:///" + os.environ["TEMP"].replace("\\", "/") + "/claude/c--Users-admin-Akki-Portfolio-main/30173890-75cd-439c-ae4d-37294cbc60ee/images/58.jpg"
F = "file:///C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/node_modules/@fontsource-variable/"


def svgfile(path, fg=None):
    s = open(ROOT + path).read()
    s = s[s.index("<svg"):]
    s = re.sub(r'<rect width="256" height="256" fill="[^"]+"/>', "", s)
    s = re.sub(r'<title>.*?</title>', "", s)
    if fg:
        s = s.replace(f'fill="{NIGHT}"', f'fill="{fg}"').replace('fill="#0B0B0C"', f'fill="{fg}"').replace('fill="#06070B"', f'fill="{fg}"').replace('fill="#08090D"', f'fill="{fg}"').replace('fill="#07080C"', f'fill="{fg}"')
    return s


EVO = [
    ("R1", "Twin Peaks", "concepts/a-symbol.svg", "Two peaks: M, with a crossbar: A."),
    ("R3", "Ligature", "round3/logos/a-ligature-black.svg", "A built type; A and M share a stem."),
    ("R4", "Fusion", "round4/m1-fusion-black.svg", "Saira italic. One knife cut."),
    ("R5", "///AM", "round5/02-speedbars.svg", "The diary's speed bars arrive."),
    ("R7", "Square A", "round7/ch-1-bars.svg", "Flat-topped A, as sketched."),
    ("R8", "The cut", "round8/03-bars-only.svg", "Cut moves into the bars."),
    ("R10", "Typefaces", "round10/titillium-square.svg", "24 combos. Titillium wins."),
    ("R10", "Refined", "round10/fix-1.svg", "Custom M, equal strokes, φ."),
]
evo = ""
for i, (r, name, path, note) in enumerate(EVO):
    svg = svgfile(path, ICE).replace("<svg ", '<svg style="width:100%;height:100%" ', 1)
    evo += (f'<div class="evo"><div class="ev-art">{svg}</div><div class="ev-r">{r}</div><div class="ev-n">{name}</div><div class="ev-t">{note}</div></div>')
    if i < len(EVO) - 1:
        evo += '<div class="arrow">→</div>'

big = f'<svg viewBox="{-PAD} {-PAD} {VW + 2 * PAD:.2f} {100 + 2 * PAD}" style="width:100%;display:block"><path fill="{ICE}" fill-rule="evenodd" d="{D}"/></svg>'
# construction overlay, master units
Mg = m.glyph("titillium", "M")
mx0, my0, mx1, my1 = Mg.bounds
st = m.stem(affinity.translate(Mg, -mx0, -my0)) * (100 / (my1 - my0))
sh = st * 0.86
cb = 61.8 - sh / 2
guides = (f'<line x1="-40" x2="{VW + 30:.0f}" y1="0" y2="0" class="g"/><line x1="-40" x2="{VW + 30:.0f}" y1="100" y2="100" class="g"/>'
          f'<line x1="-40" x2="{VW + 30:.0f}" y1="61.8" y2="61.8" class="gr"/>'
          f'<line x1="-40" x2="{VW + 30:.0f}" y1="38.2" y2="38.2" class="gb"/>'
          f'<text x="{VW + 32:.0f}" y="1.5" class="t">CAP</text><text x="{VW + 32:.0f}" y="101.5" class="t">BASE</text>'
          f'<text x="{VW + 32:.0f}" y="63.3" class="tr">1/φ · 0.618</text><text x="{VW + 32:.0f}" y="39.7" class="tb">1/φ² · 0.382</text>')
k = math.tan(math.radians(12))
lean = f'<line x1="{VW - 5:.1f}" y1="100" x2="{VW - 5 + 100 * k:.1f}" y2="0" class="gr"/><text x="{VW - 30:.0f}" y="-4" class="tr">12°</text>'
cons = (f'<svg viewBox="-45 -14 {VW + 110:.0f} 128" style="width:100%;display:block"><style>.g{{stroke:#3a4152;stroke-width:.35}}.gr{{stroke:{RED};stroke-width:.35;stroke-dasharray:1.4 1}}'
        f'.gb{{stroke:#4a63ff;stroke-width:.3;stroke-dasharray:1.4 1}}.t{{font:3.4px Arial;fill:#8C93A3}}.tr{{font:3.4px Arial;fill:{RED}}}.tb{{font:3.4px Arial;fill:#6d82ff}}</style>'
        f'<path fill="{ICE}" fill-opacity=".14" stroke="{ICE}" stroke-width=".3" fill-rule="evenodd" d="{D}"/>{guides}{lean}</svg>')

sizes = "".join(f'<div class="sz"><img src="svg/{"am-small" if px < 24 else "am-white"}.svg" style="height:{px}px;{"filter:invert(1)" if px < 24 else ""}"/><span>{px}px</span></div>' for px in (16, 24, 32, 48, 72))

PRINCIPLES = [
    ("01", "FROM THE DIARY", "Every element was in a 31 January sketch: speed bars before the letters, a flat-topped A, AM in a box."),
    ("02", "THREE BARS, φ APART", "Bars 13 : 8 : 5. Each is the last divided by φ: acceleration you can measure."),
    ("03", "ONE LINE", "A pinstripe at the A's crossbar runs back through the bars: the racing line through the mark."),
    ("04", "ONE GAP", "Bar spacing = A–M gap. Every stroke in the M equals the A's stems."),
    ("05", "12° FORWARD", "Everything leans 12°. Width : height = 2.618 = φ²."),
]
pr = "".join(f'<div class="pr"><div class="pr-n">{n}</div><div class="pr-h">{h}</div><div class="pr-t">{t}</div></div>' for n, h, t in PRINCIPLES)
sw = "".join(f'<div class="sw" style="background:{c}"><span style="color:{tc}">{n}<br/>{c}</span></div>' for n, c, tc in (("MIDNIGHT", NIGHT, ICE), ("SIGNAL RED", RED, ICE), ("ICE", ICE, NIGHT), ("STEEL", STEEL, NIGHT)))

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Saira; src: url({F}saira/files/saira-latin-wdth-normal.woff2) format('woff2'); font-weight:100 900; font-stretch:50% 125%; }}
@font-face {{ font-family: Saira; src: url({F}saira/files/saira-latin-wdth-italic.woff2) format('woff2'); font-weight:100 900; font-stretch:50% 125%; font-style:italic; }}
@font-face {{ font-family: JBM; src: url({F}jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2) format('woff2'); font-weight:100 800; }}
@font-face {{ font-family: IT; src: url({F}inter-tight/files/inter-tight-latin-wght-normal.woff2) format('woff2'); font-weight:100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:2400px; background:{NIGHT}; color:{ICE}; }}
#poster {{ width:2400px; height:3400px; position:relative; overflow:hidden; background:radial-gradient(ellipse at 70% 18%, {NAVY} 0%, {NIGHT} 55%); }}
.k {{ font-family:Saira; font-stretch:125%; font-weight:600; text-transform:uppercase; letter-spacing:.28em; font-size:20px; color:{STEEL}; }}
.k.r {{ color:{RED}; }}
.mono {{ font-family:JBM; font-size:18px; color:{STEEL}; letter-spacing:.04em; }}
.h {{ font-family:Saira; font-stretch:62%; font-weight:900; font-style:italic; text-transform:uppercase; line-height:.86; }}
.rule {{ position:absolute; left:120px; right:120px; height:1px; background:rgba(244,245,247,.12); }}
.evo-row {{ position:absolute; left:120px; right:120px; top:1600px; display:flex; align-items:flex-start; justify-content:space-between; }}
.evo {{ width:200px; }} .ev-art {{ height:150px; border:1px solid rgba(244,245,247,.12); padding:14px; display:flex; align-items:center; justify-content:center; }}
.ev-r {{ font-family:JBM; color:{RED}; font-size:16px; margin-top:16px; }} .ev-n {{ font-family:Saira; font-stretch:125%; font-weight:800; font-style:italic; font-size:24px; text-transform:uppercase; margin-top:6px; }}
.ev-t {{ font-family:IT; font-size:16px; color:#A9AFBC; margin-top:8px; line-height:1.4; }}
.arrow {{ color:{RED}; font-size:30px; margin-top:62px; font-family:Arial; }}
.pr-grid {{ position:absolute; left:120px; right:120px; top:2680px; display:grid; grid-template-columns:repeat(5,1fr); gap:40px; }}
.pr {{ border-top:2px solid {RED}; padding-top:22px; }} .pr-n {{ font-family:JBM; color:{RED}; font-size:18px; }}
.pr-h {{ font-family:Saira; font-stretch:125%; font-weight:800; font-style:italic; font-size:26px; margin-top:12px; text-transform:uppercase; }}
.pr-t {{ font-family:IT; font-size:19px; color:#A9AFBC; margin-top:12px; line-height:1.5; }}
.sz {{ display:flex; flex-direction:column; align-items:flex-start; gap:10px; }} .sz span {{ font-family:JBM; font-size:15px; color:{STEEL}; }}
.sw {{ flex:1; height:150px; display:flex; align-items:flex-end; padding:18px; border:1px solid rgba(244,245,247,.12); }} .sw span {{ font-family:JBM; font-size:15px; line-height:1.5; }}
</style></head><body><div id="poster">
  <div style="position:absolute;left:120px;top:110px;right:120px;display:flex;justify-content:space-between"><div class="k r">AKKI MEISTER · LOGO STORY</div><div class="k">MOTORSPORT · PERFORMANCE · 2026</div></div>
  <div class="h" style="position:absolute;left:112px;top:190px;font-size:150px">FROM A DIARY PAGE<br/><span style="color:{RED}">TO A RACE NUMBER.</span></div>
  <div style="position:absolute;left:420px;top:530px;width:1560px">{big}</div>
  <div style="position:absolute;left:120px;top:1300px;display:flex;gap:30px;align-items:center"><div class="k r">THE MARK</div><div class="mono">///AM · TITILLIUM-DERIVED M · CONSTRUCTED SQUARE A · 139 ITERATIONS · 10 ROUNDS</div></div>
  <div class="rule" style="top:1400px"></div>
  <div style="position:absolute;left:120px;top:1450px" class="k r">EVOLUTION</div>
  <div style="position:absolute;left:120px;top:1500px" class="mono">ROUND 1 TO FINAL · THE MAJOR TURNS</div>
  <div class="evo-row">{evo}</div>
  <div class="rule" style="top:2000px"></div>
  <div style="position:absolute;left:120px;top:2050px;width:560px;height:290px;overflow:hidden;border:1px solid rgba(244,245,247,.12)">
    <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%;filter:grayscale(1) contrast(1.3) brightness(.85)"/>
    <div class="mono" style="position:absolute;left:16px;bottom:12px;color:{ICE};background:{NIGHT};padding:4px 8px">31 JAN · THE ORIGINAL BRIEF</div></div>
  <div style="position:absolute;left:740px;top:2050px;width:1540px">
    <div class="k r">CONSTRUCTION</div><div style="margin-top:18px">{cons}</div></div>
  <div class="pr-grid">{pr}</div>
  <div class="rule" style="top:2980px"></div>
  <div style="position:absolute;left:120px;top:3030px;width:1000px"><div class="k r">PALETTE</div><div style="display:flex;gap:16px;margin-top:22px">{sw}</div></div>
  <div style="position:absolute;left:1240px;top:3030px"><div class="k r">SCALE</div><div style="display:flex;gap:46px;align-items:flex-end;margin-top:22px">{sizes}</div>
    <div class="mono" style="margin-top:18px">BELOW 24 PX USE THE AM-ONLY CUT</div></div>
  <div style="position:absolute;left:1900px;top:3030px;width:400px;height:240px;border-radius:52px;background:{RED};display:flex;align-items:center;justify-content:center">
    <img src="svg/am-white.svg" style="width:300px"/></div>
</div></body></html>"""
open(OUT + "logo-story.html", "w", encoding="utf-8").write(html)
print("ok", round(VW, 1))
