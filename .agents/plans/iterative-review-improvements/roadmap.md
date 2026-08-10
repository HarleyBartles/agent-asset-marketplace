# Iterative review improvements — roadmap

Source spec: [`.agents/specs/completed/2026-08-09-iterative-review-improvements-design.md`](../../specs/completed/2026-08-09-iterative-review-improvements-design.md)

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|---|---|---|---|---|---|---|
| 1 | State/router split and record scripts | done | [Plan 1](../completed/iterative-review-improvements/2026-08-09-plan-1-state-router-split.md) | c1e59ac4 | #287 | 10/10 | Plan implemented; `iterative-review` dogfood reached `reviewer-strong: clean`. Ready to merge. |
| 2 | Ergonomic and reliability improvements | done | [Plan 2](../completed/iterative-review-improvements/2026-08-09-plan-2-ergonomic-improvements.md) | c0b2cd39 | #288 | — | Plan implemented; archived. |
| 3 | Lens dispatch, write-safety, and final polish | done | [Plan 3](../completed/iterative-review-improvements/2026-08-09-plan-3-lens-dispatch-and-polish.md) | df9a41b8 | #289 | 9/10 | `select_lenses.py`, self-review template, tests, docs, plus a no-hand-write contract for all scratch files (`review-state.json`, `*.jsonl`, `review-log-*.md`) and a script for orchestrator markdown logs |
| 4 | TDD and fast-fix churn reduction | in_progress | [Plan 4](2026-08-10-plan-4-tdd-fast-fix.md) | — | — | — | Enforce `test-driven-development` for implementers and orchestrators, add TDD to implementer profiles and subagent-driven-development prompts, and tighten the `finding-fix`/`reviewer-fixes`/`fast-fix` node recipes so fixes are proven by failing tests and re-run only the originating lens, not a full final branch review. |

## Constraints

- All work in canonical source: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`.
- Regenerate `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` with `py -3 tools/run.py installed-skills --apply` where needed.
- Each plan must pass `py -3 tools/run.py ci --check` before being considered complete.
- Each plan must be handed off through `handoff-gates` plan-readiness before execution.
