"""AKKI MEISTER round 3: monograms built from the MEISTER typeface, straight from Akshat's diary sketches."""
import math, os
from mtype import stroke_open, stroke_closed, clip, to_d, text_svg_path, text_polys, H, ANGLE

OUT = "../round3/"
os.makedirs(OUT, exist_ok=True)

NIGHT, CARBON, ICE, STEEL, RED, COBALT = "#08090D", "#14161D", "#F2F3F5", "#8A8F99", "#E8112D", "#2440FF"
K = math.tan(math.radians(ANGLE))


def shear_polys(polys):
    return [[(x + (H - y) * K, y) for x, y in p] for p in polys]


def build(open_lines, t, box, closed=(), accents=()):
    """centre-lines in units → (main polys, accent polys), clipped to box, sheared"""
    x0, x1 = box
    main, acc = [], []
    for p in open_lines:
        for poly in stroke_open(p, t):
            c = clip(poly, x0, x1, 0, H)
            if c:
                main.append(c)
    for p in closed:
        main += stroke_closed(p, t)
    for p in accents:
        acc.append(p)
    return shear_polys(main), shear_polys(acc)


T_SYM = 1.9
c = 2.1


def ligature(t=T_SYM):
    """the A and the M share one stem; the A keeps a chamfered top-left corner like the sketch"""
    L, B, T = t / 2, H - t / 2, t / 2
    S = 6.2 - t / 2          # shared stem
    R = 11.6 - t / 2
    mid = H * 0.56
    # V point solved so that after the 15-degree lean the left diagonal is exactly 60 deg and the right 45 deg
    D = (R - S) / (1 + 1 / math.sqrt(3))
    V = S + D * K + D / math.sqrt(3)
    VY = T + D
    lines = [[(L, B), (L, T + c), (L + c, T), (S, T), (V, VY), (R, T), (R, B)],
             [(S, T), (S, B)]]
    # crossbar sits only inside the A's counter
    tt = t * 0.62
    acc = [[(L + t / 2, mid - tt / 2), (S - t / 2, mid - tt / 2), (S - t / 2, mid + tt / 2), (L + t / 2, mid + tt / 2)]]
    return lines, acc, (0, 11.6)


def concept_ligature():
    lines, acc, box = ligature()
    m, a = build(lines, T_SYM, box, accents=acc)
    return m, a


def concept_launch():
    """///AM — three speed bars launch into the ligature (the diary's first sketch)"""
    lines, acc, box = ligature()
    m, a = build(lines, T_SYM, box, accents=acc)
    bars = []
    for x, w in ((-5.2, 0.45), (-3.9, 0.85), (-2.3, 1.35)):
        bars.append([(x, 0), (x + w, 0), (x + w, H), (x, H)])
    return m + shear_polys(bars), a


def concept_strike():
    """the overtake: one strike runs through A and M at crossbar height and fires out to the left"""
    t = T_SYM
    lines, _, box = ligature()
    m, _ = build(lines, t, box)
    # cut a gap around the strike out of the letters, then lay the strike in it
    mid = H * 0.56
    g = 0.55
    out = []
    for p in m:
        # p is sheared; unshear for clipping by y, then reshear
        up = [(x - (H - y) * K, y) for x, y in p]
        for y0, y1 in ((0, mid - t * 0.32 - g), (mid + t * 0.32 + g, H)):
            cpoly = clip(up, -99, 99, y0, y1)
            if cpoly:
                out.append(cpoly)
    strike = [(-6.0, mid - t * 0.32), (11.6, mid - t * 0.32), (11.6, mid + t * 0.32), (-6.0, mid + t * 0.32)]
    return shear_polys(out), shear_polys([strike])


def concept_box():
    """the ligature locked in a chamfered grid box, the box broken where the strike would exit"""
    lines, acc, box = ligature()
    m, a = build(lines, T_SYM, box, accents=acc)
    return m, a


def fit(main, acc, size=256, box=200.0, cy=128.0, cx=128.0):
    allp = main + acc
    xs = [x for p in allp for x, _ in p]
    ys = [y for p in allp for _, y in p]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = box / max(w, h)
    ox, oy = cx - (min(xs) + w / 2) * s, cy - (min(ys) + h / 2) * s
    tr = lambda ps: [[(x * s + ox, y * s + oy) for x, y in p] for p in ps]
    return tr(main), tr(acc)


def d(ps):
    return to_d(ps)


def sym_svg(main, acc, fg, ac, bg=None, title="AKKI MEISTER", frame=None):
    b = f'<rect width="256" height="256" fill="{bg}"/>' if bg else ""
    f = frame or ""
    a = f'<path fill="{ac}" d="{d(acc)}"/>' if acc else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>{title}</title>{b}{f}<path fill="{fg}" d="{d(main)}"/>{a}</svg>'


def box_frame(col, t=14):
    """chamfered frame with an opening on the right edge (the exit)"""
    def ring(i):
        cc = 34 - i * 0.6
        return [(i, i), (256 - cc - i, i), (256 - i, cc + i), (256 - i, 256 - i), (cc + i, 256 - i), (i, 256 - cc - i)]
    o, n = ring(8), ring(8 + t)
    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in o) + " Z M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in n[::-1]) + " Z"
    gap = f'<rect x="230" y="112" width="40" height="26" fill="{{bg}}"/>'
    return f'<path fill="{col}" fill-rule="evenodd" d="{path}"/>'


def wordmark_svg(fg, ac, w=1000, weight=1.55, sub=True, title="AKKI MEISTER wordmark"):
    p1, w1 = text_svg_path("AKKI MEISTER", 100, weight, 1.1, fill=fg)
    p2, w2 = text_svg_path("MOTORSPORT · PERFORMANCE", 22, 0.7, 2.35, x=0, y=128, fill=STEEL)
    W = max(w1, w2) + 10
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -4 {W:.0f} 160"><title>{title}</title>{p1}{p2 if sub else ""}</svg>'


if __name__ == "__main__":
    concepts = {"a-ligature": concept_ligature(), "b-launch": concept_launch(), "c-box": concept_box()}
    for k, (m, a) in concepts.items():
        bx = 176.0 if k == "c-box" else 210.0
        fm, fa = fit(m, a, box=bx)
        frame = box_frame(NIGHT) if k == "c-box" else None
        open(OUT + f"{k}-black.svg", "w").write(sym_svg(fm, fa, NIGHT, NIGHT, frame=frame, title=f"AKKI MEISTER {k}"))
        open(OUT + f"{k}-color.svg", "w").write(sym_svg(fm, fa, NIGHT, RED, frame=frame, title=f"AKKI MEISTER {k} colour"))
        open(OUT + f"{k}-rev.svg", "w").write(sym_svg(fm, fa, ICE, RED, bg=NIGHT, frame=box_frame(ICE) if k == "c-box" else None, title=f"AKKI MEISTER {k} reversed"))
    open(OUT + "wordmark.svg", "w").write(wordmark_svg(NIGHT, RED))
    print("ok")
