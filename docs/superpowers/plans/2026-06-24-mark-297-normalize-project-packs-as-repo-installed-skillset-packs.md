# MARK-297: Normalize Project Packs as Repo-Installed Skillset Packs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the Wild Bunch project pack so Codex receives a manifest-driven, installable plugin projection from a single central pack definition, with any repo-local `.agents/skills` projection generated from the same source rather than treated as canonical.

**Architecture:** The repository already has a deterministic projection pipeline built around `references/bundle-manifest.json`, `tools/materialize_projection.py`, `tools/update_skill_artifacts.py`, `tools/generate_marketplace.py`, `tools/generate_repo_index.py`, `tools/generate_provenance_maps.py`, and `tools/generate_source_maps.py`. MARK-297 should reuse that pipeline if the new repo-skillset manifest pattern from MARK-298 lands cleanly; if it does not, the work must add deterministic generator/validator tooling and wire it into the standard pipeline rather than introducing a one-off Wild Bunch script. The Wild Bunch pack must remain plugin-first, generated from a central manifest, and must not depend on hand-rolled file copies or hard-coded membership lists. `MARK-298` is a dependency gate only; MARK-297 is the Wild Bunch normalization issue and must not drift into repo-skillset manifest implementation for other packs.

**Tech Stack:** Markdown plans, Linear issue and document contracts, Codex marketplace bundle manifests, Python `py -3` generator/validator tooling, PowerShell, Git, GitHub PR publication.

## Global Constraints

- Do not begin implementation until this plan is approved.
- Keep the work to one branch and one PR.
- Use the existing deterministic marketplace/tooling pipeline where possible; if it cannot consume the repo-skillset manifest deterministically, add deterministic tooling and register it in the standard generator/validator path.
- Do not hand-edit generated zips, marketplace manifests, repo indexes, provenance maps, source maps, or projection trees.
- Do not hard-code Wild Bunch pack membership in ad hoc scripts.
- Use `py -3` for generator and validator commands.
- Treat `MARK-298` as the manifest-pattern dependency gate for any repo-skillset manifest work.
- The repo currently has no checked-in `.agents/skills` tree at the root; if a repo-local projection is introduced, it must be generated from the same manifest/source and not become source truth.
- Preserve the plugin-first posture already documented in `docs/custody-and-projection-doctrine.md` and `codex-marketplace/README.md`.
- Update the repo guidance in the relevant `AGENTS.md` files so future workers do not reintroduce hand-edited pack files, hard-coded membership, or one-off scripts when the deterministic tooling pipeline already exists or needs to be created.
- This implementation is Wild Bunch-only. Adventures and Rooms are deferred unless source inspection proves they must be touched to support the Wild Bunch pack contract.

## Worktree Preflight Evidence

- Worktree path: `C:\WORK\codex-lanes\codex-b\worktrees\mark-297`
- Branch: `harleydbartles/mark-297-normalize-project-packs-as-repo-installed-skillset-packs`
- Starting `origin/main` SHA: `d236ac8f13578fdac074b3d85334c59b8860e03f`
- Current status: clean at worktree creation
- Repo-local `.agents/skills` tree: absent in this checkout
- Current Wild Bunch plugin source of truth: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Current deterministic projection tooling already present: `tools/materialize_projection.py`, `tools/update_skill_artifacts.py`, `tools/generate_marketplace.py`, `tools/generate_repo_index.py`, `tools/generate_provenance_maps.py`, `tools/generate_source_maps.py`, `tools/validate_marketplace.py`, `tools/validate_repo_index.py`, `tools/validate_skill_zips.py`

## Preflight Findings

### Current Wild Bunch surfaces

- Plugin wrapper: `codex-marketplace/plugins/wild-bunch-project-pack/.codex-plugin/plugin.json`
- Bundle source notes: `codex-marketplace/plugins/wild-bunch-project-pack/SOURCE.md`
- Projection notes: `codex-marketplace/plugins/wild-bunch-project-pack/PROJECTION.md`
- Current bundle manifest: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Current source map: `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`
- Current provenance map: `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`
- Current projected skills: `wild-bunch-project-doctrine`, `wild-bunch-domain-modeling`, `wild-bunch-dotnet-architecture`, `wild-bunch-browser-game`, `wild-bunch-worker-verification`, `web-game-foundations`, `phaser-2d-game`, `game-ui-frontend`, `game-playtest`, `sprite-pipeline`

### Controlling membership contract

The attached document `Implementation detail — Wild Bunch project pack plugin normalization` is the controlling keep/remove contract for this issue. If any repo file and that document disagree, the implementation must bring the repo into line with the attached contract or stop and report the discrepancy.

