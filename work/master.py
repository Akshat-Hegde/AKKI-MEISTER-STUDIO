"""Master iteration sheet: every logo iteration, grouped by round, as one HTML page."""
import os, re, glob

ROOT = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/"
SKIP = re.compile(r"concepts-r|saira-test|type-test|-rev\.svg$|-white\.svg$|-orange\.svg$")
ROUNDS = [
    ("concepts", "Round 1", "First concepts · Twin Peaks, Cut Block, Hairpin, Grid Slot, Speed-Line A"),
    ("round2", "Round 2", "Sliced Peaks family · Apex Star, Meister Seal, lockups"),
    ("round3/logos", "Round 3", "Constructed MEISTER type · ligature, ///AM, grid box"),
    ("round4", "Round 4", "Saira Black Italic · Fusion, Speed, Visor crest"),
    ("round5", "Round 5", "Fusion refinements · ///AM, red line, box styles"),
    ("round6", "Round 6", "Weight / gap / flat-tip study + fusions"),
    ("round7", "Round 7", "Square-shouldered A · square and chamfered"),
    ("round8", "Round 8", "Horizontal cut iterations"),
    ("round9", "Round 9", "Block monograms and single-stroke app marks"),
    ("round10", "Round 10", "Typeface × A-tip matrix, full cut, partial cut, equal spacing"),
]


def tiles(folder):
    files = sorted(f for f in glob.glob(ROOT + folder + "/*.svg") if not SKIP.search(os.path.basename(f)))
    out = []
    for f in files:
        name = os.path.basename(f)[:-4]
        wide = any(k in name for k in ("lockup", "wordmark"))
        out.append(f'<figure class="{"wide" if wide else ""}"><div class="art"><img src="file:///{f}"/></div><figcaption>{name}</figcaption></figure>')
    return out, len(files)


body, total = "", 0
for folder, title, sub in ROUNDS:
    t, n = tiles(folder)
    total += n
    body += f'<section><header><h2>{title}</h2><p>{sub}</p><span>{n} iterations · {folder}/</span></header><div class="grid">{"".join(t)}</div></section>'

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>AKKI MEISTER · master iteration sheet</title><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#ECEBE7; font-family:Arial,sans-serif; color:#111; width:1800px; padding:60px; }}
h1 {{ font-size:44px; letter-spacing:-.02em; }}
.lead {{ color:#666; margin:8px 0 40px; font-size:16px; }}
section {{ margin-bottom:56px; }}
header {{ display:flex; align-items:baseline; gap:18px; border-top:2px solid #111; padding-top:14px; margin-bottom:18px; }}
h2 {{ font-size:26px; }} header p {{ color:#444; font-size:15px; }} header span {{ margin-left:auto; color:#888; font-size:13px; }}
.grid {{ display:grid; grid-template-columns:repeat(8,1fr); gap:12px; }}
figure {{ background:#fff; border-radius:8px; overflow:hidden; }}
figure.wide {{ grid-column:span 2; }}
.art {{ height:170px; display:flex; align-items:center; justify-content:center; padding:10px; }}
.art img {{ max-width:100%; max-height:100%; }}
figcaption {{ font-size:11px; color:#555; padding:7px 10px; border-top:1px solid #eee; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
</style></head><body><h1>AKKI MEISTER — master iteration sheet</h1><p class="lead">{total} logo iterations across 10 rounds · reversed duplicates omitted · files live in akki-meister-logos/&lt;round&gt;/</p>{body}</body></html>"""
open(ROOT + "master-iterations.html", "w", encoding="utf-8").write(html)
print("total", total)
