/* EXPLAINER reel (1080×1920): a creator teaching one idea in 30–40 s.
   Scenes play back to back. Each scene has ONE visual source, plus layered teaching elements:
     clip    a live footage window (src, in, crop [x,y,w,h] of the source, area [x,y,w,h] on screen); the rest of
             the frame is a blurred, darkened copy of the same crop, so nothing is ever empty black
     freeze  a frame grab (src, at, crop) that the page zooms into: keys [{t, rect:[x,y,w,h]}] in crop coords,
             rings [{at, x, y, r, label}] circle the exact number being discussed
     photo   a still photo (src, focus) as a full-bleed backdrop
     (none)  brand backdrop (midnight + glow) for diagrams / big type
   Teaching layers: head {kicker, lines}, diagram {type: "spot" | "trace" | "split"} (illustrative, labelled),
   host {src (rembg cutout PNG), side, h} (Akki next to the content), say (word-by-word caption, works with sound off), chip.
   Audio: soft knock per cut + quiet tick when type lands (audio.py), + voiceover.src and music.src when the files exist.
   The crop of every clip / freeze is applied in ffmpeg BEFORE anything reaches the page, so cropped-away pixels
   (e.g. a browser bar with email addresses) can never appear, however the page zooms. */
const path = require("path"), fs = require("fs"), { spawn } = require("child_process");
const { ROOT, fileUrl, browser, run, resolveMedia } = require("./common");
const FPS = 30, W = 1080, H = 1920;
const GRADE = "eq=saturation=0.88:contrast=1.06:brightness=-0.01,colorbalance=bs=0.05:bm=0.02";
const ev = (n) => Math.round(n / 2) * 2;

function buildFootage(scenes, dur, work) {
  const inputs = [], fc = [], vl = [];
  const addIn = (a) => { inputs.push(...a.map(String)); return inputs.filter((x) => x === "-i").length - 1; };
  scenes.forEach((s, i) => {
    const d = s.dur.toFixed(3);
    if (s.clip) {
      const c = s.clip, [cx, cy, cw, ch] = c.crop, [ax, ay, aw, ah] = c.area || [0, 0, W, H];
      const k = addIn(["-ss", c.in || 0, "-t", d, "-i", c.src]);
      fc.push(`[${k}:v]crop=${cw}:${ch}:${cx}:${cy},fps=${FPS},split[a${i}][b${i}]`,
        `[a${i}]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},setsar=1,boxblur=34:2,eq=brightness=-0.22:saturation=0.7[bg${i}]`,
        `[b${i}]scale=${ev(aw)}:${ev(ah)}:force_original_aspect_ratio=increase,crop=${ev(aw)}:${ev(ah)},setsar=1,${GRADE}[fg${i}]`,
        `[bg${i}][fg${i}]overlay=${ax}:${ay},trim=duration=${d},setpts=PTS-STARTPTS[v${i}]`);
    } else {
      const k = addIn(["-f", "lavfi", "-t", d, "-i", `color=c=0x07080C:s=${W}x${H}:r=${FPS}`]);
      fc.push(`[${k}:v]setsar=1[v${i}]`);
    }
    vl.push(`[v${i}]`);
  });
  fc.push(`${vl.join("")}concat=n=${vl.length}:v=1:a=0[vout]`);
  const key = require("crypto").createHash("md5").update(JSON.stringify([inputs, fc])).digest("hex").slice(0, 10);
  const bg = path.join(work, `xbg-${key}.mp4`);
  if (fs.existsSync(bg)) { console.log("  footage unchanged, reusing cache"); return bg; }
  for (const f of fs.readdirSync(work)) if (/^xbg-.*\.mp4$/.test(f)) fs.rmSync(path.join(work, f));
  run("ffmpeg", ["-y", ...inputs, "-filter_complex", fc.join(";"), "-map", "[vout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p", "-t", dur.toFixed(3), bg]);
  return bg;
}

