"""HTML report builder for valkey-pr-watchtower.

Renders the actionability-ordered lane report + stateless outreach dry-run from a
buckets.bucketize() result and an outreach.build_outreach() result. Section order
(top = most immediately actionable):

  By the Numbers → Owed a Review (if any) → Land-ready → Bot/backport quick-wins
  → First-time contributors → Ball in reviewer's court → Needs a decision
  → Deflake/test-fix → Outreach dry-run (re-engage / closure / superseded /
  maintainer-flagged) → Ball in author's court → Charts
"""
from datetime import datetime, timezone

import buckets as B


def _age_days(dt_str):
    if not dt_str:
        return None
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def _age_str(days):
    if days is None:
        return "—"
    if days < 14:
        return f"{days}d"
    if days < 60:
        return f"{days // 7}w"
    if days < 365:
        return f"{days // 30}mo"
    return f"{days / 365:.1f}y"


def _pr_link(entry):
    n = entry["number"]
    return f'<a href="{entry["url"]}" target="_blank" rel="noopener noreferrer">#{n}</a>'


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _title(entry, n=60):
    t = entry.get("title", "")
    return _esc(t[:n] + ("…" if len(t) > n else ""))


def _table(headers, rows):
    h = "".join(f"<th>{hdr}</th>" for hdr in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>\n"
    return f"<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>"


def _panel(title, badge_text, content, scroll=False, anchor=None):
    body_cls = "panel-body-scroll" if scroll else "panel-body"
    id_attr = f' id="{anchor}"' if anchor else ""
    # Self-linking header: clicking the title sets the URL hash (shareable link).
    title_html = (f'<a class="anchor-link" href="#{anchor}">{title}</a>'
                  if anchor else title)
    return (f'<div class="panel"{id_attr} style="margin-bottom:12px;">'
            f'<div class="panel-header"><span>{title_html}</span>'
            f'<span class="badge badge-ai">{badge_text}</span></div>'
            f'<div class="{body_cls}">{content}</div></div>')


def _ci_badge(enr):
    """CI + merge badge from an enrichment dict (verdict-based, not success==total)."""
    if not enr:
        return '<span class="muted">—</span>'
    checks = enr.get("checks") or {}
    verdict = checks.get("verdict", "none")
    total = checks.get("total", 0)
    success = checks.get("success", 0)
    if verdict == "failing":
        ci = f'<span class="danger">❌ {checks.get("failure", 0)}/{total} failing</span>'
    elif verdict == "pending":
        ci = f'<span class="warn">⏳ {success}/{total} running</span>'
    elif verdict == "green":
        ci = f'<span class="ok">✅ green</span>'
    else:
        ci = '<span class="muted">no checks</span>'
    ms = enr.get("mergeable_state")
    if ms == "dirty":
        ci += ' · <span class="danger">conflicts</span>'
    elif ms == "clean":
        ci += ' · <span class="ok">mergeable</span>'
    return ci


def _blocked_reason(enr):
    if not enr:
        return "—"
    if (enr.get("checks") or {}).get("verdict") == "failing":
        return '<span class="danger">CI failing</span>'
    if enr.get("mergeable_state") == "dirty":
        return '<span class="danger">merge conflict</span>'
    if enr.get("review_state") == "changes_requested":
        return '<span class="warn">changes requested</span>'
    return '<span class="muted">awaiting author</span>'


def _dormancy_cell(entry):
    dd = entry.get("dormancy_days")
    tier = entry.get("dormancy_tier", "unknown")
    cls = {"warm": "ok", "cooling": "", "dormant": "warn",
           "stale": "danger", "ancient": "danger"}.get(tier, "muted")
    return f'<span class="{cls}">{_age_str(dd)} idle</span>'


# ── lane renderers ───────────────────────────────────────────────────────────

def _lane_land_ready(entries):
    rows = [[_pr_link(e), _title(e), _esc(e["author"]),
             _age_str(_age_days(e["created_at"])), _ci_badge(e.get("enr"))]
            for e in sorted(entries, key=lambda e: e["created_at"] or "")]
    return _table(["PR", "Title", "Author", "Age", "CI + merge"], rows)


def _lane_bot(entries):
    rows = [[_pr_link(e), _title(e), _esc(e["author"]),
             _age_str(_age_days(e["created_at"]))]
            for e in sorted(entries, key=lambda e: e["created_at"] or "")]
    return _table(["PR", "Title", "Author", "Age"], rows)


def _lane_reviewer(entries):
    rows = [[_pr_link(e), _title(e), _esc(e["author"]),
             _ci_badge(e.get("enr")), _dormancy_cell(e)]
            for e in sorted(entries, key=lambda e: e.get("dormancy_days") or 0, reverse=True)]
    return _table(["PR", "Title", "Author", "CI + merge", "Waiting"], rows)


def _lane_decision(entries):
    rows = [[_pr_link(e), _title(e), _esc(e["author"]), _age_str(_age_days(e["created_at"]))]
            for e in sorted(entries, key=lambda e: e["created_at"] or "")]
    return _table(["PR", "Title", "Author", "Age"], rows)


def _lane_author(entries):
    rows = [[_pr_link(e), _title(e), _esc(e["author"]),
             _blocked_reason(e.get("enr")), _dormancy_cell(e)]
            for e in sorted(entries, key=lambda e: e.get("dormancy_days") or 0, reverse=True)]
    return _table(["PR", "Title", "Author", "Blocked on", "Idle"], rows)


def _overlay_rows(entries, extra_col=None):
    rows = []
    for e in sorted(entries, key=lambda e: e["created_at"] or "", reverse=True):
        row = [_pr_link(e), _title(e), _esc(e["author"]), _age_str(_age_days(e["created_at"]))]
        if extra_col:
            row.append(extra_col(e))
        rows.append(row)
    return rows


# ── outreach renderers ───────────────────────────────────────────────────────

def _outreach_rows(candidates):
    rows = []
    for c in candidates:
        link = f'<a href="{c["url"]}" target="_blank" rel="noopener noreferrer">#{c["number"]}</a>'
        evidence = "; ".join(_esc(x) for x in c.get("evidence", []))
        action = f'<code>{_esc(c.get("proposed_action", ""))}</code>'
        draft = c.get("draft_message")
        note = c.get("note")
        detail = ""
        if draft:
            detail = (f'<details><summary class="muted" style="cursor:pointer">draft message</summary>'
                      f'<div style="white-space:pre-wrap;font-size:0.85em;padding:6px 0">{_esc(draft)}</div></details>')
        elif note:
            detail = f'<span class="muted" style="font-size:0.85em">{_esc(note)}</span>'
        rows.append([link, _title(c, 45), _esc(c["author"]), evidence, action, detail])
    return _table(["PR", "Title", "Author", "Evidence", "Proposed action", "Detail"], rows)


# ── charts (age histogram + weekly activity) ─────────────────────────────────

def _build_charts(prs, non_draft, weeks):
    import json as _json
    buckets = {"0-2w": 0, "2-4w": 0, "1-3mo": 0, "3-6mo": 0, "6-12mo": 0, "1y+": 0}
    for pr in non_draft:
        days = _age_days(pr["created_at"]) or 0
        if days <= 14: buckets["0-2w"] += 1
        elif days <= 28: buckets["2-4w"] += 1
        elif days <= 90: buckets["1-3mo"] += 1
        elif days <= 180: buckets["3-6mo"] += 1
        elif days <= 365: buckets["6-12mo"] += 1
        else: buckets["1y+"] += 1
    labels_hist = _json.dumps(list(buckets.keys()))
    data_hist = _json.dumps(list(buckets.values()))
    if weeks:
        week_labels = _json.dumps([w["week_start"] for w in weeks])
        opened_data = _json.dumps([w["opened"] for w in weeks])
        merged_data = _json.dumps([w["merged"] for w in weeks])
    else:
        week_labels = opened_data = merged_data = "[]"
    return f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
  <div><h3 style="margin-bottom:8px;">PR Age Distribution (non-draft)</h3>
    <canvas id="ageChart" style="max-height:250px;"></canvas></div>
  <div><h3 style="margin-bottom:8px;">Weekly Activity (last 8 weeks)</h3>
    <canvas id="activityChart" style="max-height:250px;"></canvas></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
(function() {{
  var style = getComputedStyle(document.documentElement);
  var textColor = style.getPropertyValue('--text').trim() || '#d4d4f0';
  var mutedColor = style.getPropertyValue('--muted').trim() || '#7878aa';
  var borderColor = style.getPropertyValue('--border').trim() || '#2a2a5a';
  new Chart(document.getElementById('ageChart'), {{
    type: 'bar',
    data: {{ labels: {labels_hist}, datasets: [{{ label: 'Open PRs', data: {data_hist},
      backgroundColor: ['#50fa7b','#50fa7b','#ffb86c','#ffb86c','#ff5555','#ff5555'],
      borderColor: borderColor, borderWidth: 1 }}] }},
    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }},
      scales: {{ y: {{ beginAtZero: true, ticks: {{ color: mutedColor }}, grid: {{ color: borderColor }} }},
        x: {{ ticks: {{ color: mutedColor }}, grid: {{ display: false }} }} }} }}
  }});
  new Chart(document.getElementById('activityChart'), {{
    type: 'line',
    data: {{ labels: {week_labels}, datasets: [
      {{ label: 'Opened', data: {opened_data}, borderColor: '#ffb86c', backgroundColor: 'rgba(255,184,108,0.1)', tension: 0.3, fill: true }},
      {{ label: 'Merged', data: {merged_data}, borderColor: '#50fa7b', backgroundColor: 'rgba(80,250,123,0.1)', tension: 0.3, fill: true }} ] }},
    options: {{ responsive: true, plugins: {{ legend: {{ labels: {{ color: textColor }} }} }},
      scales: {{ y: {{ beginAtZero: true, ticks: {{ color: mutedColor }}, grid: {{ color: borderColor }} }},
        x: {{ ticks: {{ color: mutedColor, maxRotation: 45 }}, grid: {{ display: false }} }} }} }}
  }});
}})();
</script>'''


AI_BADGE = "🤖 auto-generated daily"


def build_report_html(prs, generated, bucket_result, outreach, weeks=None):
    weeks = weeks or []
    non_draft = [p for p in prs if not p.get("draft")]
    lanes = bucket_result["lanes"]
    counts = bucket_result["counts"]
    by_number = bucket_result["by_number"]

    # overlays gathered across lanes
    first_timers = [e for e in by_number.values() if "first_timer" in e["overlays"]
                    and e["lane"] not in (B.LANE_EXCLUDED_DRAFT,)]
    deflake = [e for e in by_number.values() if "deflake" in e["overlays"]]

    sections = []

    # ── By the Numbers (lane counts, actionability order) ──
    # Lane → section anchor (flagged_close has no own panel; it lives in outreach).
    lane_anchor = {
        B.LANE_LAND_READY: "land-ready",
        B.LANE_BOT_BACKPORT: "bot-backport",
        B.LANE_REVIEWER_COURT: "reviewer-court",
        B.LANE_NEEDS_DECISION: "needs-decision",
        B.LANE_FLAGGED_CLOSE: "outreach",
        B.LANE_AUTHOR_COURT: "author-court",
    }

    def crow(label, key, cls=""):
        n = counts.get(key, 0)
        anchor = lane_anchor.get(key)
        # Link the label to its section only when that section will render (n>0).
        lbl = f'<a class="lane-link" href="#{anchor}">{label}</a>' if (anchor and n) else label
        return [lbl, f'<span class="num-badge {cls}">{n}</span>']
    rows = [
        ["Total open PRs", f'<span class="num-badge warn">{bucket_result["total"]}</span>'],
        crow("🟢 Land-ready", B.LANE_LAND_READY, "ok"),
        crow("🤖 Bot / backport", B.LANE_BOT_BACKPORT),
        crow("👀 Ball in reviewer's court", B.LANE_REVIEWER_COURT),
        crow("🗳 Needs a decision", B.LANE_NEEDS_DECISION),
        crow("🏷 Flagged to close", B.LANE_FLAGGED_CLOSE, "warn"),
        crow("✍️ Ball in author's court", B.LANE_AUTHOR_COURT),
        crow("📝 Draft (excluded)", B.LANE_EXCLUDED_DRAFT, "muted"),
    ]
    if counts.get(B.LANE_UNKNOWN):
        rows.append(crow("❔ Unclassified", B.LANE_UNKNOWN, "muted"))
    sections.append(_panel("📊 By the Numbers", AI_BADGE, _table(["Lane", "Count"], rows),
                           anchor="by-the-numbers"))

    # ── Owed a review (priority, label-driven) — only if populated ──
    if outreach["priority_owed_review"]:
        sections.append(_panel(
            "⭐ Owed a Review (priority)", AI_BADGE,
            '<p class="muted" style="font-size:0.85em;">Authors confirmed still-wanted '
            '(via label) — the project owes these a review.</p>'
            + _outreach_rows(outreach["priority_owed_review"]), anchor="owed-review"))

    # ── Land-ready ──
    if lanes[B.LANE_LAND_READY]:
        sections.append(_panel(
            "🟢 Land-ready — one click to merge", AI_BADGE,
            '<p class="muted" style="font-size:0.85em;">Community-approved / to-be-merged, '
            'CI not failing, no conflicts.</p>' + _lane_land_ready(lanes[B.LANE_LAND_READY]), anchor="land-ready"))

    # ── Bot / backport quick-wins ──
    if lanes[B.LANE_BOT_BACKPORT]:
        sections.append(_panel(
            "🤖 Bot / backport quick-wins", AI_BADGE,
            '<p class="muted" style="font-size:0.85em;">Human-approved, fast to land.</p>'
            + _lane_bot(lanes[B.LANE_BOT_BACKPORT]), scroll=True, anchor="bot-backport"))

    # ── First-time contributors (retention priority) ──
    if first_timers:
        rows = _overlay_rows(first_timers, extra_col=lambda e: f'<code>{e["lane"]}</code>')
        sections.append(_panel(
            "🌱 First-Time Contributors", AI_BADGE,
            f'<p>{len(first_timers)} PRs from new contributors — a timely response may retain '
            f'a future regular. Cross-cut; each also appears in its lane.</p>'
            + _table(["PR", "Title", "Author", "Age", "Lane"], rows), scroll=True, anchor="first-timers"))

    # ── Ball in reviewer's court ──
    if lanes[B.LANE_REVIEWER_COURT]:
        sections.append(_panel(
            "👀 Ball in Reviewer's Court", AI_BADGE,
            f'<p><strong>{len(lanes[B.LANE_REVIEWER_COURT])} PRs</strong> where the author acted '
            f'last — these need a reviewer. Sorted longest-waiting first.</p>'
            + _lane_reviewer(lanes[B.LANE_REVIEWER_COURT]), scroll=True, anchor="reviewer-court"))

    # ── Needs a decision ──
    if lanes[B.LANE_NEEDS_DECISION]:
        sections.append(_panel(
            "🗳 Needs a Decision", AI_BADGE,
            f'<p><strong>{len(lanes[B.LANE_NEEDS_DECISION])} PRs</strong> blocked on a community '
            f'decision (major-decision-pending / -deferred).</p>'
            + _lane_decision(lanes[B.LANE_NEEDS_DECISION]), scroll=True, anchor="needs-decision"))

    # ── Deflake overlay ──
    if deflake:
        rows = _overlay_rows(deflake, extra_col=lambda e: f'<code>{e["lane"]}</code>')
        sections.append(_panel(
            "🔥 Deflake / Test-Fix", AI_BADGE,
            '<p class="muted" style="font-size:0.85em;">Merging these reduces CI noise for '
            'everyone. Cross-cut; each also appears in its lane.</p>'
            + _table(["PR", "Title", "Author", "Age", "Lane"], rows), anchor="deflake"))

    # ── Outreach dry-run ──
    outreach_html = ""
    if outreach["reengage"]:
        outreach_html += (f'<h3 class="warn">Re-engage ({len(outreach["reengage"])}) — '
                          f'reviewer\'s court, idle ≥{outreach["thresholds"]["reengage_days"]}d</h3>'
                          '<p class="muted" style="font-size:0.85em;">Project let these sit; '
                          'apologise and ask if the author still wants to land it.</p>'
                          + _outreach_rows(outreach["reengage"]))
    if outreach["closure_abandoned"]:
        outreach_html += (f'<h3 class="danger" style="margin-top:14px;">Closure candidates '
                          f'({len(outreach["closure_abandoned"])}) — author\'s court, idle '
                          f'≥{outreach["thresholds"]["closure_days"]}d</h3>'
                          '<p class="muted" style="font-size:0.85em;">Ball is the author\'s and '
                          'gone quiet. First-timers get a gentle nudge instead of a close threat.</p>'
                          + _outreach_rows(outreach["closure_abandoned"]))
    if outreach["maintainer_flagged_close"]:
        outreach_html += (f'<h3 style="margin-top:14px;">Maintainer-flagged to close '
                          f'({len(outreach["maintainer_flagged_close"])})</h3>'
                          + _outreach_rows(outreach["maintainer_flagged_close"]))
    if outreach["superseded_suggestions"]:
        outreach_html += (f'<h3 style="margin-top:14px;">Possibly superseded '
                          f'({len(outreach["superseded_suggestions"])}) — verify before acting</h3>'
                          + _outreach_rows(outreach["superseded_suggestions"]))
    if outreach_html:
        outreach_html = ('<p style="font-size:0.85em;"><strong>Dry-run only.</strong> '
                         'Nothing is posted, closed, or labelled automatically — these are '
                         'proposals with draft messages for a human to review and act on.</p>'
                         + outreach_html)
        sections.append(_panel("📮 Outreach Dry-Run", AI_BADGE, outreach_html, anchor="outreach"))

    # ── Ball in author's court (bottom: blocked on someone else) ──
    if lanes[B.LANE_AUTHOR_COURT]:
        sections.append(_panel(
            "✍️ Ball in Author's Court", AI_BADGE,
            f'<p><strong>{len(lanes[B.LANE_AUTHOR_COURT])} PRs</strong> waiting on the author '
            f'(CI red / conflicts / unaddressed review). Nothing for a reviewer to do yet.</p>'
            + _lane_author(lanes[B.LANE_AUTHOR_COURT]), scroll=True, anchor="author-court"))

    # ── Charts ──
    sections.append(_panel("📈 Charts", AI_BADGE, _build_charts(prs, non_draft, weeks), anchor="charts"))

    body = "\n".join(sections)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Live Report — Valkey PR Watchtower</title>
  <link rel="stylesheet" href="style.css">
  <style>
    html {{ scroll-behavior: smooth; }}
    .panel[id] {{ scroll-margin-top: 12px; }}
    .panel[id]:target {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
    .lane-link {{ color: var(--accent); text-decoration: none; }}
    .lane-link:hover {{ text-decoration: underline; }}
    .anchor-link {{ color: inherit; text-decoration: none; }}
    .anchor-link:hover {{ text-decoration: underline; }}
  </style>
  <script src="components.js" defer></script>
</head>
<body>
<div class="page-wrap">
  <site-header></site-header>
  <site-nav></site-nav>
  <div class="grid">
  <main>
  <div class="panel" style="margin-bottom:12px;">
    <div class="panel-header"><span>📊 Live PR Health Report</span><attr-badge type="ai"></attr-badge></div>
    <div class="panel-body">
      <p>Generated: <strong>{generated}</strong> from
      <a href="https://github.com/valkey-io/valkey/pulls" target="_blank" rel="noopener noreferrer">live GitHub API data</a>.
      PRs are sorted into lanes by <em>who owns the next move</em>, most immediately actionable first.
      Source: <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower/blob/main/scripts/build_report.py" target="_blank" rel="noopener noreferrer">build_report.py</a>.</p>
    </div>
  </div>
  {body}
  </main>
  <site-sidebar></site-sidebar>
  </div>
  <site-footer></site-footer>
</div>
</body>
</html>'''
