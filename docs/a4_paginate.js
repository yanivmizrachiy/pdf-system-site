/* print-first: A4 helper + auto-print when ?print=1 */
(function () {
  function addClass(el, cls) { if (el && el.classList) el.classList.add(cls); }
  function markAvoidSplit() {
    var selectors = ["table","img","pre","code","blockquote","figure",".ex",".question",".problem",".math",".MathJax",".mjx-container","svg","canvas",".no-split"];
    var list = document.querySelectorAll(selectors.join(","));
    for (var i = 0; i < list.length; i++) addClass(list[i], "a4-avoid-split");
  }
  function injectCSS() {
    var css = "@media print{.a4-avoid-split{break-inside:avoid!important;page-break-inside:avoid!important}.a4-page-break-before{break-before:page!important;page-break-before:always!important}}";
    var style = document.createElement("style");
    style.setAttribute("data-a4-paginate", "1");
    style.textContent = css;
    document.head.appendChild(style);
  }
  function autoPrintIfRequested() {
    try { var url = new URL(window.location.href); if (url.searchParams.get("print")==="1") setTimeout(function(){window.print();}, 250); } catch(e){}
  }
  function init(){ injectCSS(); markAvoidSplit(); autoPrintIfRequested(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
