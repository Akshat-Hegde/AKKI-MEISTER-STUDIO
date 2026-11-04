# AKKI MEISTER: cloud session playbook

**The goal:** become a valuable sim racing, motorsport and lifestyle creator. That means getting invited to sim expos, earning F1 paddock access and team invites, landing partnerships and ambassador roles, and teaching real knowledge along the way.

**How to use this file:** run the sessions in order. Each one is a fresh cloud session on the `akki-meister-studio` repo. Paste the prompt, review what comes back, merge the PR, then move to the next. Every session writes its output into the repo, so later sessions build on earlier ones.

**Budget guide (about $100):**

| Sessions | Share | Purpose |
|---|---|---|
| 1–2 | ~25% | Research and strategy (the foundation; do it properly once) |
| 3 | ~15% | Outreach kit |
| 4 | ~25% | Content templates |
| 5+ | ~35% | Batch production |

---

## Session 0: setup (local, before any cloud session)

- Push this folder to the private repo `akki-meister-studio`.
- Upload your media to `media/photos/`, `media/videos/` and `media/telemetry/`.
- Make sure `CLAUDE.md`, `CONTENT-CALENDAR.md` and this file are in the repo.

---

## Session 1: research the creator landscape

```
Read CLAUDE.md (especially "The mission").

My end goal: become a popular and genuinely valuable sim racing / motorsport / lifestyle content creator — starting in India — who gets invited to sim racing expos, gets F1 paddock passes, gets invited by teams, lands brand partnerships and ambassador roles through my content, and above all delivers real value and knowledge to my audience. I want to study the creators who already did this — Jimmy Broadbent, Super GT, Jardier globally, Adi Plays in India — and find everyone else doing this in India, then craft my own path: positioning, ideas, content plan.

Research (use web search, cite every source with a link, never invent numbers — if you can't verify a figure, say so):
1. Global sim racing creators: Jimmy Broadbent, Super GT, Jardier, and 6–10 others in the same space (find them). For each: platforms, approx audience (with source + date), niche/angle, signature formats, posting cadence, how they grew (key videos/moments), how they make money (sponsors, ambassadors, merch, team deals), and any F1/team/expo partnerships.
2. Indian sim racing & motorsport creators: Adi Plays and everyone else doing this in India (search thoroughly — YouTube, Instagram, Indian sim leagues, F1 Sim Racing India Open participants who post content). Same fields as above.
3. The Indian ecosystem: sim racing events/expos (e.g. F1 Sim Racing India Open, gaming expos like IGDC/Comic Con gaming zones/esports events), Indian sim leagues and Discords, Indian motorsport series (karting, JK Tyre, Formula 4 India / Indian Racing League), hardware brands active in India (Fanatec, Moza, Logitech, Playseat, Simagic distributors).
4. Gaps: what nobody in India is doing well yet.

Output: research/creator-landscape.md (tables + short analysis) and research/india-ecosystem.md. Flag anything unverified.
```

---

## Session 2: positioning, strategy and the path

