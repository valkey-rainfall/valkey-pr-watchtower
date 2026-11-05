#!/usr/bin/env python3
"""Assemble the publishable site into one output directory.

Every page has exactly one canonical source, chosen by which file exists:

* ``docs/<slug>.html``  -- hand-written HTML, copied as-is.
* ``guides/<slug>.md``  -- markdown, rendered into ``<slug>.html`` here.
* ``guides/<dir>/README.md`` -- markdown, rendered into ``<dir>.html``; every
  other ``guides/<dir>/<name>.md`` becomes ``<dir>-<name>.html`` (lower case).
  Only ``<dir>.html`` needs an entry in ``docs/articles.json``; the other pages
  of the directory use its emoji and badge.

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

Two conventions make markdown pages link to each other the same way on GitHub
and on the site:

* A relative link to another ``guides/`` markdown file (``triage.md``,
  ``../review-guide.md#change-ladder``) is rewritten to that page's ``.html``
  slug, keeping the fragment. A link to a markdown file that is not a page is
  an error.
* A ``##`` section whose body starts with ``<a id="name"></a>`` on its own line
  gives that id to the section's panel, so ``page.html#name`` lands on the
  panel header.

Requires the ``markdown`` package.
"""

import argparse
import html
import json
import re
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

PANEL = """  <div class="panel"{panel_id} style="margin-bottom:12px;">
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


SECTION_ANCHOR = re.compile(r'^<a id="([A-Za-z][A-Za-z0-9_-]*)"></a>\s*(?:\n|$)')
HREF = re.compile(r'href="([^"]*)"')
EXTERNAL = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


def rewrite_md_links(rendered, md_path, slug_by_path):
    """Point relative links to guides/ markdown files at their rendered pages."""

    def fix(match):
        href = html.unescape(match.group(1))
        if not href or href.startswith("#") or href.startswith("//") or EXTERNAL.match(href):
            return match.group(0)
        path, _, fragment = href.partition("#")
        if not path.endswith(".md"):
            return match.group(0)
        target = (md_path.parent / path).resolve()
        if target not in slug_by_path:
            raise BuildError(
                f"{md_path.relative_to(ROOT)} links to '{path}', which is not a page under guides/"
            )
        new = slug_by_path[target] + (f"#{fragment}" if fragment else "")
        return f'href="{html.escape(new)}"'

    return HREF.sub(fix, rendered)


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


def render(md_text, badge, emoji, source_url, md_path=None, slug_by_path=None):
    """Render one markdown document into a full article page."""
    title, intro, sections = split_sections(md_text)
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    def body(text):
        md.reset()
        rendered = md.convert(text)
        if md_path is not None:
            rendered = rewrite_md_links(rendered, md_path, slug_by_path or {})
        return "\n".join("      " + ln for ln in rendered.splitlines())

    heading = f"{emoji} {html.escape(title)}" if emoji else html.escape(title)
    intro_html = body(intro) if intro else ""
    intro_html += (
        '\n      <p class="muted" style="font-size:0.82em; margin-top:10px;">'
        f'Canonical text and revision history: <a href="{html.escape(source_url)}" '
        'target="_blank" rel="noopener noreferrer">markdown source on GitHub ↗</a>. '
        "This page is generated from it.</p>"
    )
    panels = [PANEL.format(panel_id="", heading=heading, badge=badge, body=intro_html)]
    for h, b in sections:
        anchor = SECTION_ANCHOR.match(b)
        panel_id = f' id="{anchor.group(1)}"' if anchor else ""
        if anchor:
            b = b[anchor.end():].lstrip("\n")
        panels.append(PANEL.format(panel_id=panel_id, heading=html.escape(h), badge=badge, body=body(b)))
    return PAGE.format(
        source=html.escape(source_url),
        title=html.escape(title),
        panels="\n".join(panels),
    )


ARTICLE_FIELDS = {
    "slug": str,
    "title": str,
    "emoji": str,
    "date": str,
    "updated": str,
    "badge": str,
    "summary": str,
    "tags": list,
}
UPDATE_FIELDS = {"date": str, "text": str, "href": str}
BADGES = {"ai", "approved", "human"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_fields(problems, where, obj, fields):
    """Every field present with the right type; nothing missing or extra."""
    if not isinstance(obj, dict):
        problems.append(f"{where}: expected an object")
        return False
    for name, kind in fields.items():
        if name not in obj:
            problems.append(f"{where}: missing '{name}'")
        elif not isinstance(obj[name], kind):
            problems.append(f"{where}: '{name}' should be {kind.__name__}")
    for name in obj.keys() - fields.keys():
        problems.append(f"{where}: unknown field '{name}'")
    return True


def load_manifest():
    """Return {slug.html: entry} from docs/articles.json after validating its shape.

    Every page's metadata comes from this file, so a malformed entry would
    publish a page with a missing badge or a dead link in the updates feed.
    """
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BuildError(f"docs/articles.json is not valid JSON: {exc}") from exc

    problems = []
    if not isinstance(data, dict) or set(data) != {"articles", "updates"}:
        raise BuildError("docs/articles.json must be an object with exactly 'articles' and 'updates'")

    manifest = {}
    for i, entry in enumerate(data["articles"]):
        where = f"articles[{i}]"
        if not check_fields(problems, where, entry, ARTICLE_FIELDS):
            continue
        slug = entry.get("slug", "")
        if not isinstance(slug, str) or not slug.endswith(".html") or "/" in slug:
            problems.append(f"{where}: slug '{slug}' must be a bare '<name>.html'")
        if slug in manifest:
            problems.append(f"{where}: duplicate slug '{slug}'")
        if entry.get("badge") not in BADGES:
            problems.append(f"{where}: badge '{entry.get('badge')}' not one of {sorted(BADGES)}")
        for field in ("date", "updated"):
            if isinstance(entry.get(field), str) and not DATE_RE.match(entry[field]):
                problems.append(f"{where}: {field} '{entry[field]}' is not YYYY-MM-DD")
        if isinstance(entry.get("tags"), list) and not all(isinstance(t, str) for t in entry["tags"]):
            problems.append(f"{where}: tags must all be strings")
        if isinstance(slug, str):
            manifest[slug] = entry

    pages = set(manifest) | {p.name for p in DOCS.glob("*.html") if not p.name.startswith("_")}
    for i, upd in enumerate(data["updates"]):
        where = f"updates[{i}]"
        if not check_fields(problems, where, upd, UPDATE_FIELDS):
            continue
        if isinstance(upd.get("date"), str) and not DATE_RE.match(upd["date"]):
            problems.append(f"{where}: date '{upd['date']}' is not YYYY-MM-DD")
        href = upd.get("href", "")
        if isinstance(href, str) and href.split("#")[0] not in pages:
            problems.append(f"{where}: href '{href}' does not name a page in articles or docs/")

    if problems:
        raise BuildError("\n".join(problems))
    return manifest


def find_md_pages():
    """Return {slug: (md_path, manifest_slug)} for every markdown page under guides/."""
    pages = {}
    if not GUIDES.is_dir():
        return pages
    for md_path in sorted(GUIDES.glob("*.md")):
        pages[md_path.stem] = (md_path, f"{md_path.stem}.html")
    for sub in sorted(p for p in GUIDES.iterdir() if p.is_dir()):
        if not (sub / "README.md").exists():
            continue
        for md_path in sorted(sub.glob("*.md")):
            stem = md_path.stem.lower()
            slug = sub.name if stem == "readme" else f"{sub.name}-{stem}"
            if slug in pages:
                raise BuildError(f"two markdown sources for '{slug}': {pages[slug][0].relative_to(ROOT)} and {md_path.relative_to(ROOT)}")
            pages[slug] = (md_path, f"{sub.name}.html")
    return pages


def check_sources(manifest):
    """Every page has exactly one source; every manifest entry points at a page."""
    problems = []
    md_pages = find_md_pages()
    for slug, (md_path, entry_slug) in md_pages.items():
        html_path = DOCS / f"{slug}.html"
        if html_path.exists():
            problems.append(
                f"two sources for '{slug}': {md_path.relative_to(ROOT)} and "
                f"{html_path.relative_to(ROOT)}; keep one"
            )
        if entry_slug not in manifest:
            problems.append(
                f"{md_path.relative_to(ROOT)} has no entry in docs/articles.json "
                f"(slug '{entry_slug}'); the badge and emoji come from there"
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

    slug_by_path = {md_path.resolve(): f"{slug}.html" for slug, (md_path, _) in md_pages.items()}
    for slug, (md_path, entry_slug) in md_pages.items():
        entry = manifest[entry_slug]
        source = md_path.relative_to(ROOT).as_posix()
        page = render(
            md_path.read_text(encoding="utf-8"),
            entry.get("badge", "approved"),
            entry.get("emoji", ""),
            SOURCE_URL_BASE + source,
            md_path,
            slug_by_path,
        )
        (out_dir / f"{slug}.html").write_text(page, encoding="utf-8")
        panels = page.count('class="panel"')
        print(f"rendered {source} -> {out_dir.name}/{slug}.html ({panels} panels)")

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
