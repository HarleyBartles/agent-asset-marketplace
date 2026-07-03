# MARK-324 Trim Superpowers+ to Core Plus Environment Inspection Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire the router-only `*-superpowers` wrappers from first-party custody, trim `superpowers-plus` so it keeps core Superpowers plus `/inspecting-the-environment`, and refresh every derived marketplace surface that depends on that bundle shape.

**Architecture:** Treat this as a source-custody trim plus projection reconciliation. First confirm the current wrapper source, bundle manifest, and adapted `using-superpowers` overlay. Then remove the router-only wrappers, update the overlay so it no longer names removed wrapper skills, and regenerate the first-party and marketplace projections so `house-skills` and `superpowers-plus` stay aligned with the new source custody shape. Keep `using-superpowers` itself and `/inspecting-the-environment` in the bundle.

**Tech Stack:** Markdown skill source, bundle manifests, source/provenance maps, projection overlays, generated skill zips, Python regeneration scripts, Linear route-state updates, Git/GitHub publication.

## Global Constraints

- Keep scope to the router-only `*-superpowers` wrappers, `using-superpowers`, `inspecting-the-environment`, and the downstream surfaces they affect.
- Do not broaden into unrelated specialist skills or unrelated marketplace plugins.
- Do not hand-edit generated projection trees, source maps, provenance maps, registry files, or skill zips.
- If source custody is retired, regenerate `sources/first_party/skills/INDEX.md`, `codex-marketplace/plugins/house-skills`, `codex-marketplace/plugins/superpowers-plus`, and the generated skill-zips surfaces from the updated source state.
- Use `py -3` for rebuild and check gates.
- Stop at the plan-only boundary until the plan is reviewed and approved.

## Worker route state

```text
Route status: preflight-needed
Plan PR: none
Plan repo path: .agents/docs/superpowers/plans/2026-07-03-mark-324-trim-superpowers-plus-to-core-plus-environment-inspection.md
Plan approved: no
Plan merged to main: no
Approved plan commit: none
Last staleness check: none
Execution PR: none
```

---

### Task 1: Confirm the current active source and projection surfaces

**Files:**
- Read: `sources/first_party/skills/architecture-superpowers/SKILL.md`
- Read: `sources/first_party/skills/github-superpowers/SKILL.md`
- Read: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Read: `sources/first_party/skills/unslop-superpowers/SKILL.md`
- Read: `sources/first_party/skills/inspecting-the-environment/SKILL.md`
- Read: `sources/first_party/skills/INDEX.md`
- Read: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Read: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Read: `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- Read: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Read: `codex-marketplace/plugins/superpowers-plus/README.md`
- Read: `codex-marketplace/plugins/superpowers-plus/PROJECTION.md`
- Read: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Read: `codex-marketplace/plugins/superpowers-plus/references/source-map.md`
- Read: `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- Read: `adapters/codex/superpowers-plus/using-superpowers/overlay.yaml`

- [ ] **Step 1: Verify the four wrapper skills are still thin routing shells**

Confirm that `architecture-superpowers`, `github-superpowers`, `linear-superpowers`, and `unslop-superpowers` only exist to route to other skills or workflow gates, and record whether they should be retired from first-party custody or only dropped from `superpowers-plus`.

- [ ] **Step 2: Confirm the retained `superpowers-plus` core**

Verify that the bundle still needs the upstream Superpowers core set plus `/inspecting-the-environment`, and that `using-superpowers` is the only remaining adapted wrapper that should survive the trim.

- [ ] **Step 3: Capture the exact dependency surfaces**

Record the downstream files that will need regeneration if the wrappers are retired from first-party custody, including `house-skills`, `superpowers-plus`, the generated skill zips, and the repo-wide index/registry surfaces.

### Task 2: Retire the router-only wrappers and trim the `using-superpowers` overlay

