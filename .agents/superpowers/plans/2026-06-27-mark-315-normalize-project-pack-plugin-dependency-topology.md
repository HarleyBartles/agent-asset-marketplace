# MARK-315: Normalize Project-Pack Plugin Dependency Topology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reshape `wild-bunch-project-pack` so it keeps only Wild Bunch native skills and thin bridge/overlay skills, while dependency plugins such as `game-studio`, `dotnet-kit`, `architecture-pack`, `frontend-pack`, `security-pack`, `api-contracts-pack`, and `repo-worker-pack` are consumed as separate install surfaces by the repo that needs them.

**Architecture:** The Wild Bunch pack should become an overlay and bridge surface, not a copy of whole plugin inventories. Keep the project-pack source of truth in the central bundle manifest, regenerate the projected plugin surfaces from repo tooling, and add a validation guard that detects when a project pack has silently absorbed an entire dependency plugin. `game-studio` stays a standalone plugin, and browser verification stays outside the Wild Bunch pack surface.

**Tech Stack:** Markdown plans, Linear, Git worktrees, PowerShell, Codex marketplace manifests, Python `py -3` generator/validator tooling, and the repository's existing projection/index/validation scripts.

## Global Constraints

- Do not begin implementation until this plan is approved.
- Keep the work to one branch and one PR.
- Start from the latest fetched `origin/main` in a fresh dedicated worktree under `.worktrees/`.
- Keep all Superpowers docs under `.agents/docs/superpowers/`; treat any `docs/superpowers/` references as stale until they are removed or repointed.
- Do not hand-edit generated marketplace artifacts, source maps, provenance maps, repo indexes, or skill zips.
- Use `py -3` for generator and validator commands.
- Do not mutate `HarleyBartles/wild-bunch` in this issue.
- Do not update `BUNCH-103` in this issue.
- Do not package or install GPT skill zips as part of this issue.
- Keep the route-state handoff durable: plan PR first, then execution only after approval and a fresh staleness check.

## Worker Route State

```text
Route status: execution-in-progress
Plan PR: https://github.com/HarleyBartles/agent-asset-marketplace/pull/171
Plan repo path: .agents/docs/superpowers/plans/2026-06-27-mark-315-normalize-project-pack-plugin-dependency-topology.md
Plan approved: yes
Plan merged to main: no
Approved plan commit: 56354c72a546a2014a42c803a2bc19522ad355e9
Last staleness check: current origin/main checked before implementation
Execution PR: https://github.com/HarleyBartles/agent-asset-marketplace/pull/171
```

## Worktree Preflight Evidence

- Worktree path: `C:\WORK\repo-workspace\agent-asset-marketplace\.worktrees\mark-315-normalize-project-pack-plugin-dependency-topology`
- Branch: `harleydbartles/mark-315-normalize-project-pack-plugin-dependency-topology`
- Starting `origin/main` SHA: `d953b4c4b2268abed784e41bb503eec2f7dab8db`
- Current status at worktree creation: clean
- Pre-existing dirty state: none

## Preflight Findings

### Current plugin inventories

- `game-studio`: `game-playtest`, `game-studio`, `game-ui-frontend`, `phaser-2d-game`, `react-three-fiber-game`, `sprite-pipeline`, `three-webgl-game`, `web-3d-asset-pipeline`, `web-game-foundations`
- `dotnet-kit`: `clean-architecture`, `ddd`, `ef-core`, `modern-csharp`, `testing`, `vertical-slice`
- `architecture-pack`: `cqrs-event-sourcing`, `database-design-patterns`, `event-driven-architecture`
- `frontend-pack`: `accessibility-audit`, `feature-sliced-design`, `interaction-design`, `react-performance-optimization`, `ux-review`, `webapp-testing`
- `security-pack`: `owasp-top-10`, `safety-guard`, `secure-coding-practices`, `security-review`, `security-testing-patterns`, `threat-modeling-techniques`
- `api-contracts-pack`: `api-design-patterns`, `openapi-specification`
- `repo-worker-pack`: `base-doctrine`, `boring-loop`, `connector-safety`, `context-safety`, `github-operations`, `linear-issue-shaping`, `repo-worker-base`, `unslop-plus`, `work-mode-router`
- `wild-bunch-project-pack`: 5 installed skills in `references/bundle-manifest.json`

### Current duplication shape in `wild-bunch-project-pack`

