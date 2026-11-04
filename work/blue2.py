import os, json
import iter2
from grid import cells
from iter3 import chk
from tune import NIGHT, ICE, RED, BLUE
iter2.OUT = OUT = "../FINAL-AM/iter6/"
os.makedirs(OUT, exist_ok=True)
SKY = "#1C8CFF"
V = [("01-red", "Original (red)", RED, (1, .58, .28)),
     ("02-cobalt", "Cobalt", BLUE, (1, .58, .28)),
     ("03-cobalt-soft", "Cobalt, soft fade", BLUE, (1, .75, .5)),
     ("04-cobalt-nofade", "Cobalt, no fade", BLUE, (1, 1, 1)),
     ("05-cobalt-sky", "Cobalt to sky blue", (BLUE, SKY, SKY), (1, .8, .55)),
     ("06-red-lead", "Red lead, cobalt tail", (RED, BLUE, BLUE), (1, .7, .4))]
for bg, tag, fg in ((NIGHT, "d", ICE), (ICE, "l", NIGHT)):
    for n, l, c, f in V:
        body, g = cells(3, 2)
        iter2.write(f"{tag}-{n}", body, chk(g, c, f), bg, fg)
json.dump([(n, l) for n, l, *_ in V], open(OUT + "index.json", "w"))
