# Frontend Pack Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the first `frontend-pack` projection slice by packaging the retained browser UI, shared browser-game architecture, React-hosted 3D, and frontend QA guidance into an installable Codex marketplace pack, while explicitly deferring the exact candidate names that are not present in retained source.

**Architecture:** Keep the pack narrow and source-backed. Project the reusable frontend guidance that already exists in retained `game-studio` custody, use it as the new `frontend-pack` install surface, and document the exact issue-named candidates as deferred when no retained source file exists for them. Preserve source custody, pack documentation, bundle inventory, generated skill zips, and repo registries as separate surfaces.

**Tech Stack:** PowerShell, Git, repo Python tooling (`py -3`), Markdown, JSON, Codex marketplace plugin layout, retained `game-studio` source custody.

---

### Task 1: Record the source-fit decision for `frontend-pack`

**Files:**
- Create: `provenance/frontend-pack.md`
- Create: `codex-marketplace/plugins/frontend-pack/SOURCE.md`
- Create: `codex-marketplace/plugins/frontend-pack/references/source-map.md`

- [ ] **Step 1: Capture the retained source basis**

Use the retained `game-studio` source snapshot as the only source basis for this slice:

- `sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-ui-frontend/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/react-three-fiber-game/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-playtest/SKILL.md`
- `sources/third_party/game-studio/upstream/references/frontend-prompts.md`
- `sources/third_party/game-studio/upstream/references/playtest-checklist.md`

Record that the issue-named candidates `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, and `webapp-testing` were searched for in live repo source and were not present as retained source files in this checkout, so they are deferred rather than invented.

- [ ] **Step 2: Write the pack custody note**

Document the include/defer split in `provenance/frontend-pack.md` and the pack `SOURCE.md`. Keep the note concrete:

```markdown
## Source basis

This pack projects retained `game-studio` frontend-adjacent guidance into `frontend-pack`.

## Included

- `web-game-foundations`
- `game-ui-frontend`
- `react-three-fiber-game`
- `game-playtest`

## Deferred

- `react-performance-optimization`
- `accessibility-audit`
- `ux-review`
- `interaction-design`
- `webapp-testing`

These exact candidates are not present in the retained source snapshot in this checkout, so they are deferred until a real source file is available.
```

- [ ] **Step 3: Verify the live source search result**

Run:

```powershell
rg -n "react-performance-optimization|accessibility-audit|ux-review|interaction-design|webapp-testing" sources codex-marketplace generated provenance docs
```

Expected: no retained source file for those exact candidate names is found in this checkout, confirming the defer decision.

### Task 2: Project the retained frontend slice into `frontend-pack`

**Files:**
- Create: `codex-marketplace/plugins/frontend-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/frontend-pack/README.md`
- Create: `codex-marketplace/plugins/frontend-pack/LICENSE`
- Create: `codex-marketplace/plugins/frontend-pack/assets/icon.svg`
- Create: `codex-marketplace/plugins/frontend-pack/skills/web-game-foundations/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/web-game-foundations/agents/openai.yaml`
- Create: `codex-marketplace/plugins/frontend-pack/skills/game-ui-frontend/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/game-ui-frontend/agents/openai.yaml`
- Create: `codex-marketplace/plugins/frontend-pack/skills/react-three-fiber-game/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/react-three-fiber-game/agents/openai.yaml`
- Create: `codex-marketplace/plugins/frontend-pack/skills/game-playtest/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/game-playtest/agents/openai.yaml`
- Create: `codex-marketplace/plugins/frontend-pack/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/frontend-pack/references/source-map.md`

- [ ] **Step 1: Project the skill bodies and references**

Copy the retained `game-studio` skill bodies into the new pack, preserving the source content and normalizing only the projection path roots so they resolve under `frontend-pack/skills/...`:

- `web-game-foundations`
- `game-ui-frontend`
- `react-three-fiber-game`
- `game-playtest`

Keep the shared reference links inside the projected skills pointed at pack-relative paths where the skill spec requires it.

- [ ] **Step 2: Add the pack wrapper files**

Write the new pack `plugin.json`, README, LICENSE, and icon so the pack is installable and has a clear boundary:

- UI/front-end implementation guidance
- React-hosted 3D frontend integration
- frontend/browser QA and playtest guidance

The README and source map must mention the deferred exact candidate names from Task 1 so the pack does not silently imply that those source files were imported.

- [ ] **Step 3: Verify the projected tree**

Run:

```powershell
Get-ChildItem codex-marketplace\plugins\frontend-pack\skills | Select-Object Name
```

Expected: `web-game-foundations`, `game-ui-frontend`, `react-three-fiber-game`, and `game-playtest` are present under the new `frontend-pack` projection.

### Task 3: Regenerate install artifacts, validate, and publish

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Create or update: `generated/skill-zips/frontend-pack/web-game-foundations/skill.zip`
- Create or update: `generated/skill-zips/frontend-pack/game-ui-frontend/skill.zip`
- Create or update: `generated/skill-zips/frontend-pack/react-three-fiber-game/skill.zip`
- Create or update: `generated/skill-zips/frontend-pack/game-playtest/skill.zip`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `repo-index/repo-index.json`
- Create: `docs/superpowers/records/2026-06-18-mark-214-frontend-pack.md`

- [ ] **Step 1: Regenerate the skill zips**

Run:

```powershell
py -3 tools/update_skill_artifacts.py --all
```

Expected: the generator updates the new `frontend-pack` zip archives and the registry entries for the projected skills.

- [ ] **Step 2: Run validation**

Run:

```powershell
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
py -3 tools/validate_generated_drift.py --base origin/main
git diff --check
py -3 tools/validate_marketplace.py
```

Expected: repo index, zip validation, drift validation, and diff checks pass; if marketplace validation reports unrelated known drift, capture it without widening scope.

- [ ] **Step 3: Create the implementation record, commit, push, and open a draft PR**

Write the implementation record with the final branch, changed files, included skills, deferred candidates, validation results, and any blockers. Then publish the branch and open a draft PR against `main` using the required branch:

`harleydbartles/mark-214-project-frontend-first-wave-skills-into-frontend-pack`

Expected: the branch is committed, pushed, and represented by a draft PR URL for publication evidence.
