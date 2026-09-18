# CI parity

## Canonical CI registry

The hosted workflow `.github/workflows/marketplace-validation.yml` runs:

```text
REPO_STANDARDS_HOSTED_COMMIT=HEAD githooks/pre-commit
```

The hook reads `.agents/contracts/repo-standards-commands.json`, whose apply and
check vectors both use the shared `_TASKS["ci"]` registry in `tools/run.py`.
Its dependency list is exactly `lint`, `repo-standards`, and `validate`; normal
DAG resolution adds the transitive `mesh` dependency of `validate`.

## Local and hosted sequences

| path | sequence | parity result |
|---|---|---|
| hosted Ready PR or `main` push | clean checkout -> reconstruct `HEAD` as a staged snapshot over its first parent -> tracked hook -> declared apply -> declared check | uses the same tracked hook, staged-snapshot marker, and consumer command declaration as local Git |
| normal local commit | tracked hook -> materialize the staged snapshot -> declared apply -> stage only owned generated surfaces -> declared check | uses the same staged-snapshot marker and consumer command declaration as hosted validation |
| local uncommitted check | `tools/run ci --check` or `--check --diagnostics` when explicitly needed | same registry and check targets; no apply step |

The tracked pre-commit hook is the local and hosted gate authority. Hosted CI
names its checked-out commit with `REPO_STANDARDS_HOSTED_COMMIT=HEAD`; the hook
reconstructs that tree in the index, exports
`REPO_STANDARDS_STAGED_SNAPSHOT=1`, and verifies validation did not change the
published tree. Consumer commands use the staged index or complete materialized
tree rather than committed `HEAD` when that marker is present.

## Anti-bypass proof

| workflow/caller | event | branch/state | automatic? | paid-equivalent? | runs during Draft? | rationale |
|---|---|---|---|---|---|---|
| `marketplace-validation.yml` PR job | opened/synchronize/reopened | any PR, job requires non-Draft | yes | yes | no | Draft guard skips the job |
| `marketplace-validation.yml` PR job | ready_for_review | PR becomes Ready | yes | yes | no | Ready transition is the intended automatic start |
| `marketplace-validation.yml` push | push | `main` | yes | yes | n/a | feature branches are excluded |
| `marketplace-validation.yml` manual | `workflow_dispatch` | selected ref | no | yes | only by explicit dispatch | separate manual operation, not an automatic bypass |

No other tracked executable workflow, workflow caller, dispatch script, or
scheduled automation was found that invokes an equivalent paid validation
path. Any future caller must be added to `workflow-inventory.md` and this
table before it can be considered parity-safe.
