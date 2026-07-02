# valkey-pr-watchtower 🗼

Project-wide PR health monitoring for [valkey-io/valkey](https://github.com/valkey-io/valkey).

**[→ View the live report](https://valkey-rainfall.github.io/valkey-pr-watchtower/)**

---

## What this is

A personal tool that generates automated health reports on the Valkey PR backlog: aging patterns, stalled decisions, duplicate PRs, flaky test signals, contributor load, and actionable triage recommendations.

Reports are regenerated daily by GitHub Actions and published to GitHub Pages. No human needed in the loop for the data — just data → analysis → page.

> **Disclaimer:** This is a personal project maintained by [@rainsupreme](https://github.com/rainsupreme), a Valkey contributor, not an official Valkey project representative. The analysis and opinions here are my own.

---

## What's in here

```
scripts/
  build_report.py        # fetches live GitHub data → generates docs/report.md
  build_affinity.py      # (planned) git log analysis → reviewer affinity scoring
  suggest_reviewers.py   # (planned) PR → ranked reviewer suggestions

docs/
  index.md               # landing page (static)
  report.md              # auto-generated daily PR health report

.github/workflows/
  update-report.yml      # daily cron: run build_report.py, commit, push
```

---

## PR process orientation (personal perspective)

The official contributing guide lives at [valkey-io/valkey/blob/unstable/CONTRIBUTING.md](https://github.com/valkey-io/valkey/blob/unstable/CONTRIBUTING.md). Read that first.

What follows is my personal read on how the PR process works in practice — not rules, just patterns I've observed.

**What makes a PR land quickly:**
- Small and focused. One thing per PR. Reviewers are busy; a 50-line fix gets reviewed in days, a 2000-line refactor sits for months.
- CI green before requesting review. Broken CI is an immediate context-switch cost for reviewers.
- Clear description: what changes, why, how to verify it. Don't make the reviewer reverse-engineer your intent.
- For anything non-trivial, check if there's an open issue or prior discussion. "Fixes #NNNN" or "continuing discussion from #NNNN" tells reviewers there's context.

**What makes a PR die quietly:**
- No activity after initial submission. If you get feedback and go quiet, maintainers assume you've moved on.
- Scope creep mid-review. If a reviewer asks for a small fix and you refactor three unrelated things in the same commit, they lose the thread.
- No `release-notes` or `no-release-notes` label. The bot will flag it and reviewers will skip it until it's labeled.
- Duplicate of an existing open PR. Search before submitting.

**The `major-decision-pending` label:**
This means maintainers haven't reached consensus yet. It's not a blocker on your end — your code is fine. It means the community is still debating whether to take the feature at all. These can take weeks to months to resolve. Patience is the only option; pinging won't speed it up.

**Reviewer assignment:**
There's no formal assignment process for most PRs. Maintainers pick up what they have context on. If your PR has sat 3+ weeks with no activity, a polite ping in the PR is appropriate. Tag someone who has reviewed similar code recently — check `git log` on the files you changed.

**First contributions:**
The project is welcoming but bandwidth-constrained. Your first PR might take longer than you expect. That's normal and not a signal about the PR quality. A good first PR to build trust: fix a real bug (not just a typo), keep it small, include a test.

---

## Running locally

```bash
pip install requests python-dateutil
export GITHUB_TOKEN=your_token
python scripts/build_report.py > docs/report.md
```

---

## Roadmap

- [x] Daily automated PR health report
- [ ] First-contribution welcome workflow
- [ ] Reviewer affinity scoring (file ownership × review history)
- [ ] Automated reviewer suggestions on new PRs
- [ ] Flaky test tracker (correlate bot-filed issues with open deflake PRs)
