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


def _panel(title, badge_text, content):
    return f'''<div class="panel" style="margin-bottom:12px;">
  <div class="panel-header"><span>{title}</span><span class="badge badge-ai">{badge_text}</span></div>
  <div class="panel-body">{content}</div>
</div>'''


def build_report_html(prs, generated):
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
            rows.append([_pr_link(pr), pr["title"][:65], pr.get("user", {}).get("login", "?"), _age_str(_age_days(pr["created_at"]))])
        action_html += f'<h3 class="ok">Merge Now (<code>to-be-merged</code>)</h3>{_table(["PR", "Title", "Author", "Age"], rows)}'

    if approved:
        rows = []
        for pr in sorted(approved, key=lambda p: p["created_at"]):
            rows.append([_pr_link(pr), pr["title"][:65], pr.get("user", {}).get("login", "?"), _age_str(_age_days(pr["created_at"]))])
        action_html += f'<h3 class="ok" style="margin-top:14px;">Community-Approved, Awaiting Merge</h3><p class="muted" style="font-size:0.85em;">Decision is made — just needs someone to click merge.</p>{_table(["PR", "Title", "Author", "Age"], rows)}'

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
        sections.append(_panel("🟡 Decision Bottleneck", "🤖 auto-generated daily", content))

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
        sections.append(_panel("🕰 Long-Dormant PRs (90+ days)", "🤖 auto-generated daily", content))

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
        sections.append(_panel("⏱ High CI Burden (run-extra-tests)", "🤖 auto-generated daily", content))

    # ── Assemble page
    body = "\n".join(sections)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Live Report — Valkey PR Watchtower</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="page-wrap">

  <header role="banner">
    <div class="site-title">🗼 VALKEY PR WATCHTOWER</div>
    <div class="site-subtitle"><a href="https://github.com/valkey-io/valkey" style="color:var(--accent3)">valkey-io/valkey</a> — live report</div>
  </header>

  <nav aria-label="Site navigation">
    <span>→</span>
    <a href="index.html">🏠 Home</a>
    <a href="report.html">📊 Live Report</a>
    <a href="analysis.html">🔍 Deep Analysis</a>
    <a href="orientation.html">🧭 PR Orientation</a>
    <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower">⚙️ Source</a>
  </nav>

  <div class="panel" style="margin-bottom:12px;">
    <div class="panel-header"><span>📊 Live PR Health Report</span><span class="badge badge-ai">🤖 auto-generated daily at 06:00 UTC</span></div>
    <div class="panel-body">
      <p>Generated: <strong>{generated}</strong> from <a href="https://github.com/valkey-io/valkey/pulls" target="_blank" rel="noopener noreferrer">live GitHub API data</a>.
      Source: <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower/blob/main/scripts/build_report.py" target="_blank" rel="noopener noreferrer">build_report.py</a>.</p>
    </div>
  </div>

  {body}

  <footer role="contentinfo">
    <p>🗼 <strong>valkey-pr-watchtower</strong> · by <a href="https://github.com/rainsupreme">rainsupreme</a> · <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower">source</a></p>
    <p style="margin-top:6px;">Personal project, not an official Valkey project. Data from the GitHub API. Opinions are the author\'s own.</p>
  </footer>

</div>
</body>
</html>'''
