---
date: 2026-07-27
topic: ci-preflight-pipeline
---

# CI Preflight Pipeline Design

## Goal

Make `scripts/ci-preflight` the repo-owned, read-only mirror of a repo's CI
pipeline. The preflight script runs the same checks as CI and tells the agent
the exact command to run when a check fails. The `repo-standards` skill provides a
scaffold, not a fixed pipeline.

## Scope

1. Rewrite `sources/first_party/skills/repo-standards/templates/ci-preflight.sh`
   and `.ps1` as a commented menu of available checks.
2. Add `sources/first_party/skills/repo-standards/references/ci-validation-pipeline.md`
   documenting the preflight/CI/pre-commit contract.
3. Update `sources/first_party/skills/repo-standards/references/repository-shape-standard.md`
   to describe `scripts/ci-preflight` as a required, repo-owned surface.
4. Update `sources/first_party/skills/repo-standards/SKILL.md` routing table to
   point to `ci-validation-pipeline.md`.
5. Rewrite `agent-asset-marketplace` `scripts/ci-preflight.sh` and `.ps1` to
   compose the full CI pipeline for this repo.
6. Update `.github/workflows/marketplace-validation.yml` to run the same checks
   as separate steps.
7. Delete `tools/check_marketplace.py`.
8. Update `tools/AGENTS.md`, `.agents/guides/*.md`, and `codex-marketplace/AGENTS.md`
   to remove `check_marketplace.py` references and point to the new pipeline.

## Non-goals

- Do not add a generic `ci-preflight-lint` or `ci-preflight-extra` hook standard;
  lint is inlined in the repo-owned preflight script.
- Do not make CI call `scripts/ci-preflight.sh`; CI and preflight are peers that
  compose the same commands.
- Do not change `tools/rebuild_marketplace.py` phase logic.
- Do not rewrite historical specs or plans.

## Principles

- `scripts/ci-preflight` is repo-owned and mirrors the CI pipeline for that repo.
- It is read-only in `--check` mode and never mutates.
- It is a warning-raiser: on failure it exits non-zero and prints the exact
  command(s) to run to fix the failure.
- The pre-commit hook fires `scripts/ci-preflight.sh --check`.
- CI composes the same checks as separate workflow steps.
- `tools/check_marketplace.py` is deleted; `tools/rebuild_marketplace.py --phase
  <phase> --check` is the decomposition primitive.

## Contract

### `repo-standards` skill

- `templates/ci-preflight.sh` and `templates/ci-preflight.ps1` are scaffolds.
  They include a commented list of common checks and a placeholder for
  repo-specific lint and final CI checks. They do not prescribe a fixed sequence.
- `references/ci-validation-pipeline.md` explains:
  - preflight is a repo-owned CI mirror;
  - the pre-commit hook fires preflight;
  - CI composes the same checks directly;
  - each failing check prints the command that repairs it.
- `references/repository-shape-standard.md` lists `scripts/ci-preflight.sh` and
  `scripts/ci-preflight.ps1` as required, repo-owned surfaces.
- `SKILL.md` routing table links to `ci-validation-pipeline.md` for "How
  preflight, pre-commit, and CI relate".

### `agent-asset-marketplace` preflight and CI

`scripts/ci-preflight.sh` and `.github/workflows/marketplace-validation.yml`
run the same checks, in this order:

1. **Lint changed Python files** — `ruff check` on files changed since
   `origin/main...HEAD`.
2. **Repo standards** —
   `bash .agents/skills/repo-standards/scripts/repo-standards.sh --check`
3. **Agent mesh validation** —
   `bash .agents/skills/generating-agent-mesh/scripts/validate-agent-mesh.sh --check`
4. **Marketplace inventory** —
   `python tools/rebuild_marketplace.py --phase inventory --check`
5. **Overlay healing** —
   `python tools/rebuild_marketplace.py --phase heal --check`
6. **Project/projection validation** —
   `python tools/rebuild_marketplace.py --phase project --check`
7. **Repo index and index-mesh** —
   `python tools/rebuild_marketplace.py --phase index --check`
8. **First-party skill catalog** —
   `python tools/rebuild_marketplace.py --phase catalog --check`
9. **Final validation** —
   `python tools/rebuild_marketplace.py --phase validate --check`

The `.ps1` preflight script uses the same steps with PowerShell-equivalent
invocation and error handling.

### Failure messages

Each failed check prints a repair command to stderr:

- Lint → `python -m ruff check --fix <files> && python -m ruff format <files>`
- Repo standards →
  `python .agents/skills/repo-standards/scripts/repo_standards.py --apply --yes`
- Agent mesh →
  `python .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py`
- Any `rebuild_marketplace` phase → `python tools/rebuild_marketplace.py` (full
  rebuild), then re-run preflight.

### Deletions and doc updates

- Delete `tools/check_marketplace.py`.
- Update `tools/AGENTS.md` to list the decomposed CI steps as the green-path
  proof and `python tools/rebuild_marketplace.py` as the local rebuild command.
- Update `.agents/guides/testing-guide.md`, `.agents/guides/pr-guide.md`,
  `.agents/guides/implementing-guide.md`, `.agents/guides/marketplace-generation-guide.md`,
  `.agents/guides/code-review-guide.md`, `.agents/guides/skill-authoring-guide.md`,
  and `.agents/guides/planning-guide.md` to replace `check_marketplace.py`
  references.
- Update `codex-marketplace/AGENTS.md` to point to the new CI pipeline instead
  of `check_marketplace.py`.

## Testing and verification

- Run `bash scripts/ci-preflight.sh --check` locally and confirm each step
  reports OK.
- Run the workflow steps locally or in CI and confirm equivalent output.
- Run `py -3 -m pytest` to ensure no test regressions.
- Regenerate the marketplace with `python tools/rebuild_marketplace.py` and
  confirm `bash scripts/ci-preflight.sh --check` passes.

## Risks and open questions

- `rebuild_marketplace.py --phase validate --check` includes `git diff
  --exit-code`, which fails if generated surfaces are stale. This is intended, but
  it requires `python tools/rebuild_marketplace.py` before preflight can pass.
- Pre-commit now takes roughly as long as a full marketplace validation because
  it runs the entire pipeline. This is acceptable for an agent-facing gate.
- The `.ps1` script must locate `py -3` or `python` on Windows; the implementation
  will include a fallback pattern.
