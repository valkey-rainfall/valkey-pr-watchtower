#!/usr/bin/env python3
"""Offline unit tests for enrich.py pure helpers (no network). Run: python scripts/test_enrich.py"""
import sys
from enrich import derive_review_state, summarize_checks, split_activity, _max_ts

_fail = 0


def check(name, got, want):
    global _fail
    ok = got == want
    if not ok:
        _fail += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}  got={got!r} want={want!r}")


def test_review_state():
    check("no reviews", derive_review_state([]), "none")
    check("only comments", derive_review_state([{"user": {"login": "a"}, "state": "COMMENTED"}]), "commented")
    check("approved", derive_review_state([{"user": {"login": "a"}, "state": "APPROVED"}]), "approved")
    check("cr dominates approve",
          derive_review_state([{"user": {"login": "a"}, "state": "APPROVED"},
                               {"user": {"login": "b"}, "state": "CHANGES_REQUESTED"}]), "changes_requested")
    check("reviewer re-approves overrides own CR",
          derive_review_state([{"user": {"login": "b"}, "state": "CHANGES_REQUESTED"},
                               {"user": {"login": "b"}, "state": "APPROVED"}]), "approved")
    check("dismissed clears standing",
          derive_review_state([{"user": {"login": "b"}, "state": "CHANGES_REQUESTED"},
                               {"user": {"login": "b"}, "state": "DISMISSED"}]), "none")


def test_checks_verdict():
    runs = ([{"status": "completed", "conclusion": "success"}] * 27 +
            [{"status": "completed", "conclusion": "skipped"}] * 70 +
            [{"status": "completed", "conclusion": "neutral"}] * 3)
    v = summarize_checks(runs)
    check("green despite 73 neutral", v["verdict"], "green")
    check("success count", v["success"], 27)
    check("neutral count", v["neutral"], 73)
    check("failing", summarize_checks([{"status": "completed", "conclusion": "failure"}])["verdict"], "failing")
    check("pending", summarize_checks([{"status": "in_progress", "conclusion": None}])["verdict"], "pending")
    check("none", summarize_checks([])["verdict"], "none")
    check("failure beats pending",
          summarize_checks([{"status": "completed", "conclusion": "failure"},
                            {"status": "queued", "conclusion": None}])["verdict"], "failing")


def test_split_activity():
    pr = {"user": {"login": "auth"}, "created_at": "2026-01-01T00:00:00Z"}
    commits = [{"commit": {"committer": {"date": "2026-03-01T00:00:00Z"},
                           "author": {"date": "2026-03-01T00:00:00Z"}}}]
    icomments = [{"user": {"login": "rev"}, "created_at": "2026-04-01T00:00:00Z"}]
    rcomments = [{"user": {"login": "auth"}, "created_at": "2026-02-01T00:00:00Z"}]
    reviews = [{"user": {"login": "rev"}, "submitted_at": "2026-05-01T00:00:00Z"}]
    la, lr = split_activity(pr, commits, icomments, rcomments, reviews)
    check("last_author = commit 03-01", la[:10], "2026-03-01")
    check("last_reviewer = review 05-01", lr[:10], "2026-05-01")
    check("_max_ts ignores None", _max_ts(None, "2026-01-01T00:00:00Z", None)[:10], "2026-01-01")
    check("_max_ts all None", _max_ts(None, None), None)


if __name__ == "__main__":
    test_review_state()
    test_checks_verdict()
    test_split_activity()
    print(f"\n{'ALL PASS' if _fail == 0 else str(_fail) + ' FAILED'}")
    sys.exit(1 if _fail else 0)
