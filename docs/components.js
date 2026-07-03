/**
 * Shared Web Components for valkey-pr-watchtower.
 * Single source of truth for header, nav, sidebar, footer, and attribution badges.
 */

/* ── <attr-badge type="ai|approved|human"> ─────────────────────────────── */
class AttrBadge extends HTMLElement {
  connectedCallback() {
    const type = this.getAttribute('type') || 'ai';
    const map = {
      ai:       { cls: 'badge-ai',       text: '🤖 AI-generated' },
      approved: { cls: 'badge-approved',  text: '✅ AI-drafted, human-approved' },
      human:    { cls: 'badge-human',     text: '✍️ Human-authored' },
    };
    const { cls, text } = map[type] || map.ai;
    this.innerHTML = `<span class="badge ${cls}">${text}</span>`;
  }
}
customElements.define('attr-badge', AttrBadge);

/* ── <site-header> ─────────────────────────────────────────────────────── */
class SiteHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
  <header role="banner">
    <div class="site-title">🗼 VALKEY PR WATCHTOWER</div>
    <div class="site-subtitle">project-wide health monitoring for <a href="https://github.com/valkey-io/valkey" style="color:var(--accent3)">valkey-io/valkey</a></div>
    <div class="visitor-counter" role="img" aria-label="Visitor number 000001">
      VISITOR: 000001
    </div>
    <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap; margin-bottom:8px;">
      <div class="visitor-counter" aria-label="Open PRs being tracked">
        WATCHING: <span class="counter-prs-open">0271</span> OPEN PRS
      </div>
      <div class="visitor-counter" aria-label="PRs that have passed under this watchtower's gaze">
        GAZED UPON: <span class="counter-prs-since">0276</span> PRS
      </div>
      <div class="visitor-counter" aria-label="Last updated">
        UPDATED: <span class="counter-last-updated" id="last-updated-utc">2026-07-03 00:19 UTC</span>
      </div>
    </div>
    <script>
      (function() {
        var el = document.getElementById('last-updated-utc');
        if (!el) return;
        try {
          var raw = el.textContent.trim();
          var iso = raw.replace(' UTC','Z').replace(' ','T');
          var d = new Date(iso);
          if (isNaN(d)) return;
          el.textContent = d.toLocaleString(undefined, {
            month: 'short', day: 'numeric', year: 'numeric',
            hour: '2-digit', minute: '2-digit', timeZoneName: 'short'
          });
        } catch(e) {}
      })();
    </script>
    <div style="font-size:0.75em; color:var(--muted); margin-top:4px;">
      a personal project by <a href="https://github.com/rainsupreme">rainsupreme</a>
      &nbsp;·&nbsp; a personal project, not an official Valkey project
      &nbsp;·&nbsp; <button id="theme-toggle" onclick="toggleTheme()" style="background:none;border:1px solid var(--border);border-radius:4px;padding:2px 8px;color:var(--muted);cursor:pointer;font-family:inherit;font-size:1em;">🌓 theme</button>
    </div>
  </header>`;
  }
}
customElements.define('site-header', SiteHeader);

/* ── Theme toggle logic ────────────────────────────────────────────────── */
function toggleTheme() {
  const root = document.documentElement;
  const current = root.getAttribute('data-theme');
  let next;
  if (current === 'dark') next = 'light';
  else if (current === 'light') next = null; // system default
  else next = 'dark'; // from system → force dark

  if (next) {
    root.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  } else {
    root.removeAttribute('data-theme');
    localStorage.removeItem('theme');
  }
  updateToggleLabel();
}

function updateToggleLabel() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  const current = document.documentElement.getAttribute('data-theme');
  if (current === 'dark') btn.textContent = '🌙 dark';
  else if (current === 'light') btn.textContent = '☀️ light';
  else btn.textContent = '🌓 auto';
}

// Apply saved preference on load
(function() {
  const saved = localStorage.getItem('theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
  // Update label after components render
  setTimeout(updateToggleLabel, 50);
})();

/* ── <site-nav> ────────────────────────────────────────────────────────── */
class SiteNav extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
  <nav aria-label="Site navigation">
    <span>→</span>
    <a href="index.html">🏠 Home</a>
    <a href="report.html">📊 Live Report</a>
    <a href="analysis.html">🔍 Deep Analysis</a>
    <a href="orientation.html">🧭 PR Orientation</a>
    <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower">⚙️ Source</a>
  </nav>`;
  }
}
customElements.define('site-nav', SiteNav);

