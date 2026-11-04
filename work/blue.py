import os, json
import iter2, tight
from tune import NIGHT, ICE, RED, BLUE
from iter2 import bars_solid
iter2.OUT = OUT = "../FINAL-AM/iter5/"
os.makedirs(OUT, exist_ok=True)
CYAN = "#1C8CFF"
V = [("01-flag", "Chequered flag (touching)", dict(col_gap=0.0, row_gap=0.0, a_gap=0.035, widths=(0.12, 0.12, 0.12))),
     ("02-five", "5-row chequer", dict(rows=(3, 2))),
     ("03-seven", "7-row chequer", dict()),
     ("04-flag-steep", "Flag, steeper fade", dict(col_gap=0.0, row_gap=0.0, a_gap=0.035, widths=(0.12, 0.12, 0.12), fade=(1, .45, .18))),
     ("05-flag-nofade", "Flag, no fade", dict(col_gap=0.0, row_gap=0.0, a_gap=0.035, widths=(0.12, 0.12, 0.12), fade=(1, 1, 1))),
     ("06-flag-duo", "Flag, cobalt to sky blue", dict(col_gap=0.0, row_gap=0.0, a_gap=0.035, widths=(0.12, 0.12, 0.12), fade=(1, .8, .55), colours=(BLUE, CYAN, CYAN))),
     ("07-seven-redlead", "7-row, red lead column", dict(colours=(RED, BLUE, BLUE))),
     ("08-five-redlead", "5-row, red lead column", dict(rows=(3, 2), colours=(RED, BLUE, BLUE)))]
for bg, tag, fg in ((NIGHT, "d", ICE), (ICE, "l", NIGHT)):
    body, bars, H = bars_solid()
    iter2.write(f"{tag}-00-bars", body, [(b, BLUE, (1, .58, .28)[i]) for i, b in enumerate(bars)], bg, fg)
    for n, l, kw in V:
        kw = dict(kw); c = kw.pop("colours", BLUE)
        body, it = tight.build(col=c, **kw)
        iter2.write(f"{tag}-{n}", body, it, bg, fg)
json.dump([("00-bars", "Reference: cobalt fade bars")] + [(n, l) for n, l, _ in V], open(OUT + "index.json", "w"))
print("ok")
