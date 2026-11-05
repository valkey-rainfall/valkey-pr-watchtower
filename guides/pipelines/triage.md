# Stage brief: triage

Triage decides the route for one PR and sets its flags. It reads; it does not review the code line by line. Both flows use it. See [the pipelines model](README.md#model) for the rules every stage follows.

## Reads

<a id="reads"></a>

- The PR: title, description, labels, file list and line counts, linked issues, every existing thread and review, approvals and the commit each one is on, and CI status on the current head.
- For a re-review: the last staged review and the head SHA it was written for.
- The [review guide](../review-guide.md) at the pinned commit.

## Steps

<a id="steps"></a>

1. Record the guide commit used and the PR head SHA.
2. Place the PR on the guide's [change ladder](../review-guide.md#change-ladder) and run the [release check](../review-guide.md#release-check). Note whether the PR has moved up a rung from what it was filed as.
3. List any [major-decision triggers](../review-guide.md#major-decision) and [log wording](../review-guide.md#log-wording) changes visible from the file list and the description.
4. For an old PR or a re-review, run the guide's [stale PR checks](../review-guide.md#stale-pr): approval on head, conflicts, base drift of the touched functions.
5. Set the [performance flag](README.md#perf-flag): `perf: claim`, `perf: risk`, or none, each with its reason.
6. Decide the route:
   - "Open the issue first" when the PR is on the third or fourth rung with no issue or design artifact. The route goes straight to drafting with that verdict.
   - Fast lane when the PR meets every [fast lane](README.md#fast-lane) condition. Record each condition and whether it held.
   - Full review otherwise.
7. Add "needs you" items that only the maintainer can act on: a first-time contributor's PR that touches `.github/` (the guide's [fork CI check](../review-guide.md#fork-ci)), and a `run-benchmark` request for `perf: risk`.

## Produces

<a id="produces"></a>

A triage record on the PR's status record: route and reason, ladder rung, release check result, triggers found, stale-PR results, performance flag and reason, "needs you" items, guide commit, and head SHA.

## Gate

<a id="gate"></a>

The route is set with a reason, and the guide commit and head SHA are recorded. A PR whose head moves during triage starts triage again.
