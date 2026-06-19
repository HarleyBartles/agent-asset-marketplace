# MARK-244 Create Superpowers ECC Pack and Compose It from Superpowers+ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`[ ]`) syntax for tracking.

**Goal:** Create a dedicated `superpowers-ecc` marketplace pack for the selected ECC Superpowers-style workflow skills, then add only a thin `ecc-superpowers` composition wrapper in `superpowers-plus` so the existing Superpowers+ projection can route to the new pack without absorbing the ECC doctrine itself.

**Architecture:** Treat `superpowers-ecc` as a separate plugin projection sourced from the retained ECC custody tree, not as a rewrite of `superpowers-plus`. Keep the ECC workflow material in the new pack, keep `superpowers-plus` broadly useful, and update the projection metadata, registry surfaces, and generated exports together so the new root is installable and the wrapper is discoverable.

**Tech Stack:** Markdown skill sources, JSON plugin metadata, provenance notes, repo index metadata, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_skill_zips.py`, `git diff --check`

---

### Task 1: Lock the ECC source basis and finalize the pack slice

**Files:**
- Read: `sources/third_party/ecc/upstream/manifest.json`
- Read: `sources/third_party/ecc/upstream/skills/agent-harness-construction/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/ai-first-engineering/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/deployment-patterns/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/dmux-workflows/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/messages-ops/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/ml-adoption-playbook/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/prediction-market-oracle-research/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/recursive-decision-ledger/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/research-ops/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/safety-guard/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/search-first/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/team-agent-orchestration/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/team-builder/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/token-budget-advisor/SKILL.md`
- Read: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Read: `codex-marketplace/plugins/superpowers-plus/PROJECTION.md`
- Read: `adaptation-overlays/superpowers-plus/using-superpowers/SKILL.md`
- Read: `codex-marketplace/plugins/AGENTS.md`
- Read: `codex-marketplace/plugin-roots.json`
- Read: `.agents/plugins/marketplace.json`
- Read: `codex-marketplace/manifest.json`
- Read: `repo-index/repo-index.json`

- [ ] **Step 1: Confirm the include set and reject the obvious non-fit rows**

  Keep the pack focused on the explicit workflow slice from MARK-244:
  `agent-harness-construction`, `ai-first-engineering`, `deployment-patterns`,
  `dmux-workflows`, `messages-ops`, `ml-adoption-playbook`,
  `prediction-market-oracle-research`, `recursive-decision-ledger`,
  `research-ops`, `safety-guard`, `search-first`,
  `team-agent-orchestration`, `team-builder`, and `token-budget-advisor`.
  Do not promote clearly unrelated ECC rows such as branding, social, media,
  or domain-specialist content that is not part of the ECC Superpowers-style
  workflow doctrine.

- [ ] **Step 2: Record the projection decision**

  Create a provenance note for the new pack that records the ECC upstream
  repository, pinned commit, retained custody root, selected include set, and
  the fact that the pack is a separate marketplace projection rather than a
  new source of truth.

### Task 2: Create the dedicated `superpowers-ecc` marketplace pack

**Files:**
- Create: `codex-marketplace/plugins/superpowers-ecc/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/superpowers-ecc/README.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/SOURCE.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/assets/icon.svg`
- Create: `codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/superpowers-ecc/references/source-map.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/agent-harness-construction/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/ai-first-engineering/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/deployment-patterns/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/dmux-workflows/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/messages-ops/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/ml-adoption-playbook/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/prediction-market-oracle-research/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/recursive-decision-ledger/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/research-ops/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/safety-guard/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/search-first/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/team-agent-orchestration/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/team-builder/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-ecc/skills/token-budget-advisor/SKILL.md`
- Create: `provenance/superpowers-ecc.md`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `repo-index/repo-index.json`

- [ ] **Step 1: Project the ECC skills into a new plugin root**

  Copy the selected ECC skill trees from
  `sources/third_party/ecc/upstream/skills/` into
  `codex-marketplace/plugins/superpowers-ecc/skills/`, preserving third-party
  provenance and only adapting text where the marketplace projection requires
  it.

- [ ] **Step 2: Write the pack metadata and source map**

  Make the new plugin read as a dedicated ECC Superpowers-style pack in
  `README.md`, `SOURCE.md`, `bundle-manifest.json`, and `source-map.md`, and
  list the included skills explicitly so the install surface is readable.

- [ ] **Step 3: Wire the new root into the marketplace inventory**

  Add `superpowers-ecc` to the active root inventory, marketplace registry,
  Codex marketplace manifest, and repo index so the plugin appears as a live
  installable root instead of a dangling source directory.

### Task 3: Add the thin `ecc-superpowers` wrapper and remove stale guidance

**Files:**
- Create: `sources/first_party/skills/ecc-superpowers/SKILL.md`
- Create: `sources/first_party/skills/ecc-superpowers/agents/openai.yaml`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/PROJECTION.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/source-map.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/agents/openai.yaml`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify only if the projection data model needs it: `gpt-overlays/manifest.json`

- [ ] **Step 1: Add the wrapper skill as the minimal Superpowers+ composition**

  Create a narrow `ecc-superpowers` skill that starts with `@using-superpowers`
  and routes ECC-workflow-shaped work to `superpowers-ecc` instead of folding
  the ECC doctrine into `superpowers-plus`.

- [ ] **Step 2: Update the Superpowers+ router and bundle docs**

  Add the new wrapper to the `using-superpowers` route list and update
  `SOURCE.md`, `PROJECTION.md`, the bundle manifest, and the source map so they
  describe `superpowers-plus` as broad and compositional while `superpowers-ecc`
  remains the dedicated ECC home.

- [ ] **Step 3: Remove or rewrite stale wrapper-ban and fork-era guidance**

  Search the touched Superpowers+ projection surfaces for language that still
  forbids a compositional wrapper or refers to a Superpowers fork as the live
  model, then replace that with the repo-local `superpowers-plus` plus
  `superpowers-ecc` composition story.

### Task 4: Regenerate, validate, record, and publish

**Files:**
- Modify: `generated/skill-zips/**`
- Modify: `generated/skill-zips/registry.json`
- Modify: `repo-index/repo-index.json`
- Create: `docs/superpowers/records/2026-06-19-mark-244-create-superpowers-ecc-pack-and-compose-it-from-superpowers.md`

- [ ] **Step 1: Regenerate the marketplace skill artifacts**

  Run:

  ```powershell
  py -3 tools/update_skill_artifacts.py --all
  ```

  Expected: the new `superpowers-ecc` install surface and the `ecc-superpowers`
  wrapper are regenerated together, along with any registry churn the new root
  requires.

- [ ] **Step 2: Validate the repo surfaces**

  Run:

  ```powershell
  py -3 tools/validate_marketplace.py
  py -3 tools/validate_repo_index.py
  py -3 tools/validate_skill_zips.py
  git diff --check
  ```

  Expected: validation passes, or any blocker is reported with the exact
  command and error text that failed.

- [ ] **Step 3: Write the implementation record**

  Capture the final branch, changed files, selected ECC include set, wrapper
  change, generated-artifact explanation, validation results, and any blockers
  in the implementation record under `docs/superpowers/records/`.

- [ ] **Step 4: Commit, push, and open the draft PR**

  Commit the scoped change set on the required branch, push it to origin, and
  open a draft PR against `main` so the publication surface is durable before
  the final return.
