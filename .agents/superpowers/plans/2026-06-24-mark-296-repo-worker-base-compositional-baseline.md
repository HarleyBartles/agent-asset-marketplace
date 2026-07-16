# Repo Worker Base Compositional Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `repo-worker-base` as a thin compositional entrypoint for repo-backed workers, delegating baseline coordination to `boring-loop`, `connector-safety`, `github-operations`, and only the retained `search-first` complement if source inspection proves that skill still belongs in the baseline bundle instead of carrying hand-rolled Git/GitHub/process doctrine.

**Architecture:** Keep the editable source of truth in `sources/first_party/skills/repo-worker-base/`. Update the source skill and its prompt overlay first, then refresh the repo-worker-base plugin prose and metadata so the marketplace copy describes the skill as a compositional router rather than a standalone handbook. Treat all plugin trees, zips, manifests, and repo index entries as derived outputs produced by the regeneration tooling.

**Tech Stack:** Markdown skill sources, YAML prompt overlays, Codex marketplace plugin metadata, generated bundle manifests, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/generate_marketplace.py`, `py -3 tools/generate_repo_index.py`, `py -3 tools/materialize_projection.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_skill_zips.py`, `py -3 tools/validate_generated_drift.py`, `git diff --check`.

## Global Constraints

- Start from the current `origin/main` in the fresh repo-local worktree and keep the work on one branch and one PR.
- Keep scope limited to the repo-worker-base source, its directly shared projections, and the generated surfaces those files drive.
- Do not hand-edit generated zips, registry files, or projection trees.
- Preserve first-party source custody in `sources/first_party/skills/`.
- Do not assume `search-first` belongs in the baseline bundle unless source inspection proves retained custody and baseline fit.
- Keep generated/plugin/zips/registry surfaces derivative only.
- This plan is intentionally open until the draft PR is approved.

---

## Preflight Basis

- Worktree and branch: a fresh repo-local `.worktrees/` checkout on `harleydbartles/mark-296-normalize-repo-worker-base-into-a-compositional-baseline`.
- Starting main SHA: `77d92ff2...` from current `origin/main` at worktree creation.
- Cleanliness at plan time: the branch worktree was clean after the plan commit, and only the plan file changed there.
- Source seam: `sources/first_party/skills/repo-worker-base/SKILL.md` is the source-of-truth entrypoint; `codex-marketplace/plugins/repo-worker-base/**` and `generated/skill-zips/**` are downstream surfaces only.
- Current exposure: the repo-worker-base plugin currently exposes `boring-loop`, `connector-safety`, `github-operations`, `repo-worker-base`, and `search-first`, with additional shared projections visible in `house-skills` and `wild-bunch-project-pack`.
- Baseline inventory rule: keep only generic repo-worker baseline skills in the plugin after rechecking each current entry; any non-baseline skill must be justified by source custody and fit, not by historical presence.
- Composition model: the entrypoint stays thin and routes outward to `boring-loop`, `connector-safety`, `github-operations`, and any retained `search-first` only if the source inspection confirms it is still the right baseline complement.
- Generated surfaces: plugin projections, skill zips, registry entries, marketplace manifests, repo index entries, and proof maps remain derived outputs regenerated from source custody.
- Validation baseline: the plan must match the current deterministic generator path, not older one-off checks.

### Task 1: Rewrite the repo-worker-base source as a compositional entrypoint

**Files:**
- Modify: `sources/first_party/skills/repo-worker-base/SKILL.md`
- Modify: `sources/first_party/skills/repo-worker-base/agents/openai.yaml`

**Interfaces:**
- Consumes: the current `repo-worker-base` skill text, the existing first-party support skills `boring-loop`, `connector-safety`, `github-operations`, and the retained `search-first` skill only if inspection confirms it is still in-scope.
- Produces: a short entrypoint that tells workers what to invoke first, what to route to each support skill, and which short Harley-specific invariants remain in scope.

- [ ] **Step 1: Replace the handbook-style intro with a compositional router intro**

Rewrite the frontmatter description and opening paragraphs so the skill reads as a thin entrypoint for repo-backed work, not as the primary home for long Git/GitHub/process doctrine.

- [ ] **Step 2: Keep only the short repo-worker invariants**

Retain the direct instructions for fresh current `origin/main`, dedicated worktree isolation, no hand-edited generated artifacts, validation evidence, branch and PR proof, and GREEN / AMBER / RED / BLOCKED return posture.

- [ ] **Step 3: Route the support cases explicitly**

Make the body point workers to `boring-loop` for queue discipline, `connector-safety` for blocked or sensitive connector writes, `github-operations` for publication and merge evidence, and `search-first` only if source inspection still justifies it as the retained research-before-code complement.

- [ ] **Step 4: Remove duplicated doctrine**

Delete or collapse any paragraphs that re-state the same branch, publication, or validation law that belongs in the support skills, so the skill body stays thin and compositional.

- [ ] **Step 5: Update the prompt overlay**

Update `agents/openai.yaml` so the visible prompt says the skill is a compositional repo-worker base and does not advertise the old handbook-style behavior.

- [ ] **Step 6: Read the result against the support skills**

Compare the rewritten source to `boring-loop`, `connector-safety`, and `github-operations` to confirm the routing is complementary and not contradictory.

### Task 2: Align the repo-worker-base plugin prose and metadata

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-base/package.json`
- Modify: `codex-marketplace/plugins/repo-worker-base/README.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/PROJECTION.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/repo-worker-base/references/source-map.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/references/provenance-map.json`
- Modify: `provenance/repo-worker-base.md`

**Interfaces:**
- Consumes: the rewritten source skill from Task 1 and the current plugin inventory rooted at `codex-marketplace/plugins/repo-worker-base/`.
- Produces: plugin-facing prose and metadata that explain the bundle as a thin compositional baseline with a retained research complement, while keeping the actual inventory narrow and stable.

- [ ] **Step 1: Update the package and plugin-facing descriptions**

Reword the package metadata and README so the bundle description matches the new compositional entrypoint and no longer reads like a standalone worker handbook.

- [ ] **Step 2: Reword the source and projection notes**

Update `SOURCE.md` and `PROJECTION.md` so they describe the baseline support set, the conditional `search-first` complement decision, and the boundary that keeps generated zips and registry entries derivative.

- [ ] **Step 3: Refresh the bundle inventory notes**

Adjust `references/bundle-manifest.json` note text, then regenerate `source-map.md` and `provenance-map.json` from that manifest so the derived maps still match the bundle posture.

- [ ] **Step 4: Update provenance**

Rewrite `provenance/repo-worker-base.md` so the provenance note reflects the compositional baseline posture and the current first-party source custody path.

- [ ] **Step 5: Sanity-check the bundle scope**

Confirm the inventory still matches the intended baseline set, that `search-first` is either justified by custody and fit or explicitly re-homed/deferred, and that no new skill family is being introduced without a separate source-custody decision.

### Task 3: Regenerate shared projections and validate the final surfaces

**Files:**
- Regenerate: `codex-marketplace/plugins/repo-worker-base/**`
- Regenerate: `codex-marketplace/plugins/house-skills/skills/repo-worker-base/**`
- Regenerate: `codex-marketplace/plugins/wild-bunch-project-pack/skills/repo-worker-base/**`
- Regenerate: `generated/skill-zips/repo-worker-base/**`
- Regenerate: `generated/skill-zips/house-skills/repo-worker-base/**`
- Regenerate: `generated/skill-zips/wild-bunch-project-pack/repo-worker-base/**`
- Regenerate: `generated/skill-zips/registry.json`
- Regenerate if drift appears: `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`, `repo-index/repo-index.json`

**Interfaces:**
- Consumes: the edited source and plugin metadata from Tasks 1 and 2.
- Produces: refreshed marketplace projections, zips, and registry/index evidence that can be checked back against the source files and the issue contract.

- [ ] **Step 1: Run the deterministic refresh**

Run: `py -3 tools/update_skill_artifacts.py --all`

Expected: the deterministic generator refreshes the affected marketplace projections, zips, and registry data from source custody. Only the repo-worker-base shared surfaces should move if the edit stays localized.

- [ ] **Step 2: Run the current check path for the deterministic refresh**

Run: `py -3 tools/update_skill_artifacts.py --check`

Expected: the generated surfaces remain aligned after the full-regeneration pass.

- [ ] **Step 3: Check the repo-level manifests without writing**

Run:

```text
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/generate_mega_packs.py --check
py -3 tools/generate_provenance_maps.py --check
py -3 tools/generate_source_maps.py --check
```

Expected: all checks report no drift.

- [ ] **Step 4: Run the validation ladder**

Run:

```text
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
py -3 tools/materialize_projection.py --check
py -3 tools/validate_generated_drift.py --base origin/main
git diff --check
```

Expected: all commands pass and the diff stays limited to the intended source, projection, and derived metadata changes.

- [ ] **Step 5: Verify the publication surface**

Confirm the branch can be published as the same PR that carries the plan, then continue implementation on that branch after approval instead of opening a second PR unless later inspection proves the work needs to split.
