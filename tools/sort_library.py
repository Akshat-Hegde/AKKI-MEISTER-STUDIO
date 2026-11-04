"""Move library/_staging/* into library/<category>/ and write MEDIA.md.
Categories and descriptions come from a visual review of the contact sheets (tools/contact_sheets.py)."""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"; ST = LIB / "_staging"

CATS = {
 "sim-rig":        "Akki driving or sitting in sim rigs: home setup, triple-screen rigs, sim venues and events. Best for sim racing tips, rig/setup posts, hotlap reels.",
 "sim-coaching":   "Coaching sessions: Akki coaching drivers (incl. kids) at a karting-venue sim tent, explaining telemetry on a tablet, group briefings. Best for coaching, teaching, community, credibility.",
 "telemetry":      "Telemetry/data screens, track maps, laptop setups. Best for data, telemetry and engineering posts.",
 "karting":        "Akki karting: action shots (Rotax, rental/race karts), panning shots, track portraits, karting clips. Best for sim-to-real, lifestyle, racecraft.",
 "formula-student":"Formula Student: the car (#10), workshop builds, chassis, suspension, testing at the track, team presentations, BIC pit-lane photos. Best for engineering, sim-to-real, story posts.",
 "portraits":      "Akki in race suit / team kit, posed portraits (studio wall, outdoors, kart track at sunset). Best for hook slides, intros, announcements, profile/media kit.",
 "lifestyle":      "Events and lifestyle: F1/Williams fan moments, US trip (Texas), vintage car, paddock-style shots. Best for lifestyle and personality posts.",
 "results":        "Results graphics and trophies: runner-up (Forza Horizon 5 league), championship standings, P2/P3 tournament posts. Best for credibility, media kit, recap posts.",
 "design":         "Sketches and design work: wheel/button-box sketches, car design on laptop. Best for engineering/creative process posts.",
 "website":        "Photos already used on Akki's portfolio website (curated, good quality): podium shots (Jeddah, Austria, Brazil, Spa, VRH, Supra, Red Rabbit, Teho), rig, telemetry, Formula Student, karting, portraits.",
 "screenshots":    "Phone/app screenshots and screen recordings of old posts (Instagram, LinkedIn). Reference only; avoid in new posts.",
}
G = {  # filename stem -> (category, note)
 "0646c0a0-2712-4f04-9285-36bb3054b7c1": ("design", "collage: rig photos + wheel sketches"),
 "2edfcfcd-e69c-4f6a-a892-b8af13081da2": ("formula-student", "clip: team around the FS car in the workshop"),
 "37baf5b4-f209-42cc-9d9c-39dbed4013eb": ("design", "pencil sketch of a sim wheel / button box"),
 "5f0b7f44-1afe-4c58-90cc-389afe093b82": ("formula-student", "FS car at night with team"),
 "7e76cb51-ff6b-4f43-94d1-fab48be8ef79": ("karting", "kart panning shot, motion blur (strong)"),
 "dd6f54db-2471-4640-a5a8-3b6120a5c5d0": ("karting", "kart panning shot, motion blur"),
 "988a01d1-e2a6-464c-a40e-b849e9dbab85": ("sim-rig", "driver in a rig at a sim event, screen visible"),
 "ec76bb75-662a-4ba0-92d6-94c446a90dd6": ("lifestyle", "F1 fan-zone sim rig"),
 "esports-flying-lap": ("sim-rig", "screen capture of an esports flying lap with timing tower (58s) - good for hotlap/lap-breakdown reels"),
 "img-0037": ("sim-rig", "Akki in helmet + hoodie at home rig (moody)"),
 "img-0041": ("sim-rig", "Akki in helmet at home rig, relaxed pose"),
 "img-0170": ("design", "car design on laptop"),
 "img-0172": ("design", "car design on laptop + game screen"),
 "img-0415": ("formula-student", "night driving clip (43s), dark"),
 "img-0421": ("formula-student", "night driving clip (53s), dark"),
 "img-0502": ("portraits", "race suit + helmet, arms crossed, studio wall"),
 "img-0505": ("portraits", "race suit + helmet, hands on helmet (strong hook image)"),
 "img-0507": ("portraits", "race suit, standing"),
 "img-0511": ("portraits", "race suit holding helmet"),
 "img-0517": ("portraits", "race suit, flexing / celebrating (fun)"),
 "img-0538": ("portraits", "race suit outdoors, holding helmet, glass building"),
 "img-0541": ("formula-student", "FS car #10 being worked on"),
 "img-0548": ("formula-student", "clip (28s), open lot / test area"),
 "img-0856": ("lifestyle", "vintage pickup truck at a car show"),
 "img-0941": ("sim-rig", "home rig setup with shelves, wheels on wall (setup tour)"),
 "img-0972": ("sim-rig", "clip (21s) at home rig"),
 "img-1316": ("lifestyle", "'Welcome to Texas' - US trip with a friend"),
 "img-1802": ("sim-rig", "Akki at desk rig, Red Bull shirt"),
 "img-1805": ("sim-rig", "Akki at desk rig"),
 "img-1806": ("sim-rig", "Akki at desk rig"),
 "img-1826": ("sim-coaching", "Akki standing, coaching someone at desk rig"),
 "img-1834": ("sim-rig", "clip (19s): triple-screen rig at a venue"),
 "img-2474": ("karting", "clip (75s): karting track, wide"),
 "img-2539": ("karting", "clip (13s): karting track"),
 "img-2541": ("karting", "clip (19s): karting track"),
 "img-2610": ("karting", "kart panning shot (strong)"),
 "img-2612": ("karting", "Akki in suit at kart track, arms crossed"),
 "img-2613": ("karting", "kart + chequered flag"),
 "img-3079": ("portraits", "orange team shirt at kart track, sunset"),
 "img-3080": ("portraits", "orange team shirt at kart track, sunset, close"),
 "img-3082": ("portraits", "dark shirt at kart track, dusk"),
 "img-4365": ("sim-rig", "clip (5s) at home rig"),
 "img-4366": ("telemetry", "telemetry traces on monitor behind wheel"),
 "img-4368": ("telemetry", "telemetry traces on monitor behind wheel"),
 "img-4609": ("sim-rig", "driving with neon lighting (moody, good hero)"),
 "img-4762": ("sim-rig", "clip (12s): driving with a friend"),
 "img-4856": ("sim-rig", "triple-screen rig, dark"),
 "img-4857": ("sim-rig", "clip (18s): triple-screen rig"),
 "img-4862": ("sim-rig", "clip (6s): triple-screen rig"),
 "img-5010": ("sim-rig", "Akki in an orange-frame rig"),
 "img-5024": ("sim-rig", "triple-screen rig, from behind"),
 "img-5033": ("sim-rig", "triple-screen rig, from behind"),
 "img-5112": ("sim-rig", "triple-screen rig"),
 "img-5265": ("sim-rig", "driving in red light"),
 "img-5386": ("sim-rig", "triple-screen pro rig at venue"),
 "img-5390": ("sim-rig", "rig at orange-graffiti venue"),
 "img-5415": ("sim-rig", "rig at orange venue, wide (good)"),
 "img-6229": ("sim-rig", "Akki in rig, orange venue"),
 "img-6230": ("sim-rig", "Akki in rig, orange venue"),
 "img-6232": ("sim-rig", "Akki in rig, orange venue"),
 "img-6234": ("sim-rig", "Akki in rig, orange venue (smiling)"),
 "img-6636": ("lifestyle", "Atlassian Williams Racing flag with a friend"),
 "img-7577": ("sim-rig", "clip (43s): driving a rig"),
 "img-7875": ("design", "wheel on desk with sketches"),
 "img-8084": ("lifestyle", "at a circuit / paddock area"),
 "img-8214": ("sim-rig", "clip (6s): wheel close-up / race on screen"),
 "img-8254": ("karting", "clip (12s): kart on track behind tyre wall"),
 "img-8350": ("sim-rig", "Red Bull neon sim setup, Akki driving (strong hero)"),
 "img-8758": ("telemetry", "telemetry on monitor, wheel in front"),
 "img-9142": ("sim-rig", "Akki in a pro cockpit rig at an event"),
 "img-9148": ("sim-rig", "cockpit view: wheel + curved screen"),
 "img-9320": ("telemetry", "telemetry + track map on monitor"),
 "img-9939": ("sim-rig", "clip (6s): driving at a venue"),
 "img-9997": ("telemetry", "track map on monitor + wheel (Marina Bay?)"),
 "lotus": ("telemetry", "clip (9s): laptop setup / data"),
 "race-engineer": ("sim-coaching", "clip (7s): two people at the rig, engineer/driver dynamic"),
 "reel-1": ("karting", "clip (41s) black & white kart footage"),
 "reel": ("formula-student", "clip (7s): FS car outside"),
 "screenshot-2025-06-10-210507": ("sim-rig", "triple-screen rig screenshot"),
 "sim-intro": ("sim-rig", "clip (22s): Akki talking to camera at his rig - TALKING-HEAD intro, great for hooks"),
 "img-5384": ("results", "RUNNER-UP graphic, Acer Predator Forza Horizon 5 league"),
 "img-5943": ("results", "AM Championship standings (VRH) - Akki P4"),
 "toruni": ("results", "P2 overall at a sim racing event (story graphic)"),
 "tourni-2": ("results", "P2 in VRH ACC AM Championship (story graphic)"),
 "img-5078": ("screenshots", ""), "img-7798": ("screenshots", ""), "img-9848": ("screenshots", ""),
 "ogl": ("screenshots", "screen recording of an old post"), "raceatwill": ("screenshots", "screen recording of an old post"),
 "screenshot-2025-06-10-210439": ("screenshots", "LinkedIn profile screenshot"),
}
GROUP_CAT = {"formula-student": "formula-student", "karting": "karting", "sim-coach": "sim-coaching", "website": "website"}
NOTES = {  # notable picks inside the named groups
 "sim-coaching": {"dsc00978": "Akki explaining to a young driver in the rig (strong)", "dsc00987": "telemetry traces on tablet (strong data shot)",
   "dsc00988": "reviewing telemetry on tablet", "e": "coaching with tablet, vertical", "g": "telemetry on tablet",
   "dsc00970": "Akki briefing a group", "dsc00945": "group briefing in the tent", "dsc00963": "Akki portrait, Red Bull kit",
   "dsc00601": "karting on track at the venue", "dsc00603": "karting on track", "dsc00604": "karting on track"},
 "formula-student": {"img-1636": "Akki in suit sitting on FS car #10 (strong hero)", "img-1679": "FS car at BIC with crew",
   "img-1589": "Akki on the BIC pit straight", "img-1605": "BIC pit straight, wide", "img-0550": "FS car, front 3/4",
   "img-20241014-wa0021": "Akki with trophy, black background (cut-out style)", "posterrrr-mustangggg": "'Danke 2024' team poster",
   "pxl-20230606-123607415-portrai": "team jacket 'Akshat - Intern Suspension'", "img-7524": "clip (14s): workshop build",
   "img-7783": "clip (10s): workshop", "img-1013": "team presentation (projector)", "img-1014": "team presentation"},
 "karting": {"img-6017": "Rotax kart in action, Akki (strong)", "img-6018": "Rotax kart in action", "img-6019": "Rotax kart in action",
   "img-2636": "kart panning shot", "1691336118710": "Akki with helmet at Indian Racing League backdrop (strong)",
   "img-6791": "pack of karts racing", "20241109182011-2-nef": "kart cornering"},
 "website": {"podium-p1-jeddah": "P1 podium Jeddah", "podium-p1-supra": "P1 podium", "podium-p1-redrabbit": "P1 podium",
   "podium-p2-austria": "P2 podium Austria", "podium-p2-brazil": "P2 podium Brazil", "podium-p2-teho": "P2 podium",
   "podium-p3-spa": "P3 podium Spa", "podium-p3-vrh": "P3 podium VRH", "williams": "Williams sim rig",
   "telemetry": "telemetry screen (has black side bars; use telemetry-review or crop)", "fscarbw": "FS car side-on, B&W, landscape"},
}

