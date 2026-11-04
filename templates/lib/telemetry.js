/* Lap telemetry: CSV in, aligned laps + delta + per-corner numbers out, and the DEBRIEF carousel slide list.
   CSV: one row per sample, header row required. Column names are matched loosely:
     distance  (distance, lap_distance, dist, LapDist, distance_m)        metres into the lap   [required]
     time      (time, lap_time, laptime, time_s, CurrentLapTime)          seconds into the lap   [required]
     speed     (speed, speed_kph, kph, Speed)                             km/h (m/s if column says _ms / mps)
     throttle  (throttle, gas, thr)  brake (brake, brk)                   0–1 or 0–100 (auto-scaled)
     steer     (steer, steering, steering_angle)                          any unit (only shape is drawn)
   Every number shown on a slide is computed from these files and also written to debrief-numbers.json. */
const fs = require("fs");

function parseCsv(file) {
  const txt = fs.readFileSync(file, "utf8").replace(/\r/g, "").trim().split("\n").filter((l) => l && !l.startsWith("#"));
  const sep = txt[0].includes(";") && !txt[0].includes(",") ? ";" : txt[0].includes("\t") ? "\t" : ",";
  const head = txt[0].split(sep).map((h) => h.trim().replace(/^"|"$/g, ""));
  const find = (names, re) => { const i = head.findIndex((h) => names.includes(h.toLowerCase().replace(/[\s()]/g, "")) || (re && re.test(h))); return i; };
  const col = {
    d: find(["distance", "lapdistance", "lap_distance", "dist", "lapdist", "distance_m", "distancem"], /dist/i),
    t: find(["time", "laptime", "lap_time", "time_s", "times", "currentlaptime", "elapsed"], /^time|lap.?time/i),
    v: find(["speed", "speed_kph", "kph", "speedkph", "speed_kmh", "kmh", "speed_ms", "mps"], /speed/i),
    th: find(["throttle", "gas", "thr", "throttle_pct"], /throttle|gas/i),
    br: find(["brake", "brk", "brake_pct"], /brake/i),
    st: find(["steer", "steering", "steering_angle", "steer_angle"], /steer/i),
  };
  if (col.d < 0 || col.t < 0) throw new Error(`${file}: needs a distance and a time column (found: ${head.join(", ")})`);
  const rows = txt.slice(1).map((l) => l.split(sep).map((x) => parseFloat(x)));
  const pick = (i) => (i < 0 ? null : rows.map((r) => r[i]));
  let v = pick(col.v); if (v && /_ms|mps/i.test(head[col.v])) v = v.map((x) => x * 3.6);
  const norm = (a) => { if (!a) return null; const mx = Math.max(...a.filter(Number.isFinite)); return mx > 1.5 ? a.map((x) => x / 100) : a; };
  const lap = { d: pick(col.d), t: pick(col.t), v, th: norm(pick(col.th)), br: norm(pick(col.br)), st: pick(col.st) };
  // keep monotonic distance only
  const keep = []; let last = -Infinity;
  lap.d.forEach((d, i) => { if (Number.isFinite(d) && Number.isFinite(lap.t[i]) && d > last) { keep.push(i); last = d; } });
  for (const k in lap) if (lap[k]) lap[k] = keep.map((i) => lap[k][i]);
  lap.length = lap.d.at(-1); lap.lapTime = lap.t.at(-1) - lap.t[0];
  return lap;
}
/* linear interpolation of channel ch at distance x */
function interp(lap, ch, x) {
  const d = lap.d; let lo = 0, hi = d.length - 1;
  if (x <= d[0]) return lap[ch][0]; if (x >= d[hi]) return lap[ch][hi];
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (d[m] <= x) lo = m; else hi = m; }
  const f = (x - d[lo]) / (d[hi] - d[lo]); return lap[ch][lo] + (lap[ch][hi] - lap[ch][lo]) * f;
}
/* align two laps on a common distance grid (step metres). delta = B − A (positive: B is slower) */
function compare(A, B, step = 2) {
  const L = Math.min(A.length, B.length), n = Math.floor(L / step);
  const g = { d: [], tA: [], tB: [], vA: [], vB: [], bA: [], bB: [], thA: [], thB: [], delta: [] };
  for (let i = 0; i <= n; i++) {
    const x = i * step; g.d.push(x);
    const ta = interp(A, "t", x) - A.t[0], tb = interp(B, "t", x) - B.t[0];
    g.tA.push(ta); g.tB.push(tb); g.delta.push(tb - ta);
    for (const [k, lap, ch] of [["vA", A, "v"], ["vB", B, "v"], ["bA", A, "br"], ["bB", B, "br"], ["thA", A, "th"], ["thB", B, "th"]]) g[k].push(lap[ch] ? interp(lap, ch, x) : null);
  }
  return g;
}
/* corners: from the spec ({name, from, to} in metres) or auto = braking zones of lap A */
function corners(g, spec) {
  if (spec && spec.length) return spec.map((c) => ({ ...c }));
  const out = []; const b = g.bA; if (!b[0] && b[0] !== 0) return out;
  let i = 0;
  while (i < b.length) {
    if (b[i] > .2) {
      const s = i; while (i < b.length && !(g.thA[i] > .9 && b[i] < .05)) i++;
      out.push({ name: `T${out.length + 1}`, from: Math.max(0, g.d[s] - 60), to: Math.min(g.d.at(-1), g.d[Math.min(i, b.length - 1)] + 40) });
    } else i++;
  }
  return out;
}
function cornerStats(g, c) {
  const idx = (x) => Math.max(0, Math.min(g.d.length - 1, Math.round(x / (g.d[1] - g.d[0]))));
  const a = idx(c.from), z = idx(c.to);
  const bp = (arr) => { for (let i = a; i <= z; i++) if (arr[i] > .2) return g.d[i]; return null; };
  const minv = (arr) => { let m = Infinity, at = 0; for (let i = a; i <= z; i++) if (arr[i] < m) { m = arr[i]; at = g.d[i]; } return [m, at]; };
  const [vminA, atA] = minv(g.vA), [vminB, atB] = minv(g.vB);
  return { ...c, lost: g.delta[z] - g.delta[a], brakeA: bp(g.bA), brakeB: bp(g.bB), vminA, vminB, atA, atB };
}
const r2 = (x, d = 2) => Math.round(x * 10 ** d) / 10 ** d;
const fmtLap = (s) => { const m = Math.floor(s / 60), r = s - m * 60; return `${m}:${r.toFixed(3).padStart(6, "0")}`; };
const tpl = (s, v) => (Array.isArray(s) ? s.map((x) => tpl(x, v)) : s && typeof s === "object" ? Object.fromEntries(Object.entries(s).map(([k, x]) => [k, tpl(x, v)])) : typeof s === "string" ? s.replace(/\{(\w+)\}/g, (_, k) => v[k] ?? `{${k}}`) : s);

