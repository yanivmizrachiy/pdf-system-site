import { chromium } from "playwright";
import fs from "fs";
import path from "path";

const BASE_URL = process.env.BASE_URL || "https://yanivmizrachiy.github.io/pdf-system-site";
const OUT_DIR = path.join("docs", "pdfs");
const PAGES = [1, 2, 3];

function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

async function waitForMathJaxAndFonts(page) {
  // fonts
  await page.evaluate(async () => {
    try {
      if (document.fonts && document.fonts.ready) await document.fonts.ready;
    } catch (e) {}
  });

  // MathJax (if exists)
  await page.evaluate(async () => {
    try {
      const mj = window.MathJax;
      if (mj && typeof mj.typesetPromise === "function") {
        await mj.typesetPromise();
      }
    } catch (e) {}
  });
}

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1200, height: 1600 },
    deviceScaleFactor: 2
  });

  // Important: render like screen (your layout is screen-first), then PDF
  await page.emulateMedia({ media: "screen" });

  for (const n of PAGES) {
    const url = `${BASE_URL}/pages/page-${n}.html?fresh=${Date.now()}`;
    console.log(`OPEN ${url}`);

    await page.goto(url, { waitUntil: "domcontentloaded" });
    await sleep(300);

    await waitForMathJaxAndFonts(page);
    await sleep(300);

    const outPath = path.join(OUT_DIR, `page-${n}.pdf`);
    await page.pdf({
      path: outPath,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: "0mm", right: "0mm", bottom: "0mm", left: "0mm" }
    });

    const st = fs.statSync(outPath);
    console.log(`WROTE ${outPath} size=${st.size}`);
  }

  await browser.close();
  console.log("DONE");
})();
