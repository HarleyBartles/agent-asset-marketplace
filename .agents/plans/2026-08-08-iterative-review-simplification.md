# Simplify the `iterative-review` skill surface

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the `iterative-review` skill into a thin orchestrator that delegates every node recipe to a dedicated `references/node-<name>.md` file, while keeping the full review graph and subagent loop intact.

**Architecture:** The existing `SKILL.md` walkthrough is split into 19 per-node reference files (one for every node in `review-state-graph.md`). `SKILL.md` is replaced with a 6-step orchestrator that repeatedly calls `next_node.py` and opens the matching node reference. `review-state-graph.md` is updated to point each node at its reference doc.

**Tech Stack:** Markdown, the existing `iterative-review/scripts/` helpers, and `tools/run.py` for CI and installed-skills regen.

## Global Constraints

- Only edit the canonical source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`; regenerate `.agents/skills/` with `py -3 tools/run.py installed-skills --apply`.
- Every commit must pass `py -3 tools/run.py ci --check`.
- Do not change the `reviewer-*.md` profiles or the `reviewer-strong` guard. The graph and `next_node.py` may be updated to make the new per-node reference surface routable, with matching changes to `review-metrics-schema.json`.
- Work in a feature branch/worktree; do not commit to `main` directly.

---

### Task 1: Extract all node recipes into `references/node-*.md`

**Files:**
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-setup.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-normalize-inputs.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-preflight.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-fast-fix.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-scope-honesty.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-orchestrator-self-review.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-lens-dispatch.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-lens-triage.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-metrics-track.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-finding-fix.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-re-preflight.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-reviewer-fixes.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-regression-scan.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-resolved-ledger.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-final-strong.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-closeout.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-ready.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-blocked.md`
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-next-node.md`
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md` (remove these sections)

**Interfaces:**
- **Consumes:** the existing `### <node>` sections in `SKILL.md`.
- **Produces:** one `references/node-<name>.md` per graph node, each with `## Purpose`, `## Inputs`, `## Recipe`, `## Outputs`, `## Next check`.

- [ ] **Step 1: Create `node-setup.md`**
  Copy the `### setup` section from `SKILL.md` and wrap it in the node template. Run `py -3 tools/run.py ci --check` to ensure no markdown lint errors.

- [ ] **Step 2: Create `node-preflight.md` and `node-fast-fix.md`**
  Copy the `### preflight` and `### fast-fix` sections. Add the `## Outputs` and `## Next check` lines that reference `next_node.py`.

- [ ] **Step 3: Create `node-orchestrator-self-review.md`, `node-lens-dispatch.md`, and `node-lens-triage.md`**
  Copy the matching `SKILL.md` subsections. Preserve the subagent input packaging and severity classification language.

- [ ] **Step 4: Create the fix-loop and ledger nodes (`finding-fix`, `reviewer-fixes`, `regression-scan`, `resolved-ledger`)**
  Copy the matching `SKILL.md` subsections. Ensure `resolved-ledger.md` explicitly mentions `resolved_ledger.py --apply`.

- [ ] **Step 5: Create the terminal nodes (`final-strong`, `closeout`, `ready`, `blocked`)**
  Copy the matching `SKILL.md` subsections. Ensure `final-strong.md` mentions `next_node.py --propose final-strong` and the `reviewer-strong` guard inputs.

- [ ] **Step 6: Remove the node subsections from `SKILL.md`**
  Delete the `### <node>` sections from `SKILL.md` but keep the frontmatter, `## When to Use`, `## Core Pattern`, `## Required reading`, and a short `## Following the graph` orchestrator.

- [ ] **Step 7: Mark Task 1 checkboxes `[x]` in this plan file**
- [ ] **Step 8: Commit**
  ```bash
  git add -A
  git commit -m "Extract iterative-review node recipes into references/node-*.md"
  ```

---

### Task 2: Rewrite `SKILL.md` as the thin orchestrator

**Files:**
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

**Interfaces:**
- **Consumes:** the `node-*.md` references created in Task 1.
- **Produces:** a `SKILL.md` that only contains the 6-step orchestrator plus `## Required reading`.

- [ ] **Step 1: Replace `## Following the graph` with the 6-step orchestrator**
  The new `SKILL.md` body must be:
  1. Determine `<base>`, `<branch>`, and create the off-repo scratch workspace.
  2. Create an empty `review-metrics.json` in the scratch.
  3. Run `py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json`.
  4. Open `references/node-<node>.md` for the node printed by `next_node.py` and follow it exactly.
  5. Return to step 3 after the node is done.
  6. Stop when `next_node.py` prints `ready` or `blocked`.

