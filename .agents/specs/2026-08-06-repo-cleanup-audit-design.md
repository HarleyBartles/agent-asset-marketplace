# Repo cleanup audit

## Goal

Remove stale, redundant, and split-brain repository surfaces that no longer serve active work, consolidating the tree into one docs location and one doctrine location while keeping `py -3 tools/run.py ci --check` green.

## Scope

### 1. Remove retired surface trees

- Delete `adapters/`. The overlay adaptation machinery has been retired; the tree now contains only generated indexes and a stale `__pycache__` directory.
- Delete `generated/`. The zip-export lane is retired and no tooling writes here; the directory only contains a generated `INDEX.md`.

### 2. Consolidate docs and doctrine

- `.agents/docs/` becomes the single docs home:
  - `unslop/profile.md` (repo-specific anti-slop profile)
  - `contracts/openai-agent-yaml.md`
  - `contracts/skill-frontmatter.md`
- `.agents/doctrine/` becomes the single doctrine home:
  - `mesh-policy.md` (moved from `.agents/docs/`)
  - `repo-runbook-policy.md` (moved from `.agents/docs/`)
  - `repo-local-plugin-marketplace.md` (moved from `.agents/docs/`)
  - `marketplace-worker-doctrine.md` (moved from `.agents/docs/`)
  - `project-gate-over-plugin-flattening.md` (moved from `.agents/docs/`)
  - `custody-and-marketplace-doctrine.md` (moved from `docs/`)
  - `non-repo-locations-policy.md` (moved from `docs/`)
  - `skill-standards-policy.md` (moved from `docs/`)
  - delete `docs/overlay-adapter-policy.md` — the overlay machinery is retired
- Delete the root `docs/` tree after its remaining children are moved to `.agents/docs/` or `.agents/doctrine/`.

### 3. Rehome and prune provenance

- Delete historical closeout/audit markdown records in `provenance/` that duplicate git history:
  - `2026-08-01-agents-md-migration-audit.md`
  - `2026-08-04-mark-skill-authoring-retired.md`
  - `2026-08-04-report-hygiene-retired.md`
  - `2026-08-04-review-branch-diff-retired.md`
- Create `tests/pressure/using-playwright-mcp/` and move the pressure-test evidence there:
  - `provenance/using-playwright-mcp-pressure-test-proof.md` → `tests/pressure/using-playwright-mcp/README.md`
  - `provenance/pressure-test-red.md` → `tests/pressure/using-playwright-mcp/red.md`
  - `provenance/pressure-test-green.md` → `tests/pressure/using-playwright-mcp/green.md`

### 4. Reference refresh and validation

- Update hard-coded references to the moved/removed paths.
- Delete `.devin/rules/adapters.md` and `.agents/doctrine/adapters.md`.
- Remove `adapters` and `generated` entries from `.gitignore`.
- Run `py -3 tools/run.py mesh --apply` to regenerate `INDEX.md` files and prune removed surfaces.
- Run `py -3 tools/run.py ci --check` for final validation.

## Non-goals

- No changes to upstream source custody in `provenance/` (`afpse-*.md`, pack provenance files) without separate review.
- No changes to active `codex-marketplace/plugins/` skill content other than path reference updates.
- No new marketplace packs or skills.

## Validation

- `py -3 tools/run.py ci --check` passes.
- `py -3 tools/run.py ci --apply` regenerates indexes and derived surfaces cleanly.
- No broken internal markdown links after archive-link healing.
- A draft PR is opened with branch name and head SHA.

## Reference-bearing surfaces to update

The following files carry hard-coded references to the moved or removed surfaces and must be edited manually (the mesh generator cannot rewrite prose inside AGENTS.md or skills):

- `AGENTS.md` — `mesh-policy.md`, `repo-runbook-policy.md`, `non-repo-locations-policy.md` links.
- `README.md` — `.agents/doctrine/mesh-policy.md` link.
- `REVIEW.md` and `CONTRIBUTING.md` — `.agents/doctrine/repo-runbook-policy.md` links.
- `.agents/docs/AGENTS.md` — scope from "agent doctrine, mesh policy, and other agent-facing docs" to the new docs-only scope.
- `.agents/doctrine/docs.md` and `.agents/doctrine/docs-contracts.md` — re-scope to `.agents/docs/` and `.agents/docs/contracts/`.
- `.agents/doctrine/adapters.md` and `.devin/rules/adapters.md` — delete with `adapters/`.
- `.devin/rules/docs.md` and `.devin/rules/docs-contracts.md` — delete (no more `docs/` surface to trigger).
- `.agents/doctrine/skill-standards-policy.md` — remove `docs/overlay-adapter-policy.md` cross-reference before moving to `.agents/doctrine/`.
- `codex-marketplace/plugins/superpowers-plus/skills/publishing-source/SKILL.md` and `references/publishing-decisions.md` — remove `adapters/codex/` references.
- `tools/validate_agents_md.py` — `.agents/doctrine/mesh-policy.md` string.
- `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold_*.py`, `repo_standards.py`, `SKILL.md`, `references/repository-shape-standard.md`, `references/repository-runbook-standard.md`, `agents/openai.yaml` — `.agents/doctrine/repo-runbook-policy.md` references.
- `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/references/repo-doctrine.md` — `.agents/doctrine/mesh-policy.md` references.
- `codex-marketplace/plugins/mcp-usage-pack/references/codex-marketplace-compatibility.md` and `codex-marketplace/plugins/superpowers-plus/references/codex-marketplace-compatibility.md` — `.agents/docs/contracts/*` relative paths.
- `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/references/skill-authoring-checklist.md` and `.agents/skills/writing-skills/references/skill-authoring-checklist.md` — `.agents/docs/contracts/*` references.
- `tests/test_shared_checkout.py` — `repo_root / "adapters"` search root can remain because it already skips missing directories.
- `provenance/INDEX.md` and generated `INDEX.md` files — will refresh via `tools/run.py mesh --apply` after the manual edits.

## Trade-offs / risks

- This is a large rename/repath diff. The root `docs/` removal and the `.agents/docs` vs `.agents/doctrine` split will churn indexes and AGENTS.md pointers.
- If `mesh` regeneration does not fully heal references, some manual reference edits are required.
- The `overlay-adapter-policy.md` will be deleted because the overlay machinery is retired; any remaining references must be removed.
