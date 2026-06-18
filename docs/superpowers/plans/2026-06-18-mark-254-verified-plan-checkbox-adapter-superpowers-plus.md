# Verified Plan Checkbox Adapter in Superpowers+ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Teach the shipped Superpowers+ workflow skills to treat plans as live execution artifacts with verified checkbox updates and a final verification backstop.

**Architecture:** Keep the change inside the `superpowers-plus` projection layer and GPT overlay layer. Update the four core workflow skills so the plan adapter is explicit end to end: `using-superpowers` routes plan-shaped work through the verified-plan path, `writing-plans` requires checkable evidence-backed steps, `executing-plans` requires live checkbox updates as steps complete, and `verification-before-completion` enforces checkbox/evidence consistency before completion claims. Regenerate the affected skill zips and registry instead of hand-editing generated outputs.

**Tech Stack:** Markdown, YAML, JSON, PowerShell, repository Python validators, skill artifact generation.

---

### Task 1: Update the projection-layer adapter wording

**Files:**
- Modify: `adaptation-overlays/superpowers-plus/using-superpowers/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/SKILL.md`
- Modify: `gpt-overlays/superpowers-plus/using-superpowers/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Modify: `gpt-overlays/superpowers-plus/writing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/SKILL.md`
- Modify: `gpt-overlays/superpowers-plus/executing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/SKILL.md`

- [ ] **Step 1: Rewrite the `using-superpowers` projection and GPT overlay so plan-shaped work explicitly routes through `writing-plans -> executing-plans -> verification-before-completion` as the verified-plan adapter path, while keeping routing inside `superpowers-plus`.**
- [ ] **Step 2: Rewrite `writing-plans` in the projection and GPT overlay so executable plans require checkable steps with named evidence, and intentionally open steps stay unchecked with an explanation.**
- [ ] **Step 3: Rewrite `executing-plans` in the projection and GPT overlay so each completed step is checked off only after the named evidence is collected, and unfinished or blocked steps stay open.**
- [ ] **Step 4: Rewrite `verification-before-completion` in the projection so final completion claims require rereading the plan, checking checkbox/evidence consistency, and running the final validation ladder.**

### Task 2: Refresh the generated `superpowers-plus` artifacts

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/superpowers-plus/*`

- [ ] **Step 1: Reconcile the marketplace projection from source custody plus overlays and regenerate the affected `superpowers-plus` skill zips.**
- [ ] **Step 2: Validate the refreshed generated registry against the on-disk artifacts and confirm the updated skills are the only changed `superpowers-plus` export surfaces.**

### Task 3: Publish the worker result

**Files:**
- Create or modify: any commit / branch / PR publication state required by GitHub

- [ ] **Step 1: Run the repo validation ladder: `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_skill_zips.py`, and `git diff --check`.**
- [ ] **Step 2: Commit, push `harleydbartles/mark-254-implement-verified-plan-checkbox-adapter-in-superpowers`, and open a draft PR.**

### Non-goals

- Do not change source custody under `sources/third_party/superpowers/obra-superpowers/v5.1.0/`.
- Do not route any plan traffic outside the `superpowers-plus` projection.
- Do not add a universal blocker for every unchecked plan file.
