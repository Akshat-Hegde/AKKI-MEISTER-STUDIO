// node shoot.js  -> story-01-debrief.png, story-02-thank-you.png (1080x1920)
const puppeteer = require("C:/Users/admin/Akki-Portfolio-main/brag-output/work/tools/node_modules/puppeteer-core");
const path = require("path");
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true, args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: 2400, height: 2000 });
  p.on("pageerror", (e) => console.error("PAGE", e.message));
  await p.goto("file:///" + path.resolve(__dirname, "stories.html").replace(/\\/g, "/"), { waitUntil: "load" });
  await p.evaluate(() => window.ready);
  for (const [id, name] of [["#s1", "story-01-debrief.png"], ["#s2", "story-02-thank-you.png"]]) {
    await (await p.$(id)).screenshot({ path: path.resolve(__dirname, name) });
  }
  await b.close();
  console.log("ok");
})();
