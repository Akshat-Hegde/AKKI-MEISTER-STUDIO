# AKKI MEISTER: social media studio

This folder is the brand kit and production setup for **AKKI MEISTER** (Instagram **@akki_meister**), the personal brand of Akshat Hegde ("Akki"). It covers sim racing, karting, Formula Student and the motorsport lifestyle. Use it to make posts, stories, reels, captions and graphics, all on-brand.

## Brand

- **Mark:** `///AM`. There are three cobalt bars at decreasing opacity (1, .58, .28), then a monogram with a 12° italic lean. Proportions follow φ: bars are 13:8:5, the crossbar sits at 0.618, and width:height is 2.618.
- **Lockup:** the mark, then a hairline with a small inverted chequered finish, then the wordmark "AKKI MEISTER" in spaced Clash Grotesk.
- **Colours:** Midnight `#07080C` (background), Cobalt `#2440FF` (accent), Sky `#5B7BFF` (secondary accent and kickers), Ice `#F3F4F6` (text), Steel `#8C93A3` (muted text).
- **Type:**
  - Clash Display 600 for headlines: uppercase, tight, ending in a full stop, e.g. "SIM TO / TARMAC.", with the last line in Cobalt.
  - Clash Grotesk 600 for kickers: uppercase with wide letter spacing (.3em).
  - JetBrains Mono for small labels and captions inside designs.
  - Fonts are in `AKKI-MEISTER-COMPLETE/fonts/` and `reel/assets/`.
- **Look:** dark midnight background with subtle grain, a soft blue glow at the top and bottom, and a vignette. Photos are slightly desaturated with a cobalt soft-light tint. Use slanted parallelogram panels at 12°, diagonal photo strips and bands, and chequer accents.
- **Handle line:** `@akki_meister` followed by `SIM · TRACK · PADDOCK`.

## Voice

Short, confident and racing-flavoured, but not cheesy. Examples that worked:
- "HEY, I'M AKKI. / I'VE RACED IN SIM RACING. / KARTING. / FORMULA STUDENT."
- "BUILT ON THE RIG." / "SIM TO TARMAC." / "OFF THE CLOCK." / "ON THE FEED."
- Team-radio sign-off: "Copy. See you on track."

Content pillars: sim racing hotlaps, racecraft tips, motorsport lifestyle, rig and setup tours, behind the scenes (coaching, telemetry, the Formula Student build).

Captions are simple: one or two short lines, an optional emoji (🏁 🏎️), `@akki_meister`, then hashtags such as `#simracing #motorsport #karting #formulastudent #racing #simracer #motorsportlife`. Offer a few alternatives.

## What's where

| Path | Contents |
|---|---|
| `AKKI-MEISTER-COMPLETE/` | **The final brand kit. Start here.** |
| `…/logo/` | Lockup in dark and light, round avatars (cobalt, gradient, ice, midnight); SVG and PNG |
| `…/patterns/`, `…/patterns-transparent/` | 8 brand patterns, solid and transparent overlays |
| `…/icons/` | Roundel highlight covers (mark, finish, apex, data, sim, launch) |
| `…/posts/` | 3 teaser posts, 1080×1350 |
| `…/story/` | 8-frame teaser story, 1080×1920 |
| `…/AKKI-MEISTER-reel.mp4` | Final 31 s teaser reel, 1080×1920 |
| `…/index.html` | Open in a browser for an overview of the whole kit |
| `reel/assets/` | **The photo library** (sim rigs, coaching, karts, Formula Student, podiums, suit and helmet) plus fonts and patterns |
| `reel/comp.html` | Reel composition: an HTML page where `window.render(t)` draws frame `t` |
| `reel/tools/scenes.js` | Source of the reel's scenes. Copy it into `comp.html` after the `/* time shift` marker after editing |
| `reel/tools/render.js` | `node render.js stills 3.4 12` writes frames to `reel/stills/`; `events` exports the sound cue list; `video` renders every frame to `frames.mp4` |
| `reel/tools/audio.py` | Builds `reel/audio.wav` from the sound cues, using the licensed track in `reel/music/drums.wav` |
| `work/`, `round*/`, `concepts/` | Logo exploration history. Ignore unless asked. |

Photo crops: check every crop on a rendered still before calling it done. `telemetry.jpg` originally had black bars, so use `telemetry-c.jpg`. For wide diagonal bands, use landscape photos.

## How to make things

- **Posts and stories:** build them as HTML pages at 1080×1350 (feed) or 1080×1920 (story) using the brand fonts and colours. Screenshot them with headless Chrome (puppeteer-core) or Python/Pillow, then look at the result before handing it over.
- **Reel edits:**
  1. Edit `reel/tools/scenes.js`.
  2. Sync it into `comp.html`.
  3. Run `node render.js events`, then `python audio.py`.
  4. Check stills.
  5. Run `node render.js video`.
  6. Mux: `ffmpeg -i frames.mp4 -i audio.wav -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart AKKI-MEISTER-reel.mp4`
  7. Keep `END` the same in scenes.js and audio.py, or the mux cuts the video short.
- **New machine setup:** `render.js` has hard-coded paths from the desktop PC: the puppeteer-core `require` and the Chrome `executablePath`. Fix them first:
  - run `npm i puppeteer-core` (and `sharp` if needed),
  - point `executablePath` at this machine's Chrome or Edge,
  - check that `ffmpeg` and Python with `numpy` are installed.

## The mission (read this first, every session)

Akki wants to become a **popular, genuinely valuable sim racing, motorsport and lifestyle creator**, starting in India. The goals:
- get invited to **sim racing expos and events**,
- earn **F1 paddock access** and **invitations from teams**,
- land **brand partnerships** and **ambassador roles** through content,
- above all, deliver **real value and knowledge**. The audience should learn something from every post.