- Whole `game-studio` inventory is embedded in the project pack.
- Whole `dotnet-kit` inventory is embedded in the project pack.
- `architecture-pack` is partially duplicated: `database-design-patterns` and `event-driven-architecture` are embedded in the project pack, while required `cqrs-event-sourcing` still belongs in the dependency-plugin model.
- Whole `api-contracts-pack` inventory is embedded in the project pack.
- `repo-worker-pack` is partially duplicated as a baseline subset: `repo-worker-base`, `boring-loop`, `connector-safety`, and `github-operations` are embedded in the project pack, while `base-doctrine`, `context-safety`, `linear-issue-shaping`, `unslop-plus`, and `work-mode-router` remain outside that subset in the separate pack.
- `frontend-pack` overlaps only partially; the project pack also carries extra frontend/UI/QA skills beyond the current pack inventory.
- `security-pack` is nearly duplicated; the project pack appears to carry the full surface except `safety-guard`.
- browser verification stays outside the retained Wild Bunch pack surface.

### Bridge decisions

- Keep `wild-bunch-project-doctrine` as the top-level Wild Bunch project doctrine.
- Keep `wild-bunch-domain-modeling` as the domain bridge.
- Keep `wild-bunch-dotnet-architecture` as the bridge over installed .NET and architecture dependency plugins.
- Keep `wild-bunch-browser-game` as the bridge over installed `game-studio` skills.
- Keep `wild-bunch-worker-verification` as the verification bridge over repo-worker, browser, frontend, and proof expectations.
- Expand or normalize `frontend-pack` if the current Wild Bunch-only frontend/UI/QA skills truly belong in a reusable frontend dependency plugin.
- Treat any remaining `security-pack` or `api-contracts-pack` usage as explicit dependency-plugin selection, not embedded project-pack duplication.

### Final intended dependency-plugin posture for a Wild Bunch-consuming repo

- Default dependency plugins: `repo-worker-pack`, `superpowers-plus`, `wild-bunch-project-pack`, `game-studio`, `dotnet-kit`, `architecture-pack`, `frontend-pack`
- Conditional dependency plugins: `security-pack`, `api-contracts-pack`
- No embedded whole-plugin inventories inside `wild-bunch-project-pack`

## File Map

- `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`: central membership source and bridge/native classification.
- `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`: generated projection map for the final membership.
- `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`: generated provenance map for the final membership.
- `codex-marketplace/plugins/wild-bunch-project-pack/SOURCE.md`: explain the plugin-first posture and dependency-plugin separation.
- `codex-marketplace/plugins/wild-bunch-project-pack/PROJECTION.md`: explain the install surface and the bridge/dependency split.
- `codex-marketplace/plugins/wild-bunch-project-pack/README.md`: keep the marketplace-facing description aligned with the final manifest.
- `codex-marketplace/plugins/wild-bunch-project-pack/.codex-plugin/plugin.json`: keep Codex-facing metadata aligned with the final projection.
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/INDEX.md`: reflect the final projected membership.
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/**`: generated projection tree for the corrected pack membership.
- `codex-marketplace/plugins/frontend-pack/skills/INDEX.md`: expand or normalize only if the frontend/UI/QA slice belongs there.
- `codex-marketplace/plugins/frontend-pack/SOURCE.md`: document any frontend-pack normalization decision.
- `codex-marketplace/plugins/game-studio/SOURCE.md`: record the plugin-level browser verification posture if the current source-custody review still requires it.
- `tools/update_skill_artifacts.py`: use the existing deterministic update entrypoint.
- `tools/generate_marketplace.py`: regenerate marketplace manifests and plugin registries.
- `tools/generate_repo_index.py`: regenerate the repo index.
- `tools/generate_provenance_maps.py`: regenerate provenance maps.
- `tools/generate_source_maps.py`: regenerate source maps.
- `tools/validate_marketplace.py`: prove the marketplace surfaces are consistent.
- `tools/validate_repo_index.py`: prove the repo index reflects the final surfaces.
- `tools/validate_skill_zips.py`: prove the export corpus stays in sync.
- `generated/skill-zips/**`: regenerated GPT export corpus if the pack surface changes there.
- `.agents/plugins/marketplace.json`: refreshed marketplace registry if the projection changes there.
- `codex-marketplace/manifest.json`: refreshed local marketplace manifest if the projection changes there.
- `repo-index/repo-index.json`: refreshed repo index if the projection changes there.
- `.agents/docs/INDEX.md`: keep the Superpowers docs entry pointed at the `.agents/docs/superpowers/` surface.
- `.agents/docs/superpowers/INDEX.md`: keep the Superpowers docs index aligned with the relocated docs surface.
- `.agents/docs/superpowers/plans/INDEX.md`: keep the plan index current after any Superpowers-doc move.

