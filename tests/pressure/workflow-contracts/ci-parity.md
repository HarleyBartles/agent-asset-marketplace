# CI parity

## Canonical registry

The hosted workflow `.github/workflows/marketplace-validation.yml` runs:

```text
tools/run ci --check
```

The shared registry is `_TASKS["ci"]` in `tools/run.py`. Its dependency list
is exactly `lint`, `repo-standards`, `validate`, and `archive-links`; normal DAG
resolution adds the transitive `mesh` dependency of `validate`.

## Local and hosted sequences

| path | sequence | parity result |
|---|---|---|
| hosted Ready PR or `main` push | checkout -> fetch `origin/main` -> Python 3.12 -> install requirements -> `tools/run ci --check` | uses the canonical CI registry in check mode |
| normal local commit | materialize the staged snapshot -> `tools/run ci --apply` -> stage only owned generated surfaces -> `tools/run ci --check --diagnostics` | uses the same canonical registry after mechanical apply; diagnostics collect independent failures |
| local uncommitted check | `tools/run ci --check` or `--check --diagnostics` when explicitly needed | same registry and check targets; no apply step |

The pre-commit hook is the local tracked-gate authority. Its apply step may
materialize generated outputs, but it does not replace or narrow the hosted
check. Hosted CI does not omit the local target sequence; its environment and
fail-fast/diagnostics behavior are the only material differences.

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
