# MARK-171 Claude-Cortex Upstream Inventory Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` or `superpowers:subagent-driven-development` to execute this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Inventory the upstream `NickCrew/Claude-Cortex` source tree and select the first `codex-cortex` import candidates with evidence-backed classification.

**Architecture:** Keep the upstream GitHub clone as the source basis, keep the inventory output in a repo-resident markdown record, and keep the candidate decision narrow to `cqrs-event-sourcing` plus only the minimum adjacent surfaces needed to justify the selection. The repo change should document what was inspected, what was excluded, and why `cqrs-event-sourcing` is or is not the first seed for MARK-172.

**Tech Stack:** GitHub source evidence, PowerShell, Markdown records, Linear issue context, `git`.

---

### Task 1: Capture upstream source evidence

**Files:**
- None

- [ ] **Step 1: Resolve the upstream default branch and commit**

Run:

```powershell
git ls-remote --symref https://github.com/NickCrew/Claude-Cortex.git HEAD
```

Expected: `refs/heads/main` and the exact upstream HEAD commit.

- [ ] **Step 2: Clone the upstream source snapshot**

Run:

```powershell
git clone --depth 1 --branch main https://github.com/NickCrew/Claude-Cortex.git $env:TEMP\claude-cortex-upstream
```

Expected: a shallow clone containing the upstream skill tree, registry, docs, and license.

### Task 2: Inspect the candidate surfaces

**Files:**
- None

- [ ] **Step 1: Read the source basis files**

Inspect:

- `LICENSE`
- `README.md`
- `skills/cqrs-event-sourcing/SKILL.md`
- `skills/event-driven-architecture/SKILL.md`
- `skills/database-design-patterns/SKILL.md`
- `skills/registry.yaml`
- `skills/skill-index.json`
- `skills/dependencies.map`
- `docs/reference/moved-readmes/skills.md`

- [ ] **Step 2: Classify the first import candidates**

Produce a narrow table that classifies each candidate as `import now`, `import later`, `reject`, or `needs clarification`, with source evidence and a one-line reason.

### Task 3: Write the durable repo record

**Files:**
- Create: `docs/superpowers/records/2026-06-17-mark-171-claude-cortex-upstream-inventory.md`

- [ ] **Step 1: Write the inventory record**

Record the upstream commit, license, inspected source surfaces, candidate classifications, the `cqrs-event-sourcing` seed decision, the MARK-172 constraint or replacement recommendation, and a statement that no plugin implementation or generated zips were produced.

- [ ] **Step 2: Keep the scope narrow**

Do not add marketplace manifests, generated zips, or plugin implementation files. This issue is inventory and candidate selection only.

### Task 4: Validate and close out

**Files:**
- None

- [ ] **Step 1: Run validation**

Run:

```powershell
git diff --check
```

Expected: no whitespace or patch-format errors.

- [ ] **Step 2: Confirm the publication surface**

Verify the record is committed on the worker branch and the final response includes the upstream commit, the repo branch, and the no-plugin/no-zip confirmation.
