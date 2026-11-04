# AKKI MEISTER: 4-week content calendar

**Runs 9 Nov – 6 Dec 2026.** Follows `strategy/STRATEGY.md`. Outreach runs alongside it: `outreach/PLAN.md` says who to contact each week, once the relevant posts are live.

**Positioning:** *India's own sim racing coach. Real laps, real data, real racecraft. Every post makes you faster.*

> **India Open figure:** top 80 out of 33,000+ registered participants. Use exactly that wording, and keep the leaderboard screenshot as proof.
>
> ⚠️ **Before week 1:** get parental consent before any coached child's face is used.

## The weekly rhythm

| Day | What | Series |
|---|---|---|
| **Mon** | Carousel: one technique or setting, explained | 📐 **APEX NOTES** |
| **Tue** | LinkedIn post (carousel as a PDF, or a lesson / recap) | — |
| **Wed** | Reel, rotating sim to real / Indian scene / life at speed | 🏁 **SIM TO TARMAC** (monthly) or standalone |
| **Sat** | Reel: a follower's (or coached driver's) lap, reviewed | 🎙️ **THE DEBRIEF**, *the show* |
| **Sun** | Story set on one piece of the rig or one setting | **SETUP SUNDAY** |

**Every week:**
- Every reel is mirrored to **YouTube Shorts** the same or next day: re-export without the IG watermark and give it a search-style title.
- Stories on 4–5 days: polls, the lap-submission call, behind the scenes.
- **Minimum viable week** (exams or travel): the Debrief, one story set and one Short. Nothing else.
- Launch week has 4 feed posts; from week 2 it's 3.

**Best times to post (India):** 7–9 pm on weekdays, and late morning on weekends. Check Instagram Insights after week 2 and move the slots to whenever your followers are most active.

**Status key:** ✅ assets exist · 📸 needs photos from Akki · 🎥 needs footage · 📊 needs telemetry export · 🔎 facts to verify before posting · ⚠️ decision or consent needed

**Every Debrief reel ends with:** "Send me your lap → link in bio / broadcast channel." The show only works if submitting is easy.

---

## Hashtag sets (rotate them, 8–12 tags per post)

- **Core (always):** `#simracing #simracer #f126 #f1sim #motorsport #simracingindia #esports #akkimeister`
- **Racecraft:** `#racecraft #trailbraking #racingline #drivercoaching #simracingtips #learntodrive`
- **Data:** `#telemetry #motorsportengineering #f1telemetry #datadriven #laptime #thedebrief`
- **Rig and setup:** `#simrig #simracingsetup #cockpit #setupsunday` (add brand tags only when they're actually in shot, and never imply a partnership that doesn't exist)
- **India and lifestyle:** `#indianmotorsport #karting #formulastudent #motorsportlife #racingdriver #f1simracingindiaopen`

---

## Week 1 · 9–15 Nov: the reintroduction (who I am, what I teach, send me your lap)

India Open finals week (NSCI Dome, Mumbai), so the scene is paying attention.

### Mon 9 · REEL · the AKKI MEISTER teaser ✅ · *P5 · launch*
- **Hook (text on screen):** "Sim. Track. Paddock."
- **Asset:** `AKKI-MEISTER-COMPLETE/AKKI-MEISTER-reel.mp4`. It's gitignored, so it's on Akki's PC, not in the repo. Re-render it with `reel/tools/render.js` if needed.
- **Caption:**
  > Sim. Track. Paddock. 🏁
  > Real laps, real data, real racecraft. Every post here should make you faster. Starting now.
  > @akki_meister
- **Alternative caption:**
  > I race, I coach, and I read the data. Now I'm putting all of it on the feed. 🏎️ @akki_meister
- **Tags:** Core + India and lifestyle

### Wed 11 · CAROUSEL · APEX NOTES #1: "The ERS mistake that killed my race pace" 🔎 · *P2*
- **Hook slide:** "I UNDERESTIMATED ONE THING IN F1 26. IT COST ME MY RACE PACE."
- **Hero:** `library/telemetry/img-9320.jpg` (telemetry + track map)
- **Slides:**
  1. What changed with the 2026 power units: a much bigger electric share, so deployment matters more. 🔎 Verify the exact split and the F1 26 ERS modes.
  2. How I drove it at the India Open: deploying too early on the straights.
  3. What happened: the battery ran dry, I was defenceless late in the lap, and my pace fell away.
  4. What I'm changing: harvest and deploy zones planned per track (a diagram).
  5. Takeaway, then a CTA.
