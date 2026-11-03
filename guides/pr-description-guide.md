# Writing a Valkey PR description

How I write descriptions for pull requests to valkey-io/valkey, and the habits behind them. These are personal working notes, not project policy. The official process is in [CONTRIBUTING.md](https://github.com/valkey-io/valkey/blob/unstable/CONTRIBUTING.md); where this page and the project disagree, the project wins. Parts of this page were drafted with AI assistance and edited by me.

## Why the description matters

- **It becomes the commit message.** At the time of writing, the repository squash-merges with the PR title as the commit title and the PR body as the commit message. The text you write is what `git log` shows for years.
- **It is read twice, by different people.** A reviewer reads it today, to decide what to look for. A maintainer reads it later, to learn why the code looks this way. Write for the second reader and the first is also served.
- **Review time is limited.** A description that states the problem, the mechanism and the evidence saves the reviewer from working them out from the diff.

CONTRIBUTING.md asks for a clear statement of what you want to accomplish and why, and for `Fixes #xyz` in the description when the PR closes an issue. Everything below is a way of doing that well.

## Shape

Use short sections with bold labels or `##` headings. The order I use:

1. **Problem.** The symptom a user or developer sees, then the mechanism that causes it. If the bug is in upstream code (a dependency, a compiler, a sanitizer), say so and link the upstream issue.
2. **Fix.** What the change does and why this is the right place for it. State tradeoffs plainly: what gets slower, what behavior changes, what is lost.
3. **Validation.** What you ran and what it showed. Link the GitHub Actions run when CI is the evidence.
4. **Compatibility.** One line, even when the answer is "none". Reviewers look for it.

Small changes do not need headings. A two-paragraph description (problem and mechanism, then the change) is enough for a one-line fix. Add sections as the change gets bigger, not before.

Write the first paragraph so it still makes sense alone. It is the part people see first in notifications and previews. It should carry symptom, mechanism and change.

## Title

- Imperative mood, under about 72 characters, says what changed ("Fix return types of three module API declarations to match definitions").
- No PR number, no "WIP", no trailing period.
- Name the area when it helps ("valkey-benchmark: ..."), and match the prefix style of recent commits in that area.

## Attributing the cause

When a bug involves both code you depend on and your own code, separate them in the text:

- which defect is upstream's, and which is yours
- which part of the change fixes the cause, and which only works around it

A reader who cannot tell a workaround from a fix will treat the workaround as permanent design.

## Evidence

- **Show a reproduction** for a bug: the commands and the wrong output, then what you expect. A short code block is the best form.
- **Cite the documented behavior** when a command does not do what the documentation says. Link the page on valkey.io instead of paraphrasing it.
- **Say what the tests prove.** For a regression test, run it without the fix and confirm it fails; say so. A test that passes without the fix is a smoke test, and the description should not call it a guard.
- **Count tests honestly.** If you quote a number, take it from the test runner's list (`--gtest_list_tests` for the unit tests), not from counting parameterized definitions by hand.
- **For performance changes**, name the workload and hardware, give a before and after, and note the noise. Put full tables in a comment; keep a one-paragraph summary in the description, because the description is what lands in the commit.
- **For flaky-test fixes**, show the failing signature, the mechanism, and a repeated A/B run of the old and new code. "I ran it three times and it passed" is not evidence of a fix for an intermittent failure.

## Leave out

- A walk through the diff. The reviewer has the diff.
- Development history: "an earlier revision did X". It is not true of the merged code and it ages badly. If the history matters, put it in a comment.
- Pasted test output, long logs, checklists and process chatter.
- `@mentions`, which can notify people again when the commit is copied to other branches, and bare `#1234` references that the reader must decode. Prefer a full URL or "PR 1234" when the number is not part of a closing keyword.
- Claims you did not check ("known flaky", "pre-existing failure"). Link the evidence or leave the claim out.

Short is a goal, not an accident. Drafts written with AI help tend to run long; read yours once and cut every sentence that does not change what the reader does or believes.

## Formatting

- Do not hard-wrap paragraphs. One paragraph is one line; GitHub wraps it for display.
- Put lists of links as markdown lists of `[text](url)`. A URL inside a code block is not clickable.
- Use fenced code blocks for code and command output only, not for prose.
- Put `Fixes <issue URL>` or `Fixes #N` on a line by itself, near the end.
- Credit the person who reported the bug, by name or handle, in the description.

## Examples

Four merged PRs written in this style, each showing a different size of change:

- **A small fix: [PR 4676, fix three module API return types](https://github.com/valkey-io/valkey/pull/4676).** Two short paragraphs and a "found by" line. The first paragraph states the symptom and why it is undefined behavior; the second states the change and who is affected (nobody who ignored the return value). No headings were needed.
- **A bug with a reproduction: [PR 4497, lex range sentinel handling](https://github.com/valkey-io/valkey/pull/4497).** One section per bug. Each has a short reproduction in a code block, a link to the command documentation that the behavior violates, and the fix. A closing paragraph says why the tests had missed both bugs and what changed in them.
- **A flaky test: [PR 4251, `_exit()` when a child is killed](https://github.com/valkey-io/valkey/pull/4251).** Problem, Mechanism, Fix, Verification. The Problem section shows the log signature. The Verification section compares the old and new code on the same CI job, with the run linked.
- **A performance change: [PR 4332, valkey-benchmark hot path](https://github.com/valkey-io/valkey/pull/4332).** Summary, Changes, Results, Caveats. The Results section names the hardware and workload, and the Caveats section lists what the change does not guarantee.

These are my own PRs, so I can say what I was aiming for. They are examples of a style, not the only acceptable one; look at recently merged PRs from the maintainers of the area you are changing, too.

## Checklist before asking for review

1. The first paragraph makes sense on its own.
2. The title is imperative, short and specific.
3. Upstream versus own-code causes are separated, if both are involved.
4. Evidence is linked or shown, and test counts match the runner.
5. Compatibility is stated.
6. Nothing in it describes the diff line by line or an earlier version of the change.
7. The closing keyword (`Fixes ...`) is present if the PR closes an issue.
8. If you pushed more commits after writing it, the description still matches the current code.
