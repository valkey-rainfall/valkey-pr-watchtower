# Stage brief: draft and passes

This stage turns evidence into a review: a body and anchored inline comments. Separate passes check the draft, and one round applies all their findings. The stage ends by staging a pending review for the maintainer to read and publish. See [the pipelines model](README.md#model) for the rules every stage follows.

## Reads

<a id="reads"></a>

- The evidence file, or for a fast-lane PR the triage record and the one full read.
- Content decisions from the maintainer when there are any: event, blocking items, questions, which suggestions to keep. These are fixed. No pass reopens them.
- The PR description, threads and the current head.
- The [review guide](../review-guide.md) at the pinned commit, mostly [writing the review](../review-guide.md#writing-the-review).

## Steps

<a id="steps"></a>

1. Facts. Write a facts sheet: one line per claim the review will make, each with its source (path and line at the current head, test output, URL). Include a fact for every acceptance criterion the review asks for. Re-check the head SHA and new comments first. List dropped evidence items with the reason.
2. Draft. Write the body and the inline comments in one file, then generate the review payload from it: body, and for each inline comment the path, line, side, and start line for a multi-line comment. The payload has no event.
   - Body: what looks right in one or two sentences, then the blocking items (a table when there are several), questions as questions, and only the suggestions that have no inline home. Do not restate the inline comments.
   - Inline: one mechanism each. Optional ones are marked per [nit markers](../review-guide.md#nit-markers). A `suggestion` block when the fix is one or two lines; long evidence in `<details>`.
   - Event: per [the review event](../review-guide.md#review-event).
3. Passes, in parallel. Each pass writes its own findings and a verdict. No pass edits the draft.
   - a. Accuracy: every sentence against the facts sheet and the code at head. Flag overclaims and facts the sheet does not have.
   - b. Cold reader, as the PR author: reads only the draft and the PR description. For each item: what am I asked to do, does it block, what does done look like.
   - c. Style: B2 English, ASCII only, no hard-wrapped lines, [cross-references](../review-guide.md#cross-references), [review markdown](../review-guide.md#review-markdown), [provenance](../review-guide.md#provenance), nit markers on every optional inline comment.
   - d. Tone and proportion: the fixed decisions listed as "do not challenge"; [do not repeat](../review-guide.md#do-not-repeat), [no rebase nudges](../review-guide.md#no-rebase-nudges), [deferral](../review-guide.md#deferral), [request changes](../review-guide.md#request-changes); length against the guide's [comment length](../review-guide.md#comment-length) as a reasoned target, not a fixed number.
   - e. Placement: every anchor is a right-side line in the PR diff at head and on topic; each suggestion block replaces exactly its lines with valid code; a multi-line suggestion leaves the rest of the code consistent; the payload is valid.
4. Round. Apply all findings in one new draft. Add any new fact to the facts sheet first, with its source. Re-run only the passes that had findings, and always re-run accuracy when sentences were added: text written to answer a pass is the least checked text in the draft. Regenerate the payload from the new draft.
5. Stage. Confirm the PR head has not moved since the facts sheet, then stage the pending review.

A fast-lane PR uses the same steps with a short draft.

## Produces

<a id="produces"></a>

The final draft, the payload built from it, the facts sheet, each pass's findings, and the staged pending review. A short hand-off for the maintainer: the body, the inline anchors, and any open questions.

## Gate

<a id="gate"></a>

A full round has no new accuracy finding, and placement confirms every anchor on the current head. The cap is two rounds; after that the item goes to "Needs you" with the open findings. The stage never submits the review.
