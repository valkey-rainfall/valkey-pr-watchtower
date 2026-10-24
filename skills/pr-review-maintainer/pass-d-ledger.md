# Pass D ledger

Does an adversarial second read of the diff (Subagent D in `SKILL.md`) find
things the mechanics read (Subagent B) does not, often enough to pay for the
run? One row per non-trivial review while D runs. PRs reviewed inline with no
subagents are not rows.

## Columns

- **date**: when the review was drafted (UTC date)
- **PR**: repo-qualified, e.g. `valkey-io/valkey#4895`
- **D total**: findings D returned (at most 5)
- **D unique**: of those, findings B did not raise
- **changed verdict**: unique findings that changed a severity call or the
  approve / request-changes outcome
- **posted**: unique findings that became a comment the maintainer posted.
  Filled in after the maintainer posts; `-` until then
- **model**: the model D ran on, or `same` when it matched the parent
- **note**: one line, optional. What the unique finding was, or why D was wrong

## Stop rule

At ten rows, sum `changed verdict` and `posted` over unique findings. Two or
more: keep D, drop the "experiment" marker in `SKILL.md`, and keep writing rows
only when something changes (new model, new brief). Fewer than two: fold D's two
questions into Subagent B's brief and remove D. Either way, the decision goes in
as the last row with the counts in the note.

Ten is small. It is enough to tell "D finds nothing B does not" from "D earns
its run", which is the only question here; it is not enough to compare models,
and the ledger does not try to.

## Where rows are written

This is the one file in the skill directory that the local copy edits directly;
`SKILL.md` stays canonical-by-PR. Append rows to the local copy as reviews
happen and sync them here by PR every few rows, or at the stop rule, whichever
comes first.

## Rows

| date | PR | D total | D unique | changed verdict | posted | model | note |
|------|----|---------|----------|-----------------|--------|-------|------|
