# Voiceover: Trail braking: release it, don't drop it (30.2 s)

Record in one take, calm and conversational. Each line must fit its window; the on-screen captions already carry these words, so the reel also works with sound off.
Save as `voiceover.wav` in this folder, then render the MP4 once:

```bash
node templates/make.js posts/bank-trail-braking/reel/spec.json
```

If a line runs long, raise that scene's `dur` in `spec.json` (captions retime automatically). Music slot: `reel/music/drums.wav` on your PC.

| Time | On screen | Say |
|---|---|---|
| 0.0–2.6 | DON'T DROP THE BRAKE. | "Don'T Drop The Brake." |
| 2.6–5.8 | BRAKE HARD, THEN SNAP OFF. | "The common mistake: brake hard, then snap off the pedal as you turn in." |
| 5.8–9.2 | BRAKING LOADS THE FRONT. | "Braking shifts weight forward. More load on the front tyres means more grip to turn in." |
| 9.2–12.4 | THE FRONT GOES LIGHT. | "Drop the brake and the weight jumps back. Less front grip, more understeer." |
| 12.4–16.0 | RELEASE IT GRADUALLY. | "Keep a little pressure as you turn in, then bleed it off as the steering goes on." |
| 16.0–19.4 | ONE UP, ONE DOWN. | "Steering lock goes up, brake pressure comes down. One smooth hand-off." |
| 19.4–22.6 | FAST CORNER? RELEASE EARLIER. | "In fast corners you'll often release earlier to keep the rear settled." |
| 22.6–25.8 | EASE OFF AS YOU TURN IN. | "Ease off as you turn in. Don't drop it." |
| 25.8–30.2 | @akki_meister · follow for more | "Save this and try it in your next session. Copy. See you on track." |

Sources for every claim: `../caption.md`. Diagrams and charts are labelled ILLUSTRATIVE.