- **Caption:**
  > The India Open taught me the hard way: in F1 26, battery management *is* race pace. 🔋 Here's what went wrong and what I'm changing. Save this before your next race.
- **Tags:** Core + Racecraft + Data

### Fri 13 · REEL · "33,000+ registered. Here's what top 80 took." 🎥 · *P4*
- **Structure:**
  1. The email-zoom clip: "Congratulations on qualifying…".
  2. Venue photos.
  3. Three fast lessons as kinetic type.
  4. End card: "NEXT TIME."
- **Assets:**
  - Render `email-motion/email-zoom.html` to mp4 first.
  - `stories-india-open/assets/venue.jpg`, `room.jpg`, `cockpit.jpg`.
  - Any clips Akki has from Mumbai.
- **Caption:**
  > 33,000+ registered. I finished top 80. Not where I wanted to finish, but I learned more in those days than in a year of hotlapping. Coming back stronger. 🏁 @akki_meister
- Add a congratulations line for the 2026 champions once the finals results are out.
- **Tags:** Core + India and lifestyle

### Sat 14 · REEL · THE DEBRIEF, Ep 0: "I debriefed my own lap" 📊 🎥 · *P2 · the show begins*
- **Hook:** "Same car. Same track. 0.Xs slower. Here's exactly where." Use Akki's real gap; never invent it.
- **Assets:**
  - 📊 Akki's lap + a faster reference lap export (speed trace, brake/throttle overlay, delta).
  - Opening b-roll: `library/sim-rig/img-8214.mp4` (wheel close-up; check frames).
  - Template: the Debrief template from Playbook Session 4.
- **Structure:**
  1. The gap.
  2. Two corners where it's lost.
  3. The one drill.
  4. "Your lap next. Send it in."
- **Caption:**
  > Episode 0 of The Debrief: I put my own lap under the microscope first. Most of the gap was in two corners. 📊
  > Want yours reviewed? Send your lap (link in bio).
- **Tags:** Core + Data

### Tue 10 · LINKEDIN
"What competing at India's first official F1 sim championship taught me about preparation". Uses `stories-india-open/assets/cockpit.jpg`.

### Stories this week
- **Mon:** poll, "What should I break down next? 🛞 trail braking / 🎯 FOV".
- **Wed:** congratulations story for the India Open finalists (tag the ones who post).
- **Thu:** question box, "Ask me anything about sim racing".
- **Sat:** a lap-submission explainer story (what to send, how). Pin it to highlights.
- **Sun:** Setup Sunday #1, "My wheel + pedals" 📸 (close-ups; `library/sim-rig/img-0941.jpg` for the overview).

---

## Week 2 · 16–22 Nov: racecraft (teach one skill properly)

### Mon 16 · CAROUSEL · APEX NOTES #2: "Trail braking, explained" 🔎 · *P1*
- **Hook slide:** "YOU'RE BRAKING IN A STRAIGHT LINE. THAT'S WHY YOU'RE SLOW."
- **Hero:** `library/sim-coaching/dsc00978.jpg` (coaching a young driver in the rig). ⚠️ Needs parental consent; if not cleared, use `library/sim-rig/img-9148.jpg`.
- **Slides:**
  1. Brake pressure vs distance: straight-line braking vs trail braking (a chart).
  2. Why it works: weight transfer loads the front tyres.
  3. How to practise it: one corner at a time.
  4. The common mistake: releasing too fast and losing the front.
  5. The drill: 10 laps, one corner.
- **Caption:**
  > Trail braking is the biggest single jump in pace for most sim racers I coach. 🛞 The idea in 6 slides, plus the drill I give my drivers. Save it, try it tonight.
- **Tags:** Core + Racecraft