## Tasks

### Task 1: Freeze the current contract and isolate the target surfaces

**Files:**
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/SOURCE.md`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/PROJECTION.md`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/README.md`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/.codex-plugin/plugin.json`
- Inspect: `codex-marketplace/plugins/wild-bunch-project-pack/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/game-studio/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/dotnet-kit/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/architecture-pack/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/frontend-pack/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/security-pack/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/api-contracts-pack/skills/INDEX.md`
- Inspect: `codex-marketplace/plugins/repo-worker-pack/skills/INDEX.md`
- Inspect: `sources/third_party/game-studio/upstream/skills/`

- [ ] Confirm the exact keep/remove boundary for `wild-bunch-project-pack` from the live source tree and the attached Linear brief.
- [ ] Confirm whether `frontend-pack` should absorb the current Wild Bunch-only frontend/UI/QA skills or whether those skills should be removed from the pack entirely.
- [ ] Confirm whether `game-studio` needs any plugin-level `SOURCE.md` or `PROJECTION.md` note beyond the existing browser verification posture.

### Task 2: Move the Superpowers docs surface under `.agents/docs/superpowers/`

**Files:**
- Modify: `.agents/docs/INDEX.md`
- Modify: `.agents/docs/superpowers/INDEX.md`
- Modify: `.agents/docs/superpowers/plans/INDEX.md`
- Modify: `.agents/docs/superpowers/plans/**/*.md` if any stale `docs/superpowers/` references remain in the plan corpus
- Modify: any other repo file that still points at `docs/superpowers/` instead of `.agents/docs/superpowers/`

- [x] Repoint the repo-local Superpowers docs navigation so the canonical docs home is `.agents/docs/superpowers/` and the old `docs/superpowers/` wording is treated as stale.
- [x] Update the Superpowers plan and spec indexes so they continue to enumerate the current docs corpus after the move.
- [x] Keep the plan corpus, route-state references, and docs navigation aligned with the relocated docs surface.

### Task 3: Reshape the Wild Bunch pack to native skills plus bridge skills

