"""Chequered bars: outlines drawn as inner rings so outlined and filled boxes share identical edges."""
from grid import cells, save
from tune import NIGHT, ICE, RED, ORANGE, BLUE
TEAL, GOLD, YEL = "#00D2BE", "#D4AF37", "#FFC400"

def ring(c, H, w=0.012):
    return c.difference(c.buffer(-H * w, join_style=2))

FADE = (1, .62, .32)
SETS = {"bw": None, "red": RED, "orange": ORANGE, "cobalt": BLUE, "teal": TEAL, "gold": GOLD,
        "heat": (RED, ORANGE, YEL), "tyres": (RED, YEL, None)}
for bg, tag, fg in ((NIGHT, "d", ICE), (ICE, "l", NIGHT)):
    body, g = cells()
    H = body.bounds[3] - body.bounds[1]
    for name, col in SETS.items():
        for mode in ("fade", "solid"):
            it = []
            for i, colm in enumerate(g):
                c_ = col[i] if isinstance(col, tuple) else col
                c_ = c_ or fg
                op = FADE[i] if mode == "fade" else 1
                for j, c in enumerate(colm):
                    shape = c if (i + j) % 2 == 0 else ring(c, H)
                    it.append((shape, c_, op, None))
            save(f"{tag}-chk-{name}-{mode}", body, it, bg, fg)
print("ok")