```
Read CLAUDE.md (especially "The mission"), research/creator-landscape.md, research/india-ecosystem.md, MEDIA.md.

My end goal (repeat it back in one paragraph before you start, so I know you've got it): become a popular, valuable sim racing / motorsport / lifestyle creator who gets invited to sim expos, earns F1 paddock access and team invitations, lands partnerships and ambassador roles through content, and delivers real knowledge — built the way Jimmy Broadbent, Super GT, Jardier and Adi Plays built theirs, but in my own lane.

My real assets: competed at F1 Sim Racing India Open 2026 (top 80 of 33k+ registered), sim racing podiums, karting, Formula Student (engineering + driving), I coach sim racing (incl. kids), I understand data/telemetry, I have a finished brand (AKKI MEISTER).

Build my strategy:
1. Positioning: one-line "why follow me" that no one else in India owns (e.g. the sim-to-real engineer-driver who teaches). Give 3 options, recommend one.
2. Content pillars (4–5) with % mix, and the 3–4 repeatable signature series (named, with format + length), e.g. a weekly "Lap Breakdown".
3. Platform plan: Instagram, YouTube Shorts, YouTube long-form (when/how to start), LinkedIn (for brands/teams), Discord/community. What to post where, cadence I can realistically sustain while studying/working.
4. The path to my goals as milestones with rough timelines: e.g. 0–3 months, 3–6, 6–12, 12–24 — audience targets, credibility markers (results, collabs, event appearances), and what unlocks each goal: expo invites → brand partnerships → ambassador roles → team/paddock access. Be realistic; say what depends on racing results vs content vs networking.
5. Metrics to track monthly and what "working" looks like.
6. Risks and what to avoid (burnout, inconsistency, copying others, unverified claims).

7. Content ideas: 30 specific post/reel ideas mapped to pillars and series, each noting which files from MEDIA.md it would use (or what I need to film).
8. Update CONTENT-CALENDAR.md so it follows this strategy.

Output: strategy/STRATEGY.md and strategy/ROADMAP.md (checklist format I can tick off), plus the updated calendar.
```

---

## Session 3: outreach kit (partnerships, expos, teams)

```
Read CLAUDE.md, strategy/STRATEGY.md, research/*.md.

1. Media kit: a 1-page (or 4-slide) sponsor/media kit in the AKKI MEISTER brand — who I am, results, content pillars, audience (leave clearly marked placeholders for numbers I'll fill), formats I offer partners, contact. Render as PDF + PNGs into outreach/media-kit/.
2. Target list: outreach/targets.md — brands, Indian distributors, event organisers, sim leagues, motorsport teams/series, other creators to collab with. For each: why it fits, the right first ask (small), how to reach (public channel only), priority. Verify each exists and is active; cite links.
3. Templates: outreach/templates.md — cold DM, email to a brand, email to an event organiser asking to cover/attend/host a session, collab pitch to a creator, follow-up. Short, specific, value-first, no begging.
4. A 4-week outreach cadence I can run alongside content.
```

---

## Session 4: the content engine (reusable templates)

```
Read CLAUDE.md and strategy/STRATEGY.md. Build reusable templates so future posts take minutes:
1. infographics/_kit/ — carousel slide system (1080×1350): hook slide, content slides (text+diagram, chart, table, before/after, track-corner sketch), closing slide. One command renders a carousel from a simple JSON/markdown spec.
2. A hotlap-overlay reel template: input a screen recording from media/videos/, output a 1080×1920 reel with title card, lap timer, sector notes, ///AM mark, end card.
3. A telemetry comparison template: input two lap CSVs from media/telemetry/, output speed-trace + delta charts as slides and an animated clip.
4. A quote/announcement story template (like stories-india-open/).
Document each in CLAUDE.md under "Templates" with the exact command. Test each with real media and show me the renders.
```

---

## Session 5 onward: batch production

```
Read CLAUDE.md, MEDIA.md, CONTENT-CALENDAR.md, strategy/STRATEGY.md. For every post, choose the photos/clips from library/ whose subject actually matches the post (see "Choosing media" in CLAUDE.md) — look at the frames before using a clip, and tell me which files you picked and why. Using the templates, produce Week <N> from the calendar: every post as finished files in posts/<date>-<slug>/ with caption.md. Fact-check everything marked 🔎 with cited sources. Then extend CONTENT-CALENDAR.md by 4 more weeks aligned with the strategy's signature series.
```

Run one session per 1–2 weeks of content. Give it the media first.

---

## What only you can do (no session replaces this)

- **Race and improve.** Results are credibility. Keep entering leagues and qualifiers.
- **Film consistently.** Record every session with inputs visible; raw footage is the fuel.
- **Show up in the community.** Reply to every comment and DM, join Indian sim Discords and leagues, comment on other creators' posts.
- **Be at events in person.** Expos, karting events, Formula Student competitions. Introduce yourself to organisers and brand reps, with the media kit on your phone.
- **Stay consistent for 6+ months.** Most creators quit before the algorithm and the brands notice them.