**Files:**
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/PROJECTION.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/README.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/skills/INDEX.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/skills/**`

- [x] Remove the whole embedded `game-studio`, `dotnet-kit`, `architecture-pack`, `api-contracts-pack`, and `repo-worker-pack` inventories from the Wild Bunch pack projection.
- [x] Keep the Wild Bunch native/bridge skills only, and keep any selected projections explicit rather than inheriting them through duplicated plugin inventories.
- [x] Normalize the pack prose so it reads as an installable bridge/overlay surface rather than a self-contained dump of other plugins.

### Task 4: Normalize dependency plugins where the issue scope requires it

**Files:**
- Modify: `codex-marketplace/plugins/frontend-pack/skills/INDEX.md`
- Modify: `codex-marketplace/plugins/frontend-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/game-studio/SOURCE.md`
- Modify: `codex-marketplace/plugins/game-studio/README.md` if the source-custody note needs to be surfaced there

- [x] Decide whether the current Wild Bunch-only frontend/UI/QA skills belong in `frontend-pack`: keep `frontend-pack` unchanged and do not absorb the Wild Bunch slice there.
- [x] Keep `game-studio` complete as its own plugin and document the browser verification decision at the plugin level only if the existing source/projection notes are not already sufficient.
- [x] Avoid moving any game-studio gap into the Wild Bunch pack as a workaround.

### Task 5: Add validation that prevents whole-plugin inventory duplication

**Files:**
- Modify: `tools/validate_marketplace.py`
- Modify: `tools/generate_marketplace.py` if the guard needs marketplace context
- Modify: `tools/update_skill_artifacts.py` if the new guard must be called from the update path
- Create: `tools/validate_project_pack_topology.py` only if the existing validation chain cannot express the required guard deterministically

- [x] Compare the project pack skill set against every active marketplace plugin inventory, and require explicit bridge/rationale metadata for any material overlap.
- [x] Fail or warn when a project pack contains 100% of another dependency plugin's skill set.
- [x] Fail or warn when a project pack contains a substantial partial dependency-plugin inventory without an explicit bridge skill and manifest rationale.
- [x] Fail or warn when a project pack is missing a required dependency-plugin skill that the bridge/dependency model says must come from the dependency plugin rather than from ad hoc projection.
- [x] Allow explicit selected-skill projection only when the manifest explains why installing the whole plugin would be excessive.
- [x] Keep the guard generic so it applies to future project packs, not just `wild-bunch-project-pack`.

### Task 6: Regenerate the marketplace and export surfaces from tooling

**Files:**
- Modify: `generated/skill-zips/wild-bunch-project-pack/**`
- Modify: `generated/skill-zips/registry.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `repo-index/repo-index.json`
- Modify: any generated `codex-marketplace/plugins/wild-bunch-project-pack/**` proof files produced by tooling

- [x] Regenerate the corrected pack through the existing deterministic pipeline instead of hand-editing downstream outputs.
- [x] Re-run the marketplace and repo-index generators after the pack shape changes.
- [x] Confirm the generated export corpus, source maps, and provenance maps all agree on the final membership.

### Task 7: Validate, publish, and record the durable route state

**Files:**
- Modify: `.agents/docs/superpowers/plans/2026-06-27-mark-315-normalize-project-pack-plugin-dependency-topology.md`
- Modify: the Linear issue route-state comment or body entry for `MARK-315`

- [x] Run the repository's marketplace and topology validation commands, plus a targeted duplicate-inventory search over the plugin `skills/INDEX.md` files.
- [x] Fully regenerate the repo-wide index mesh with `py -3 tools/generate_index_mesh.py` during execution so the Superpowers docs move and any follow-on docs/index updates are reflected across the whole mesh.
- [x] Publish the plan-only PR against `main` and keep implementation paused until the plan is approved.
- [x] Update the durable Linear route state with the plan path and plan PR once the plan PR exists.

## Validation Plan

Planned validation commands for the implementation branch after approval:

```powershell
py -3 tools/update_skill_artifacts.py --skill wild-bunch-project-pack
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/generate_index_mesh.py --check
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
git diff --check
```

Targeted topology checks:

```powershell
rg -n "^(game-playtest|game-studio|game-ui-frontend|phaser-2d-game|react-three-fiber-game|sprite-pipeline|three-webgl-game|web-3d-asset-pipeline|web-game-foundations)$" codex-marketplace\plugins\wild-bunch-project-pack\skills\INDEX.md
rg -n "^(clean-architecture|ddd|ef-core|modern-csharp|testing|vertical-slice)$" codex-marketplace\plugins\wild-bunch-project-pack\skills\INDEX.md
rg -n "^(cqrs-event-sourcing|database-design-patterns|event-driven-architecture)$" codex-marketplace\plugins\wild-bunch-project-pack\skills\INDEX.md
```

Expected result:

- the Wild Bunch pack no longer embeds whole dependency-plugin inventories
- the final pack surface is explainable as native Wild Bunch skills plus thin bridges
- `game-studio` remains a standalone plugin with browser verification handled at the plugin/source-custody boundary, not hidden inside Wild Bunch

## Self-Review

### Spec coverage

1. Inspect current source and durable issue state - Worktree Preflight Evidence, Preflight Findings
2. Separate Wild Bunch native skills from dependency plugins - Task 2
3. Normalize `frontend-pack` only if the current Wild Bunch frontend slice belongs there - Task 3
4. Keep `game-studio` complete at the plugin level and treat browser verification as a plugin/source-custody decision - Preflight Findings, Task 3
5. Add validation that blocks future whole-plugin duplication in project packs - Task 4
6. Regenerate the marketplace and export surfaces from tooling - Task 5
7. Publish the plan-only PR and durable route state before implementation - Task 6

### Placeholder scan

- No TBDs or hand-wavy paths remain in the plan.
- All conditional decisions are tied to live source inspection, not memory.

### Type consistency

- `wild-bunch-project-pack` remains the only project pack being reshaped in this issue.
- Dependency plugins remain separate install surfaces and are not treated as nested source custody.
- The plan file is the durable preflight artifact that execution must later check off and carry forward.
- The relocated Superpowers docs surface remains under `.agents/docs/superpowers/` so future route-state and plan docs stay discoverable in one repo-local home.
