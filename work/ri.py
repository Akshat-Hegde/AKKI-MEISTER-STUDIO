import os, re
D = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/AKKI-MEISTER-LAUNCH/"
h = open(D + "index.html", encoding="utf-8").read()
pats = sorted(f for f in os.listdir(D + "patterns") if f.endswith(".svg"))
grid = '<div class="grid3">' + "".join(f'<div class="card"><img src="patterns/{f}"/><span><b>{f[:2]}</b> {f[3:-4].replace("-", " ").upper()} · <a href="patterns/{f}" download style="color:#5B7BFF">SVG</a> · <a href="patterns/{f[:-4]}.png" download style="color:#5B7BFF">PNG</a></span></div>' for f in pats) + '</div>'
h = re.sub(r'(<h2>Pattern system</h2><p>)[^<]*(</p></div>)<div class="grid3">.*?(?=</section>)', lambda m: m.group(1) + f"{len(pats)} patterns, all derived from the mark · SVG + PNG" + m.group(2) + grid, h, flags=re.S)
for title, d, cls, sub in (("Teaser posts", "posts", "grid3", "1080 × 1350 · introducing · logo breakdown · follow the line"), ("Teaser story", "story", "grid6", "1080 × 1920 · post in order")):
    items = "".join(f'<div class="card"><img src="{d}/{f}"/><span>{f}</span></div>' for f in sorted(os.listdir(D + d)))
    h = re.sub(rf'(<h2>{title}</h2><p>)[^<]*(</p></div>)<div class="{cls}">.*?(?=</section>)', lambda m: m.group(1) + sub + m.group(2) + f'<div class="{cls}">{items}</div>', h, flags=re.S)
open(D + "index.html", "w", encoding="utf-8").write(h)
print(len(pats), len(os.listdir(D + "posts")), len(os.listdir(D + "story")))
