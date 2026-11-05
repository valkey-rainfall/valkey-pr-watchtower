# Stage brief: self-review

Self-review runs independent review passes on one of the maintainer's own PRs (Flow B) before other reviewers see it. Passes read and report; they do not edit the branch. See [the pipelines model](README.md#model) for the rules every stage follows.

## Reads

<a id="reads"></a>

- The triage record.
- The PR's diff against its base, the code around every hunk, the PR title and description, the linked issue or repro, and test logs.
- The [review guide](../review-guide.md) at the pinned commit.

A pass sees the diff, the issue and the logs. It does not see the author's reasoning, so it judges the change the way an outside reviewer would.

## Passes

<a id="passes"></a>

| Pass | Lens | Guide sections it applies |
|---|---|---|
| A. Guide | The guide's checklist: scope, ladder rung, triggers, mechanical checks, test present, commit and PR text. | [change ladder](../review-guide.md#change-ladder), [major decision](../review-guide.md#major-decision), [log wording](../review-guide.md#log-wording), [mechanical](../review-guide.md#mechanical), [code rules](../review-guide.md#code-rules) |
| B. Adversarial | Try to break the fix. Revert each hunk and show a test fails. Try to make the new test pass on the base. Try other configs: cluster, TLS, io-threads, RESP3, valgrind. | [fails on base](../review-guide.md#fails-on-base), [correctness classes](../review-guide.md#correctness), [test oracle](../review-guide.md#test-oracle) |
| C. Neighbor bugs | The same bug class at sibling sites, in other commands and on other branches. Each finding is "part of the fix" or "tracker item". | [siblings](../review-guide.md#siblings) |
| D. Test quality | The flake checklist on every new or changed test. Repeat the test about 20 times, and with `--accurate`, io-threads and valgrind where they apply. | [flake read](../review-guide.md#flake-read), [test_defer](../review-guide.md#test-defer), [valgrind budget](../review-guide.md#valgrind-budget), [deflakes](../review-guide.md#deflake), [cheap missing test](../review-guide.md#cheap-test) |
| E. Compatibility | Backport branches, behavior or error text or reply shape changes, docs need, release-note need, command JSON. | [compatibility](../review-guide.md#compatibility), [release check](../review-guide.md#release-check), [backport](../review-guide.md#backport) |
| F. Cold reader | A reader with only the PR text summarizes the change in two sentences. Checks B2 English and ASCII. | [squash commit](../review-guide.md#squash-commit), [compatibility line](../review-guide.md#compatibility-line) |
| G. Description accuracy | Every claim in the title and body against the code, including premises outside the diff. | [claim premise](../review-guide.md#claim-premise) |

Order: A, F and G first because they are cheap, then B, C and D in parallel, then E. After the fix round, a final B runs on the changed hunks only. A `perf: claim` flag adds the guide's [evidence bar](../review-guide.md#perf-evidence) to pass G.

Bugs found in other code go to the follow-ups tracker, not into the PR text; see [deferral](../review-guide.md#deferral).

## Produces

<a id="produces"></a>

One findings file per pass. Each finding: severity (Critical, High, Medium or Low), path and line, trigger, consequence, smallest fix. A status row per PR with one column per pass.

## Gate

<a id="gate"></a>

A full round has no new legitimate Critical or High finding. The cap is two rounds; after that the item goes to "Needs you" with the open findings. The findings then go to [auto-revise](auto-revise.md).
