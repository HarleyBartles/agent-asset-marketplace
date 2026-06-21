# Superpowers+ v6.0.3 Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `superpowers-plus` to retained upstream `obra/superpowers` `v6.0.3`, then remove only the Marketplace plan-checking text that upstream now covers and regenerate the affected marketplace outputs.

**Architecture:** Keep upstream custody, marketplace projection, and Codex-specific overlays as separate layers. First retain the upstream snapshot and update the source/provenance ledgers, then regenerate the projected plugin and only narrow local adaptations where the inspected upstream `v6.0.3` source clearly covers them. Treat generated zips and indexes as derived outputs only.

**Tech Stack:** PowerShell, `git`, `py -3`, repo generator scripts under `tools/`, Codex marketplace bundle manifests, provenance maps, and skill projection materializers.

---

## Global Constraints

- Keep scope limited to `superpowers-plus` and its directly affected generated outputs.
- Preserve the retained `v5.1.0` snapshot.
- Do not hand-edit generated projections or zips; use repo tooling.
- Do not remove Marketplace-specific publication or instruction-precedence behavior unless the inspected `v6.0.3` source makes it redundant.
- Distinguish observed upstream evidence from inference in the implementation note / PR body.

### Task 1: Retain upstream `v6.0.3` source custody

**Files:**
- Create: `sources/third_party/superpowers/obra-superpowers/v6.0.3/**`
- Modify: `sources/third_party/superpowers/obra-superpowers/v6.0.3/AGENTS.md`
- Modify: `sources/third_party/superpowers/obra-superpowers/v6.0.3/LICENSE`
- Modify: `sources/third_party/superpowers/obra-superpowers/v6.0.3/README.md`
- Modify: `sources/third_party/superpowers/obra-superpowers/v6.0.3/RELEASE-NOTES.md`

- [ ] **Step 1: Mirror the upstream tag into third-party custody**

Use the real upstream tag/commit as the source of truth:

```powershell
git -C C:/Users/hbart/.codex/worktrees/33f9/_superpowers_v603 rev-parse HEAD
git ls-remote --tags https://github.com/obra/superpowers refs/tags/v6.0.3 refs/tags/v6.0.3^{}
```

Copy the full `v6.0.3` tree into `sources/third_party/superpowers/obra-superpowers/v6.0.3/`, keeping the upstream file set intact and preserving the license and release notes.

- [ ] **Step 2: Verify custody contents**

Run:

```powershell
Test-Path sources/third_party/superpowers/obra-superpowers/v6.0.3/LICENSE
Test-Path sources/third_party/superpowers/obra-superpowers/v6.0.3/README.md
Test-Path sources/third_party/superpowers/obra-superpowers/v6.0.3/RELEASE-NOTES.md
Test-Path sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/subagent-driven-development/SKILL.md
```

Expected: all return `True`.

- [ ] **Step 3: Record the upstream anchor for later provenance updates**

Capture the resolved commit `45c3cc5b66cfc5f147a7ddcfb86f7650e47a8ae0` and the tag object evidence in the PR notes and later manifest edits.

### Task 2: Update bundle, provenance, and source-map surfaces

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/source-map.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/PROJECTION.md`
- Modify: `provenance/superpowers-plus.md`
- Modify: `repo-index/repo-index.json` if the source ledger entries or versioned paths change

- [ ] **Step 1: Point all source-ledger fields at `v6.0.3`**

Update `bundle_version`, `canonical_source_root`, `source_tag`, `source_commit`, upstream tag/commit references, and any source-ledger entries that still cite `v5.1.0`.

- [ ] **Step 2: Add a compact plan/progress diff note**

Document the upstream behavior shift as observed evidence, not inference:

```text
Observed upstream evidence:
- `subagent-driven-development` now uses a progress ledger under `.superpowers/sdd/`, writes task briefs and review packages as files, and resumes from the ledger after compaction or interruption.
- `subagent-driven-development` now pre-flights the plan for conflicts before Task 1, uses a single task-reviewer prompt, and ends with a whole-branch review.
- `writing-plans` now defines task right-sizing and global constraints.
- `executing-plans` now points to subagent-capable platforms and creates todos for plan items.
- `using-git-worktrees` now prefers project-local worktrees and no longer relies on the old global worktree directory.

Inference:
- The upstream `v6.0.3` flow reduces the need for local plan-checking backstops that duplicate progress-ledger and resume behavior, but Marketplace-specific verification and publication gates remain separate.
```

- [ ] **Step 3: Keep retained-source references consistent**

Ensure the docs still point to the new retained snapshot path and the unchanged `v5.1.0` tree remains referenced only as historical custody.

### Task 3: Regenerate the projected Superpowers+ skill surfaces and narrow only redundant local text

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/**`
- Modify: `adapters/codex/superpowers-plus/using-superpowers/**`
- Modify: `adapters/codex/superpowers-plus/finishing-a-development-branch/**` if the regenerated projection still needs a narrow overlay update
- Modify: `adapters/codex/superpowers-plus/verification-before-completion/**` only if the upstream comparison proves a local line is now redundant

- [ ] **Step 1: Materialize the updated projection from the new source custody**

Run:

```powershell
py -3 tools/materialize_projection.py --plugin superpowers-plus
```

Then inspect the diff to confirm the projected upstream skills now reflect `v6.0.3`.

- [ ] **Step 2: Remove or narrow only duplicated plan-checking wording**

If the regenerated projection still carries local plan-checking text that the inspected upstream `v6.0.3` source already covers, shrink it instead of duplicating upstream doctrine. Keep the Marketplace-only behavior intact:

- system / developer / repo precedence in `using-superpowers`
- publication gate and PR readiness rules in `finishing-a-development-branch`
- plan/evidence reconciliation backstop in `verification-before-completion`

- [ ] **Step 3: Verify the retained overlays still match the source diff**

Check the overlay-backed skills against the upstream comparison so any remaining local text has a source-backed reason to exist.

### Task 4: Regenerate derived outputs and validate

**Files:**
- Modify: `generated/skill-zips/**`
- Modify: `codex-marketplace/plugins/**/references/*.json` as needed by the generators
- Modify: `repo-index/repo-index.json`
- Modify: `.agents/plugins/marketplace.json` if the marketplace generator updates it

- [ ] **Step 1: Regenerate the derived artifacts with repo tooling**

Run the current generator stack:

```powershell
py -3 tools/update_skill_artifacts.py --all
py -3 tools/generate_source_maps.py
py -3 tools/generate_provenance_maps.py
py -3 tools/generate_repo_index.py
py -3 tools/generate_marketplace.py
```

- [ ] **Step 2: Run the required validation ladder**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/materialize_projection.py --check
py -3 tools/validate_generated_drift.py
py -3 tools/update_skill_artifacts.py --check
git diff --check HEAD~1 HEAD
```

If any generator or validator command differs in the current repo, use the actual supported replacement and record it in the PR body.

- [ ] **Step 3: Commit, push, and open a draft PR**

Publish the branch with the implementation note included in the PR body, then return the PR URL, branch name, changed files by lane, validation results, and any remaining blockers.

