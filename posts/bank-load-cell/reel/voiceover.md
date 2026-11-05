# Voiceover: Load cell: brake by pressure, not travel (30.0 s)

Record in one take, calm and conversational. Each line must fit its window; the on-screen captions already carry these words, so the reel also works with sound off.
Save as `voiceover.wav` in this folder, then render the MP4 once:

```bash
node templates/make.js posts/bank-load-cell/reel/spec.json
```

If a line runs long, raise that scene's `dur` in `spec.json` (captions retime automatically). Music slot: `reel/music/drums.wav` on your PC.

| Time | On screen | Say |
|---|---|---|
| 0.0–2.6 | BRAKE BY PRESSURE. | "Brake By Pressure." |
| 2.6–5.8 | FORCE VS TRAVEL. | "A load cell reads how hard you press. A potentiometer reads how far the pedal moves." |
| 5.8–9.2 | POSITION OR FORCE? | "With travel, your foot learns a position. With pressure, it learns a force." |
| 9.2–12.6 | A FORCE, NOT A POSITION. | "A force is easier to repeat at the limit, like the brake in a real race car." |
| 12.6–15.8 | SAME PUSH. SAME BRAKING. | "Same pressure, same braking force, wherever the pedal sits." |
| 15.8–19.2 | NO FLEX. | "It only works if the rig doesn't flex. Mount the pedals solid and set a force you can repeat." |
| 19.2–22.4 | CONSISTENCY FIRST. | "The first win isn't raw speed. It's being the same every lap." |
| 22.4–25.6 | BRAKE BY FEEL, NOT DISTANCE. | "Brake by feel, not by distance." |
| 25.6–30.0 | @akki_meister · follow for more | "Save this for your next rig upgrade. Copy. See you on track." |

Sources for every claim: `../caption.md`. Diagrams and charts are labelled ILLUSTRATIVE.
