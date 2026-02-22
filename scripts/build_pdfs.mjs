import fs from "fs";
import path from "path";
import { chromium } from "playwright";

function listPages() {
  const dirs = ["docs/pages", "pages"];
  for (const d of dirs) {
    if (fs.existsSync(d)) {
      return fs.readdirSync(d)
        .filter(f => /^page-\d+\.html$/i.test(f))
        .sort((a,b)=>parseInt(a.match(/\d+/)[0]) - parseInt(b.match(/\d+/)[0]))
        .map(f=>path.join(d,f));
    }
  }
  return [];
}

async function waitReady(page) {
  await page.waitForLoadState("domcontentloaded");
  await page.waitForLoadState("networkidle").catch(()=>{});
  await page.evaluate(async ()=>{
    try { if (document.fonts) await document.fonts.ready; } catch {}
    try { if (window.MathJax?.typesetPromise) await window.MathJax.typesetPromise(); } catch {}
  });
}

async function main(){
  const pages = listPages();
  if(!pages.length){
    console.log("❌ no html pages found");
    process.exit(1);
  }

  fs.mkdirSync("pdfs",{recursive:true});

  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport:{width:1240,height:1754}
  });

  const page = await ctx.newPage();

  let ok=0,fail=0;

  for(const file of pages){
    const num=file.match(/page-(\d+)/)[1];
    const abs=path.resolve(file);
    const url="file://"+abs;

    console.log("LOCAL OPEN",url);

    try{
      await page.goto(url,{waitUntil:"domcontentloaded"});
      await waitReady(page);

      const out="pdfs/page-"+num+".pdf";

      await page.pdf({
        path:out,
        format:"A4",
        printBackground:true,
        margin:{top:"10mm",right:"10mm",bottom:"10mm",left:"10mm"}
      });

      console.log("WROTE",out,"size=",fs.statSync(out).size);
      ok++;
    }catch(e){
      console.log("FAILED",file,String(e));
      fail++;
    }
  }

  await browser.close();

  console.log("DONE ok=",ok,"fail=",fail);
  if(ok===0) process.exit(1);
}

main().catch(e=>{
  console.error("FATAL",e);
  process.exit(1);
});
