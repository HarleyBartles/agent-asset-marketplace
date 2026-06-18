# Language Patterns Pack Projection Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Project the retained Claude-Cortex `typescript-advanced-patterns` skill into a new installable `language-patterns-pack` Codex plugin.

**Architecture:** Keep `codex-cortex` as retained source custody only. Create a new `language-patterns-pack` install surface with one projected skill, pack-level source/projection docs, and the matching marketplace/provenance/index surfaces. Mirror the upstream skill content verbatim unless a repo rule requires a narrow adaptation, and keep the scope limited to this one skill.

**Tech Stack:** PowerShell, JSON, Markdown, Codex marketplace plugin layout, `py -3` validation scripts, generated `skill.zip` artifacts.

---

### Task 1: Add retained source custody for `typescript-advanced-patterns`

**Files:**
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/SKILL.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/advanced-generics.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/branded-types.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/builder-pattern.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/common-pitfalls.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/conditional-types.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/decorators.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/discriminated-unions.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/mapped-types.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/performance-best-practices.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/template-literal-types.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/testing-types.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/type-guards.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/type-inference.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/utility-types.md`

- [ ] **Step 1: Copy the upstream skill snapshot into retained custody**

Use the upstream Claude-Cortex skill contents as the canonical source snapshot for the new retained custody tree.

- [ ] **Step 2: Verify the retained snapshot inventory**

Run:

```powershell
Get-ChildItem sources\third_party\codex-cortex\upstream\skills\typescript-advanced-patterns -Recurse -File | Select-Object FullName
```

Expected: one `SKILL.md` plus 14 reference files, with no extra outputs or generated artifacts.

### Task 2: Create the `language-patterns-pack` install surface

**Files:**
- Create: `codex-marketplace/plugins/language-patterns-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/language-patterns-pack/README.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/SOURCE.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/LICENSE`
- Create: `codex-marketplace/plugins/language-patterns-pack/assets/icon.svg`
- Create: `codex-marketplace/plugins/language-patterns-pack/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/language-patterns-pack/references/source-map.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/SKILL.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/advanced-generics.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/branded-types.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/builder-pattern.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/common-pitfalls.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/conditional-types.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/decorators.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/discriminated-unions.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/mapped-types.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/performance-best-practices.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/template-literal-types.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/testing-types.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/type-guards.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/type-inference.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/references/utility-types.md`

- [ ] **Step 1: Scaffold the plugin root**

Create the plugin manifest, README, source note, license, asset, and references folder.

- [ ] **Step 2: Project the skill tree**

Mirror the upstream `typescript-advanced-patterns` skill folder into `codex-marketplace/plugins/language-patterns-pack/skills/`.

- [ ] **Step 3: Record the pack boundary**

Document that the pack owns language/runtime guidance only and does not pull in React, CQRS, database, security, or frontend architecture doctrine.

### Task 3: Update marketplace inventories and derived indexes

**Files:**
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `codex-marketplace/README.md`
- Modify: `codex-marketplace/plugins/README.md`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `repo-index/repo-index.json`
- Modify: `provenance/codex-cortex.md`

- [ ] **Step 1: Add the new root to the active inventory**

Insert `language-patterns-pack` into the protected root list in the inventory and regenerate the marketplace registry/manifest pair.

- [ ] **Step 2: Add repo-index coverage**

Update the repo index to include the new pack with the source/provenance/bundle paths that match the new plugin root.

- [ ] **Step 3: Refresh provenance references**

Record the new retained source custody and the new projected install pack in the Codex Cortex provenance note.

### Task 4: Regenerate and validate generated skill zips

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Create: `generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`

- [ ] **Step 1: Regenerate the targeted skill zip**

Run:

```powershell
py -3 tools/update_skill_artifacts.py --skill language-patterns-pack/typescript-advanced-patterns
```

- [ ] **Step 2: Validate the marketplace and repo index**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
git diff --check
```

- [ ] **Step 3: Confirm the generated artifact surface**

Verify `generated/skill-zips/registry.json` includes only the new `language-patterns-pack/typescript-advanced-patterns` artifact for this issue slice and no unrelated generated drift.
