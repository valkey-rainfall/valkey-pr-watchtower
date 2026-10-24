# Valkey review guide

Derived from the project's written norms (CONTRIBUTING, the test READMEs, the
governance docs) and a study of 981 merged PRs, 21 post-merge regressions, and
~160 deflake commits from 2022 onward. One maintainer's working checklist, not
project policy.

## How review actually works here

- The gate is an open inline thread, not the review state. CHANGES_REQUESTED was used
  34 times in a year against ~2300 COMMENTED reviews; 92% of TSC-started threads led
  to a code change. Leave the thread open until it is resolved; approve with caveats
  if the remaining items are minor.
- Approvals are terse (70% are five words or fewer). The scrutiny lives in threads.
- One TSC reviewer per PR is the measured median at every size, even above 1000
  lines, and the merger approved the PR themselves 68% of the time. Review as if
  yours is the only one, because it usually is: one review has to be complete. A
  second reviewer is welcome, not redundant.
- First review lands in ~12 hours at the median, but p90 is three weeks. Picking up
  a stale PR in your area is part of the job.
- Reviewers defer freely ("follow-up PR", "file an issue") and state scope discipline
  as a norm ("the bugfix PR needs to be as small as possible").

## Before reading the diff

1. Read the whole description and every existing thread. The threads alone have
   reversed a verdict more than once (PR 4490).
