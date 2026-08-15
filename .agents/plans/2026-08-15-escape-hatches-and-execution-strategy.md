# Escape Hatches and Execution Strategy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Surface plan-escape hatches in the planning skills, encode a recommended `Execution Strategy` in every plan header, and make execution skills read and respect that recommendation without re-litigating the plan.

**Architecture:** Add canonical shared references in the `superpowers-plus` plugin source, update `SKILL.md` files to act as lean routers that point to bundled references, and add a build step that injects copies of shared references into each vendored skill directory so consumers receive self-contained skills.

**Tech Stack:** Markdown, Python 3 build tooling.

**Execution Strategy:** `subagent-driven-development` — one subagent per skill update and one for the build integration. Tasks are independent across skills after the shared references exist.

## Global Constraints

- **No cross-skill references.** Each `SKILL.md` is a lean router that points to files bundled under its own `references/` directory. Shared canonical files live under `codex-marketplace/plugins/superpowers-plus/references/` and are injected into each skill at build time.
- **Vendored skills are canonical.** The source skills under `codex-marketplace/plugins/superpowers-plus/skills/` are what consumers install. Every skill that needs a shared reference must carry a physical copy, not a pointer outside the skill.
- **Plan header encodes execution strategy.** Every `writing-plans` plan must include an `Execution Strategy` field in its header. Execution skills read this field on startup.
- **One-lane rule.** An execution agent picks one lane at the start, announces it, and sticks to it unless the human asks to change. Human explicit direction wins over the plan's recommendation.
- **Execution strategy is advisory.** The executing agent can override the plan's recommendation if it has a defensible assessment or human direction, but it must report the choice.

---

