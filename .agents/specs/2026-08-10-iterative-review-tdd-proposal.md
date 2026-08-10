# Iterative review - TDD and fast-fix churn reduction (proposal)

**Status:** Implemented in Plan 4 / PR #290.
**Source:** Design discussion after Plan 3 final branch review of PR #289.

## Goal

Reduce the "fast to fix" and "reduce regressions" cycle time in iterative review by making test-driven development the default for implementation work and by tightening the fast-fix/re-run loop so fixes are re-checked at the originating lens instead of always triggering a full final branch review.

## Motivation

The Plan 3 implementation of `select_lenses.py`, `record_orchestrator_log.py`, `next_node.py --non-trivial`, and the orchestrator self-review template went through several full final branch review cycles. Many of the late findings (regex over-capture, glob matching, BOM-tolerant state reads, stale `non_trivial_fix` routing) would have been caught earlier or prevented entirely if the implementation work were required to prove the bug with a failing test before landing the fix. TDD also leaves behind regression tests, which directly supports the "reduce regressions" metric.

## Proposed scope

### 1. TDD in implementer profiles

Update the repo's global `implementer` and `implementer-strong` profiles (and the `subagent-driven-development` skill) to mandate TDD for blocking/important work:

- Before editing code, write or identify a failing test that reproduces the issue.
- Implement the minimal change to make the test pass.
- Run the test and the canonical `py -3 tools/run.py ci --check` before claiming the fix.
- Add the new test to the repo's permanent test suite.
- For trivial one-liners, allow a fast fix, but still require the existing test suite to pass.

### 2. TDD in the iterative-review graph

Update `fast-fix` and `finding-fix` node recipes so the orchestrator must invoke the `test-driven-development` skill when the finding is important or `non_trivial_fix` is set. A fix is not considered resolved until the orchestrator can point to a failing-then-passing test (or an existing regression test) that covers the changed behavior.

### 3. Implementer prompt templates

Add TDD-aware prompt templates for the `iterative-review` implementer lane (or to the shared `selecting-a-subagent` assets). The template should include a RED/GREEN/REFACTOR preamble and require the implementer to return both the change and the test that proves it.

### 4. Fast re-run over full final review

Document and enforce that a fix should be followed by:

1. A failing test (RED).
2. The minimal fix (GREEN).
3. Targeted tests + `py -3 tools/run.py ci --check`.
4. Re-running only the originating lens (or `reviewer-fixes` for that lens).
5. A full `final-strong` review only when the fix touches surfaces outside the originating lens's scope.

## Non-goals

- Do not change the core graph topology.
- Do not remove `final-strong`; keep it as the final gate before merge.
- Do not mandate TDD for trivial, obvious fixes.

## Validation sketch

- `py -3 tools/run.py ci --check` passes after the changes.
- New implementer profiles carry a TDD preamble that `subagent-driven-development` respects.
- `review-metrics.json` tracks `fast_fix_cycles` and `regressions_introduced`.
