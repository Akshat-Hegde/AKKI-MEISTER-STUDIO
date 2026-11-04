"""Contact sheets of library/_staging (photos + a frame from each video), labelled with filenames."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ST = ROOT / "library" / "_staging"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "library" / "_sheets"
OUT.mkdir(parents=True, exist_ok=True)
TW, TH, COLS, ROWS = 230, 230, 8, 5


def thumb(p):
    if p.suffix == ".mp4":
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout or 2)
        tmp = OUT / "_f.jpg"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(d * .4), "-i", str(p), "-frames:v", "1", "-vf", "scale=400:-2", str(tmp)])
        im = Image.open(tmp).convert("RGB"); tag = f"VID {d:.0f}s"
    else:
        im = Image.open(p).convert("RGB"); tag = ""
    im.thumbnail((TW, TH - 30))
    return im, tag


for g in sorted(d for d in ST.iterdir() if d.is_dir()):
    files = sorted(g.iterdir())
    for k in range(0, len(files), COLS * ROWS):
        S = Image.new("RGB", (COLS * TW, ROWS * TH), "#222"); dr = ImageDraw.Draw(S)
        for i, p in enumerate(files[k:k + COLS * ROWS]):
            x, y = (i % COLS) * TW, (i // COLS) * TH
            im, tag = thumb(p); S.paste(im, (x + (TW - im.width) // 2, y + 2))
            dr.text((x + 4, y + TH - 26), p.stem[:30], fill="#fff")
            if tag: dr.rectangle([x + 4, y + 4, x + 70, y + 18], fill="#2440FF"); dr.text((x + 7, y + 5), tag, fill="#fff")
        S.save(OUT / f"{g.name}-{k // (COLS * ROWS) + 1}.jpg", quality=80)
        print(OUT / f"{g.name}-{k // (COLS * ROWS) + 1}.jpg")
