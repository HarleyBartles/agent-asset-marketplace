# Preflight surface relocation

## Problem

The root `scripts/` directory has only one job: it holds `ci-preflight.sh` and
`ci-preflight.ps1`. The name `scripts/` is a generic magnet for arbitrary
repo-owned scripts, but the standard does not intend it to be a dumping ground.
Only the preflight files live there.

## Goal

Move the preflight files from `scripts/` to a directory whose name matches its
purpose: `pre-commit/`. This makes the repo's surface shape self-describing and
removes the temptation to add unrelated scripts to a folder called `scripts/`.

## Non-goals

- Do not change `.agents/skills/<skill>/scripts/` directories.
- Do not change `tools/`.
- Do not remove the preflight files; only relocate them.
- Do not change the preflight logic beyond the path.

## Design

### New location

- `pre-commit/ci-preflight.sh`
- `pre-commit/ci-preflight.ps1`
- `pre-commit/INDEX.md` (generated or tracked alongside the preflight files)

The existing `scripts/` directory at the repo root becomes surplus and is no
longer scaffolded or validated by `repo-standards`.

### Updates to `repo-standards`

- `repository-shape-manifest.json`:
  - Change `ci-preflight-sh` path from `scripts/ci-preflight.sh` to
    `pre-commit/ci-preflight.sh`.
  - Change `ci-preflight-ps1` path from `scripts/ci-preflight.ps1` to
    `pre-commit/ci-preflight.ps1`.
- `scaffold_ci_preflight.py`:
  - Write files to `pre-commit/` instead of `scripts/`.
  - Create the directory if missing.
  - Keep the same template content and behavior.
- `templates/pre-commit`:
  - Update the hook path from `scripts/ci-preflight.sh` to
    `pre-commit/ci-preflight.sh`.
- Skill docs and references that mention `scripts/ci-preflight` to use
  `pre-commit/ci-preflight`.

### Backward compatibility

- `repo-standards --check` should report drift if the old `scripts/ci-preflight`
  files still exist and the new `pre-commit/` files are missing.
- `repo-standards --apply` should create `pre-commit/` and not automatically
  delete the old `scripts/` files. Repo maintainers can remove `scripts/`
  manually after verifying the new surface is in place.
- Consumer repos that already have `scripts/ci-preflight` will see the same
  drift; the repo's normal `apply` flow can recreate the files in `pre-commit/`.

### Marketplace mirror

Because `repo-standards` is a marketplace skill, the templates and scaffolder
updates must be reflected in the generated `codex-marketplace` plugin mirrors
after `py -3 tools/run.py marketplace --apply`.

### Files to touch

- `.agents/skills/repo-standards/references/repository-shape-manifest.json`
- `.agents/skills/repo-standards/scripts/scaffold_ci_preflight.py`
- `.agents/skills/repo-standards/templates/pre-commit`
- `.agents/skills/repo-standards/references/skill-script-contract-validator.md`
  if it references the preflight path
- Any `SKILL.md` or `AGENTS.md` that references `scripts/ci-preflight`
- `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/...` via
  `py -3 tools/run.py marketplace --apply`

### Validation

- After migration in this repo:
  - `py -3 tools/run.py repo-standards --check` reports `OK`.
  - `py -3 tools/run.py ci --check` passes.
  - The `.git/hooks/pre-commit` script calls `pre-commit/ci-preflight.sh` and
    that script runs successfully.

### Handoff

The planning agent should produce a plan that first updates `repo-standards`
scaffolds and templates, then updates the shape manifest, then moves the actual
preflight files in this repo, and finally regenerates the marketplace bundle.
