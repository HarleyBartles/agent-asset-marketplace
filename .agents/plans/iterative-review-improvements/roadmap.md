# Iterative review improvements — roadmap

Source spec: [`.agents/specs/2026-08-09-iterative-review-improvements-design.md`](../../../specs/2026-08-09-iterative-review-improvements-design.md)

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|---|---|---|---|---|---|---|
| 1 | State/router split and record scripts | done | [Plan 1](2026-08-09-plan-1-state-router-split.md) | 9906f58c | #287 | 9/10 | Creates `review-state.json`, record scripts, `compile_metrics.py`, and refactors `next_node.py` |
| 2 | Ergonomic and reliability improvements | pending | [Plan 2](2026-08-09-plan-2-ergonomic-improvements.md) | — | — | — | `status`, `--resync`, artifact-aware `--propose`, schema cleanup, round cap, batching |
| 3 | Lens dispatch and final polish | pending | [Plan 3](2026-08-09-plan-3-lens-dispatch-and-polish.md) | — | — | — | `select_lenses.py`, self-review template, tests, docs |

## Constraints

- All work in canonical source: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`.
- Regenerate `.agents/skills/iterative-review/` with `py -3 tools/run.py installed-skills --apply` where needed.
- Each plan must pass `py -3 tools/run.py ci --check` before being considered complete.
- Each plan must be handed off through `handoff-gates` plan-readiness before execution.
