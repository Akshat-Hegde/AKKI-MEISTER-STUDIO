# AKKI MEISTER templates

One command for every signature-series format. Write a small JSON spec, point it at files in `library/`, run:

```bash
node templates/make.js <spec.json>
```

| `"template"` | Series | Output |
|---|---|---|
| `apex-notes` | 📐 APEX NOTES carousel | `slide-01.png …` 1080×1350 |
| `debrief-carousel` | 🎙️ THE DEBRIEF, two-lap comparison | `slide-01.png …` + `debrief-numbers.json` |
| `debrief-reel` | 🎙️ THE DEBRIEF reel | `<name>.mp4` 1080×1920 + `stills/` |
| `hotlap` | ⏱️ Hotlap / onboard overlay | `<name>.mp4` + `stills/` |
| `sim-to-tarmac` | 🏁 SIM TO TARMAC kinetic reel | `<name>.mp4` + `stills/` |
| `stories` | Story set: announcement · result · quote · question · poll | `story-01-<type>.png …` 1080×1920 |

Working examples (all tested with real library files) are in `templates/examples/`, their renders in `templates/samples/`. Sample MP4s aren't committed (like every render, `*.mp4` is gitignored); re-create one with its command, or look at the committed `*-stills.jpg` contact sheet.

**Flags:** `--out <dir>` overrides the output folder · `--no-video` renders only the review stills of a reel (seconds, not minutes) · `--stills 3.5,12` adds review stills at those reel times.
**Output folder:** `"out"` in the spec, else `posts/<date>-<slug>/` when `"date"` and `"slug"` are set, else next to the spec. If the spec has a `"caption"`, it's written to `caption.md`.
**Media paths:** relative to the spec, the repo root, or `library/` (so `"library/sim-rig/img-0972.mp4"` and `"sim-rig/img-0972.mp4"` both work).

**Before posting, always:** open the PNGs / `stills/` and scrub the MP4. The renderers print `⚠` lines for text that overflows a slide, a visual taller than its box, or text over a story's sticker zone, but crops of faces, wheels and cars still need your eyes.

---

## Setup (once per machine)

- **Node 18+** and **Playwright** (`npm i playwright`, then `npx playwright install chromium`), or puppeteer-core with `CHROME_PATH` pointing at Chrome/Edge (same fallback as `outreach/media-kit/render.js`).
- **ffmpeg / ffprobe** on PATH (reels only).
- **Python 3 + numpy** (reels only: the knock track). Set `PYTHON=python` on Windows if `python3` isn't the name.
- Library videos are Git LFS: run `git lfs pull` after cloning, or ffprobe will say "moov atom not found".

---

## 1 · APEX NOTES carousel (`apex-notes`)

Example: `infographics/trail-braking/spec.json` → renders into the same folder.

```json
{ "template": "apex-notes", "series": "APEX NOTES", "number": 2,
  "pattern": "AKKI-MEISTER-COMPLETE/patterns-transparent/02-pinstripe-overlay.png",
  "slides": [ { "type": "hook", … }, { "type": "content", … }, { "type": "close", … } ],
  "caption": "…" }
```

**Slides**
- `hook`: `photo`, `pos` (object-position, check faces), `kicker`, `title` (array of lines; last line goes Cobalt, end with a full stop), `sub`, `size`.
- `content`: `kicker` ("02 · Why it works"), `title`, one `visual`, `body` (1–2 lines), `note` (small footer label, e.g. "Illustrative · not real data", "My setup"). Layout knobs: `visualTop`, `visualHeight`, `bodyTop`, `size`.
- `close`: `title` (the one-line takeaway), `body`, `cta` (defaults to "FOLLOW FOR MORE · SAVE THIS").