/* DEBRIEF carousel: spec -> {series, slides} for the shared carousel renderer */
function debriefSlides(spec, res) {
  const A = parseCsv(res(spec.lapA.csv)), B = parseCsv(res(spec.lapB.csv));
  const g = compare(A, B, spec.step || 2);
  const cs = corners(g, spec.corners).map((c) => cornerStats(g, c));
  const top = [...cs].sort((x, y) => y.lost - x.lost).slice(0, spec.focus || 2);
  const gap = B.lapTime - A.lapTime, topLost = top.reduce((s, c) => s + c.lost, 0);
  const la = spec.lapA.label || "REFERENCE", lb = spec.lapB.label || "DRIVER";
  const V = { gap: r2(gap).toFixed(2), lost: r2(topLost).toFixed(2), n: top.length, nWord: ["zero", "one", "two", "three", "four"][top.length] || top.length,
    share: Math.round(topLost / gap * 100), lapA: fmtLap(A.lapTime), lapB: fmtLap(B.lapTime), A: la, B: lb, c1: top[0]?.name, c2: top[1]?.name, track: spec.track || "" };
  const ep = spec.episode != null ? `EP ${spec.episode}` : "";
  const slides = [];
  slides.push({ type: "hook", photo: spec.hook?.photo, pos: spec.hook?.pos, photoHeight: 900, kicker: tpl(spec.hook?.kicker || `THE DEBRIEF · ${ep} · {track}`, V),
    title: tpl(spec.hook?.title || ["{gap}s off.", "{lost}s of it in {nWord} corners."], V), size: spec.hook?.size || 100, sub: tpl(spec.hook?.sub || "", V) });
  slides.push({ type: "content", kicker: "01 · The laps", title: ["Same car.", "{gap}s apart."].map((s) => tpl(s, V)), visualTop: 520, visualHeight: 300,
    visual: { type: "stats", items: [{ value: V.lapA, label: la.toUpperCase(), size: 66 }, { value: V.lapB, label: lb.toUpperCase(), size: 66 }, { value: `+${V.gap}`, label: "GAP (S)", hot: true, size: 66 }] },
    body: tpl(spec.lapsBody || `${spec.car ? `${spec.car} · ` : ""}${spec.track || ""}. The gap isn't spread evenly: **{share}% of it comes from {nWord} corners.**`, V), bodyTop: 900 });
  const ds = (arr, k = 4) => g.d.filter((_, i) => i % k === 0).map((d, j) => [d, arr[j * k]]);
  slides.push({ type: "content", kicker: "02 · Speed trace", title: ["Where the", "speed goes."], visualHeight: 560,
    visual: { type: "chart", xLabel: "DISTANCE (M)", yLabel: "SPEED (KM/H)", yTicks: 4,
      bands: top.map((c) => ({ x0: c.from, x1: c.to, label: c.name })),
      series: [{ label: la, color: "#2440FF", points: ds(g.vA), width: 4 }, { label: lb, color: "#8C93A3", points: ds(g.vB), width: 3 }] },
    body: tpl(spec.traceBody || "Highlighted: the corners where most of the time goes. **Look at the entries.**", V) });
  slides.push({ type: "content", kicker: "03 · The delta", title: ["Time lost,", "metre by metre."], visualHeight: 560,
    visual: { type: "chart", xLabel: "DISTANCE (M)", yLabel: `${lb.toUpperCase()} VS ${la.toUpperCase()} (S)`, zeroLine: true, yTicks: 4, yFmt: 2,
      marks: top.map((c, i) => ({ x: c.from, label: c.name, color: "#5B7BFF", dy: i * 26 })),
      series: [{ label: "delta", color: "#2440FF", points: ds(g.delta), area: true, width: 4 }] },
    body: tpl(spec.deltaBody || "Line going up = time lost. **Steep steps are the corners.** Flat = matching pace.", V) });
  const c1 = top[0];
  if (c1) {
    const pad = 120, lo = Math.max(0, c1.from - pad), hi = Math.min(g.d.at(-1), c1.to + pad);
    const zoom = (arr) => g.d.map((d, i) => [d, arr[i]]).filter(([d]) => d >= lo && d <= hi);
    const dotsA = c1.brakeA != null ? [[c1.brakeA, interp({ d: g.d, v: g.vA }, "v", c1.brakeA), `${la.toUpperCase()} BRAKES`, "start"]] : [];
    const dotsB = c1.brakeB != null ? [[c1.brakeB, interp({ d: g.d, v: g.vB }, "v", c1.brakeB), `${lb.toUpperCase()} BRAKES`, "end"]] : [];
    const earlier = c1.brakeA != null && c1.brakeB != null ? Math.round(c1.brakeA - c1.brakeB) : null;
    V.early = earlier != null ? Math.abs(earlier) : "?"; V.earlyWord = earlier >= 0 ? "earlier" : "later";
    V.vmA = Math.round(c1.vminA); V.vmB = Math.round(c1.vminB); V.c1lost = r2(c1.lost).toFixed(2);
    slides.push({ type: "content", kicker: `04 · ${c1.name} up close`, title: tpl(spec.cornerTitle || ["Brakes {early} m {earlyWord}.", "Carries less speed."], V), visualHeight: 560,
      visual: { type: "chart", xLabel: "DISTANCE (M)", yLabel: "SPEED (KM/H)", yTicks: 4,
        series: [{ label: la, color: "#2440FF", points: zoom(g.vA), dots: dotsA }, { label: lb, color: "#8C93A3", points: zoom(g.vB), dots: dotsB, width: 3 }] },
      body: tpl(spec.cornerBody || "Minimum speed **{vmB} vs {vmA} km/h**. That's **{c1lost}s** in one corner, and it carries down the next straight.", V) });
  }
  slides.push({ type: "content", kicker: "05 · Corner by corner", title: ["The", "breakdown."], visualHeight: 620,
    visual: { type: "table", columns: ["Corner", "Brake point", "Min speed (km/h)", "Lost"], mono: [3],
      rows: [...cs].sort((x, y) => y.lost - x.lost).slice(0, spec.tableRows || 5).map((c) => [c.name,
        c.brakeA != null && c.brakeB != null ? (Math.abs(c.brakeA - c.brakeB) < 3 ? "Same" : `${Math.round(Math.abs(c.brakeA - c.brakeB))} m ${c.brakeB < c.brakeA ? "earlier" : "later"}`) : "—",
        `${Math.round(c.vminB)} vs ${Math.round(c.vminA)}`, `${c.lost >= 0 ? "+" : ""}${r2(c.lost).toFixed(2)}s`]),
      highlight: [0, 1].slice(0, top.length) },
    note: `${lb} vs ${la} · from the lap files` });
  if (spec.drill) slides.push({ type: "content", kicker: "06 · The one drill", title: tpl(spec.drill.title || ["One drill.", "This week."], V), visualHeight: 680,
    visual: { type: "flow", steps: tpl(spec.drill.steps, V) }, body: tpl(spec.drill.body, V) });
  slides.push({ type: "close", kicker: "Your lap next", title: tpl(spec.close?.title || ["Send me", "your lap."], V),
    body: tpl(spec.close?.body || "Lap video with inputs or a telemetry export, plus track, car and wheel. **Link in bio.** The best ones get a Debrief.", V), cta: "THE DEBRIEF · EVERY SATURDAY" });
  return { template: "debrief-carousel", series: "THE DEBRIEF", number: spec.episode != null ? `EP ${spec.episode}` : null, demo: spec.demo, pattern: spec.pattern, slides,
    _numbers: { lapA: { label: la, time: A.lapTime }, lapB: { label: lb, time: B.lapTime }, gap, corners: cs, top: top.map((c) => c.name) } };
}

module.exports = { parseCsv, interp, compare, corners, cornerStats, debriefSlides, fmtLap };
