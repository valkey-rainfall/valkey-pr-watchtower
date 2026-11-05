# Valkey review guide

Derived from the project's written norms (CONTRIBUTING, the test READMEs, the governance docs) and a study of 981 PRs merged between 2025-10-16 and 2026-10-14, the 21 post-merge regressions traced back to PRs in that set, and about 160 deflake commits from 2022-03-20 onward ([where the numbers come from](#data-sources)). One maintainer's working checklist, not project policy.

## How review actually works here

<a id="how-review-works"></a>

- The gate is an open inline thread, not the review state. CHANGES_REQUESTED was used 34 times in the study window against about 2300 COMMENTED reviews; 92% of TSC-started threads led to a code change. Leave the thread open until it is resolved.
- Approvals are terse (70% are five words or fewer). The scrutiny lives in threads.
- One TSC reviewer per PR is the measured median at every size, even above 1000 lines, and the merger approved the PR themselves 68% of the time. Review as if yours is the only one, because it usually is: one review has to be complete. A second reviewer is welcome, not redundant.
- First review lands in about 12 hours at the median, but p90 is three weeks. Picking up a stale PR in your area is part of the job.
- Reviewers defer freely ("follow-up PR", "file an issue") and state scope discipline as a norm ("the bugfix PR needs to be as small as possible").
- <a id="review-event"></a>This guide's choice for the review event differs from the measured habit above, and it is the maintainer's choice, not a project rule: when a change is needed, the review is Request changes. Comment is for nits and optional notes only. Approve when nothing is left but nits.

## Before reading the diff

<a id="before-the-diff"></a>