**Visuals** (`visual.type`)
| type | fields |
|---|---|
| `chart` | `series:[{label, points:[[x,y]…], color, width, dash, area, dots:[[x,y,label,"start"/"end"]]}]`, `xLabel`, `yLabel`, `xDomain`, `yDomain`, `marks:[{x,label}]`, `bands:[{x0,x1,label}]`, `zeroLine`, **`illustrative: true`** (hides numbers: use it for concept shapes, never fake numbers) |
| `bars` | `items:[{label, value, note, hl}]`, `unit`, `dec` |
| `table` | `columns`, `rows` (a cell can be `"main||sub"`), `highlight:[rowIndex]`, `mono:[colIndex]` |
| `before-after` | `before`/`after`: `{label, title, body, visual}` (a mini chart or corner sketch) |
| `corner` | track-corner sketch: `turns:[{angle, radius, dir:"L"/"R"}]`, `straight:[entry, …, exit]`, `trackWidth`, `line:{apex: 0.5 (lower = earlier apex)}`, `altLine` (a second, dashed line, e.g. defensive), `brake:{from, to, peak}` (thick Cobalt = pressure), `markers:[{at:"brake"/"turnin"/"apex"/"exit"/0–1, label, side, dy}]` |
| `flow` | `steps:[{title, body}]` (drills, procedures) |
| `split` | `left/right:{label, value}` (e.g. brake bias %) |
| `gauge` | `value, min, max, label, unit` |
| `car-load` | `cars:[{front, rear, frontText, rearText, label}]` (weight-transfer concept) |
| `stats` | `items:[{value, label, hot}]` |
| `photo` | `src`, `pos` |

Inline text: `**bold**` → Sky emphasis, `~~aside~~` → Steel.

## 2a · THE DEBRIEF carousel (`debrief-carousel`)

