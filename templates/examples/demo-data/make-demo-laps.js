/* Generates two SYNTHETIC lap CSVs so the Debrief templates can be tested before real exports exist.
   They are NOT real laps: a made-up circuit and a simple point-mass model. Any render made from them
   carries the "DEMO DATA" tag (spec "demo": true). Replace with real exports for every real post.
     node templates/examples/demo-data/make-demo-laps.js  -> demo-lap-reference.csv, demo-lap-driver.csv */
const fs = require("fs"), path = require("path");
// made-up circuit: [straight metres, corner radius m (0 = none), corner angle deg]
const TRACK = [[620, 45, 110], [260, 120, 70], [380, 30, 160], [180, 200, 45], [520, 60, 95], [240, 90, 80], [700, 0, 0]];
const LAT = 32, BRK = 42, ACC = 11, VMAX = 86; // m/s², m/s
function lap({ brakeScale = {}, cornerScale = {}, early = {} }) {
  // build segments with per-metre speed limit
  const lim = [], cid = [];
  TRACK.forEach(([st, r, ang], i) => {
    for (let k = 0; k < st; k++) { lim.push(VMAX); cid.push(-1); }
    if (r) { const len = Math.round(r * ang * Math.PI / 180), v = Math.min(VMAX, Math.sqrt(LAT * r) * (cornerScale[i] || 1)); for (let k = 0; k < len; k++) { lim.push(v); cid.push(i); } }
  });
  const N = lim.length, v = lim.slice();
  // forward pass (acceleration limit, power fades with speed)
  for (let k = 1; k < N; k++) { const a = ACC * (1 - (v[k - 1] / (VMAX * 1.08)) ** 2) + 1; v[k] = Math.min(v[k], Math.sqrt(v[k - 1] ** 2 + 2 * a)); }
  // backward pass (braking limit; per-corner scale = a less confident driver; `early` adds a coast gap before braking)
  const brk = new Array(N).fill(0);
  for (let k = N - 2; k >= 0; k--) {
    let next = cid.slice(k).find((c) => c >= 0); const s = brakeScale[next] || 1;
    const vb = Math.sqrt(v[k + 1] ** 2 + 2 * BRK * s * (1 + v[k + 1] / 200));
    if (vb < v[k]) { v[k] = vb; brk[k] = s; }
  }
  // trail-brake shape: pressure tapers into the corner instead of a step
  const out = []; let t = 0;
  for (let k = 0; k < N; k++) {
    if (k) t += 1 / ((v[k] + v[k - 1]) / 2);
    let b = brk[k] ? .95 : 0;
    if (cid[k] >= 0 && k > 0 && (brk[k - 1] || out[k - 1]?.b > .02)) b = Math.max(0, (out[k - 1]?.b || 0) - .03);
    const th = b > .02 ? 0 : Math.min(1, cid[k] >= 0 ? .35 + .65 * (v[k] / lim[k]) ** 4 : 1);
    const st = cid[k] >= 0 ? (cid[k] % 2 ? -1 : 1) * Math.min(1, 40 / TRACK[cid[k]][1]) : 0;
    out.push({ d: k, t, v: v[k] * 3.6, b, th, st });
  }
  return out;
}
const ref = lap({});
const drv = lap({ brakeScale: { 0: .72, 2: .8 }, cornerScale: { 0: .955, 2: .95, 4: .99 } });
const csv = (rows) => "# SYNTHETIC DEMO LAP - not a real lap\ndistance_m,time_s,speed_kph,throttle,brake,steer\n" + rows.map((r) => [r.d, r.t.toFixed(4), r.v.toFixed(2), r.th.toFixed(3), r.b.toFixed(3), r.st.toFixed(3)].join(",")).join("\n") + "\n";
fs.writeFileSync(path.join(__dirname, "demo-lap-reference.csv"), csv(ref));
fs.writeFileSync(path.join(__dirname, "demo-lap-driver.csv"), csv(drv));
console.log("reference", ref.at(-1).t.toFixed(3), "driver", drv.at(-1).t.toFixed(3));
