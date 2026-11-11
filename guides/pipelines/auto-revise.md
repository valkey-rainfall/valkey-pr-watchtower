# Stage brief: auto-revise

Auto-revise applies the self-review findings on one of the maintainer's own PRs (Flow B). Safe fixes are pushed as new commits; everything else is staged for the maintainer. See [the pipelines model](README.md#model) for the rules every stage follows.

## Reads

<a id="reads"></a>

- The self-review findings and status row.
- The PR branch, its base, and the PR description.
- The [auto-revise triage table](README.md#auto-revise).
- The [review guide](../review-guide.md) at the pinned commit, and the [PR description guide](../pr-description-guide.md).

## Steps

<a id="steps"></a>

1. Sort every legitimate finding into a column of the [triage table](README.md#auto-revise), with the reason. When the column is unclear, or the PR already has an approval, the finding is staged.
2. For the push column: make one change per finding, sign off every commit (DCO, see [mechanical](../review-guide.md#mechanical)), run the related tests, and push as a new commit with a plain push. Never amend or force-push an existing commit on the PR branch. A description or title change is an edit to the PR, not a commit.
3. For a rebase: rebase onto unstable only when it is clean, run the related tests, and push with the lease pinned to the branch's previous SHA.
4. For the staged column: put the changes on `<branch>--proposed` on the fork, one commit per finding, and list each one with its reason.
5. Check every test robustness fix against the guide's [deflake rule](../review-guide.md#deflake) before it goes in the push column.
6. Write the PR description against the guide's [squash commit](../review-guide.md#squash-commit) rules, including the [compatibility line](../review-guide.md#compatibility-line), and the [PR description guide](../pr-description-guide.md). A changed description goes through the checker passes again before it is published; see [self-review](self-review.md#passes).
7. For a failing check on the current head: when a known flake or an infrastructure failure explains it and the diff does not, record the flake per the guide's [flakes rule](../review-guide.md#flakes) and [red CI test](../review-guide.md#red-ci), rerun only the failed jobs, and note it. No code or test change is pushed for a failure the PR did not cause.

## Produces

<a id="produces"></a>

Pushed commits, a staged branch when there are staged changes, an updated description, and a short list for the maintainer: each staged item, each finding left open, each with its triage reason.

## Gate

<a id="gate"></a>

Every pushed commit has its related tests green on head, no force-push happened except the pinned rebase, no existing commit was amended, and every finding is either pushed, staged, or listed as open with a reason. The PR then moves to "Proposed", or straight to "CI and checks" when nothing was staged.