Example: `templates/examples/debrief-carousel.json`. Input = **two lap CSVs** (yours = `lapA`, the driver's = `lapB`).

- CSV columns, matched loosely: `distance` (m) and `time` (s) are required; `speed` (km/h, or m/s if the column says `_ms`), `throttle`, `brake` (0–1 or 0–100), `steer` are optional. Lines starting with `#` are ignored. Export from whichever tool the driver uses (F1 games broadcast UDP telemetry that many free apps record), one row per sample, one lap per file.
- Corners: `"corners": [{"name":"T1","from":480,"to":700}, …]` in metres, or leave `[]` to auto-detect braking zones from lap A.
- Everything is **computed**: gap, the `focus` worst corners, brake points, minimum speeds, time lost. The numbers are also written to `debrief-numbers.json`; check them before posting.
- Text fields can use `{gap}`, `{lost}`, `{nWord}`, `{share}`, `{lapA}`, `{lapB}`, `{c1}`, `{c2}`, `{early}`, `{vmA}`, `{vmB}`, `{track}`.
- Slides: hook → lap times + gap → full speed trace (worst corners highlighted) → delta → worst corner zoom (both brake points) → corner table → `drill` (flow) → "Send me your lap".
- `"demo": true` stamps **DEMO DATA · NOT A REAL LAP** on every slide. The example uses synthetic laps from `templates/examples/demo-data/make-demo-laps.js`, so the sample must never be posted as-is.

## 2b · THE DEBRIEF reel (`debrief-reel`), 3 · Hotlap (`hotlap`), 5 · Sim to Tarmac (`sim-to-tarmac`)

All three share one engine (`templates/lib/reel.js` + `templates/reel/reel.html`). Examples: `templates/examples/debrief-reel.json`, `hotlap.json`, `sim-to-tarmac.json`.

```json
{ "template": "hotlap", "name": "hotlap-nurburgring",
  "title":   { "kicker": "HOTLAP · ONBOARD", "lines": ["Nürburgring", "GP."], "sub": "…", "dur": 2.6 },
  "header":  { "kicker": "…", "title": ["…"], "sub": "…" },
  "segments": [ { "type": "clip", "src": "library/sim-rig/esports-flying-lap.mp4", "in": 13, "out": 47,
                  "fit": "band", "crop": [560, 0, 1258, 960], "lap": true, "audio": 0.5 } ],
  "lap":   { "offset": 2.953, "best": "BEST 1:27.130 · P2 IN QUALIFYING",
             "splits": [ { "name": "S1", "time": 42.104, "delta": "+0.08" }, { "name": "S2" }, { "name": "S3" } ] },
  "notes": [ { "lap": 19.5, "kicker": "Sector 1", "text": "…", "dur": 3.4 } ],
  "inputs": { "csv": "my-lap-inputs.csv", "lapTimeAtStart": 0 },
  "end":   { "kicker": "…", "lines": ["Copy.", "See you on track."], "body": "…", "dur": 3.2 },
  "music": { "src": "reel/music/drums.wav", "gain": 0.16 } }
```

**Segments** play back to back (`t` is reel time):
- `clip`: `src`, `in`, `out` or `dur`. `fit: "cover"` (vertical clips, full bleed; `focus: "x% y%"`, `zoom`) or `fit: "band"` (landscape screen recordings: the `crop` rectangle `[x,y,w,h]` of the source becomes a full-width band, with the persistent `header` above and the lap timer below). Optional: `tag` (chip, e.g. "SIM · HOME RIG"), `kicker` + `lines` (kinetic type), `size`, `linesY`, `audio` (clip sound level, default 0.3), `dim`, `wipe` (Cobalt 12° wipe into this cut), `lap: true` (lap timer runs on this clip).
- `split`: `top` / `bottom` clips (`src`, `in`, `focus`), `tags`, `lines`. Sim on top, real below.
- `card`: a full-screen brand card: `kicker`, `lines`, and `steps` (drill), `body`, or `chart` (a lineChart spec; set `demo` if the data isn't real).

**Lap timer, without inventing anything:** the overlay timer is the game's own timer. Pause the recording on two or three frames, read the in-game lap time, and set `lap.offset = lap time − clip time` (they should agree to within a frame). Splits: `time` is the split as shown by the game, `delta` is copied exactly as shown; the main timer holds the split for `lap.hold` seconds (2.5) in Sky. Splits with no `time` show "—".

**Notes** (`notes`): sector or coaching cards, placed by lap time (`lap`) or reel time (`t`).

**Inputs overlay** (`inputs`): throttle / brake bars + a steering dial, driven by a CSV with `time`, `throttle`, `brake`, `steer` columns. `lapTimeAtStart` = the lap time of the CSV's first row; `steerRange` = the CSV value at full lock; `steerDeg` = how far the dial turns. Only use a real export of *that* lap; with no CSV the widget is simply not drawn.

**Title** (≤ 3.8 s, intros stay short) plays over the first footage. **End** is a midnight card with the lockup, the headline, a body line and `@akki_meister`.

**Audio** (CLAUDE.md preferences): clip sound kept low, a soft tactile knock on cuts and a quiet tick when type lands (`templates/lib/audio.py`). No whooshes, no engine/beep/radio effects. Music is a real, licensed track you provide (`music.src`, default gain 0.16 ≈ −16 dB, faded in and out). The licensed `reel/music/drums.wav` lives on Akki's PC (gitignored); if the file is missing, the render warns and continues without music.

Rendering speed: ~3–5 s of compute per second of reel. Footage is cached in `<out>/.work/` (gitignored), so re-rendering after text tweaks skips the slow ffmpeg pass. Use `--no-video` while iterating on layout.

## 4 · Stories (`stories`)

Example: `templates/examples/stories.json`. `"stories": [ … ]`, each with a `type`:
- `announcement`: `photo`, `pos`, `kicker`, `title`, `body`, `chips:[{value,label,hot}]`
- `result`: `photo`, `kicker` (event), `title`, `chips`, `body`, optional `rows:[{pos,name,pts,hl}]` (standings)
- `quote`: `photo` (full bleed), `kicker`, `quote`, `by`
- `question` / `poll`: `kicker`, `title`, `body`, `photo` (diagonal strip at the bottom). The bracketed box is where the Instagram question/poll sticker goes; `zoneLabel: ""` hides its faint label.
Common: `label` (shown in the counter), `pattern`, `flag: false`, `cta` (a Cobalt pill above the handle).

## Shared kit

`infographics/_kit/` holds the brand: `kit.css` (fonts, colours, grain/glow/vignette, photo treatment, chips, tables), `kit.js` (mark, lockup, breaking chequered flag, charts, corner sketches, flows, gauges), `logo.js`, fonts and the faint patterns. Every template uses it, so a brand tweak there updates everything.
