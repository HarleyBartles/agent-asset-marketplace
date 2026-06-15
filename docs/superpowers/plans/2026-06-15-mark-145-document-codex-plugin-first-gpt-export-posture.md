# Document Codex-plugin-first GPT export posture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repo guidance layer state the Codex-plugin-first / generated-GPT-export posture plainly before workers edit plugin, skill, overlay, or generated zip surfaces.

**Architecture:** Update the highest-read README and AGENTS surfaces first, then mirror the same posture into the plugin and overlay entrypoints that workers will naturally open next. Keep the wording consistent with the existing marketplace/projection model so the docs clarify source custody, install surface, and GPT export handling without introducing new policy.

**Tech Stack:** Markdown, repo guidance docs, marketplace manifests.

---

### Task 1: Update repo-root guidance

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Add the failing wording gap to the root guidance**

```md
Codex plugin first; generated GPT-safe skill zips second.
```

- [ ] **Step 2: Add the policy in the repo-root docs**

Use wording that says plugin roots are the canonical marketplace install surface, and generated `skill.zip` artifacts are GPT-ready derivatives, not canonical source.

- [ ] **Step 3: Verify the new wording appears in both files**

Run: `rg -n "Codex plugin first|generated GPT-safe skill zips|plugin roots are the canonical" README.md AGENTS.md`
Expected: matches in both files.

### Task 2: Update marketplace and overlay entrypoints

**Files:**
- Modify: `codex-marketplace/README.md`
- Modify: `codex-marketplace/AGENTS.md`
- Modify: `codex-marketplace/plugins/README.md`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `gpt-overlays/README.md`
- Modify: `gpt-overlays/AGENTS.md`

- [ ] **Step 1: Add the posture to the marketplace and overlay guidance**

```md
Codex plugin first; generated GPT-safe skill zips second.
```

- [ ] **Step 2: Keep each surface aligned to its role**

State that marketplace plugin roots are canonical, `generated/skill-zips/` is the GPT-ready export corpus, and `gpt-overlays/manifest.json` controls direct, overlay, and excluded GPT exports.

- [ ] **Step 3: Verify the wording is present in the targeted docs**

Run: `rg -n "Codex plugin first|generated GPT-safe skill zips|gpt-overlays/manifest.json|generated/skill-zips" codex-marketplace gpt-overlays`
Expected: matches in the updated docs.

### Task 3: Validate documentation-only changes

**Files:**
- None

- [ ] **Step 1: Run the marketplace validator**

Run: `py -3 tools/validate_marketplace.py`
Expected: pass with no new marketplace warnings or errors.

- [ ] **Step 2: Check the diff for accidental formatting issues**

Run: `git diff --check HEAD~1 HEAD`
Expected: no whitespace or patch-format errors.

- [ ] **Step 3: Commit after validation**

Run: `git status --short`
Expected: only the intended documentation files and this plan file are modified before commit.
