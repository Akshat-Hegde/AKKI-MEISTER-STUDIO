/* Reel engine for hotlap / debrief-reel / sim-to-tarmac.
   1. spec -> timeline (TL)                      2. ffmpeg builds the footage track (bg.mp4 + bg audio)
   3. the overlay page (templates/reel/reel.html) is screenshotted frame by frame WITH ALPHA and composited over bg
   4. audio: clip sound (low) + soft knocks on cuts (templates/lib/audio.py) + optional licensed music, mixed and muxed
   5. review stills (one per segment + any --stills) are written to <out>/stills/ — look at them before posting. */
const path = require("path"), fs = require("fs"), { spawn, spawnSync } = require("child_process");
const { ROOT, fileUrl, browser, ffprobe, run, resolveMedia } = require("./common");
const { parseCsv } = require("./telemetry");
const FPS = 30, W = 1080, H = 1920;

const DEFAULTS = {
  hotlap: { kicker: "HOTLAP", wipe: false },
  "debrief-reel": { kicker: "THE DEBRIEF", wipe: true },
  "sim-to-tarmac": { kicker: "SIM TO TARMAC", wipe: true },
};

function timeline(spec, res) {
  const D = DEFAULTS[spec.template] || {};
  let t = 0;
  const segs = spec.segments.map((s0) => {
    const s = { ...s0 };
    if (s.type === "card" && !s.src) s.color = true;
    const src = s.src ? res(s.src) : null;
    if (src) { s.src = src; s.probe = ffprobe(src); }
    if (s.type === "split") for (const k of ["top", "bottom"]) { s[k] = { ...s[k], src: res(s[k].src) }; s[k].probe = ffprobe(s[k].src); }
    s.clipIn = s.in || 0;
    s.dur = s.dur ?? ((s.out ?? s.probe?.duration ?? 3) - s.clipIn);
    s.t0 = t; s.t1 = t + s.dur; t = s.t1;
    s.fit = s.fit || (s.type === "split" ? "split" : s.type === "card" ? "card" : "cover");
    if (s.fit === "band") {
      const crop = s.crop || [0, 0, s.probe.w, s.probe.h];
      const h = Math.round(W * crop[3] / crop[2] / 2) * 2;
      s.band = { y: s.bandY ?? Math.round((H - h) / 2 - 40), h, crop };
    }
    if (s.wipe === undefined) s.wipe = D.wipe;
    return s;
  });
  const endDur = spec.end ? spec.end.dur ?? 3.2 : 0;
  const TL = { dur: +(t + endDur).toFixed(3), segs, header: spec.header, demo: spec.demo };
  if (spec.title) TL.title = { ...spec.title, t1: Math.min(spec.title.dur ?? 2.8, 3.8), kicker: spec.title.kicker || D.kicker };
  if (spec.end) TL.end = { ...spec.end, t0: t, pattern: spec.end.pattern ? fileUrl(res(spec.end.pattern)) : "" };
  if (spec.lap) {
    // lap time = clip time + offset (read the game's own timer on 2+ frames to get the offset)
    TL.lap = { ...spec.lap, splits: (spec.lap.splits || []).map((s) => ({ ...s, at: s.at ?? s.time })) };
  }
  // notes: place by lap time (needs a lap-synced segment) or by reel time
  TL.notes = (spec.notes || []).map((n) => {
    let t0 = n.t;
    if (t0 == null && n.lap != null && TL.lap) { const sg = segs.find((s) => s.lap && n.lap - TL.lap.offset >= s.clipIn && n.lap - TL.lap.offset < s.clipIn + s.dur); if (sg) t0 = sg.t0 + (n.lap - TL.lap.offset - sg.clipIn); }
    if (t0 == null) throw new Error(`note "${n.text}" is outside the footage`);
    return { ...n, t0, t1: t0 + (n.dur ?? 3.2) };
  });
  if (spec.inputs) {
    const lap = parseCsv(res(spec.inputs.csv));
    TL.inputs = { t: lap.t.map((x) => x - lap.t[0] + (spec.inputs.lapTimeAtStart || 0)), th: lap.th || [], b: lap.br || [], st: lap.st ? lap.st.map((x) => x / (spec.inputs.steerRange || 1)) : null, steerDeg: spec.inputs.steerDeg || 90 };
  }
  for (const s of segs) if (s.pattern) s.pattern = fileUrl(res(s.pattern));
  return TL;
}

