// Theme bootstrap. Loaded as a blocking <script> in the <head> of index.html and
// backend/templates/base.html so the theme is applied before first paint.
(function () {
  try {
    var stored = localStorage.getItem("theme");
    var theme = stored === "light" || stored === "dark" ? stored : window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    document.documentElement.dataset.theme = theme;
  } catch {}
})();
