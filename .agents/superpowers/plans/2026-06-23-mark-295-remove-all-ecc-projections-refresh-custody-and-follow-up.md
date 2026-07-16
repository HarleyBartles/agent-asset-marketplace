# MARK-295: Remove All ECC Projections, Refresh Custody, and Hand Off Reprojection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** remove every ECC-derived marketplace projection from every plugin, record the removals on MARK-295, refresh the retained ECC source custody, and close this issue with a follow-up issue for a clean re-projection pass.

**Architecture:** Treat this as a cleanup and custody refresh, not a rebuild. First remove all ECC projection surfaces from installable marketplace plugins and derived outputs, while preserving non-ECC projections in mixed packs. Then refresh the retained ECC upstream snapshot and provenance so the repo still has durable source custody for a future issue. Finally, write the removal ledger into Linear and hand off a follow-up reprojection issue that starts from fresh source inspection and explicit projection design.

**Tech Stack:** Markdown docs, marketplace manifests, generated skill zip registry, Python validation scripts, Linear issue comments/issue creation, PowerShell/Git.

## Global Constraints

- Do not start implementation until the revised plan is shared and approved.
- Keep the scope narrow to ECC removal, custody refresh, and follow-up handoff.
- Preserve non-ECC projections and unrelated marketplace assets.
- Do not hand-edit generated zips, generated registry data, source maps, or provenance maps when tooling owns them.
- Use `py -3` for generator and validator commands.
- Publish the resulting repo change through GitHub before claiming completion.
- Linear writes are conditional on actual worker capability: if Linear write access is available in this runtime, post the removal ledger and create the follow-up issue; if not, return paste-ready text for both and do not claim Linear was updated.
- Fresh upstream custody refresh has a hard fallback: if live upstream fetch or inspection is unavailable, do not silently reuse stale custody; report the blocker and either stop or record that the retained snapshot is unchanged with a hard reason.

---

### Task 1: Build the exact ECC removal matrix and Linear removal ledger

**Files:**
- Inspect: `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- Inspect: `codex-marketplace/plugins/superpowers-ecc/SOURCE.md`
- Inspect: `codex-marketplace/plugins/security-pack/README.md`
- Inspect: `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- Inspect: `codex-marketplace/plugins/architecture-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/data-platform-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/frontend-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/language-patterns-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/ops-connectors-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/media-content-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/*/references/bundle-manifest.json`
- Inspect: `codex-marketplace/plugins/*/references/source-map.md`
- Inspect: `codex-marketplace/plugins/*/references/provenance-map.json`
- Inspect: `generated/skill-zips/registry.json`
- Inspect: `repo-index/repo-index.json`
- Inspect: `.agents/plugins/marketplace.json`
- Inspect: `codex-marketplace/manifest.json`
- Inspect: `provenance/ecc.md`
- Inspect: `provenance/repo-worker-base.md`
- Inspect: `provenance/codex-cortex.md`
- Inspect: `provenance/architecture-pack.md`
- Inspect: `provenance/data-platform-pack.md`
- Inspect: `provenance/frontend-pack.md`
- Inspect: `provenance/language-patterns-pack.md`
- Inspect: `provenance/ops-connectors-pack.md`
- Inspect: `provenance/media-content-pack.md`
- Inspect: `provenance/security-pack.md`
- Inspect: `provenance/superpowers-ecc.md`

- [ ] **Step 1: Enumerate the current ECC-derived projection inventory**

Run the exact repo scan needed to build the removal matrix:

```powershell
rg -n '"source_family": "ecc"|source_repo: https://github.com/affaan-m/ECC|sources/third_party/ecc/upstream' codex-marketplace/plugins repo-index/repo-index.json generated/skill-zips/registry.json .agents/plugins/marketplace.json codex-marketplace/manifest.json
```

- [ ] **Step 2: Classify each affected plugin as delete-or-prune**

Build a matrix with these actions:

- delete entire plugin root if it contains only ECC projections
- prune only ECC entries if the plugin also contains non-ECC projections
- keep the non-ECC entries and regenerate the pack metadata around the remaining surface

Current observed ECC-bearing plugin families to process:

- delete entirely: `superpowers-ecc`, `ops-connectors-pack`, `media-content-pack`
- prune ECC entries only: `repo-worker-base`, `security-pack`, `codex-cortex`, `architecture-pack`, `data-platform-pack`, `frontend-pack`, `language-patterns-pack`
- recheck for any other active ECC-bearing plugin references before editing