/* ── <site-sidebar> ────────────────────────────────────────────────────── */
class SiteSidebar extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
    <aside class="sidebar" aria-label="Stats and links">

      <div class="panel">
        <div class="panel-header">
          <span>📊 Snapshot</span>
          <attr-badge type="ai"></attr-badge>
        </div>
        <div class="panel-body">
          <div class="stat-grid">
            <div class="stat-box">
              <span class="stat-number warn"><span class="counter-prs-open">0271</span></span>
              <span class="stat-label">open PRs</span>
            </div>
            <div class="stat-box">
              <span class="stat-number danger">38</span>
              <span class="stat-label">decision-pending</span>
            </div>
            <div class="stat-box">
              <span class="stat-number ok">8</span>
              <span class="stat-label">approved, unmerged</span>
            </div>
            <div class="stat-box">
              <span class="stat-number danger">17</span>
              <span class="stat-label">PRs from 2024</span>
            </div>
          </div>
          <p style="font-size:0.72em; color:var(--muted); margin-top:8px; text-align:center;">
            <a href="report.html">live report →</a>
          </p>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">🔗 Quick Links</div>
        <div class="panel-body">
          <ul style="list-style:none; padding:0; margin:0;">
            <li style="padding:4px 0; border-bottom:1px solid var(--border)"><a href="https://rainsupreme.github.io/PR-Dashboard/" target="_blank" rel="noopener noreferrer">Daily PR Dashboard ↗</a></li>
            <li style="padding:4px 0; border-bottom:1px solid var(--border)"><a href="https://github.com/valkey-io/valkey/pulls" target="_blank" rel="noopener noreferrer">All open PRs ↗</a></li>
            <li style="padding:4px 0; border-bottom:1px solid var(--border)"><a href="https://github.com/valkey-io/valkey/pulls?q=is%3Apr+is%3Aopen+label%3Amajor-decision-pending" target="_blank" rel="noopener noreferrer">Decision-pending ↗</a></li>
            <li style="padding:4px 0; border-bottom:1px solid var(--border)"><a href="https://github.com/valkey-io/valkey/pulls?q=is%3Apr+is%3Aopen+label%3Amajor-decision-approved" target="_blank" rel="noopener noreferrer">Approved, unmerged ↗</a></li>
            <li style="padding:4px 0; border-bottom:1px solid var(--border)"><a href="https://github.com/valkey-io/valkey/blob/unstable/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer">CONTRIBUTING.md ↗</a></li>
            <li style="padding:4px 0;"><a href="https://github.com/valkey-rainfall/valkey-pr-watchtower" target="_blank" rel="noopener noreferrer">This site's source ↗</a></li>
          </ul>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">🏗 What's Planned</div>
        <div class="panel-body" style="font-size:0.82em;">
          <ul style="padding-left:14px;">
            <li>First-contribution welcome bot</li>
            <li>Reviewer affinity scoring</li>
            <li>Automated reviewer suggestions</li>
            <li>Flaky test issue tracker</li>
          </ul>
          <p style="margin-top:8px; color:var(--muted); font-size:0.85em;">
            Contributions welcome! <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower/issues" target="_blank" rel="noopener noreferrer">Open an issue ↗</a>
          </p>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">✉️ Best viewed in</div>
        <div class="panel-body" style="text-align:center; font-size:0.8em; color:var(--muted);">
          <p>Netscape Navigator 4.0</p>
          <p style="font-size:1.5em; margin:6px 0;">🖥️</p>
          <p>800×600 resolution</p>
          <p style="margin-top:6px; color:var(--accent3);">
            (jk, any modern browser is fine)
          </p>
        </div>
      </div>

    </aside>`;
  }
}
customElements.define('site-sidebar', SiteSidebar);

/* ── <site-footer> ─────────────────────────────────────────────────────── */
class SiteFooter extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
  <footer role="contentinfo">
    <p>
      🗼 <strong>valkey-pr-watchtower</strong> &nbsp;·&nbsp;
      by <a href="https://github.com/rainsupreme">rainsupreme</a> &nbsp;·&nbsp;
      <a href="https://github.com/valkey-rainfall/valkey-pr-watchtower">source on GitHub</a>
    </p>
    <p style="margin-top:6px;">
      Personal project, not an official Valkey project.
      Data from the GitHub API.
      Opinions are the author's own.
    </p>
    <p style="margin-top:6px;">
      <span class="blink">★</span>
      Sign my guestbook!
      <span class="blink">★</span>
      &nbsp;(just kidding, there is no guestbook)
    </p>
  </footer>`;
  }
}
customElements.define('site-footer', SiteFooter);
