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
from enrich import enrich_all
from buckets import bucketize, LANE_LAND_READY, LANE_BOT_BACKPORT, LANE_REVIEWER_COURT, \
    LANE_NEEDS_DECISION, LANE_AUTHOR_COURT, LANE_FLAGGED_CLOSE, LANE_EXCLUDED_DRAFT
from outreach import build_outreach

REPO = "valkey-io/valkey"
BASE_URL = "https://api.github.com"
TODAY = datetime.now(timezone.utc)


def gh_get(path, params=None):
    import time as _time
    token = os.environ.get("GITHUB_TOKEN", "")
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "valkey-pr-watchtower/1.0")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < 2:
                wait = int(e.headers.get("Retry-After", 30))
                print(f"  Rate limited ({e.code}), waiting {wait}s... (attempt {attempt+1})", file=sys.stderr)
                _time.sleep(wait)
            else:
                raise


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


def fetch_weekly_activity():
    """Fetch merged and closed PR counts for the past 8 weeks."""
    import time
    weeks = []
    for w in range(8):
        end = TODAY - timedelta(weeks=w)
        start = end - timedelta(weeks=1)
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")
        try:
            # Use search API for merged count
            merged = gh_get("/search/issues", {
                "q": f"repo:{REPO} is:pr is:merged merged:{start_str}..{end_str}",
                "per_page": 1
            }).get("total_count", 0)
            time.sleep(2)  # respect secondary rate limit
            # Opened
            opened = gh_get("/search/issues", {
                "q": f"repo:{REPO} is:pr created:{start_str}..{end_str}",
                "per_page": 1
            }).get("total_count", 0)
            time.sleep(2)
        except Exception as e:
            print(f"  Rate limited at week {start_str}, stopping: {e}", file=sys.stderr)
            break
        weeks.append({
            "week_start": start_str,
            "week_end": end_str,
            "opened": opened,
            "merged": merged,
        })
        print(f"  Week {start_str}: opened={opened} merged={merged}", file=sys.stderr)
    weeks.reverse()  # chronological order
    return weeks


def fetch_pr_ci_status(pr_numbers):
    """Fetch CI status and mergeability for specific PRs (individual API calls)."""
    results = {}
    for num in pr_numbers:
        pr_detail = gh_get(f"/repos/{REPO}/pulls/{num}")
        # Get check runs for head SHA
        sha = pr_detail.get("head", {}).get("sha", "")
        checks = {"total": 0, "success": 0, "failure": 0, "pending": 0}
        if sha:
            check_data = gh_get(f"/repos/{REPO}/commits/{sha}/check-runs", {"per_page": 100})
            for run in check_data.get("check_runs", []):
                checks["total"] += 1
                if run["conclusion"] == "success":
                    checks["success"] += 1
                elif run["conclusion"] in ("failure", "timed_out"):
                    checks["failure"] += 1
                elif run["status"] != "completed":
                    checks["pending"] += 1
        results[num] = {
            "mergeable": pr_detail.get("mergeable"),
            "mergeable_state": pr_detail.get("mergeable_state"),
            "checks": checks,
        }
    print(f"  Fetched CI status for {len(results)} PRs.", file=sys.stderr)
    return results


def save_history(stats, weeks):
    """Append today's snapshot to data/history.json."""
    history_path = os.path.join(os.path.dirname(__file__), "../data/history.json")
    history_path = os.path.normpath(history_path)
    history = []
    if os.path.exists(history_path):
        with open(history_path) as f:
            history = json.loads(f.read())
    # Append today's entry (deduplicate by date)
    today_str = TODAY.strftime("%Y-%m-%d")
    history = [h for h in history if h.get("date") != today_str]
    history.append({
        "date": today_str,
        "open_prs": stats["open_prs"],
        "weekly_activity": weeks,
    })
    # Keep last 90 days
    history = history[-90:]
    with open(history_path, "w") as f:
        f.write(json.dumps(history, indent=2))
    print(f"  Saved history ({len(history)} entries).", file=sys.stderr)
    return history


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
    """Rewrite the counter placeholders in docs/components.js with live stats."""
    target_path = os.path.join(os.path.dirname(__file__), "../docs/components.js")
    target_path = os.path.normpath(target_path)
    if not os.path.exists(target_path):
        print(f"  components.js not found at {target_path}, skipping patch", file=sys.stderr)
        return

    with open(target_path) as f:
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
        r'(<span class="counter-last-updated"[^>]*>)[^<]*(</span>)',
        rf'\g<1>{stats["generated"]}\g<2>',
        html
    )

    with open(target_path, "w") as f:
        f.write(html)
    print(f"  Patched components.js counters.", file=sys.stderr)


