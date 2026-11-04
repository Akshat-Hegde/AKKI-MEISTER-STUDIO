/* AKKI MEISTER kit: brand chrome + chart/diagram helpers (plain SVG, no libraries).
   Every helper returns an SVG/HTML string or element so slides, stories and reel overlays share one look. */
(function () {
  const C = { night: "#07080C", blue: "#2440FF", sky: "#5B7BFF", ice: "#F3F4F6", steel: "#8C93A3" };
  const K = Math.tan(12 * Math.PI / 180);
  const NS = "http://www.w3.org/2000/svg";
  const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  /* inline markup: **x** -> sky emphasis, ~~x~~ -> steel aside */
  const rich = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<em>$1</em>").replace(/~~(.+?)~~/g, "<i>$1</i>").replace(/\n/g, "<br>");
  /* headline: array of lines (or "A / B"), last line cobalt, must end in a full stop (brand rule) */
  const headline = (t) => {
    const lines = Array.isArray(t) ? t : String(t).split(/\s*\/\s*|\n/);
    return lines.map((l, i) => i === lines.length - 1 && lines.length > 1 ? `<span class="c">${esc(l)}</span>` : esc(l)).join("<br>");
  };
  const mark = () => LOGO.lockup.slice(0, LOGO.lockup.indexOf("<g transform"));
  const markSvg = (w = 120, op = 1) => `<svg viewBox="0 0 262 100" width="${w}" height="${w * 100 / 262}" style="opacity:${op}">${mark()}</svg>`;
  const lockupSvg = (w = 520) => { const v = LOGO.lvb.split(" ").map(Number); return `<svg viewBox="${LOGO.lvb}" width="${w}" height="${w * v[3] / v[2]}">${LOGO.lockup}</svg>`; };

  /* photo block with brand treatment. fade: css gradient (or preset name) */
  const FADES = {
    bottom: "linear-gradient(180deg,rgba(7,8,12,.55) 0%,rgba(7,8,12,0) 22%,rgba(7,8,12,0) 45%,rgba(7,8,12,.75) 75%,#07080C 100%)",
    top: "linear-gradient(0deg,rgba(7,8,12,.55) 0%,rgba(7,8,12,0) 25%,rgba(7,8,12,0) 55%,rgba(7,8,12,.8) 85%,#07080C 100%)",
    both: "linear-gradient(180deg,#07080C 0%,rgba(7,8,12,0) 22%,rgba(7,8,12,0) 62%,rgba(7,8,12,.8) 88%,#07080C 100%)",
    soft: "linear-gradient(180deg,rgba(7,8,12,.35),rgba(7,8,12,.35))",
    none: "none",
  };
  const photo = ({ src, pos = "50% 50%", x = 0, y = 0, w, h, fade = "bottom", tint = .28, clip = "", z = 1, bright = .82, zoom = 1 }) =>
    `<div class="photo" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;z-index:${z};${clip ? `clip-path:${clip};` : ""}">
      <img src="${src}" style="object-position:${pos};filter:grayscale(.12) contrast(1.06) brightness(${bright}) saturate(.9);transform:scale(${zoom});transform-origin:${pos}">
      <div class="tint" style="opacity:${tint}"></div><div class="scan"></div><div class="fade" style="background:${FADES[fade] || fade}"></div></div>`;
  /* 12° parallelogram clip for a w×h box */
  const lean = (h, side = "both") => { const o = h * K; return side === "both" ? `polygon(${o}px 0,100% 0,calc(100% - ${o}px) 100%,0 100%)` : side === "right" ? `polygon(0 0,100% 0,calc(100% - ${o}px) 100%,0 100%)` : `polygon(${o}px 0,100% 0,100% 100%,0 100%)`; };

  /* breaking chequered flag (svg string). cols shrink, drift and fade to the right */
  function flag(x, y, { cols = 12, rows = 4, sq = 20, op = .5, fill = C.ice } = {}) {
    const para = (x, y, w, h) => `${x + h * K},${y} ${x + w + h * K},${y} ${x + w},${y + h} ${x},${y + h}`;
    let out = "", cx = x;
    for (let c = 0; c < cols; c++) {
      const k = c / (cols - 1), s2 = sq * (1 - .62 * k), gap = sq * .06 + k * sq * .55;
      for (let r = 0; r < rows; r++) {
        if ((r + c) % 2) continue; if (k > .45 && ((c * 7 + r * 3) % 5 === 0)) continue;
        const yy = y + r * sq + (sq - s2) / 2 + (r - rows / 2) * k * sq * .25;
        out += `<polygon points="${para(cx, yy, s2, s2)}" fill="${fill}" fill-opacity="${(op * (1 - .75 * k)).toFixed(3)}"/>`;
      }
      cx += s2 + gap;
    }
    return out;
  }

  /* ---------------- charts ---------------- */
  const niceStep = (span, n = 5) => { const r = span / n, p = Math.pow(10, Math.floor(Math.log10(r))), m = r / p; return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p; };
  const fmt = (v, d) => (Math.abs(v) < 1e-9 ? 0 : v).toFixed(d);
  /* lineChart({w,h,series:[{label,points:[[x,y]],color,width,dash}],xLabel,yLabel,xDomain,yDomain,bands:[{x0,x1,label}],marks:[{x,label}],illustrative,zeroLine,yFmt})
     illustrative=true hides numeric ticks (for concept charts with no real data). */
  function lineChart(o) {
    const W = o.w, H = o.h, L = o.illustrative ? 40 : 96, R = 24, T = 30, B = 70;
    const all = o.series.flatMap((s) => s.points);
    const xd = o.xDomain || [Math.min(...all.map((p) => p[0])), Math.max(...all.map((p) => p[0]))];
    let yd = o.yDomain || [Math.min(...all.map((p) => p[1])), Math.max(...all.map((p) => p[1]))];
    if (!o.yDomain) { const pad = (yd[1] - yd[0]) * .1 || 1; yd = [yd[0] - pad, yd[1] + pad]; }
    const X = (v) => L + (v - xd[0]) / (xd[1] - xd[0]) * (W - L - R), Y = (v) => T + (1 - (v - yd[0]) / (yd[1] - yd[0])) * (H - T - B);
    let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="overflow:visible">`;
    for (const b of o.bands || []) s += `<rect x="${X(b.x0)}" y="${T}" width="${X(b.x1) - X(b.x0)}" height="${H - T - B}" fill="${C.blue}" fill-opacity=".14"/>` +
      (b.label ? `<text x="${(X(b.x0) + X(b.x1)) / 2}" y="${T - 8}" fill="${C.sky}" font-family="JBM" font-size="18" letter-spacing="2" text-anchor="middle">${esc(b.label)}</text>` : "");
    if (!o.illustrative) {
      const ys = niceStep(yd[1] - yd[0], o.yTicks || 4), yf = o.yFmt ?? (ys < 1 ? 2 : 0);
      for (let v = Math.ceil(yd[0] / ys) * ys; v <= yd[1] + 1e-9; v += ys)
        s += `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" stroke="${C.ice}" stroke-opacity=".1"/><text x="${L - 14}" y="${Y(v) + 6}" fill="${C.steel}" font-family="JBM" font-size="18" text-anchor="end">${fmt(v, yf)}</text>`;
      const xs = niceStep(xd[1] - xd[0], o.xTicks || 5);
      for (let v = Math.ceil(xd[0] / xs) * xs; v <= xd[1] + 1e-9; v += xs)
        s += `<line x1="${X(v)}" x2="${X(v)}" y1="${T}" y2="${H - B}" stroke="${C.ice}" stroke-opacity=".06"/><text x="${X(v)}" y="${H - B + 30}" fill="${C.steel}" font-family="JBM" font-size="18" text-anchor="middle">${fmt(v, xs < 1 ? 1 : 0)}</text>`;
    } else {
      for (let i = 0; i <= 4; i++) s += `<line x1="${L}" x2="${W - R}" y1="${T + i * (H - T - B) / 4}" y2="${T + i * (H - T - B) / 4}" stroke="${C.ice}" stroke-opacity=".08"/>`;
    }
    if (o.zeroLine && yd[0] < 0 && yd[1] > 0) s += `<line x1="${L}" x2="${W - R}" y1="${Y(0)}" y2="${Y(0)}" stroke="${C.ice}" stroke-opacity=".45" stroke-width="1.5"/>`;
    s += `<line x1="${L}" x2="${W - R}" y1="${H - B}" y2="${H - B}" stroke="${C.ice}" stroke-opacity=".35"/>`;
    for (const m of o.marks || []) s += `<line x1="${X(m.x)}" x2="${X(m.x)}" y1="${T}" y2="${H - B}" stroke="${m.color || C.ice}" stroke-opacity=".55" stroke-dasharray="6 6"/>` +
      (m.label ? `<text x="${X(m.x) + 10}" y="${T + 22 + (m.dy || 0)}" fill="${m.color || C.ice}" font-family="JBM" font-size="18" letter-spacing="1.5">${esc(m.label)}</text>` : "");
    o.series.map((sr, i) => [sr, i]).reverse().forEach(([sr, i]) => {
      const col = sr.color || [C.blue, C.sky, C.steel][i % 3];
      if (sr.area) s += `<path d="M${X(sr.points[0][0])},${Y(0)} ${sr.points.map((p) => `L${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join(" ")} L${X(sr.points.at(-1)[0])},${Y(0)} Z" fill="${col}" fill-opacity=".18"/>`;
      s += `<polyline points="${sr.points.map((p) => `${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join(" ")}" fill="none" stroke="${col}" stroke-width="${sr.width || 4}" stroke-linejoin="round" stroke-linecap="round" ${sr.dash ? `stroke-dasharray="${sr.dash}"` : ""}/>`;
      for (const d of sr.dots || []) s += `<circle cx="${X(d[0])}" cy="${Y(d[1])}" r="8" fill="${C.night}" stroke="${col}" stroke-width="4"/>` + (d[2] ? `<text x="${X(d[0]) + (d[3] === "end" ? -16 : 16)}" y="${Y(d[1]) - 16}" fill="${col}" font-family="JBM" font-size="18" letter-spacing="1" text-anchor="${d[3] || "start"}">${esc(d[2])}</text>` : "");
    });
    if (o.xLabel) s += `<text x="${W - R}" y="${H - 6}" fill="${C.steel}" font-family="JBM" font-size="18" letter-spacing="2" text-anchor="end">${esc(o.xLabel)}</text>`;
    if (o.yLabel) s += `<text x="${L}" y="${T - 8 - (o.bands?.some((b) => b.label) ? 26 : 0)}" fill="${C.steel}" font-family="JBM" font-size="18" letter-spacing="2">${esc(o.yLabel)}</text>`;
    return s + "</svg>";
  }
  /* legend row (html) */
  const legend = (series) => `<div style="display:flex;gap:34px;flex-wrap:wrap">${series.map((s, i) => `<div class="m" style="display:flex;align-items:center;gap:12px;font-size:20px;color:${C.ice}"><span style="width:34px;height:0;border-top:5px ${s.dash ? "dashed" : "solid"} ${s.color || [C.blue, C.sky, C.steel][i % 3]}"></span>${esc(s.label)}</div>`).join("")}</div>`;

  /* horizontal bars: items [{label, value, note, hl}] */
  function bars({ w, items, unit = "", max, dec = 2 }) {
    const mx = max || Math.max(...items.map((i) => Math.abs(i.value))) * 1.1;
    return `<div style="width:${w}px;display:flex;flex-direction:column;gap:22px">${items.map((it) => `
      <div><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px">
        <span class="b" style="font-size:30px">${esc(it.label)}</span><span class="m" style="font-size:26px;color:${it.hl ? C.sky : C.ice}">${typeof it.value === "number" ? it.value.toFixed(dec) : it.value}${unit}</span></div>
        <div style="height:18px;background:rgba(243,244,246,.07);position:relative"><div style="position:absolute;left:0;top:0;bottom:0;width:${Math.abs(it.value) / mx * 100}%;background:${it.hl ? C.blue : C.steel};transform:skewX(-12deg);transform-origin:0 100%"></div></div>
        ${it.note ? `<div class="m" style="font-size:18px;color:${C.steel};margin-top:10px">${esc(it.note)}</div>` : ""}</div>`).join("")}</div>`;
  }

  /* semicircle gauge: value in [min,max] */
  function gauge({ size = 360, value, min = 0, max = 100, label = "", unit = "", ticks = 10 }) {
    const r = size / 2 - 20, cx = size / 2, cy = size / 2 + 10, a0 = Math.PI, a = (v) => a0 - (v - min) / (max - min) * Math.PI;
    const pt = (ang, rr) => [cx + rr * Math.cos(ang), cy - rr * Math.sin(ang)];
    const arc = (v0, v1, rr) => { const [x0, y0] = pt(a(v0), rr), [x1, y1] = pt(a(v1), rr); return `M${x0},${y0} A${rr},${rr} 0 0 1 ${x1},${y1}`; };
    let s = `<svg width="${size}" height="${size / 2 + 60}">`;
    s += `<path d="${arc(min, max, r)}" stroke="${C.ice}" stroke-opacity=".12" stroke-width="22" fill="none"/>`;
    s += `<path d="${arc(min, value, r)}" stroke="${C.blue}" stroke-width="22" fill="none"/>`;
    for (let i = 0; i <= ticks; i++) { const v = min + (max - min) * i / ticks, [x0, y0] = pt(a(v), r - 22), [x1, y1] = pt(a(v), r - 36); s += `<line x1="${x0}" y1="${y0}" x2="${x1}" y2="${y1}" stroke="${C.steel}" stroke-width="2"/>`; }
    s += `<text x="${cx}" y="${cy - 10}" fill="${C.ice}" font-family="ClashD" font-size="${size / 5}" text-anchor="middle">${esc(value)}${esc(unit)}</text>`;
    s += `<text x="${cx}" y="${cy + 40}" fill="${C.steel}" font-family="JBM" font-size="18" letter-spacing="3" text-anchor="middle">${esc(label)}</text>`;
    return s + "</svg>";
  }

  /* split bar e.g. brake bias 56/44: {left:{label,value}, right:{label,value}} */
  const split = ({ w = 900, left, right }) => `<div style="width:${w}px">
    <div style="display:flex;height:96px;gap:10px">
      <div style="flex:${left.value};background:${C.blue};display:flex;align-items:center;padding-left:28px;clip-path:${lean(96, "right")}"><span class="h" style="font-size:54px">${esc(left.value)}%</span></div>
      <div style="flex:${right.value};background:rgba(243,244,246,.1);display:flex;align-items:center;justify-content:flex-end;padding-right:28px;clip-path:${lean(96, "left")}"><span class="h" style="font-size:54px">${esc(right.value)}%</span></div></div>
    <div class="m" style="display:flex;justify-content:space-between;font-size:20px;color:${C.steel};margin-top:16px;letter-spacing:.18em"><span>${esc(left.label)}</span><span>${esc(right.label)}</span></div></div>`;

  /* flow diagram: steps [{title, body}] stacked with arrows */
  const flow = ({ w = 936, steps }) => `<div style="width:${w}px;display:flex;flex-direction:column;gap:0">${steps.map((s, i) => `
    ${i ? `<div style="height:44px;display:flex;align-items:center;padding-left:46px"><svg width="24" height="40"><path d="M12 0v32M3 24l9 10 9-10" stroke="${C.sky}" stroke-width="3" fill="none"/></svg></div>` : ""}
    <div class="card${i === steps.length - 1 ? " lead" : ""}" style="display:flex;gap:26px;align-items:flex-start;padding:24px 28px">
      <div class="m" style="font-size:22px;color:${C.sky};padding-top:6px">0${i + 1}</div>
      <div><div class="b" style="font-size:32px">${rich(s.title)}</div>${s.body ? `<div class="b" style="font-size:24px;color:${C.steel};margin-top:6px">${rich(s.body)}</div>` : ""}</div></div>`).join("")}</div>`;

  /* top-down car with axle-load discs (concept diagram): front/rear = relative size, frontText/rearText = label shown */
  function carLoad({ w = 440, front = 1, rear = 1, frontText = "", rearText = "", label = "" }) {
    const h = w * 1.4, cx = w * .3, mx = Math.max(front, rear), fy = h * .27, ry = h * .7;
    let s = `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">`;
    s += `<path d="M${cx - 34},${h * .16} L${cx + 34},${h * .16} L${cx + 60},${h * .42} L${cx + 70},${h * .78} L${cx - 70},${h * .78} L${cx - 60},${h * .42} Z" fill="rgba(243,244,246,.05)" stroke="${C.ice}" stroke-opacity=".45" stroke-width="2"/>`;
    s += `<rect x="${cx - 120}" y="${h * .11}" width="240" height="18" fill="${C.ice}" fill-opacity=".45"/><rect x="${cx - 95}" y="${h * .82}" width="190" height="18" fill="${C.ice}" fill-opacity=".45"/>`;
    for (const [yy, sc] of [[fy, 1], [ry, 1.15]]) for (const sd of [-1, 1]) s += `<rect x="${cx + sd * 104 - 22 * sc}" y="${yy - 42 * sc}" width="${44 * sc}" height="${84 * sc}" rx="9" fill="#1a1e2b" stroke="${C.steel}" stroke-width="2"/>`;
    s += `<circle cx="${cx}" cy="${fy}" r="${16 + 44 * front / mx}" fill="${C.blue}" fill-opacity=".9"/><circle cx="${cx}" cy="${ry}" r="${16 + 44 * rear / mx}" fill="${C.sky}" fill-opacity=".45"/>`;
    s += `<text x="${cx + 140}" y="${fy - 6}" fill="${C.steel}" font-family="JBM" font-size="18" letter-spacing="2">FRONT</text><text x="${cx + 140}" y="${fy + 28}" fill="${C.ice}" font-family="ClashD" font-size="28">${esc(frontText)}</text>`;
    s += `<text x="${cx + 140}" y="${ry - 6}" fill="${C.steel}" font-family="JBM" font-size="18" letter-spacing="2">REAR</text><text x="${cx + 140}" y="${ry + 28}" fill="${C.ice}" font-family="ClashD" font-size="28">${esc(rearText)}</text>`;
    if (label) s += `<text x="${w / 2}" y="${h - 4}" fill="${C.sky}" font-family="JBM" font-size="19" letter-spacing="2.5" text-anchor="middle">${esc(label)}</text>`;
    return s + "</svg>";
  }

  /* ---------------- track-corner sketch ----------------
     corner({w,h, turns:[{angle:90, radius:220, dir:"R"}], straight:[before, between..., after] (px),
             line:{apex:.5, width:.8} racing line (apex = fraction through the turn; <.5 early apex, >.5 late),
             markers:[{at:"brake"|"turnin"|"apex"|"exit"| number 0..1 along whole path, label}],
             brake:{from, to} (fractions along path) -> brake-pressure ramp drawn as a fading band on the line,
             trackWidth}) */
  function corner(o) {
    const W = o.w, H = o.h, tw = o.trackWidth || 120;
    const turns = o.turns || [{ angle: 90, radius: 220, dir: "R" }];
    const st = o.straight || [380, ...turns.slice(1).map(() => 140), 380];
    // centreline polyline in local units, starting heading "up"
    let x = 0, y = 0, hd = -Math.PI / 2; const pts = [[x, y, -1]]; // third = turn index or -1
    const go = (len, ti) => { const n = Math.max(2, Math.round(len / 6)); for (let i = 1; i <= n; i++) { x += Math.cos(hd) * len / n; y += Math.sin(hd) * len / n; pts.push([x, y, ti]); } };
    const turnSeg = (t, ti) => { const ang = t.angle * Math.PI / 180, sgn = t.dir === "L" ? -1 : 1, n = Math.max(8, Math.round(t.angle / 3)); const step = t.radius * ang / n; for (let i = 0; i < n; i++) { hd += sgn * ang / n / 2; x += Math.cos(hd) * step; y += Math.sin(hd) * step; hd += sgn * ang / n / 2; pts.push([x, y, ti, (i + 1) / n]); } };
    go(st[0], -1); turns.forEach((t, i) => { turnSeg(t, i); go(st[i + 1] ?? 300, -1); });
    // cumulative length
    const cum = [0]; for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const Ltot = cum.at(-1);
    // normals
    const nrm = pts.map((p, i) => { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)]; const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1; return [-dy / l, dx / l]; });
    // racing line offset: per turn, outside -> inside at apex -> outside. sign: inside of a right turn is +normal side for our normal convention
    const ln = o.line || {}; const apexF = ln.apex ?? .5, lw = (ln.width ?? .8) * tw / 2;
    const turnIdx = pts.map((p) => p[2]);
    const tStart = turns.map((_, ti) => pts.findIndex((p) => p[2] === ti)), tEnd = turns.map((_, ti) => pts.length - 1 - [...pts].reverse().findIndex((p) => p[2] === ti));
    const inside = (ti) => (turns[ti].dir === "L" ? -1 : 1);
    const off = pts.map((p, i) => {
      // find nearest turn by arc length and blend
      let best = 0;
      turns.forEach((t, ti) => {
        const s0 = cum[tStart[ti]], s1 = cum[tEnd[ti]], sA = s0 + (s1 - s0) * apexF, span = Math.max(160, (s1 - s0) * .9);
        const s = cum[i]; const pre = s0 - span, post = s1 + span;
        let v;
        if (s < pre || s > post) v = -1; else if (s <= sA) v = -1 + 2 * Math.sin(Math.PI / 2 * (s - pre) / (sA - pre)) ** 2; else v = 1 - 2 * Math.sin(Math.PI / 2 * (s - sA) / (post - sA)) ** 2;
        const val = v * inside(ti); // +1 = inside of this turn
        const w = Math.exp(-Math.pow((s - sA) / (span * 1.2), 2));
        best += val * w;
        if (ti === 0 && turns.length === 1) best = val;
      });
      return Math.max(-1, Math.min(1, best));
    });
    const line = pts.map((p, i) => [p[0] + nrm[i][0] * off[i] * lw, p[1] + nrm[i][1] * off[i] * lw]);
    // fit into box
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const pad = tw / 2 + 30, minx = Math.min(...xs) - pad, maxx = Math.max(...xs) + pad, miny = Math.min(...ys) - pad, maxy = Math.max(...ys) + pad;
    const sc = Math.min(W / (maxx - minx), H / (maxy - miny)), ox = (W - (maxx - minx) * sc) / 2 - minx * sc, oy = (H - (maxy - miny) * sc) / 2 - miny * sc;
    const P = ([px, py]) => `${(px * sc + ox).toFixed(1)},${(py * sc + oy).toFixed(1)}`;
    const atF = (f) => { const s = f * Ltot; let i = cum.findIndex((c) => c >= s); if (i < 0) i = cum.length - 1; return i; };
    const named = (m) => typeof m === "number" ? atF(m) : m === "turnin" ? Math.max(0, tStart[0] - 4) : m === "apex" ? Math.round(tStart[0] + (tEnd[0] - tStart[0]) * apexF) : m === "exit" ? Math.min(pts.length - 1, tEnd[0] + Math.round(30 / 6 * 6)) : m === "brake" ? atF(o.brake?.from ?? Math.max(0, cum[tStart[0]] / Ltot - .22)) : 0;
    let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`;
    const cl = pts.map(P).join(" ");
    s += `<polyline points="${cl}" fill="none" stroke="#151926" stroke-width="${tw * sc}" stroke-linejoin="round"/>`;
    // kerbs on the inside of each turn
    turns.forEach((t, ti) => { const a = Math.max(0, tStart[ti] - 2), b = Math.min(pts.length - 1, tEnd[ti] + 2); const ins = inside(ti);
      const kp = pts.slice(a, b + 1).map((p, j) => [p[0] + nrm[a + j][0] * ins * (tw / 2 - 6), p[1] + nrm[a + j][1] * ins * (tw / 2 - 6)]);
      s += `<polyline points="${kp.map(P).join(" ")}" fill="none" stroke="${C.ice}" stroke-opacity=".7" stroke-width="${10 * sc}" stroke-dasharray="${14 * sc} ${14 * sc}"/>`; });
    // track edges
    for (const sd of [-1, 1]) s += `<polyline points="${pts.map((p, i) => P([p[0] + nrm[i][0] * sd * tw / 2, p[1] + nrm[i][1] * sd * tw / 2])).join(" ")}" fill="none" stroke="${C.ice}" stroke-opacity=".28" stroke-width="2"/>`;
    // racing line (optionally the alternative line, dashed steel)
    if (o.altLine) { const al = o.altLine, aw = (al.width ?? .8) * tw / 2; const o2 = corner({ ...o, line: al, _offsetsOnly: true }); if (o2) s += `<polyline points="${o2.map(P).join(" ")}" fill="none" stroke="${C.steel}" stroke-width="5" stroke-dasharray="12 10"/>`; }
    if (o._offsetsOnly) return line;
    s += `<polyline points="${line.map(P).join(" ")}" fill="none" stroke="${C.sky}" stroke-opacity=".35" stroke-width="5"/>`;
    // brake ramp: segment of line from brake.from to brake.to, opacity decreasing (pressure released)
    if (o.brake) { const a = atF(o.brake.from), b = atF(o.brake.to); const n = b - a; const peak = o.brake.peak ?? .15; for (let i = a; i < b; i++) { const f = (i - a) / n; const v = f < peak ? 1 : 1 - (f - peak) / (1 - peak) * (o.brake.trail === false ? 0 : 1); s += `<line x1="${P(line[i]).split(",")[0]}" y1="${P(line[i]).split(",")[1]}" x2="${P(line[i + 1]).split(",")[0]}" y2="${P(line[i + 1]).split(",")[1]}" stroke="${C.blue}" stroke-width="${8 + 10 * v}" stroke-opacity="${(.35 + .65 * v).toFixed(2)}" stroke-linecap="round"/>`; } }
    s += `<polyline points="${line.map(P).join(" ")}" fill="none" stroke="${C.ice}" stroke-width="3" stroke-opacity=".85"/>`;
    for (const m of o.markers || []) {
      const i = named(m.at); const [px, py] = P(line[i]).split(",").map(Number);
      const side = m.side || (px > W / 2 ? -1 : 1);
      s += `<circle cx="${px}" cy="${py}" r="11" fill="${C.night}" stroke="${m.color || C.sky}" stroke-width="4"/>`;
      if (m.label) { const tx = px + side * 26, anchor = side > 0 ? "start" : "end"; s += `<text x="${tx}" y="${py + 7 + (m.dy || 0)}" fill="${m.color || C.ice}" font-family="JBM" font-size="20" letter-spacing="1.5" text-anchor="${anchor}">${esc(m.label)}</text>`; }
    }
    if (o.dirArrow !== false) { const [ax, ay] = P(pts[2]).split(",").map(Number); s += `<path d="M${ax - 14},${ay + 30} L${ax},${ay} L${ax + 14},${ay + 30}" fill="none" stroke="${C.steel}" stroke-width="3"/>`; }
    return s + "</svg>";
  }

  /* brand chrome for any frame: mark top-left, counter top-right, handle bottom, optional demo tag */
  function chrome(el, { w, h, counter = "", handle = "@akki_meister", demo = false, flagAt, pattern, patternOp = .14, markW = 112, pad = 64 }) {
    let s = `<div class="vig"></div><div class="glow"></div><div class="grain"></div>`;
    if (pattern) s = `<div class="pat" style="background-image:url(${pattern});opacity:${patternOp};z-index:0"></div>` + s;
    s += `<div class="wm" style="left:${pad}px;top:${pad - 6}px">${markSvg(markW)}</div>`;
    if (counter) s += `<div class="counter" style="right:${pad}px;top:${pad + 6}px">${esc(counter)}</div>`;
    if (handle) s += `<div class="handle" style="left:${pad}px;bottom:${pad - 16}px">${esc(handle)}</div>`;
    if (demo) s += `<div class="demo" style="right:${pad}px;bottom:${pad - 20}px">${esc(typeof demo === "string" ? demo : "DEMO DATA · NOT A REAL LAP")}</div>`;
    if (flagAt) s += `<svg class="abs" width="${w}" height="${h}" style="left:0;top:0;z-index:44;pointer-events:none">${flag(flagAt[0], flagAt[1], { cols: 11, rows: 4, sq: 16, op: .45 })}</svg>`;
    el.insertAdjacentHTML("beforeend", s);
  }

  const ready = () => document.fonts.ready.then(() => Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((r) => (i.onload = i.onerror = r)))));
  window.AM = { C, K, esc, rich, headline, mark, markSvg, lockupSvg, photo, lean, flag, lineChart, legend, bars, gauge, split, flow, carLoad, corner, chrome, ready, FADES };
})();
