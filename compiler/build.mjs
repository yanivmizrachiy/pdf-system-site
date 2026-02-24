import fs from "fs";
import path from "path";

const root = process.cwd();
const contentDir = path.join(root, "content");
const pagesDir = path.join(root, "pages");

if (!fs.existsSync(contentDir)) fs.mkdirSync(contentDir, { recursive: true });
if (!fs.existsSync(pagesDir)) fs.mkdirSync(pagesDir, { recursive: true });

// keep only non-generated pages
for (const f of fs.readdirSync(pagesDir)) {
  if (/^page-\d+\.html$/i.test(f)) fs.unlinkSync(path.join(pagesDir, f));
}

const files = fs.readdirSync(contentDir).filter(f => f.endsWith(".json")).sort();

function esc(s = "") {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
function pad3(n) { return String(n).padStart(3, "0"); }

let index = 1;

for (const file of files) {
  const data = JSON.parse(fs.readFileSync(path.join(contentDir, file), "utf8"));
  const title = esc(data.title || file.replace(/\.json$/i, ""));

  let body = "";
  for (const b of (data.blocks || [])) {
    if (b.type === "heading") {
      body += `<h2>${esc(b.text || "")}</h2>\n`;
    } else if (b.type === "question") {
      body += `<div class="question">\\(${String(b.math || "")}\\)</div>\n`;
    } else if (b.type === "text") {
      body += `<p>${esc(b.text || "")}</p>\n`;
    }
  }

  const html =
`<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
<link rel="stylesheet" href="../style.css">
<script>
window.MathJax = { tex: { inlineMath: [["\\\\(","\\\\)"]] } };
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
<h1>${title}</h1>
${body}
</body>
</html>`;

  const outName = `page-${pad3(index)}.html`;
  fs.writeFileSync(path.join(pagesDir, outName), html, "utf8");
  console.log("Built:", outName);
  index++;
}

if (files.length === 0) {
  console.log("WARN: no content/*.json found (generator produced 0 pages).");
}
