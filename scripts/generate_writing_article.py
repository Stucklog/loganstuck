#!/usr/bin/env python3
"""Render the published writing article from its Markdown and metadata."""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ARTICLE_DIR = ROOT / "content" / "writing" / "Global Health from a Land Cruiser"
OUTPUT = ROOT / "global-health-from-a-land-cruiser.html"
IMAGE_PATTERN = re.compile(r"^!\[(?P<alt>.*)]\((?P<src>.*)\)$")
HEADING_PATTERN = re.compile(r"^(?P<level>#{1,3})\s+(?P<text>.+)$")


def render_markdown(source: str) -> str:
    blocks: list[str] = []

    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "---":
            blocks.append(
                '        <div class="article-break" role="separator" '
                'aria-label="Section break"><span aria-hidden="true">...</span></div>'
            )
            continue

        image_match = IMAGE_PATTERN.match(line)
        if image_match:
            src = image_match.group("src").removeprefix("../../../")
            blocks.append(
                "        <figure class=\"article-figure\">\n"
                f"          <img src=\"{html.escape(src, quote=True)}\" "
                f"alt=\"{html.escape(image_match.group('alt'), quote=True)}\">\n"
                "        </figure>"
            )
            continue

        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            level = len(heading_match.group("level")) + 1
            blocks.append(
                f"        <h{level}>{html.escape(heading_match.group('text'))}</h{level}>"
            )
            continue

        blocks.append(f"        <p>{html.escape(line)}</p>")

    return "\n".join(blocks)


def main() -> None:
    metadata = json.loads((ARTICLE_DIR / "metadata.json").read_text(encoding="utf-8"))
    body = render_markdown((ARTICLE_DIR / "article.md").read_text(encoding="utf-8"))
    title = html.escape(metadata["title"])
    subtitle = html.escape(metadata["subtitle"])
    preview = html.escape(metadata["preview"], quote=True)
    stylesheet = ROOT / "assets" / "css" / "styles.css"
    stylesheet_version = hashlib.sha256(stylesheet.read_bytes()).hexdigest()[:12]

    page = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} | Logan Stuck</title>
    <meta name="description" content="{preview}">
    <link rel="canonical" href="https://loganstuck.com/global-health-from-a-land-cruiser.html">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{preview}">
    <meta property="og:url" content="https://loganstuck.com/global-health-from-a-land-cruiser.html">
    <meta property="og:image" content="https://loganstuck.com/assets/images/global-health-land-cruiser.webp">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="assets/css/styles.css?v={stylesheet_version}">
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header" data-site-header>
      <div class="container header-inner">
        <a class="brand" href="index.html" aria-label="Logan Stuck home">
          <span class="brand-mark">LS</span>
          <span>Logan Stuck</span>
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">
          Menu
        </button>
        <nav class="primary-nav" id="primary-nav" aria-label="Primary navigation">
          <a href="about.html">About</a>
          <a href="resume.html">Resume</a>
          <a href="publications.html">Publications</a>
          <a href="writing.html" aria-current="page">Writing</a>
          <a href="consulting.html">Consulting</a>
          <a class="nav-cta" href="mailto:logan@loganstuck.com">Contact</a>
        </nav>
      </div>
    </header>

    <main id="main">
      <header class="page-hero article-hero">
        <div class="container article-hero-copy">
          <p class="eyebrow">Essay</p>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
      </header>

      <section class="section article-section">
        <article class="container article-prose">
{body}
        </article>
        <div class="container article-footer-link">
          <a class="text-link" href="writing.html">← Back to writing</a>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <div class="container footer-grid">
        <div>
          <a class="brand footer-brand" href="index.html" aria-label="Logan Stuck home">
            <span class="brand-mark">LS</span>
            <span>Logan Stuck</span>
          </a>
          <p>Public health evaluation, epidemiology, and data science.</p>
        </div>
        <div class="footer-links" aria-label="Footer navigation">
          <a href="about.html">About</a>
          <a href="resume.html">Resume</a>
          <a href="publications.html">Publications</a>
          <a href="writing.html">Writing</a>
          <a href="consulting.html">Consulting</a>
        </div>
        <div class="footer-contact">
          <p>Based in the Netherlands. Working internationally.</p>
          <a href="mailto:logan@loganstuck.com">logan@loganstuck.com</a>
        </div>
      </div>
    </footer>
    <script src="assets/js/site.js"></script>
  </body>
</html>
"""

    OUTPUT.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
