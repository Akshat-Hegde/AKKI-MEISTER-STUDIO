// node shot.js <html> <out.png> [width]  — full-page screenshot, waits for images
const puppeteer = require("C:/Users/admin/Akki-Portfolio-main/brag-output/work/tools/node_modules/puppeteer-core");
const path = require("path");
(async () => {
  const [html, out, w] = process.argv.slice(2);
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true, args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: +(w || 2112), height: 900 });
  await p.goto("file:///" + path.resolve(html).replace(/\\/g, "/"), { waitUntil: "load" });
  await p.evaluate(async () => { await Promise.all([...document.images].map((i) => (i.complete ? 0 : new Promise((r) => (i.onload = i.onerror = r))))); });
  console.log("broken", await p.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).length));
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