### Task 1: Create canonical shared references and the sync script

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/references/plan-scope-sizing.md`
- Create: `codex-marketplace/plugins/superpowers-plus/references/execution-lane-override.md`
- Create: `tools/sync_skill_shared_references.py`
- Modify: `tools/run.py` (insert the sync step into the marketplace task)
- Modify: `tools/validate_marketplace.py` (add a `shared-references` validation phase)

**Interfaces:**
- Produces: `tools/sync_skill_shared_references.py --check` and `--apply` commands.
- Produces: `tools/validate_marketplace.py --phase shared-references`.
- Produces: fresh reference copies in `codex-marketplace/plugins/superpowers-plus/skills/*/references/`.

- [x] **Step 1: Write `plan-scope-sizing.md`**

Create `codex-marketplace/plugins/superpowers-plus/references/plan-scope-sizing.md` with this exact content:

```markdown
# Plan Scope Sizing

Use when a `writing-plans` or `working-with-epics` session feels large, overwhelming, or "huge".

## The three escape hatches

A plan is too large when it no longer fits in your context as a single execution unit. If you find yourself thinking "this is a lot", "this is huge", or "this plan is too big", use one of these escape hatches in this order.

### 1. Well-sliced but long plan

The plan has many tasks, but each task is self-contained, has its own test cycle, and fits in a single review.

- This is correct. Do not shrink the plan to make it shorter.
- The length is not the problem; the slice quality is what matters.
- Hand the plan to `subagent-driven-development` and execute one task at a time.
- If the tasks are tightly coupled and not independent, see hatch 2.

### 2. Cross-concern plan

The plan covers multiple independent subsystems, concerns, or code boundaries that could be reviewed and delivered separately.

- Stop writing the current plan.
- Invoke `working-with-epics` and build a sequenced roadmap.
- Write Plan 1 from the first concern, and leave the others as pending plans.
- This is for legitimately cross-concern work, not for making tiny plans.

### 3. Oversized plan inside an epic

The plan is already part of an epic, but while writing it you discover it is too big for one deliverable.

- Stop writing the current plan.
- Split the remaining scope into a new plan.
- Update the epic roadmap with the new plan, its place in the sequence, and a note explaining the split.
- This is a fallback for legitimately over-scoped plans, not a license to create endless epics of tiny plans.

## What "huge" does not mean

- A large number of well-scoped tasks is not huge. It is the expected shape for `subagent-driven-development`.
- A long plan with every task testable on its own is not a bug.
- The right response to a well-sliced large plan is execution, not decomposition.
```

- [x] **Step 2: Write `execution-lane-override.md`**

Create `codex-marketplace/plugins/superpowers-plus/references/execution-lane-override.md` with this exact content:

```markdown
# Execution Lane Override

Use when the execution skill you are in differs from the `Execution Strategy` written in the plan.

## Authority order

When picking an execution lane, follow this order:

1. **Human explicit direction.** The user told you which skill to use, or explicitly chose a lane (for example, by typing `/executing-plans`). This wins over all other signals.
2. **Your own assessment of the plan.** If the user did not direct the lane, read the plan, look at the task shape, and choose the lane that fits best.
3. **The plan's `Execution Strategy`.** This is a recommendation, not a command. It is one input to your decision.

## One-lane rule

Pick one lane before execution starts. Announce it:

> "I am using `<lane-name>` to execute this plan."

Then see it through. Do not switch lanes mid-execution unless the human asks you to.

## When the plan recommends a different lane

If the plan's `Execution Strategy` does not match the lane you chose, do not ask the human for confirmation by default. Instead:

1. Note the mismatch:
   - "Plan recommends `subagent-driven-development`. I am using `executing-plans` because you invoked it."
   - "Plan recommends `executing-plans`. I am using `subagent-driven-development` because the tasks are independent and this is the better fit."
2. Confirm to yourself that you have human direction or a defensible assessment for the mismatch.
3. Proceed. If you can give neither human direction nor a clear assessment, raise a focused question to the human.
```

- [x] **Step 3: Create `tools/sync_skill_shared_references.py`**

Implement `tools/sync_skill_shared_references.py` with `--check` and `--apply` modes:

- Read the canonical reference files from `codex-marketplace/plugins/superpowers-plus/references/`.
- Copy `plan-scope-sizing.md` into:
  - `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/references/`
  - `codex-marketplace/plugins/superpowers-plus/skills/working-with-epics/references/`
- Copy `execution-lane-override.md` into:
  - `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/references/`
  - `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/references/`
  - `codex-marketplace/plugins/superpowers-plus/skills/dispatching-parallel-agents/references/`
- In `--check` mode, fail with a clear message if any destination copy is missing or differs from the canonical source.
- In `--apply` mode, write the canonical text to each destination, creating the `references/` directory if needed.
- Print a concise summary of which files were checked or written.

- [x] **Step 4: Wire the sync script into `tools/run.py` and `tools/validate_marketplace.py`**

Modify `tools/run.py`:
- In `_apply_marketplace`, before `tools/generate_marketplace.py --apply`, run `[sys.executable, "tools/sync_skill_shared_references.py", "--apply"]`.
- In `_check_marketplace` or the `all` validation path, ensure `tools/validate_marketplace.py --phase all` eventually covers the shared references. Either add a `shared-references` phase that calls `tools/sync_skill_shared_references.py --check`, or call it directly before validation.

Modify `tools/validate_marketplace.py`:
- Add a `shared-references` phase choice to the `--phase` argument.
- Add `def validate_shared_references():` that calls `tools/sync_skill_shared_references.py --check`.
- Register the phase in the `phase_runners` mapping.

- [x] **Step 5: Commit** (`Task 1`)

```bash
git add codex-marketplace/plugins/superpowers-plus/references/ tools/sync_skill_shared_references.py tools/run.py tools/validate_marketplace.py
git commit -m "feat: add canonical shared skill references and sync tooling

Add plan-scope-sizing and execution-lane-override references in the
superpowers-plus plugin source. Add a build-time sync script that injects
copies into the vendored skill directories and validates they stay fresh.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 2: Update `writing-plans/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/references/plan-scope-sizing.md` (via the sync script from Task 1, then verify)

**Interfaces:**
- Consumes: `plan-scope-sizing.md` and `execution-lane-override.md` exist as canonical references.
- Produces: `Execution Strategy` header field, right-sizing pointer, size check, and updated execution handoff.

- [x] **Step 1: Add `Execution Strategy` to the Plan Document Header**

In the `## Plan Document Header` section, insert the following line after `**Tech Stack:**`:

```markdown
**Execution Strategy:** `subagent-driven-development` (default for independent tasks) — `executing-plans` (for tightly coupled/sequential tasks), `dispatching-parallel-agents` (for 2+ independent parallel tracks), or `manual` (for human-driven work). The planner picks the recommended lane.
```

- [x] **Step 2: Add a Right-Sizing section**

Insert a new `## Right-Sizing and Escape Hatches` section between `## Task Right-Sizing` and `## Bite-Sized Task Granularity` (or after `## Task Right-Sizing` if the file order differs). Use this exact text:

```markdown
## Right-Sizing and Escape Hatches

If you think "this is a lot" or "the plan is huge" while writing, you are at a scope sizing decision point. **MUST READ:** `references/plan-scope-sizing.md` and follow one of the three escape hatches before continuing.

A long plan with well-sliced, independently testable tasks is not a problem. The `subagent-driven-development` execution lane is designed for that shape. A plan is too big only when it crosses independent concerns or one of its tasks cannot fit in one review cycle.
```

- [x] **Step 3: Add the Plan Size Check to the self-review gate**

In the `## Self-review & plan-readiness gate` section, add `### 5. Plan Size Check` before the final `Plan-readiness rating` step:

```markdown
**5. Plan Size Check:** Did you think the plan was too large while writing? If yes, did you apply one of the escape hatches in `references/plan-scope-sizing.md`? Is the `Execution Strategy` field filled with an allowed value and a clear rationale?
```

- [x] **Step 4: Update the Execution Handoff**

Replace the `## Execution Handoff` section with this:

```markdown
## Execution Handoff

After the plan is saved and the plan-readiness rating meets the floor, read the `Execution Strategy` and present it to the user:

> "Plan complete and saved to `.agents/plans/<filename>.md`. The `Execution Strategy` is `<strategy>`. The plan-readiness rating is `<X>/10`.
> Do you want to proceed with the recommended strategy, or switch to another lane?"

If the user chooses a different lane, note it in the handoff and let the executing skill handle the override. Do not re-derive the whole plan from scratch.
```

- [x] **Step 5: Run the sync script and commit** (`Task 2`)

```bash
py -3 tools/sync_skill_shared_references.py --apply
git add codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/writing-plans/references/plan-scope-sizing.md
git commit -m "feat(writing-plans): encode execution strategy and escape hatches

Add the Execution Strategy field to the plan header, route planners to
plan-scope-sizing.md when a plan feels too large, and update the execution
handoff to present the plan's recommendation.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 3: Update `working-with-epics/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/working-with-epics/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/working-with-epics/references/plan-scope-sizing.md` (via the sync script, then verify)

**Interfaces:**
- Consumes: `plan-scope-sizing.md` canonical reference.
- Produces: A Lane 3 for splitting oversized plans and a clear pointer to the scope sizing reference.

- [x] **Step 1: Add Lane 3 — Split an Oversized Plan**

Insert a new `## Lane 3 — Split an Oversized Plan` section after `## Lane 2 — Continue an Epic`:

```markdown
## Lane 3 — Split an Oversized Plan

If a plan in progress grows beyond one deliverable, stop writing. **MUST READ:** `references/plan-scope-sizing.md` and use escape hatch 3:

1. Close the current plan file at a clean boundary (end of the last fully scoped task).
2. Create a new plan file for the remaining scope in the same epic directory.
3. Update the epic roadmap table with the new plan, its place in the sequence, and a `Handoff Notes` entry explaining why the split happened.
4. Mark the original plan as `blocked` or `replan` in the roadmap if it cannot continue as written.

This is a fallback for legitimately over-scoped plans. It is not an excuse to create endless epics of tiny plans.
```

- [x] **Step 2: Update Boundary cases to point to the reference**

In the `## Boundary cases` section, replace the existing text with this:

```markdown
## Boundary cases

If a roadmap item should split into a new epic, a scope change invalidates multiple pending plans, or you are choosing between asking the human and escalating through `risk-gates`, load `references/scope-notes.md` and `references/plan-scope-sizing.md` and follow their guidance.
```

- [x] **Step 3: Run the sync script and commit** (`Task 3`)

```bash
py -3 tools/sync_skill_shared_references.py --apply
git add codex-marketplace/plugins/superpowers-plus/skills/working-with-epics/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/working-with-epics/references/plan-scope-sizing.md
git commit -m "feat(working-with-epics): add JIT plan splitting lane

Add a Lane 3 for splitting oversized epic plans and point to the shared
plan-scope-sizing.md reference for the right escape hatch.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 4: Update `executing-plans/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/references/execution-lane-override.md` (via the sync script)

**Interfaces:**
- Consumes: Plan `Execution Strategy` field; `execution-lane-override.md` reference.
- Produces: Execution lane decision step in `Step 1: Load and Review Plan`.

- [x] **Step 1: Add the execution lane decision to the load step**

In `### Step 1: Load and Review Plan`, replace the numbered list with this:

```markdown
### Step 1: Load and Review Plan
1. Ensure an isolated workspace: use /using-git-worktrees to create one or verify the existing one
2. Read plan file
3. Note the `Execution Strategy` in the plan header. **MUST READ:** `references/execution-lane-override.md` and confirm the lane you are using is the right one: human explicit direction wins, then your own assessment, then the plan's recommendation
4. Announce the lane you will use and see it through unless the human asks to change
5. Review critically - identify any questions or concerns about the plan
6. If concerns: Raise them with your human partner before starting
7. If no concerns: Create todos for the plan items and proceed
```

- [x] **Step 2: Run the sync script and commit** (`Task 4`)

```bash
py -3 tools/sync_skill_shared_references.py --apply
git add codex-marketplace/plugins/superpowers-plus/skills/executing-plans/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/executing-plans/references/execution-lane-override.md
git commit -m "feat(executing-plans): read plan execution strategy

Add a step to read the plan's Execution Strategy and decide the lane
according to the execution-lane-override guidance.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 5: Update `subagent-driven-development/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/references/execution-lane-override.md` (via the sync script)

**Interfaces:**
- Consumes: Plan `Execution Strategy` field; `execution-lane-override.md` reference.
- Produces: Execution lane note in the `## Setup` section.

- [x] **Step 1: Add the execution lane note to Setup**

In the `## Setup` section, after the `Read the repo's .agents/runbooks/implementing.md` block, add this paragraph:

```markdown
Read the plan once, note its context and Global Constraints, and create a todo per task. Before Task 1, note the `Execution Strategy` in the plan header. **MUST READ:** `references/execution-lane-override.md` to confirm `subagent-driven-development` is the right lane. If the plan recommends a different lane but you are using this one because the tasks are independent or the human directed it here, state that at the start of execution and do not re-litigate.
```

- [x] **Step 2: Run the sync script and commit** (`Task 5`)

```bash
py -3 tools/sync_skill_shared_references.py --apply
git add codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/references/execution-lane-override.md
git commit -m "feat(subagent-driven-development): respect plan execution strategy

Add guidance to read the plan's Execution Strategy and confirm the lane
using the execution-lane-override reference.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 6: Update `dispatching-parallel-agents/SKILL.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/dispatching-parallel-agents/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/dispatching-parallel-agents/references/execution-lane-override.md` (via the sync script)

**Interfaces:**
- Consumes: Plan `Execution Strategy` field; `execution-lane-override.md` reference.
- Produces: A short execution strategy note near the top of the skill.

- [x] **Step 1: Add an Execution Strategy note**

After `## Overview` (or near the top of the process), insert:

```markdown
## Execution Strategy Note

If you are invoking this skill from a plan, read the `Execution Strategy` in the plan header and **MUST READ:** `references/execution-lane-override.md` before dispatching. Announce that you are using `dispatching-parallel-agents` and see it through unless the human asks to change.
```

- [x] **Step 2: Run the sync script and commit** (`Task 6`)

```bash
py -3 tools/sync_skill_shared_references.py --apply
git add codex-marketplace/plugins/superpowers-plus/skills/dispatching-parallel-agents/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/dispatching-parallel-agents/references/execution-lane-override.md
git commit -m "feat(dispatching-parallel-agents): respect plan execution strategy

Add an Execution Strategy note that reads the plan header and follows the
execution-lane-override guidance before parallel dispatch.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 7: Regenerate marketplace and installed skills

**Files:**
- Modify: `codex-marketplace/manifest.json` (regenerated)
- Modify: `.agents/plugins/marketplace.json` (regenerated)
- Modify: `.agents/skills/` installed copies (regenerated)

**Interfaces:**
- Consumes: All source skill changes from Tasks 1-6.
- Produces: Fresh marketplace manifest and installed skill copies.

- [x] **Step 1: Run the full marketplace apply**

```bash
py -3 tools/run.py marketplace --apply
```

- [x] **Step 2: Verify the vendored and installed copies are fresh**

```bash
py -3 tools/sync_skill_shared_references.py --check
py -3 tools/run.py installed-skills --check
```

If either fails, run the corresponding `--apply` command and re-check.

- [x] **Step 3: Commit regenerated files** (`Task 7`)

```bash
git add codex-marketplace/manifest.json .agents/plugins/marketplace.json .agents/skills/
git commit -m "chore: regenerate marketplace and installed skills

Project the updated superpowers-plus skill sources into the marketplace
manifest and the installed `.agents/skills/` copies.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
```

---

### Task 8: Run CI and open a pull request

**Files:**
- None (verification and publication)

**Interfaces:**
- Produces: Passing `py -3 tools/run.py ci --check` and an open draft PR.

- [x] **Step 1: Run the canonical CI check**

```bash
py -3 tools/run.py ci --check
```

If it fails, fix the issue or split the problem into a new plan. Do not proceed until `ci --check` passes.

- [x] **Step 2: Self-review and plan-readiness rating**

Run the `handoff-gates` `plan-readiness` lane. Verify:

1. **Spec coverage:** This plan covers all discussed changes (escape hatches, execution strategy in header, one-lane rule, build-time reference sync, and updates to five skills).
2. **Placeholder scan:** No TBD, TODO, or vague steps remain. Each task contains exact file paths and exact content to write.
3. **Type consistency:** The `Execution Strategy` allowed values are consistent across the header definition and the execution skill references.
4. **Validation completeness:** Marketplace regeneration and `ci --check` are the final validation steps.

Report the final rating here before handoff.

- [x] **Step 3: Push and open a draft PR**

```bash
git push -u origin plan-escape-hatches-execution-strategy
gh pr create --draft --title "feat: plan escape hatches and execution strategy" --body-file .agents/plans/2026-08-15-escape-hatches-and-execution-strategy.md
```

Capture the PR URL and head SHA for publication proof.

---

## Plan-Readiness Rating

**Rating:** 8/10

The plan is concrete on the skill and reference content. The remaining 9/10 uncertainty is the exact insertion points inside the legacy `tools/run.py` and `tools/validate_marketplace.py` Python code; those files are straightforward to extend but the implementer should inspect the current `phase_runners` and `_apply_marketplace` helper before writing the exact edits. The plan names the function and the task clearly, so a competent implementer can close this gap in context.

## Execution and Completion Notes

- Execution lane: `executing-plans` (plan recommended `subagent-driven-development`; overridden because the user was in the session and the work was sequential and small enough for a single execution session).
- All Tasks 1-8 completed and verified.
- `py -3 tools/run.py ci --check`: passed.
- `py -3 tools/run.py marketplace --apply`: passed.
- Shared references stay in sync via `tools/sync_skill_shared_references.py`.
- Completion-readiness self-rating: 9/10.