idx = json.loads((LIB / "_index.json").read_text())
moved = []
for e in idx:
    p = LIB / e["file"]; group = p.parent.name; stem = p.stem
    if group == "unsorted":
        cat, note = G.get(stem, ("screenshots", "unreviewed"))
    else:
        cat = GROUP_CAT.get(group, group); note = NOTES.get(cat, {}).get(stem, "")
    dst = LIB / cat / p.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if p.exists(): shutil.move(str(p), str(dst))
    e.update(file=f"{cat}/{p.name}", cat=cat, note=note,
             orient="vertical" if e["h"] > e["w"] * 1.1 else ("horizontal" if e["w"] > e["h"] * 1.1 else "square"))
    moved.append(e)
(LIB / "_index.json").write_text(json.dumps(moved, indent=1))
shutil.rmtree(ST, ignore_errors=True)

L = ["# MEDIA.md: Akki's photo and video library", "",
     "Every file in `library/`, sorted by category from a visual review. Photos: JPG, long edge 2048 px. Videos: H.264 MP4, short edge 1080 px or less.",
     "Originals (full resolution, HEIC/MOV) stay on Akki's PC in `media/`; ask him if a full-size original is needed.", "",
     "**How to choose media:** match the post's subject to the category, prefer files with a note marked *(strong)*, match orientation to the format",
     "(vertical for reels/stories, vertical or square for 1080×1350 carousels), and look at the actual frames of a clip before cutting it.", "",
     "| Category | Files | What it is / best for |", "|---|---|---|"]
from collections import Counter
cnt = Counter(e["cat"] for e in moved)
for c, d in CATS.items(): L.append(f"| `{c}/` | {cnt.get(c, 0)} | {d} |")
for c in CATS:
    items = sorted((e for e in moved if e["cat"] == c), key=lambda e: (e["type"], e["file"]))
    if not items: continue
    L += ["", f"## {c}", "", CATS[c], "", "| File | Type | Orientation | Size | Notes |", "|---|---|---|---|---|"]
    for e in items:
        size = f'{e["w"]}×{e["h"]}' + (f', {e["dur"]}s' if e["type"] == "video" else "")
        L.append(f'| `{e["file"]}` | {e["type"]} | {e["orient"]} | {size} | {e["note"]} |')
(ROOT / "MEDIA.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(dict(cnt), len(moved))
