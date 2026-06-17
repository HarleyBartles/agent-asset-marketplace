# Architecture Pack README Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `architecture-pack` README text so it reflects the projected first-wave triad: `cqrs-event-sourcing`, `event-driven-architecture`, and `database-design-patterns`.

**Architecture:** This is a docs-only consistency fix. Keep the scope limited to `codex-marketplace/plugins/architecture-pack/README.md` unless the live README contradicts the plugin metadata in another nearby architecture-pack surface.

**Tech Stack:** Markdown, repo validation scripts, PowerShell

---

### Task 1: Update the Architecture Pack README

**Files:**
- Modify: `codex-marketplace/plugins/architecture-pack/README.md`
- Test: `py -3 tools/validate_marketplace.py`
- Test: `py -3 tools/validate_repo_index.py`
- Test: `git diff --check`

- [ ] **Step 1: Inspect the README wording against plugin metadata and bundle manifest**

- [ ] **Step 2: Update the README to name all three first-wave projected skills**

- [ ] **Step 3: Run marketplace and repo-index validation**

Run:
```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
git diff --check
```

Expected: all commands succeed with no formatting or validation errors.

- [ ] **Step 4: Confirm only the README changed and no generated artifacts moved**

Run:
```powershell
git status --short
```

Expected: only the intended README edit plus this plan file until the work is finalized.