1. <a id="read-threads"></a>Read the whole description and every existing thread. The threads alone have reversed a verdict more than once ([PR 4490](https://github.com/valkey-io/valkey/pull/4490)).

2. <a id="change-ladder"></a>Decide what kind of change it is: bug fix, feature, refactor, test, CI. Refactor mixed with behavior change is the first thing to ask to split. Then place it on a ladder; each rung names what I want to see written down before I review the code line by line (a personal bar, except where a project rule is cited):
    - Strict bug fix: an edge case, design unchanged, no behavior anyone could depend on changes. Nothing beyond the PR.
    - Small additive feature, existing behavior unchanged: an issue.
    - Changes existing behavior beyond fixing an edge-case bug: an issue with the design settled in it, and consult the TSC. Behavior changes are often breaking changes, and behavior includes the wording of log messages and any other user-visible text, not only command semantics; log scrapers and clients match on both. Where the change touches backward compatibility or adds a user-visible field that must be maintained, GOVERNANCE.md makes it a major decision outright; item 3 below routes it.
    - New concept: an issue first, per CONTRIBUTING ("major feature or a semantical change ... start by creating an issue"); a new data structure or API is a major decision under GOVERNANCE.md.

    <a id="release-check"></a>Separately from the ladder, the release question. The project generally follows semantic versioning ([releases](https://valkey.io/topics/releases/)): patch and minor releases are backward compatible; only a major release may break any of the seven API contracts listed there (command inputs, outputs and defined behavior; Lua API; RDB version; replication protocol; cluster bus; Module API; AOF format), alter an existing command's behavior, remove a deprecated command, or change a config default. Check which release the PR would land in; a change in that class aimed at a minor or patch release is a blocking finding on its own, before any design question.

    A PR on the third or fourth rung with no such artifact gets "please open the issue first" instead of a line-by-line review. The drift to catch is the inverse: a PR filed as a bug fix whose fix quietly changes the design, or changes behavior beyond the edge case it names, has moved up a rung without paying for it.

3. <a id="major-decision"></a>Major-decision check (the TSC decides; a reviewer routes). Triggers visible in a diff: `src/commands/*.json` change; new `VM_*`, or a changed return-value or flag contract of an existing `VM_*` with no signature change ([PR 4645](https://github.com/valkey-io/valkey/pull/4645) made `VM_ZsetRangeEndReached` non-sticky; same class); new INFO / CLUSTER / CLIENT LIST field; new config; new `OBJ_ENCODING_*` or `RDB_TYPE_*`; layout change to `robj`, `hashtable`, `kvstore`, `client`, `clusterNode`; changed default; renamed or removed user-visible anything; changed error prefix; replication stream content; RESP2/3 reply shape; anything under `deps/`. Two more that no list spells out: a tradeoff where one thing gets worse to gain another, and any one-way door (if undoing it later would be a major decision, it is one now). Action: `major-decision-pending`, don't approve, confirm a linked issue has TSC discussion, keep reviewing the code. Plain bug fixes for an edge case are not major decisions; do not raise a TSC question for them.
    - <a id="log-wording"></a>Changed wording of a log message or other user-visible text. A trivial wording change is blocking: ask for it to be reverted. If there is a good reason to keep it, it is a breaking change and needs a TSC decision like any other trigger above.
    - <a id="tsc-parked"></a>Parked decisions. The TSC's timetable is its own; what you can do is note on the thread what the decision is waiting on and, if you want to see it through, put a revisit date in your own calendar. Without that, a parked item sits for months with everyone agreeing it is valid.

4. <a id="mechanical"></a>Mechanical: DCO on every commit, clang-format-18, test present, `src/commands` json for command changes (and the `key_specs` in it are right: they drive cluster routing and ACL key checks, so a wrong spec is a silent cluster bug), Makefile, CMakeLists and license header for new files, `needs-doc-pr` for user-facing changes, no security fix in a public PR.

5. <a id="author-readiness"></a>Author readiness. Authors are expected to have reviewed and understood their own change before opening the PR and to be able to discuss and reason about it. A PR is not ready for review when that is not the case, whoever or whatever wrote the code. The test is a question, not a guess at provenance: pick one non-obvious hunk and ask why it is shaped that way. An answer that restates the diff, contradicts the code, or defers to "the tool" means the PR goes back with "please review your own change first and come back ready to walk through it", and no further review time until then.

6. <a id="fork-ci"></a>Fork CI runs. Before approving a workflow run for a first-time contributor, diff `.github/` in the PR. A workflow change is fine when the description announces it and the diff does what the description says; an unannounced one, or one whose effect differs from its claim, means do not approve the run, ask about it in a thread first. Approving the run is what executes the PR's own workflow definition.

## Picking up a stale or previously approved PR

<a id="stale-pr"></a>

The p90 wait for a first review is three weeks, and [PR 3496](https://github.com/valkey-io/valkey/pull/3496) sat six months with an approval on it. Before acting on an old approval, your own or anyone's, and before a re-review after a new push:

1. Confirm the approval is on the current head (`gh pr view --json reviews` gives the commit per review). A later push voids it.
2. `git merge-tree --write-tree unstable PR` for conflicts (git 2.38+; the older three-argument form prints a trivial-merge diff instead of a conflict list), then diff every touched function and its callees between the PR's base and current unstable. Unchanged means the old CI run still describes the merged result.
3. If anything moved, or the PR adds a test, press "Update branch" to get CI on today's base before merging.
4. Treat the project board's approved field as a hint only; it lagged live state on [PR 4644](https://github.com/valkey-io/valkey/pull/4644). The reviews array is the record.

## Red flags, in the order reviewers raise them

<a id="red-flags"></a>

Counts are effective TSC threads in the study window (PRs merged 2025-10-16 to 2026-10-14).

1. **Design / API shape (157).** Reply shape that varies with input; struct passed by value; an API wider than its one caller; a config where a heuristic would do; negative or special-cased arguments without a use case.
2. <a id="compatibility"></a>**Compatibility (129).** Checked surfaces, ranked: config keys and defaults; RDB format and version gating; command reply shape RESP2 vs RESP3 and field order; INFO fields (don't duplicate config in INFO); replication stream content; module API signatures and naming; AOF preamble; cluster bus message format; ACL semantics; binary safety (`strlen` on an sds).
3. <a id="correctness"></a>**Correctness (126).** By class, one example each:
    - Propagation: a new or changed write path missing one of `server.dirty++`, `signalModifiedKey`, `notifyKeyspaceEvent`, or `alsoPropagate` / argument rewrite for a non-deterministic command. The write lands locally and never reaches replicas or AOF; no test catches it unless someone wrote a replication test, so read for it.
    - Ownership: who frees an sds or robj on each path out of the function; refcount on a shared object; `OBJ_SHARED_INTEGERS` returned where the caller mutates.
    - Lookup flags: `lookupKeyRead` vs `lookupKeyWrite`, `LOOKUP_NOTOUCH` / `LOOKUP_NOEXPIRE` on paths that must not bump LRU or expire; replicas return logically-expired keys as missing without deleting them.
    - Error paths: early `return` that abandons a loop or skips cleanup; NULL on an edge path (empty backlog, [PR 2877](https://github.com/valkey-io/valkey/pull/2877)).
    - Mode duality: a definition that is right for one of two cluster modes, or for primary but not replica, or with io-threads but not without.
    - Mechanical: wrong variable of the same type (hash seed, [PR 3366](https://github.com/valkey-io/valkey/pull/3366)); off-by-one at a boundary.
4. **Comments and docs (120).** Stale comment after the code changed; comment that restates code; function without a contract comment; a project-name prefix in a symbol name where `server` is the convention.
5. **Naming and style (69).** Surrounding-code convention wins over the guide.
6. **Performance (50).** Work added to a hot path without numbers; per-completion or per-command overhead that is "small"; metrics on hot paths. What counts as numbers is in [Performance](#performance).
7. **IO-threads (37).** Reviewers trace which thread runs each syscall. "This still runs on the main thread" is a defect class, as is re-entrancy on the offload path.
8. <a id="hostile-input"></a>**Memory safety (34).** Overflow, leak, UAF, output-buffer limits ignored. Narrower trigger, checkable from the file list: any change to a decoder of bytes the server did not produce itself (RESTORE payload, RDB load, RESP parsing, cluster bus messages, module API arguments, Lua values) gets a hostile-input read: a length field larger than the buffer, a truncated input, a count that overflows the allocation size.
9. **Logging (31), error handling (22), process (16), scope creep (12), weak tests (11), flaky tests (9).** Test items are raised rarely in review yet are the largest class of post-merge regressions (see below). That gap is the reviewer's to close.

<a id="provenance"></a>Two patterns reviewers reject on sight: struct or helper definitions mid-function, and decorative section-divider comments. Comment on the pattern and the fix, never on who or what wrote it; provenance is not reviewable, the author's understanding is ([author readiness](#author-readiness)).

## What review missed (21 regressions)

<a id="review-misses"></a>

- 9 were tests that passed in one CI config and broke in another (valgrind, tmpfs, TLS, slow runner, allocator rounding, async loading).
- 4 were performance regressions, none benchmarked in review. [PR 3544](https://github.com/valkey-io/valkey/pull/3544) regressed SET 20%, was reverted, reapplied, and regressed again.
- 4 logic bugs, 2 UB, 1 crash. The crash was a 12-line PR with one approval and no threads.
- <a id="plausible-answer"></a>Only 3 of the 21 faulty hunks were questioned in review; each time the reviewer asked the right question and accepted the author's answer. The misses were verification gaps, not reading gaps. Rule: when a sharp question gets a plausible answer, ask for the test that proves it instead of accepting the prose.
- Misses cluster at both size extremes. Small PRs look trivial and get no threads; large PRs get design debate while a hunk goes unexercised.

## Checks the project does not write down

<a id="unwritten-checks"></a>

<a id="tests"></a>**Tests.** <a id="flake-read"></a>Every new or changed test gets a flake read against the checklist in `tests/README.md` ("Writing tests that don't flake", [PR 4895](https://github.com/valkey-io/valkey/pull/4895); until it merges, the branch is `valkey-rainfall:tests/flaky-test-checklist`). The ranking there held across five years of deflake commits: fixed sleeps and tight time budgets, then missing convergence waits, account for about half of all fixes in every window. Reviewer-side rules on top of the checklist:

- <a id="fails-on-base"></a>A regression test must fail without the fix. Check out the base and run the test yourself; that is usually faster than asking. When you do ask, ask whether they ran it against the base and what it reported, not for a statement that they did. "Test present" is mechanical; this is the check that separates a regression test from one that would pass anyway. A PR with no test that reproduces the bug on the base gets a closer read of every hunk, not a lighter one.
- <a id="cheap-test"></a>A missing test is blocking when it is cheap to write with the existing harness: no large new scaffolding, no mocks, no refactoring for a test seam. A costly one is non-blocking, with one line on why. Base the cost on a real test, not a guess: name an existing test it can copy (file and line), its rough size, and anything new it needs. The same rule applies to a flake fix the checklist calls for: blocking when the fix is small with the existing harness and the flake risk is real in the project's CI (the daily valgrind, sanitizer, libc and io-threads jobs).
- <a id="test-defer"></a>Prefer the newer test mechanism over old practice. Per-test cleanup with `test_defer` ([PR 4871](https://github.com/valkey-io/valkey/pull/4871)) replaces restoring state inline at the end of a test, which leaks the state into every later test when an assertion fails first. "Matches the existing pattern" is not a reason to keep a known failure mode.
- <a id="valgrind-budget"></a>A `wait_for_condition` budget that passes locally with margin can still time out under valgrind; ask for `$::valgrind` scaling or a 10x margin, not a 2x one.
- <a id="extra-tests"></a>Any test added to the convergence-heavy suites (cluster, replication, dual-channel, failover, sentinel) gets a `run-extra-tests` or `run-valgrind-tests` run before approval. Nine of the 21 post-merge regressions were tests that passed in one CI config only.
- gtests: leak-clean under LeakSanitizer, `-Werror` clean, C-readable style per `src/unit/README.md`.
- <a id="test-oracle"></a>Before commenting on a test, name what it compares against and what bug class that oracle can catch, and take both from the test source, not from the PR's account of it. The two can disagree: on [PR 4875](https://github.com/valkey-io/valkey/pull/4875) the description undersold a gtest loop whose oracle (unconditional `strtod`) was the right design and only needed a wider corpus.

<a id="small-prs"></a>**Small test-only and CI-only PRs.** These need less reading, not fewer checks, because small PRs are where review missed a crash ([what review missed](#review-misses)). Each one still gets: the flake read; the fails-on-base run for any new test; the oracle check; for a CI change, what the change could hide (a job that no longer runs, a check that no longer fails, a matrix entry dropped); for a deflake, whether it weakens the assertion the test exists to make ([deflakes](#deflake)); and a check that the PR is really test-only or CI-only, with no production hunk.

<a id="code-rules"></a>**Code.** Opaque interfaces honored at every call site in the same PR; generic structures never learn about their callers. No issue numbers in source comments. API comments state the contract, not the rationale. New files wired into both Makefile and CMakeLists. Description matches the diff, including a test count that was actually listed. <a id="claim-premise"></a>Every "fixes", "more correct", or "harmless" claim in the body deserves the same scrutiny as a hunk: find its premise, then check the premise against the source the diff does not touch. [PR 3496](https://github.com/valkey-io/valkey/pull/3496) claimed its early return fixed a suppressed SELECT; `rewriteAppendOnlyFileBackground` already resets `aof_selected_db` on every path out of that state, so the claim was false and would have gone into the squash commit as history.

<a id="maintainer-hat"></a>**Maintainer hat.** <a id="siblings"></a>Scan the file for sibling instances of the bug. Check coverage of analogous paths. Note untested public APIs. Never merge your own PR on your own approval; it needs another maintainer's.

<a id="flakes"></a>**Flakes and red CI.** Never call a failure "known flaky" without a build-history link, and record the flake before rerunning, not after: a rerun with no record is a data point lost, and the record of flakes is what justifies fixing the suite instead of retrying it. <a id="red-ci"></a>Before calling a red check infrastructure, open `unstable`'s own most recent run of the same workflow: the same red there means infra ([PR 4332](https://github.com/valkey-io/valkey/pull/4332)'s `build-debian-old` was a repo-wide mirror 404), a green there means the red is the PR's.

<a id="deflake"></a>**Deflakes.** A deflake that only lengthens an `after`, weakens the assertion the test exists to make, or skips the test on the runner where it failed hides the signal; the fix is the one the `tests/README.md` checklist names for that pattern: poll with `wait_for_condition` instead of `after`, scale the budget for valgrind, wait explicitly for replication or cluster convergence, or fix the real race. Two loosenings the checklist itself prescribes are not that: widening a time range or asserting an ordering or lower bound instead of an upper bound on a duration, and skipping on a probed platform capability (`valgrind:skip`, `tls:skip`). The checklist's closing line is the rule: fix the synchronization rather than retrying; the next slower runner will find the same gap.

<a id="backport"></a>**Backport decision.** Decide at merge, not later, which release branches the change goes to. Every real bug is backported to every maintained release branch where it has a real impact, whatever its severity; a defect in a CI workflow or the release process counts too. Features, performance work, refactors and docs are not backported. Decide branch by branch from the code, not from a label: on each release branch, read the function the fix touches and check whether the commit that introduced the bug is an ancestor of that branch (`git merge-base --is-ancestor <commit> <branch>`). A branch where the buggy code does not exist is not affected; say so. Keep the fix minimal so it can be cherry-picked; when it is mixed with a cleanup, ask for the split before merging. <a id="backport-project"></a>The mechanism is the GitHub project for each applicable release, not a label: add the PR to the project before merging with status `todo`; on merge the status moves to `to be backported` on its own and the backport workflow picks it up. If the PR is only added after merge, check that its status reads `to be backported`, since the automatic transition did not run and nothing will pick it up otherwise.

## Performance

<a id="performance"></a>

<a id="perf-evidence"></a>**Evidence bar.** Required for any hot-path change or any performance claim: workload named (command mix, key count and size, pipeline, threads, build flags, host and architecture); both sides of a tradeoff measured; allocator named for memory. Reject as evidence: a single run per side; no spread; under a minute of steady state at the stated rate; a dataset that fits in cache; default `valkey-benchmark` flags; a mismatched base; only the improved metric shown. Run-to-run drift on a single developer host is about 4%, so a 3% gain with no spread means nothing. If evidence is missing, apply the `run-benchmark` label (the project's own benchmark workflow) or run it yourself: PR head vs merge-base on both architectures, builds pinned so code layout does not move between the two trees, per-run spread, cycles/req and instructions/req alongside throughput.

Two rules the project's own benchmark threads do not state:

- One architecture is not evidence for the other. The same change has shown opposite-sign effects on Graviton 3 and Graviton 4. For a tradeoff, ask for both x86 and arm or run the missing one; for a strict subtraction one is enough.
- For "removes work from the main thread", the metric is instructions/req and cycles/req on the main thread, not throughput. Throughput across two source trees moves with code layout; the per-request counters do not.

<a id="perf-scale"></a>**Scale the bar to the claim.** The full bar is for a tradeoff (one path gets worse) or a gain that justifies added complexity. A strict subtraction of work with no new code on any path ([PR 3496](https://github.com/valkey-io/valkey/pull/3496) removed one alloc + memcpy + free, and the diff got simpler) needs only a no-regression read on the path that does not benefit, with per-run numbers so the noise floor is visible; a short run is acceptable there. Still read the evidence for the two things that make a subtraction not strict: a larger allocation growing in bigger steps, or work moved onto a path that was previously skipped.

<a id="perf-flag"></a>**When to ask for a benchmark.** Two different triggers, handled differently:

| Trigger | What it looks like | What to do |
|---|---|---|
| Claim | The PR says it is faster, uses less memory, or allocates less. | Ask for evidence that meets the bar above, scaled to the claim. Missing evidence is a normal review comment. |
| Risk | The PR claims nothing, but touches a hot path (command dispatch, reply buffers, hashtable, io-threads, eviction and expire, listpack and other encodings), adds an allocation or a lock inside a loop, or changes a common data structure. | Measure first: apply `run-benchmark` or run it yourself. Do not write a performance concern into the review without a measurement; only a measured regression is a finding. |

## Green flags (108 large PRs approved with two or fewer threads)

<a id="green-flags"></a>

Body tells the story symptom -> mechanism -> fix, with before/after; names the introducing PR or commit; states compatibility impact up front (RDB version, binary safety, ACL); links the issue or the TSC decision; diff is one thing; author says how they split the work. Reviewers approve fast when the PR did the compatibility reasoning for them.

## Writing the review

<a id="writing-the-review"></a>

- <a id="comment-length"></a>Comments here run short (median 25 words, p90 87) and carry one mechanism each.
- Phrase disagreement as a question with the reason attached: "Shouldn't we X, since Y?" rather than "Change this to X." Explain why every time; the corpus has almost no bare instructions from TSC members.
- Describe the problem; offer the fix when it is cheap (18% of comments carry a `suggestion` block). For a first-time contributor, lean toward offering it.
- <a id="nit-markers"></a>Mark low-stakes items `nit:` or `(non-blocking)`. Only 4% of comments are marked, so an unmarked comment reads as blocking.
- <a id="request-changes"></a>Pick the event per [the review event](#review-event). A Request changes review says briefly what looks right and what needs to change; it does not open with "looks good to me".
- <a id="do-not-repeat"></a>Add only what is new. Do not repeat the PR body, your own inline comments in the review summary, or what another reviewer already said. When someone has already raised a finding, reply in that thread with only the new detail; if nothing new is left, do not reply.
- <a id="no-rebase-nudges"></a>Do not ask for a rebase or describe merge conflicts. GitHub shows conflicts and CI reruns on the new base. Spell out only what CI will not catch.
- <a id="deferral"></a>Defer rather than block when the item is real but out of scope, and give the deferral a disposition before the review posts: filed (with the `#` of the issue you opened), dropped (say why it does not matter), or the author handles it in this PR. "Fine for now, follow up later" with none of the three is where the item dies. Filing it is the reviewer's job; the review does not ask the author for a follow-up PR.
- <a id="review-markdown"></a>Review text never lands in git history, so full GitHub markdown is allowed and helps: a table of blocking items, numbered repro steps, `suggestion` blocks, `<details>` for long evidence. PR titles, PR bodies and commit messages are history and keep the plain rules in [the next section](#squash-commit).
- <a id="cross-references"></a>Cross-references: write `#1234` for a PR or issue in the same repository; GitHub resolves it. Use a full URL only for a PR or issue in another repository. The same rule applies to review text, PR bodies and commit messages.

## Title and description as the squash commit

<a id="squash-commit"></a>

The repo squash-merges with the PR title and body as the commit message, so the description is what history keeps. Check it against the final diff as part of approval, and edit it in the merge dialog rather than asking for another round.

<a id="title"></a>Title: imperative, says what changed not what activity ("Reject bare `(` in zset score ranges", not "Fix issue 3483" or "Address review comments"); under 72 chars (GitHub appends ` (#NNNN)`); no WIP or draft markers at merge.

<a id="body"></a>Body: the first paragraph must stand alone after `git log --oneline` plus one `git show`: symptom or gap, mechanism, what the change does. <a id="compatibility-line"></a>Then compatibility impact, stated every time; write "None" when there is none. Benchmark: one sentence with the workload named, and only a result that stock tooling can reproduce (`valkey-benchmark`, a gtest); numbers from a throwaway DEBUG hook or a local script stay on the PR, since the commit cannot be checked against them. Tables are fine when they are the evidence. `Fixes #N` as its own trailer line, always, whenever the PR resolves an issue: it closes the issue on merge, and the one reference comment it posts per release-branch cherry-pick is a link worth having. Write the body unwrapped; the web merge dialog wraps the body at 72 columns on commit (`gh pr merge` does not), so merge from the web UI.

<a id="merge-dialog"></a>Remove in the merge dialog: `@mentions` (they fire on every cherry-pick to a release branch), test-run output ("370 passed"), checklists, review-process chatter ("addressed comments", "rebased"), screenshots. Keep the mechanism paragraph even when trimming hard.

## Where the numbers come from

<a id="data-sources"></a>

Every count above is from a GitHub API pull of the 981 PRs merged into valkey-io/valkey between 2025-10-16 and 2026-10-14: files touched, reviewers, review threads and their outcomes, labels and timeline. The 21 post-merge regressions were traced to the PR that introduced each, within the same window. The about 160 commits that fix a flaky test run from 2022-03-20 to the time of the study (October 2026); the exact end date of that series was not recorded. The dataset and the scripts that build it are not published.
