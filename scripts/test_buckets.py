#!/usr/bin/env python3
"""Offline unit tests for buckets.py (no network). Run: python scripts/test_buckets.py"""
import sys
from datetime import datetime, timezone
import buckets as B

NOW = datetime(2026, 7, 24, tzinfo=timezone.utc)
_fail = 0


def check(name, got, want):
    global _fail
    ok = got == want
    if not ok:
        _fail += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}  got={got!r} want={want!r}")


def pr(n, *, draft=False, login="alice", labels=(), assoc="MEMBER", title="t", created="2026-01-01T00:00:00Z"):
    return {"number": n, "draft": draft, "user": {"login": login},
            "labels": [{"name": l} for l in labels], "author_association": assoc,
            "title": title, "created_at": created}


def enr(*, verdict="green", mergeable_state="clean", la=None, lr=None, review_state="none"):
    return {"checks": {"verdict": verdict}, "mergeable_state": mergeable_state,
            "last_author_at": la, "last_reviewer_at": lr, "review_state": review_state}


def test_lanes():
    check("draft", B.assign_lane(pr(1, draft=True), None), B.LANE_EXCLUDED_DRAFT)
    check("bot author", B.assign_lane(pr(2, login="valkey-bot[bot]"), None), B.LANE_BOT_BACKPORT)
    check("backport label", B.assign_lane(pr(3, labels=["backport-8.0"]), None), B.LANE_BOT_BACKPORT)
    check("to-be-closed", B.assign_lane(pr(4, labels=["to-be-closed"]), enr()), B.LANE_FLAGGED_CLOSE)
    check("stalled", B.assign_lane(pr(5, labels=["stalled"]), enr()), B.LANE_FLAGGED_CLOSE)
    check("approved+green", B.assign_lane(pr(6, labels=["major-decision-approved"]), enr()), B.LANE_LAND_READY)
    check("to-be-merged", B.assign_lane(pr(7, labels=["to-be-merged"]), enr()), B.LANE_LAND_READY)
    # approved but CI failing → not land-ready, falls to author court (override)
    check("approved+failing→author", B.assign_lane(pr(8, labels=["major-decision-approved"],),
          enr(verdict="failing", lr="2026-01-02T00:00:00Z", la="2026-01-01T00:00:00Z")), B.LANE_AUTHOR_COURT)
    check("decision-pending", B.assign_lane(pr(9, labels=["major-decision-pending"]), enr()), B.LANE_NEEDS_DECISION)
    # reviewer court: author acted last (la > lr), green
    check("reviewer court (author last)", B.assign_lane(pr(10),
          enr(la="2026-05-01T00:00:00Z", lr="2026-04-01T00:00:00Z")), B.LANE_REVIEWER_COURT)
    # author court: reviewer acted last (lr > la)
    check("author court (reviewer last)", B.assign_lane(pr(11),
          enr(la="2026-04-01T00:00:00Z", lr="2026-05-01T00:00:00Z")), B.LANE_AUTHOR_COURT)
    # author court via CI failing even though author acted last
    check("author court (CI red override)", B.assign_lane(pr(12),
          enr(verdict="failing", la="2026-05-01T00:00:00Z", lr="2026-04-01T00:00:00Z")), B.LANE_AUTHOR_COURT)
    # author court via conflicts
    check("author court (dirty override)", B.assign_lane(pr(13),
          enr(mergeable_state="dirty", la="2026-05-01T00:00:00Z", lr="2026-04-01T00:00:00Z")), B.LANE_AUTHOR_COURT)
    # never reviewed → reviewer court
    check("never reviewed → reviewer", B.assign_lane(pr(14), enr(la="2026-05-01T00:00:00Z", lr=None)), B.LANE_REVIEWER_COURT)
    # non-draft non-bot, no enrichment → unknown
    check("no enrichment → unknown", B.assign_lane(pr(15), None), B.LANE_UNKNOWN)


def test_overlays():
    check("first_timer (NONE)", "first_timer" in B.overlays(pr(1, assoc="NONE")), True)
    check("first_timer not for bot", "first_timer" in B.overlays(pr(2, login="x[bot]", assoc="NONE")), False)
    check("deflake title", "deflake" in B.overlays(pr(3, title="Deflake active-defrag test")), True)
    check("community_approved", "community_approved" in B.overlays(pr(4, labels=["major-decision-approved"])), True)
    check("no overlays", B.overlays(pr(5, assoc="MEMBER", title="normal fix")), set())


def test_dormancy():
    check("warm", B.dormancy_tier(10), "warm")
    check("cooling", B.dormancy_tier(60), "cooling")
    check("dormant", B.dormancy_tier(120), "dormant")
    check("stale", B.dormancy_tier(300), "stale")
    check("ancient", B.dormancy_tier(500), "ancient")
    check("unknown", B.dormancy_tier(None), "unknown")


def test_reconciliation():
    prs = [
        pr(1, draft=True),
        pr(2, login="bot[bot]"),
        pr(3, labels=["to-be-closed"]),
        pr(4, labels=["to-be-merged"]),
        pr(5, labels=["major-decision-pending"]),
        pr(6), pr(7), pr(8),
    ]
    enriched = {
        3: enr(), 4: enr(), 5: enr(),
        6: enr(la="2026-05-01T00:00:00Z", lr="2026-04-01T00:00:00Z"),   # reviewer court
        7: enr(la="2026-04-01T00:00:00Z", lr="2026-05-01T00:00:00Z"),   # author court
        # 8: intentionally missing enrichment → unknown
    }
    res = B.bucketize(prs, enriched, now=NOW)
    check("reconciled flag", res["reconciled"], True)
    check("sum(counts)==total", sum(res["counts"].values()), len(prs))
    check("by_number size", len(res["by_number"]), len(prs))
    # each PR appears in exactly one lane
    seen = [e["number"] for lane in res["lanes"].values() for e in lane]
    check("no PR in two lanes", sorted(seen), sorted(p["number"] for p in prs))
    check("PR8 unknown", res["by_number"][8]["lane"], B.LANE_UNKNOWN)
    check("PR6 reviewer_court", res["by_number"][6]["lane"], B.LANE_REVIEWER_COURT)
    # dormancy computed from last activity (PR6 last activity 2026-05-01 → ~84d @ NOW)
    check("PR6 dormancy tier", res["by_number"][6]["dormancy_tier"], "cooling")


if __name__ == "__main__":
    test_lanes()
    test_overlays()
    test_dormancy()
    test_reconciliation()
    print(f"\n{'ALL PASS' if _fail == 0 else str(_fail) + ' FAILED'}")
    sys.exit(1 if _fail else 0)
