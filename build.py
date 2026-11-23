#!/usr/bin/env python3
"""Build the standalone site from src/page.html.

The source doubles as a Claude Artifact, where the host supplies <head> and a CSS
reset. A real website needs its own: doctype, meta, social cards, favicon, and a
theme toggle (an artifact gets its theme from the viewer's host instead).

  python3 build.py   ->  public/index.html
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "src" / "page.html").read_text(encoding="utf-8")

SITE  = "https://zaidmarwat.com"
DESC  = ("Zaid Marwat builds and repairs the layer other people stand on: automation at "
         "Texas Instruments, test infrastructure at Visa, a submitted container-ancestry fix for "
         "Podman, and co-invention of a patent for a real-time thermal detection system.")

# Split the artifact source into head-safe and body parts at the end of <style>.
cut = src.index("</style>") + len("</style>")
head_part, body_part = src[:cut], src[cut:]

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%F0%9F%90%A7%3C/text%3E%3C/svg%3E"
)

TOGGLE_CSS = """
<style>
.theme-toggle {
  position: fixed; top: 16px; right: 16px; z-index: 20;
  width: 38px; height: 38px; display: grid; place-items: center;
  background: var(--bg-soft); color: var(--ink-soft);
  border: 1px solid var(--line); border-radius: 8px; cursor: pointer;
  font-family: "IBM Plex Mono", monospace; font-size: 15px; line-height: 1;
  transition: color .12s ease, border-color .12s ease;
}
.theme-toggle:hover { color: var(--accent); border-color: var(--accent); }
@media (max-width: 640px) { .theme-toggle { top: 10px; right: 10px; } }
@media print { .theme-toggle { display: none; } }
</style>
"""

TOGGLE_HTML = """
<button class="theme-toggle" id="themeToggle" type="button"
        aria-label="Switch between light and dark" title="Switch theme">◐</button>
<script>
(function () {
  var root = document.documentElement, btn = document.getElementById("themeToggle");
  var saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}
  if (saved === "dark" || saved === "light") root.setAttribute("data-theme", saved);
  btn.addEventListener("click", function () {
    var dark = getComputedStyle(root).getPropertyValue("--bg").trim().indexOf("#28") === 0;
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) {}
  });
})();
</script>
"""

HEAD_EXTRA = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{DESC}">
<meta name="author" content="Zaid Marwat">
<meta name="theme-color" content="#fbf1c7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#282828" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{SITE}/">
<link rel="icon" href="{FAVICON}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Zaid Marwat">
<meta property="og:title" content="Zaid Marwat">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Zaid Marwat">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}/og-image.png">
"""

out = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n"
    + HEAD_EXTRA
    + head_part
    + TOGGLE_CSS
    + "</head>\n<body>\n"
    + TOGGLE_HTML
    + body_part
    + "\n</body>\n</html>\n"
)

(ROOT / "public").mkdir(exist_ok=True)
(ROOT / "public" / "index.html").write_text(out, encoding="utf-8")

# sanity checks
problems = []
for tag in ("<!doctype html>", "<html lang=\"en\">", "</head>", "</body>", "</html>"):
    if tag not in out: problems.append("missing " + tag)
if out.count("<style>") != out.count("</style>"): problems.append("unbalanced <style>")
if out.count("<script>") != out.count("</script>"): problems.append("unbalanced <script>")
if problems:
    print("BUILD PROBLEMS: " + "; ".join(problems), file=sys.stderr); sys.exit(1)

print(f"built public/index.html  ({len(out)/1024:.1f} KB)")
