# CI parity

## Canonical CI registry

The hosted workflow `.github/workflows/marketplace-validation.yml` checks out and validates the exact proposed commit SHA for pull requests, or `github.sha` for pushes and manual runs:

```text
REPO_STANDARDS_HOSTED_COMMIT=<exact-proposed-commit-sha> githooks/pre-commit
```

The hook reads `.agents/contracts/repo-standards-commands.json`, whose apply and check vectors both use the shared `_TASKS["ci"]` registry in `tools/run.py`. Its dependency list is exactly `lint`, `repo-standards`, and `validate`; the validation DAG contains no index-mesh target.

## Local and hosted sequences

| path                           | sequence                                                                                                                            | parity result                                                                                     |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| hosted Draft or Ready PR, or `main` push | checkout and assert the exact PR head SHA or `github.sha` -> fetch `origin/main` -> reconstruct the commit as a staged snapshot over its first parent -> tracked hook -> declared apply -> declared check | uses the same tracked hook, staged-snapshot marker, and consumer command declaration as local Git |
| normal local commit            | tracked hook -> materialize the staged snapshot -> declared apply -> stage only owned generated surfaces -> declared check          | uses the same staged-snapshot marker and consumer command declaration as hosted validation        |
| local uncommitted check        | `tools/run ci --check` or `--check --diagnostics` when explicitly needed                                                            | same registry and check targets; no apply step                                                    |

The tracked pre-commit hook is the local and hosted gate authority. Hosted CI passes the exact PR head SHA, or `github.sha` for other events, as `REPO_STANDARDS_HOSTED_COMMIT`; both the workflow and hook reject a mismatch between that SHA and detached `HEAD`. The hook reconstructs that commit tree in the index, exports `REPO_STANDARDS_STAGED_SNAPSHOT=1`, and verifies validation did not change the published tree. Consumer commands use the staged index or complete materialized tree rather than committed `HEAD` when that marker is present.

## Anti-bypass proof

| workflow/caller                     | event                       | branch/state                   | automatic? | paid-equivalent? | runs during Draft?        | rationale                                          |
| ----------------------------------- | --------------------------- | ------------------------------ | ---------- | ---------------- | ------------------------- | -------------------------------------------------- |
| `marketplace-validation.yml` PR job | opened/synchronize/reopened | any PR, exact PR head          | yes        | yes              | yes                       | checks the proposed commit on every PR update       |
| `marketplace-validation.yml` PR job | ready_for_review            | PR becomes Ready               | yes        | yes              | yes                       | the exact-head gate continues when the PR becomes Ready |
| `marketplace-validation.yml` push   | push                        | `main`                         | yes        | yes              | n/a                       | feature branches are excluded                      |
| `marketplace-validation.yml` manual | `workflow_dispatch`         | selected ref                   | no         | yes              | only by explicit dispatch | separate manual operation, not an automatic bypass |

No other tracked executable workflow, workflow caller, dispatch script, or scheduled automation was found that invokes an equivalent paid validation path. Any future caller must be added to `workflow-inventory.md` and this table before it can be considered parity-safe.
