# Workflow inventory

Inventory captured from the live repository at the MARK-373 evaluation
checkpoint.

| workflow/caller | event | branch/state | automatic? | paid-equivalent? | runs during Draft? | rationale |
|---|---|---|---|---|---|---|
| `.github/workflows/marketplace-validation.yml` | `pull_request`: opened, synchronize, reopened, ready_for_review | PR; job guard requires `draft == false` | yes | yes | no | canonical hosted validation; Draft PR events are filtered by the job condition |
| `.github/workflows/marketplace-validation.yml` | `push` | `main` only | yes | yes | n/a | post-merge/main validation |
| `.github/workflows/marketplace-validation.yml` | `workflow_dispatch` | manually selected ref | no | yes | only when explicitly dispatched | explicit manual operation, not Draft iteration |
| `.github/workflows/INDEX.md` | none | documentation index | no | no | no | generated non-executable inventory surface |

## Workflow definition facts

There is one tracked executable workflow YAML: `.github/workflows/marketplace-validation.yml`.
It has no `workflow_call`, `workflow_run`, `pull_request_target`, or `schedule`
trigger. It has one job, `marketplace-validation`, and its validation command is
`tools/run ci --check` after checkout, `origin/main` fetch, Python 3.12 setup,
and dependency installation. The automatic PR job guard is:

```text
github.event_name != 'pull_request' || github.event.pull_request.draft == false
```

## Caller search

The live-repository search covered `.github`, `tools`, `.agents`, `tests`, and
the root package/config files for local reusable workflows, workflow events,
Actions dispatch calls, and equivalent CI commands. Results are classified as
follows:

| hit class | result |
|---|---|
| executable workflow caller | none beyond the canonical workflow above |
| manual-only caller | `workflow_dispatch` in the canonical workflow |
| documentation or test fixture | references to `tools/run ci --check` in runbooks, plans, specs, and pressure fixtures |
| irrelevant | historical/completed plan prose and generated/downstream copies |

No tracked workflow or automation caller automatically runs the equivalent
paid validation during Draft PR iteration. Feature-branch pushes are not a
workflow trigger. A manual dispatch remains possible by explicit operator
choice and is not evidence of an automatic Draft bypass.
