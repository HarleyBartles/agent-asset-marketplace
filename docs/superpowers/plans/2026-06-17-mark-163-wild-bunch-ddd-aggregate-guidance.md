# MARK-163 Wild Bunch DDD Aggregate Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Update the Wild Bunch marketplace skill guidance so DDD tactical modeling is explicit, `GameSession` is clearly the live-play Aggregate Root, and policy/coordinator-only extraction is not treated as aggregate work.

**Architecture:** Edit the paired Wild Bunch skill source files in `house-skills` and the mirrored `wild-bunch-project-pack` copies. Keep wording compact, replace route-metaphor language with DDD Aggregate Root terminology, and keep the reference notes aligned with the entrypoint guidance.

**Tech Stack:** Markdown skill source, repo search/validation scripts, marketplace skill-zip regeneration.

---

### Task 1: Update the canonical Wild Bunch skill source

**Files:**
- Modify: `codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling/SKILL.md`
- Modify: `codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling/references/domain-model.md`
- Modify: `codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture/SKILL.md`
- Modify: `codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture/references/dotnet-architecture.md`

- [x] **Step 1: Replace route-metaphor wording with DDD Aggregate Root language**

- [x] **Step 2: Make `GameSession` the explicit live-play Aggregate Root and require external live-play commands to mutate through it**

- [x] **Step 3: State that owned aggregate/component files may own cohesive state, behavior, invariants, and lifecycle transitions**

- [x] **Step 4: Explicitly reject policy/coordinator/resolver-only extraction as aggregate work**

### Task 2: Keep the project-pack mirrors consistent

**Files:**
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-domain-modeling/SKILL.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-domain-modeling/references/domain-model.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-dotnet-architecture/SKILL.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-dotnet-architecture/references/dotnet-architecture.md`

- [x] **Step 1: Mirror the canonical house-skill wording exactly where the project pack copies are projected verbatim**

- [x] **Step 2: Verify the mirrored copies stay byte-aligned with the canonical source**

### Task 3: Regenerate and verify derived marketplace artifacts

**Files:**
- Modify: `generated/skill-zips/house-skills/wild-bunch-domain-modeling/skill.zip`
- Modify: `generated/skill-zips/house-skills/wild-bunch-dotnet-architecture/skill.zip`
- Modify: `generated/skill-zips/wild-bunch-project-pack/wild-bunch-domain-modeling/skill.zip`
- Modify: `generated/skill-zips/wild-bunch-project-pack/wild-bunch-dotnet-architecture/skill.zip`
- Modify: `generated/skill-zips/registry.json`

- [x] **Step 1: Rebuild the four affected skill zips with `py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`**

- [x] **Step 2: Run marketplace validation and targeted search validation for remaining `aggregate route` text**

- [x] **Step 3: Review the diff for accidental scope drift before committing**