def _md_row(entry, extra=None):
    n = entry["number"]
    title = entry["title"][:70] + ("…" if len(entry["title"]) > 70 else "")
    row = f"| [{n}]({entry['url']}) | {title} | {entry['author']} | {age_str(age_days(entry['created_at'])) if entry.get('created_at') else '—'} |"
    if extra is not None:
        row += f" {extra} |"
    return row


def _md_outreach(lines, title, candidates):
    if not candidates:
        return
    lines.append(section_header(title, 3))
    lines.append("| PR | Title | Author | Evidence | Proposed action |")
    lines.append("|----|-------|--------|----------|-----------------|")
    for c in candidates:
        title_s = c["title"][:50] + ("…" if len(c["title"]) > 50 else "")
        ev = "; ".join(c.get("evidence", []))
        lines.append(f"| [{c['number']}]({c['url']}) | {title_s} | {c['author']} | {ev} | `{c['proposed_action']}` |")
    lines.append("")


def build_report(prs, bucket_result, outreach):
    """Markdown report — actionability-ordered lanes + outreach dry-run."""
    lines = []
    generated = TODAY.strftime("%Y-%m-%d %H:%M UTC")
    lanes = bucket_result["lanes"]
    counts = bucket_result["counts"]
    by_number = bucket_result["by_number"]

    lines.append("# Valkey PR Health Report")
    lines.append("")
    lines.append(f"**Generated:** {generated} | **Repo:** [{REPO}](https://github.com/{REPO})")
    lines.append("")
    lines.append("_PRs are sorted into lanes by who owns the next move, most immediately actionable first._")
    lines.append("")
    lines.append("---")

    # ── By the Numbers ──
    lines.append(section_header("📊 By the Numbers"))
    lines.append("| Lane | Count |")
    lines.append("|------|-------|")
    lines.append(f"| Total open PRs | {bucket_result['total']} |")
    for label, key in [("🟢 Land-ready", LANE_LAND_READY),
                       ("🤖 Bot / backport", LANE_BOT_BACKPORT),
                       ("👀 Ball in reviewer's court", LANE_REVIEWER_COURT),
                       ("🗳 Needs a decision", LANE_NEEDS_DECISION),
                       ("🏷 Flagged to close", LANE_FLAGGED_CLOSE),
                       ("✍️ Ball in author's court", LANE_AUTHOR_COURT),
                       ("📝 Draft (excluded)", LANE_EXCLUDED_DRAFT)]:
        lines.append(f"| {label} | {counts.get(key, 0)} |")
    lines.append("")

    def lane_section(title, key, note=None, cols="| PR | Title | Author | Age |",
                     sep="|----|-------|--------|-----|", sort_key=None):
        entries = lanes.get(key, [])
        if not entries:
            return
        lines.append(section_header(title))
        if note:
            lines.append(f"_{note}_")
            lines.append("")
        lines.append(cols)
        lines.append(sep)
        skey = sort_key or (lambda e: e.get("created_at") or "")
        for e in sorted(entries, key=skey):
            lines.append(_md_row(e))
        lines.append("")

    # ── Priority: owed a review (label-driven) ──
    _md_outreach(lines, "⭐ Owed a Review (priority)", outreach["priority_owed_review"]) \
        if outreach["priority_owed_review"] else None

    # ── Lanes, actionability order ──
    lane_section("🟢 Land-ready — one click to merge", LANE_LAND_READY,
                 note="Community-approved / to-be-merged, CI not failing, no conflicts.")
    lane_section("🤖 Bot / backport quick-wins", LANE_BOT_BACKPORT,
                 note="Human-approved, fast to land.")

    # First-timers overlay
    first_timers = [e for e in by_number.values() if "first_timer" in e["overlays"]
                    and e["lane"] != LANE_EXCLUDED_DRAFT]
    if first_timers:
        lines.append(section_header("🌱 First-Time Contributors"))
        lines.append("_A timely response may retain a future regular. Cross-cut; each also appears in its lane._")
        lines.append("")
        lines.append("| PR | Title | Author | Age | Lane |")
        lines.append("|----|-------|--------|-----|------|")
        for e in sorted(first_timers, key=lambda e: e.get("created_at") or "", reverse=True):
            lines.append(_md_row(e, extra=f"`{e['lane']}`"))
        lines.append("")

    lane_section("👀 Ball in Reviewer's Court", LANE_REVIEWER_COURT,
                 note="Author acted last — these need a reviewer. Longest-waiting first.",
                 sort_key=lambda e: -(e.get("dormancy_days") or 0))
    lane_section("🗳 Needs a Decision", LANE_NEEDS_DECISION,
                 note="Blocked on a community decision.")

    # Deflake overlay
    deflake = [e for e in by_number.values() if "deflake" in e["overlays"]]
    if deflake:
        lines.append(section_header("🔥 Deflake / Test-Fix"))
        lines.append("_Merging these reduces CI noise. Cross-cut; each also appears in its lane._")
        lines.append("")
        lines.append("| PR | Title | Author | Age | Lane |")
        lines.append("|----|-------|--------|-----|------|")
        for e in sorted(deflake, key=lambda e: e.get("created_at") or ""):
            lines.append(_md_row(e, extra=f"`{e['lane']}`"))
        lines.append("")

    # ── Outreach dry-run ──
    if any(outreach[k] for k in ("reengage", "closure_abandoned",
                                 "maintainer_flagged_close", "superseded_suggestions")):
        lines.append(section_header("📮 Outreach Dry-Run"))
        lines.append("_**Dry-run only.** Nothing is posted, closed, or labelled automatically — "
                     "these are proposals for a human to review and act on._")
        lines.append("")
        th = outreach["thresholds"]
        _md_outreach(lines, f"Re-engage (reviewer's court, idle ≥{th['reengage_days']}d)", outreach["reengage"])
        _md_outreach(lines, f"Closure candidates (author's court, idle ≥{th['closure_days']}d)", outreach["closure_abandoned"])
        _md_outreach(lines, "Maintainer-flagged to close", outreach["maintainer_flagged_close"])
        _md_outreach(lines, "Possibly superseded (verify first)", outreach["superseded_suggestions"])

    # ── Ball in author's court (bottom) ──
    lane_section("✍️ Ball in Author's Court", LANE_AUTHOR_COURT,
                 note="Waiting on the author (CI red / conflicts / unaddressed review). Longest-idle first.",
                 sort_key=lambda e: -(e.get("dormancy_days") or 0))

    lines.append("---")
    lines.append("")
    lines.append(f"*Report generated by [valkey-pr-watchtower](https://github.com/valkey-rainfall/valkey-pr-watchtower). "
                 f"Data from GitHub API. Opinions are the author's own.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="Output file (default: stdout)")
    parser.add_argument("--html", help="Output HTML report file")
    parser.add_argument("--enrich-limit", type=int, default=None,
                        help="Cap PRs enriched (for quick low-rate-limit runs)")
    args = parser.parse_args()

    prs = fetch_all_open_prs()

    LAUNCH_DATE = "2026-07-02"
    prs_since = fetch_prs_since(LAUNCH_DATE)

    print("Fetching weekly activity...", file=sys.stderr)
    weeks = fetch_weekly_activity()

    generated = TODAY.strftime("%Y-%m-%d %H:%M UTC")
    stats = {
        "generated": generated,
        "open_prs": len(prs),
        "prs_since_launch": prs_since,
        "launch_date": LAUNCH_DATE,
    }
    save_history(stats, weeks)

    # Enrich all non-draft, non-bot PRs (review state, CI, mergeable, activity timelines).
    print("Enriching open PRs...", file=sys.stderr)

    def _progress(num, count):
        if count % 25 == 0:
            print(f"  enriched {count} PRs...", file=sys.stderr)

    enriched = enrich_all(prs, gh_get, gh_paginate, repo=REPO,
                          limit=args.enrich_limit, progress=_progress)
    print(f"  enriched {len(enriched)} PRs.", file=sys.stderr)

    bucket_result = bucketize(prs, enriched, now=TODAY)
    if not bucket_result["reconciled"]:
        print("  WARNING: lane counts did not reconcile to total!", file=sys.stderr)
    prs_by_num = {p["number"]: p for p in prs}
    outreach_data = build_outreach(bucket_result, prs_by_num)

    patch_index_html(stats)

    report = build_report(prs, bucket_result, outreach_data)
    if args.out:
        with open(args.out, "w") as f:
            f.write(report)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(report)

    if args.html:
        html = build_report_html(prs, generated, bucket_result, outreach_data, weeks=weeks)
        with open(args.html, "w") as f:
            f.write(html)
        print(f"Wrote {args.html}", file=sys.stderr)


if __name__ == "__main__":
    main()
