/* shared helpers: browser launch, path resolution, ffprobe, logging */
const path = require("path"), fs = require("fs"), { spawnSync } = require("child_process");
const ROOT = path.resolve(__dirname, "../..");
const KIT = path.join(ROOT, "infographics/_kit");
const fileUrl = (p) => require("url").pathToFileURL(path.resolve(p)).href;

/* Playwright first (cloud / any machine with `npm i playwright`), else puppeteer-core with CHROME_PATH (Akki's desktop). */
async function browser(viewport) {
  let b, pw = true;
  try { const { chromium } = require("playwright"); b = await chromium.launch({ args: ["--allow-file-access-from-files", "--hide-scrollbars"] }); }
  catch (e) {
    pw = false;
    const pp = require("puppeteer-core");
    b = await pp.launch({ executablePath: process.env.CHROME_PATH, headless: true, args: ["--allow-file-access-from-files", "--hide-scrollbars"] });
  }
  const p = await b.newPage();
  if (pw) await p.setViewportSize(viewport); else await p.setViewport(viewport);
  p.on("pageerror", (e) => console.error("PAGE ERROR", e.message));
  p.on("console", (m) => { if (m.type() === "error") console.error("PAGE", m.text()); });
  return { b, p };
}

/* resolve a media path from a spec: absolute, relative to the spec file, the repo root, or library/ */
function resolver(specDir) {
  return (p) => {
    if (!p || /^(https?:|file:|data:)/.test(p)) return p;
    for (const base of [specDir, ROOT, path.join(ROOT, "library")]) { const f = path.resolve(base, p); if (fs.existsSync(f)) return f; }
    throw new Error(`media not found: ${p}`);
  };
}
const MEDIA_RE = /\.(jpe?g|png|webp|mp4|mov|m4v|csv|wav|mp3|m4a)$/i;
/* walk the spec and turn media paths into absolute file paths (or file:// URLs for images used in pages) */
function resolveMedia(obj, res, asUrl = true) {
  if (Array.isArray(obj)) return obj.map((v) => resolveMedia(v, res, asUrl));
  if (obj && typeof obj === "object") { const o = {}; for (const k in obj) o[k] = resolveMedia(obj[k], res, asUrl); return o; }
  if (typeof obj === "string" && MEDIA_RE.test(obj) && !/\s/.test(obj.trim().slice(0, 1))) {
    const f = res(obj);
    return asUrl && /\.(jpe?g|png|webp)$/i.test(f) ? fileUrl(f) : f;
  }
  return obj;
}

function ffprobe(f) {
  const r = spawnSync("ffprobe", ["-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:stream_tags=rotate:format=duration", "-of", "json", f], { encoding: "utf8" });
  const j = JSON.parse(r.stdout || "{}");
  const v = (j.streams || []).find((s) => s.codec_type === "video") || {};
  return { duration: +(j.format?.duration || 0), w: v.width, h: v.height, audio: (j.streams || []).some((s) => s.codec_type === "audio") };
}
function run(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, { stdio: opts.quiet === false ? "inherit" : ["ignore", "ignore", "pipe"], encoding: "utf8", maxBuffer: 1 << 26 });
  if (r.status !== 0) throw new Error(`${cmd} failed (${r.status}): ${(r.stderr || "").slice(-1500)}`);
  return r;
}
const slugify = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60);

module.exports = { ROOT, KIT, fileUrl, browser, resolver, resolveMedia, ffprobe, run, slugify };
