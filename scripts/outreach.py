#!/usr/bin/env python3
"""
outreach.py — stateless, label-aware outreach dry-run for valkey-pr-watchtower.

Consumes the Stage-2 bucketize() result and DERIVES outreach candidates. Emits,
per candidate: classification, the evidence that fired it, a proposed action, a
neutral-voice DRAFT message, and the direct link. It NEVER posts, closes, or
labels anything — it produces lists a human reviews and acts on.

Court-split dormancy (both clocks measure time since the last activity of any
kind, i.e. how long the PR has sat):
  - reviewer_court + dormant ≥ REENGAGE_DAYS  → re-engage (project apologises;
    author did their part, review never came)
  - author_court   + dormant ≥ CLOSURE_DAYS   → closure candidate (ball is the
    author's: CI red / conflict / unaddressed review, and gone quiet)

Retention guard: a first-time contributor in author_court is NEVER proposed for
closure — it downgrades to a gentle, no-threat nudge, so we don't scare off a
would-be regular.

Superseded is confirm-only: we only flag it when the PR text itself references
another PR as its replacement, and even then it is a "verify before acting"
suggestion, never a proposed action.

Label-driven priority (stateless): a PR carrying a STILL_WANTED label surfaces
on the "owed a review" priority list — no local state needed, the label on
GitHub is the state. That label doesn't exist yet; the list stays empty until
maintainers add one.
"""

import re

import buckets as B

# ── tunable thresholds (days since last activity) ────────────────────────────
REENGAGE_DAYS = 60     # reviewer's court: apologise sooner (project's fault)
CLOSURE_DAYS  = 90     # author's court: close slower

STILL_WANTED_LABELS = {"still-wanted", "revived"}   # future, maintainer-applied
SUPERSEDE_PATTERNS = (
    r"superseded by\s+#?(\d+)",
    r"replaced by\s+#?(\d+)",
    r"duplicate of\s+#?(\d+)",
    r"obsoletes?\s+#?(\d+)",
)

# proposed-action identifiers (what a human WOULD do — never done automatically)
ACT_CLOSE          = "comment_and_close"
ACT_REENGAGE       = "ping_reengage"
ACT_NUDGE          = "ping_gentle_nudge"
ACT_VERIFY_SUPERSEDE = "verify_supersede"
ACT_MERGE_OR_CLOSE = "review_flagged_close"


def _labels(pr):
    return {l["name"] for l in pr.get("labels", [])}


def _needs_phrase(enr):
    """What the author must do next, from the enrichment signals."""
    if not enr:
        return "follow up"
    if (enr.get("checks") or {}).get("verdict") == "failing":
        return "fix the failing CI"
    if enr.get("mergeable_state") == "dirty":
        return "rebase onto the latest unstable and resolve the conflicts"
    if enr.get("review_state") == "changes_requested":
        return "address the review feedback"
    return "push an update"


