#!/usr/bin/env python3
"""
build_report.py — generates a PR health report for valkey-io/valkey.

Usage:
    GITHUB_TOKEN=xxx python scripts/build_report.py > docs/report.md
    python scripts/build_report.py --out docs/report.md
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict
import urllib.request
import urllib.parse

from html_report import build_report_html

REPO = "valkey-io/valkey"
BASE_URL = "https://api.github.com"
TODAY = datetime.now(timezone.utc)


def gh_get(path, params=None):
    token = os.environ.get("GITHUB_TOKEN", "")
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "valkey-pr-watchtower/1.0")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def gh_paginate(path, params=None):
    """Fetch all pages of a GitHub list endpoint."""
    params = dict(params or {})
    params.setdefault("per_page", 100)
    results = []
    page = 1
    while True:
        params["page"] = page
        data = gh_get(path, params)
        if not data:
            break
        results.extend(data)
        if len(data) < params["per_page"]:
            break
        page += 1
    return results


def age_days(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return (TODAY - dt).days


def age_str(days):
    if days < 14:
        return f"{days}d"
    if days < 60:
        return f"{days // 7}w"
    if days < 365:
        return f"{days // 30}mo"
    return f"{days / 365:.1f}y"


def label_names(pr):
    return [l["name"] for l in pr.get("labels", [])]


def pr_url(number):
    return f"https://github.com/{REPO}/pull/{number}"


def fetch_all_open_prs():
    print("Fetching open PRs...", file=sys.stderr)
    prs = gh_paginate(f"/repos/{REPO}/pulls", {"state": "open"})
    print(f"  {len(prs)} open PRs fetched.", file=sys.stderr)
    return prs


def fetch_labeled_prs(label):
    return gh_paginate(f"/repos/{REPO}/issues", {
        "state": "open", "labels": label, "filter": "all"
    })


def section_header(title, level=2):
    return f"\n{'#' * level} {title}\n"


def pr_row(pr, extra=""):
    n = pr["number"]
    title = pr["title"][:70] + ("…" if len(pr["title"]) > 70 else "")
    author = pr.get("user", {}).get("login", "?")
    created = age_str(age_days(pr["created_at"]))
    updated = age_str(age_days(pr["updated_at"]))
    draft = " (draft)" if pr.get("draft") else ""
    labels = ", ".join(f"`{l}`" for l in label_names(pr)) if label_names(pr) else ""
    row = f"| [{n}]({pr_url(n)}) | {title}{draft} | {author} | {created} old | {updated} ago |"
    if extra:
        row += f" {extra} |"
    return row


def fetch_prs_since(since_date):
    """Count PRs opened on valkey-io/valkey since a given ISO date string."""
    print(f"Fetching PRs since {since_date}...", file=sys.stderr)
    # GitHub search API: issues/PRs created after date
    result = gh_get("/search/issues", {
        "q": f"repo:{REPO} is:pr created:>={since_date}",
        "per_page": 1
    })
    return result.get("total_count", 0)


def patch_index_html(stats):
    """Rewrite the counter placeholders in docs/index.html with live stats."""
    index_path = os.path.join(os.path.dirname(__file__), "../docs/index.html")
    index_path = os.path.normpath(index_path)
    if not os.path.exists(index_path):
        print(f"  index.html not found at {index_path}, skipping patch", file=sys.stderr)
        return

    with open(index_path) as f:
        html = f.read()

    # Replace counter placeholders with live values
    # Visitor counter: keep as 000001 (static joke)
    # Total PRs gazed upon = open at time of report + new ones since launch
    # This is "all PRs that have existed during the watchtower's watch"
    total_gazed = stats["open_prs"] + stats["prs_since_launch"]

    # PR count watched (open) — zero-padded to 4 digits
    html = re.sub(
        r'(<span class="counter-prs-open">)[^<]*(</span>)',
        rf'\g<1>{stats["open_prs"]:04d}\g<2>',
        html
    )
    # Total PRs gazed upon — zero-padded to 4 digits
    html = re.sub(
        r'(<span class="counter-prs-since">)[^<]*(</span>)',
        rf'\g<1>{total_gazed:04d}\g<2>',
        html
    )
    # Last updated
    html = re.sub(
        r'(<span class="counter-last-updated">)[^<]*(</span>)',
        rf'\g<1>{stats["generated"]}\g<2>',
        html
    )

    with open(index_path, "w") as f:
        f.write(html)
    print(f"  Patched index.html counters.", file=sys.stderr)


def build_report(prs):
    lines = []
    generated = TODAY.strftime("%Y-%m-%d %H:%M UTC")

    lines.append(f"# Valkey PR Health Report")
    lines.append(f"")
    lines.append(f"**Generated:** {generated} | **Repo:** [{REPO}](https://github.com/{REPO})")
    lines.append(f"")
    lines.append(f"---")

    # ── By the Numbers ──────────────────────────────────────────────────────
    non_draft = [p for p in prs if not p.get("draft")]
    draft = [p for p in prs if p.get("draft")]
    bot_prs = [p for p in prs if p.get("user", {}).get("login", "").endswith("[bot]")]

    label_counts = Counter()
    for pr in prs:
        for l in label_names(pr):
            label_counts[l] += 1

    lines.append(section_header("📊 By the Numbers"))
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Total open PRs | {len(prs)} |")
    lines.append(f"| Non-draft | {len(non_draft)} |")
    lines.append(f"| Draft | {len(draft)} |")
    lines.append(f"| Bot PRs (backports etc.) | {len(bot_prs)} |")
    for label in ["major-decision-pending", "major-decision-approved",
                  "major-decision-deferred", "to-be-merged", "to-be-closed",
                  "stalled", "run-extra-tests", "needs-doc-pr"]:
        if label in label_counts:
            lines.append(f"| `{label}` | {label_counts[label]} |")
    lines.append("")

    # ── Immediate Actions ────────────────────────────────────────────────────
    lines.append(section_header("⚡ Immediate Actions"))

    # to-be-merged
    tbm = [p for p in non_draft if "to-be-merged" in label_names(p)]
    if tbm:
        lines.append(section_header("Merge Now (`to-be-merged`)", 3))
        lines.append("| PR | Title | Author | Age | Last update |")
        lines.append("|----|-------|--------|-----|-------------|")
        for pr in sorted(tbm, key=lambda p: p["created_at"]):
            lines.append(pr_row(pr))
        lines.append("")

    # major-decision-approved, non-draft
    approved = [p for p in non_draft
                if "major-decision-approved" in label_names(p)
                and "to-be-merged" not in label_names(p)]
    if approved:
        lines.append(section_header("Community-Approved, Awaiting Merge (`major-decision-approved`)", 3))
        lines.append("_Decision is made — these just need someone to merge them._")
        lines.append("")
        lines.append("| PR | Title | Author | Age | Last update |")
        lines.append("|----|-------|--------|-----|-------------|")
        for pr in sorted(approved, key=lambda p: p["created_at"]):
            lines.append(pr_row(pr))
        lines.append("")

    # to-be-closed
    tbc = [p for p in prs if "to-be-closed" in label_names(p)]
    stalled = [p for p in prs if "stalled" in label_names(p)]
    if tbc or stalled:
        lines.append(section_header("Close Now", 3))
        lines.append("| PR | Title | Author | Age | Reason |")
        lines.append("|----|-------|--------|-----|--------|")
        for pr in tbc:
            n, title, author = pr["number"], pr["title"][:60], pr.get("user", {}).get("login", "?")
            lines.append(f"| [{n}]({pr_url(n)}) | {title} | {author} | {age_str(age_days(pr['created_at']))} | `to-be-closed` |")
        for pr in stalled:
            n, title, author = pr["number"], pr["title"][:60], pr.get("user", {}).get("login", "?")
            lines.append(f"| [{n}]({pr_url(n)}) | {title} | {author} | {age_str(age_days(pr['created_at']))} | `stalled` |")
        lines.append("")

    # ── Decision Bottleneck ──────────────────────────────────────────────────
    pending = [p for p in non_draft if "major-decision-pending" in label_names(p)]
    if pending:
        lines.append(section_header("🟡 Decision Bottleneck (`major-decision-pending`)"))
        lines.append(f"**{len(pending)} PRs** blocked waiting for a community vote.")
        lines.append("")
        lines.append("| PR | Title | Author | Age | Last update |")
        lines.append("|----|-------|--------|-----|-------------|")
        for pr in sorted(pending, key=lambda p: p["created_at"])[:20]:
            lines.append(pr_row(pr))
        if len(pending) > 20:
            lines.append(f"| … | *{len(pending) - 20} more* | | | |")
        lines.append("")

    # ── Top Contributors ─────────────────────────────────────────────────────
    lines.append(section_header("🧑‍💻 Top Contributors by Open PR Count"))
    author_counts = Counter(
        p.get("user", {}).get("login", "?")
        for p in non_draft
        if not p.get("user", {}).get("login", "").endswith("[bot]")
    )
    lines.append("| Author | Open PRs |")
    lines.append("|--------|----------|")
    for author, count in author_counts.most_common(15):
        flag = " 🚨" if count >= 8 else (" ⚠️" if count >= 5 else "")
        lines.append(f"| [{author}](https://github.com/{author}) | {count}{flag} |")
    lines.append("")

    # ── Aging ────────────────────────────────────────────────────────────────
    lines.append(section_header("🕰 Long-Dormant PRs (90+ days since last update)"))
    dormant = [p for p in non_draft
               if age_days(p["updated_at"]) >= 90
               and not p.get("user", {}).get("login", "").endswith("[bot]")]
    dormant.sort(key=lambda p: p["updated_at"])

    lines.append(f"**{len(dormant)} non-draft PRs** haven't been updated in 90+ days.")
    lines.append("")
    lines.append("| PR | Title | Author | Created | Last update |")
    lines.append("|----|-------|--------|---------|-------------|")
    for pr in dormant[:25]:
        lines.append(pr_row(pr))
    if len(dormant) > 25:
        lines.append(f"| … | *{len(dormant) - 25} more* | | | |")
    lines.append("")

    # ── Deflake PRs ──────────────────────────────────────────────────────────
    deflake = [p for p in non_draft
               if any(kw in p["title"].lower()
                      for kw in ["flak", "deflak", "stale tmpdir", "timing"])]
    if deflake:
        lines.append(section_header("🔥 Open Deflake / Test-Fix PRs"))
        lines.append("_Merging these reduces CI noise for everyone._")
        lines.append("")
        lines.append("| PR | Title | Author | Age | Last update |")
        lines.append("|----|-------|--------|-----|-------------|")
        for pr in sorted(deflake, key=lambda p: p["created_at"]):
            lines.append(pr_row(pr))
        lines.append("")

    # ── High CI Burden ───────────────────────────────────────────────────────
    run_extra = [p for p in non_draft if "run-extra-tests" in label_names(p)]
    if run_extra:
        lines.append(section_header("⏱ High CI Burden (`run-extra-tests`)"))
        lines.append(f"**{len(run_extra)} PRs** trigger extended CI runs.")
        lines.append("")
        lines.append("| PR | Title | Author | Age |")
        lines.append("|----|-------|--------|-----|")
        for pr in sorted(run_extra, key=lambda p: p["created_at"]):
            n = pr["number"]
            title = pr["title"][:60]
            author = pr.get("user", {}).get("login", "?")
            a = age_str(age_days(pr["created_at"]))
            lines.append(f"| [{n}]({pr_url(n)}) | {title} | {author} | {a} |")
        lines.append("")

    # ── Footer ───────────────────────────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append(f"*Report generated by [valkey-pr-watchtower](https://github.com/valkey-rainfall/valkey-pr-watchtower). Data from GitHub API. Opinions are the author's own.*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="Output file (default: stdout)")
    parser.add_argument("--html", help="Output HTML report file")
    args = parser.parse_args()

    prs = fetch_all_open_prs()

    # Fetch PRs-since-launch count (site went live 2026-07-02)
    LAUNCH_DATE = "2026-07-02"
    prs_since = fetch_prs_since(LAUNCH_DATE)

    generated = TODAY.strftime("%Y-%m-%d %H:%M UTC")
    stats = {
        "generated": generated,
        "open_prs": len(prs),
        "prs_since_launch": prs_since,
        "launch_date": LAUNCH_DATE,
    }

    # Patch live counters into index.html
    patch_index_html(stats)

    report = build_report(prs)

    if args.out:
        with open(args.out, "w") as f:
            f.write(report)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(report)

    # Generate HTML report
    if args.html:
        html_report = build_report_html(prs, generated)
        with open(args.html, "w") as f:
            f.write(html_report)
        print(f"Wrote {args.html}", file=sys.stderr)


if __name__ == "__main__":
    main()
