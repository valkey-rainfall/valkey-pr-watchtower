# Stage brief: draft and passes

This stage turns evidence into a review: a body, anchored inline comments, and replies on existing threads. Separate checkers read the draft, each for one thing, and the drafter applies their findings in rounds. The stage ends by staging a pending review for the maintainer to read and publish. See [the pipelines model](README.md#model) for the rules every stage follows.

## Reads

<a id="reads"></a>

- The evidence file, or for a fast-lane PR the triage record and the short evidence file from the [fast-lane read](README.md#fast-lane).
- Content decisions from the maintainer when there are any: event, blocking items, questions, which suggestions to keep. These are fixed. No pass reopens them.
- The PR description, threads and the current head. The diff is the one GitHub serves for the PR, not a local merge base: a merge from the base branch moves the local one.
- The PR's lockkeeper status: whether the maintainer already has a pending review on the PR, and whether the maintainer edited the pipeline's staged one. See [lockkeeper](README.md#lockkeeper).
- The [review guide](../review-guide.md) at the pinned commit, mostly [writing the review](../review-guide.md#writing-the-review).
- For the cold reader: the common-knowledge baseline (what a Valkey contributor can be assumed to know), the published docs at a pinned commit, and `valkey.conf` at the merge base.

## Steps

<a id="steps"></a>

1. Facts. Re-check the evidence file against the live PR: the head SHA and new comments first. Every claim the review will make must have a line in it with its source (path and line at the current head, test output, URL), including one for every acceptance criterion the review asks for; add what is missing, with its source. List dropped evidence items with the reason.
2. Draft. Write the body, the inline comments and the thread replies in one file, then generate the review payload from it: body, and for each inline comment the path, line, side, and start line for a multi-line comment. The payload has no event (Approve, Comment or Request changes); the stage reports the recommended one, per [the review event](../review-guide.md#review-event).
   - Body order: what looks right and the evidence for the verdict, then the blocking items (a table when there are several), then the answers to questions, then non-blocking notes.
   - Inline: one mechanism each. Optional ones are marked per [nit markers](../review-guide.md#nit-markers). A `suggestion` block when the fix is one or two lines; long evidence in `<details>`.
   - Answers follow the guide's [answer in place](../review-guide.md#answer-in-place) rule; a reply to an inline thread is staged on that thread, not posted. One reply per thread, and none on a resolved thread, which GitHub keeps folded.
   - Per [do not repeat](../review-guide.md#do-not-repeat), an inline comment that only agrees with an existing thread is never staged.
3. Checker passes, the four passes a to d below. Each checker runs in its own fresh session, started for that one pass and that one round, so round two has new checkers. Each sees only its own input folder. The drafter never checks its own text, and no checker sees another checker's output or the drafter's reasoning. Lockkeeper builds the folders, one per pass, with nothing else in them; see [lockkeeper](README.md#lockkeeper). Two rule files recur below: the language rules (B2 English, ASCII only, no hard-wrapped lines, precise links) and the review text rules (what a review body must contain and avoid, following the guide's [writing the review](../review-guide.md#writing-the-review)). Each checker writes a verdict file: the first four lines are the verdict, the id of the checker's session (filled in by the drafter, because a checker cannot see its own), the input folder, and the round; findings follow as a numbered list under a `Findings` heading. No pass edits the draft.
   - a. Accuracy: every sentence against the evidence file, the threads and the code at head. Gets the draft, the evidence file, the threads, the PR diff and the changed files at head; the drafter adds the review text rules. Flags overclaims, facts the evidence file does not have, and text the rules forbid. Verdict ACCURATE or FIX.
   - b. Cold reader, as the PR author: gets the draft, the common-knowledge baseline, the published docs at the pinned commit and `valkey.conf` at the merge base. It may look up what the draft names or links (a command, a config, an INFO field) in the docs, and lists every lookup in its verdict. For each item: what am I asked to do, does it block, what does done look like. The verdict is UNCLEAR when the main point only makes sense after a lookup; a docs page that contradicts the draft is flagged for accuracy; a feature with no docs page yet is normal and the draft must explain it. Verdict CLEAR or UNCLEAR.
   - c. Style: B2 English, ASCII only, no hard-wrapped lines, [cross-references](../review-guide.md#cross-references), [review markdown](../review-guide.md#review-markdown), [provenance](../review-guide.md#provenance), nit markers on every optional inline comment. Gets the draft, the language rules and the review text rules. Verdict PASS or REVISE.
   - d. Tone and proportion: gets the draft, the review text rules and a "do not challenge" list of the review's fixed decisions (verdict, blocking point, whether the "what looks right" line may be a bare confirmation). Checks [do not repeat](../review-guide.md#do-not-repeat), [no rebase nudges](../review-guide.md#no-rebase-nudges), [deferral](../review-guide.md#deferral), [request changes](../review-guide.md#request-changes); length against the guide's [comment length](../review-guide.md#comment-length) as a reasoned target, not a fixed number. Verdict PASS or REVISE.
   - e. Placement, run by the drafter: every anchor is a right-side line in the PR diff at head and on topic; each suggestion block replaces exactly its lines with valid code; a multi-line suggestion leaves the rest of the code consistent; the payload is valid.
4. Rounds. Every review gets two rounds of all four checker passes, the fast lane included. A round applies all findings in one new draft: for each finding, change the text, or write one line in the round's notes on why not; the evidence wins over a checker's opinion. Add any new fact to the evidence file first, with its source. After round two, pure cuts and rewording from its verdicts may still go in, listed in the notes. Any added or changed factual sentence gets one more accuracy pass by a new checker, because text written to answer a pass is the least checked text in the draft. Regenerate the payload from the final draft.
5. Stage. Confirm the PR head has not moved since the evidence file was checked and that the maintainer has no pending review on the PR, then stage the pending review. Record it with lockkeeper: the review id, one reason per inline comment and for the body (blocking or optional, with its evidence), each staged reply, and any backport row. File every verdict file and notes file as it is written; an edit or a reply recorded after the last round's files makes the writing gate stale until a new round is filed. An edit of the staged review on GitHub is recorded at once, naming every changed part; a part not named counts as the maintainer's. The pipeline does not touch a staged review the maintainer has edited: no change, no re-stage, no delete.

A fast-lane PR uses the same steps with a short draft.

## Produces

<a id="produces"></a>

The final draft, the payload built from it, the checked evidence file, each round's verdict files and notes, and the staged pending review with its reasons. A short hand-off for the maintainer: the body, the inline anchors, the staged replies, the recommended event, and any open point left from the last round.

## Gate

<a id="gate"></a>

Two full rounds exist. The last round's four verdict files come from distinct sessions, none of them the drafter's, and are on the current head. Every verdict is clean, or each open finding has its one-line note. Placement confirms every anchor on the current head, and the maintainer has no pending review on the PR. Lockkeeper reads the same files and shows the result, the writing gate, on the staged review: satisfied, open points, waiting or stale. A finding from any pass that round two leaves without a fix or a note sends the item to "Needs you". The stage never submits the review.