def _human_age(days):
    if days is None:
        return "a while"
    if days < 60:
        return f"{days} days"
    if days < 365:
        return f"about {days // 30} months"
    return f"over {days // 365} year" + ("s" if days // 365 > 1 else "")


def extract_superseded_ref(pr):
    """Return the PR number this PR says it's replaced by, or None. Text-only."""
    text = f"{pr.get('title','')}\n{pr.get('body','') or ''}".lower()
    for pat in SUPERSEDE_PATTERNS:
        m = re.search(pat, text)
        if m:
            return int(m.group(1))
    return None


# ── draft messages (neutral, warm-but-not-overpromising; marked DRAFT) ───────

def draft_reengage(entry):
    age = _human_age(entry["dormancy_days"])
    return (f"Thanks for this contribution, and apologies it has sat without a "
            f"review for {age}. Are you still interested in landing it? If so, a "
            f"quick rebase onto the current unstable will help reviewers pick it "
            f"back up. If not, no problem — just let us know and we can close it.")


def draft_closure(entry):
    needs = _needs_phrase(entry.get("enr"))
    age = _human_age(entry["dormancy_days"])
    return (f"This PR looks like it may have stalled — it needs someone to "
            f"{needs}, and there has been no update in {age}. If you are still "
            f"planning to finish it, please go ahead and it can stay open. "
            f"Otherwise it will be closed to keep the review queue focused; "
            f"you are welcome to reopen it anytime.")


def draft_nudge(entry):
    needs = _needs_phrase(entry.get("enr"))
    age = _human_age(entry["dormancy_days"])
    return (f"Thanks for opening this! It looks like it stalled — the next step "
            f"is to {needs}, and it has been quiet for {age}. Are you still "
            f"interested in finishing it? Happy to help if the next step is "
            f"unclear. No pressure either way.")


def _evidence(entry):
    """Human-readable reasons this candidate fired."""
    ev = []
    enr = entry.get("enr") or {}
    verdict = (enr.get("checks") or {}).get("verdict")
    if verdict == "failing":
        ev.append("CI failing")
    if enr.get("mergeable_state") == "dirty":
        ev.append("merge conflicts")
    if enr.get("review_state") == "changes_requested":
        ev.append("changes requested, not addressed")
    if entry.get("court") == "reviewer":
        ev.append("author acted last; awaiting review")
    ev.append(f"no activity in {_human_age(entry['dormancy_days'])}"
              f" ({entry['dormancy_tier']})")
    return ev


def _candidate(entry, classification, action, draft, extra=None):
    c = {
        "number": entry["number"],
        "title": entry["title"],
        "author": entry["author"],
        "url": entry["url"],
        "classification": classification,
        "proposed_action": action,
        "evidence": _evidence(entry),
        "draft_message": draft,
        "dormancy_days": entry["dormancy_days"],
        "first_timer": "first_timer" in entry.get("overlays", []),
    }
    if extra:
        c.update(extra)
    return c


def build_outreach(bucket_result, prs_by_num):
    """
    Derive outreach lists from a bucketize() result.

    Returns:
      {
        "priority_owed_review": [...],     # STILL_WANTED-labelled (label-driven)
        "maintainer_flagged_close": [...], # flagged_close lane (just close it)
        "reengage": [...],                 # reviewer_court + dormant ≥ REENGAGE_DAYS
        "closure_abandoned": [...],        # author_court + dormant ≥ CLOSURE_DAYS
        "superseded_suggestions": [...],   # text-referenced, verify-only
        "thresholds": {...},
      }
    """
    by_number = bucket_result["by_number"]
    out = {
        "priority_owed_review": [],
        "maintainer_flagged_close": [],
        "reengage": [],
        "closure_abandoned": [],
        "superseded_suggestions": [],
        "thresholds": {"reengage_days": REENGAGE_DAYS, "closure_days": CLOSURE_DAYS},
    }

    for num, entry in by_number.items():
        pr = prs_by_num.get(num, {})
        labels = _labels(pr)
        lane = entry["lane"]
        dd = entry["dormancy_days"]

        # Label-driven priority list (stateless): surfaces regardless of lane.
        if labels & STILL_WANTED_LABELS:
            out["priority_owed_review"].append(_candidate(
                entry, "owed_review", ACT_REENGAGE, draft_reengage(entry),
                extra={"reason": "carries a still-wanted / revived label"}))

        # Maintainer already flagged for closure — just needs the click.
        if lane == B.LANE_FLAGGED_CLOSE:
            out["maintainer_flagged_close"].append(_candidate(
                entry, "flagged_close", ACT_MERGE_OR_CLOSE, None,
                extra={"labels": sorted(labels & B.CLOSE_LABELS)}))

        # Re-engage: project's fault, apologise sooner.
        if lane == B.LANE_REVIEWER_COURT and dd is not None and dd >= REENGAGE_DAYS:
            out["reengage"].append(_candidate(
                entry, "reengage", ACT_REENGAGE, draft_reengage(entry)))

        # Closure candidate: ball is author's and gone quiet.
        if lane == B.LANE_AUTHOR_COURT and dd is not None and dd >= CLOSURE_DAYS:
            if "first_timer" in entry.get("overlays", []):
                # Retention guard: never threaten closure on a first PR.
                out["closure_abandoned"].append(_candidate(
                    entry, "abandoned_first_timer", ACT_NUDGE, draft_nudge(entry),
                    extra={"gentle": True}))
            else:
                out["closure_abandoned"].append(_candidate(
                    entry, "abandoned", ACT_CLOSE, draft_closure(entry)))

        # Superseded: confirm-only, text-referenced.
        ref = extract_superseded_ref(pr)
        if ref and lane not in (B.LANE_EXCLUDED_DRAFT, B.LANE_FLAGGED_CLOSE):
            out["superseded_suggestions"].append(_candidate(
                entry, "possibly_superseded", ACT_VERIFY_SUPERSEDE, None,
                extra={"superseded_by": ref,
                       "note": f"PR text references #{ref} as its replacement — "
                               f"verify #{ref} is merged and equivalent before acting"}))

    return out
