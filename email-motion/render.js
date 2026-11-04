// node render.js stills t1 t2 … | events | video   (env FROM/TO/OUT for partial video)
const puppeteer = require("C:/Users/admin/Akki-Portfolio-main/brag-output/work/tools/node_modules/puppeteer-core");
const path = require("path"), fs = require("fs"), { spawn } = require("child_process");
const FPS = 30;
(async () => {
  const [mode, ...times] = process.argv.slice(2);
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true, args: ["--allow-file-access-from-files", "--hide-scrollbars"] });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920 });
  p.on("pageerror", (e) => console.error("PAGE", e.message));
  await p.goto("file:///" + path.resolve(__dirname, "comp.html").replace(/\\/g, "/"), { waitUntil: "load" });
  await p.evaluate(() => window.ready);
  const END = await p.evaluate(() => window.END);
  if (mode === "events") {
    fs.writeFileSync(path.resolve(__dirname, "events.json"), JSON.stringify(await p.evaluate(() => window.EVENTS)));
    console.log("events ok");
  } else if (mode === "stills") {
    fs.mkdirSync(path.resolve(__dirname, "stills"), { recursive: true });
    for (const t of times) { await p.evaluate((t) => window.render(t), +t); await p.screenshot({ path: path.resolve(__dirname, `stills/t_${t}.png`) }); }
  } else {
    const F0 = Math.round((+process.env.FROM || 0) * FPS), F1 = process.env.TO ? Math.round(+process.env.TO * FPS) : END * FPS;
    const ff = spawn("ffmpeg", ["-y", "-f", "image2pipe", "-framerate", "30", "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", path.resolve(__dirname, process.env.OUT || "email-open.mp4")], { stdio: ["pipe", "ignore", "ignore"] });
    for (let f = F0; f < F1; f++) {
      await p.evaluate((t) => window.render(t), f / FPS);
      const buf = await p.screenshot({ type: "png" });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
      if (f % 90 === 0) console.log("frame", f);
    }
    ff.stdin.end(); await new Promise((r) => ff.on("close", r));
  }
  await b.close();
})();