- [ ] **Step 3: Draft the Linear removal ledger and follow-up handoff text**

Prepare the issue comment text that records:

- which skills were removed
- from which plugin pack each skill was removed
- which plugin roots were deleted entirely
- which packs were kept and pruned
- the recommended next issue title for clean reprojection

The follow-up issue should explicitly require:

- fresh source inspection
- projection reconsideration from current custody
- pack-by-pack selection decisions
- review of mixed packs before any new projection work

If Linear writes are unavailable at execution time, keep this step as paste-ready evidence only and do not claim the issue was updated remotely.

---

### Task 2: Remove ECC projections from the marketplace plugin surfaces

**Files:**
- Delete: `codex-marketplace/plugins/superpowers-ecc/`
- Modify: `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/repo-worker-base/references/source-map.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/repo-worker-base/skills/*` for ECC removals only
- Modify: `codex-marketplace/plugins/security-pack/README.md`
- Modify: `codex-marketplace/plugins/security-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/security-pack/PROJECTION.md`
- Modify: `codex-marketplace/plugins/security-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/security-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/security-pack/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/security-pack/skills/*` for ECC removals only
- Modify: `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/codex-cortex/references/source-map.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/codex-cortex/skills/*` for ECC removals only
- Modify: `codex-marketplace/plugins/architecture-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/architecture-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/architecture-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/architecture-pack/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/architecture-pack/skills/*` for ECC removals only
- Modify: `codex-marketplace/plugins/data-platform-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/data-platform-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/data-platform-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/data-platform-pack/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/data-platform-pack/skills/*` for ECC removals only
- Modify: `codex-marketplace/plugins/frontend-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/frontend-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/frontend-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/frontend-pack/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/frontend-pack/skills/*` for ECC removals only
- Modify: `codex-marketplace/plugins/language-patterns-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/language-patterns-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/language-patterns-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/language-patterns-pack/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/language-patterns-pack/skills/*` for ECC removals only
- Modify: `codex-marketplace/plugins/ops-connectors-pack/` if any residual files remain after deleting its plugin root
- Modify: `codex-marketplace/plugins/media-content-pack/` if any residual files remain after deleting its plugin root

- [ ] **Step 1: Delete the pure-ECC plugin roots**

Remove the plugin roots that become empty once ECC is removed:

- `codex-marketplace/plugins/superpowers-ecc/`
- `codex-marketplace/plugins/ops-connectors-pack/`
- `codex-marketplace/plugins/media-content-pack/`

- [ ] **Step 2: Prune ECC skill roots from the mixed packs**

Remove only the ECC-derived skill directories and matching manifest entries from the mixed packs so their non-ECC content remains installable.

Keep the non-ECC portions intact:

- `repo-worker-base` keeps `boring-loop`, `connector-safety`, and `github-operations`
- `security-pack` keeps the Claude-Cortex security trio and threat-modeling content
- `codex-cortex` keeps its Claude-Cortex source-backed projections
- `architecture-pack` keeps its Claude-Cortex architecture roots
- `data-platform-pack` keeps its non-ECC PlanetScale and other non-ECC data roots
- `frontend-pack` keeps its Claude-Cortex and feature-sliced roots
- `language-patterns-pack` keeps its Claude-Cortex roots

- [ ] **Step 3: Remove the deleted packs from the active marketplace inventory**

Update the active pack listings so the deleted pure-ECC bundles no longer appear in:

- `codex-marketplace/plugin-roots.json`
- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `repo-index/repo-index.json`

---

### Task 3: Refresh the retained ECC source custody and provenance

**Files:**
- Modify: `sources/third_party/ecc/upstream/manifest.json`
- Modify: `sources/third_party/ecc/upstream/source-custody.md`
- Modify: `sources/third_party/ecc/upstream/LICENSE` only if the upstream snapshot materially changes the retained license evidence
- Modify: `provenance/ecc.md`
- Modify: `provenance/repo-worker-base.md`
- Modify: `provenance/security-pack.md`
- Modify: `provenance/codex-cortex.md`
- Modify: `provenance/architecture-pack.md`
- Modify: `provenance/data-platform-pack.md`
- Modify: `provenance/frontend-pack.md`
- Modify: `provenance/language-patterns-pack.md`
- Modify: `provenance/ops-connectors-pack.md`
- Modify: `provenance/media-content-pack.md`
- Modify: `provenance/superpowers-ecc.md`

- [ ] **Step 1: Refresh the retained upstream snapshot**

