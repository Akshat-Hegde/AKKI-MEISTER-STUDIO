"""Iterations on #15: filled chequer squares only."""
import os, json, random
from shapely.ops import unary_union
import mark10 as m
from grid import cells
from iter2 import write as _w, bars_solid
import iter2
from tune import NIGHT, ICE, RED, ORANGE, BLUE

iter2.OUT = OUT = "../FINAL-AM/iter3/"
os.makedirs(OUT, exist_ok=True)
TEAL, YEL = "#00D2BE", "#FFC400"
V = []


def chk(g, cols, fade, phase=0, keep=None, seed=3):
    rnd = random.Random(seed)
    it = []
    for i, colm in enumerate(g):
        c_ = cols[i] if isinstance(cols, (list, tuple)) else cols
        for j, c in enumerate(colm):
            if (i + j + phase) % 2 == 0 and (keep is None or rnd.random() < keep[i]):
                it.append((c, c_, fade[i]))
    return it


for bg, tag, fg in ((NIGHT, "d", ICE), (ICE, "l", NIGHT)):
    def add(n, label, rows=(3, 2), cols=RED, fade=(1, .58, .28), phase=0, keep=None, lead=False):
        body, g = cells(*rows)
        it = chk(g, cols, fade, phase, keep)
        if lead:
            _, bars, _ = bars_solid()
            it = [(bars[0], cols if isinstance(cols, str) else cols[0], 1)] + [x for x in it if not x[0].within(bars[0].buffer(0.01))]
        _w(f"{tag}-{n}", body, it, bg, fg)
        if tag == "d": V.append((n, label))
    add("01-base", "Base · as picked")
    add("02-flip", "Flipped phase", phase=1)
    add("03-nofade", "No fade · full strength", fade=(1, 1, 1))
    add("04-soft", "Soft fade", fade=(1, .78, .55))
    add("05-steep", "Steep fade", fade=(1, .4, .12))
    add("06-big", "Bigger squares (3 rows)", rows=(2, 1))
    add("07-fine", "Finer squares (8 rows)", rows=(5, 3))
    add("08-7rows", "7 rows", rows=(4, 3))
    add("09-lead", "Solid lead bar + chequer", lead=True)
    add("10-dissolve", "Dissolving outward", keep=(1, .8, .5))
    add("11-mono", "Monochrome", cols=fg)
    add("12-cobalt", "Cobalt", cols=BLUE)
    add("13-orange", "Orange", cols=ORANGE)
    add("14-teal", "Teal", cols=TEAL)
    add("15-heat", "Heat · red → orange → yellow", cols=(RED, ORANGE, YEL), fade=(1, .9, .8))
    add("16-red-mono", "Red lead, mono tail", cols=(RED, fg, fg), fade=(1, .6, .3))
    add("17-tricolour", "Red · white · cobalt", cols=(RED, fg, BLUE), fade=(1, .85, .85))
    add("18-big-nofade", "Big squares, no fade", rows=(2, 1), fade=(1, 1, 1))
json.dump(V, open(OUT + "index.json", "w"))
print(len(V))
