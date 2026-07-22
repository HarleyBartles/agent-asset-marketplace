# Update subagent-model-routing Devin Desktop profile

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the first-party `subagent-model-routing` skill so its Devin Desktop profile reflects the actual `run_subagent` dispatch controls (profile only, no model/reasoning/paid selection), and add a `use_after` link to `inspecting-the-environment`. Codex and generic profiles remain untouched.

**Architecture:** Edit the canonical first-party source files under `sources/first_party/skills/subagent-model-routing/`, then run the full marketplace rebuild to project the changes into plugin copies and installed skill copies. Detailed guidance stays in `references/`; `SKILL.md` body remains short.

**Tech Stack:** Markdown skill docs, YAML frontmatter, `py -3 tools/rebuild_marketplace.py`, `py -3 tools/check_marketplace.py`.

## Global Constraints

- Only edit first-party source; never hand-edit generated plugin projections or `.agents/skills/` installed copies.
- Do not touch `references/codex-profile.md` or `references/generic-free-first-profile.md`.
- Do not encode specific model version numbers (e.g., `SWE-1.7`, `GLM-5.2`) in the Devin Desktop profile; model families (`SWE-family`, `GLM-family`) are allowed without versions.
- No budget/cost constraints in Devin Desktop; the runtime does not expose paid route selection.
- All marketplace projection changes must be produced by `py -3 tools/rebuild_marketplace.py` and verified by `py -3 tools/check_marketplace.py`.
- Worktree: `Z:\_agent-worktrees\agent-asset-marketplace\2026-07-22-subagent-model-routing-devin`, branch `subagent-model-routing-devin`, base `origin/main` (`3f83269d5ecbba174afd55f83dfc3205112098b4`).

---

### Task 1: Add `use_after` link to `SKILL.md` frontmatter

**Files:**
- Modify: `sources/first_party/skills/subagent-model-routing/SKILL.md` (frontmatter only)

**Interfaces:**
- Consumes: existing `SKILL.md` frontmatter
- Produces: updated frontmatter with `use_after: [inspecting-the-environment]`

- [x] **Step 1: Replace the `related_skills` block with the block including `use_after`**

```markdown
  related_skills:
  - dispatching-parallel-agents
  - risk-gates
  - work-mode-router
  - repo-worker-base
  use_after:
  - inspecting-the-environment
```

- [x] **Step 2: Verify the file still parses as YAML**

Run: `py -3 tools/normalize_first_party_skill_sources.py --check`
Expected: `OK` or no error for `subagent-model-routing`.

- [x] **Step 3: Commit the frontmatter change**

```bash
git add sources/first_party/skills/subagent-model-routing/SKILL.md
git commit -m "feat(subagent-model-routing): add use_after link to inspecting-the-environment"
```

---

### Task 2: Rewrite Devin Desktop profile for dispatch-profile routing

**Files:**
- Modify: `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md`

**Interfaces:**
- Consumes: existing `devin-desktop-profile.md`
- Produces: a profile that describes only the `run_subagent` `profile` parameter and task-to-dispatch mapping

- [x] **Step 1: Replace the entire file content**

```markdown
### Devin Desktop dispatch contract

The only caller-controllable subagent control in Devin Desktop is the `run_subagent` dispatch `profile`. The runtime selects the actual model, reasoning effort, context tier, and any paid route. Do not attempt to specify those in the `task` prompt or elsewhere.

`run_subagent` accepts:

- `profile`: `subagent_explore` (read-only) or `subagent_general` (full tool access)
- `task`: the instruction
- `title`: short human-readable label
- `is_background`: launch in the background for parallel work
- `resume`: continue a previous subagent

The runtime assigns the same model as the parent session. Do not encode current model names or versions in prompts, task briefs, or rationale; they may change.

### Selecting the dispatch profile

- `subagent_explore` — read-only exploration, research, inventories, scans, technical review, code review, and any task that does not require file edits or command execution.
- `subagent_general` — implementation, mutation, file edits, command execution, validation, and any task that requires write or exec access.

A task that mixes read-heavy exploration with mutation is normally `subagent_general` with bounded mutation. Use `subagent_explore` only when the work is genuinely read-only.

### Task routing

| Task | Dispatch |
|---|---|
| Live source exploration / planning (read-only) | `subagent_explore` |
| Planning that will be implemented by the same subagent | `subagent_general` |
| Mechanical / approved implementation | `subagent_general` |
| Hidden root-cause bug | `subagent_general` with broad investigation and bounded mutation |
| Screenshot / frontend diagnosis | `subagent_general` if interactive tooling is needed, else `subagent_explore` |
| Technical code review | `subagent_explore` with fresh context |
| Architecture / intent challenge | `subagent_explore` with a focused, non-overlapping prompt |
| Large repo / diff context pressure | Decompose across `subagent_explore` and `subagent_general`; there is no paid context tier |
| Retry after a failed subagent | Refine the prompt, narrow scope, or decompose; do not retry by "changing model" |

### Deviation from shared policy

The shared policy's free/included/metered and cost-preference rules do not apply in Devin Desktop because the runtime does not expose paid or metered choices. Route by capability and access need only.

### What not to do

- Do not specify a model name, version, reasoning level, context tier, or paid route. The tool has no such parameters.
- Do not select `subagent_general` for purely read-only work; it broadens the permission surface unnecessarily.
- Do not select `subagent_explore` for tasks that must write files or run commands.
- Do not treat `is_background` as a model or reasoning selector; it only controls parallel launch.
- Do not request paid context; no such option exists.
```

