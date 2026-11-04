"""AKKI MEISTER round 2: a symbol family in one language (20-degree lean, horizontal speed slices,
sharp points), plus patterns, icons and applications on one brand board."""
import math, os
from gen import (concept_a, shear, clip_y, d_of, wordmark, LEAN, T, B, H, ORANGE, INK, WHITE)

OUT = "../round2/"
os.makedirs(OUT, exist_ok=True)
PAPER = "#F4F2EE"


def fit_parts(parts, box=212.0, cx=128.0, cy=128.0, lean=True):
    sh = [((shear(p) if lean else p), r) for p, r in parts]
    xs = [x for p, _ in sh for x, _ in p]; ys = [y for p, _ in sh for _, y in p]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = box / max(w, h)
    ox, oy = cx - (min(xs) + w / 2) * s, cy - (min(ys) + h / 2) * s
    return [([(x * s + ox, y * s + oy) for x, y in p], r) for p, r in sh]


def paths(parts, main, accent, rule="nonzero"):
    out = []
    for role, col in (("main", main), ("accent", accent)):
        ps = [p for p, r in parts if r == role]
        if ps:
            out.append(f'<path fill="{col}" fill-rule="{rule}" d="{" ".join(d_of(p) for p in ps)}"/>')
    return "".join(out)


def svg(inner, title, vb="0 0 256 256", bg=None):
    b = f'<rect x="-9999" y="-9999" width="99999" height="99999" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><title>{title}</title>{b}{inner}</svg>'


# ------------------------------------------------------------------ 1. SLICED PEAKS (primary)
def sliced_peaks():
    """the Twin Peaks M/A, cut into three speed slices; each lower slice trails a little further behind"""
    outline, bar = [p for p, _ in concept_a()]
    g = 9.0
    # both cuts sit above the counters (their tips are at y=137.6), so the letters stay whole
    y1 = 104.0
    bands = [(T - 2, y1 - g / 2, 0.0), (y1 + g / 2, B, -8.0)]
    parts = []
    for a, b, dx in bands:
        poly = clip_y(outline, a, b)
        parts.append(([(x + dx, y) for x, y in poly], "main"))
    # the A's crossbar becomes the orange slice inside the first counter (bottom band)
    parts.append(([(x - 8, y) for x, y in bar], "accent"))
    return parts


# ------------------------------------------------------------------ 2. APEX STAR (secondary symbol)
def apex_star():
    """a four-point flare: the apex of a corner, the moment of max speed. Tall sharp vertical, long thin
    horizontal needles (the racing line), a diamond-shaped apex cut at the centre."""
    c = (128.0, 128.0)
    pts = [(128, 18), (139, 117), (246, 128), (139, 139), (128, 238), (117, 139), (10, 128), (117, 117)]
    hole = [(128, 112), (144, 128), (128, 144), (112, 128)]
    return [(pts, "main"), (hole, "hole")]


# ------------------------------------------------------------------ 3. MEISTER SEAL (hanko)
def seal_svg(fill, knock, title):
    """a square seal (like a hanko stamp) with A and M cut from one grid of 24-unit strokes"""
    t = 24
    A = [(44, 196), (90, 60), (136, 196), (112, 196), (101, 162), (79, 162), (68, 196)]
    Acounter = [(84, 140), (96, 140), (90, 116)]
    M = [(148, 196), (148, 60), (172, 60), (186, 112), (200, 60), (224, 60), (224, 196), (200, 196), (200, 120), (190, 156), (182, 156), (172, 120), (172, 196)]
    border = "M18 18 H238 V238 H18 Z M28 28 V228 H228 V28 Z"
    tile = "M0 0 H256 V256 H0 Z"
    d = tile + " " + d_of(A) + " " + d_of(M) + " " + border.split(" M28")[0].replace("M18 18 H238 V238 H18 Z", "")
    c, c2 = 34, 26
    tile = d_of([(0, 0), (256 - c, 0), (256, c), (256, 256), (c, 256), (0, 256 - c)])
    ring_o = d_of([(14, 14), (242 - c2, 14), (242, 14 + c2), (242, 242), (14 + c2, 242), (14, 242 - c2)])
    ring_i = d_of([(20, 20), (20, 236 - c2 + 6), (20 + c2 - 6, 236), (236, 236), (236, 20 + c2 - 6), (236 - c2 + 6, 20)])
    inner = (f'<path fill="{fill}" fill-rule="evenodd" d="{tile} {d_of(A)} {d_of(M)} {ring_o} {ring_i}"/>'
             f'<path fill="{fill}" d="{d_of(Acounter)}"/>')
    return svg(inner, title)


