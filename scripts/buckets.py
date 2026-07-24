#!/usr/bin/env python3
"""
buckets.py — lane-bucketing engine for valkey-pr-watchtower.

Assigns every open PR to exactly ONE primary lane (priority-ordered, mutually
exclusive) and computes the attributes the report + outreach layers need:
court (whose move is next), dormancy, and independent overlay flags.

Lanes reconcile to the total: sum(lane counts) == len(prs), and no PR is in two
exclusive lanes. The outreach classification (Stage 3) is DERIVED from
(lane, court, dormancy_days), not a separate exclusive lane — so it can overlap
the closure/re-engage view without breaking reconciliation here.

Inputs
------
prs      : list of PR dicts from /repos/{repo}/pulls (labels, draft, user,
           author_association, created_at, ...)
enriched : dict {pr_number: enrichment} from enrich.py (review_state, checks,
           mergeable_state, last_author_at, last_reviewer_at). May omit drafts
           and bots — those lanes are decided from list fields alone.
"""

from datetime import datetime, timezone

# ── lane identifiers, in priority order (first match wins) ───────────────────
LANE_EXCLUDED_DRAFT = "excluded_draft"
LANE_BOT_BACKPORT   = "bot_backport"
LANE_FLAGGED_CLOSE  = "flagged_close"      # maintainer already labelled to-be-closed / stalled
LANE_LAND_READY     = "land_ready"         # approved/to-be-merged, CI ok, no conflict
LANE_NEEDS_DECISION = "needs_decision"     # major-decision-pending / -deferred
LANE_REVIEWER_COURT = "reviewer_court"     # author acted last → awaiting review
LANE_AUTHOR_COURT   = "author_court"       # CI red / conflict / reviewer waiting on author
LANE_UNKNOWN        = "unknown"            # non-draft/non-bot but no enrichment available

# Display/priority order (also the actionability order used by the report).
LANE_ORDER = [
    LANE_LAND_READY,
    LANE_BOT_BACKPORT,
    LANE_REVIEWER_COURT,
    LANE_NEEDS_DECISION,
    LANE_FLAGGED_CLOSE,
    LANE_AUTHOR_COURT,
    LANE_UNKNOWN,
    LANE_EXCLUDED_DRAFT,
]

DECISION_LABELS = {"major-decision-pending", "major-decision-deferred"}
APPROVED_LABELS = {"major-decision-approved", "to-be-merged"}
CLOSE_LABELS    = {"to-be-closed", "stalled"}

DEFLAKE_KEYWORDS = ("flak", "deflak", "stale tmpdir", "timing")

# Dormancy tier boundaries (days since last activity).
def dormancy_tier(days):
    if days is None:
        return "unknown"
    if days < 30:
        return "warm"
    if days < 90:
        return "cooling"
    if days < 180:
        return "dormant"
    if days < 365:
        return "stale"
    return "ancient"


def _labels(pr):
    return {l["name"] for l in pr.get("labels", [])}


def _login(pr):
    return (pr.get("user") or {}).get("login", "")


def _is_bot(pr):
    return _login(pr).endswith("[bot]")


def _is_backport(pr):
    labels = _labels(pr)
    return _is_bot(pr) or any("backport" in l.lower() for l in labels)


def _parse(ts):
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _days_since(ts, now):
    dt = _parse(ts)
    if dt is None:
        return None
    return (now - dt).days


def court(enr):
    """
    Whose move is next: 'author' | 'reviewer'.

    Overrides (ball is the author's regardless of who spoke last):
      - CI failing  → author must fix
      - conflicts   → author must rebase
    Otherwise whoever acted LAST is not the one we wait on:
      - reviewer acted after author (lr > la) → waiting on author
      - author acted last, or nobody reviewed → waiting on a reviewer
    A changes_requested review with no author push since is naturally captured
    by lr > la → author court.
    """
    if not enr:
        return None
    if (enr.get("checks") or {}).get("verdict") == "failing":
        return "author"
    if enr.get("mergeable_state") == "dirty":
        return "author"
    la = _parse(enr.get("last_author_at"))
    lr = _parse(enr.get("last_reviewer_at"))
    if lr is None:
        return "reviewer"          # never reviewed → awaiting first review
    if la is None:
        return "reviewer"
    return "author" if lr > la else "reviewer"


