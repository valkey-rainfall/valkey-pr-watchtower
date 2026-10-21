#!/usr/bin/env python3
"""Check that every internal link in the built site points at something.

Walks the HTML pages under the build output directory and resolves each
``href`` and ``src`` that is not an external URL, a ``mailto:``, or a bare
fragment. A link must name a file that exists in the output tree; a link with a
``#fragment`` must also name an element ``id`` present in the target page.

External links are deliberately not fetched: they fail on the other site's
uptime, not on anything a change to this repository did.

Usage:
    tools/check_links.py [--site _site]

Exit status is 1 when any link is broken, with one line per broken link.
"""

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

EXTERNAL = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)  # http:, https:, mailto:, data:, ...


class Collector(HTMLParser):
    """Gather link targets and element ids from one page."""

    def __init__(self):
        super().__init__()
        self.links = []  # (line, attribute, value)
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name == "id":
                self.ids.add(value)
            elif name in ("href", "src") or (tag == "a" and name == "name"):
                if name == "name":
                    self.ids.add(value)
                else:
                    self.links.append((self.getpos()[0], name, value))


def scan(site):
    pages = {}
    for path in sorted(site.rglob("*.html")):
        parser = Collector()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        pages[path] = parser
    return pages


def check(site):
    site = site.resolve()
    pages = scan(site)
    ids_by_page = {path: parser.ids for path, parser in pages.items()}
    broken = []
    for path, parser in pages.items():
        for line, attr, value in parser.links:
            value = value.strip()
            if not value or EXTERNAL.match(value) or value.startswith("//"):
                continue
            parts = urlsplit(value)
            target_path = unquote(parts.path)
            if target_path.startswith("/"):
                target = site / target_path.lstrip("/")
            elif target_path:
                target = (path.parent / target_path).resolve()
            else:
                target = path  # bare fragment: same page
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append(f"{path.relative_to(site)}:{line}: {attr}=\"{value}\" -> no such file")
                continue
            if parts.fragment and target.suffix == ".html":
                if parts.fragment not in ids_by_page.get(target, set()):
                    broken.append(
                        f"{path.relative_to(site)}:{line}: {attr}=\"{value}\" -> "
                        f"no id '{parts.fragment}' in {target.relative_to(site)}"
                    )
    return broken, sum(len(p.links) for p in pages.values()), len(pages)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--site", type=Path, default=ROOT / "_site", help="built site directory")
    args = ap.parse_args(argv)
    if not args.site.is_dir():
        sys.exit(f"check_links: {args.site} does not exist; run tools/build_site.py first")
    broken, total, pages = check(args.site)
    for line in broken:
        print(line)
    print(f"{pages} pages, {total} links, {len(broken)} broken")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
