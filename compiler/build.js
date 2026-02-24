const fs = require("fs");
const path = require("path");

const config = JSON.parse(
  fs.readFileSync(path.join(__dirname, "..", "layout", "layout.config.json"), "utf8")
);

const contentDir = path.join(__dirname, "..", "content");
const outputDir = path.join(__dirname, "..", "pages");

if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

const files = fs.readdirSync(contentDir).filter(f => f.endsWith(".json"));

files.forEach(file => {
  const data = JSON.parse(
    fs.readFileSync(path.join(contentDir, file), "utf8")
  );

  let body = "";

  data.blocks.forEach(block => {
    if (block.type === "heading") {
      body += `<h2>${block.text}</h2>\n`;
    }
    if (block.type === "question") {
      body += `<div class="question">\\(${block.math}\\)</div>\n`;
    }
  });

  const html = `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<title>${data.title}</title>
<link rel="stylesheet" href="../style.css">
<script>
window.MathJax = { tex: { inlineMath: [['\\\\(','\\\\)']] } };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
<h1>${data.title}</h1>
${body}
</body>
</html>`;

  const outputFile = file.replace(".json", ".html");
  fs.writeFileSync(path.join(outputDir, outputFile), html);
  console.log("Built:", outputFile);
});