/* ---------- footage track ---------- */
const GRADE = "eq=saturation=0.86:contrast=1.05:brightness=-0.025,colorbalance=bs=0.05:bm=0.025:bh=0.01";
function coverChain(s, label, w = W, h = H) {
  const [fx, fy] = (s.focus || "50% 50%").split(" ").map((v) => parseFloat(v) / 100);
  const z = s.zoom || 1, cw = Math.round(w / z / 2) * 2, ch = Math.round(h / z / 2) * 2;
  return `scale=${w}:${h}:force_original_aspect_ratio=increase,crop=${cw}:${ch}:(iw-${cw})*${fx}:(ih-${ch})*${fy},scale=${w}:${h},setsar=1,fps=${FPS},${GRADE}${s.dim ? `,drawbox=c=black@${s.dim}:t=fill` : ""}[${label}]`;
}
function buildFootage(TL, work) {
  const inputs = [], fc = [], vl = [], al = [];
  const addIn = (args) => { inputs.push(...args); return inputs.filter((a) => a === "-i").length - 1; };
  TL.segs.forEach((s, i) => {
    const d = s.dur.toFixed(3);
    if (s.type === "split") {
      const a = addIn(["-ss", s.top.in || 0, "-t", d, "-i", s.top.src]), b = addIn(["-ss", s.bottom.in || 0, "-t", d, "-i", s.bottom.src]);
      fc.push(`[${a}:v]${coverChain(s.top, `t${i}`, W, H / 2)}`, `[${b}:v]${coverChain(s.bottom, `b${i}`, W, H / 2)}`, `[t${i}][b${i}]vstack,trim=duration=${d},setpts=PTS-STARTPTS[v${i}]`);
      const src = s.audioFrom === "top" ? [a, s.top] : [b, s.bottom];
      al.push(src[1].probe.audio && (s.audio ?? .3) > 0 ? `[${src[0]}:a]aresample=48000,aformat=channel_layouts=stereo,volume=${s.audio ?? .3},apad,atrim=0:${d},asetpts=PTS-STARTPTS[a${i}]` : null);
    } else if (s.src) {
      const k = addIn(["-ss", s.clipIn, "-t", d, "-i", s.src]);
      if (s.fit === "band") {
        const [cx, cy, cw, ch] = s.band.crop;
        fc.push(`[${k}:v]split[s${i}a][s${i}b]`, `[s${i}a]${coverChain({ focus: "50% 50%" }, `bg${i}`)}`, `[bg${i}]boxblur=40:2,drawbox=c=black@0.55:t=fill[bgb${i}]`,
          `[s${i}b]crop=${cw}:${ch}:${cx}:${cy},scale=${W}:${s.band.h},setsar=1,fps=${FPS},${GRADE}[fg${i}]`, `[bgb${i}][fg${i}]overlay=0:${s.band.y},trim=duration=${d},setpts=PTS-STARTPTS[v${i}]`);
      } else fc.push(`[${k}:v]${coverChain(s, `c${i}`)}`, `[c${i}]trim=duration=${d},setpts=PTS-STARTPTS[v${i}]`);
      al.push(s.probe.audio && (s.audio ?? .3) > 0 ? `[${k}:a]aresample=48000,aformat=channel_layouts=stereo,volume=${s.audio ?? .3},apad,atrim=0:${d},asetpts=PTS-STARTPTS[a${i}]` : null);
    } else {
      const k = addIn(["-f", "lavfi", "-t", d, "-i", `color=c=0x07080C:s=${W}x${H}:r=${FPS}`]);
      fc.push(`[${k}:v]setsar=1[v${i}]`); al.push(null);
    }
    vl.push(`[v${i}]`);
  });
  // end card: midnight
  if (TL.end) { const k = addIn(["-f", "lavfi", "-t", (TL.dur - TL.end.t0).toFixed(3), "-i", `color=c=0x07080C:s=${W}x${H}:r=${FPS}`]); fc.push(`[${k}:v]setsar=1[vend]`); vl.push("[vend]"); al.push(null); }
  // silent fillers for segments without sound
  const pieces = al.map((a, i) => {
    if (a) { fc.push(a); return `[a${i}]`; }
    const d = i < TL.segs.length ? TL.segs[i].dur : TL.dur - TL.end.t0;
    const k = addIn(["-f", "lavfi", "-t", d.toFixed(3), "-i", "anullsrc=r=48000:cl=stereo"]); fc.push(`[${k}:a]atrim=0:${d.toFixed(3)},asetpts=PTS-STARTPTS[z${i}]`); return `[z${i}]`;
  });
  fc.push(`${vl.map((v, i) => v + pieces[i]).join("")}concat=n=${vl.length}:v=1:a=1[vout][aout]`);
  const key = require("crypto").createHash("md5").update(JSON.stringify([inputs, fc, TL.dur])).digest("hex").slice(0, 10);
  const bg = path.join(work, `bg-${key}.mp4`);
  if (fs.existsSync(bg.replace(/\.mp4$/, ".mov"))) { console.log("  footage unchanged, reusing cache"); return bg.replace(/\.mp4$/, ".mov"); }
  for (const f of fs.readdirSync(work)) if (/^bg-.*\.mov$/.test(f)) fs.rmSync(path.join(work, f));
  run("ffmpeg", ["-y", ...inputs.map(String), "-filter_complex", fc.join(";"), "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-t", TL.dur.toFixed(3), bg.replace(/\.mp4$/, ".mov")]);
  return bg.replace(/\.mp4$/, ".mov");
}

