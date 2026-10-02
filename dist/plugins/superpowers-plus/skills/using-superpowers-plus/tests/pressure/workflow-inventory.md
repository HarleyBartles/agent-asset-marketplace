# Workflow inventory

Inventory refreshed after Plan 11 changed the live hosted workflow to validate Draft PRs and the exact proposed commit.

| workflow/caller                                | event                                                           | branch/state                            | automatic? | paid-equivalent? | runs during Draft?              | rationale                                                                      |
| ---------------------------------------------- | --------------------------------------------------------------- | --------------------------------------- | ---------- | ---------------- | ------------------------------- | ------------------------------------------------------------------------------ |
| `.github/workflows/marketplace-validation.yml` | `pull_request`: opened, synchronize, reopened, ready_for_review | PR head SHA | yes        | yes              | yes                             | canonical hosted validation checks the exact proposed commit, including Draft PRs |
| `.github/workflows/marketplace-validation.yml` | `push`                                                          | `main` only                             | yes        | yes              | n/a                             | post-merge/main validation                                                     |
| `.github/workflows/marketplace-validation.yml` | `workflow_dispatch`                                             | manually selected ref                   | no         | yes              | only when explicitly dispatched | explicit manual operation, not Draft iteration                                 |

## Workflow definition facts

There is one tracked executable workflow YAML: `.github/workflows/marketplace-validation.yml`. It has no `workflow_call`, `workflow_run`, `pull_request_target`, or `schedule` trigger. It has one job, `marketplace-validation`, which checks out `github.event.pull_request.head.sha || github.sha`, asserts that exact commit is detached and clean, fetches `origin/main`, installs Python 3.12 dependencies, and invokes `githooks/pre-commit` with the same SHA as `REPO_STANDARDS_HOSTED_COMMIT`. Draft PR events receive the gate.

## Caller search

The live-repository search covered `.github`, `tools`, `.agents`, `tests`, and the root package/config files for local reusable workflows, workflow events, Actions dispatch calls, and equivalent CI commands. Results are classified as follows:

| hit class                     | result                                                                                                     |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| executable workflow caller    | none beyond the canonical workflow above                                                                   |
| manual-only caller            | `workflow_dispatch` in the canonical workflow                                                              |
| documentation or test fixture | references to the tracked hook and `tools/run ci --check` in runbooks, plans, specs, and pressure fixtures |
| irrelevant                    | historical/completed plan prose and generated/downstream copies                                            |

The canonical pull-request workflow automatically runs the equivalent gate during Draft PR iteration. Feature-branch pushes remain excluded, while a manual dispatch on a selected ref remains an explicit operator action.
