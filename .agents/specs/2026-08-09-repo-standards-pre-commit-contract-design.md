# Design: repo-standards pre-commit contract and staging

## Problem

The `repo-standards` skill enforces a byte-for-byte identical pre-commit hook at `.git/hooks/pre-commit` by comparing the hook to the vendored template in `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pre-commit`.

This causes two related problems:

1. **No local customization.** Consumer repos cannot have a pre-commit hook that adapts to their own needs (e.g., different staging strategy, local-only checks) without tripping `repo-standards` `drift` findings.
2. **Over-staging.** The current template ends with `git add -A`, which stages every modified and untracked file in the working tree. This can pull in untracked artifacts the author did not intend to commit.

The canonical fix belongs in the `repo-standards` source skill. Consumer copies are installed from this source and refreshed by `refresh-installed-skills`; editing them locally is futile.

## Goals

1. Allow consumer repos to own their `.git/hooks/pre-commit` content while still guaranteeing the hook satisfies the `repo-standards` contract.
2. Make the default `pre-commit` template safer by staging only surfaces that `tools/run.py ci --apply` is allowed to regenerate, rather than all files.
3. Keep the default template the source-of-truth for newly-initialized repos, but do not force existing repos to match it exactly.

## Non-goals

- Redesigning the `ci --apply` task runner or the set of surfaces it regenerates.
- Adding a new pre-commit format or switching to a framework like pre-commit.
- Changing CI behavior (pre-commit hooks are already skipped in CI; see `repo_standards.py` `_is_ci()`).

## Affected surfaces

### Source custody

- `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py` (the validator)
- `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pre-commit` (the default hook template)
- `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md` (shape description)
- `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-manifest.json` (manifest surface definitions)

### Installed copy (regenerated)

- `.agents/skills/repo-standards/` will receive the updated skill copy when `marketplace --apply` is next run.

## Contract

### Pre-commit hook contract

A valid `.git/hooks/pre-commit` must:

1. Be a file at the platform's git hooks path (`git rev-parse --git-path hooks`/pre-commit).
2. Be executable.
3. Invoke `tools/run.py ci --apply` (or `py -3 tools/run.py ci --apply`) so the mechanical surfaces are regenerated before each commit.
4. Run with `set -euo pipefail` or an equivalent `errexit`/`nounset`/pipefail guard.
5. Not be required to equal the vendored template.

### Default template contract

The default `templates/pre-commit` should:

1. Run `tools/run.py ci --apply --allow-shared-checkout` as it does today.
2. Stage only the set of paths `ci --apply` is permitted to write.
3. If a deterministic list cannot be produced, at minimum avoid staging untracked files not created by the apply step.

## Proposed design

### 1. Validator: contract check for hooks

In `repo_standards.py`, for `kind == "hook"`, replace the byte-for-byte `expected == actual` check with a contract scan:

- Confirm the hook path is a regular executable file.
- Confirm the file content contains `tools/run.py ci --apply` (allowing `py -3 tools/run.py ci --apply`, `python3 tools/run.py ci --apply`, etc.).
- Confirm the file content contains `set -euo pipefail` (or the three options independently).
- (Optional) Confirm the hook does not contain `git add -A` as a warning, not a hard error, to nudge consumers away from the old template.

Do not require the content to equal `templates/pre-commit`.

### 2. Apply behavior for hooks

The `--apply` path for `kind == "hook"` already scaffolds the hook if it is missing. Leave that behavior unchanged. Do not overwrite an existing local hook unless `--force` is supplied.

### 3. Template: targeted staging

Change `templates/pre-commit` from a single `git add -A` to a two-step staging strategy:

1. Re-stage any tracked files that the hook itself may have modified by running `ci --apply`. Use `git diff --name-only --diff-filter=M` after the apply and `git add` each modified tracked file.
2. Add the canonical generated file globs that `ci --apply` creates or updates and that may not yet be tracked in a fresh checkout:
   - `INDEX.md`
   - `**/INDEX.md`
   - `INDEX.json`
   - `**/INDEX.json`
   - `.provenance.json`
   - `.agents/skills/.provenance.json`
   - `codex-marketplace/plugin-roots.json`
   - `.agents/plugins/marketplace.json`
   - `codex-marketplace/manifest.json`

This is not perfectly minimal, but it is far narrower than `git add -A` and does not stage arbitrary untracked files.

If a generated file is not on this list and not already tracked, the commit fails and the author must stage it explicitly. This is acceptable because the `ci --apply` contract is stable and the listed paths cover the current generation surface.

### 4. Standards documents

Update `repository-shape-standard.md` and `repository-shape-manifest.json` so the pre-commit hook surface is described as a contract, not a pinned file copy. Remove or reword language that claims the hook is generated byte-for-byte from the template.

## Trade-offs

- **Contract vs. byte-for-byte:** Contract validation gives consumers flexibility but is slightly harder to test. The existing template still provides a reference implementation.
- **Targeted staging vs. `git add -A`:** Targeted staging avoids the untracked-file footgun but requires the template to keep its path list in sync with `tools/run.py` generated outputs. If new generated surfaces are added, the list may need updating. A future enhancement could have `tools/run.py` emit a list of written paths and consume it from the hook.
- **No `--force` overwrite by default:** Prevents `repo-standards --apply` from clobbering a repo's custom hook. `--force` can still be used to reset to the template.

## Validation

- `py -3 tools/run.py ci --check` must pass.
- A unit/CLI test or local manual test should verify that a modified pre-commit hook passes `--check` when it contains the contract elements.
- The default template should be checked to confirm `git add -A` is gone and the new staged paths are syntactically valid.
- `py -3 tools/run.py marketplace --apply` must regenerate the pack copy and installed copy correctly.

## Handoff

This design is intentionally small enough for one implementation plan. The planner should prepare:

1. Edit `repo_standards.py` hook validation.
2. Edit `templates/pre-commit` staging.
3. Update `repository-shape-standard.md` and `repository-shape-manifest.json`.
4. Run `marketplace --apply` to refresh installed copies.
5. Run `ci --check`.
6. Commit and open a draft PR.
