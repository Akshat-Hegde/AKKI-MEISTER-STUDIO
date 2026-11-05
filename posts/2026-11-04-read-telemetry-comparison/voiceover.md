# Voiceover: How to read a telemetry comparison (31.2 s)

Record in one take, calm and conversational, ~150 words per minute. Each line has to fit inside its window;
the on-screen captions already show these exact words, so the reel still works with sound off.
Save as `voiceover.wav` in this folder, then re-run the command (the spec's `voiceover` slot picks it up; no other change needed):

```bash
node templates/make.js posts/2026-11-04-read-telemetry-comparison/spec.json
```

If your take runs long, stretch the matching scene's `dur` in `spec.json`. The captions retime automatically.

| Time | On screen | Say |
|---|---|---|
| 0.0–2.6 | Zoom on the dashboard: 279 vs 35 km/h | "Two-seventy-nine versus thirty-five. Who's faster?" |
| 2.6–5.4 | Live dashboard, me on the right | "This is a live telemetry comparison. Two rigs, one track." |
| 5.4–8.2 | Zoom into the map, both cars circled | "Most people compare the numbers live. Look at the map: they're not in the same place." |
| 8.2–11.2 | Step 1 diagram: two cars move to one spot | "Step one: line both laps up at the same spot on track." |
| 11.2–14.2 | Speed vs distance chart with a cursor | "Plot speed against distance, then read both laps at the same point." |
| 14.2–17.8 | Step 2: where the lines split, 3 markers | "Find where the lines split: braking point, minimum speed, back on the throttle." |
| 17.8–20.6 | Step 3: live onboard panel | "Then check the inputs at that exact spot." |
| 20.6–24.0 | Zoom on gear, throttle, brake | "Throttle, brake and gear tell you why one lap is faster there." |
| 24.0–27.0 | Takeaway card | "Compare by distance, not by time." |
| 27.0–31.2 | Me at the rig (sim-intro clip) | "Save this for your next debrief. Copy. See you on track." |

Notes
- The 279 / 35 km/h and gears 7 / 3 are what the dashboard shows at 37.6 s of `telemetry/img-9855.mp4` (PLAYER and AKKI3346).
- The two charts are labelled ILLUSTRATIVE: they show the method, not data from this session.
- Music slot: `reel/music/drums.wav` (licensed, on your PC). It's ducked to 60 % automatically under the voiceover.