#### Keep

- `wild-bunch-project-doctrine`
- `wild-bunch-domain-modeling`
- `wild-bunch-dotnet-architecture`
- `wild-bunch-browser-game`
- `wild-bunch-worker-verification`
- `web-game-foundations`
- `phaser-2d-game`
- `game-ui-frontend`
- `game-playtest`
- `sprite-pipeline`
- `game-studio`
- `react-three-fiber-game`
- `three-webgl-game`
- `web-3d-asset-pipeline`
- `repo-worker-base`
- `boring-loop`
- `connector-safety`
- `github-operations`
- `crew`
- `clean-architecture`
- `ddd`
- `ef-core`
- `modern-csharp`
- `testing`
- `vertical-slice`
- `accessibility`
- `browser-qa`
- `design-system`
- `e2e-testing`
- `make-interfaces-feel-better`
- `react-patterns`
- `react-testing`
- `ux-review`
- `interaction-design`
- `webapp-testing`
- `api-design-patterns`
- `openapi-specification`
- `architecture-decision-records`
- `backend-patterns`
- `database-design-patterns`
- `event-driven-architecture`
- `hexagonal-architecture`
- `docker-patterns`
- `secure-coding-practices`
- `owasp-top-10`
- `security-review`
- `security-testing-patterns`
- `threat-modeling-techniques`

#### Remove

- `github-superpowers`
- `linear-superpowers`
- `unslop-superpowers`
- `session-buster`
- `session-buster-ingress`
- `linear-issue-compactor`
- `worker-dispatch-linear`
- `buster-framework`
- `ambiguity-buster`
- `invariant-buster`
- `crew-buster`
- `security-scan`
- `linear`

### Relevant repo-resident skills discovered

- `sources/first_party/skills/repo-worker-base/SKILL.md`
- `sources/first_party/skills/boring-loop/SKILL.md`
- `sources/first_party/skills/connector-safety/SKILL.md`
- `sources/first_party/skills/github-operations/SKILL.md`
- `sources/first_party/skills/crew/SKILL.md`

### Dependency state

- `MARK-298` is still the repo-skillset manifest-pattern dependency gate only.
- The repo already has manifest-driven marketplace projection tooling, but it does not yet prove the new repo-skillset manifest pattern that MARK-297 wants for the Wild Bunch pack.
- Because `.agents/skills` is absent in this checkout, the implementation must decide whether the first repo-local projection should create it or leave it intentionally absent and documented until MARK-298 lands.

## File Map