### Wed 18 · REEL · "Watch my feet, not the screen." 🎥 · *P1*
- **Asset:** an onboard hotlap screen recording with an input overlay (throttle, brake, steering) and, ideally, a pedal-cam. Pick a track Akki is quick at.
- **Overlay:** lap timer, a short note per sector ("brake here", "patience on throttle"), and a `///AM` corner mark.
- **Caption:**
  > One lap of <track>, every input shown. Notice how little I'm on full throttle out of slow corners. Patience = exit speed. ⏱️
- **Tags:** Core + Racecraft

### Sat 21 · REEL · THE DEBRIEF, Ep 1: a coached driver's lap 📊 ⚠️ · *P2*
- **Asset:** the lap of someone Akki coaches, with their permission (and a parent's, if they're a minor), next to Akki's.
- **Opening:** `library/sim-coaching/race-engineer.mp4` (7 s, engineer/driver dynamic; check frames).
- **Hook:** "<Name> was 1.2s off. 0.8 of it was one habit." Use the real numbers.
- **Caption:**
  > Episode 1 of The Debrief. One habit, one drill, and we'll see next week if it stuck. 🎧 Send yours: link in bio.
- **Tags:** Core + Data + Racecraft

### Tue 17 · LINKEDIN
APEX NOTES #2 (trail braking) as a PDF document post, with an engineering framing (load transfer).

### Stories this week
- A poll: "Do you trail brake? Yes / What's that 😅".
- Behind the scenes of making the trail-braking post.
- **Sun:** Setup Sunday #2, "Force-feedback settings: my numbers" 🔎 (labelled "my setup").

---

## Week 3 · 23–29 Nov: sim to real (where the sim meets the track)

### Mon 23 · CAROUSEL · APEX NOTES #3: "Your brake bias is probably wrong for half the track" 🔎 · *P1*
- **Hero:** `library/sim-rig/img-9148.jpg` (cockpit view: wheel + curved screen). If week 2 used it as a fallback, use `library/sim-rig/img-4856.jpg` instead.
- **Slides:**
  1. What bias is, with a front/rear split diagram.
  2. Too far forward means understeer and lock-ups.
  3. Too far rear means the car snaps.
  4. Changing it per corner type.
  5. Brake migration, if it applies in F1 26. 🔎 Verify before posting.
- **Caption:**
  > Brake bias isn't set-and-forget. 🔧 Here's how I think about it, corner by corner.
- **Tags:** Core + Racecraft + Data

### Wed 25 · REEL · SIM TO TARMAC #1: "Does sim racing actually make you faster in a kart?" 🎥 · *P3*
- **Assets:**
  - `library/karting/img-6017.jpg` (Rotax kart in action, strong).
  - `library/karting/img-2539.mp4` and `library/karting/img-2541.mp4` (vertical karting clips; check frames, cut the best 2–6 s).
  - `library/sim-rig/img-4857.mp4` (triple-screen rig).
- **Structure:**
  1. What carried over: braking references, vision, consistency.
  2. What didn't: g-forces, grip feel, fear.
  3. One verdict line.
- **Caption:**
  > Sim to tarmac. 🏎️ What the rig taught me that worked in a kart, and the one thing no sim can teach you.
- **Tags:** Core + India and lifestyle + Racecraft

### Sat 28 · REEL · THE DEBRIEF, Ep 2 📊 · *P2*
- **Lap:** the first outside submission. If there isn't one yet, use a second coached driver, and **re-run the Ep 1 driver** for the before/after ("last week: 1.2s off; this week: …").
- **Caption:**
  > Episode 2. Last week's driver went back out, and here's what changed. 📊 Your lap could be next.
- **Tags:** Core + Data

