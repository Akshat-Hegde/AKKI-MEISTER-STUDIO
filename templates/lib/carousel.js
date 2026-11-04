/* renders a carousel spec (APEX NOTES or a DEBRIEF carousel already converted to slides) to slide-01.png … */
const path = require("path"), fs = require("fs");
const { KIT, fileUrl, browser } = require("./common");

async function renderCarousel(spec, outDir) {
  fs.mkdirSync(outDir, { recursive: true });
  const { b, p } = await browser({ width: 1200, height: 1500 });
  await p.goto(fileUrl(path.join(KIT, "carousel.html")), { waitUntil: "load" });
  await p.evaluate((s) => window.build(s), spec);
  const warnings = await p.evaluate(() => window.audit());
  const files = [];
  for (let i = 1; i <= spec.slides.length; i++) {
    const f = path.join(outDir, `slide-${String(i).padStart(2, "0")}.png`);
    await (await p.$("#slide-" + i)).screenshot({ path: f });
    files.push(f);
  }
  await b.close();
  return { files, warnings };
}
module.exports = { renderCarousel };
