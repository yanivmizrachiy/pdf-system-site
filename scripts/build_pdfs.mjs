import { chromium } from "playwright";
import fs from "fs";
import path from "path";

const BASE_URL = "https://yanivmizrachiy.github.io/pdf-system-site";
const OUT_DIR = path.join("docs", "pdfs");
const PAGES = [1,2,3];

function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive:true });

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1240, height: 1754 } // A4 ratio
  });
  const page = await context.newPage();

  for(const n of PAGES){
    const url = `${BASE_URL}/pages/page-${n}.html?fresh=${Date.now()}`;
    console.log("OPEN", url);

    await page.goto(url, { waitUntil:"networkidle" });
    await sleep(500);

    // חכה שיש באמת תרגילים בדף
    await page.waitForSelector(".item", { timeout:10000 });

    // חכה לפונטים
    await page.evaluate(async ()=>{
      if(document.fonts?.ready){
        await document.fonts.ready;
      }
    });

    await sleep(300);

    const out = path.join(OUT_DIR, `page-${n}.pdf`);

    await page.pdf({
      path: out,
      format: "A4",
      printBackground: true,
      margin: { top:"10mm", bottom:"10mm", left:"10mm", right:"10mm" }
    });

    const size = fs.statSync(out).size;
    console.log("WROTE", out, "size=", size);
  }

  await browser.close();
  console.log("DONE");
})();