### Tue 24 · LINKEDIN
"What Formula Student taught me about setup that no sim menu explains". Uses `library/formula-student/img-1636.jpg` (Akki on car #10) and `library/website/fs-simulate.jpg`.

### Stories this week
- **Tue:** a telemetry teaser, "Guess where they're losing time?" (quiz sticker, before the Debrief).
- Formula Student throwbacks: `library/formula-student/img-7524.mp4` (workshop build).
- **Sun:** Setup Sunday #3, "How I set my FOV" 🔎 (this sets up next Monday's carousel).

---

## Week 4 · 30 Nov – 6 Dec: community (bring people in)

### Mon 30 · CAROUSEL · APEX NOTES #4: "Wrong FOV = wrong braking points" 🔎 📸 · *P1*
- **Hero:** `library/sim-rig/img-5112.jpg` (triple-screen rig).
- **Slides:**
  1. What field of view is.
  2. Why a wide FOV feels faster but kills distance judgement.
  3. How to calculate it: screen size and eye distance. 🔎 Verify the formula.
  4. My numbers (labelled "my setup").
  5. Before/after screenshots 📸.
- **Caption:**
  > If your braking points feel random, check your FOV first. 🎯 Here's how to set it properly in 2 minutes.
- **Tags:** Core + Rig and setup

### Wed 2 Dec · REEL · "I coach kids. Here's what they teach me." ⚠️ ✅ · *P4*
- **Assets:**
  - `library/sim-coaching/dsc00970.jpg` (Akki briefing a group)
  - `library/sim-coaching/dsc00945.jpg` (group briefing in the tent)
  - `library/sim-coaching/e.jpg` (coaching with a tablet, vertical)
  - `library/sim-coaching/dsc00987.jpg` (telemetry on the tablet)
  - Plus any coaching clips.
- ⚠️ Use only consent-cleared faces.
- **Hook:** "Teaching someone to trail brake in 20 minutes."
- **Caption:**
  > Coaching is my favourite part of sim racing. Watching someone find a second in one session never gets old. 🎧 Want a session? DM me.
- **Tags:** Core + Racecraft + India and lifestyle

### Sat 5 · REEL · THE DEBRIEF, Ep 3 📊 · *P2*
- **Lap:** an outside submission.
- **Ending:** tease Hotlap Challenge #1 ("next month, you race *my* lap").
- **Caption:**
  > Episode 3 of The Debrief. 📊 Next month it's your turn to chase my lap: Hotlap Challenge #1 drops soon.
- **Tags:** Core + Data

### Tue 1 Dec · LINKEDIN
"What coaching drivers taught me about how people learn". Uses `library/website/coach-brief.jpg`.

### Optional bonus (only if the week is ahead of schedule) · CAROUSEL · "5 things I'd tell myself before my first sim competition" · *P4*
- **Assets:** `library/sim-rig/img-9142.jpg` (pro cockpit at an event), `library/website/podium-p1-jeddah.jpg`.
- **Hook slide:** "I LEARNED THESE THE HARD WAY SO YOU DON'T HAVE TO."
- **Caption:**
  > Competing at the F1 Sim Racing India Open taught me more than a year of hotlapping. Here are 5 things I wish I'd known. Which one hits hardest? 👇

### Stories this week
- Answers to week 1's question box.
- A "what should month 2 cover?" poll.
- A Hotlap Challenge teaser: "which track?" poll.
- **Sun:** Setup Sunday #4, "Seat position and ergonomics" 📸.

---

## Coming next (weeks 5–8, to plan in Session 5)

- **Hotlap Challenge #1** launch (`library/sim-rig/img-8350.jpg`, `library/portraits/img-0505.jpg`).
- Setup Sunday monthly round-up carousel: "My rig, piece by piece".
- APEX NOTES: telemetry in 5 traces, tyre temps, load-cell pedals.
- SIM TO TARMAC #2: Formula Student.
- Formula Bharat 2027 preview (19–24 Jan).
- Pitch the Adi Plays collab.

The full list of 30 ideas is in `strategy/STRATEGY.md` §8.

---

## What Akki needs to supply (drop it in `media/`)

| For | What |
|---|---|
| Before week 1 | Leaderboard screenshot (top 80 of 33,000+, as proof); consent list for coached kids; any Mumbai clips or photos |
| Week 1 | 📊 Your lap + a faster reference lap export (Debrief Ep 0); 📸 wheel and pedal close-ups |
| Week 2 | 🎥 Onboard hotlap with input overlay (+ pedal-cam if possible); 📊 a coached driver's lap (with permission) |
| Week 3 | 🎥 Kart footage with timing if you have it; 📊 the Ep 1 driver's re-run lap |
| Week 4 | 📸 FOV before/after screenshots; coaching clips; seat and ergonomics photos; 📊 an outside submission |

🔎 Everything marked "verify" (2026 regs, F1 26 game mechanics, FOV formula, brake migration, FFB values) must be fact-checked against current sources before it's published.
