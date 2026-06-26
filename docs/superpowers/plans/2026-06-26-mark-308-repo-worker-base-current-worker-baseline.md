# MARK-308 Repo Worker Base Current Worker Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the `repo-worker-pack` plugin so its installed projection matches the current repo-local worker baseline from MARK-305/MARK-303: `repo-worker-base`, `base-doctrine`, `work-mode-router`, `linear-issue-shaping`, `boring-loop`, `connector-safety`, `github-operations`, `unslop-plus`, and `safe-large-file-writing`.

**Architecture:** Keep `sources/first_party/skills/` as canonical source custody and treat `codex-marketplace/plugins/repo-worker-pack/` plus `generated/skill-zips/repo-worker-pack/` as derived surfaces. Use the existing first-party source files for the approved skill set, update the repo-worker-pack bundle metadata and plugin prose to describe that approved set, then regenerate the projections and skill zips through the deterministic tooling. Do not hand-edit generated outputs, and do not pull broader Superpowers+ or unrelated project packs into this bundle.

**Tech Stack:** Markdown skill sources, YAML agent prompts, JSON bundle and provenance maps, Codex marketplace projection tooling, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/generate_provenance_maps.py`, `py -3 tools/generate_source_maps.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_skill_zips.py`, `git diff --check`.

## Global Constraints

- Start from the latest `origin/main` in the fresh repo-local `.worktrees/` checkout.
- Keep the work on one branch and one PR.
- Preserve first-party verbatim source custody for every included skill.
- Keep `worker-dispatch-linear` out of active surfaces; the active worker route names are `work-mode-router` and `linear-issue-shaping`.
- Keep the bundle narrow and first-party only.
- Do not hand-edit generated zips, registry files, or projection trees.
- Use the repo-local `.agents/skills/INDEX.md` as the current baseline reference, but do not mutate the `.agents/skills/` surface in this issue unless inspection proves it is stale.

## Preflight Basis

- Worktree: `.worktrees/mark-308`
- Branch: `harleydbartles/mark-308-update-repo-worker-base-plugin-with-current-worker-baseline`
- Starting main SHA: `b205dabc139185107ce93d005510ba4b7ffa22e3`
- Repo-local worker baseline reference: `.agents/skills/INDEX.md` now lists the nine-skill worker set the plugin should mirror.
- Current plugin exposure: `codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json` now reflects the approved nine-skill worker baseline.

### Task 1: Lock the approved repo-worker baseline against current source custody

**Files:**
- Inspect: `.agents/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json`
- Inspect: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Inspect: `codex-marketplace/plugins/unslop-plus/references/bundle-manifest.json`
- Inspect: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Inspect: `sources/first_party/skills/work-mode-router/SKILL.md`
- Inspect: `sources/first_party/skills/linear-issue-shaping/SKILL.md`
- Inspect: `sources/first_party/skills/boring-loop/SKILL.md`
- Inspect: `sources/first_party/skills/connector-safety/SKILL.md`
- Inspect: `sources/first_party/skills/github-operations/SKILL.md`
- Inspect: `sources/first_party/skills/unslop-plus/SKILL.md`
- Inspect: `sources/first_party/skills/safe-large-file-writing/SKILL.md`

**Interfaces:**
- Consumes: the repo-local worker surface in `.agents/skills/INDEX.md`, the current repo-worker-pack bundle manifest, and the first-party source custody paths for the approved skills.
- Produces: a locked target inventory that explains why `work-mode-router` and `linear-issue-shaping` are included, why `unslop-plus` and `safe-large-file-writing` are included, and why broader Superpowers+ skills stay out.

- [x] **Step 1: Compare the current baseline surfaces**

Run:

```powershell
rg -n "work-mode-router|linear-issue-shaping|boring-loop|connector-safety|github-operations|unslop-plus|safe-large-file-writing|repo-worker-base|base-doctrine|repo-worker-pack|worker-dispatch-linear" .agents\skills\INDEX.md codex-marketplace\plugins\repo-worker-pack\references\bundle-manifest.json codex-marketplace\plugins\house-skills\references\bundle-manifest.json codex-marketplace\plugins\unslop-plus\references\bundle-manifest.json codex-marketplace\plugins\superpowers-plus\references\bundle-manifest.json
```

Expected: `.agents/skills/INDEX.md` shows the nine-skill worker baseline, `repo-worker-pack` mirrors that approved set, and `worker-dispatch-linear` does not appear as an active route name.

- [x] **Step 2: Confirm source custody and exclusions**

Read the first-party skill bodies for `work-mode-router`, `linear-issue-shaping`, `unslop-plus`, and `safe-large-file-writing` and confirm they are source-led, first-party, and compatible with the repo-worker baseline.

Expected: the approved set is all first-party and verbatim, while `linear-superpowers`, `github-superpowers`, `using-superpowers`, `executing-plans`, and other broader Superpowers+ route or execution skills remain out of this plugin.

- [x] **Step 3: Freeze the approved entry list**

Record the final bundle set as:

```text
  repo-worker-base
  base-doctrine
  work-mode-router
  linear-issue-shaping
  boring-loop
  connector-safety
  github-operations
  unslop-plus
  safe-large-file-writing