- `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`: own the Wild Bunch pack membership and any central manifest fields needed to drive deterministic projection.
- `codex-marketplace/plugins/wild-bunch-project-pack/SOURCE.md`: document the durable source custody and the fact that the plugin is projection-only.
- `codex-marketplace/plugins/wild-bunch-project-pack/PROJECTION.md`: document the installable plugin posture and the repo-local projection rule.
- `codex-marketplace/plugins/wild-bunch-project-pack/README.md`: describe the pack at the marketplace surface in terms of manifest-driven projection.
- `codex-marketplace/plugins/wild-bunch-project-pack/.codex-plugin/plugin.json`: keep the Codex-facing plugin metadata aligned with the manifest-driven bundle.
- `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`: regenerate from the manifest.
- `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`: regenerate from the manifest.
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/**`: regenerate the projected skill tree from the manifest, removing any excluded skills.
- `generated/skill-zips/wild-bunch-project-pack/**`: regenerate the GPT export corpus from the same projection.
- `generated/skill-zips/registry.json`: refresh the zip registry deterministically.
- `.agents/plugins/marketplace.json`: refresh the marketplace registry from the project-root inventory.
- `codex-marketplace/manifest.json`: refresh the local marketplace manifest from the project-root inventory.
- `repo-index/repo-index.json`: refresh the repo index entry for the pack.
- `docs/custody-and-projection-doctrine.md`: update only if the implementation needs a repo-wide clarification about repo-installed skillset packs and repo-local projections.
- `AGENTS.md`: add the repo-wide deterministic pipeline posture and the no-hand-edits rule for project-pack work.
- `codex-marketplace/AGENTS.md`: reinforce the projection-root no-hand-edits rule for marketplace pack work.
- `codex-marketplace/plugins/AGENTS.md`: reinforce the install-surface no-hand-edits rule for plugin roots and bundle manifests.
- `tools/AGENTS.md`: reinforce the generator/validator-only rule and the prohibition on one-off pack scripts.
- `docs/superpowers/plans/2026-06-24-mark-297-normalize-project-packs-as-repo-installed-skillset-packs.md`: this plan file, saved in the branch for review.
- `tools/materialize_projection.py`: extend only if the current bundle-manifest pipeline cannot consume the required manifest shape deterministically.
- `tools/update_skill_artifacts.py`: extend only if the pack update path needs to call a new deterministic manifest generator.
- `tools/validate_marketplace.py`: extend only if validation needs a new guard for repo-installed skillset pack determinism.
- `tools/generate_marketplace.py`, `tools/generate_repo_index.py`, `tools/generate_provenance_maps.py`, `tools/generate_source_maps.py`: use as the existing deterministic regeneration chain and adjust only if the manifest pattern requires it.
- `tools/validate_skill_zips.py`: run to confirm the generated export surface stays in sync.

## Tasks

### Task 1: Lock the manifest pattern and the repo-local projection contract

**Files:**
- Inspect: `MARK-298` and its attached implementation brief
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/PROJECTION.md`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/README.md`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/.codex-plugin/plugin.json`
- Inspect: `docs/custody-and-projection-doctrine.md`
- Inspect: `tools/materialize_projection.py`
- Inspect: `tools/update_skill_artifacts.py`
- Inspect: `tools/validate_marketplace.py`
- Inspect: `tools/generate_marketplace.py`
- Inspect: `tools/generate_repo_index.py`
- Inspect: `tools/generate_provenance_maps.py`
- Inspect: `tools/generate_source_maps.py`
- Inspect: `tools/validate_skill_zips.py`

- [ ] **Step 1: Confirm whether the existing bundle-manifest pipeline can express the repo-skillset contract without special cases**

Check whether the current `bundle-manifest.json` + `tools/materialize_projection.py` + `tools/update_skill_artifacts.py` chain can deterministically drive the Wild Bunch pack from one manifest with no hard-coded membership lists.

If it can, keep that pipeline and use it.

If it cannot, the implementation must add deterministic tooling under `tools/` and wire it into the standard generator/validator flow rather than creating a one-off script.

Expected result:

- the implementation path is deterministic
- the plan has a single source of truth for pack membership
- no hard-coded membership list is introduced in an ad hoc helper

- [ ] **Step 2: Confirm the current repo-local `.agents/skills` position**

Use the current checkout state to prove whether a repo-local `.agents/skills` projection already exists.

If it remains absent, record that the first implementation decision is whether MARK-298 should materialize it as generated output or leave it intentionally absent for this repo.

Expected result:

- the plan does not assume `.agents/skills` exists when it does not
- the repo-local projection decision is explicit before implementation begins

### Task 2: Normalize the Wild Bunch pack membership through the central manifest

**Files:**
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/PROJECTION.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/README.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`
- Modify or delete: `codex-marketplace/plugins/wild-bunch-project-pack/skills/**`

- [ ] **Step 1: Encode the keep/remove policy in the manifest, not in generated files**

Update the Wild Bunch manifest so the final membership matches the controlling membership contract above:

- keep the exact skills listed under `Keep`;
- remove the exact skills listed under `Remove`.

Expected result:

- pack membership is defined once, centrally
- generated surfaces will follow the manifest instead of carrying hidden membership logic

- [ ] **Step 2: Keep the Codex-facing bundle plugin-first**

Ensure the plugin metadata and source notes describe the bundle as an installable Codex plugin projection of the manifest, not a raw `.agents/skills` dump.

Expected result:

- `codex-marketplace/plugins/wild-bunch-project-pack` remains the install surface
- the pack reads as plugin-first in source, projection, and README text

### Task 3: Make the deterministic tooling pipeline produce the pack without hard codes

**Files:**
- Modify: `tools/materialize_projection.py` if the existing generic projection engine needs new manifest-shape support
- Modify: `tools/update_skill_artifacts.py` if the pack update path must call a new manifest-driven generator
- Modify: `tools/validate_marketplace.py` if the pack needs a new determinism guard
- Modify: `tools/generate_marketplace.py` if the active plugin inventory needs a new root or a new shape
- Modify: `tools/generate_repo_index.py` if the new pack shape changes repo-index emission
- Modify: `tools/generate_provenance_maps.py` if the new manifest shape changes provenance emission
- Modify: `tools/generate_source_maps.py` if the new manifest shape changes source-map emission
- Create: `tools/generate_repo_skillset_bundle_manifest.py` only if the current generic tooling cannot consume the required manifest deterministically
- Create: `tools/validate_repo_skillset_bundle_manifest.py` only if the current validation chain cannot prove the desired output deterministically

- [ ] **Step 1: Reuse the current generator chain if it already consumes the manifest cleanly**

Prefer the existing deterministic pipeline:

`py -3 tools/update_skill_artifacts.py`
`py -3 tools/materialize_projection.py --check`
`py -3 tools/generate_marketplace.py --check`
`py -3 tools/generate_repo_index.py --check`

If the chain already produces the Wild Bunch pack from the manifest without hard-coded membership, keep it and do not add extra tooling.

Expected result:

- the pack is generated by the existing deterministic path
- no special-case Wild Bunch script exists

- [ ] **Step 2: Add deterministic tooling only if the existing chain cannot express the manifest**

If a new repo-skillset manifest shape or a new projection rule is required, add one generic tool and one validation path that handle the shape for any repo-installed skillset pack.

The tool must:

- read the manifest;
- materialize the plugin projection;
- fail on missing or stale members;
- avoid hard-coded pack membership;
- be called by the standard update/validation entrypoints.

Expected result:

- deterministic generation remains centralized
- the implementation does not become a Wild Bunch one-off

### Task 4: Regenerate the full marketplace and export surface

**Files:**
- Modify: `generated/skill-zips/wild-bunch-project-pack/**`
- Modify: `generated/skill-zips/registry.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `repo-index/repo-index.json`
- Modify: any generated `codex-marketplace/plugins/wild-bunch-project-pack/**` proof files produced by tooling

- [ ] **Step 1: Regenerate from the manifest-driven pipeline**

Run the full deterministic chain from repo tooling rather than editing outputs directly.

Expected command family:

```powershell
py -3 tools/update_skill_artifacts.py --pack wild-bunch-project-pack
py -3 tools/generate_marketplace.py
py -3 tools/generate_repo_index.py
py -3 tools/generate_provenance_maps.py
py -3 tools/generate_source_maps.py
```

If a new deterministic generator or validator is added, include it in this chain and in the validation step below.

Expected result:

- all generated marketplace surfaces reflect the manifest
- the Wild Bunch plugin is produced deterministically
- no manual copy step is required

### Task 5: Update durable agent guidance in the repo AGENTS files

**Files:**
- Modify: `AGENTS.md`
- Modify: `codex-marketplace/AGENTS.md`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `tools/AGENTS.md`

- [ ] **Step 1: Add the deterministic tooling posture to the repo-wide guidance**

Document the rule that if the deterministic tooling pipeline does not exist, workers must create it and wire it in rather than hand-editing project-pack files or scripting a one-off shortcut.

Expected result:

- future workers see the no-hand-edits, no-hard-codes, no-one-offs rule before they touch the pack

- [ ] **Step 2: Mirror the same rule in the scoped marketplace and tooling AGENTS files**

Update the marketplace-scoped and tools-scoped AGENTS files so they reinforce the same posture for plugin-root work and generator/validator work.

Expected result:

- repo guidance stays aligned with the implementation plan
- future pack work is steered back into the deterministic pipeline instead of bespoke edits

### Task 6: Validate, search, and keep the draft PR published

**Files:**
- None beyond the generated surfaces and the plan file

- [ ] **Step 1: Run the repo validations that prove deterministic projection**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/materialize_projection.py --check
py -3 tools/validate_skill_zips.py
git diff --check
```

Then run targeted searches to confirm the final projection does not rely on hard-coded or stale surfaces.

Expected result:

- the bundle-manifest chain is still the source of truth
- generated surfaces are current
- there is no hidden manual step left in the pack flow

- [ ] **Step 2: Keep the draft PR published against `main` and wait for approval**

The plan-only PR is already open and must remain the publication surface for this preflight stage. Keep it on `main`, do not begin source changes, and wait for approval before implementation starts.

Expected result:

- the plan is visible in GitHub
- implementation remains paused behind review approval

## Self-Review

### Spec coverage

1. Read the issue and attached brief - Task 1
2. Inspect current repo surfaces and resident skills - Worktree Preflight Evidence, Preflight Findings
3. Confirm or create deterministic manifest-driven tooling - Task 1, Task 3
4. Normalize Wild Bunch membership through a central manifest - Task 2
5. Keep the plugin-first posture and optional repo-local projection explicit - Global Constraints, Task 2
6. Regenerate the marketplace and export surfaces through tooling - Task 4
7. Update the repo AGENTS guidance so future workers do not regress to hand edits or one-offs - Task 5
8. Validate and publish the plan PR before implementation - Task 6

### Placeholder scan

- No TBDs or hand-wavy file paths remain in the plan.
- Any new tooling is conditional on the observed gap in the current deterministic pipeline, not assumed up front.

### Type consistency

- `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json` remains the central membership source unless MARK-298 forces a new manifest shape.
- The repo-local `.agents/skills` projection is treated as optional generated output, not canonical source.
- The deterministic tooling path always ends in the standard marketplace and zip generators or in a generic replacement wired into that same path.
