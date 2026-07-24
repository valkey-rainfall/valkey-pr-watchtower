#!/usr/bin/env python3
"""Offline unit tests for outreach.py (no network). Run: python scripts/test_outreach.py"""
import sys
from datetime import datetime, timezone
import buckets as B
import outreach as O

NOW = datetime(2026, 7, 24, tzinfo=timezone.utc)
_fail = 0


def check(name, got, want):
    global _fail
    ok = got == want
    if not ok:
        _fail += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}  got={got!r} want={want!r}")


def pr(n, *, login="alice", labels=(), assoc="MEMBER", title="t", body=""):
    return {"number": n, "draft": False, "user": {"login": login},
            "labels": [{"name": l} for l in labels], "author_association": assoc,
            "title": title, "body": body, "created_at": "2026-01-01T00:00:00Z"}


def enr(*, verdict="green", mergeable_state="clean", la=None, lr=None, review_state="none"):
    return {"checks": {"verdict": verdict}, "mergeable_state": mergeable_state,
            "last_author_at": la, "last_reviewer_at": lr, "review_state": review_state}


# reviewer court (author acted last): last activity = la
REV_70D = enr(la="2026-05-15T00:00:00Z", lr="2026-05-14T00:00:00Z")   # ~70d dormant
REV_40D = enr(la="2026-06-14T00:00:00Z", lr="2026-06-13T00:00:00Z")   # ~40d dormant
REV_WARM = enr(la="2026-07-20T00:00:00Z", lr="2026-07-19T00:00:00Z")  # warm
# author court (reviewer acted last): last activity = lr
AUTH_120D_CR = enr(la="2026-03-20T00:00:00Z", lr="2026-03-26T00:00:00Z", review_state="changes_requested")
AUTH_120D_FAIL = enr(verdict="failing", la="2026-03-26T00:00:00Z", lr="2026-03-20T00:00:00Z")
AUTH_120D_DIRTY = enr(mergeable_state="dirty", la="2026-03-26T00:00:00Z", lr="2026-03-20T00:00:00Z")


def run(prs, enriched):
    res = B.bucketize(prs, enriched, now=NOW)
    return O.build_outreach(res, {p["number"]: p for p in prs})


def test_reengage():
    prs = [pr(1), pr(2)]
    o = run(prs, {1: REV_70D, 2: REV_40D})
    nums = [c["number"] for c in o["reengage"]]
    check("reengage fires at 70d", 1 in nums, True)
    check("reengage skips 40d", 2 in nums, False)
    c = next(c for c in o["reengage"] if c["number"] == 1)
    check("reengage action", c["proposed_action"], O.ACT_REENGAGE)
    check("reengage has draft", bool(c["draft_message"]), True)
    check("reengage evidence mentions awaiting review",
          any("awaiting review" in e for e in c["evidence"]), True)


def test_closure():
    prs = [pr(1), pr(2), pr(3)]
    o = run(prs, {1: AUTH_120D_CR, 2: AUTH_120D_FAIL, 3: AUTH_120D_DIRTY})
    nums = {c["number"]: c for c in o["closure_abandoned"]}
    check("closure fires for 3 author-court dormant", sorted(nums), [1, 2, 3])
    check("closure action", nums[1]["proposed_action"], O.ACT_CLOSE)
    check("closure needs=address feedback", "address the review feedback" in nums[1]["draft_message"], True)
    check("closure needs=fix CI", "fix the failing CI" in nums[2]["draft_message"], True)
    check("closure needs=rebase", "rebase" in nums[3]["draft_message"], True)


def test_closure_not_yet():
    # author court but only ~40d dormant → no closure
    prs = [pr(1)]
    o = run(prs, {1: enr(verdict="failing", la="2026-06-14T00:00:00Z", lr="2026-06-10T00:00:00Z")})
    check("no closure under 90d", o["closure_abandoned"], [])


def test_first_timer_gentle():
    prs = [pr(1, assoc="NONE")]
    o = run(prs, {1: AUTH_120D_FAIL})
    check("one candidate", len(o["closure_abandoned"]), 1)
    c = o["closure_abandoned"][0]
    check("first-timer → gentle nudge action", c["proposed_action"], O.ACT_NUDGE)
    check("first-timer classification", c["classification"], "abandoned_first_timer")
    check("gentle flag", c.get("gentle"), True)
    check("no closure threat in draft", "will be closed" not in c["draft_message"], True)


def test_flagged_close():
    prs = [pr(1, labels=["to-be-closed"])]
    o = run(prs, {1: enr()})
    check("maintainer_flagged_close list", [c["number"] for c in o["maintainer_flagged_close"]], [1])
    check("flagged action", o["maintainer_flagged_close"][0]["proposed_action"], O.ACT_MERGE_OR_CLOSE)


def test_priority_label():
    prs = [pr(1, labels=["still-wanted"])]
    o = run(prs, {1: REV_WARM})
    check("still-wanted → priority list", [c["number"] for c in o["priority_owed_review"]], [1])


def test_superseded():
    prs = [pr(1, body="This is superseded by #4200, closing soon.", title="old approach")]
    o = run(prs, {1: REV_WARM})
    check("superseded extracted", o["superseded_suggestions"][0]["superseded_by"], 4200)
    check("superseded verify-only action", o["superseded_suggestions"][0]["proposed_action"], O.ACT_VERIFY_SUPERSEDE)
    check("superseded no auto draft", o["superseded_suggestions"][0]["draft_message"], None)
    check("extract 'replaced by' form", O.extract_superseded_ref(pr(9, body="replaced by 4321")), 4321)
    check("extract none", O.extract_superseded_ref(pr(9, body="unrelated text")), None)


if __name__ == "__main__":
    for t in (test_reengage, test_closure, test_closure_not_yet, test_first_timer_gentle,
              test_flagged_close, test_priority_label, test_superseded):
        t()
    print(f"\n{'ALL PASS' if _fail == 0 else str(_fail) + ' FAILED'}")
    sys.exit(1 if _fail else 0)
