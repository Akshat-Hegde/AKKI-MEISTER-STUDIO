"""Add new clips to the library without rebuilding it.

Encodes each clip in NEW with the same settings as build_library.py, then appends
it to library/_index.json and to its category in MEDIA.md. Clips already in the
index are skipped, so it is safe to rerun. Edit NEW for the next batch of uploads.
"""
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = "videos/new vids"
NEW = {  # source file -> (category, note)
    "IMG_9855.MOV": ("telemetry", "live telemetry comparison dashboard on a monitor: Suzuka map, onboard vs player speed and gear (strong; best for THE DEBRIEF and data posts; CROP THE TOP before posting: the browser bookmarks bar shows email addresses, and an orange warning banner sits under the header)"),
    "1723324577150150.MP4": ("sim-rig", "over-the-shoulder at the home rig: hands on wheel, F1 race on screen, colour-changing ambient light (strong; hotlap reels, moody intros)"),
    "IMG_0130.MOV": ("sim-rig", "F1 Sim Racing India Open venue: rows of Playseat rigs with people (strong; event recap, India scene posts)"),
    "IMG_0086.mov": ("sim-rig", "Akki in helmet at home rig, screen visible (strong)"),
    "IMG_1875.MOV": ("sim-rig", "driving at a blue-lit venue rig, friend watching"),
    "IMG_5665.MOV": ("sim-rig", "hands on wheel in a red pro rig"),
    "IMG_2856.MOV": ("sim-rig", "Race At Will rig: screen and hands on wheel"),
    "IMG_2853.MOV": ("sim-rig", "Race At Will venue walkthrough"),
    "IMG_5009.MOV": ("sim-rig", "Race At Will banner, very short b-roll"),
    "IMG_5036.MOV": ("sim-rig", "Race At Will triple-screen rig, very short b-roll"),
    "IMG_6312.MOV": ("sim-rig", "helmeted driver at home rig"),
    "IMG_2461.MOV": ("sim-coaching", "Akki coaching a friend at the rig with a tablet, extends race-engineer.mp4 (strong)"),
    "IMG_2465.MOV": ("sim-coaching", "Akki coaching a friend at the rig with a tablet, extends race-engineer.mp4 (strong)"),
    "IMG_4451.MOV": ("karting", "karts at a kart track; use the moment nearest the camera"),
    "IMG_4452.MOV": ("karting", "karts at a kart track, closest pass of this set"),
    "IMG_4462.MOV": ("karting", "karts at a kart track; use the moment nearest the camera"),
}


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", str(p)], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    return j["streams"][0]["width"], j["streams"][0]["height"], round(float(j["format"]["duration"]), 1)


idx_path = ROOT / "library" / "_index.json"
idx = json.loads(idx_path.read_text(encoding="utf-8"))
have = {e["src"] for e in idx}
md_path = ROOT / "MEDIA.md"
md = md_path.read_text(encoding="utf-8").split("\n")

for name, (cat, note) in NEW.items():
    src = f"{SRC}/{name}"
    if src in have:
        continue
    out = ROOT / "library" / cat / (Path(name).stem.lower().replace("_", "-") + ".mp4")
    if out.exists():
        raise SystemExit(f"{out} already exists, refusing to overwrite")
    tmp = out.with_suffix(".tmp.mp4")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(ROOT / "media" / src),
                    "-vf", "scale='if(gt(iw,ih),-2,min(1080,iw))':'if(gt(iw,ih),min(1080,ih),-2)'",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.rename(out)
    w, h, dur = probe(out)
    orient = "vertical" if h > w else "horizontal" if w > h else "square"
    rel = f"{cat}/{out.name}"
    idx.append({"file": rel, "src": src, "type": "video", "w": w, "h": h, "dur": dur, "cat": cat, "note": note, "orient": orient})
    # last table row of this category's section, then bump the count in the summary table
    i = md.index(f"## {cat}") + 1
    while not md[i].startswith("|"):
        i += 1
    while md[i].startswith("|"):
        i += 1
    md.insert(i, f"| `{rel}` | video | {orient} | {w}×{h}, {dur}s | {note} |")
    for k, line in enumerate(md):
        m = re.match(rf"(\| `{cat}/` \| )(\d+)( \|.*)", line)
        if m:
            md[k] = f"{m[1]}{int(m[2]) + 1}{m[3]}"
    idx_path.write_text(json.dumps(idx, indent=1, ensure_ascii=False), encoding="utf-8")
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"{rel}  {w}x{h}  {dur}s  {out.stat().st_size / 1e6:.1f} MB", flush=True)
