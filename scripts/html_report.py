"""HTML report builder for valkey-pr-watchtower. Generates report.html."""
from collections import Counter
from datetime import datetime, timezone


def _age_days(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def _age_str(days):
    if days < 14:
        return f"{days}d"
    if days < 60:
        return f"{days // 7}w"
    if days < 365:
        return f"{days // 30}mo"
    return f"{days / 365:.1f}y"


def _label_names(pr):
    return [l["name"] for l in pr.get("labels", [])]


def _pr_link(pr):
    n = pr["number"]
    return f'<a href="https://github.com/valkey-io/valkey/pull/{n}" target="_blank" rel="noopener noreferrer">#{n}</a>'


def _table(headers, rows):
    """Build an HTML table from headers list and rows (list of lists)."""
    h = "".join(f"<th>{hdr}</th>" for hdr in headers)
    body = ""
    for row in rows:
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        body += f"<tr>{cells}</tr>\n"
    return f"<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>"


def _panel(title, badge_text, content, scroll=False):
    body_cls = "panel-body-scroll" if scroll else "panel-body"
    return f'''<div class="panel" style="margin-bottom:12px;">
  <div class="panel-header"><span>{title}</span><span class="badge badge-ai">{badge_text}</span></div>
  <div class="{body_cls}">{content}</div>
</div>'''


def _ci_badge(ci_info):
    """Render a CI status badge from ci_status dict entry."""
    if not ci_info:
        return '<span class="muted">—</span>'
    checks = ci_info.get("checks", {})
    total = checks.get("total", 0)
    success = checks.get("success", 0)
    failure = checks.get("failure", 0)
    mergeable = ci_info.get("mergeable")

    if total == 0:
        ci_text = '<span class="muted">no checks</span>'
    elif failure > 0:
        ci_text = f'<span class="danger">❌ {failure}/{total} failing</span>'
    elif success == total:
        ci_text = f'<span class="ok">✅ {total}/{total}</span>'
    else:
        ci_text = f'<span class="warn">⏳ {success}/{total}</span>'

    merge_text = ""
    if mergeable is True:
        merge_text = ' · <span class="ok">no conflicts</span>'
    elif mergeable is False:
        merge_text = ' · <span class="danger">conflicts</span>'

    return ci_text + merge_text


def _build_charts(prs, non_draft, weeks):
    """Generate Chart.js HTML for PR age histogram and weekly activity."""
    import json as _json

    # PR Age Histogram buckets
    buckets = {"0-2w": 0, "2-4w": 0, "1-3mo": 0, "3-6mo": 0, "6-12mo": 0, "1y+": 0}
    for pr in non_draft:
        days = _age_days(pr["created_at"])
        if days <= 14:
            buckets["0-2w"] += 1
        elif days <= 28:
            buckets["2-4w"] += 1
        elif days <= 90:
            buckets["1-3mo"] += 1
        elif days <= 180:
            buckets["3-6mo"] += 1
        elif days <= 365:
            buckets["6-12mo"] += 1
        else:
            buckets["1y+"] += 1

    labels_hist = _json.dumps(list(buckets.keys()))
    data_hist = _json.dumps(list(buckets.values()))

    # Weekly activity chart
    if weeks:
        week_labels = _json.dumps([w["week_start"] for w in weeks])
        opened_data = _json.dumps([w["opened"] for w in weeks])
        merged_data = _json.dumps([w["merged"] for w in weeks])
    else:
        week_labels = "[]"
        opened_data = "[]"
        merged_data = "[]"

    return f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
  <div>
    <h3 style="margin-bottom:8px;">PR Age Distribution (non-draft)</h3>
    <canvas id="ageChart" style="max-height:250px;"></canvas>
  </div>
  <div>
    <h3 style="margin-bottom:8px;">Weekly Activity (last 8 weeks)</h3>
    <canvas id="activityChart" style="max-height:250px;"></canvas>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
(function() {{
  // Age histogram
  new Chart(document.getElementById('ageChart'), {{
    type: 'bar',
    data: {{
      labels: {labels_hist},
      datasets: [{{
        label: 'Open PRs',
        data: {data_hist},
        backgroundColor: ['#50fa7b','#50fa7b','#ffb86c','#ffb86c','#ff5555','#ff5555'],
        borderColor: '#2a2a5a',
        borderWidth: 1
      }}]
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ display: false }} }},
      scales: {{
        y: {{ beginAtZero: true, ticks: {{ color: '#7878aa' }}, grid: {{ color: '#2a2a5a' }} }},
        x: {{ ticks: {{ color: '#7878aa' }}, grid: {{ display: false }} }}
      }}
    }}
  }});
  // Weekly activity
  new Chart(document.getElementById('activityChart'), {{
    type: 'line',
    data: {{
      labels: {week_labels},
      datasets: [
        {{ label: 'Opened', data: {opened_data}, borderColor: '#ffb86c', backgroundColor: 'rgba(255,184,108,0.1)', tension: 0.3, fill: true }},
        {{ label: 'Merged', data: {merged_data}, borderColor: '#50fa7b', backgroundColor: 'rgba(80,250,123,0.1)', tension: 0.3, fill: true }}
      ]
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ labels: {{ color: '#d4d4f0' }} }} }},
      scales: {{
        y: {{ beginAtZero: true, ticks: {{ color: '#7878aa' }}, grid: {{ color: '#2a2a5a' }} }},
        x: {{ ticks: {{ color: '#7878aa', maxRotation: 45 }}, grid: {{ display: false }} }}
      }}
    }}
  }});
}})();
</script>'''


def build_report_html(prs, generated, weeks=None, ci_status=None):
    if weeks is None:
        weeks = []
    if ci_status is None:
        ci_status = {}

    non_draft = [p for p in prs if not p.get("draft")]
    draft = [p for p in prs if p.get("draft")]
    bot_prs = [p for p in prs if p.get("user", {}).get("login", "").endswith("[bot]")]

    label_counts = Counter()
    for pr in prs:
        for l in _label_names(pr):
            label_counts[l] += 1

    sections = []

    # ── By the Numbers
    rows = [
        ["Total open PRs", f'<span class="num-badge warn">{len(prs)}</span>'],
        ["Non-draft", f'<span class="num-badge">{len(non_draft)}</span>'],
        ["Draft", f'<span class="num-badge">{len(draft)}</span>'],
        ["Bot PRs (backports)", f'<span class="num-badge">{len(bot_prs)}</span>'],
    ]
    for label in ["major-decision-pending", "major-decision-approved",
                  "major-decision-deferred", "to-be-merged", "to-be-closed",
                  "stalled", "run-extra-tests", "needs-doc-pr"]:
        if label in label_counts:
            color = "danger" if label in ("major-decision-pending", "stalled") else ("ok" if "approved" in label else "warn")
            rows.append([f"<code>{label}</code>", f'<span class="num-badge {color}">{label_counts[label]}</span>'])
    sections.append(_panel("📊 By the Numbers", "🤖 auto-generated daily", _table(["Metric", "Count"], rows)))

    # ── Immediate Actions: to-be-merged
    tbm = [p for p in non_draft if "to-be-merged" in _label_names(p)]
    approved = [p for p in non_draft if "major-decision-approved" in _label_names(p) and "to-be-merged" not in _label_names(p)]
    tbc = [p for p in prs if "to-be-closed" in _label_names(p)]
    stalled = [p for p in prs if "stalled" in _label_names(p)]

    action_html = ""
    if tbm:
        rows = []
        for pr in sorted(tbm, key=lambda p: p["created_at"]):
            ci = _ci_badge(ci_status.get(pr["number"]))
            rows.append([_pr_link(pr), pr["title"][:55], pr.get("user", {}).get("login", "?"), _age_str(_age_days(pr["created_at"])), ci])
        action_html += f'<h3 class="ok">Merge Now (<code>to-be-merged</code>)</h3>{_table(["PR", "Title", "Author", "Age", "CI + Merge"], rows)}'

    if approved:
        rows = []
        for pr in sorted(approved, key=lambda p: p["created_at"]):
            ci = _ci_badge(ci_status.get(pr["number"]))
            rows.append([_pr_link(pr), pr["title"][:55], pr.get("user", {}).get("login", "?"), _age_str(_age_days(pr["created_at"])), ci])
        action_html += f'<h3 class="ok" style="margin-top:14px;">Community-Approved, Awaiting Merge</h3><p class="muted" style="font-size:0.85em;">Decision is made — just needs someone to click merge.</p>{_table(["PR", "Title", "Author", "Age", "CI + Merge"], rows)}'

    if tbc or stalled:
        rows = []
        for pr in tbc:
            rows.append([_pr_link(pr), pr["title"][:55], pr.get("user", {}).get("login", "?"), _age_str(_age_days(pr["created_at"])), "<code>to-be-closed</code>"])
        for pr in stalled:
            rows.append([_pr_link(pr), pr["title"][:55], pr.get("user", {}).get("login", "?"), _age_str(_age_days(pr["created_at"])), "<code>stalled</code>"])
        action_html += f'<h3 class="danger" style="margin-top:14px;">Close Now</h3>{_table(["PR", "Title", "Author", "Age", "Reason"], rows)}'

    if action_html:
        sections.append(_panel("⚡ Immediate Actions", "🤖 auto-generated daily", action_html))

    # ── Decision Bottleneck
    pending = [p for p in non_draft if "major-decision-pending" in _label_names(p)]
    if pending:
        rows = []
        for pr in sorted(pending, key=lambda p: p["created_at"])[:20]:
            rows.append([_pr_link(pr), pr["title"][:60], pr.get("user", {}).get("login", "?"),
                         _age_str(_age_days(pr["created_at"])), _age_str(_age_days(pr["updated_at"])) + " ago"])
        extra = f'<p class="muted" style="font-size:0.85em; margin-top:6px;">…and {len(pending) - 20} more</p>' if len(pending) > 20 else ""
        content = f'<p><strong>{len(pending)} PRs</strong> blocked waiting for a community vote.</p>{_table(["PR", "Title", "Author", "Age", "Last update"], rows)}{extra}'
        sections.append(_panel("🟡 Decision Bottleneck", "🤖 auto-generated daily", content, scroll=True))

    # ── Top Contributors
    author_counts = Counter(
        p.get("user", {}).get("login", "?")
        for p in non_draft
        if not p.get("user", {}).get("login", "").endswith("[bot]")
    )
    rows = []
    for author, count in author_counts.most_common(15):
        flag = ' <span class="danger">🚨</span>' if count >= 8 else (' <span class="warn">⚠️</span>' if count >= 5 else "")
        rows.append([f'<a href="https://github.com/{author}" target="_blank" rel="noopener noreferrer">{author}</a>', f'{count}{flag}'])
    sections.append(_panel("🧑‍💻 Top Contributors by Open PR Count", "🤖 auto-generated daily", _table(["Author", "Open PRs"], rows)))

    # ── Dormant PRs
    dormant = [p for p in non_draft
               if _age_days(p["updated_at"]) >= 90
               and not p.get("user", {}).get("login", "").endswith("[bot]")]
    dormant.sort(key=lambda p: p["updated_at"])
    if dormant:
        rows = []
        for pr in dormant[:25]:
            rows.append([_pr_link(pr), pr["title"][:55], pr.get("user", {}).get("login", "?"),
                         _age_str(_age_days(pr["created_at"])), f'<span class="danger">{_age_str(_age_days(pr["updated_at"]))} ago</span>'])
        extra = f'<p class="muted" style="font-size:0.85em; margin-top:6px;">…and {len(dormant) - 25} more</p>' if len(dormant) > 25 else ""
        content = f'<p><strong>{len(dormant)} non-draft PRs</strong> haven\'t been updated in 90+ days.</p>{_table(["PR", "Title", "Author", "Created", "Last update"], rows)}{extra}'
        sections.append(_panel("🕰 Long-Dormant PRs (90+ days)", "🤖 auto-generated daily", content, scroll=True))

    # ── Deflake PRs
    deflake = [p for p in non_draft
               if any(kw in p["title"].lower() for kw in ["flak", "deflak", "stale tmpdir", "timing"])]
    if deflake:
        rows = []
        for pr in sorted(deflake, key=lambda p: p["created_at"]):
            rows.append([_pr_link(pr), pr["title"][:60], pr.get("user", {}).get("login", "?"),
                         _age_str(_age_days(pr["created_at"])), _age_str(_age_days(pr["updated_at"])) + " ago"])
        content = f'<p class="muted" style="font-size:0.85em;">Merging these reduces CI noise for everyone.</p>{_table(["PR", "Title", "Author", "Age", "Last update"], rows)}'
        sections.append(_panel("🔥 Open Deflake / Test-Fix PRs", "🤖 auto-generated daily", content))

    # ── High CI Burden
    run_extra = [p for p in non_draft if "run-extra-tests" in _label_names(p)]
    if run_extra:
        rows = []
        for pr in sorted(run_extra, key=lambda p: p["created_at"]):
            rows.append([_pr_link(pr), pr["title"][:55], pr.get("user", {}).get("login", "?"), _age_str(_age_days(pr["created_at"]))])
        content = f'<p><strong>{len(run_extra)} PRs</strong> trigger extended CI runs.</p>{_table(["PR", "Title", "Author", "Age"], rows)}'
        sections.append(_panel("⏱ High CI Burden (run-extra-tests)", "🤖 auto-generated daily", content, scroll=True))

    # ── First-Time Contributors
    first_timers = [p for p in non_draft
                    if p.get("author_association") in ("FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER", "NONE")
                    and not p.get("user", {}).get("login", "").endswith("[bot]")]
    if first_timers:
        rows = []
        for pr in sorted(first_timers, key=lambda p: p["created_at"], reverse=True)[:20]:
            rows.append([_pr_link(pr), pr["title"][:55], pr.get("user", {}).get("login", "?"),
                         _age_str(_age_days(pr["created_at"])),
                         pr.get("author_association", "?").replace("_", " ").lower()])
        content = f'<p>PRs from contributors with no prior merged PRs in this repo ({len(first_timers)} total). These deserve extra attention — a response now may retain a future regular contributor.</p>{_table(["PR", "Title", "Author", "Age", "Association"], rows)}'
        sections.append(_panel("🌱 First-Time Contributors", "🤖 auto-generated daily", content, scroll=True))

    # ── Charts: PR Age Histogram + Weekly Activity
    chart_html = _build_charts(prs, non_draft, weeks)
    if chart_html:
        sections.append(_panel("📈 Charts", "🤖 auto-generated daily", chart_html))

    # ── Assemble page
    body = "\n".join(sections)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Live Report — Valkey PR Watchtower</title>
  <link rel="stylesheet" href="style.css">
  <script src="components.js" defer></script>
</head>
<body>
<div class="page-wrap">

  <site-header></site-header>
  <site-nav></site-nav>

  <div class="panel" style="margin-bottom:12px;">
    <div class="panel-header"><span>📊 Live PR Health Report</span><attr-badge type="ai"></attr-badge></div>
    <div class="panel-body">
      <p>Generated: <strong>{generated}</strong> from <a href="https://github.com/valkey-io/valkey/pulls" target="_blank" rel="noopener noreferrer">live GitHub API data</a>.
      Source: <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower/blob/main/scripts/build_report.py" target="_blank" rel="noopener noreferrer">build_report.py</a>.</p>
    </div>
  </div>

  {body}

  <site-footer></site-footer>

</div>
</body>
</html>'''
