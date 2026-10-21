#!/usr/bin/env python3
"""Render a markdown guide into a site article page.

The markdown file is the canonical text; the HTML page is derived from it and
is regenerated, never hand-edited. The page uses the same shell as every other
article (site-header, site-nav, sidebar, footer web components) and turns each
``##`` section into one panel, so a rendered guide looks like the rest of the
site rather than a wall of prose.

Usage:
    tools/build_article.py SOURCE.md docs/SLUG.html \\
        [--badge ai|approved|human] [--emoji X] [--source-url URL]

The page title comes from the markdown's first ``#`` heading. Text before the
first ``##`` becomes the intro panel. Requires the ``markdown`` package.
"""

import argparse
import html
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover - environment check
    sys.exit("python-markdown is required: pip install markdown")

MD_EXTENSIONS = ["fenced_code", "tables", "sane_lists", "smarty"]

PAGE = """<!DOCTYPE html>
<!-- GENERATED from {source} by tools/build_article.py. Edit the markdown, not this file. -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Valkey PR Watchtower</title>
  <link rel="stylesheet" href="style.css">
  <script src="components.js" defer></script>
  <style>
    .article ol {{ margin: 6px 0 6px 22px; font-size: 0.9em; }}
    .article ul ul, .article ol ul {{ margin-top: 3px; margin-bottom: 3px; }}
    .article pre {{ background: var(--bg2); border: 1px solid var(--border); padding: 8px;
                    overflow-x: auto; font-size: 0.85em; }}
    .article pre code {{ background: none; border: none; padding: 0; }}
    .article li > p {{ margin: 0; }}
  </style>
</head>
<body>
<div class="page-wrap">

  <site-header></site-header>
  <site-nav></site-nav>

  <div class="grid">
  <main class="article">

{panels}
  </main>
  <site-sidebar></site-sidebar>
  </div>

  <site-footer></site-footer>

</div>
</body>
</html>
"""

PANEL = """  <div class="panel" style="margin-bottom:12px;">
    <div class="panel-header">
      <span>{heading}</span>
      <attr-badge type="{badge}"></attr-badge>
    </div>
    <div class="panel-body">
{body}
    </div>
  </div>
"""


def split_sections(text):
    """Return (title, intro, [(heading, body), ...]) from markdown text."""
    lines = text.splitlines()
    title = None
    intro, sections = [], []
    current = None
    in_fence = False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and title is None and line.startswith("# "):
            title = line[2:].strip()
            continue
        if not in_fence and line.startswith("## "):
            current = (line[3:].strip(), [])
            sections.append(current)
            continue
        (current[1] if current else intro).append(line)
    if title is None:
        sys.exit("markdown needs a top-level '# Title' heading")
    return title, "\n".join(intro).strip(), [(h, "\n".join(b).strip()) for h, b in sections]


def render(md_text, badge, emoji, source_url):
    title, intro, sections = split_sections(md_text)
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    def body(text):
        md.reset()
        rendered = md.convert(text)
        return "\n".join("      " + ln for ln in rendered.splitlines())

    heading = f"{emoji} {html.escape(title)}" if emoji else html.escape(title)
    intro_html = body(intro) if intro else ""
    if source_url:
        intro_html += (
            '\n      <p class="muted" style="font-size:0.82em; margin-top:10px;">'
            f'Canonical text and revision history: <a href="{html.escape(source_url)}" '
            'target="_blank" rel="noopener noreferrer">markdown source on GitHub ↗</a>. '
            "This page is generated from it.</p>"
        )
    panels = [PANEL.format(heading=heading, badge=badge, body=intro_html)]
    for h, b in sections:
        panels.append(PANEL.format(heading=html.escape(h), badge=badge, body=body(b)))
    return PAGE.format(
        source=html.escape(source_url or "markdown"),
        title=html.escape(title),
        panels="\n".join(panels),
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", type=Path, help="markdown file (canonical text)")
    ap.add_argument("output", type=Path, help="HTML page to write under docs/")
    ap.add_argument("--badge", default="approved", choices=["ai", "approved", "human"])
    ap.add_argument("--emoji", default="", help="emoji shown before the title")
    ap.add_argument("--source-url", default="", help="link to the markdown on GitHub")
    args = ap.parse_args(argv)

    page = render(args.source.read_text(encoding="utf-8"), args.badge, args.emoji, args.source_url)
    args.output.write_text(page, encoding="utf-8")
    panels = len(re.findall(r'class="panel"', page))
    print(f"wrote {args.output} ({panels} panels)")


if __name__ == "__main__":
    main()
