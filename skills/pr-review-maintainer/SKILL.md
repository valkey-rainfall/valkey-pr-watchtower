# Maintainer-Hat PR Review

Operating procedure for an AI agent drafting an OSS PR review on a maintainer's
behalf (primarily valkey-io/valkey and related repos). Use when the maintainer
says "review this PR", "put on your maintainer hat", or links a PR for
evaluation. The core design principle: **subagents gather evidence; the parent
session owns the verdict and every written word.**

This file is procedure only. What to look for and why lives in the review guide,
`guides/review-guide.md` in this repo (published at
<https://valkey-rainfall.github.io/valkey-pr-watchtower/review-guide.html>).
The guide is canonical for review knowledge: norms, red flags, evidence bars,
the squash-commit check. When this file and the guide disagree, the guide wins;
fix this file.

## HARD RULES

1. **Subagents feed the review; they NEVER write it.** The verdict, severity
   calls, and all prose are composed in the parent session with full context.
2. **Every finding gets a severity class BEFORE the review is written:**
   `blocking` / `suggest-not-blocking` / `pre-existing-out-of-scope`.
   No finding ships without one. This is the discipline mechanism that keeps
   nits from becoming merge hostages. **Every non-blocking finding also gets a
   disposition:** `file` (an issue is opened and its `#` is in the comment
   before the review posts) / `drop` (one line on why it does not matter) /
   `author-in-this-PR`. A deferral with no disposition is not a finding yet
   (guide, "Writing the review").
3. **Never demand fixes for pre-existing warts** in code the contributor
   merely touched. Note them, mark out-of-scope, move on.
4. **Read the actual diff, hunk by hunk.** Never the description's claim about
   the diff, and never present a review as complete without that read.
5. **Judge a test from its source, not from the PR's account of it.** Name the
   oracle it compares against and the bug class that oracle can catch before
   commenting on the test. Reasoning from the description alone has reversed a
   verdict on a test three times in one review; one read of the source settled it.
6. **Clean-room policy applies to subagent briefs too:** no reading code from
   Redis, Dragonfly, memcached, or any non-BSD-licensed project. High-level
   articles/discussions are fine.
7. Reviews are posted by the maintainer, not the agent. Draft comments for them
   to post.

## Phase 0 — Load the guide

Read `guides/review-guide.md` in full before anything else. It is the checklist
the rest of this procedure fills in: the major-decision triggers and mechanical
checks ("Before reading the diff"), the red-flag taxonomy with its examples, the
test and performance evidence bars, the backport decision, and the squash-commit
check. Do not reproduce its content here; cite it.

## Phase 1 — Evidence gathering (subagent-dispatchable)

Fan out up to 3 subagents when the PR is non-trivial; do it inline for small
PRs (< ~50 lines, familiar area). Each subagent returns distilled findings,
not raw dumps. Each brief says which guide sections it covers.

### Subagent A — History & context
- PR description, full review/comment history: who asked for what, what was
  already litigated and settled, what the bots (coderabbit, valkey-review-bot)
  already flagged and whether the author addressed it. Bot comments land in
  the issue discussion as well as inline; fetch both.
- Related/predecessor PRs and issues (search PR body, comments, commit
  messages for cross-references; check if this PR is part N of an agreed
  multi-part fix)
- Which rung of the guide's change ladder ("Before reading the diff", item 2)
  the PR claims, and whether the artifact that rung owes exists: a linked
  issue, a settled design discussion, a TSC thread. Report "claims rung N,
  artifact present/absent", not a verdict.
- Author's track record on this repo: prior merged PRs, responsiveness to
  feedback, DCO signoff present
- CI status per check; anything red or flaky. Before calling a red check
  infrastructure, compare against `unstable`'s most recent run of the same
  workflow (guide, "Maintainer hat"). For a flaky candidate, bring the
  build-history link the guide requires; once the flaky-test tracking
  dashboard exists, it is the reference for which flakes are currently
  active (see the guide's FLAKE-LEDGER note).
- Target branch and release: which release the PR would land in, and
  whether anything in it is a breaking change (guide, item 2).

### Subagent B — Diff mechanics
- The full diff, hunk by hunk: what actually changed vs. what the description
  claims
- Classify each change: new logic / pure move / refactor / test / doc
- Test coverage: do the tests pin the behavior contract (would a regression
  fail them)? Do they cover the edge cases the review history raised? Does a
  regression test fail without the fix (check out the base and run it)?
- **Flakiness scan of new/modified tests** against the guide's "Tests" rules
  and the checklist in `tests/README.md`. The four shapes that account for most
  deflake commits: a fixed sleep standing in for a condition; a timeout or
  budget sized for a fast local machine; an assertion on state another thread,
  process or replica updates asynchronously (including a mid-operation `INFO`
  read); a bound on an in-test duration or latency. The one question that
  catches most of it: "if this process freezes for 2 seconds at any point, does
  the test still pass?" If no, flag it.
- Per-language suspect scan (see lists below)
- **Classify every finding: pre-existing vs. introduced by this PR**

### Subagent C — Local build/test + conflict check (only when warranted)
- Build + run the touched test files locally when correctness is in doubt
- Conflict check against the maintainer's own open branches (perf/*, exp/*,
  feature/*): does this PR touch code in-flight work also touches?
- For valkey changes touching call()/execution paths: does the verification
  need moduleapi/postnotifications? (CI does not gate that suite.)

### Per-language suspect lists

**C (valkey core, benchmark):**
- `atoi`/`atol`/unchecked `strtol` — overflow UB, silent garbage acceptance
- VLAs with user-controlled size — stack overflow vector
- Error-path leaks (fine on process-exit paths; flag if path could become
  non-fatal)
- Off-by-one in loop sentinels; `<=` vs `<` vs `==` intent mismatches
- Cross-thread cache-line traffic: per-event reads of lines other threads
  write per-batch (coherence ping-pong)
- Main-thread-only machinery called transitively from IO-thread paths
- Behavior observable by modules or the replication stream = published API,
  even if comments call it "wrong" — flag any change to it as
  maintainer-discussion material
- Memory ordering on ARM (acquire/release pairing, not just x86-TSO habits)

**Python (tooling):**
- Mutable default args, broad `except:`, unclosed resources
- Import-time binding vs. late lookup (monkeypatch hazards)
- Missing type hints on public surface if repo uses them
- CI parity: does the repo's workflow run pylint/mypy beyond pytest?

**Tcl (valkey tests):**
- db 9 default (`$db` var) — keyspace-notification channels must use `${db}`
- Crash-bug regression tests: assert liveness from an independent connection
  before blocking reads
- `runtest --only` takes exact name or /regex/, not globs
- Prefer `wait_for_condition` over `after <ms>`; `wait_for_ofs_sync` /
  `wait_for_sync` over sleeping through replication

## Phase 2 — Verdict (parent-only; questions, not rules)

Answer these with the evidence in hand. They are prompts for attention —
not boxes to check, and never demands to transmit to the contributor.

1. **What did prior reviewers already settle?** Don't re-litigate. If the
   author did what a maintainer asked, that's a point in favor, not a
   surprise to re-examine.
2. **Which findings are pre-existing?** They inform context; they don't
   block. At most one "since you're touching this anyway" suggestion,
   explicitly marked optional.
3. **Would I own this code?** Maintenance surface, blast radius, rebase
   friction for in-flight work, what it costs the project at 2am.
4. **Do the tests pin the contract?** A test that proves the headline claim
   (e.g. fails-before-connect against a closed port) outweighs prose polish.
   When a sharp question got a plausible answer in the threads, the guide's
   rule applies: ask for the test that proves it, not the prose.
5. **What does this review teach the contributor?** Is this someone building
   toward bigger contributions? A welcoming, specific review is an investment
   in the pipeline. Proportionality is the difference between a maintainer
   and a gatekeeper.
6. **Is the PR the right size and shape for the project?** Would it be
   better split, or is asking to split it disproportionate?
7. **Is this a major decision?** Run the guide's trigger list. If any fires,
   the verdict routes to the TSC rather than approving; note on the thread what
   the decision waits on (guide, item 3). A behavior change beyond fixing an
   edge-case bug also goes to the TSC, and changed log-message or other
   user-visible text is a behavior change (guide, item 2). A change in the
   major-release-only class (guide, item 2) aimed at a minor or patch release is
   blocking on its own.
8. **Which rung is this really on, and was the debt paid?** Take Subagent A's
   "claims rung N, artifact present/absent" and check it against the diff.
   Third or fourth rung with no artifact: the review is one comment, "please
   open the issue first", not a line-by-line. Claims bug fix but the diff
   changes the design, or changes behavior beyond the edge case it names: say
   so before anything else; the rest of the review is premature until that is
   settled.

## Phase 3 — Write it

Structure: **Summary → What's good → Issues (each tagged with its severity
class) → Verdict.** The verdict states plainly what is blocking (if anything)
and what is merely suggested. If nothing blocks: say "approve" without hedging.

On every later round, open with one line restating what still blocks
("blocking: X, Y; everything else is nit"), even when the answer is "nothing".
A PR's merge state should be readable from its newest review comment, not
reconstructed from the thread history.

Draft inline comments to the corpus the guide describes: short (median 25
words, p90 87), one mechanism each, disagreement phrased as a question with
the reason attached, low-stakes items marked `nit:` or `(non-blocking)`.
Cross-reference with `#NNNN` only where the guide says the link is intentional.

Include the squash-commit check (guide, "Title and description as the squash
commit"): proposed title and body edits for the merge dialog, if any.

Offer the maintainer: a draft comment to post, or discussion of specific points.

## Maintenance note

When another maintainer shares their own review checklist, diff this file and
the guide against it; gaps between the two are the interesting part. Update
suspect lists when a review misses something a later bug reveals. Knowledge
goes in the guide; procedure goes here.
