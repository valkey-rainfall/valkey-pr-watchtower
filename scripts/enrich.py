#!/usr/bin/env python3
"""
enrich.py — per-PR enrichment layer for valkey-pr-watchtower.

Given the open-PR list (from /repos/{repo}/pulls), compute the extra signals the
lane-bucketing engine needs but that the list endpoint does not provide:

  - review_state        : none | commented | approved | changes_requested
  - checks              : {total, success, failure, pending} from head-SHA check-runs
  - mergeable           : True | False | None (None = GitHub still computing)
  - mergeable_state     : clean | dirty | blocked | behind | unstable | unknown
  - last_author_at      : ISO ts of the author's most recent push OR comment (NOT updated_at)
  - last_reviewer_at    : ISO ts of the most recent activity by anyone other than the author
  - author_login        : convenience copy

Design notes
------------
* updated_at is deliberately NOT used as an activity signal: a stray reviewer
  comment or a bot re-label bumps it, masking real author silence. We derive
  last_author_at from the commit + comment + review timelines instead.
* This module is transport-agnostic: callers inject `gh_get` (single GET) and
  `gh_paginate` (paged GET) so the same code runs against build_report.py's
  rate-limited, retrying fetchers in production and against a bare urllib
  fetcher in tests / spot-checks.
* Court determination and dormancy thresholds live in the bucketing engine
  (Stage 2), not here. This layer only produces the raw signals.
"""

from datetime import datetime, timezone


# ── pure helpers (no network) ────────────────────────────────────────────────

def _parse_ts(ts):
    """ISO-8601 (with trailing Z) -> aware datetime, or None."""
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _max_ts(*ts_values):
    """Return the latest of several ISO timestamps as an ISO string, or None."""
    dts = [_parse_ts(t) for t in ts_values]
    dts = [d for d in dts if d is not None]
    if not dts:
        return None
    return max(dts).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def derive_review_state(reviews):
    """
    Collapse a PR's review list into a single standing state.

    Mirrors GitHub's own model: a reviewer's *standing* is their most recent
    APPROVED or CHANGES_REQUESTED review; a COMMENTED / DISMISSED review does
    not change their standing. Overall precedence: any outstanding
    changes_requested dominates; else any approval; else commented; else none.
    """
    standing = {}   # reviewer login -> "approved" | "changes_requested"
    any_comment = False
    for r in reviews:
        login = (r.get("user") or {}).get("login", "")
        state = (r.get("state") or "").upper()
        if state == "APPROVED":
            standing[login] = "approved"
        elif state == "CHANGES_REQUESTED":
            standing[login] = "changes_requested"
        elif state == "DISMISSED":
            standing.pop(login, None)
        elif state == "COMMENTED":
            any_comment = True
    values = set(standing.values())
    if "changes_requested" in values:
        return "changes_requested"
    if "approved" in values:
        return "approved"
    if any_comment:
        return "commented"
    return "none"


def summarize_checks(check_runs):
    """
    Reduce a check-runs list to a tally plus a single CI verdict.

    Buckets: success, failure (failure/timed_out/startup_failure), pending
    (not yet completed), neutral (completed but non-blocking: neutral / skipped
    / cancelled / stale / action_required). neutral runs must NOT count against
    "green" — Valkey's matrix emits many skipped/neutral runs, so a
    success==total test would mislabel nearly every green PR as amber.

    verdict:
      failing  -> at least one failure
      pending  -> no failures but some runs still running
      green    -> no failures, nothing pending (neutral/skipped ignored)
      none     -> no check-runs at all
    """
    checks = {"total": 0, "success": 0, "failure": 0, "pending": 0, "neutral": 0}
    for run in check_runs:
        checks["total"] += 1
        conclusion = run.get("conclusion")
        status = run.get("status")
        if conclusion == "success":
            checks["success"] += 1
        elif conclusion in ("failure", "timed_out", "startup_failure"):
            checks["failure"] += 1
        elif status != "completed":
            checks["pending"] += 1
        else:
            # completed but non-blocking: neutral, skipped, cancelled, stale, action_required
            checks["neutral"] += 1

    if checks["total"] == 0:
        checks["verdict"] = "none"
    elif checks["failure"] > 0:
        checks["verdict"] = "failing"
    elif checks["pending"] > 0:
        checks["verdict"] = "pending"
    else:
        checks["verdict"] = "green"
    return checks


