"""Colour only selected edges of the outlined bars: leading (right) slanted edges and/or the cut edges."""
from shapely import affinity
from shapely.ops import unary_union
import mark10 as m
from tune import NIGHT, ICE, RED, ORANGE, BLUE

OUT = "../FINAL-AM/tuning/"
TEAL = "#00D2BE"


def pieces(cutw=0.06):
    body, bars, (yc, t, H) = m.build4(cutw=cutw, parts=True)
    ps = []
    for b in bars:
        ps += list(b.geoms) if hasattr(b, "geoms") else [b]
    return body, ps, yc, t, H


def classify(p, yc, t, H):
    """returns dict of edge lists: right, left, cut, outer (top/bottom of mark)"""
    c = list(p.exterior.coords)[:-1]
    out = {"right": [], "left": [], "cut": [], "outer": []}
    xs = [q[0] for q in c]
    for i in range(len(c)):
        a, b = c[i], c[(i + 1) % len(c)]
        if abs(a[1] - b[1]) < 1e-6:          # horizontal
            yv = a[1]
            out["cut" if abs(yv - (yc - t / 2)) < 1e-3 * H or abs(yv - (yc + t / 2)) < 1e-3 * H else "outer"].append((a, b))
        else:
            mx = (a[0] + b[0]) / 2
            my = (a[1] + b[1]) / 2
            # compare to the other slanted edge at same height
            out["right" if mx > sum(xs) / len(xs) else "left"].append((a, b))
    return out


def render(name, accent_parts, accent, base, bg, fg, sw=1.0):
    body, ps, yc, t, H = pieces()
    allg = unary_union([body] + ps)
    x0, y0, x1, y1 = allg.bounds
    s = 220 / max(x1 - x0, y1 - y0)
    T = lambda pt: (pt[0] * s + 128 - (x0 + x1) / 2 * s, pt[1] * s + 128 - (y0 + y1) / 2 * s)
    body_t = affinity.affine_transform(body, [s, 0, 0, s, 128 - (x0 + x1) / 2 * s, 128 - (y0 + y1) / 2 * s])
    segs_base, segs_acc = [], []
    for p in ps:
        e = classify(p, yc, t, H)
        for k, lst in e.items():
            (segs_acc if k in accent_parts else segs_base).extend(lst)
    def path(segs):
        return " ".join(f"M{T(a)[0]:.2f} {T(a)[1]:.2f} L{T(b)[0]:.2f} {T(b)[1]:.2f}" for a, b in segs)
    basep = f'<path d="{path(segs_base)}" stroke="{base}" stroke-width="{sw}" fill="none" stroke-linecap="square"/>' if base else ""
    accp = f'<path d="{path(segs_acc)}" stroke="{accent}" stroke-width="{sw * 1.6:.2f}" fill="none" stroke-linecap="square"/>'
    open(OUT + name + ".svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><rect width="256" height="256" fill="{bg}"/>'
                                         f'<path fill="{fg}" fill-rule="evenodd" d="{m.d_of(body_t)}"/>{basep}{accp}</svg>')


N = []
for bg, tag, fg, dim in ((NIGHT, "d", ICE, "#3a3f4c"), (ICE, "l", NIGHT, "#c4c8d0")):
    for col, cn in ((TEAL, "teal"), (RED, "red"), (ORANGE, "orange"), (BLUE, "cobalt")):
        render(f"{tag}-edge-lead-{cn}", {"right"}, col, dim, bg, fg)              # A: leading edges coloured, rest dim
        render(f"{tag}-edge-cut-{cn}", {"right", "cut"}, col, dim, bg, fg)        # B: leading + cut edges
        render(f"{tag}-edge-only-{cn}", {"right", "cut"}, col, None, bg, fg)      # C: only those edges, nothing else
        N += [f"edge-lead-{cn}", f"edge-cut-{cn}", f"edge-only-{cn}"]
print("ok")
