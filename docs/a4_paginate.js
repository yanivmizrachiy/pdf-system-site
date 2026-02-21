/* A4 paginate engine — PRINT ONLY (safe) */
(function () {
  "use strict";

  function hasPrintParam() {
    try { return (new URL(location.href)).searchParams.get("print") === "1"; }
    catch (e) { return false; }
  }

  function injectPrintCSS() {
    if (document.getElementById("a4-paginate-css")) return;

    var css = `
@media print {
  @page { size: A4; margin: 12mm; }
  html, body { background: #fff !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .no-print { display: none !important; }
  .page { break-after: page; page-break-after: always; }
  .avoid-split, .item, .item-line { break-inside: avoid; page-break-inside: avoid; }
}
`;
    var style = document.createElement("style");
    style.id = "a4-paginate-css";
    style.textContent = css;
    document.head.appendChild(style);
  }

  function markAvoidSplit() {
    // Only for print layout stability
    try {
      var nodes = document.querySelectorAll(".item, .item-line, .eq, .answer-space");
      for (var i = 0; i < nodes.length; i++) nodes[i].classList.add("avoid-split");
    } catch (e) {}
  }

  function activateForPrint() {
    injectPrintCSS();
    markAvoidSplit();
  }

  // Activate when user actually prints
  window.addEventListener("beforeprint", function () {
    activateForPrint();
  });

  // Optional: auto-print flow when ?print=1
  if (hasPrintParam()) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        activateForPrint();
        setTimeout(function () { window.print(); }, 250);
      });
    } else {
      activateForPrint();
      setTimeout(function () { window.print(); }, 250);
    }
  }
})();