- [ ] **Step 2: Update `## Required reading`**
  Add the `references/node-*.md` pattern to `## Required reading` and remove detailed node instructions that now live in the node files.

- [ ] **Step 3: Run `ci --check` and fix any lint or link errors**
  Run: `py -3 tools/run.py ci --check`
  Expected: all targets pass.

- [ ] **Step 4: Mark Task 2 checkboxes `[x]` in this plan file**
- [ ] **Step 5: Commit**
  ```bash
  git commit -m "Rewrite iterative-review SKILL.md as thin orchestrator"
  ```

---

### Task 3: Update `review-state-graph.md` with node reference pointers

**Files:**
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md`

**Interfaces:**
- **Consumes:** the `node-*.md` references and the `references/review-state-graph.md` node table.
- **Produces:** a node table that maps each graph node to its recipe file.

- [ ] **Step 1: Add a `Recipe` column to the node table**
  For each node, add a link to `references/node-<name>.md` in the `## Nodes` table.

- [ ] **Step 2: Add an intro sentence before the Mermaid graph**
  State that the canonical node recipes live in the `references/node-*.md` files and that the orchestrator uses `next_node.py` to discover the current node.

- [ ] **Step 3: Run `ci --check` and commit**
  Run: `py -3 tools/run.py ci --check`
  Expected: all targets pass.
  ```bash
  git add -A
  git commit -m "Point review-state-graph nodes at node reference docs"
  ```
- [ ] **Step 4: Mark Task 3 checkboxes `[x]` in this plan file**

---

### Task 4: Regenerate installed skills and verify CI

**Files:**
- **Modify:** `.agents/skills/iterative-review/` (regenerated)

**Interfaces:**
- **Consumes:** the canonical source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`.
- **Produces:** an up-to-date `.agents/skills/` copy and a passing CI.

- [ ] **Step 1: Regenerate installed skills**
  Run: `py -3 tools/run.py installed-skills --apply`

- [ ] **Step 2: Run the canonical preflight**
  Run: `py -3 tools/run.py ci --check`
  Expected: all targets pass.

- [ ] **Step 3: Stage and commit the regenerated installed skills**
  ```bash
  git add -A
  git commit -m "Regenerate installed skills for iterative-review refactor"
  ```
- [ ] **Step 4: Mark Task 4 checkboxes `[x]` in this plan file**

---

### Task 5: Smoke-test the new structure on a trivial PR

**Files:**
- **Create (off-repo, temporary):** a scratch `review-metrics.json` for the test

**Interfaces:**
- **Consumes:** the new `SKILL.md`, `next_node.py`, and a temporary `review-metrics.json`.
- **Produces:** evidence that `next_node.py` advances through `setup`, `preflight`, etc., and that the orchestrator can open the matching `node-*.md`.

- [ ] **Step 1: Create a minimal `review-metrics.json` in a temp directory**
  ```json
  {
    "pr": {"branch": "feat/test", "base": "main", "head_sha": "test"},
    "rounds_per_finding": [],
    "regressions": []
  }
  ```

- [ ] **Step 2: Run `next_node.py` and verify it returns `setup`**
  Run: `py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <temp>/review-metrics.json`
  Expected: prints `setup` because `review-metrics.json` is new and the ledger is missing.

- [ ] **Step 3: Advance through a few synthetic nodes and verify the reference files open correctly**
  Manually update `review-metrics.json` with `findings_by_node.preflight: 0` and re-run `next_node.py` to see it move to `preflight`. Open `references/node-preflight.md` and confirm it contains the preflight recipe.

- [ ] **Step 4: Record the smoke test result in the scratch directory or a short note**
  No source code change needed. This step is for confidence only.
- [ ] **Step 5: Mark Task 5 checkboxes `[x]` in this plan file**

---

## Spec coverage check

| Spec acceptance criterion | Task |
|---|---|
| `SKILL.md` is reduced to the 6-step orchestrator | Task 2 |
| Every current node section becomes a `references/node-<name>.md` file | Task 1 |
| `next_node.py` is a stateful graph router with `current_node`/`previous_node` and `--propose` validation | Task 5 (smoke test) + script changes per spec section 5 |
| `ci --check` passes after refactor | Task 1–4 |
| Test walkthrough of a trivial PR follows the new structure | Task 5 |

## Placeholder scan

No `TBD`, `TODO`, or undefined file names. All paths and commands are explicit.
