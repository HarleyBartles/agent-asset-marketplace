# MARK-137 Codex-Plugin-First GPT Export Posture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repo advertise `Codex plugin first; generated GPT-safe skill zips second.` and capture a durable audit of the current source/export posture.

**Architecture:** Update the repo-facing posture docs first so workers read the same source-truth split before editing. Then record a provenance audit that classifies the live marketplace roots, GPT overlay modes, generated zip registry, and any repair findings against the current repo state.

**Tech Stack:** Markdown docs, provenance notes, repository validation scripts, generated skill-zip registry, Linear issue tracking.

---

### Task 1: Advertise the posture in the repo-facing docs

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `codex-marketplace/README.md`
- Modify: `gpt-overlays/README.md`

- [ ] **Step 1: Strengthen the source-truth wording**

Add explicit language that the marketplace is `Codex plugin first; generated GPT-safe skill zips second.` Make it clear that plugin roots are canonical source custody and `generated/skill-zips/` is a derived GPT export surface.

- [ ] **Step 2: Clarify overlay posture**

State that `gpt-overlays/` holds GPT-safe adaptations only, not canonical source, and that excluded entries are intentionally omitted from raw GPT exports instead of being forced through as plugin-only content.

- [ ] **Step 3: Keep the existing root inventory intact**

Do not rename the active protected roots or introduce a new source tree. The task is posture and guidance only unless the audit proves a real drift repair is required.

### Task 2: Record the repo audit in provenance

**Files:**
- Create: `provenance/MARK-137-codex-plugin-first-gpt-export-audit.md`

- [ ] **Step 1: Record the inspected surfaces**

Document the live repo surfaces inspected for this audit, including:

```text
codex-marketplace/plugin-roots.json
codex-marketplace/manifest.json
.agents/plugins/marketplace.json
gpt-overlays/manifest.json
generated/skill-zips/registry.json
provenance/house-skills.md
```

- [ ] **Step 2: Classify the current posture**

Summarize the active plugin roots, the generated export modes, the overlay/exclusion state for the `superpowers` pack, and whether any drift or repair was found.

- [ ] **Step 3: Record the consequence**

If the audit finds no mismatch, state that clearly and keep the report as durable evidence. If the audit finds drift, name the exact follow-up issue boundary instead of broadening this issue.

### Task 3: Validate the updated posture

**Files:**
- None expected if the audit finds no repair work.

- [ ] **Step 1: Run marketplace and export validation**

Run:

```bash
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_generated_drift.py
py -3 tools/validate_export_skill_zips.py
```

- [ ] **Step 2: Check the working tree diff**

Run:

```bash
git diff --check
```

- [ ] **Step 3: Publish the result**

Commit the doc and audit updates together if the repo surfaces remain aligned. If validation exposes a real drift repair, split that repair into the smallest follow-up issue that owns it.