2. Decide what kind of change it is: bug fix, feature, refactor, test, CI. Refactor
   mixed with behavior change is the first thing to ask to split. Then place it on
   a ladder where each rung names the written artifact owed before code:
   - Bug fix that keeps the design: none.
   - Small additive feature, existing behavior unchanged: an issue is enough.
   - Changes an existing user experience: an issue with the design settled in it
     (a one-pager at most) before line-by-line review.
   - New concept: a design discussion, usually TSC.
   A PR on the third or fourth rung with no such artifact gets "please open the
   issue first" instead of a line-by-line review. The drift to catch is the inverse:
   a PR filed as a bug fix whose fix quietly changes the design has moved up a rung
   without paying for it. (The ladder is borrowed from kirodotdev/KiroCrew's T1-T4
   issue tiers; the artifacts are Valkey's.)
3. Major-decision check (the TSC decides; a reviewer routes). Triggers visible in a diff:
   `src/commands/*.json` change; new `VM_*`, or a changed return-value or flag
   contract of an existing `VM_*` with no signature change (PR 4645 made
   `VM_ZsetRangeEndReached` non-sticky; same class); new INFO / CLUSTER / CLIENT LIST field;
   new config; new `OBJ_ENCODING_*` or `RDB_TYPE_*`; layout change to `robj`,
   `hashtable`, `kvstore`, `client`, `clusterNode`; changed default; renamed or
   removed user-visible anything; changed error prefix; replication stream content;
   RESP2/3 reply shape; anything under `deps/`. Two more that no list spells out: a
   tradeoff where one thing gets worse to gain another, and any one-way door (if
   undoing it later would be a major decision, it is one now). Action: `major-decision-pending`,
   don't approve, confirm a linked issue has TSC discussion, keep reviewing the code.
   Parking needs an owner and a date: write on the thread who decides (TSC vote,
   a named maintainer, the author after a measurement) and put a revisit date in
   your own calendar. A parked item with neither is how a valid request sits
   for months with everyone agreeing it is valid.
4. Mechanical: DCO on every commit, clang-format-18, test present, `src/commands`
   json for command changes (and the `key_specs` in it are right: they drive
   cluster routing and ACL key checks, so a wrong spec is a silent cluster bug),
   CMakeLists and license header for new files, `needs-doc-pr` for user-facing
   changes, no security fix in a public PR.
5. Author readiness. Authors are expected to have reviewed and understood their
   own change before opening the PR and to be able to discuss and reason about it.
   A PR is not ready for review when that is not the case, whoever or whatever
   wrote the code. The test is a question, not a guess at provenance: pick one
   non-obvious hunk and ask why it is shaped that way. An answer that restates the
   diff, contradicts the code, or defers to "the tool" means the PR goes back with
   "please review your own change first and come back ready to walk through it",
   and no further review time until then.
6. Fork CI runs. Before approving a workflow run for a first-time contributor,
   diff `.github/` in the PR. A workflow change is fine when the description
   announces it and the diff does what the description says; an unannounced one,
   or one whose effect differs from its claim, means do not approve the run, ask
   about it in a thread first. Approving the run is what executes the PR's own
   workflow definition.

## Picking up a stale or previously approved PR

The p90 wait for a first review is three weeks, and PR 3496 sat six months with an
approval on it. Before acting on an old approval, your own or anyone's:

1. Confirm the approval is on the current head (`gh pr view --json reviews` gives
   the commit per review). A later push voids it.
2. `git merge-tree --write-tree unstable PR` for conflicts (git 2.38+; the older
   three-argument form prints a trivial-merge diff instead of a conflict list),
   then diff every touched function and its callees between the PR's base and
   current unstable. Unchanged means the old CI run still describes the merged
   result.
3. If anything moved, or the PR adds a test, press "Update branch" (or ask for a
   rebase) to get CI on today's base before merging.
4. Treat the project board's approved field as a hint only; it lagged live state on
   PR 4644. The reviews array is the record.

## Red flags, in the order reviewers raise them

Counts are effective TSC threads in 12 months.

1. **Design / API shape (157).** Reply shape that varies with input; struct passed by
   value; an API wider than its one caller; a config where a heuristic would do;
   negative or special-cased arguments without a use case.
2. **Compatibility (129).** Checked surfaces, ranked: config keys and defaults; RDB
   format and version gating; command reply shape RESP2 vs RESP3 and field order;
   INFO fields (don't duplicate config in INFO); replication stream content;
   module API signatures and naming; AOF preamble; cluster bus message format;
   ACL semantics; binary safety (`strlen` on an sds).
3. **Correctness (126).** By class, one example each:
   - Propagation: a new or changed write path missing one of `server.dirty++`,
     `signalModifiedKey`, `notifyKeyspaceEvent`, or `alsoPropagate` / argument
     rewrite for a non-deterministic command. The write lands locally and never
     reaches replicas or AOF; no test catches it unless someone wrote a
     replication test, so read for it.
   - Ownership: who frees an sds or robj on each path out of the function;
     refcount on a shared object; `OBJ_SHARED_INTEGERS` returned where the caller
     mutates.
   - Lookup flags: `lookupKeyRead` vs `lookupKeyWrite`, `LOOKUP_NOTOUCH` /
     `LOOKUP_NOEXPIRE` on paths that must not bump LRU or expire; replicas return
     logically-expired keys as missing without deleting them.
   - Error paths: early `return` that abandons a loop or skips cleanup; NULL on an
     edge path (empty backlog, PR 2877).
   - Mode duality: a definition that is right for one of two cluster modes, or for
     primary but not replica, or with io-threads but not without.
   - Mechanical: wrong variable of the same type (hash seed, PR 3366); off-by-one
     at a boundary.
4. **Comments and docs (120).** Stale comment after the code changed; comment that
   restates code; function without a contract comment; `redis`/`valkey` in symbol
   names where `server` is the convention.
5. **Naming and style (69).** Surrounding-code convention wins over the guide.
6. **Performance (50).** Work added to a hot path without numbers; per-completion
   or per-command overhead that is "small"; metrics on hot paths.
7. **IO-threads (37).** Reviewers trace which thread runs each syscall. "This still
   runs on the main thread" is a defect class, as is re-entrancy on the offload path.
8. **Memory safety (34).** Overflow, leak, UAF, output-buffer limits ignored.
   Narrower trigger, checkable from the file list: any change to a decoder of
   bytes the server did not produce itself (RESTORE payload, RDB load, RESP
   parsing, cluster bus messages, module API arguments, Lua values) gets a
   hostile-input read: a length field larger than the buffer, a truncated
   input, a count that overflows the allocation size.
9. **Logging (31), error handling (22), process (16), scope creep (12), weak tests
   (11), flaky tests (9).** Test items are raised rarely in review yet are the
   largest class of post-merge regressions (see below). That gap is the reviewer's
   to close.

Two patterns reviewers reject on sight: struct or helper definitions mid-function,
and decorative section-divider comments. Comment on the pattern and the fix, never
on who or what wrote it; provenance is not reviewable, the author's understanding
is (item 5 above).

## What review missed (21 regressions)

- 9 were tests that passed in one CI config and broke in another (valgrind, tmpfs,
  TLS, slow runner, allocator rounding, async loading).
- 4 were performance regressions, none benchmarked in review. PR 3544 regressed SET
  20%, was reverted, reapplied, and regressed again.
- 4 logic bugs, 2 UB, 1 crash. The crash was a 12-line PR with one approval and no
  threads.
- Only 3 of the 21 faulty hunks were questioned in review; each time the reviewer
  asked the right question and accepted the author's answer. The misses were
  verification gaps, not reading gaps. Rule: when a sharp question gets a plausible
  answer, ask for the test that proves it instead of accepting the prose.
- Misses cluster at both size extremes. Small PRs look trivial and get no threads;
  large PRs get design debate while a hunk goes unexercised.

## Checks the project does not write down

**Tests.** Every new or changed test gets a flake read against the checklist in
`tests/README.md` ("Writing tests that don't flake", PR 4895; until it merges, the
branch is `valkey-rainfall:tests/flaky-test-checklist`). The ranking there held
across five years of deflake commits: fixed sleeps and tight time budgets, then
missing convergence waits, account for about half of all fixes in every window.
Reviewer-side rules on top of the checklist:
- A regression test must fail without the fix. Check out the base and run the
  test yourself; that is usually faster than asking. When you do ask, ask whether
  they ran it against the base and what it reported, not for a statement that
  they did. "Test present" is mechanical; this is the check that separates a
  regression test from one that would pass anyway.
- A `wait_for_condition` budget that passes locally with margin can still time out
  under valgrind; ask for `$::valgrind` scaling or a 10x margin, not a 2x one.
- Any test added to the convergence-heavy suites (cluster, replication, dual-channel,
  failover, sentinel) gets a `run-extra-tests` or `run-valgrind-tests` run before
  approval. Nine of the 21 post-merge regressions were tests that passed in one CI
  config only.
- gtests: leak-clean under LeakSanitizer, `-Werror` clean, C-readable style per
  `src/unit/README.md`.
- Before commenting on a test, name what it compares against and what bug class
  that oracle can catch, and take both from the test source, not from the PR's
  account of it. The two can disagree: on PR 4875 the description undersold a gtest
  loop whose oracle (unconditional `strtod`) was the right design and only needed
  a wider corpus.

**Performance and memory.** Required evidence for any hot-path change or any claim:
workload named (command mix, key count and size, pipeline, threads, build flags,
host and architecture); both sides of a tradeoff measured; allocator named for
memory. Reject as evidence: a single run per side; no spread; under a minute of
steady state at the stated rate; a dataset that fits in cache; default
`valkey-benchmark` flags; a mismatched base; only the improved metric shown. Run-to-run
drift on a single developer host is ~4%, so a 3% gain with no spread means
nothing. If evidence is missing, apply the `run-benchmark` label (the project's
own benchmark workflow) or run it yourself: PR head vs merge-base on both
architectures, builds pinned so code layout does not move between the two trees,
per-run spread, cycles/req and instructions/req alongside throughput.

Two rules the project's own benchmark threads do not state:
- One architecture is not evidence for the other. The same change has shown
  opposite-sign effects on Graviton 3 and Graviton 4. For a tradeoff, ask for both
  x86 and arm or run the missing one; for a strict subtraction one is enough.
- For "removes work from the main thread", the metric is instructions/req and
  cycles/req on the main thread, not throughput. Throughput across two source
  trees moves with code layout; the per-request counters do not.

Scale that bar to the claim. The full bar is for a tradeoff (one path gets worse)
or a gain that justifies added complexity. A strict subtraction of work with no new
code on any path (PR 3496 removed one alloc + memcpy + free, and the diff got
simpler) needs only a no-regression read on the path that does not benefit, with
per-run numbers so the noise floor is visible; a short run is acceptable there.
Still read the evidence for the two things that make a subtraction not strict:
a larger allocation growing in bigger steps, or work moved onto a path that was
previously skipped.

**Code.** Opaque interfaces honored at every call site in the same PR; generic
structures never learn about their callers. No issue numbers in source comments.
API comments state the contract, not the rationale. New files wired into both
Makefile and CMakeLists. Description matches the diff, including a test count that
was actually listed. Every "fixes", "more correct", or "harmless" claim in the body
deserves the same scrutiny as a hunk: find its premise, then check the premise
against the source the diff does not touch. PR 3496 claimed its early return fixed a
suppressed SELECT; `rewriteAppendOnlyFileBackground` already resets
`aof_selected_db` on every path out of that state, so the claim was false and would
have gone into the squash commit as history.

**Maintainer hat.** Scan the file for sibling instances of the bug. Check coverage of
analogous paths. Note untested public APIs. Never call a failure "known flaky"
without a build-history link, and record the flake before rerunning, not after:
a rerun with no record is a data point lost, and the ledger of recorded flakes is
what justifies fixing the suite instead of retrying it. Never fix a flake with a
retry, a longer sleep, a relaxed assertion or a skip; those hide the signal the
ledger exists to keep. <!-- FLAKE-LEDGER: when the flake tooling (Rain + Ranma)
ships, name its output here as the canonical build-history link and point the
skill's Subagent A at it. --> Before calling a red check infrastructure, open
`unstable`'s own most recent run of the same workflow: the same red there means
infra (PR 4332's `build-debian-old` was a repo-wide mirror 404), a green there
means the red is the PR's. Never merge your own PR on your own approval; it needs
another maintainer's.

**Backport decision.** Decide at merge, not later, whether the change goes to a
release branch: bug fixes with user impact and no behavior change are candidates,
features and refactors are not. A candidate must be minimal enough to cherry-pick
clean; if it is not, the bug fix and the cleanup should have been separate PRs,
and that is a reason to ask for the split before merging. The mechanism is the
GitHub project for each applicable release, not a label: add the PR to the
project before merging with status `todo`; on merge the status moves to
`to be backported` on its own and the backport AI workflow picks it up. If the PR
is only added after merge, check that its status reads `to be backported`, since
the automatic transition did not run and nothing will pick it up otherwise.

## Green flags (108 large PRs approved with two or fewer threads)

Body tells the story symptom -> mechanism -> fix, with before/after; names the
introducing PR or commit; states compatibility impact up front (RDB version, binary
safety, ACL); links the issue or the TSC decision; diff is one thing; author says
how they split the work. Reviewers approve fast when the PR did the compatibility
reasoning for them.

## Writing the review

- Comments here run short (median 25 words, p90 87) and carry one mechanism each.
- Phrase disagreement as a question with the reason attached: "Shouldn't we X,
  since Y?" rather than "Change this to X." Explain why every time; the corpus has
  almost no bare instructions from TSC members.
- Describe the problem; offer the fix when it is cheap (18% of comments carry a
  `suggestion` block). For a first-time contributor, lean toward offering it.
- Mark low-stakes items `nit:` or `(non-blocking)`. Only 4% of comments are marked,
  so an unmarked comment reads as blocking.
- Approve with caveats when only minor items remain; leave the thread open.
- Defer rather than block when the item is real but out of scope; say "follow-up"
  and give the deferral a disposition before the review posts: filed (with the
  `#` of the issue you opened), dropped (say why it does not matter), or author
  handles it in this PR. "Fine for now, follow up later" with none of the three
  is where the item dies.
- `#1234` creates a cross-reference on the other issue or PR. Use it when that
  link is intentional and adds value for someone landing on the other side (the
  issue this fixes, the PR this builds on or reverts, a sibling fix); write
  "PR 1234" in prose when it is only context for this thread. The thing to avoid
  is a pile of unjustified cross-references, not cross-references.

## Title and description as the squash commit

The repo squash-merges with the PR title and body as the commit message, so the
description is what history keeps. Check it against the final diff as part of
approval, and edit it in the merge dialog rather than asking for another round.

Title: imperative, says what changed not what activity ("Reject bare `(` in zset
score ranges", not "Fix issue 3483" or "Address review comments"); under 72 chars
(GitHub appends ` (#NNNN)`); no WIP or draft markers at merge.

Body: the first paragraph must stand alone after `git log --oneline` plus one
`git show`: symptom or gap, mechanism, what the change does. Then compatibility
impact, stated even when none. Benchmark: one sentence with the workload named,
and only a result that stock tooling can reproduce (`valkey-benchmark`, a gtest);
numbers from a throwaway DEBUG hook or a local script stay on the PR, since the
commit cannot be checked against them. Tables are fine when they are the evidence.
`Fixes #N` as its own trailer line, always, whenever the PR resolves an issue: it
closes the issue on merge, and the one reference comment it posts per
release-branch cherry-pick is a link worth having. Write the body
unwrapped; the web merge dialog wraps the body at 72 columns on commit (`gh pr
merge` does not), so merge from the web UI.

Remove in the merge dialog: `@mentions` (they fire on every cherry-pick to a
release branch), `#NNNN` references that are incidental rather than intentional
(each one also fires per cherry-pick; keep the ones that earn their link, drop the
rest to "PR 1234" or a URL), test-run
output ("370 passed"), checklists, review-process chatter ("addressed comments",
"rebased"), screenshots. Keep the mechanism paragraph even when trimming hard.

## Where the numbers come from

Every count above is from a GitHub API pull of the 981 PRs merged into
valkey-io/valkey from 2022 onward: files touched, reviewers, review threads and
their outcomes, labels and timeline; plus 21 post-merge regressions traced to the
PR that introduced each, and ~160 commits that fix a flaky test. The dataset and
the scripts that build it are not published.
