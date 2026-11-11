# Review pipelines changelog

Changes to the pages in this directory, newest first. Changes to the review guide itself are in the git history of `guides/review-guide.md`.

## 2026-11-11

<a id="v2026-11-11"></a>

- Draft and passes: each checker pass runs in its own fresh session with only its own input folder, two rounds on every review, the fast lane included, with new checkers each round. A four-line verdict header; the cold reader starts from a common-knowledge baseline and may look up the published docs at a pinned commit; an accuracy re-check after any new fact; answers go where the question was asked.
- Evidence: confirmation runs for a deflake are dispatches of the project's daily workflow on the PR head, trimmed to the failing variant, one dispatch per commit; local loops are not evidence. The evidence file and a results file are filed with lockkeeper.
- Self-review: runs before the maintainer's branch is pushed; the passes run in three separate sessions; the description is checked against the PR description guide and goes through the checker passes; security-adjacent findings stay private and are reported to the maintainer directly.
- Auto-revise: fixes are new signed-off commits pushed plainly, never an amend; a failing check that a flake or infrastructure explains gets a recorded rerun, not a code change.
- Triage: the PR is claimed in lockkeeper first; a refused claim is reported and the review goes on without lockkeeper.
- README: a Lockkeeper section on what the pipeline records (claim, stage changes, briefs, flags, the staged review and its reasons, replies, thread verdicts, backport rows, checker input folders and the writing gate in shadow) and what stays the maintainer's.

## 2026-11-05

<a id="v2026-11-05"></a>

- First version: the model, Flow A (review requested) and Flow B (own PRs), stages, gates, work in progress limits, fast lane, performance flag, and auto-revise triage.
- One brief per stage: triage, evidence, draft and passes, self-review, auto-revise. Each brief cites the review guide by anchor.
