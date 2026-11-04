const puppeteer=require('C:/Users/admin/Akki-Portfolio-main/brag-output/work/tools/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--allow-file-access-from-files']});
const p=await b.newPage();await p.setViewport({width:1100,height:1400});
for(const f of ['p13','breakdown']){await p.goto('file:///C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/'+f+'.html',{waitUntil:'load'});await p.evaluate(async()=>{await document.fonts.ready});
for(const el of await p.$$('section')){const n=await el.evaluate(e=>e.dataset.snap);await el.screenshot({path:n+'.png'});}}
await b.close();})();
