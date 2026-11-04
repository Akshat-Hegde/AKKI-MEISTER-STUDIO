"""Iterations on two picks: A = fade bars (cobalt), B = chequered fade (red). Plus hybrids. -> ../FINAL-AM/iter2/"""
import os, random
from shapely import affinity
from shapely.geometry import box
from shapely.ops import unary_union
import mark10 as m
from grid import cells
from tune import NIGHT, ICE, RED, ORANGE, BLUE

OUT = "../FINAL-AM/iter2/"
os.makedirs(OUT, exist_ok=True)
TEAL, GOLD, YEL, PURP = "#00D2BE", "#D4AF37", "#FFC400", "#7B2CFF"
FADE = (1, .58, .28)


def ring(c, H, w=0.012):
    return c.difference(c.buffer(-H * w, join_style=2))


def write(name, body, items, bg, fg, defs=""):
    allg = unary_union([body] + [g for g, *_ in items])
    x0, y0, x1, y1 = allg.bounds
    s = 220 / max(x1 - x0, y1 - y0)
    T = lambda g: affinity.affine_transform(g, [s, 0, 0, s, 128 - (x0 + x1) / 2 * s, 128 - (y0 + y1) / 2 * s])
    out = f'<defs>{defs}</defs><rect width="256" height="256" fill="{bg}"/><path fill="{fg}" fill-rule="evenodd" d="{m.d_of(T(body))}"/>'
    for g, fill, op in items:
        out += f'<path d="{m.d_of(T(g))}" fill="{fill}" opacity="{op}" fill-rule="evenodd"/>'
    open(OUT + name + ".svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">{out}</svg>')


def bars_solid(cutw=0.035, bar_gap=None):
    body, bars, (yc, t, H) = m.build4(cutw=cutw, parts=True, bar_gap=bar_gap)
    return body, bars, H


def checker_items(g, H, cols, fade=FADE, phase=0, outline=True):
    it = []
    for i, colm in enumerate(g):
        c_ = cols[i] if isinstance(cols, (list, tuple)) else cols
        for j, c in enumerate(colm):
            filled = (i + j + phase) % 2 == 0
            it.append((c if filled or not outline else ring(c, H), c_, fade[i]) if (filled or outline) else (c, c_, 0))
    return it


V = []   # (name, group, label)
for bg, tag, fg in ((ICE, "l", NIGHT), (NIGHT, "d", ICE)):
    def A(n, label, items_fn, **kw):
        body, bars, H = bars_solid(**kw)
        write(f"{tag}-{n}", body, items_fn(bars, H), bg, fg)
        if tag == "l": V.append((n, "A · Fade bars", label))
    # ---- A family: fade bars
    for cn, c in (("cobalt", BLUE), ("red", RED), ("teal", TEAL), ("orange", ORANGE), ("purple", PURP), ("mono", fg)):
        A(f"a-fade-{cn}", f"Fade · {cn}", lambda bars, H, c=c: [(b, c, FADE[i]) for i, b in enumerate(bars)])
    A("a-fade-cobalt-steep", "Steeper fade", lambda bars, H: [(b, BLUE, o) for b, o in zip(bars, (1, .4, .14))])
    A("a-fade-cobalt-reverse", "Reverse fade (bright outside)", lambda bars, H: [(b, BLUE, o) for b, o in zip(bars, (.3, .6, 1))])
    A("a-fade-cobalt-wide", "Fade + wider gap to A", lambda bars, H: [(b, BLUE, FADE[i]) for i, b in enumerate(bars)], bar_gap=0.16)
    A("a-fade-duo", "Cobalt → teal", lambda bars, H: [(b, c, o) for b, c, o in zip(bars, (BLUE, "#1C8CFF", TEAL), (1, .8, .6))])
    A("a-fade-cobalt-am-red", "Cobalt bars, red cut line", lambda bars, H: [(b, BLUE, FADE[i]) for i, b in enumerate(bars)])
    # ---- B family: chequered fade
    def B(n, label, rows=(3, 2), cols=RED, fade=FADE, phase=0, outline=True, extra=None):
        body, g = cells(*rows)
        H = body.bounds[3] - body.bounds[1]
        it = checker_items(g, H, cols, fade, phase, outline)
        if extra: it = extra(g, H, it)
        write(f"{tag}-{n}", body, it, bg, fg)
        if tag == "l": V.append((n, "B · Chequered fade", label))
    B("b-chk-red", "Red chequer · 5 rows")
    B("b-chk-red-phase", "Red chequer · flipped phase", phase=1)
    B("b-chk-red-3rows", "Red chequer · 3 rows (bigger squares)", rows=(2, 1))
    B("b-chk-red-8rows", "Red chequer · 8 rows (fine)", rows=(5, 3))
    B("b-chk-red-solid-only", "Filled squares only (no outlines)", outline=False)
    B("b-chk-red-strong", "Red chequer · no fade", fade=(1, 1, 1))
    B("b-chk-cobalt", "Cobalt chequer", cols=BLUE)
    B("b-chk-redblack", "Red + mono chequer", cols=(RED, fg, fg), fade=(1, .7, .4))
    B("b-chk-heat", "Heat chequer", cols=(RED, ORANGE, YEL))
    def dissolve(g, H, it):
        rnd = random.Random(7); keep = (1, .75, .45)
        return [x for x, (i, j) in zip(it, [(i, j) for i, c in enumerate(g) for j in range(len(c))]) if rnd.random() < keep[i]]
    B("b-chk-dissolve", "Chequer breaking up", extra=dissolve)
    # ---- C hybrids
    def Cn(n, label, fn):
        fn_items = fn()
        write(f"{tag}-{n}", *fn_items, bg, fg)
        if tag == "l": V.append((n, "C · Hybrids", label))
    def h1():   # solid bar next to A, chequer outside
        body, g = cells(3, 2); H = body.bounds[3] - body.bounds[1]
        _, bars, _ = bars_solid()
        it = [(bars[0], RED, 1)] + [x for x in checker_items(g, H, RED) if True][len(g[0]):]
        return body, it
    Cn("c-solid-then-chk", "Solid lead bar, chequer behind", h1)
    def h2():   # cobalt fade bars, red cut stripe
        body, bars, (yc, t, H) = m.build4(cutw=0.035, parts=True)
        x0 = unary_union(bars).bounds[0]
        return body, [(b, BLUE, FADE[i]) for i, b in enumerate(bars)] + [(box(x0, yc - t / 2, body.bounds[0] + H * 0.25, yc + t / 2), RED, 1)]
    Cn("c-cobalt-redline", "Cobalt fade + red cut line", h2)
    def h3():   # chequer only in the outer bar, solid two inner
        body, g = cells(3, 2); H = body.bounds[3] - body.bounds[1]
        _, bars, _ = bars_solid()
        it = [(bars[0], RED, 1), (bars[1], RED, .6)] + [x for x in checker_items(g, H, RED, (1, 1, .45))][len(g[0]) + len(g[1]):]
        return body, it
    Cn("c-chk-tail", "Chequer only on the tail", h3)
    def h4():   # cobalt chequer + red lead bar
        body, g = cells(3, 2); H = body.bounds[3] - body.bounds[1]
        _, bars, _ = bars_solid()
        return body, [(bars[0], RED, 1)] + checker_items(g, H, BLUE)[len(g[0]):]
    Cn("c-red-lead-cobalt-chk", "Red lead bar, cobalt chequer", h4)
print(len(V))
import json; json.dump(V, open(OUT + "index.json", "w"))