```

Expected: the implementer can point to a single approved inventory before touching any bundle metadata.

### Task 2: Update the repo-worker-pack source and plugin-facing bundle docs

**Files:**
- Modify: `sources/first_party/skills/repo-worker-base/SKILL.md`
- Modify: `sources/first_party/skills/repo-worker-base/agents/openai.yaml`
- Modify: `codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/repo-worker-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/README.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/PROJECTION.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/references/provenance-map.json`
- Modify: `provenance/repo-worker-pack.md`

**Interfaces:**
- Consumes: the approved entry list from Task 1 and the current repo-worker-pack source prose.
- Produces: a thin repo-worker-pack entrypoint plus bundle-facing docs that all describe the same nine-skill baseline without importing broader route doctrine.

- [x] **Step 1: Keep the source entrypoint thin while naming the approved support set**

Edit the source skill so it still acts as a compositional entrypoint, but its support list now names the approved baseline skills that belong in the plugin.

Expected: the source still routes out instead of expanding into a handbook, and it no longer reads like an eight-skill bundle.

- [x] **Step 2: Rewrite the bundle manifest as the source of truth for projection**

Update `codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json` so the `entries[]` array matches the approved inventory and the repo index section points at the right source-led paths.

Expected: the bundle manifest, source map, and provenance map all describe the same approved nine-skill set.

- [x] **Step 3: Align the plugin prose and provenance**

Update `SOURCE.md`, `README.md`, `PROJECTION.md`, and `provenance/repo-worker-pack.md` so they stop describing the old subset and instead describe the approved worker baseline.

Expected: the prose explains that `repo-worker-base` is thin, first-party only, and aligned to the current worker baseline installed in `.agents/skills/`.

- [x] **Step 4: Reconcile the skill maps**

Update `codex-marketplace/plugins/repo-worker-pack/references/source-map.md` and `codex-marketplace/plugins/repo-worker-pack/references/provenance-map.json` from the same bundle manifest change, not by hand.

Expected: the maps stay mechanically aligned with the manifest and do not invent any extra skills.

### Task 3: Regenerate the repo-worker-pack projections and export surfaces

**Files:**
- Regenerate: `codex-marketplace/plugins/repo-worker-pack/skills/**`
- Regenerate: `generated/skill-zips/repo-worker-pack/**`
- Regenerate: `generated/skill-zips/registry.json`
- Regenerate if drift appears: `codex-marketplace/manifest.json`
- Regenerate if drift appears: `.agents/plugins/marketplace.json`
- Regenerate if drift appears: `repo-index/repo-index.json`

**Interfaces:**
- Consumes: the updated repo-worker-pack source and bundle manifest from Task 2.
- Produces: refreshed plugin projections, skill zips, and registry surfaces that reflect the approved nine-skill baseline.

- [x] **Step 1: Run the deterministic repo-worker-pack regeneration**

Run:

```powershell
py -3 tools\update_skill_artifacts.py --pack repo-worker-pack
```

Expected: the repo-worker-pack projection tree and generated skill zips refresh from source custody, and the generated registry surfaces move only as needed for the new baseline.

- [x] **Step 2: Regenerate proof maps from the new manifest**

Run:

```powershell
py -3 tools\generate_provenance_maps.py
py -3 tools\generate_source_maps.py
```

Expected: the provenance and source map outputs match the updated bundle manifest without manual edits.

- [x] **Step 3: Falsify accidental drift**

Run:

```powershell
py -3 tools\validate_marketplace.py
py -3 tools\validate_repo_index.py
py -3 tools\validate_skill_zips.py
git diff --check
```

Expected: validation passes, and `worker-dispatch-linear` does not reappear as an active skill in the repo-worker-pack surfaces.

- [x] **Step 4: Verify the final skill list in the projected surfaces**

Run:

```powershell
rg -n "work-mode-router|linear-issue-shaping|boring-loop|connector-safety|github-operations|unslop-plus|safe-large-file-writing|repo-worker-base|base-doctrine|repo-worker-pack|worker-dispatch-linear" codex-marketplace\plugins\repo-worker-pack generated\skill-zips .agents\skills
```

Expected: the repo-worker-pack plugin surfaces and generated zips show the approved nine-skill baseline, and any `worker-dispatch-linear` hit is historical or absent from active surfaces.

### Task 4: Publish the plan branch and leave the implementation gate clean

**Files:**
- Commit: `docs/superpowers/plans/2026-06-26-mark-308-repo-worker-base-current-worker-baseline.md`

**Interfaces:**
- Consumes: the completed plan document and the clean preflight state.
- Produces: a committed plan-only branch and a draft PR targeting `main`.

- [x] **Step 1: Review the plan for scope and placeholder drift**

Confirm that every task names exact files or exact commands, that there are no broad placeholder steps, and that the approved baseline is still the nine-skill set from Task 1.

Expected: the plan is specific enough for implementation without additional route discovery.

- [x] **Step 2: Commit the plan**

Run:

```powershell
git add docs\superpowers\plans\2026-06-26-mark-308-repo-worker-base-current-worker-baseline.md
git commit -m "docs: add MARK-308 repo-worker-base preflight plan"
```

Expected: the branch has a single plan-only commit ready for draft PR publication.

- [x] **Step 3: Open a draft PR targeting `main`**

Create the draft PR from the committed plan branch and keep it plan-only. The plan PR is reviewed and merged first. After approval and merge, implementation starts from latest `main` in a fresh branch/PR, and the implementation worker performs a staleness check against the approved plan before changing files. Only combine plan and implementation in one PR if the issue explicitly authorizes that exception.

Expected: the plan PR exists, targets `main`, and remains a plan-only review surface until it is approved and merged.

### Task 5: Preserve the execution receipt in the implementation PR

**Files:**
- Update during execution: `docs/superpowers/plans/2026-06-26-mark-308-repo-worker-base-current-worker-baseline.md`

**Interfaces:**
- Consumes: the approved and merged plan file from Task 4, plus the implementation branch's current source state.
- Produces: an execution PR that carries both the implementation changes and the checked-off repo-resident plan file when scope remains within the approved plan.

- [x] **Step 1: Require the plan file in the execution branch**

Add the repo-resident plan file to the implementation branch and check off completed steps before publication.

Expected: the execution PR includes the plan file with completed checkboxes, so the durable receipt travels with the implementation.

- [x] **Step 2: Repair stale plans only when the drift stays in scope**

If the approved plan is stale but the drift is repairable inside the approved scope, repair the plan in the execution branch, then execute against the repaired plan.

Expected: the execution PR includes the repaired checked-off plan plus implementation, and the branch stays within the approved scope.

- [x] **Step 3: Stop when drift changes the shape materially**

If the drift changes scope materially, stop for human review instead of broadening the implementation or silently re-planning.

Expected: no implementation proceeds until the scope question is resolved explicitly.

## Self-Review

- [x] The plan names the current repo-local worker baseline from `.agents/skills/INDEX.md`.
- [x] The plan keeps the repo-worker-pack bundle narrow and first-party only.
- [x] The plan excludes `worker-dispatch-linear` from active surfaces.
- [x] The plan gives exact files and exact commands for regeneration and validation.
- [x] The plan does not rely on manual edits to generated zips or registry files.
- [x] The plan clearly separates the plan-only PR from the later implementation PR.
- [x] The plan requires the checked-off plan file to ride in the implementation PR.

## Execution Receipt

- The implementation branch now uses the canonical `tools/generate_pack_manifests.py` generator name instead of the ECC-specific script name.
- The local `.agents/skills` projection now includes `base-doctrine` alongside the repo worker baseline skills.
- The Adventures bundle no longer carries the deprecated `tps-reporting` or `tps-ingress` dependencies.
- The checked-off plan file remains part of the execution PR so the durable receipt travels with the implementation.