async function renderReel(ctx) {
  const { raw, res, outDir } = ctx;
  const spec = resolveMedia(raw, res, false);
  const TL = timeline(spec, res);
  const work = path.join(outDir, ".work"); fs.mkdirSync(work, { recursive: true });
  const name = raw.name || raw.template;
  console.log(`timeline ${TL.dur.toFixed(2)} s, ${TL.segs.length} segments → building footage…`);
  const bg = buildFootage(TL, work);
  const { b, p } = await browser({ width: W, height: H });
  await p.goto(fileUrl(path.join(ROOT, "templates/reel/reel.html")), { waitUntil: "load" });
  const pageTL = JSON.parse(JSON.stringify(TL, (k, v) => (k === "probe" || k === "ly" ? undefined : v)));
  await p.evaluate((tl) => window.setup(tl), pageTL);
  const events = await p.evaluate(() => window.EVENTS);
  const files = [];
  // review stills: middle of every segment, the title and the end card (+ --stills)
  const stillT = [...new Set([1.4, ...TL.segs.map((s) => +(s.t0 + s.dur * .55).toFixed(2)), ...(TL.end ? [TL.dur - .6] : []), ...(TL.notes || []).map((n) => +(n.t0 + 1).toFixed(2)), ...(ctx.stills || [])])].sort((a, c) => a - c);
  const sd = path.join(outDir, "stills"); fs.mkdirSync(sd, { recursive: true });
  for (const st of stillT) {
    await p.evaluate((t) => window.render(t), st);
    const ov = path.join(work, "ov.png"); await p.screenshot({ path: ov, omitBackground: true });
    const f = path.join(sd, `t_${st.toFixed(2)}.png`);
    run("ffmpeg", ["-y", "-ss", st.toFixed(3), "-i", bg, "-i", ov, "-filter_complex", "[0:v][1:v]overlay", "-frames:v", "1", f]);
    files.push(f);
  }
  // one-row contact sheet of the review stills (small enough to commit / attach to a PR)
  const sheet = path.join(outDir, `${name}-stills.jpg`);
  run("ffmpeg", ["-y", ...files.flatMap((f) => ["-i", f]), "-filter_complex", files.map((_, i) => `[${i}:v]scale=360:-2[s${i}]`).join(";") + ";" + files.map((_, i) => `[s${i}]`).join("") + `hstack=inputs=${files.length}`, "-q:v", "4", sheet]);
  files.unshift(sheet);
  if (ctx.noVideo) { await b.close(); return { files, warnings: [] }; }
  // frames -> composite over footage
  const vid = path.join(work, "video.mp4");
  const N = Math.round(TL.dur * FPS);
  const ff = spawn("ffmpeg", ["-y", "-i", bg, "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-", "-filter_complex", "[0:v][1:v]overlay=format=auto,format=yuv420p[v]", "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", String(FPS), "-frames:v", String(N), vid], { stdio: ["pipe", "ignore", "pipe"] });
  let err = ""; ff.stderr.on("data", (d) => (err = (err + d).slice(-2000)));
  const t0 = Date.now();
  for (let f = 0; f < N; f++) {
    await p.evaluate((t) => window.render(t), f / FPS);
    const buf = await p.screenshot({ type: "png", omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (f % 150 === 0) process.stdout.write(`  frame ${f}/${N} (${((Date.now() - t0) / 1000).toFixed(0)} s)\n`);
  }
  ff.stdin.end(); const code = await new Promise((r) => ff.on("close", r));
  await b.close();
  if (code) throw new Error("ffmpeg overlay failed: " + err);
  // audio
  const evf = path.join(work, "events.json"); fs.writeFileSync(evf, JSON.stringify(events));
  const knocks = path.join(work, "knocks.wav");
  run(process.env.PYTHON || "python3", [path.join(__dirname, "audio.py"), evf, String(TL.dur), knocks]);
  const music = spec.music && spec.music.src && fs.existsSync(spec.music.src) ? spec.music : null;
  if (spec.music && !music) console.warn(`⚠ music file not found (${spec.music.src}); rendering without music`);
  const ins = ["-i", vid, "-i", bg, "-i", knocks]; let mix = `[1:a]volume=1[c];[2:a]volume=1[k]`, n = 2, lab = "[c][k]";
  if (music) { ins.push("-i", music.src); const g = music.gain ?? .16; mix += `;[3:a]atrim=${music.in || 0}:${(music.in || 0) + TL.dur},asetpts=PTS-STARTPTS,volume=${g},afade=t=in:d=0.6,afade=t=out:st=${(TL.dur - 1.6).toFixed(2)}:d=1.6[m]`; lab += "[m]"; n++; }
  mix += `;${lab}amix=inputs=${n}:normalize=0,alimiter=limit=0.9[a]`;
  const out = path.join(outDir, `${name}.mp4`);
  run("ffmpeg", ["-y", ...ins, "-filter_complex", mix, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-t", TL.dur.toFixed(3), "-movflags", "+faststart", out]);
  files.unshift(out);
  for (const f of ["video.mp4", "ov.png", "knocks.wav", "events.json"]) fs.rmSync(path.join(work, f), { force: true }); // bg-*.mov stays as a cache (gitignored)
  return { files, warnings: music || !spec.music ? (spec.music ? [] : ["no music in the spec: only clip sound + knocks. Add \"music\": {\"src\": \"reel/music/drums.wav\", \"gain\": 0.16} for a licensed track."]) : [] };
}
module.exports = { renderReel, timeline };