async function renderExplainer(ctx) {
  const { raw, res, outDir } = ctx;
  // optional audio slots: a missing file just leaves the slot empty (warned at mux time)
  const slot = (o) => { if (!o || !o.src) return null; try { return { ...o, src: res(o.src) }; } catch (e) { return { ...o, src: null, missing: o.src }; } };
  const spec = { ...resolveMedia({ ...raw, voiceover: undefined, music: undefined, caption: undefined }, res, false), voiceover: slot(raw.voiceover), music: slot(raw.music) };
  const work = path.join(outDir, ".work"); fs.mkdirSync(work, { recursive: true });
  const name = raw.name || "explainer";
  const warnings = [];
  let t = 0;
  const scenes = spec.scenes.map((s0, i) => {
    const s = { ...s0, i, t0: t, t1: t + s0.dur }; t = s.t1;
    if (s.freeze) {
      const f = s.freeze, [cx, cy, cw, ch] = f.crop;
      const png = path.join(work, `freeze-${i}-${path.basename(f.src, path.extname(f.src))}-${f.at}-${f.crop.join("_")}.png`);
      if (!fs.existsSync(png)) run("ffmpeg", ["-y", "-ss", String(f.at), "-i", f.src, "-frames:v", "1", "-vf", `crop=${cw}:${ch}:${cx}:${cy}`, png]);
      s.freeze = { ...f, img: fileUrl(png), w: cw, h: ch };
    }
    for (const k of ["photo"]) if (s[k] && s[k].src) s[k] = { ...s[k], src: fileUrl(s[k].src) };
    if (s.host && s.host.src) s.host = { ...s.host, src: fileUrl(s.host.src) };
    if (s.backdrop && s.backdrop.src) s.backdrop = { ...s.backdrop, src: fileUrl(s.backdrop.src) };
    return s;
  });
  const dur = +t.toFixed(3);
  if (dur < 30 || dur > 40) warnings.push(`explainer is ${dur.toFixed(1)} s (target 30–40 s)`);
  scenes.forEach((s) => { if (s.dur > 3.6 && !(s.beats > 1)) warnings.push(`scene ${s.i + 1} holds ${s.dur} s: change the visual every 2–3 s (zoom keys / rings / diagram steps)`); });
  console.log(`explainer ${dur.toFixed(2)} s, ${scenes.length} scenes → building footage…`);
  const bg = buildFootage(scenes, dur, work);
  const { b, p } = await browser({ width: W, height: H });
  await p.goto(fileUrl(path.join(ROOT, "templates/reel/explainer.html")), { waitUntil: "load" });
  await p.evaluate((tl) => window.setup(tl), { dur, scenes, handle: spec.handle || "@akki_meister" });
  await p.evaluate(() => document.fonts.ready);
  const events = await p.evaluate(() => window.EVENTS);
  const files = [];
  const stillT = [...new Set([0.9, ...scenes.flatMap((s) => [+(s.t0 + s.dur * .35).toFixed(2), +(s.t0 + s.dur * .85).toFixed(2)]), ...(ctx.stills || [])])].sort((a, c) => a - c);
  const sd = path.join(outDir, "stills"); fs.mkdirSync(sd, { recursive: true });
  for (const f of fs.readdirSync(sd)) fs.rmSync(path.join(sd, f));
  for (const st of stillT) {
    await p.evaluate((x) => window.render(x), st);
    const ov = path.join(work, "ov.png"); await p.screenshot({ path: ov, omitBackground: true });
    const f = path.join(sd, `t_${st.toFixed(2).padStart(5, "0")}.png`);
    run("ffmpeg", ["-y", "-ss", st.toFixed(3), "-i", bg, "-i", ov, "-filter_complex", "[0:v][1:v]overlay", "-frames:v", "1", f]);
    files.push(f);
  }
  // contact sheet, 6 per row
  const sheet = path.join(outDir, `${name}-stills.jpg`), cols = 6, rows = Math.ceil(files.length / cols);
  run("ffmpeg", ["-y", ...files.flatMap((f) => ["-i", f]), "-filter_complex", files.map((_, i) => `[${i}:v]scale=270:-2[s${i}]`).join(";") + ";" + files.map((_, i) => `[s${i}]`).join("") + `xstack=inputs=${files.length}:layout=${files.map((_, i) => `${(i % cols) * 270}_${Math.floor(i / cols) * 480}`).join("|")}:fill=black`, "-frames:v", "1", "-q:v", "4", sheet]);
  files.unshift(sheet);
  if (ctx.noVideo) { await b.close(); return { files, warnings }; }

  const vid = path.join(work, "video.mp4"), N = Math.round(dur * FPS);
  const ff = spawn("ffmpeg", ["-y", "-i", bg, "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-", "-filter_complex", "[0:v][1:v]overlay=format=auto,format=yuv420p[v]", "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", String(FPS), vid]);
  let err = ""; ff.stderr.on("data", (d) => (err = (err + d).slice(-2000)));
  const t0 = Date.now();
  for (let f = 0; f < N; f++) {
    await p.evaluate((x) => window.render(x), f / FPS);
    const buf = await p.screenshot({ type: "png", omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (f % 150 === 0) process.stdout.write(`  frame ${f}/${N} (${((Date.now() - t0) / 1000).toFixed(0)} s)\n`);
  }
  ff.stdin.end(); const code = await new Promise((r) => ff.on("close", r));
  await b.close();
  if (code) throw new Error("ffmpeg overlay failed: " + err);
  // audio: knocks/ticks + optional voiceover + optional licensed music
  const evf = path.join(work, "events.json"); fs.writeFileSync(evf, JSON.stringify(events));
  const knocks = path.join(work, "knocks.wav");
  run(process.env.PYTHON || "python3", [path.join(__dirname, "audio.py"), evf, String(dur), knocks]);
  const ins = ["-i", vid, "-i", knocks]; let mix = "[1:a]volume=1[k]", lab = "[k]", n = 1;
  const vo = spec.voiceover && spec.voiceover.src && fs.existsSync(spec.voiceover.src) ? spec.voiceover : null;
  if (vo) { ins.push("-i", vo.src); mix += `;[${++n}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=${Math.round((vo.at || 0) * 1000)}:all=1,volume=${vo.gain ?? 1}[vo]`; lab += "[vo]"; }
  else warnings.push("voiceover slot empty: record voiceover.md and set \"voiceover\": {\"src\": \"…/voiceover.wav\"} (captions already carry the words)");
  const music = spec.music && spec.music.src && fs.existsSync(spec.music.src) ? spec.music : null;
  if (music) { ins.push("-i", music.src); const g = (music.gain ?? .16) * (vo ? .6 : 1); mix += `;[${++n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=${music.in || 0}:${(music.in || 0) + dur},asetpts=PTS-STARTPTS,volume=${g},afade=t=in:d=0.6,afade=t=out:st=${(dur - 1.6).toFixed(2)}:d=1.6[m]`; lab += "[m]"; }
  else warnings.push("music slot empty (licensed reel/music/drums.wav not in the repo): add \"music\": {\"src\": \"reel/music/drums.wav\", \"gain\": 0.16} on Akki's PC");
  mix += `;${lab}amix=inputs=${n}:normalize=0,alimiter=limit=0.9[a]`;
  const out = path.join(outDir, `${name}.mp4`);
  run("ffmpeg", ["-y", ...ins, "-filter_complex", mix, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-t", dur.toFixed(3), "-movflags", "+faststart", out]);
  files.unshift(out);
  for (const f of ["video.mp4", "ov.png", "knocks.wav", "events.json"]) fs.rmSync(path.join(work, f), { force: true });
  return { files, warnings };
}
module.exports = { renderExplainer };
