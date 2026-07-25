# Epic Workflow Design

## Goal

Add an epic workflow to the agent-asset-marketplace skill tree so agents can decompose large goals into a sequenced roadmap of plans, execute those plans with readiness gates at every stage boundary, and track progress in a committed roadmap artifact.

## Problem

- Plans can become huge.
- Agents spend too long reasoning about whether a single plan is safe.
- `writing-plans` already guides agents to scope plans tightly, but it gives no path when the spec itself is too large for one plan.
- We need a skill that breaks huge goals into multiple consecutive plans, executes them sequentially, and keeps a live work log of the execution order.

## Design Overview

Introduce two first-party skills and update the relevant third-party overlays.

### 1. `handoff-gates`

One skill with three lanes, each a readiness gate at a stage boundary.

| Lane | Boundary | Rating question |
| --- | --- | --- |
| `spec-readiness` | `brainstorming` → `writing-plans` | Can a planning agent expand this spec into a full plan without improvising or discovering seams mid-flight? |
| `plan-readiness` | `writing-plans` → execution | Can the implementing agent or orchestrator plus subagents execute this plan without improvising mid-flight? |
| `completion-readiness` | `executing-plans` → code review | What will a code reviewer find when they review this work against the plan and the repo's code review guide? |

Each lane uses a 1–10 execution-confidence scale:

- **< 8:** Identify the gaps that lower confidence, strengthen the artifact, then re-rate. Never hand off below 8.
- **8–8.9:** Acceptable to execute, but the agent should attempt one bounded strengthening pass to reach 9+.
- **≥ 9:** Hand off to the next stage. Report the final rating in the handoff and record it in the roadmap.

For `completion-readiness`, 9/10 means "high confidence the work will pass code review with no findings or only minor nits." If the rating is below 9, the agent must address the issues before handing off to code review.

### 2. `working-with-epics`

The epic orchestrator. Triggered when `writing-plans` scope check fails or when the human frames a request as a large/epic goal. It has two lanes.

**Lane 1 — Start an Epic**

1. Read the spec from `brainstorming` or the human.
2. Run `handoff-gates` `spec-readiness`.
3. Decompose the epic into a roadmap at `.agents/superpowers/roadmaps/YYYY-MM-DD-<epic-name>.md`.
4. Use `writing-plans` to write Plan 1, enriched with the roadmap context.
5. Run `handoff-gates` `plan-readiness`.
6. Hand off to execution via `executing-plans` or `subagent-driven-development`.

**Lane 2 — Continue an Epic**

1. Read the existing roadmap.
2. Pick the next `pending` or `blocked` item.
3. Write the next plan just-in-time, incorporating all prior commits, PRs, worktree state, and learnings.
4. Run `handoff-gates` `plan-readiness`.
5. Execute the plan.
6. Update the roadmap with status, commit, PR, final rating, and notes.
7. Repeat from step 1 until the epic is done.
8. Run `handoff-gates` `completion-readiness` before code review.

## Roadmap Artifact

- **Location:** `.agents/superpowers/roadmaps/YYYY-MM-DD-<epic-name>.md`
- **Status:** Repo resident, committed, not gitignored.
- **Nature:** Live document. The executing agent edits it as the epic progresses.
- **Schema:** A markdown table with these columns:
  - `#`
  - `Title`
  - `Status` (`pending`, `writing`, `ready`, `executing`, `done`, `blocked`)
  - `Plan File`
  - `Commit`
  - `PR`
  - `Rating` (final execution-confidence rating)
  - `Notes`
- Plus a `Handoff Notes` section for learnings, dependencies, and scope-change rationale.

## Branch and Worktree Strategy

- **Default:** One worktree and one branch for the whole epic. Each plan lands as a commit. The epic closes with one PR.
- **Exception:** If a plan is expected to take days, create a feature branch and PR for that plan, merging into the epic branch. The PR merge approval gate becomes the natural human checkpoint between plans.

## Blocked Plan Handling

If a plan is stuck below 8/10 and cannot be strengthened autonomously:

1. Stop.
2. Ask the human one focused question to resolve the ambiguity.
3. Do not proceed below 8/10.
4. Do not reduce scope without human consultation.
5. Update the roadmap item to `blocked` with the question and context.

## Scope Changes

The roadmap is a live look-ahead document. If implementation decisions change the forward path, the executing agent edits the roadmap inline and documents the change in `Handoff Notes`. Major structural changes (adding, removing, or reordering plans) should trigger a quick re-plan via `brainstorming` if the epic itself has shifted.

## Third-Party Overlay Changes

Add minimal `use_before: [handoff-gates]` metadata and a thin prose pointer at each handoff point.

- `adapters/codex/superpowers-plus/brainstorming/overlay.yaml` — at spec handoff.
- `adapters/codex/superpowers-plus/writing-plans/overlay.yaml` — at execution handoff.
- `adapters/codex/superpowers-plus/executing-plans/overlay.yaml` (new) or `finishing-a-development-branch` overlay — at completion handoff.

The prose pointer should be one line: *"Use `handoff-gates` <lane> before proceeding and report the final rating."*

## Skill Metadata Relationships

`handoff-gates`:

- `use_after: [brainstorming, writing-plans, executing-plans]`
- `use_before: [writing-plans, executing-plans, finishing-a-development-branch, requesting-code-review]`
- `related_skills: [risk-gates, writing-plans, executing-plans, working-with-epics]`

`working-with-epics`:

- `use_after: [brainstorming]`
- `use_before: [handoff-gates, executing-plans]`
- `use_with: [handoff-gates, writing-plans, executing-plans, subagent-driven-development]`
- `related_skills: [handoff-gates, writing-plans, executing-plans, brainstorming]`

`writing-plans` (via overlay):

- `use_before: [handoff-gates, executing-plans]`
- `related_skills: [handoff-gates, executing-plans, subagent-driven-development]`

`brainstorming` (via overlay):

- `use_before: [handoff-gates, writing-plans]`
- `related_skills: [handoff-gates, writing-plans, working-with-epics]`

`executing-plans` (via overlay):

- `use_after: [handoff-gates, writing-plans]`
- `use_before: [handoff-gates, finishing-a-development-branch, requesting-code-review]`
- `related_skills: [handoff-gates, writing-plans, subagent-driven-development]`

## Testing Approach

Follow the `writing-skills` test-driven skill authoring pattern: define pressure scenarios, run a subagent without the new skill to establish a failing baseline, then run with the skill to verify compliance.

Scenarios:

1. **Oversized request without `working-with-epics`:** The agent attempts one giant plan or stalls.
2. **With `working-with-epics`:** The agent writes a roadmap, rates each plan, executes sequentially, and updates the roadmap.
3. **Blocked plan:** The agent asks a focused question and does not proceed below 8/10.
4. **Scope change mid-epic:** The agent updates the roadmap and adjusts the forward path.

## Open Decisions

- Exact wording of the three lane-specific rubrics.
- Whether `completion-readiness` blocks the PR or triggers self-fixes before code review.
- Whether to create a new `executing-plans` overlay or place the completion gate in `finishing-a-development-branch`.
- Which Codex plugin pack owns the new first-party skills.

## Next Steps

1. Write `handoff-gates/SKILL.md` and `working-with-epics/SKILL.md` under `sources/first_party/skills/`.
2. Create `agents/openai.yaml` wrappers for Codex compatibility.
3. Update the relevant `adapters/codex/superpowers-plus/` overlays.
4. Add an `assets/authority/CITATIONS.md` for clean-room synthesis.
5. Run the marketplace rebuild and verify projections.
6. Run pressure scenarios to confirm the skills guide behavior.