Bring `sources/third_party/ecc/upstream` up to the fresh upstream basis required by MARK-295 and preserve the retained snapshot boundary.

If live upstream fetch or inspection is unavailable, stop here or record the current snapshot as unchanged with a hard blocker reason; do not silently continue on stale custody.

- [ ] **Step 2: Rewrite the ECC provenance record**

Update `provenance/ecc.md` so it reflects:

- the refreshed snapshot basis
- the fact that active marketplace projections are removed in this issue
- the follow-up issue needed for future reprojection

- [ ] **Step 3: Retire or rewrite pack-level provenance notes**

For packs that lose all ECC content, retire the pack note if the plugin root is deleted.

For mixed packs, rewrite the provenance notes so they only describe the remaining non-ECC projections and explicitly note that ECC content was removed in MARK-295.

---

### Task 4: Regenerate downstream outputs and add a no-active-ECC guard

**Files:**
- Modify: `tools/validate_marketplace.py`
- Modify: `tools/validate_repo_index.py` if the repo-index shape needs a guard for deleted plugin roots
- Modify: `tools/update_skill_artifacts.py` only if removal of plugin roots requires explicit pruning behavior
- Modify: `generated/skill-zips/registry.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `repo-index/repo-index.json`
- Modify: affected `generated/skill-zips/**/skill.zip` artifacts

- [ ] **Step 1: Add a guard that no active marketplace plugin still projects ECC**

Add validation that fails if any active marketplace projection still declares:

- `source_family: ecc`
- `source_repo: https://github.com/affaan-m/ECC`
- an ECC source path under `sources/third_party/ecc/upstream`

The guard should apply to active install surfaces, not to the retained source custody tree.

- [ ] **Step 2: Regenerate the derived marketplace outputs**

Run the repo tooling so deleted plugin roots disappear and pruned packs stay aligned:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/update_skill_artifacts.py --all
```

- [ ] **Step 3: Verify the regenerated registry no longer advertises ECC projections**

Check the active outputs, not the retained source custody tree:

```powershell
rg -n '"source_family": "ecc"|https://github.com/affaan-m/ECC' .agents/plugins/marketplace.json codex-marketplace/manifest.json repo-index/repo-index.json generated/skill-zips/registry.json codex-marketplace/plugins
```

---

### Task 5: Close out the issue with a Linear removal record and a follow-up issue

**Files:**
- Update: MARK-295 in Linear
- Create: follow-up Linear issue for reprojection

- [ ] **Step 1: Post the removal ledger to MARK-295**

Record in Linear:

- each removed skill
- the pack it was removed from
- whether the whole pack was deleted
- the refreshed custody basis
- the exact reason reprojection is deferred to a follow-up issue

If Linear writes are unavailable, return the removal ledger text as paste-ready evidence and do not claim MARK-295 was updated.

- [ ] **Step 2: Create the follow-up issue for reprojection**

The follow-up should require:

- fresh source inspection
- explicit projection design
- pack-by-pack selection decisions
- review of mixed packs before reintroducing any ECC content
- confirmation that the new projections are self-contained inside each installable skill root

If Linear writes are unavailable, return the follow-up issue text as paste-ready evidence and do not claim the issue was created.

- [ ] **Step 3: Final validation**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/materialize_projection.py --check
py -3 tools/validate_skill_zips.py
git diff --check
```

Expected result:

- no active ECC projections remain in marketplace install surfaces
- deleted pure-ECC plugin roots are absent from the marketplace inventory
- the retained ECC custody is refreshed and recorded
- MARK-295 has a removal ledger and a clear next-step issue

---

## Self-Review

### Spec coverage

1. Removal of all ECC projections from all plugins - Tasks 1, 2, 4
2. Linear recording of removed skills by source pack - Tasks 1, 5
3. Fresh retained ECC custody - Task 3
4. Follow-up issue for proper reprojection - Task 5
5. Preservation of non-ECC marketplace content - Task 2
6. Regenerated active outputs and guards against regression - Task 4

### Placeholder scan

- This plan intentionally defers reprojection to a follow-up issue.
- The exact fresh upstream commit is not named here because the task is to inspect and refresh from the live upstream basis during execution.

### Type consistency

- `source_family: ecc` refers only to active marketplace projection entries, not retained source custody.
- `provenance/ecc.md` becomes the canonical repo note for the refreshed custody plus the removal handoff.
- The follow-up issue is separate from MARK-295 and should be created only after the removal ledger is posted.
