#!/usr/bin/env python3
"""Offline render smoke test: build_report (md) + build_report_html. No network."""
import sys
from datetime import datetime, timezone
import buckets as B
from outreach import build_outreach
from build_report import build_report
from html_report import build_report_html

NOW = datetime(2026, 7, 24, tzinfo=timezone.utc)
_fail = 0


def check(name, cond):
    global _fail
    if not cond:
        _fail += 1
    print(f"{'PASS' if cond else 'FAIL'}: {name}")


def pr(n, **kw):
    d = {"number": n, "draft": False, "user": {"login": kw.get("login", "alice")},
         "labels": [{"name": l} for l in kw.get("labels", ())],
         "author_association": kw.get("assoc", "MEMBER"),
         "title": kw.get("title", f"PR {n}"), "body": kw.get("body", ""),
         "created_at": kw.get("created", "2026-02-01T00:00:00Z"),
         "updated_at": kw.get("created", "2026-02-01T00:00:00Z")}
    return d


def enr(**kw):
    return {"checks": {"verdict": kw.get("verdict", "green"), "total": kw.get("total", 10),
                       "success": kw.get("success", 10), "failure": kw.get("failure", 0)},
            "mergeable_state": kw.get("ms", "clean"),
            "last_author_at": kw.get("la"), "last_reviewer_at": kw.get("lr"),
            "review_state": kw.get("rs", "none")}


prs = [
    pr(1, labels=["to-be-merged"]),                              # land_ready
    pr(2, login="valkey-bot[bot]", title="backport foo"),       # bot
    pr(3, labels=["major-decision-pending"]),                   # needs_decision
    pr(4),                                                       # reviewer court (dormant → reengage)
    pr(5, assoc="NONE", title="my first fix"),                  # first-timer, author court (dormant → gentle)
    pr(6, labels=["to-be-closed"]),                             # flagged_close
    pr(7, title="Deflake defrag test"),                         # deflake overlay, reviewer court warm
    pr(8, body="superseded by #4200"),                          # superseded suggestion
    pr(9, draft=True),                                          # excluded
]
enriched = {
    1: enr(), 3: enr(),
    4: enr(la="2026-05-10T00:00:00Z", lr="2026-05-09T00:00:00Z"),   # reviewer court ~75d → reengage
    5: enr(verdict="failing", la="2026-03-01T00:00:00Z", lr="2026-03-05T00:00:00Z"),  # author court ~140d
    7: enr(la="2026-07-20T00:00:00Z", lr="2026-07-19T00:00:00Z"),   # reviewer court warm
    8: enr(la="2026-07-20T00:00:00Z", lr="2026-07-19T00:00:00Z"),   # reviewer court warm
    # 6 flagged_close needs enr for court? no — lane decided by label
    6: enr(),
}

res = B.bucketize(prs, enriched, now=NOW)
out = build_outreach(res, {p["number"]: p for p in prs})

check("reconciled", res["reconciled"])
md = build_report(prs, res, out)
html = build_report_html(prs, "2026-07-24 20:55 UTC", res, out, weeks=[])

# markdown assertions
for needle in ["# Valkey PR Health Report", "🟢 Land-ready", "🤖 Bot / backport",
               "👀 Ball in Reviewer's Court", "🗳 Needs a Decision", "🌱 First-Time Contributors",
               "🔥 Deflake", "📮 Outreach Dry-Run", "✍️ Ball in Author's Court",
               "Re-engage", "Closure candidates", "Maintainer-flagged", "Possibly superseded"]:
    check(f"md has: {needle}", needle in md)
check("md land-ready before author-court", md.index("Land-ready") < md.index("Author's Court"))
check("md no removed leaderboard", "Top Contributors" not in md)
check("md no CI-burden section", "High CI Burden" not in md)

# html assertions
for needle in ["Live PR Health Report", "By the Numbers", "Land-ready",
               "Ball in Reviewer&#x27;s Court" if False else "Ball in Reviewer's Court",
               "Outreach Dry-Run", "Dry-run only", "draft message", "First-Time Contributors",
               "chart.js"]:
    check(f"html has: {needle}", needle in html)
check("html land-ready before author-court", html.index("Land-ready") < html.index("Author's Court"))
# anchors + shareable/section links
for anc in ['id="by-the-numbers"', 'id="land-ready"', 'id="reviewer-court"',
            'id="author-court"', 'id="outreach"', 'id="charts"']:
    check(f"html anchor {anc}", anc in html)
check("by-the-numbers row links to section", 'class="lane-link" href="#reviewer-court"' in html)
check("section header is self-link", 'class="anchor-link" href="#author-court"' in html)
check("smooth scroll + scroll-margin css", "scroll-margin-top" in html and "scroll-behavior: smooth" in html)
check("html gentle nudge (no close threat for first-timer PR5)",
      "will be closed" not in [c["draft_message"] for c in out["closure_abandoned"] if c["number"] == 5][0])

# write samples for inspection (temp dir — not committed)
with open("/tmp/wt-sample-report.md", "w") as f:
    f.write(md)
with open("/tmp/wt-sample-report.html", "w") as f:
    f.write(html)

print(f"\n{'ALL PASS' if _fail == 0 else str(_fail) + ' FAILED'}  (md {len(md)}B, html {len(html)}B)")
sys.exit(1 if _fail else 0)
