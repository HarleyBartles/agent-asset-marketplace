# MARK-178 Inventory Marketplace Skill References Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Inventory skill references in Codex marketplace source, classify each reference by its canonical plugin-qualified target, and publish the evidence in a durable receipt record without changing source references or generated artifacts.

**Architecture:** Use live repository inspection as the source of truth. First verify the repo schema that defines plugin names and skill names, then search marketplace source surfaces for inter-skill references, then write a durable markdown receipt with a classification table and ambiguity notes. Keep the work strictly read-mostly: no source rewrites, no generated zip mutation, and no normalization beyond classification.

**Tech Stack:** Markdown records, PowerShell/ripgrep search, git diff inspection, Linear issue context, repo documentation surfaces.

---

### Task 1: Verify the marketplace schema and search surfaces

**Files:**
- Read: `codex-marketplace/manifest.json`
- Read: `codex-marketplace/plugin-roots.json`
- Read: `codex-marketplace/plugins/*/.codex-plugin/plugin.json`
- Read: representative skill frontmatter under `codex-marketplace/plugins/*/skills/*/SKILL.md`
- Read: representative supporting reference files under `codex-marketplace/plugins/*/skills/*/references/*.md`

- [ ] **Step 1: Confirm plugin names come from `.codex-plugin/plugin.json` and skill names come from skill frontmatter**

- [ ] **Step 2: Search for skill-reference text and capture the exact source surfaces that contain it**

```powershell
rg -n "skill reference|skill references|Use the installed|Consult the installed|REQUIRED SUB-SKILL|REQUIRED BACKGROUND|superpowers:[A-Za-z0-9_-]+" codex-marketplace/plugins
```

- [ ] **Step 3: Separate marketplace-source references from GPT overlay/export-only material and generated-output material**

### Task 2: Publish the durable inventory receipt

**Files:**
- Create: `docs/superpowers/records/2026-06-17-mark-178-marketplace-skill-reference-inventory.md`

- [ ] **Step 1: Draft a table with current text, source path, inferred target plugin, canonical target, and classification for each observed reference**

```markdown
| Current text | Source path | Inferred target plugin | Canonical target | Classification |
| --- | --- | --- | --- | --- |
| `superpowers:test-driven-development` | `codex-marketplace/plugins/superpowers/skills/writing-skills/SKILL.md` | `superpowers` | `superpowers:test-driven-development` | already project-canonical |
```

- [ ] **Step 2: Call out ambiguous references explicitly, including any bare same-plugin or cross-plugin references that need follow-up**

- [ ] **Step 3: Record the repo schema evidence and the exact search command(s) used**

### Task 3: Validate the inventory and close the loop

**Files:**
- Read: `docs/superpowers/plans/2026-06-17-mark-178-inventory-marketplace-skill-references.md`
- Read: `docs/superpowers/records/2026-06-17-mark-178-marketplace-skill-reference-inventory.md`

- [ ] **Step 1: Re-read the plan against the issue goal and confirm no source rewrites or generated artifacts were produced**

- [ ] **Step 2: Run `git diff --check` and a final `rg` pass to ensure the only changed files are the plan and receipt record**

```powershell
git diff --check
git diff --name-only
```

- [ ] **Step 3: Capture the branch, head SHA, and publication state for the final return**
