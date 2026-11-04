// node outreach/media-kit/render.js
//  -> slide-01..04.png (1080x1350) and AKKI-MEISTER-media-kit.pdf (1 page, A4)
// Uses Playwright if installed; otherwise puppeteer-core with CHROME_PATH set, e.g.
//   set CHROME_PATH=C:/Program Files/Google/Chrome/Application/chrome.exe
const path = require("path");
const url = (f) => "file://" + path.resolve(__dirname, f).replace(/\\/g, "/");
async function browser() {
  try { const { chromium } = require("playwright"); return { b: await chromium.launch({ args: ["--allow-file-access-from-files"] }), pw: true }; }
  catch (e) {
    const pp = require("puppeteer-core");
    return { b: await pp.launch({ executablePath: process.env.CHROME_PATH, headless: true, args: ["--allow-file-access-from-files"] }), pw: false };
  }
}
(async () => {
  const { b, pw } = await browser();
  const p = await b.newPage();
  if (pw) await p.setViewportSize({ width: 2400, height: 3000 }); else await p.setViewport({ width: 2400, height: 3000 });
  p.on("pageerror", (e) => console.error("PAGE", e.message));
  await p.goto(url("slides.html"), { waitUntil: "load" });
  await p.evaluate(() => window.ready);
  for (let i = 1; i <= 4; i++) await (await p.$("#s" + i)).screenshot({ path: path.resolve(__dirname, `slide-0${i}.png`) });
  await p.goto(url("one-pager.html"), { waitUntil: "load" });
  await p.evaluate(() => window.ready);
  await p.pdf({ path: path.resolve(__dirname, "AKKI-MEISTER-media-kit.pdf"), width: "210mm", height: "297mm", printBackground: true, pageRanges: "1" });
  if (pw) await p.setViewportSize({ width: 1240, height: 1754 }); else await p.setViewport({ width: 1240, height: 1754 });
  await (await p.$(".page")).screenshot({ path: path.resolve(__dirname, "one-pager-preview.png") });
  await b.close();
  console.log("ok");
})();
