# Iterative Review Triage and Selection - Epic Roadmap

Source spec: derived from the PR #9 `iterative-review` lens-dispatch/triage review and follow-up discussion.

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|-------|--------|-----------|--------|----|--------|-------|
| 1 | Pre-lens dispatch shape and cheap-lens hygiene | ready | [Plan 1](2026-08-15-plan-1-pre-lens-dispatch-shape.md) | - | - | 8/10 | Close out the previous `iterative-review-improvements` epic, pull `reviewer-fast` out of `lens-dispatch`, and stop `reviewer-security` matching every PR. |
| 2 | Generation-aware lens selection and diff slicing | pending | - | - | - | - | Add a `generated-surface` classifier so `select_lenses.py` and `diff_slicer.py` do not dispatch deep reviewers for installed/marketplace/generated changes. |
| 3 | Automated `lens-triage` and resolution routing | pending | - | - | - | - | Add `triage_lenses.py`, a `not-actionable`/`generated` resolution bucket, and `lens-triage` routing that skips fix loops for generated surfaces. |

## Constraints

- All source edits live under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/`.
- Regenerate installed skills with `py -3 tools/run.py marketplace --apply`.
- `py -3 tools/run.py ci --check` must pass before claiming any plan complete.
