# Worker Playbooks

This page adapts the reusable Superpowers workflow core into first-party worker habits for `agent-asset-marketplace`.

Use it when you are planning, implementing, debugging, reviewing, or closing out repo work and you want a compact reminder of the default loop.

## Source And Posture

- Vendor mirror: `sources/vendor/obra/superpowers/v5.1.0/`
- Upstream project: `obra/superpowers`
- Upstream tag and commit: `v5.1.0` / `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
- License: MIT
- Attribution stays with Jesse Vincent and the upstream repository.
- This page is a first-party conceptual adaptation. It does not copy harness-specific bootstrap prose wholesale.

## Default Worker Loop

1. Understand the request and the current repo state.
2. Shape the work into a small, explicit plan.
3. Make the smallest useful change.
4. Verify the change against the current source of truth.
5. Record proof before claiming completion.
6. Close the branch cleanly and hand off durable evidence.

## Playbook Habits

### Brainstorming

Use when scope, route, or constraints are still unclear.

- State the goal in plain language.
- List assumptions and non-goals early.
- Compare a few viable approaches before choosing one.
- Prefer the smallest safe path that still satisfies the issue.

### Writing Plans

Use when the task is understood but needs decomposition.

- Name the files that will change.
- Break work into short, ordered steps.
- Include validation, not just implementation.
- Call out open questions, risks, and checkpoints.

### Executing Plans

Use when a written plan exists.

- Follow the steps in order.
- Keep the plan current as work lands.
- Stop when a blocker appears instead of guessing.
- Verify each checkpoint before moving on.

### Test-Driven Development

Use when changing behavior.

- Write the failing test first.
- Watch it fail for the reason you expected.
- Implement the smallest change that makes it pass.
- Refactor only after the green state is real.

### Systematic Debugging

Use when something is broken or surprising.

- Reproduce the issue first.
- Read the error or unexpected output carefully.
- Check recent changes and isolate the failing layer.
- Fix the root cause, then re-run the original check.

### Verification Before Completion

Use right before claiming success.

- Run the command that proves the claim.
- Read the full output, not just the exit code.
- Do not call work done until the evidence is fresh.
- Prefer direct proof over confidence or memory.

### Using Git Worktrees

Use when isolation matters.

- Prefer an isolated workspace for feature work.
- Detect whether you are already in a worktree before creating another one.
- Keep branch creation and cleanup explicit.
- Fall back to the current checkout only when the environment requires it.

### Requesting Code Review

Use once a meaningful checkpoint is ready for another set of eyes.

- Ask for review on a stable change set.
- Provide the base SHA and the head SHA.
- Focus the reviewer on the work product, not the session history.
- Treat review as a checkpoint, not a substitute for verification.

### Receiving Code Review

Use when feedback comes back.

- Verify each comment against current source before acting.
- Accept factual corrections quickly.
- Push back when feedback is stale, incomplete, or technically wrong.
- Keep scope and authority separate from opinion.

### Finishing A Development Branch

Use when the work is done and the branch needs to be closed out.

- Verify the relevant tests and checks first.
- Confirm the current workspace shape before cleanup.
- Capture merge, PR, or keep-as-is proof explicitly.
- Leave the branch in a boring, reviewable state.

## Local Anchors

- Worker dispatch and Linear control plane: `gpt-skills/house-skills/worker-dispatch-linear/v1/worker-dispatch-linear-v1/SKILL.md`
- Base doctrine for source and tool posture: `gpt-skills/house-skills/gpt-base-doctrine/v1/gpt-base-doctrine-v1/SKILL.md`
- Provenance note for this adaptation: `provenance/superpowers-workflow-core.md`
- Linear log for this issue: `MARK-35 Activity Log`

## Parking Lot

This playbook intentionally does not add multi-agent or subagent workflow support. That decision stays parked with `MARK-36`.
