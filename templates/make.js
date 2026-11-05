#!/usr/bin/env node
/* AKKI MEISTER template runner — one command for every signature-series template.

     node templates/make.js <spec.json> [--out <dir>] [--stills 1.5,8,20] [--no-video]

   The spec's "template" field picks the template:
     apex-notes        APEX NOTES carousel (1080×1350 PNGs)
     debrief-carousel  THE DEBRIEF two-lap comparison carousel (PNGs, from two lap CSVs)
     debrief-reel      THE DEBRIEF reel (1080×1920 MP4 from a screen recording [+ two lap CSVs])
     hotlap            Hotlap / onboard reel overlay (1080×1920 MP4)
     sim-to-tarmac     SIM TO TARMAC kinetic reel (1080×1920 MP4)
     explainer         EXPLAINER reel: Akki teaching one idea, 30–40 s (1080×1920 MP4)
     stories           Story set: announcement / result / quote / question (1080×1920 PNGs)

   Output: spec.out, else posts/<spec.date>-<slug>/ when spec.date is set, else next to the spec.
   Media paths in the spec may be relative to the spec file, the repo root, or library/.  See templates/README.md. */
const path = require("path"), fs = require("fs");
const { ROOT, resolver, resolveMedia, slugify } = require("./lib/common");

(async () => {
  const args = process.argv.slice(2);
  const specPath = args.find((a) => !a.startsWith("--") && /\.json$/i.test(a));
  if (!specPath) { console.log(fs.readFileSync(__filename, "utf8").split("*/")[0]); process.exit(1); }
  const opt = (k) => { const i = args.indexOf("--" + k); return i >= 0 ? (args[i + 1] && !args[i + 1].startsWith("--") ? args[i + 1] : true) : undefined; };
  const raw = JSON.parse(fs.readFileSync(specPath, "utf8"));
  const specDir = path.dirname(path.resolve(specPath));
  const res = resolver(specDir);
  const outDir = path.resolve(ROOT, opt("out") || raw.out || (raw.date ? `posts/${raw.date}-${slugify(raw.slug || raw.title || raw.template)}` : specDir));
  const ctx = { raw, res, specDir, outDir, stills: opt("stills") ? String(opt("stills")).split(",").map(Number) : null, noVideo: !!opt("no-video") };
  fs.mkdirSync(outDir, { recursive: true });
  const t0 = Date.now();
  let result;
  switch (raw.template) {
    case "apex-notes": {
      const { renderCarousel } = require("./lib/carousel");
      result = await renderCarousel(resolveMedia(raw, res), outDir);
      break;
    }
    case "debrief-carousel": {
      const { debriefSlides } = require("./lib/telemetry");
      const { renderCarousel } = require("./lib/carousel");
      const spec = debriefSlides(raw, res);
      fs.writeFileSync(path.join(outDir, "debrief-numbers.json"), JSON.stringify(spec._numbers, null, 1));
      result = await renderCarousel(resolveMedia(spec, res), outDir);
      break;
    }
    case "stories": {
      const { renderStories } = require("./lib/stories");
      result = await renderStories(resolveMedia(raw, res), outDir);
      break;
    }
    case "explainer": {
      const { renderExplainer } = require("./lib/explainer");
      result = await renderExplainer(ctx);
      break;
    }
    case "hotlap": case "debrief-reel": case "sim-to-tarmac": {
      const { renderReel } = require("./lib/reel");
      result = await renderReel(ctx);
      break;
    }
    default: throw new Error(`unknown template "${raw.template}"`);
  }
  if (raw.caption) fs.writeFileSync(path.join(outDir, "caption.md"), raw.caption.trim() + "\n");
  for (const w of result.warnings || []) console.warn("⚠ " + w);
  console.log(`done in ${((Date.now() - t0) / 1000).toFixed(0)} s → ${path.relative(ROOT, outDir)}`);
  for (const f of result.files) console.log("  " + path.relative(ROOT, f));
})().catch((e) => { console.error(e.stack || e); process.exit(1); });