**Reference creators:**
- Global: Jimmy Broadbent, Super GT, Jardier.
- India: Adi Plays, plus others found in `research/`.

Learn from what made them grow; never copy them.

**Akki's credibility:**
- Competed at the F1 Sim Racing India Open 2026 (top 40 from 33,000+ on the leaderboard).
- Sim racing podiums.
- Karting.
- Formula Student (engineering and driving).
- Coaches sim racing, including kids.
- Understands telemetry and data.

**Every piece of content should serve the mission:** build expertise and trust, show personality and lifestyle, and look premium enough that brands and teams want to be associated with it.

## Content plan and media

- **The plan:** `CONTENT-CALENDAR.md` has the 4-week plan, with hooks, captions, hashtag sets and the assets each post needs. `CLOUD-PLAYBOOK.md` lists the sessions in order. Tick posts off as they're made, and flag anything marked 🔎 for fact-checking.
- **The media library:** `library/` holds Akki's photos and videos. They're deduplicated, photos are resized to 2048 px JPG, and videos are compressed to 1080p MP4. **`MEDIA.md` catalogs every file:** category, what's in it, orientation and best use. Read `MEDIA.md` before choosing anything. Original full-size files stay on Akki's PC and aren't in the repo; ask him if you need a full-resolution original.
- **Choosing media (important):**
  - Pick the photo or clip whose *subject matches the post*:
    - sim racing tips → rig and cockpit shots or onboard clips
    - coaching → the coaching photos
    - Formula Student → FS photos
    - lifestyle → karting, events, people
  - Never use a random or loosely related image just to fill space.
  - Match orientation to format: vertical clips and photos for reels and stories (1080×1920); vertical or square for carousels (1080×1350).
  - Prefer the sharpest, best-lit shot of the set. Avoid repeating the same hero photo across consecutive posts.
  - **Before using a clip:** run `ffprobe` and pull a few frames with ffmpeg to see what actually happens in it. Then cut the best 2–6 s moments. Never assume a clip's content from its filename.
  - Always check crops on rendered stills: faces, wheels, cars and text must not be cut off.
- **Output:** put finished posts in `posts/<date>-<slug>/`: PNGs or MP4 plus `caption.md`.

## Infographic posts (sim racing explainers)

The current focus: carousel infographics on niche sim racing topics, posted on @akki_meister.

- **Format:** Instagram carousel, 1080×1350 per slide, 5–8 slides:
  1. A hook slide: a bold question or claim, e.g. "WHY YOUR F1 26 RACE PACE DIES ON LAP 5."
  2. 3–6 content slides, one idea per slide.
  3. A closing slide: a one-line takeaway, then `@akki_meister` and "follow for more".
- **Content slides:** each has a headline, one visual and a short line or two of copy. Good visuals: a diagram, a chart, a track corner sketch, a settings table, a before/after comparison, or a gauge. Never a wall of text.
- **Where things live:**
  - Build slides in `infographics/<slug>/` as one HTML page with a `.slide` div per slide.
  - Share styles from `infographics/_kit/` (fonts, colours, slide shell, chart helpers). Create the kit on first use and reuse it after.
  - Render each slide to `infographics/<slug>/slide-01.png` etc., with the same puppeteer screenshot approach as `stories-india-open/shoot.js`.
  - Write the caption and hashtags to `infographics/<slug>/caption.md`.
- **Photos:** Akki's own sim racing photos go in `photos/` (create it if missing). Use them as hero images or slide backgrounds with the usual cobalt soft-light tint. Crop with object-position and check that faces and wheels aren't cut off.
- **Style:**
  - Midnight background, Clash Display headlines, Mono labels.
  - Cobalt for data and highlights; Steel for secondary text.
  - Charts are clean lines and bars in Cobalt and Sky with hairline grids. No 3D, no gradients, no stock icons.
  - A small `///AM` mark and `@akki_meister` on every slide, plus a slide counter (`02 / 07`).
  - Decor: the breaking chequered flag (small, a corner only) and the brand patterns in `AKKI-MEISTER-COMPLETE/patterns-transparent/`, kept faint. No busy "vibe-coded" lines, circuits or telemetry squiggles unless the slide is actually about telemetry.
- **Accuracy matters most.** These are expert topics, and the audience will catch mistakes.
  - Never invent numbers, settings, lap times or regulation details.
  - For F1 26 (game) and 2026 F1 regulation specifics (ERS, battery deployment, active aero, override modes), check current sources on the web, or ask Akki, before stating anything as fact.
  - Mark Akki's personal setup values as "my setup", not universal truth.
- **Topic ideas:** ERS and battery management under the 2026 regs, trail braking, brake bias and migration, force-feedback settings, wheel rotation and steering ratio, load-cell pedals, FOV calculation, tyre temperatures and wear, the racing line vs the defensive line, quali vs race mindset, rig ergonomics, sim vs real-car differences, track guides (braking points per corner).

## Preferences learned so far

- **Sound:** subtle and premium. No whooshes, no generic clicks on every photo, and no gimmicky racing sound effects (engines, start-light beeps, radio static). A soft tactile knock on cuts is fine. Music should be a real track kept low in the mix, not synthesized.
- **Visuals:** dynamic layouts (diagonal strips and bands, stacked cards, kinetic type), not static grids. No extra colour-palette sections.
- **Copy:** show the story and what followers can expect. Avoid CV-style phrasing.
- **Workflow:** keep intros short (about 4 s or less). Always check rendered stills for crops and overflow before saying something is finished.
- **Git:** commits in this user's repos must not include a `Co-Authored-By` trailer, because Vercel Hobby blocks those deploys.
