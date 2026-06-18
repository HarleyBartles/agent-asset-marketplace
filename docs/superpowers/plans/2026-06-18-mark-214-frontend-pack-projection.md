# Frontend Pack Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair `frontend-pack` so it projects the exact MARK-214 first-wave frontend skills from retained upstream custody, and keep the pack boundary strictly frontend rather than browser-game.

**Architecture:** Keep the pack narrow and source-backed. Project the reusable frontend guidance that exists in retained `NickCrew/claude-cortex` custody, use it as the new `frontend-pack` install surface, and exclude game-studio/browser-game assets from this boundary. Preserve source custody, pack documentation, bundle inventory, generated skill zips, and repo registries as separate surfaces.

**Tech Stack:** PowerShell, Git, repo Python tooling (`py -3`), Markdown, JSON, Codex marketplace plugin layout, retained `NickCrew/claude-cortex` source custody.

---

### Task 1: Record the source-fit decision for `frontend-pack`

**Files:**
- Create: `provenance/frontend-pack.md`
- Create: `codex-marketplace/plugins/frontend-pack/SOURCE.md`
- Create: `codex-marketplace/plugins/frontend-pack/references/source-map.md`

- [ ] **Step 1: Capture the retained source basis**

Use the retained `NickCrew/claude-cortex` source snapshot as the source basis for this slice:

- `sources/third_party/claude-cortex/upstream/skills/react-performance-optimization/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/accessibility-audit/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/ux-review/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/interaction-design/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/webapp-testing/SKILL.md`

Record the exact upstream commit used and the retained source paths for each imported skill.

- [ ] **Step 2: Write the pack custody note**

Document the include split in `provenance/frontend-pack.md` and the pack `SOURCE.md`. Keep the note concrete:

```markdown
## Source basis

This pack projects retained `NickCrew/claude-cortex` frontend guidance into `frontend-pack`.

## Included

- `react-performance-optimization`
- `accessibility-audit`
- `ux-review`
- `interaction-design`
- `webapp-testing`
```

- [ ] **Step 3: Verify the live source search result**

Run:

```powershell
rg -n "react-performance-optimization|accessibility-audit|ux-review|interaction-design|webapp-testing" sources codex-marketplace generated provenance docs
```

Expected: the retained `claude-cortex` source snapshot is found and provides the exact five requested frontend candidates.

### Task 2: Project the retained frontend slice into `frontend-pack`

**Files:**
- Create: `codex-marketplace/plugins/frontend-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/frontend-pack/README.md`
- Create: `codex-marketplace/plugins/frontend-pack/LICENSE`
- Create: `codex-marketplace/plugins/frontend-pack/assets/icon.svg`
- Create: `codex-marketplace/plugins/frontend-pack/skills/react-performance-optimization/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/react-performance-optimization/validation/rubric.yaml`
- Create: `codex-marketplace/plugins/frontend-pack/skills/accessibility-audit/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/ux-review/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/interaction-design/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/interaction-design/references/state-patterns.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/SKILL.md`
- Create: `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/LICENSE.txt`
- Create: `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/scripts/with_server.py`
- Create: `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/examples/static_html_automation.py`
- Create: `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/examples/element_discovery.py`
- Create: `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/examples/console_logging.py`
- Create: `codex-marketplace/plugins/frontend-pack/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/frontend-pack/references/source-map.md`

- [ ] **Step 1: Project the skill bodies and references**

Copy the retained `claude-cortex` skill bodies into the new pack, preserving the source content and normalizing only the projection path roots so they resolve under `frontend-pack/skills/...`:

- `react-performance-optimization`
- `accessibility-audit`
- `ux-review`
- `interaction-design`
- `webapp-testing`

- [ ] **Step 2: Add the pack wrapper files**

Write the new pack `plugin.json`, README, LICENSE, and icon so the pack is installable and has a clear boundary:

- React/frontend application performance guidance
- accessibility review guidance
- UX review guidance
- interaction design guidance
- browser/webapp testing guidance

- [ ] **Step 3: Verify the projected tree**

Run:

```powershell
Get-ChildItem codex-marketplace\plugins\frontend-pack\skills | Select-Object Name
```

Expected: the five imported frontend skills are present under the new `frontend-pack` projection and no game-studio skills remain.

### Task 3: Regenerate install artifacts, validate, and publish

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Create or update: `generated/skill-zips/frontend-pack/react-performance-optimization/skill.zip`
- Create or update: `generated/skill-zips/frontend-pack/accessibility-audit/skill.zip`
- Create or update: `generated/skill-zips/frontend-pack/ux-review/skill.zip`
- Create or update: `generated/skill-zips/frontend-pack/interaction-design/skill.zip`
- Create or update: `generated/skill-zips/frontend-pack/webapp-testing/skill.zip`
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

Expected: the generator updates the new `frontend-pack` zip archives and the registry entries for the projected frontend skills.

- [ ] **Step 2: Run validation**

Run:

```powershell
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
py -3 tools/validate_generated_drift.py --base origin/main --full-regeneration
git diff --check
py -3 tools/validate_marketplace.py
```

Expected: repo index, zip validation, drift validation, diff checks, and marketplace validation all pass after the superpowers byte drift repair.

- [ ] **Step 3: Create the implementation record, commit, push, and open a draft PR**

Write the implementation record with the final branch, changed files, included skills, removed game-studio skills, validation results, and any blockers. Then publish the branch and keep the draft PR against `main` on the required branch:

`harleydbartles/mark-214-project-frontend-first-wave-skills-into-frontend-pack`

Expected: the branch is committed, pushed, and represented by a draft PR URL for publication evidence.
