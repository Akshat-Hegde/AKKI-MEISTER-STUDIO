"""Bars as a grid of boxes: rows split above and below the crossbar cut, same gap everywhere."""
import random
from shapely import affinity
from shapely.geometry import box
from shapely.ops import unary_union
import mark10 as m
from tune import NIGHT, ICE, RED, BLUE

OUT = "../FINAL-AM/tuning/"


def cells(rows_above=3, rows_below=2):
    body, bars, (yc, t, H) = m.build4(cutw=0.035, parts=True)
    top, bot = yc - t / 2, yc + t / 2
    def bands(a, b, n):
        h = (b - a - (n - 1) * t) / n
        return [(a + i * (h + t), a + i * (h + t) + h) for i in range(n)]
    rows = bands(0, top, rows_above) + bands(bot, H, rows_below)
    grid = []   # grid[col][row]; col 0 = next to the A
    for b in bars:
        col = [b.intersection(box(-1e5, r0, 1e5, r1)) for r0, r1 in rows]
        grid.append([c for c in col if not c.is_empty])
    return body, grid


def save(name, body, items, bg, fg, sw=1.0):
    allg = unary_union([body] + [g for g, *_ in items])
    x0, y0, x1, y1 = allg.bounds
    s = 220 / max(x1 - x0, y1 - y0)
    T = lambda g: affinity.affine_transform(g, [s, 0, 0, s, 128 - (x0 + x1) / 2 * s, 128 - (y0 + y1) / 2 * s])
    out = f'<rect width="256" height="256" fill="{bg}"/><path fill="{fg}" fill-rule="evenodd" d="{m.d_of(T(body))}"/>'
    for g, fill, op, stroke in items:
        if stroke:
            out += f'<path d="{m.d_of(T(g))}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'
        else:
            out += f'<path d="{m.d_of(T(g))}" fill="{fill}" opacity="{op}"/>'
    open(OUT + name + ".svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">{out}</svg>')


FADE = (1.0, 0.55, 0.25)
for bg, tag, fg in ((ICE, "l", NIGHT), (NIGHT, "d", ICE)):
    for col, cn in ((BLUE, "cobalt"), (RED, "red")):
        body, g = cells()
        # 1 · solid grid, fading by column
        save(f"{tag}-grid-fade-{cn}", body, [(c, col, FADE[i], None) for i, colm in enumerate(g) for c in colm], bg, fg)
        # 2 · chequered: alternate boxes filled, the rest outlined
        it = []
        for i, colm in enumerate(g):
            for j, c in enumerate(colm):
                it.append((c, col, FADE[i], None) if (i + j) % 2 == 0 else (c, None, FADE[i], col))
        save(f"{tag}-grid-checker-{cn}", body, it, bg, fg)
        # 3 · dissolve: boxes drop out further from the A, like pixels breaking up
        rnd = random.Random(4)
        keep = (1.0, 0.7, 0.4)
        it = [(c, col, 1.0 if i == 0 else 0.85, None) for i, colm in enumerate(g) for c in colm if i == 0 or rnd.random() < keep[i]]
        save(f"{tag}-grid-dissolve-{cn}", body, it, bg, fg)
        # 4 · grid slots: all boxes outlined, column next to A solid
        it = [(c, col, 1, None) if i == 0 else (c, None, FADE[i] + .2, col) for i, colm in enumerate(g) for c in colm]
        save(f"{tag}-grid-slots-{cn}", body, it, bg, fg)
        # 5 · tall rows (2 above, 1 below): bigger boxes, calmer
        body, g2 = cells(2, 1)
        save(f"{tag}-grid-big-{cn}", body, [(c, col, FADE[i], None) for i, colm in enumerate(g2) for c in colm], bg, fg)
        # 6 · fine rows (5 above, 3 below): data / LED feel
        body, g3 = cells(5, 3)
        save(f"{tag}-grid-led-{cn}", body, [(c, col, FADE[i], None) for i, colm in enumerate(g3) for c in colm], bg, fg)
print("ok")
