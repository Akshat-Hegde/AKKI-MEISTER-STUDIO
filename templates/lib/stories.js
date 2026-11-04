/* story set renderer: spec.stories -> story-01.png … (1080×1920). Zones marked "STICKER" are where the IG poll /
   question sticker goes; set "zoneLabel": "" to hide the label, the corner brackets stay as a designed frame. */
const path = require("path"), fs = require("fs");
const { ROOT, fileUrl, browser } = require("./common");

async function renderStories(spec, outDir) {
  fs.mkdirSync(outDir, { recursive: true });
  const { b, p } = await browser({ width: 1200, height: 2000 });
  await p.goto(fileUrl(path.join(ROOT, "templates/stories/stories.html")), { waitUntil: "load" });
  await p.evaluate((s) => window.build(s), spec);
  const warnings = await p.evaluate(() => window.audit());
  const files = [];
  for (let i = 1; i <= spec.stories.length; i++) {
    const s = spec.stories[i - 1];
    const f = path.join(outDir, `story-${String(i).padStart(2, "0")}-${s.type}.png`);
    await (await p.$("#story-" + i)).screenshot({ path: f });
    files.push(f);
  }
  await b.close();
  return { files, warnings };
}
module.exports = { renderStories };
