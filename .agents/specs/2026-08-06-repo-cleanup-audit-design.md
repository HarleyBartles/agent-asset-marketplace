# Repo cleanup audit

## Goal

Remove stale, redundant, and split-brain repository surfaces that no longer serve active work, consolidating the tree into one docs location and one doctrine location while keeping `py -3 tools/run.py ci --check` green.

## Scope

### 1. Remove retired surface trees

- Delete `adapters/`. The overlay adaptation machinery has been retired; the tree now contains only generated indexes and a stale `__pycache__` directory.
- Delete `generated/`. The zip-export lane is retired and no tooling writes here; the directory only contains a generated `INDEX.md`.
- Delete `docs/overlay-adapter-policy.md` — the overlay machinery is retired.
- Delete `.devin/rules/adapters.md` and `.agents/doctrine/adapters.md` — retired with the `adapters/` tree.
- Re-point `.devin/rules/docs.md` and `.devin/rules/docs-contracts.md` to `.agents/docs/` and `.agents/docs/contracts/` instead of the old `docs/` tree; do **not** delete them.
- Remove `adapters` and `generated` entries from `.gitignore`.

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

- Update hard-coded references to the moved/removed paths in root `AGENTS.md`, `README.md`, `REVIEW.md`, `CONTRIBUTING.md`, `.agents/docs/AGENTS.md`, `.agents/doctrine/docs.md`, `.agents/doctrine/docs-contracts.md`, runbooks, skill sources, and repo tooling.
- Run `py -3 tools/run.py mesh --apply` to regenerate `INDEX.md` files and prune removed surfaces.
- Run `py -3 tools/run.py ci --check` for final validation.

### 5. Audit follow-up

- Delete the redundant/empty surfaces found in the cleanup audit:
  - `.agents/docs/superpowers/` (only a `.gitignore`)
  - `scripts/` (only a generated `INDEX.md`)
  - `tests/pressure/handoff-gates/` only if no prompts are recorded; in this branch prompts are recorded, so it is retained.
- Remove or rewrite active `adapters/` and `generated/` references in:
  - `.agents/docs/unslop/profile.md`
  - `.agents/doctrine/codex-marketplace.md`
  - `.agents/doctrine/codex-plugins.md`
  - `.agents/doctrine/marketplace-worker-doctrine.md`
  - `.agents/doctrine/sources.md`
  - `.agents/runbooks/code-style.md`
  - `.agents/runbooks/marketplace-generation.md`
  - `.agents/plugins/AGENTS.md`
  - `.agents/docs/AGENTS.md` and root `AGENTS.md` routing pointers to `mesh-policy.md` and `repo-runbook-policy.md` must be re-pointed to `.agents/doctrine/`
- Update `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md` to add a "Before you start" signpost requiring the orchestrator to read `references/review-state-graph.md` before dispatching any subagents or deciding which lenses apply.
- Update `tools/review_preflight.py` to tolerate placeholder/glob path references, completed historical plans/specs, and the `use_instead`/`use_with` skill metadata keys so the review preflight is clean.

### 6. Out of scope for this PR (follow-up work)

- Re-generate pressure-test results for skills that ship `tests/pressure/<skill>/prompts/` scenarios but lack `README.md`, `green.md`, or `red.md` records. This is deferred to a follow-up plan.

### 7. CI tooling

- Remove `review-preflight` from the `ci` task dependency graph in `tools/run.py`. `review-preflight` remains available as a manual/iterative-review gate but no longer blocks `ci --check`.

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

- `AGENTS.md` — `mesh-policy.md`, `repo-runbook-policy.md`, `non-repo-locations-policy.md` links must be re-pointed to `.agents/doctrine/`.
- `README.md` — `.agents/docs/mesh-policy.md` link.
- `REVIEW.md` and `CONTRIBUTING.md` — `.agents/docs/repo-runbook-policy.md` links.
- `.agents/docs/AGENTS.md` — scope from "agent doctrine, mesh policy, and other agent-facing docs" to the new docs-only scope; routing pointers to `mesh-policy.md` and `repo-runbook-policy.md` must point into `.agents/doctrine/`.
- `.agents/doctrine/docs.md` and `.agents/doctrine/docs-contracts.md` — re-scope to `.agents/docs/` and `.agents/docs/contracts/`.
- `.devin/rules/adapters.md` and `.agents/doctrine/adapters.md` — delete with `adapters/`.
- `.devin/rules/docs.md` and `.devin/rules/docs-contracts.md` — re-point to `.agents/docs/` and `.agents/docs/contracts/`, not deleted.
- `docs/skill-standards-policy.md` — remove `docs/overlay-adapter-policy.md` cross-reference before moving to `.agents/doctrine/`.
- `codex-marketplace/plugins/superpowers-plus/skills/publishing-source/SKILL.md` and `references/publishing-decisions.md` — remove `adapters/codex/` references.
- `tools/validate_agents_md.py` — `.agents/docs/mesh-policy.md` string.
- `tools/generate_repo_index.py` — hard-coded `docs/unslop/profile.md` string in the default repo index.
- `tests/pressure/README.md` — `docs/skill-standards-policy.md` reference.
- `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold_*.py`, `repo_standards.py`, `SKILL.md`, `references/repository-shape-standard.md`, `references/repository-runbook-standard.md`, `agents/openai.yaml` — `.agents/docs/repo-runbook-policy.md` references.
- `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/references/repo-doctrine.md` — `.agents/docs/mesh-policy.md` references.
- `codex-marketplace/plugins/mcp-usage-pack/references/codex-marketplace-compatibility.md` and `codex-marketplace/plugins/superpowers-plus/references/codex-marketplace-compatibility.md` — `docs/contracts/*` relative paths.
- `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/references/skill-authoring-checklist.md` and `.agents/skills/writing-skills/references/skill-authoring-checklist.md` — `docs/contracts/*` references.
- `tests/test_shared_checkout.py` — `repo_root / "adapters"` search root can remain because it already skips missing directories.
- `provenance/INDEX.md` and generated `INDEX.md` files — will refresh via `tools/run.py mesh --apply` after the manual edits.
- Completed plans and specs under `.agents/plans/completed/` and `.agents/specs/completed/` — `archive-links` will heal any moved `docs/` references during `mesh --apply`; these are historical context and are not live patterns.

## Trade-offs / risks

- This is a large rename/repath diff. The root `docs/` removal and the `.agents/docs` vs `.agents/doctrine` split will churn indexes and AGENTS.md pointers.
- If `mesh` regeneration does not fully heal references, some manual reference edits are required.
- The `overlay-adapter-policy.md` will be deleted because the overlay machinery is retired; any remaining references must be removed.