def last_activity_at(enr):
    """Most recent activity of any kind (max of author/reviewer timestamps)."""
    if not enr:
        return None
    la = _parse(enr.get("last_author_at"))
    lr = _parse(enr.get("last_reviewer_at"))
    dts = [d for d in (la, lr) if d]
    if not dts:
        return None
    return max(dts).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def assign_lane(pr, enr):
    """Return the single primary lane for a PR (priority-ordered, first match)."""
    if pr.get("draft"):
        return LANE_EXCLUDED_DRAFT
    if _is_backport(pr):
        return LANE_BOT_BACKPORT
    labels = _labels(pr)
    if labels & CLOSE_LABELS:
        return LANE_FLAGGED_CLOSE
    verdict = (enr.get("checks") or {}).get("verdict") if enr else None
    dirty = enr.get("mergeable_state") == "dirty" if enr else False
    if labels & APPROVED_LABELS and verdict != "failing" and not dirty:
        return LANE_LAND_READY
    if labels & DECISION_LABELS:
        return LANE_NEEDS_DECISION
    c = court(enr)
    if c == "reviewer":
        return LANE_REVIEWER_COURT
    if c == "author":
        return LANE_AUTHOR_COURT
    return LANE_UNKNOWN


def overlays(pr):
    """Independent (non-exclusive) flags that re-surface a PR for attention."""
    flags = set()
    assoc = (pr.get("author_association") or "").upper()
    if assoc in ("FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER", "NONE") and not _is_bot(pr):
        flags.add("first_timer")
    title = (pr.get("title") or "").lower()
    if any(k in title for k in DEFLAKE_KEYWORDS):
        flags.add("deflake")
    if "major-decision-approved" in _labels(pr):
        flags.add("community_approved")
    return flags


def bucketize(prs, enriched, now=None):
    """
    Assign lanes + attributes to every PR.

    Returns:
      {
        "now": iso,
        "lanes": {lane: [entry, ...]},          # entries in each lane
        "counts": {lane: n},                    # per-lane count
        "by_number": {num: entry},              # flat index
        "total": len(prs),
        "reconciled": bool,                     # sum(counts)==total and disjoint
      }
    Each entry: {number, title, author, lane, court, overlays,
                 dormancy_days, dormancy_tier, last_activity_at, url, enr}
    """
    now = now or datetime.now(timezone.utc)
    lanes = {lane: [] for lane in LANE_ORDER}
    by_number = {}

    for pr in prs:
        n = pr["number"]
        enr = enriched.get(n)
        lane = assign_lane(pr, enr)
        last_act = last_activity_at(enr)
        dd = _days_since(last_act, now)
        entry = {
            "number": n,
            "title": pr.get("title", ""),
            "author": _login(pr),
            "created_at": pr.get("created_at"),
            "lane": lane,
            "court": court(enr),
            "overlays": sorted(overlays(pr)),
            "dormancy_days": dd,
            "dormancy_tier": dormancy_tier(dd),
            "last_activity_at": last_act,
            "url": f"https://github.com/valkey-io/valkey/pull/{n}",
            "enr": enr,
        }
        lanes.setdefault(lane, []).append(entry)
        by_number[n] = entry

    counts = {lane: len(v) for lane, v in lanes.items()}
    reconciled = (sum(counts.values()) == len(prs)) and (len(by_number) == len(prs))
    return {
        "now": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "lanes": lanes,
        "counts": counts,
        "by_number": by_number,
        "total": len(prs),
        "reconciled": reconciled,
    }