**Files:**
- Delete or retire: `sources/first_party/skills/architecture-superpowers/`
- Delete or retire: `sources/first_party/skills/github-superpowers/`
- Delete or retire: `sources/first_party/skills/linear-superpowers/`
- Delete or retire: `sources/first_party/skills/unslop-superpowers/`
- Modify: `sources/first_party/skills/INDEX.md`
- Modify: `sources/first_party/skills/house-skills/SKILL.md` if the house-skills source index or router wording needs to drop the retired wrappers
- Modify: `adapters/codex/superpowers-plus/using-superpowers/overlay.yaml`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/SKILL.md`

**Interfaces:**
- Consumes: the current wrapper source bodies, the adapted `using-superpowers` overlay, and the first-party source index.
- Produces: a trimmed source-custody shape where the wrapper-only routers are gone or clearly retired, and the adapted `using-superpowers` overlay no longer names removed wrapper skills.

- [ ] **Step 1: Remove the wrapper-only source folders if source inspection still classifies them as pure routers**

Delete the four `*-superpowers` wrapper source folders only if the live source inspection confirms they are thin routing shells with no independent skill payload.

- [ ] **Step 2: Rewrite the adapted `using-superpowers` overlay**

Remove the overlay lines that route to `linear-superpowers`, `github-superpowers`, `unslop-superpowers`, and any other removed wrapper skills. Keep the upstream `using-superpowers` body intact and keep `/inspecting-the-environment` as the only remembered extra if the source still needs an adapted branch.

- [ ] **Step 3: Update the first-party skill index and any local custody notes**

Regenerate the first-party skill index and any source notes that enumerate active first-party skills so they no longer advertise retired wrapper-only source custody.

### Task 3: Regenerate the `house-skills` and `superpowers-plus` projections

**Files:**
- Regenerated: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Regenerated: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/**`
- Regenerated: `codex-marketplace/plugins/house-skills/README.md`
- Regenerated: `codex-marketplace/plugins/house-skills/PROJECTION.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/INDEX.md`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/skills/**`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/README.md`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/PROJECTION.md`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/skills/INDEX.md`
- Regenerated: `generated/skill-zips/house-skills/**`
- Regenerated: `generated/skill-zips/superpowers-plus/**`
- Regenerated: `generated/skill-zips/registry.json`
- Regenerated: `codex-marketplace/manifest.json`
- Regenerated: `.agents/plugins/marketplace.json`
- Regenerated: `repo-index/repo-index.json`

**Interfaces:**
- Consumes: the retired wrapper source state and the revised `using-superpowers` overlay.
- Produces: aligned first-party and marketplace projections with the trimmed `superpowers-plus` shape and no stale wrapper-only router surfaces.

- [ ] **Step 1: Regenerate the first-party and marketplace bundles**

Run the repo tooling that updates the bundle manifests, source/provenance maps, projected skills, and generated skill zips from source custody.

- [ ] **Step 2: Confirm the active `superpowers-plus` contents**

Verify that `superpowers-plus` keeps the upstream Superpowers core plus `/inspecting-the-environment`, and that the removed wrapper-only skills no longer appear in the active bundle inventory.

- [ ] **Step 3: Confirm the `house-skills` spillover is consistent**

If the wrapper source folders were retired, verify that `house-skills` also dropped the retired wrapper entries and that no stale source-map or provenance entries remain.

### Task 4: Validate the trim, publish the plan, and update Linear route state

**Files:**
- Validate: `sources/first_party/skills/INDEX.md`
- Validate: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Validate: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Validate: `generated/skill-zips/registry.json`
- Validate: `codex-marketplace/manifest.json`
- Validate: `.agents/plugins/marketplace.json`
- Update: `MARK-324` in Linear

**Interfaces:**
- Consumes: the regenerated projections and the trimmed source custody.
- Produces: validation evidence, a plan-only publication surface, and a Linear route-state update that points at the plan file and PR.

- [ ] **Step 1: Run the full marketplace rebuild and check gates**

Run the repo's current full regeneration and validation path, then run the non-mutating check gate so the plan-ready tree is provably fresh before publication.

- [ ] **Step 2: Search for stale wrapper references**

Run a targeted stale-reference search for `architecture-superpowers`, `github-superpowers`, `linear-superpowers`, and `unslop-superpowers` across active source, marketplace, generated registry, and index surfaces.

- [ ] **Step 3: Publish the plan-only PR and update Linear**

Commit the plan and the regenerated indexes, open the plan-only PR, then update `MARK-324` with the route-state block, plan path, PR URL, and preflight status. Stop before implementation until approval arrives.

## Validation

- `py -3 tools/rebuild_marketplace.py`
- `py -3 tools/check_marketplace.py`
- `py -3 tools/generate_index_mesh.py --check`
- `rg -n "architecture-superpowers|github-superpowers|linear-superpowers|unslop-superpowers" sources/first_party/skills codex-marketplace/plugins generated/skill-zips .agents/plugins repo-index`
- `git diff --check`

## Return Contract

When this plan is executed, return:

- the exact source folders retired or retained;
- the wrapper-only overlay lines removed from `using-superpowers`;
- the regenerated bundle and registry surfaces;
- the validation output;
- the Linear route-state update;
- the PR URL and head SHA for the plan-only publication surface.
