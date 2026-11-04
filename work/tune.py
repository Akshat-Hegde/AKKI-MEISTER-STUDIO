"""Fine-tune the locked ///AM: bar colours, outlines, gaps, small touches. Writes ../FINAL-AM/tuning/."""
import os
from shapely.geometry import box
from shapely.ops import unary_union
from shapely import affinity
import mark10 as m

OUT = "../FINAL-AM/tuning/"
os.makedirs(OUT, exist_ok=True)
NIGHT, ICE, RED, ORANGE, BLUE, STEEL, YEL = "#07080C", "#F3F4F6", "#E10A23", "#FF5A1F", "#2440FF", "#8C93A3", "#FFC400"


def shapes(cutw=0.035, **kw):
    body, bars, info = m.build4(cutw=cutw, parts=True, **kw)
    return body, bars, info  # bars listed right (next to A) to left


def svg(name, layers, bg, title, sw=1.6):
    allg = unary_union([g for g, *_ in layers])
    x0, y0, x1, y1 = allg.bounds
    s = 220 / max(x1 - x0, y1 - y0)
    T = lambda g: affinity.affine_transform(g, [s, 0, 0, s, 128 - (x0 + x1) / 2 * s, 128 - (y0 + y1) / 2 * s])
    out = f'<rect width="256" height="256" fill="{bg}"/>'
    for g, fill, stroke, op in layers:
        if stroke:
            out += f'<path d="{m.d_of(T(g))}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="miter" opacity="{op}"/>'
        else:
            out += f'<path d="{m.d_of(T(g))}" fill="{fill}" fill-rule="evenodd" opacity="{op}"/>'
    open(OUT + name + ".svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>{title}</title>{out}</svg>')


def variant(name, title, fg_am, bar_fills, bg, bar_stroke=None, extra=None, sw=1.6, cutw=0.035, **kw):
    body, bars, (yc, t, H) = shapes(cutw=cutw, **kw)
    layers = [(body, fg_am, None, 1)]
    for b, f in zip(bars, bar_fills):
        if bar_stroke:
            layers.append((b, None, f, 1))
        else:
            layers.append((b, f, None, 1) if isinstance(f, str) else (b, f[0], None, f[1]))
    if extra:
        layers += extra(body, bars, yc, t, H)
    svg(name, layers, bg, title, sw)


V = []
def add(*a, **k):
    V.append(a[0]); variant(*a, **k)

import sys
ONLY = "outline" in sys.argv
if __name__ == "__main__":
  pass
for bg, tag, fg in (((NIGHT, "d", ICE), (ICE, "l", NIGHT)) if __name__ == "__main__" else ()):
    if ONLY:
        for cw in (0.06, 0.08):
            for sw in (1.0, 0.75):
                for col, cn in ((fg, "mono"), (RED, "red")):
                    add(f"{tag}-ol-{cn}-gap{int(cw*100)}-sw{int(sw*100)}", "", fg, [col] * 3, bg, bar_stroke=True, sw=sw, cutw=cw)
        continue
    add(f"{tag}-00-base", "Locked mark", fg, [fg] * 3, bg)
    add(f"{tag}-01-red", "Bars in Signal Red", fg, [RED] * 3, bg)
    add(f"{tag}-02-orange", "Bars in racing orange", fg, [ORANGE] * 3, bg)
    add(f"{tag}-03-blue", "Bars in cobalt", fg, [BLUE] * 3, bg)
    add(f"{tag}-04-fade", "Bars fade in toward the A", fg, [(fg, 1), (fg, .55), (fg, .25)], bg)
    add(f"{tag}-05-red-fade", "Red bars fading in", fg, [(RED, 1), (RED, .6), (RED, .3)], bg)
    add(f"{tag}-06-outline", "Bars as outlines", fg, [fg] * 3, bg, bar_stroke=True)
    add(f"{tag}-07-outline-red", "Outlined bars in red", fg, [RED] * 3, bg, bar_stroke=True)
    add(f"{tag}-08-gap", "Wider gap before the A", fg, [fg] * 3, bg, bar_gap=0.16)
    add(f"{tag}-09-gap-red", "Wider gap, red bars", fg, [RED] * 3, bg, bar_gap=0.16)
    add(f"{tag}-10-tyres", "Tyre compounds: soft, medium, hard", fg, [RED, YEL, fg], bg)
    body, bars, info = shapes()
    svg(f"{tag}-11-mixed", [(body, fg, None, 1), (bars[0], fg, None, 1), (bars[1], None, fg, 1), (bars[2], None, fg, 1)], bg, "Outline, outline, solid: accelerating")
    V.append(f"{tag}-11-mixed")
    add(f"{tag}-12-steel", "Bars in Steel, AM bright", fg, [STEEL] * 3, bg)
    add(f"{tag}-13-red-line", "Red pinstripe through the whole mark", fg, [fg] * 3, bg,
        extra=lambda body, bars, yc, t, H: [(box(unary_union(bars).bounds[0] + H * .02, yc - t / 2, body.bounds[2] - H * .02, yc + t / 2), RED, None, 1)])
print(len(V))