# ------------------------------------------------------------------ wordmark lockups
def lockup_h(symbol_inner, title, word=INK, tag="#6B6762", accent=ORANGE, bg=None, w_sym=256):
    w1, w1w = wordmark("AKKI MEISTER", 64, 800, 125, 0.012)
    w2, w2w = wordmark("MOTORSPORT  ·  PERFORMANCE", 16, 600, 125, 0.34, oblique=0)
    x0 = w_sym + 34
    W = x0 + max(w1w, w2w) + 28
    b = f'<rect width="{W:.0f}" height="256" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 256"><title>{title}</title>{b}{symbol_inner}'
            f'<path fill="{word}" transform="translate({x0} 142)" d="{w1}"/>'
            f'<rect x="{x0 + 3}" y="161" width="44" height="4" fill="{accent}"/>'
            f'<path fill="{tag}" transform="translate({x0 + 58} 168)" d="{w2}"/></svg>')


def lockup_stack(symbol_inner, title, word=INK, accent=ORANGE, bg=None):
    w1, w1w = wordmark("AKKI MEISTER", 46, 800, 125, 0.012)
    W = max(400, w1w + 60)
    b = f'<rect width="{W:.0f}" height="400" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 400"><title>{title}</title>{b}'
            f'<g transform="translate({(W - 256) / 2:.1f} 0)">{symbol_inner}</g>'
            f'<path fill="{word}" transform="translate({(W - w1w) / 2:.1f} 318)" d="{w1}"/>'
            f'<rect x="{W / 2 - 22:.1f}" y="342" width="44" height="4" fill="{accent}"/></svg>')


if __name__ == "__main__":
    sp = fit_parts(sliced_peaks())
    st = fit_parts(apex_star(), box=220, lean=True)
    files = {}
    for name, parts, rule in (("sliced-peaks", sp, "nonzero"), ("apex-star", st, "evenodd")):
        if name == "apex-star":
            main = [p for p, r in parts if r == "main"]; hole = [p for p, r in parts if r == "hole"]
            def star(col):
                return f'<path fill="{col}" fill-rule="evenodd" d="{d_of(main[0])} {d_of(hole[0])}"/>'
            variants = {"black": (star(INK), None), "white": (star(WHITE), INK), "orange": (star(ORANGE), None)}
        else:
            variants = {"black": (paths(parts, INK, INK), None), "color": (paths(parts, INK, ORANGE), None),
                        "white": (paths(parts, WHITE, ORANGE), INK), "orange": (paths(parts, WHITE, INK), ORANGE)}
        for v, (inner, bg) in variants.items():
            s = svg(inner, f"AKKI MEISTER {name} {v}", bg=bg)
            open(OUT + f"{name}-{v}.svg", "w").write(s)
            files[f"{name}-{v}"] = inner
    for v, (f, k) in {"orange": (ORANGE, None), "black": (INK, None)}.items():
        open(OUT + f"meister-seal-{v}.svg", "w").write(seal_svg(f, k, f"AKKI MEISTER seal {v}"))
    sp_color = files["sliced-peaks-color"]
    open(OUT + "lockup-horizontal.svg", "w").write(lockup_h(sp_color, "AKKI MEISTER horizontal"))
    open(OUT + "lockup-horizontal-reversed.svg", "w").write(lockup_h(files["sliced-peaks-white"], "AKKI MEISTER horizontal reversed", word=WHITE, tag="#9A968F", bg=INK))
    open(OUT + "lockup-stacked.svg", "w").write(lockup_stack(sp_color, "AKKI MEISTER stacked"))
    wm, wmw = wordmark("AKKI MEISTER", 64, 800, 125, 0.012)
    open(OUT + "wordmark.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -54 {wmw + 14:.0f} 68"><title>AKKI MEISTER wordmark</title><path fill="{INK}" d="{wm}"/></svg>')
    print("round 2 symbols written")
