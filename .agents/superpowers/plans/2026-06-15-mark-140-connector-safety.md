# Connector Safety Discover-Read-Write Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Update the vendored `connector-safety` skill so side-effecting connector work follows a mandatory discover -> read -> write -> verify protocol without weakening the existing safety doctrine.

**Architecture:** Edit the canonical House Skills source first, then mirror the same content into the Adventures projection copy so the shared marketplace bundle stays consistent. Regenerate the affected skill zips and registry entries with the repo's targeted skill-update tool, then validate the generated artifact surface and drift rules against `origin/main`.

**Tech Stack:** Markdown skill sources, repo marketplace generators, `py -3 tools/update_skill_artifacts.py`, generated skill-zip registry validation.

---

### Task 1: Update the canonical skill source

**Files:**
- Modify: `codex-marketplace/plugins/house-skills/skills/connector-safety/SKILL.md`
- Modify: `codex-marketplace/plugins/adventures-pack/skills/connector-safety/SKILL.md`

- [x] **Step 1: Add the discover-before-mutation rule near the top**

```md
## Discovery-before-mutation rule

For side-effecting connector work, use the connector itself to discover the narrowest safe mutation target before writing.

Default sequence:

1. Discover the bounded surface with read-only calls.
   * Find the team, project, repository, folder, calendar, draft, issue, PR, document, or parent object using the narrowest available filters.
   * Prefer exact slugs, keys, IDs, team filters, project filters, owner filters, and limits.
   * Do not jump from session memory or chat knowledge straight to a write when a connector read can cheaply confirm the target.
2. Read the target object using the discovered stable identifier.
3. Write one bounded mutation using the discovered identifier.
4. Verify after writing.
```

- [x] **Step 2: Preserve the existing safety doctrine**

```md
Do not remove or weaken:

- blocked mutation is not proof of success;
- planned mutation is not authorization;
- one side effect per call;
- narrow payloads;
- exact-state guards for high-risk writes;
- invalid-attempt distinction;
- blocked-write report shape;
- stop signs.
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
