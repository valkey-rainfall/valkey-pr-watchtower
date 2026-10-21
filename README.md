# valkey-pr-watchtower 🗼

Write-ups, guides, analyses and small tools around [valkey-io/valkey](https://github.com/valkey-io/valkey), made in a personal capacity.

**[→ The site](https://valkey-rainfall.github.io/valkey-pr-watchtower/)**

---

## What this is

A personal, unofficial home for things [@rainsupreme](https://github.com/rainsupreme) and her AI agents have made around Valkey: review guides, deep dives, orientation notes, tooling. Everything here is public; nothing private, confidential or proprietary belongs in this repository.

It started life as a daily PR-health report generated from the GitHub API. That report ran from July to October 2026 and is retired; its last snapshot is kept at `docs/report.html` and the generator scripts live on in git history.

> **Disclaimer:** A personal project written in a personal capacity. Not an official Valkey project; does not represent the views of the Valkey project, the Linux Foundation, or the author's employer. Opinions are the author's own. AI-assisted content is marked as such.

---

## What's in here

```
docs/
  index.html             # landing page
  articles.json          # article manifest: metadata + "Latest Updates" feed
  articles.html          # browse-all-articles page (reads articles.json)
  _article-template.html # copy this to start a hand-written article
  components.js          # header, nav, sidebar, footer, attribution badges
  report.html, report.md # archived final snapshot of the daily PR report

guides/
  review-guide.md        # markdown-canonical pages; rendered to <slug>.html at build time

tools/
  build_site.py          # assembles docs/ + rendered guides/ into _site/ (the published tree)

data/
  history.json           # daily PR-count series captured while the report ran

.github/workflows/
  ci.yml                 # on pull requests: run the site build, fail on any source/manifest problem
  deploy-pages.yml       # build _site/ and publish it to GitHub Pages on push to main
```

Every page has exactly one canonical source, chosen by which file exists: `docs/<slug>.html` (hand-written HTML, served as-is) or `guides/<slug>.md` (markdown, rendered at build time). A slug with both fails the build. Rendered pages are never committed; `_site/` is gitignored.

The build also validates `docs/articles.json`: every article entry has the expected fields, `badge` is one of `ai`/`approved`/`human`, dates are `YYYY-MM-DD`, slugs are unique and point at an existing page, and every `updates[].href` names a real page. CI runs the build on every pull request, so a broken manifest or page layout is caught before merge rather than as a red deploy.

---

## Adding an article

Both formats are first-class. Pick HTML when the page needs layout or interactivity the panel renderer does not give you; pick markdown when the text will be edited over time or read straight from the repo.

Hand-written HTML page:

1. `cp docs/_article-template.html docs/your-slug.html` and fill in the title, date, and content panels.
2. Add an entry to the `articles` array in `docs/articles.json` (slug, title, emoji, date, updated, badge, summary, tags).
3. Add an entry to the **top** of the `updates` array in `docs/articles.json`.

Markdown page:

1. Write `guides/your-slug.md`. The first `#` heading is the page title; each `##` section becomes one panel. Raw inline HTML passes through, so a `<details>` block or a custom table inside an otherwise-markdown page works.
2. Same two `articles.json` entries as above. The entry's `emoji` and `badge` are what the rendered page shows; bump `updated` when the text changes.
3. Commit the markdown only. The deploy workflow renders it; no HTML to commit or keep in sync.

Switching a page between formats is a normal git change: to go markdown -> HTML, run the build, `git add` the rendered page from `_site/` into `docs/`, and delete the `.md`; the reverse is writing the `.md` and deleting the `.html`. The build refuses a slug that has both.

Preview locally (needs `pip install markdown`):

```
python3 tools/build_site.py          # writes _site/
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

The nav, the Articles page, and the sidebar "Latest Updates" panel all read `articles.json` — no other file needs editing. Attribution badges: `ai`, `approved`, or `human` (see `<attr-badge>` in `components.js`).

---

## PR process orientation (personal perspective)

The official contributing guide lives at [valkey-io/valkey/blob/unstable/CONTRIBUTING.md](https://github.com/valkey-io/valkey/blob/unstable/CONTRIBUTING.md). Read that first.

What follows is my personal read on how the PR process works in practice — not rules, just patterns I've observed.

**What makes a PR land quickly:**
- Small and focused. One thing per PR. Reviewers are busy; a 50-line fix gets reviewed in days, a 2000-line refactor sits for months.
- CI green before requesting review. Broken CI is an immediate context-switch cost for reviewers.
- Clear description: what changes, why, how to verify it. Don't make the reviewer reverse-engineer your intent.
- For anything non-trivial, check if there's an open issue or prior discussion. "Fixes #NNNN" or "continuing discussion from #NNNN" tells reviewers there's context.

**What makes a PR die quietly:**
- No activity after initial submission. If you get feedback and go quiet, maintainers assume you've moved on.
- Scope creep mid-review. If a reviewer asks for a small fix and you refactor three unrelated things in the same commit, they lose the thread.
- No `release-notes` or `no-release-notes` label. The bot will flag it and reviewers will skip it until it's labeled.
- Duplicate of an existing open PR. Search before submitting.

**The `major-decision-pending` label:**
This means maintainers haven't reached consensus yet. It's not a blocker on your end — your code is fine. It means the community is still debating whether to take the feature at all. These can take weeks to months to resolve. Patience is the only option; pinging won't speed it up.

**Reviewer assignment:**
There's no formal assignment process for most PRs. Maintainers pick up what they have context on. If your PR has sat 3+ weeks with no activity, a polite ping in the PR is appropriate. Tag someone who has reviewed similar code recently — check `git log` on the files you changed.

**First contributions:**
The project is welcoming but bandwidth-constrained. Your first PR might take longer than you expect. That's normal and not a signal about the PR quality. A good first PR to build trust: fix a real bug (not just a typo), keep it small, include a test.
