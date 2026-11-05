/* node outreach/event-pitch/render.js → event-pitch.pdf (A4) + event-pitch.png (2×) */
const path = require("path"), { browser, fileUrl } = require("../../templates/lib/common");
(async () => {
  const { b, p } = await browser({ width: 794, height: 1123 });
  await p.goto(fileUrl(path.join(__dirname, "pitch.html")), { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, "event-pitch.pdf"), width: "794px", height: "1123px", printBackground: true, pageRanges: "1" });
  const ctx = await b.newContext({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  const q = await ctx.newPage(); await q.goto(fileUrl(path.join(__dirname, "pitch.html")), { waitUntil: "load" }); await q.evaluate(() => document.fonts.ready);
  await q.screenshot({ path: path.join(__dirname, "event-pitch.png") });
  await b.close(); console.log("event-pitch.pdf + event-pitch.png written");
})().catch((e) => { console.error(e); process.exit(1); });
