// screenshot every [data-snap] element of ../round4/system.html into ../round4/out/<name>.png
const puppeteer = require("C:/Users/admin/Akki-Portfolio-main/brag-output/work/tools/node_modules/puppeteer-core");
const path = require("path");
const fs = require("fs");
(async () => {
  const out = path.resolve(__dirname, "../round4/out");
  fs.mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true, args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: 1600, height: 1000 });
  p.on("pageerror", (e) => console.error("PAGE", e.message));
  await p.goto("file:///" + path.resolve(__dirname, "../round4/system.html").replace(/\\/g, "/"), { waitUntil: "load", timeout: 120000 });
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((i) => (i.complete ? 0 : new Promise((r) => (i.onload = i.onerror = r))))); });
  const names = await p.$$eval("body > [data-snap]", (s) => s.map((e) => e.dataset.snap));
  for (const n of names) {
    const el = await p.$(`body > [data-snap="${n}"]`);
    await el.screenshot({ path: path.join(out, n + ".png") });
  }
  console.log("shots:", names.join(", "));
  await b.close();
})();
