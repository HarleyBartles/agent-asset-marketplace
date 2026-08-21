# Iterative Review Triage and Selection - Epic Roadmap

Source spec: derived from the PR #9 `iterative-review` lens-dispatch/triage review and follow-up discussion.

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|-------|--------|-----------|--------|----|--------|-------|
| 1 | Pre-lens dispatch shape and cheap-lens hygiene | completed | [Plan 1](2026-08-15-plan-1-pre-lens-dispatch-shape.md) | 4081e0f0 | #300 | 9/10 | Close out the previous `iterative-review-improvements` epic, pull `reviewer-fast` out of `lens-dispatch`, and stop `reviewer-security` matching every PR. |
| 2 | Generation-aware lens selection and diff slicing | blocked | - | - | - | - | Superseded by Plans 3 and 4 in the [Trustworthy Iterative Review roadmap](../iterative-review-trustworthy-green/roadmap.md), where generation handling is part of an explicit coverage obligation rather than a lens-skipping optimization. |
| 3 | Automated `lens-triage` and resolution routing | blocked | - | - | - | - | Superseded by Plans 3 and 4 in the [Trustworthy Iterative Review roadmap](../iterative-review-trustworthy-green/roadmap.md), which requires structured all-severity adjudication and evidence-backed dispositions. |

## Constraints

- All source edits live under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/`.
- Regenerate installed skills with `py -3 tools/run.py marketplace --apply`.
- `py -3 tools/run.py ci --check` must pass before claiming any plan complete.

## Handoff Notes

The 2026-08-21 review found that selection and triage cannot be safely improved in isolation because the graph lacks snapshot, coverage, evidence, and exact-SHA green invariants. Completed Plan 1 remains historical work. Pending Plans 2 and 3 move to the broader trustworthy-green epic linked above; do not write new implementation plans from this roadmap.
