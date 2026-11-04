// screenshot every [data-snap] in AKKI-MEISTER-FINAL/launch-kit.html into folders by prefix
const puppeteer = require("C:/Users/admin/Akki-Portfolio-main/brag-output/work/tools/node_modules/puppeteer-core");
const fs = require("fs");
const R = "C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/AKKI-MEISTER-FINAL/";
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true, args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: 1700, height: 2000 });
  p.on("pageerror", (e) => console.log("ERR", e.message));
  await p.goto("file:///" + R + "launch-kit.html", { waitUntil: "load" });
  await p.evaluate(async () => { await document.fonts.ready; });
  const names = await p.$$eval("[data-snap]", (s) => s.map((e) => e.dataset.snap));
  for (const n of names) {
    const dir = R + (n.startsWith("post") ? "posts/" : n.startsWith("story") ? "story/" : "patterns/");
    fs.mkdirSync(dir, { recursive: true });
    await (await p.$(`[data-snap="${n}"]`)).screenshot({ path: dir + n + ".png" });
  }
  console.log(names.join(" "));
  await b.close();
})();
