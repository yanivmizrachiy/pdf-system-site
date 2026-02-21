import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const pagesDir = path.resolve(__dirname, "../docs/pages");
const outDir = path.resolve(__dirname, "../docs/pdfs");

if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const files = fs.readdirSync(pagesDir).filter(f => f.startsWith("page-") && f.endsWith(".html"));

const browser = await chromium.launch();
const context = await browser.newContext();
for (const file of files) {
  const page = await context.newPage();
  const filePath = "file://" + path.join(pagesDir, file);
  await page.goto(filePath, { waitUntil: "networkidle" });
  const pdfName = file.replace(".html", ".pdf");
  const pdfPath = path.join(outDir, pdfName);
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    margin: { top: "12mm", bottom: "12mm", left: "12mm", right: "12mm" }
  });
  console.log("Generated:", pdfName);
  await page.close();
}
await browser.close();
