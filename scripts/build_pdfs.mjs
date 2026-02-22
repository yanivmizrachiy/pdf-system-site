import fs from "fs";
import path from "path";
import { chromium } from "playwright";

function listPages() {
  // prefer docs/pages (source-of-truth), fallback pages/
  const candidates = ["docs/pages", "pages"];
  for (const dir of candidates) {
    if (fs.existsSync(dir)) {
      const files = fs.readdirSync(dir)
        .filter(f => /^page-\d+\.html$/i.test(f))
        .map(f => ({ dir, file: f }))
        .sort((a,b) => {
          const na = parseInt(a.file.match(/\d+/)[0], 10);
          const nb = parseInt(b.file.match(/\d+/)[0], 10);
          return na - nb;
        });
      if (files.length) return files;
    }
  }
  return [];
}

function pageNum(filename) {
  const m = filename.match(/page-(\d+)\.html/i);
  return m ? parseInt(m[1], 10) : null;
}

async function safeWaitReady(page) {
  // 1) wait DOM + network settle
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(()=>{});
  await page.waitForLoadState("networkidle", { timeout: 60000 }).catch(()=>{});

  // 2) fonts (important for stable PDF)
  await page.evaluate(async () => {
    try {
      if (document.fonts && document.fonts.ready) await document.fonts.ready;
    } catch {}
  }).catch(()=>{});

  // 3) MathJax (if exists)
  await page.evaluate(async () => {
    try {
      // if MathJax v3 present
      // @ts-ignore
      if (window.MathJax && window.MathJax.typesetPromise) {
        // @ts-ignore
        await window.MathJax.typesetPromise();
      }
    } catch {}
  }).catch(()=>{});

  // 4) minimal render marker: accept any of these
  const selectors = [".page", ".item", "mjx-container", "svg", "body"];
  for (const sel of selectors) {
    try {
      await page.waitForSelector(sel, { state: "attached", timeout: 12000 });
      return;
    } catch {}
  }
}

async function main() {
  const SITE = "https://yanivmizrachiy.github.io/pdf-system-site";
  const pages = listPages();
  if (!pages.length) {
    console.log("❌ No pages found under docs/pages or pages/");
    process.exit(1);
  }

  fs.mkdirSync("docs/pdfs", { recursive: true });

  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    // A4-ish viewport for stable layout; PDF is true A4 anyway
    viewport: { width: 1240, height: 1754 },
    deviceScaleFactor: 1,
  });

  const page = await ctx.newPage();

  let ok = 0, fail = 0;

  for (const p of pages) {
    const n = pageNum(p.file);
    const url = `${SITE}/pages/${p.file}?fresh=${Date.now()}`;
    const out = `docs/pdfs/page-${n}.pdf`;

    console.log(`OPEN ${url}`);
    try {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
      await safeWaitReady(page);

      await page.pdf({
        path: out,
        format: "A4",
        printBackground: true,
        margin: { top: "10mm", right: "10mm", bottom: "10mm", left: "10mm" },
      });

      const size = fs.statSync(out).size;
      console.log("WROTE", out, "size=", size);
      ok++;
    } catch (e) {
      console.log("⚠️ PDF FAILED for", p.file, "->", String(e?.message || e));
      fail++;
      // keep going (do not fail whole build)
    }
  }

  await browser.close();

  console.log(`DONE pdf build: ok=${ok} fail=${fail} total=${pages.length}`);
  // do NOT exit 1 unless nothing succeeded
  if (ok === 0) process.exit(1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
