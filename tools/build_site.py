#!/usr/bin/env python3
"""Assemble the publishable site into one output directory.

Every page has exactly one canonical source, chosen by which file exists:

* ``docs/<slug>.html``  -- hand-written HTML, copied as-is.
* ``guides/<slug>.md``  -- markdown, rendered into ``<slug>.html`` here.

A slug with both is an error, so neither copy can silently shadow the other.
Rendered pages are never committed; the deploy workflow runs this script and
publishes the output directory, and a local preview serves the same directory.

Usage:
    tools/build_site.py [--out _site]

A rendered page uses the same shell as every hand-written article (site-header,
site-nav, sidebar, footer web components) and turns each ``##`` section into one
panel. The page title comes from the markdown's first ``#`` heading; text before
the first ``##`` becomes the intro panel. Emoji and attribution badge come from
the page's entry in ``docs/articles.json``, which every page must have.
Requires the ``markdown`` package.
"""

import argparse
import html
import json
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover - environment check
    sys.exit("python-markdown is required: pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
GUIDES = ROOT / "guides"
MANIFEST = DOCS / "articles.json"
SOURCE_URL_BASE = "https://github.com/valkey-rainfall/valkey-pr-watchtower/blob/main/"

MD_EXTENSIONS = ["fenced_code", "tables", "sane_lists", "smarty"]

PAGE = """<!DOCTYPE html>
<!-- GENERATED from {source} by tools/build_site.py. Edit the markdown, not this file. -->
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


class BuildError(Exception):
    """A source-layout problem the author has to fix; reported without a traceback."""


def split_sections(text):
    """Return (title, intro, [(heading, body), ...]) from markdown text."""
    title = None
    intro, sections = [], []
    current = None
    in_fence = False
    for line in text.splitlines():
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
        raise BuildError("markdown needs a top-level '# Title' heading")
    return title, "\n".join(intro).strip(), [(h, "\n".join(b).strip()) for h, b in sections]


def render(md_text, badge, emoji, source_url):
    """Render one markdown document into a full article page."""
    title, intro, sections = split_sections(md_text)
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    def body(text):
        md.reset()
        rendered = md.convert(text)
        return "\n".join("      " + ln for ln in rendered.splitlines())

    heading = f"{emoji} {html.escape(title)}" if emoji else html.escape(title)
    intro_html = body(intro) if intro else ""
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
        source=html.escape(source_url),
        title=html.escape(title),
        panels="\n".join(panels),
    )


def load_manifest():
    """Return {slug.html: entry} for every article in docs/articles.json."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {entry["slug"]: entry for entry in data["articles"]}


def check_sources(manifest):
    """Every page has exactly one source; every manifest entry points at a page."""
    problems = []
    md_pages = {p.stem: p for p in sorted(GUIDES.glob("*.md"))} if GUIDES.is_dir() else {}
    for slug, md_path in md_pages.items():
        html_path = DOCS / f"{slug}.html"
        if html_path.exists():
            problems.append(
                f"two sources for '{slug}': {md_path.relative_to(ROOT)} and "
                f"{html_path.relative_to(ROOT)}; keep one"
            )
        if f"{slug}.html" not in manifest:
            problems.append(
                f"{md_path.relative_to(ROOT)} has no entry in docs/articles.json "
                f"(slug '{slug}.html'); the badge and emoji come from there"
            )
    for slug in manifest:
        stem = slug[: -len(".html")] if slug.endswith(".html") else slug
        if not (DOCS / slug).exists() and stem not in md_pages:
            problems.append(f"docs/articles.json lists '{slug}' but no docs/{slug} or guides/{stem}.md exists")
    if problems:
        raise BuildError("\n".join(problems))
    return md_pages


def build(out_dir):
    manifest = load_manifest()
    md_pages = check_sources(manifest)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    shutil.copytree(DOCS, out_dir)

    for slug, md_path in md_pages.items():
        entry = manifest[f"{slug}.html"]
        source_url = SOURCE_URL_BASE + md_path.relative_to(ROOT).as_posix()
        page = render(
            md_path.read_text(encoding="utf-8"),
            entry.get("badge", "approved"),
            entry.get("emoji", ""),
            source_url,
        )
        (out_dir / f"{slug}.html").write_text(page, encoding="utf-8")
        panels = page.count('class="panel"')
        print(f"rendered guides/{slug}.md -> {out_dir.name}/{slug}.html ({panels} panels)")

    copied = sum(1 for p in DOCS.rglob("*") if p.is_file())
    print(f"copied {copied} files from docs/ into {out_dir}/")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=ROOT / "_site", help="output directory (replaced)")
    args = ap.parse_args(argv)
    try:
        build(args.out)
    except BuildError as exc:
        sys.exit(f"build_site: {exc}")


if __name__ == "__main__":
    main()
