# Connector Safety Upstream Discovery Fallback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Teach `connector-safety` to step back to a connector-observed parent discovery surface when a read, write, or readback blocks, then move forward again through bounded discovery, exact read, bounded mutation, and readback.

**Architecture:** Update the canonical House Skills source first, then mirror the same content into the Adventures projection copy so the shared marketplace bundle stays consistent. Regenerate the affected skill zips and registry entries with the repo's targeted skill-update tool, then validate the generated artifact surface and drift rules against `origin/main`.

**Tech Stack:** Markdown skill sources, repo marketplace generators, `py -3 tools/update_skill_artifacts.py`, generated skill-zip registry validation.

---

### Task 1: Update the canonical skill source

**Files:**
- Modify: `codex-marketplace/plugins/house-skills/skills/connector-safety/SKILL.md`
- Modify: `codex-marketplace/plugins/adventures-pack/skills/connector-safety/SKILL.md`
- Modify: `codex-marketplace/plugins/house-skills/skills/connector-safety/CHANGELOG.md`
- Modify: `codex-marketplace/plugins/adventures-pack/skills/connector-safety/CHANGELOG.md`

- [x] **Step 1: Add an upstream discovery fallback rule near the retry posture section**

```md
## Upstream discovery fallback

When a read, write, or readback is blocked even though a likely stable identifier is known, do not keep retrying the same target-level call. Step back to the nearest parent discovery surface that can prove the target exists in the current connector state.

Use the connector-observed chain:
parent discovery -> bounded target discovery -> exact target read -> one bounded mutation -> readback.

If post-mutation readback blocks, step back to the same parent discovery chain used before the mutation, then re-read the target from that chain.
```

- [x] **Step 2: Preserve the existing discovery-before-mutation, post-create read-chain, and retry guidance**

```md
Keep the existing discover -> read -> write -> verify posture intact and sharpen the retry ladder so blocked target reads, bounded discovery, and readback failures step back to a parent surface such as team, project, repository, folder, workspace, branch, or owner.
```

- [x] **Step 3: Mirror the same text into the Adventures projection copy**

```md
Keep the House Skills and Adventures `connector-safety` skill text identical so the shared projection stays aligned with the canonical source.
```

### Task 2: Regenerate the affected skill artifacts

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/house-skills/connector-safety/skill.zip`
- Modify: `generated/skill-zips/adventures-pack/connector-safety/skill.zip`

- [x] **Step 1: Regenerate the targeted artifacts**

```powershell
py -3 tools/update_skill_artifacts.py --skill house-skills/connector-safety
py -3 tools/update_skill_artifacts.py --skill adventures-pack/connector-safety
```

- [x] **Step 2: Verify the registry and drift checks**

```powershell
py -3 tools/update_skill_artifacts.py --check
py -3 tools/validate_marketplace.py
```

- [x] **Step 3: Confirm the generated zips match the updated source**

```powershell
git diff --check HEAD~1 HEAD
```