- [x] **Step 2: Verify no specific model version numbers were introduced**

Run: `git diff -- sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md`
Expected: no lines containing `SWE-1.7`, `GLM-5.2`, `1.7 Max`, `1.6`, `1.6 Fast`, `$`, or other version/price strings.

- [x] **Step 3: Commit the profile rewrite**

```bash
git add sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md
git commit -m "feat(subagent-model-routing): rewrite devin-desktop profile for run_subagent dispatch profiles"
```

---

### Task 3: Update Devin Desktop pressure scenarios

**Files:**
- Modify: `sources/first_party/skills/subagent-model-routing/references/pressure-scenarios.md`

**Interfaces:**
- Consumes: existing `### Devin Desktop` section
- Produces: dispatch-profile-based pressure scenarios with no model version numbers

- [x] **Step 1: Replace the `### Devin Desktop` section**

```markdown
### Devin Desktop

15. New repo feature needs live exploration and planning -> `subagent_explore`; switch to `subagent_general` only for implementation.
16. Product-level textual design discussion without substantial repo work -> `subagent_explore`.
17. Approved mechanical implementation -> `subagent_general`.
18. Hidden root-cause bug -> `subagent_general` with broad investigation but bounded mutation.
19. Screenshot-dependent frontend fault -> `subagent_general` if interactive tooling is needed, else `subagent_explore`.
20. Technical code review -> `subagent_explore` with fresh context.
21. Plan needs architecture / intent challenge -> `subagent_explore` with a non-overlapping prompt.
22. "Parent used one model family, therefore the other must review" -> reject automatic model-family pairing; classify the review question and choose `subagent_explore` or `subagent_general`.
23. "The task is easy, therefore use a weaker/smaller model" -> reject; model is not selectable. Use `subagent_explore` for read-only and `subagent_general` for mutation.
24. "A different/faster/cheaper model is available, therefore use it" -> reject; model, cost, and reasoning are not dispatch dimensions while current dispatches are adequate.
25. Subagent fails and retry by "changing model" is requested -> reject; retry by refining the prompt, narrowing scope, or decomposing.
26. Large diff / repo triggers a request for paid context -> reject; no paid context tier. Decompose across `subagent_explore` and `subagent_general`.
27. Provider benchmark conflicts with repeated local evaluation -> preserve the documented profile until an evaluation-backed update is made; do not drift ad hoc.
```

- [x] **Step 2: Verify no specific model version numbers were introduced**

Run: `git diff -- sources/first_party/skills/subagent-model-routing/references/pressure-scenarios.md`
Expected: no lines containing `SWE-1.7`, `GLM-5.2`, `1.7`, `1.6`, `5.2`, or other version strings.

- [x] **Step 3: Commit the pressure-scenario update**

```bash
git add sources/first_party/skills/subagent-model-routing/references/pressure-scenarios.md
git commit -m "feat(subagent-model-routing): update devin-desktop pressure scenarios for dispatch profiles"
```

---

### Task 4: Regenerate marketplace projections and validate

**Files:**
- Generated/projected: `codex-marketplace/plugins/*/skills/subagent-model-routing/**/*`
- Generated/projected: `.agents/skills/subagent-model-routing/**/*`
- Generated/projected: `generated/skill-zips/subagent-model-routing.zip`

**Interfaces:**
- Consumes: first-party source changes from Tasks 1-3
- Produces: updated, deterministic projection surfaces

- [x] **Step 1: Run the full marketplace rebuild**

Run: `py -3 tools/rebuild_marketplace.py`
Expected: exits `0` with no errors.

- [x] **Step 2: Run the CI gate**

Run: `py -3 tools/check_marketplace.py`
Expected: `Marketplace validation passed.` and exit `0`.

- [x] **Step 3: Review the diff to confirm only intended files changed**

Run: `git diff --stat`
Expected: changes only in first-party source, plugin projections, installed `.agents/skills/`, and generated zips for `subagent-model-routing`.

- [x] **Step 4: Commit the regenerated projection artifacts**

```bash
git add -A
git commit -m "chore(subagent-model-routing): regenerate marketplace projections"
```

---

### Task 5: Update plan checkboxes and publish

**Files:**
- Modify: `.agents/superpowers/plans/2026-07-22-update-subagent-model-routing-devin.md`

**Interfaces:**
- Consumes: completed tasks above
- Produces: plan file with all checkboxes checked and the implementation PR

- [x] **Step 1: Mark all task checkboxes `[x]`**

- [x] **Step 2: Commit the checked-off plan**

```bash
git add .agents/superpowers/plans/2026-07-22-update-subagent-model-routing-devin.md
git commit -m "docs(plan): mark subagent-model-routing devin update plan complete"
```

- [x] **Step 3: Push the branch**

```bash
git push -u origin subagent-model-routing-devin
```

- [x] **Step 4: Open a PR into `main`**

Use `gh pr create` with a body summarizing the changes, the base `main`, and the final head SHA.

---

## Execution confidence assessment

- **Confidence: 9/10.**
- All file paths and exact content are known and verified against the current source tree.
- No new marketplace entries or manifest edits are required; the skill already exists and is projected.
- Validation commands are deterministic and run cleanly on the current `origin/main` base.
- The only risk is a future runtime change that introduces additional `run_subagent` controls; the profile intentionally avoids encoding version numbers to stay current.
