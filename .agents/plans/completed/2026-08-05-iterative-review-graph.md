# Plan: Iterative review graph

## Spec

`.agents/specs/completed/2026-08-05-iterative-review-graph-design.md`

## Goal

Replace the `iterative-review` round list with a state graph that routes the orchestrator through preflight, prediction, lens review, strong review, fix, re-preflight, targeted re-review, and conditional regression-scan. Record metrics for every finding. Update implementer and PR runbooks so the code is written to pass the lens profiles before review starts.

## Tasks

### 1. Create `review-state-graph.md` reference

**Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md`

**Contents:**

- Mermaid graph of all nodes and edges.
- Node table with actor, purpose, and exit-edge conditions.
- Edge table with source, target, and condition.
- `review-metrics.json` schema.
- `review-log-orchestrator-prediction.md` template.

**Acceptance:**
- No numbered "Round N" procedure.
- All edges have a stated condition.

### 2. Rewrite `iterative-review/SKILL.md`

**Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

**Contents:**

- Overview of the graph.
- How to read `review-state-graph.md`.
- Step-by-step walkthrough of the graph as a control flow, not a round list.
- Instructions for `orchestrator-predict` to apply each `reviewer-*.md` `## Checklist`.
- Instructions for `lens-dispatch` to use the prediction log as input.
- Instructions for `regression-scan` and when it is required.
- Instructions for recording `review-metrics.json` at every `metrics-track`.
- Exit to `blocked` only for human escalation.

**Acceptance:**
- No "Round 0" through "Round 4" text.
- Contains a reference to `review-state-graph.md`.

### 3. Add metrics and log templates

**Modify:**
- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json`
- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-log-orchestrator-prediction.md`

**Contents:**

- JSON schema for `review-metrics.json`.
- Markdown template for the orchestrator prediction log.

**Acceptance:**
- `review-metrics.json` tracks `findings_by_node`, `rounds_per_finding`, `regressions`, `total_rounds`, `total_reviewer_subagent_dispatches`, `devin_auto_review_invocations`.

### 4. Update `reviewer-*.md` profiles with explicit checklists

**Modify:**
- `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-skills.md`
- `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-security.md`
- `.agents/agents/reviewer-marketplace.md`
- `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-strong.md`

**Contents:**

- Add a `## Checklist` section that mirrors the current `## Procedure` checks.
- Add an `## Inputs` note for `regression-scan` mode (`<regression_diff_path>` optional; when present, the reviewer scans only the fix diff and immediate surrounding area).

**Acceptance:**
- Each profile has a checklist that the orchestrator can mechanically run during `orchestrator-predict`.
- Each profile supports a narrow `regression-scan` input.

### 5. Update `pr.md`

**Modify:** `.agents/runbooks/pr.md`

**Contents:**

- Replace the numbered pre-emptive review procedure with a reference to `iterative-review` and `review-state-graph.md`.
- Emphasize that the orchestrator must not dispatch reviewers until `orchestrator-predict` is recorded.
- Keep the remote-CI wait step.

**Acceptance:**
- `pr.md` points at the graph, not a round list.

### 6. Update `implementing.md` and `subagent-driven-development`

**Modify:**
- `.agents/runbooks/implementing.md`
- `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md`

**Contents:**

- Implementer must read the relevant `reviewer-*.md` profile(s) and run the `## Checklist` against their own diff before marking a task complete.
- Implementer prompt: "Write the code as if it has already been reviewed by the relevant lens profiles."

**Acceptance:**
- Implementer self-review is a pre-condition for handoff.

### 7. Regenerate installed skills and marketplace

**Run:**
- `py -3 tools/run.py marketplace --apply`
- `py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply`
- `py -3 tools/run.py mesh --apply`

**Acceptance:**
- Installed copies of `iterative-review/SKILL.md` and `subagent-driven-development/SKILL.md` match source.
- `.agents/agents/reviewer-*.md` match source.

### 8. Validation and publication

**Run:**
- `py -3 tools/run.py ci --check`
- Fix any findings.
- Commit with a clear message.
- Push `feat/review-iterative-graph`.
- Open a draft PR and update the body.
- Wait for `marketplace-validation` to pass.

**Acceptance:**
- `py -3 tools/run.py ci --check` passes locally.
- GitHub `marketplace-validation` passes.

## Completion

- [x] Task 1: `review-state-graph.md` reference
- [x] Task 2: `iterative-review/SKILL.md` graph rewrite
- [x] Task 3: Metrics and log templates
- [x] Task 4: `reviewer-*.md` checklists and regression inputs
- [x] Task 5: `pr.md` graph reference
- [x] Task 6: Implementer self-review
- [x] Task 7: Regenerate installed surfaces
- [x] Task 8: Validation and publication
