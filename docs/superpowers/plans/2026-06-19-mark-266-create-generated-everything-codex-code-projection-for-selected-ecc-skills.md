# Everything Codex Code Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`[ ]`) syntax for tracking.

**Goal:** Create `everything-codex-code` as an installable marketplace projection of the already-selected ECC workflow skills that live in `superpowers-ecc`, without importing any raw upstream ECC snapshot or broadening the ECC slice.

**Architecture:** Treat `everything-codex-code` as a projection over the existing `superpowers-ecc` marketplace pack, not as new upstream custody. Keep the plugin root, bundle manifest, source map, provenance note, marketplace registry, and validator coverage in sync so the pack is installable and explicitly bounded to the ECC workflow skills already selected for `superpowers-ecc`.

**Tech Stack:** Markdown skill sources, JSON plugin metadata, project-scoped bundle manifests, marketplace generators, repo-index metadata, validator updates, PowerShell shell commands.

---

### Task 1: Lock the source basis and the projection boundary

**Files:**
- Read: `codex-marketplace/plugins/superpowers-ecc/README.md`
- Read: `codex-marketplace/plugins/superpowers-ecc/SOURCE.md`
- Read: `codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json`
- Read: `codex-marketplace/plugins/superpowers-ecc/references/source-map.md`
- Read: `provenance/superpowers-ecc.md`
- Read: `codex-marketplace/plugins/AGENTS.md`
- Read: `codex-marketplace/plugin-roots.json`
- Read: `.agents/plugins/marketplace.json`
- Read: `codex-marketplace/manifest.json`
- Read: `repo-index/repo-index.json`
- Read: `tools/generate_repo_index.py`
- Read: `tools/validate_marketplace.py`
- Read: `tools/update_skill_artifacts.py`
- Read: `tools/validate_generated_drift.py`

- [x] **Step 1: Confirm the exact ECC include set is the 14 skills already projected in `superpowers-ecc`.**

  Keep the pack boundary fixed to:
  `agent-harness-construction`, `ai-first-engineering`,
  `deployment-patterns`, `dmux-workflows`, `messages-ops`,
  `ml-adoption-playbook`, `prediction-market-oracle-research`,
  `recursive-decision-ledger`, `research-ops`, `safety-guard`,
  `search-first`, `team-agent-orchestration`, `team-builder`,
  and `token-budget-advisor`.

- [x] **Step 2: Record the source/projection decision for the new pack.**

  The record should state that `everything-codex-code` is installed from the
  existing `superpowers-ecc` marketplace projection and is not a raw mirror of
  `affaan-m/ECC`.

### Task 2: Create the `everything-codex-code` plugin root and projection metadata

**Files:**
- Create: `codex-marketplace/plugins/everything-codex-code/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/everything-codex-code/README.md`
- Create: `codex-marketplace/plugins/everything-codex-code/SOURCE.md`
- Create: `codex-marketplace/plugins/everything-codex-code/LICENSE`
- Create: `codex-marketplace/plugins/everything-codex-code/assets/icon.svg`
- Create: `codex-marketplace/plugins/everything-codex-code/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/everything-codex-code/references/source-map.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/agent-harness-construction/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/ai-first-engineering/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/deployment-patterns/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/dmux-workflows/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/messages-ops/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/ml-adoption-playbook/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/prediction-market-oracle-research/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/recursive-decision-ledger/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/research-ops/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/safety-guard/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/search-first/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/team-agent-orchestration/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/team-builder/SKILL.md`
- Create: `codex-marketplace/plugins/everything-codex-code/skills/token-budget-advisor/SKILL.md`
- Create: `provenance/everything-codex-code.md`

- [x] **Step 1: Materialize the new pack by mirroring the selected ECC skills from the existing `superpowers-ecc` projection.**

  The local skill tree should mirror the current `superpowers-ecc` files so the
  new pack is an installable projection surface, not a manual rewrite.

- [x] **Step 2: Write the new pack metadata and source map.**

  The bundle manifest and source map should make the installable-projection
  posture explicit, point at `codex-marketplace/plugins/superpowers-ecc/skills`
  as the source projection surface, and list the included skills directly.

- [x] **Step 3: Add a provenance note for the aggregate projection.**

  The provenance file should record the upstream ECC anchor, the retained
  `superpowers-ecc` projection surface that now acts as the source basis, and
  the fact that `everything-codex-code` is installable projection output.

### Task 3: Wire the new root into marketplace, generation, and validation surfaces

**Files:**
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `codex-marketplace/README.md`
- Modify: `codex-marketplace/plugins/README.md`
- Modify: `tools/validate_marketplace.py`
- Modify: `tests/test_validate_marketplace.py`
- Modify: `tools/update_skill_artifacts.py`
- Modify: `tools/validate_generated_drift.py`
- Modify: `generated/skill-zips/registry.json`
- Modify: `repo-index/repo-index.json`
- Modify: `generated/skill-zips/**`

- [x] **Step 1: Add the new plugin root to the protected marketplace inventory.**

  Update the active root lists and registry surfaces so `everything-codex-code`
  appears as a live installable root next to `superpowers-ecc`.

- [x] **Step 2: Add validator coverage for the installable aggregate projection.**

  Extend marketplace validation so the new pack is checked against its own
  bundle manifest, source map, and generated mirror rules rather than being
  treated as an unrecognized dangling root.

- [x] **Step 3: Confirm the existing generated-artifact pipeline picks up the new projection root from `plugin-roots.json` and bundle metadata.**

  The current `update_skill_artifacts.py`, marketplace generator, and repo
  index generator already recognize the new root once the active root inventory
  and bundle metadata are updated.

- [x] **Step 4: Regenerate the marketplace and repo-index outputs.**

  Refresh the marketplace manifest, repo index, and generated skill-zips
  registry through the normal tooling path so the new root is visible in the
  derived surfaces.

### Task 4: Validate, record, commit, push, and open a draft PR

**Files:**
- Create: `docs/superpowers/records/2026-06-19-mark-266-create-generated-everything-codex-code-projection-for-selected-ecc-skills.md`

- [x] **Step 1: Run the validation ladder.**

  Run:

  ```powershell
  py -3 tools/update_skill_artifacts.py --all
  py -3 tools/generate_marketplace.py
  py -3 tools/generate_repo_index.py
  py -3 tools/validate_marketplace.py
  py -3 tools/validate_repo_index.py
  py -3 tools/validate_skill_zips.py
  git diff --check
  ```

- [x] **Step 2: Write the implementation record.**

  Capture the final branch, changed files, generated-artifact explanation,
  validation results, and any remaining ambiguity about how future ECC-derived
  projections should be mirrored into `everything-codex-code`.

- [x] **Step 3: Commit, push, and open a draft PR.**

  Publish the branch to origin and open a draft PR against `main` before the
  final return.

### Non-goals

- Do not import the full upstream ECC snapshot into `everything-codex-code`.
- Do not move skills out of `superpowers-ecc`.
- Do not broaden the include set beyond the 14 ECC workflow skills already
  selected for the dedicated ECC pack.
- Do not hand-edit generated zips or registry outputs outside the normal
  tooling path.
