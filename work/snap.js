// screenshot every <section> of the brand board into ../round2/board-<id>.png
const puppeteer = require("C:/Users/admin/Akki-Portfolio-main/brag-output/work/tools/node_modules/puppeteer-core");
const path = require("path");
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true, args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 1 });
  p.on("pageerror", (e) => console.error("PAGE", e.message));
  await p.goto("file:///" + path.resolve(__dirname, "../round2/brand-board.html").replace(/\\/g, "/"), { waitUntil: "load" });
  await p.evaluate(async () => { await document.fonts.ready; });
  const ids = await p.$$eval("section", (s) => s.map((e) => e.id));
  for (const id of ids) {
    const el = await p.$("#" + id);
    await el.screenshot({ path: path.resolve(__dirname, `../round2/board-${id}.png`) });
  }
  console.log("shots", ids.join(", "));
  await b.close();
})();