def split_activity(pr, commits, issue_comments, review_comments, reviews):
    """
    Compute (last_author_at, last_reviewer_at) ISO strings from the timelines.

    author-side  = the PR opening, any commit on the branch, and any comment or
                   review authored by the PR author.
    reviewer-side = any comment or review authored by someone other than the
                   PR author (bots included — they represent external activity).
    """
    author = (pr.get("user") or {}).get("login", "")

    # Author side: PR creation is an author action; commits are author pushes.
    author_ts = [pr.get("created_at")]
    for c in commits:
        commit = c.get("commit") or {}
        author_ts.append((commit.get("committer") or {}).get("date"))
        author_ts.append((commit.get("author") or {}).get("date"))

    reviewer_ts = []
    for c in issue_comments:
        login = (c.get("user") or {}).get("login", "")
        (author_ts if login == author else reviewer_ts).append(c.get("created_at"))
    for c in review_comments:
        login = (c.get("user") or {}).get("login", "")
        (author_ts if login == author else reviewer_ts).append(c.get("created_at"))
    for r in reviews:
        login = (r.get("user") or {}).get("login", "")
        (author_ts if login == author else reviewer_ts).append(r.get("submitted_at"))

    return _max_ts(*author_ts), _max_ts(*reviewer_ts)


# ── network-bound enrichment ─────────────────────────────────────────────────

def enrich_pr(pr, gh_get, gh_paginate, repo="valkey-io/valkey"):
    """
    Fetch the per-PR signals for a single PR dict (as returned by the list
    endpoint). Returns a dict of enrichment fields. ~6 API calls per PR.
    """
    n = pr["number"]
    head_sha = ((pr.get("head") or {}).get("sha")) or ""

    # mergeable is computed lazily by GitHub; the pull detail endpoint triggers
    # and returns it (may still be None on a cold PR — caller can re-run).
    detail = gh_get(f"/repos/{repo}/pulls/{n}") or {}

    check_runs = []
    if head_sha:
        cr = gh_get(f"/repos/{repo}/commits/{head_sha}/check-runs", {"per_page": 100}) or {}
        check_runs = cr.get("check_runs", [])

    reviews = gh_paginate(f"/repos/{repo}/pulls/{n}/reviews") or []
    commits = gh_paginate(f"/repos/{repo}/pulls/{n}/commits") or []
    issue_comments = gh_paginate(f"/repos/{repo}/issues/{n}/comments") or []
    review_comments = gh_paginate(f"/repos/{repo}/pulls/{n}/comments") or []

    last_author_at, last_reviewer_at = split_activity(
        pr, commits, issue_comments, review_comments, reviews
    )

    return {
        "number": n,
        "author_login": (pr.get("user") or {}).get("login", ""),
        "review_state": derive_review_state(reviews),
        "checks": summarize_checks(check_runs),
        "mergeable": detail.get("mergeable"),
        "mergeable_state": detail.get("mergeable_state"),
        "last_author_at": last_author_at,
        "last_reviewer_at": last_reviewer_at,
        "commits_count": len(commits),
        "reviews_count": len(reviews),
    }


def enrich_all(prs, gh_get, gh_paginate, repo="valkey-io/valkey",
               include_drafts=False, include_bots=False, limit=None, progress=None):
    """
    Enrich a list of PRs. Skips drafts and bot authors by default (they are
    routed by dedicated lanes that don't need timeline enrichment). Returns a
    dict keyed by PR number. `limit` caps the number enriched (for spot-checks).
    """
    out = {}
    count = 0
    for pr in prs:
        if not include_drafts and pr.get("draft"):
            continue
        login = (pr.get("user") or {}).get("login", "")
        if not include_bots and login.endswith("[bot]"):
            continue
        if limit is not None and count >= limit:
            break
        out[pr["number"]] = enrich_pr(pr, gh_get, gh_paginate, repo=repo)
        count += 1
        if progress:
            progress(pr["number"], count)
    return out
