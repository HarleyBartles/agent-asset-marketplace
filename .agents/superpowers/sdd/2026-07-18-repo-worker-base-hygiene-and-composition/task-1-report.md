# MARK-336 Task 1 report

## Status

RED baseline created. This task intentionally adds contract tests and pressure
scenarios only. No source skill, router, guide, projection, package, or
generated artifact was changed.

## Worktree

- Repository: `Z:\agent-asset-marketplace`
- Worktree: `Z:\_agent-worktrees\agent-asset-marketplace\2026-07-18-harleydbartles-mark-336-add-focused-repository-hygiene-references-to-repo-worker`
- Branch: `harleydbartles/mark-336-add-focused-repository-hygiene-references-to-repo-worker`
- Starting `origin/main`: `c7e3273410a73376182d994bee1849a973c323c5`
- Starting worktree state: clean
- Branch base: `origin/main` (planning commit already present on the branch)
- Task commit: see the final handoff for the immutable commit SHA.

## Added files

- `tests/test_repo_worker_base_contract.py`
- `tests/pressure/repo-worker-base/README.md`
- `tests/pressure/repo-worker-base/repo-backed-superpowers-lane.md`
- `tests/pressure/repo-worker-base/worktree-resolution.md`

The test contract covers all ten focused reference filenames, machine-specific
drive-letter assumptions, portable worktree and scratch conventions, router
ordering, and the four canonical `.agents/guides/` stage-guide paths. The
existing `.agents/docs/guides/` home is retained as the expected RED baseline.

## Validation

Command:

```text
py -3 -m pytest tests/test_repo_worker_base_contract.py -q
```

Intentional result: `4 failed, 1 passed in 0.12s`.

The four failures are expected because the ten reference files do not yet
exist, the router does not yet place `repo-worker-base` before
`using-superpowers`, and the four canonical `.agents/guides/` files have not
yet migrated from `.agents/docs/guides/`. The drive-letter source-text check
passes.

## Concerns

- The focused test must remain failing until the later implementation and
  guide-migration tasks land.
- No full marketplace, projection, package, provenance, or downstream
  validation was run because this task is test-only RED setup.
- Publication/PR work is outside this Task 1 brief; the commit is the requested
  handoff artifact.
