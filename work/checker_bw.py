from grid import cells, save, FADE
from tune import NIGHT, ICE
for bg, tag, fg in ((NIGHT, "d", ICE), (ICE, "l", NIGHT)):
    body, g = cells()
    for name, fade in (("fade", FADE), ("solid", (1, 1, 1)), ("soft", (1, .7, .45))):
        it = []
        for i, colm in enumerate(g):
            for j, c in enumerate(colm):
                it.append((c, fg, fade[i], None) if (i + j) % 2 == 0 else (c, None, fade[i], fg))
        save(f"{tag}-checker-bw-{name}", body, it, bg, fg)
print("ok")
