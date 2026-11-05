# Voiceover: FOV: measure it, don't guess it (30.0 s)

Record in one take, calm and conversational. Each line must fit its window; the on-screen captions already carry these words, so the reel also works with sound off.
Save as `voiceover.wav` in this folder, then render the MP4 once:

```bash
node templates/make.js posts/bank-fov/reel/spec.json
```

If a line runs long, raise that scene's `dur` in `spec.json` (captions retime automatically). Music slot: `reel/music/drums.wav` on your PC.

| Time | On screen | Say |
|---|---|---|
| 0.0–2.6 | YOUR FOV IS GUESSING. | "Your Fov Is Guessing." |
| 2.6–5.8 | WIDE FEELS FAST. | "A wide field of view feels fast. But it changes how big and how far everything looks." |
| 5.8–9.2 | TWO NUMBERS. | "Measure two numbers: the visible screen width, and the distance from your eyes to the screen." |
| 9.2–12.6 | THE FORMULA. | "Two times arc-tan of width over two times distance. Same units for both." |
| 12.6–16.0 | CHECK YOUR GAME. | "Games label FOV differently: horizontal, vertical or 3D. Check which one yours uses." |
| 16.0–19.2 | REAL SCALE. | "Now the screen works like a window at true scale." |
| 19.2–22.4 | SAME MARKERS. EVERY LAP. | "Speed and distance read the same every lap, so braking points get easier to repeat." |
| 22.4–25.6 | MEASURE IT. DON'T GUESS IT. | "Measure it. Don't guess it." |
| 25.6–30.0 | @akki_meister · follow for more | "Save this before you touch your settings. Copy. See you on track." |

Sources for every claim: `../caption.md`. Diagrams and charts are labelled ILLUSTRATIVE.
