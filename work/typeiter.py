"""Wordmark typeface iterations under the final cobalt ///AM. Tracking solved so ink width == mark width."""
import os, math, json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from shapely import affinity
from shapely.ops import unary_union
import mark10 as m
from tune import NIGHT, ICE, BLUE

W_ = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/node_modules/"
P_ = "C:/Users/admin/Akki-Portfolio-main/3d_portfolio/node_modules/"
OUT = "../FINAL-AM/type-iter/"
os.makedirs(OUT, exist_ok=True)
fs = lambda f, w, st="normal": W_ + f"@fontsource/{f}/files/{f}-latin-{w}-{st}.woff2"
SAIRA = W_ + "@fontsource-variable/saira/files/saira-latin-wdth-"
# key, label, file, axes, extra shear (deg)
T = [
    ("01-saira-exp-bi", "Saira Expanded · Bold Italic (current)", SAIRA + "italic.woff2", {"wght": 700, "wdth": 125}, 0),
    ("02-saira-exp-black", "Saira Expanded · Black Italic", SAIRA + "italic.woff2", {"wght": 900, "wdth": 125}, 0),
    ("03-saira-exp-light", "Saira Expanded · Light Italic", SAIRA + "italic.woff2", {"wght": 400, "wdth": 125}, 0),
    ("04-saira-semicond", "Saira SemiCondensed · Bold Italic", SAIRA + "italic.woff2", {"wght": 700, "wdth": 87.5}, 0),
    ("05-titillium", "Titillium Web · Bold Italic (matches the M)", fs("titillium-web", 700, "italic"), None, 0),
    ("06-chakra", "Chakra Petch · Bold Italic", fs("chakra-petch", 700, "italic"), None, 0),
    ("07-exo2", "Exo 2 · ExtraBold Italic", fs("exo-2", 800, "italic"), None, 0),
    ("08-kanit", "Kanit · Bold Italic", fs("kanit", 700, "italic"), None, 0),
    ("09-barlow", "Barlow · ExtraBold Italic", fs("barlow", 800, "italic"), None, 0),
    ("10-orbitron", "Orbitron · Bold, sheared 12°", fs("orbitron", 700), None, 12),
    ("11-michroma", "Michroma · sheared 12°", fs("michroma", 400), None, 12),
    ("12-russo", "Russo One · sheared 12°", fs("russo-one", 400), None, 12),
    ("13-oxanium", "Oxanium · ExtraBold, sheared 12°", fs("oxanium", 800), None, 12),
    ("14-rajdhani", "Rajdhani · Bold, sheared 12°", fs("rajdhani", 700), None, 12),
    ("15-sora", "Sora · Bold, sheared 12°", fs("sora", 700), None, 12),
    ("16-archivo-wide", "Archivo Expanded · ExtraBold, sheared 12°", P_ + "@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2", {"wght": 800, "wdth": 125}, 12),
    ("17-michroma-upright", "Michroma · upright", fs("michroma", 400), None, 0),
    ("18-orbitron-upright", "Orbitron · Black upright", fs("orbitron", 900), None, 0),
]
TEXT = "AKKI MEISTER"


def font(path, axes):
    f = TTFont(path)
    return instantiateVariableFont(f, axes) if axes else f


def setline(f, track, shear):
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    k = math.tan(math.radians(shear))
    sp, bp = SVGPathPen(gs), BoundsPen(gs)
    x = 0
    for ch in TEXT:
        g = cmap[ord(ch)]
        tr = (1, 0, k, -1, x, 0)        # flip y, shear (y up → x right)
        gs[g].draw(TransformPen(sp, tr)); gs[g].draw(TransformPen(bp, tr))
        x += hmtx[g][0] + track * upm
    cap = f["OS/2"].sCapHeight if getattr(f["OS/2"], "sCapHeight", 0) else upm * 0.7
    return sp.getCommands(), bp.bounds, cap


# mark (from the final lockup construction)
body, bars, _ = m.build4(cutw=0.035, parts=True)
allg = unary_union([body] + bars)
x0, y0, x1, y1 = allg.bounds
s = 100 / (y1 - y0)
TR = lambda g: affinity.affine_transform(g, [s, 0, 0, s, -x0 * s, -y0 * s])
body, bars = TR(body), [TR(b) for b in bars]
W = (x1 - x0) * s
FADE = (1, .58, .28)
CAP, GAP, PAD = 19.0, 17.0, 14
idx = []
for key, label, path, axes, shear in T:
    f = font(path, axes)
    lo, hi = -0.1, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        _, b, cap = setline(f, mid, shear)
        sc = CAP / cap
        (lo, hi) = (mid, hi) if (b[2] - b[0]) * sc < W else (lo, mid)
    d, b, cap = setline(f, (lo + hi) / 2, shear)
    sc = CAP / cap
    tx, ty = -b[0] * sc, 100 + GAP + CAP
    H = ty + max(0, -b[1]) * sc + PAD
    for tag, fg, bg in (("d", ICE, NIGHT), ("l", NIGHT, ICE)):
        bar_p = "".join(f'<path fill="{BLUE}" fill-opacity="{FADE[i]}" d="{m.d_of(bb)}"/>' for i, bb in enumerate(bars))
        open(OUT + f"{tag}-{key}.svg", "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-PAD} {-PAD} {W + 2 * PAD:.2f} {H + PAD:.2f}">'
            f'<rect x="{-PAD}" y="{-PAD}" width="{W + 2 * PAD:.2f}" height="{H + PAD:.2f}" fill="{bg}"/>'
            f'<path fill="{fg}" fill-rule="evenodd" d="{m.d_of(body)}"/>{bar_p}'
            f'<path fill="{fg}" transform="translate({tx:.3f} {ty:.3f}) scale({sc:.6f})" d="{d}"/></svg>')
    idx.append((key, label))
json.dump(idx, open(OUT + "index.json", "w"))
print(len(idx))
