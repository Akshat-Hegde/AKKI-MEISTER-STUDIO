"""Iterations on the 'rule + chequered finish' separator."""
import math, sys
sys.argv = ["x", "noop"]
import upright as U
from tune import BLUE

K = math.tan(math.radians(12))
P = {}


def finish(kind, fg, y):
    W, h = U.SW, U.BAND
    rows = P.get("rows", 2)
    sq = P.get("sq", h / 2)
    n = P.get("n", 8)
    col = P.get("col", fg)
    lcol, lop, lw = P.get("lcol", fg), P.get("lop", .4), P.get("lw", .8)
    skew = P.get("skew", False)
    fade = P.get("fade", False)
    pos = P.get("pos", "end")
    gap = P.get("gap", 2)
    top = y + h / 2 - rows * sq / 2
    fw = n * sq

    def flag(x0, rev=False):
        out = ""
        for c in range(n):
            for r in range(rows):
                if (c + r + P.get("phase", 0)) % 2 == 0:
                    op = 1 if not fade else (c + 1) / n if not rev else (n - c) / n
                    xx = x0 + c * sq
                    yy = top + r * sq
                    if skew:
                        dy = (top + rows * sq) - (yy + sq)
                        out += (f'<polygon points="{xx + (sq + dy) * K:.2f},{yy:.2f} {xx + sq + (sq + dy) * K:.2f},{yy:.2f} '
                                f'{xx + sq + dy * K:.2f},{yy + sq:.2f} {xx + dy * K:.2f},{yy + sq:.2f}" fill="{col}" opacity="{op:.2f}"/>')
                    else:
                        out += f'<rect x="{xx:.2f}" y="{yy:.2f}" width="{sq:.2f}" height="{sq:.2f}" fill="{col}" opacity="{op:.2f}"/>'
        return out

    def rule(x0, x1):
        if x1 <= x0:
            return ""
        if P.get("grad"):
            return (f'<defs><linearGradient id="rg" x1="0" x2="1"><stop offset="0" stop-color="{lcol}" stop-opacity="0"/>'
                    f'<stop offset="1" stop-color="{lcol}" stop-opacity=".8"/></linearGradient></defs>'
                    f'<rect x="{x0:.2f}" y="{y + h / 2 - lw / 2:.2f}" width="{x1 - x0:.2f}" height="{lw}" fill="url(#rg)"/>')
        return f'<rect x="{x0:.2f}" y="{y + h / 2 - lw / 2:.2f}" width="{x1 - x0:.2f}" height="{lw}" fill="{lcol}" opacity="{lop}"/>'

    if pos == "end":
        return rule(0, W - fw - gap) + flag(W - fw)
    if pos == "start":
        return flag(0, rev=True) + rule(fw + gap, W)
    if pos == "both":
        return flag(0, rev=True) + rule(fw + gap, W - fw - gap) + flag(W - fw)
    if pos == "full":
        n2 = int(W / sq)
        P["n"] = n2
        return flag(0)
    if pos == "centre":
        x0 = W / 2 - fw / 2
        return rule(0, x0 - gap) + flag(x0) + rule(x0 + fw + gap, W)
    return ""


U._sep = lambda kind, fg, y: finish(kind, fg, y)

H = U.BAND
VAR = [
    ("i1", "Inverted chequer, leaning 12° (8 sq)", {"phase": 1, "skew": True}),
    ("i2", "Inverted, leaning, 10 squares", {"phase": 1, "skew": True, "n": 10}),
    ("i3", "Inverted, leaning, 6 squares", {"phase": 1, "skew": True, "n": 6}),
    ("i4", "Inverted, leaning, bigger squares", {"phase": 1, "skew": True, "sq": H * .7, "n": 6}),
    ("i5", "Inverted, leaning, cobalt", {"phase": 1, "skew": True, "col": BLUE}),
    ("i6", "Inverted, leaning, fade in", {"phase": 1, "skew": True, "fade": True, "n": 10}),
]
C = []
for k, l, p in VAR:
    P.clear()
    P.update(p)
    U.lockup(f"fin-{k}", U.FONTS[0][2], "finish")
    C.append((f"fin-{k}", l))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:2000px;background:#111;color:#eee;font-family:Arial;padding:56px}}
h1{{font-size:42px}} .lead{{color:#999;margin:10px 0 36px;font-size:17px}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
figure{{background:#1b1b1d;border-radius:10px;overflow:hidden}} .pair img{{width:100%;display:block}}
figcaption{{padding:10px 12px;font-size:14px}} b{{color:#2440FF;margin-right:6px}}</style></head><body>
<h1>AKKI MEISTER — inverted chequered finish</h1><p class="lead">Inverted chequer leaning with the AM on the rule + chequered finish · Clash Grotesk · aligned to the mark's baseline</p>
<div class="grid">{"".join(f'<figure><div class="pair"><img src="upright/d-{n}.svg"/><img src="upright/l-{n}.svg"/></div><figcaption><b>{n[-2:]}</b> {l}</figcaption></figure>' for n, l in C)}</div></body></html>"""
open("../FINAL-AM/finish-inverted.html", "w", encoding="utf-8").write(html)
print(len(C))
