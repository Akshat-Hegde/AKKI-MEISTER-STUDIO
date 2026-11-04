"""FINAL lockup: cobalt fade ///AM + AKKI MEISTER (Saira Expanded Bold Italic) spanning the mark's exact width."""
import os
from shapely import affinity
from shapely.ops import unary_union
import mark10 as m
import saira
from tune import NIGHT, ICE, BLUE

OUT = "../FINAL-AM/final-lockup/"
os.makedirs(OUT, exist_ok=True)
FADE = (1, .58, .28)

body, bars, info = m.build4(cutw=0.035, parts=True)
allg = unary_union([body] + bars)
x0, y0, x1, y1 = allg.bounds
s = 100 / (y1 - y0)
T = lambda g: affinity.affine_transform(g, [s, 0, 0, s, -x0 * s, -y0 * s])
body, bars = T(body), [T(b) for b in bars]
W = (x1 - x0) * s                       # mark width, cap height 100

TEXT, WGHT, WDTH = "AKKI MEISTER", 700, 125
CAP = 19.0                              # wordmark cap height (≈ crossbar band ×3)
GAP = 17.0                              # mark baseline → wordmark cap


def measure(track):
    b = saira.bounds(TEXT, 100, wght=WGHT, wdth=WDTH, italic=True, track=track)
    return b


# solve tracking so the ink width (scaled to CAP) equals W exactly
d0, _, cap100 = saira.outline(TEXT, 100, WGHT, WDTH, True, 0)
sc = CAP / cap100
lo, hi = -0.05, 0.6
for _ in range(60):
    mid = (lo + hi) / 2
    bx0, _, bx1, _ = measure(mid)
    (lo, hi) = (mid, hi) if (bx1 - bx0) * sc < W else (lo, mid)
track = (lo + hi) / 2
d, _, _ = saira.outline(TEXT, 100, WGHT, WDTH, True, track)
bx0, by0, bx1, by1 = measure(track)
tx = -bx0 * sc                          # left ink edge at x=0
ty = 100 + GAP + CAP                    # baseline position
print("track", round(track, 4), "ink width", round((bx1 - bx0) * sc, 2), "mark width", round(W, 2))

PAD = 14
H = ty + (by1 * sc if by1 > 0 else 0) + PAD
VB = f"{-PAD} {-PAD} {W + 2 * PAD:.2f} {H + PAD:.2f}"


def svg(name, fg, bg=None):
    bgr = f'<rect x="{-PAD}" y="{-PAD}" width="{W + 2 * PAD:.2f}" height="{H + PAD:.2f}" fill="{bg}"/>' if bg else ""
    bar_p = "".join(f'<path fill="{BLUE}" fill-opacity="{FADE[i]}" d="{m.d_of(b)}"/>' for i, b in enumerate(bars))
    open(OUT + name + ".svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}"><title>AKKI MEISTER</title>{bgr}'
        f'<path fill="{fg}" fill-rule="evenodd" d="{m.d_of(body)}"/>{bar_p}'
        f'<path fill="{fg}" transform="translate({tx:.3f} {ty:.3f}) scale({sc:.5f})" d="{d}"/></svg>')
    # mark only
    mv = f"{-PAD} {-PAD} {W + 2 * PAD:.2f} {100 + 2 * PAD}"
    mb = f'<rect x="{-PAD}" y="{-PAD}" width="{W + 2 * PAD:.2f}" height="{100 + 2 * PAD}" fill="{bg}"/>' if bg else ""
    open(OUT + name.replace("lockup", "mark") + ".svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{mv}"><title>AKKI MEISTER ///AM</title>{mb}<path fill="{fg}" fill-rule="evenodd" d="{m.d_of(body)}"/>{bar_p}</svg>')


svg("lockup-on-night", ICE, NIGHT)
svg("lockup-on-ice", NIGHT, ICE)
svg("lockup-white", ICE)
svg("lockup-black", NIGHT)
