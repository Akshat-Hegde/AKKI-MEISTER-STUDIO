"""Build library/ from media/ (Akki's raw uploads) + the website photos.

- drops exact duplicates (md5), preferring files inside a named folder over loose ones
- photos -> JPG, long edge 2048 px, EXIF-rotated, q85   (originals in media/ stay local, untracked)
- videos -> H.264 MP4, short edge <= 1080, CRF 26, AAC 128k
- writes library/_index.json (source path, size, orientation, duration) for the catalog
Run from the repo root:  python tools/build_library.py
"""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "media"
WEB = Path(os.environ.get("WEBSITE_PHOTOS", r"C:\Users\admin\Akki-Portfolio-main\3d_portfolio\src\assets\photos"))
OUT = ROOT / "library"
IMG = {".jpg", ".jpeg", ".png", ".heic", ".heif"}
VID = {".mov", ".mp4", ".m4v"}


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


files = [p for p in SRC.rglob("*") if p.is_file() and p.suffix.lower() in IMG | VID]
files += [p for p in WEB.glob("*") if p.is_file() and p.suffix.lower() in IMG]
# prefer: website > named subfolder > loose in photos/videos ; then shorter name (drops "- Copy")
def rank(p):
    rel = p.relative_to(SRC) if SRC in p.parents else Path("website") / p.name
    depth = 0 if rel.parts[0] == "website" else (1 if len(rel.parts) > 2 else 2)
    return (depth, len(p.name))

seen, keep = {}, []
for p in sorted(files, key=rank):
    h = md5(p)
    if h in seen:
        continue
    seen[h] = p; keep.append(p)

index = []
for p in keep:
    if SRC in p.parents:
        rel = p.relative_to(SRC); group = slug(rel.parts[-2]) if len(rel.parts) > 2 else "unsorted"
    else:
        rel = Path("website") / p.name; group = "website"
    ext = p.suffix.lower(); stem = slug(p.stem)
    try:
        if ext in IMG:
            dst = OUT / "_staging" / group / f"{stem}.jpg"
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
                im.thumbnail((2048, 2048), Image.LANCZOS)
                im.save(dst, "JPEG", quality=85, optimize=True, progressive=True)
            w, h = Image.open(dst).size
            index.append({"file": str(dst.relative_to(OUT)).replace("\\", "/"), "src": str(rel).replace("\\", "/"), "type": "photo", "w": w, "h": h})
        else:
            dst = OUT / "_staging" / group / f"{stem}.mp4"
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(p),
                                "-vf", "scale='if(gt(iw,ih),-2,min(1080,iw))':'if(gt(iw,ih),min(1080,ih),-2)'",
                                "-c:v", "libx264", "-preset", "medium", "-crf", "26", "-pix_fmt", "yuv420p",
                                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(dst)], check=True)
            pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                            "stream=width,height:format=duration", "-of", "json", str(dst)],
                                           capture_output=True, text=True).stdout)
            st = pr["streams"][0]
            index.append({"file": str(dst.relative_to(OUT)).replace("\\", "/"), "src": str(rel).replace("\\", "/"), "type": "video",
                          "w": st["width"], "h": st["height"], "dur": round(float(pr["format"]["duration"]), 1)})
        print("ok ", rel, flush=True)
    except Exception as e:
        print("SKIP", rel, e, flush=True)

(OUT / "_index.json").write_text(json.dumps(index, indent=1))
print(f"\nkept {len(keep)} of {len(files)} files ({len(files) - len(keep)} duplicates dropped)")
