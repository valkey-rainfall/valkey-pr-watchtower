# Stage brief: evidence

Evidence gathers the facts a Flow A review needs. It writes findings, not review prose: no verdict, no wording. It posts nothing to GitHub. See [the pipelines model](README.md#model) for the rules every stage follows.

## Reads

<a id="reads"></a>

- The triage record: route, ladder rung, triggers, flags, head SHA.
- The PR: diff as GitHub serves it, the code around every hunk, description, threads, reviews, CI runs on the current head, and linked issues.
- The PR's base (the merge-base) and the maintained release branches, read from the upstream repository.
- The [review guide](../review-guide.md) at the pinned commit, and the flaky-test checklist it points to.

## Passes

<a id="passes"></a>

Run every pass. When a pass does not apply, say so and why.

| Pass | What it records | Guide sections it applies |
|---|---|---|
| A. History | Who is assigned; what others already said; which points are valid, already fixed, or wrong; what nobody has said yet; approvals and whether they are on the current head. List "already raised by X" separately from "new". | [read threads](../review-guide.md#read-threads), [do not repeat](../review-guide.md#do-not-repeat), [stale PR](../review-guide.md#stale-pr) |
| B. Mechanics | Every hunk read in its whole function and its callers. The invariant the fix relies on and whether it holds. Sibling cases the fix misses. Every claim in the description checked, including its premise outside the diff. | [correctness classes](../review-guide.md#correctness), [compatibility](../review-guide.md#compatibility), [claim premise](../review-guide.md#claim-premise), [siblings](../review-guide.md#siblings), [hostile input](../review-guide.md#hostile-input) |
| C. Reproduction | Build the head and the base. Show the new test fails on the base and passes on the head. If it passes on the base, or there is no test, say so plainly. For each untested path, a model test (file and line), its rough size, and anything new it needs. For a deflake, a [confirmation run](#confirmation-runs). | [fails on base](../review-guide.md#fails-on-base), [cheap missing test](../review-guide.md#cheap-test), [plausible answer](../review-guide.md#plausible-answer) |
| D. Test quality | The flake checklist item by item on every new or changed test, each item marked clean, minor or problem with its line. The test's oracle. Whether a convergence-heavy suite needs an extra-tests or valgrind run. | [flake read](../review-guide.md#flake-read), [test oracle](../review-guide.md#test-oracle), [test_defer](../review-guide.md#test-defer), [valgrind budget](../review-guide.md#valgrind-budget), [extra tests](../review-guide.md#extra-tests), [deflakes](../review-guide.md#deflake) |
| E. CI | Every failing check on the current head, its log, and whether the red belongs to the PR. | [flakes and red CI](../review-guide.md#flakes) |
| F. Backport | For each maintained release branch: affected or not, from the code on that branch and the introducing commit. Whether the PR is in each release project with the right status. | [backport](../review-guide.md#backport), [backport project](../review-guide.md#backport-project) |
| G. Release notes | A call of yes, lean yes, no or lean no on the release-notes label, with one line on why. | none |
| H. Mechanical | Docs need, command JSON and key specs, build wiring, license header, code rules, triggers confirmed against the diff. | [mechanical](../review-guide.md#mechanical), [major decision](../review-guide.md#major-decision), [log wording](../review-guide.md#log-wording), [code rules](../review-guide.md#code-rules), [release check](../review-guide.md#release-check) |
| I. Squash commit | Title, body, compatibility line, issue trailer, characters that do not belong in history. | [squash commit](../review-guide.md#squash-commit) |

For a PR with a `perf: claim` flag, pass B also checks the claim against the guide's [evidence bar](../review-guide.md#perf-evidence). A `perf: risk` flag adds nothing to the findings; it stays a "needs you" item.

## Confirmation runs

<a id="confirmation-runs"></a>

A deflake, or any fix whose test fails only sometimes, is confirmed on the project's own CI runners; a local loop on a developer machine helps with debugging and is never the evidence.

- The run is a manual dispatch of the project's daily workflow on valkey-io/valkey, pointed at the PR head (the fork and the full commit SHA), trimmed to the job variant where CI fails and the suite that holds the test, with the test's file and a loop count. A base run points at the project repository and the merge-base SHA. The workflow's dispatch inputs name the job groups and suites to skip; read it on unstable first, because the groups change.
- About 100 runs on the head; also about 100 on the merge base when the base flake is not already shown by CI history or by the author. When the base fails often (for example 10 of 30), a few dozen clean head runs show the improvement; say which choice was made and why.
- One dispatch per commit. The workflow's concurrency group is keyed on the commit it tests and cancels a run in progress, so a second dispatch for the same commit stops the first. Put every variant one commit needs into one dispatch; different commits can run in parallel.
- Skip the run when the author already posted a similar one (about 100 runs of the same test on the fix) and link to it instead.
- Report fails per runs for base and head, with the variant, and cite the run links in the review text.

## Practical rules

<a id="practical"></a>

- Run one test file at a time, with a timeout. If something hangs, stop it and report it.
- Re-read the live PR before finishing: head SHA, new comments, CI. A moved head means the evidence is for the wrong commit.
- When a test needs resources the local host cannot give (large memory, a sanitizer), say so; it becomes a "needs you" item.

## Produces

<a id="produces"></a>

One evidence file per PR, filed with lockkeeper in the section order it reads:

1. Summary in three lines: is the fix right, does the test reproduce, the biggest issue.
2. One section per pass, A to I.
3. Findings, numbered. Each one: blocking, non-blocking, or pre-existing and out of scope; path and line at the current head; trigger; consequence; smallest fix; new or already raised by whom.
4. Backport table and release-notes call.

"Needs you" items (an extra-tests run, a benchmark) are flags, not sections of the file. Test results go in a separate results file: one row per test and variant with repeats and the base and head outcome, filed with lockkeeper too. Lockkeeper can run the same tests itself; for now that run is a trial whose results never replace the pipeline's, and a mismatch between the two goes in the report. A security-adjacent finding goes in a private note and a private flag, never in the evidence file.

## Gate

<a id="gate"></a>

The head SHA matches the one the stage started on, and every pass is done or marked "not applicable" with a reason. Nothing was written to GitHub.
