# Media kit

| File | What |
|---|---|
| `slide-01.png` … `slide-04.png` | 4 slides, 1080×1350, for DMs and IG: who I am, results, The Debrief and the series, audience + partner formats + contact |
| `AKKI-MEISTER-media-kit.pdf` | The same story on 1 A4 page, to attach to emails |
| `slides.html`, `one-pager.html` | Sources (brand fonts from `reel/assets/`, mark from `stories-india-open/logo.js`, photos straight from `library/`) |
| `data.js` | **The numbers you fill in:** audience figures, the month they're from, a contact email |
| `render.js` | Renders the PNGs and the PDF |

## Filling the numbers
1. Open `data.js` and replace each `null` with the real figure from Instagram Insights (e.g. `"2,140"`, `"78%"`, `"MUM · BLR · DEL"`). Set `asOf` (e.g. `"DEC 2026"`) and `email`.
2. Run `node outreach/media-kit/render.js` from the repo root.
   - It uses Playwright if it's installed.
   - Otherwise it uses `puppeteer-core`: run `npm i puppeteer-core` and set `CHROME_PATH` to your Chrome or Edge.
3. Look at the PNGs before sending. Anything left as `null` shows as a dashed **FILL** box. Never send a brand a kit with FILL boxes.

## What's on it, and where each claim comes from
- **India Open:** top 80 of 33,000+ registered (confirmed by Akki; keep the MFRL leaderboard screenshot as proof).
- **8 sim racing & esports podiums.** Each one was read off the photo or graphic itself:

| Result | Source |
|---|---|
| P1 Jeddah | `library/website/podium-p1-jeddah.jpg` (Race At Will wall) |
| P1 Red Rabbit "E-Sports Winner" | `library/website/podium-p1-redrabbit.jpg` (medal) |
| P2 Red Bull Ring | `library/website/podium-p2-austria.jpg` |
| P2 Brazil | `library/website/podium-p2-brazil.jpg` (@raceatwill tag) |
| P3 Spa | `library/website/podium-p3-spa.jpg` |
| P2 overall, Project Teho | `library/results/toruni.jpg` |
| P2 runner-up, Acer Predator Gaming League (Forza Horizon 5) | `library/results/img-5384.jpg` |
| P3, inaugural VRH ACC AM Championship | `library/results/tourni-2.jpg`, `img-5943.jpg` |

### Check before sending
- **VRH is P3, not P2.** The graphics show P3 (51 pts, tied on points with P3 Surya). `MEDIA.md` used to say P2 / P4; it's now corrected.
- **Confirm that Jeddah, Red Bull Ring and Spa were Race At Will events.** The kit says so because the venue's branding is on the wall in each photo.
- **`podium-p1-supra.jpg` is left out.** It shows a trophy with the Formula Student car, but nothing says what the P1 was for. Tell me and I'll add it.

## Photos used (no identifiable children)
| Slide | Photo | Why |
|---|---|---|
| 01 hero | `sim-rig/img-8350.jpg` | Strongest solo rig shot |
| 01 strip | `karting/img-6017.jpg`, `formula-student/img-1636.jpg`, `sim-coaching/dsc00970.jpg` | Kart, Formula Student, coaching (adults only in frame) |
| 02 | `website/podium-p1-jeddah.jpg` | The P1 podium |
| 03 | `sim-coaching/dsc00987.jpg` | Telemetry on the tablet: the Debrief in one picture. Only a hand of the coached driver is visible. |
| 04 | `sim-rig/img-4609.jpg` | Solo, moody rig shot |
| PDF | `sim-rig/img-8350.jpg` | Same hero as slide 01 |

`sim-rig/img-9142.jpg` (the event cockpit) was tried and dropped: a young competitor is identifiable in the next rig.
