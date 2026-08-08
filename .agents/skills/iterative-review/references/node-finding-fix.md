# node-finding-fix

## Purpose
Verify and fix a single `blocking/important` lens finding.

## Inputs
- `original_finding` with exact text and severity
- `lens` name (e.g., `reviewer-security`)
- `lens_checklist` from the originating `reviewer-*.md`
- `diff_slice` of the full branch diff that the finding touches
- `fix_constraints` (what not to break, tests, consumer `ci --check`)
- `<pre-fix-sha>` and branch working tree

## Recipe
1. Use `receiving-code-review` to verify the finding.
2. Choose the fix path using the decision table below.

| Path | Use when... |
|---|---|
| `implementer` subagent | The change spans more than one file, is non-trivial logic, touches consumer preflights or tests in a non-obvious way, or the orchestrator is not confident making the change directly. |
| Inline/orchestrator | The change is one file / one conceptual edit, is docs/markdown/spec text, or the blast radius is minimal and the orchestrator can safely apply it. |

3. If `implementer` is chosen:
   - Create `<scratch_dir>/review-log-implementer-brief.md` from `review-log-implementer-brief-template.md`.
   - Fill in the `## Finding`, `## Fix instructions`, `## Out of scope`, `## Verification`, and `## Outputs` sections.
   - Dispatch an `implementer` subagent with the brief and the consumer's preflight command.
   - Verify the resulting `review-log-implementer-report.md` and the fix commit.
4. If inline/orchestrator is chosen:
   - Apply the minimal change to the affected file(s).
   - Run the consumer's preflight (e.g., `py -3 tools/run.py ci --check`) and confirm it passes.
5. Record the result in `rounds_per_finding` in `review-metrics.json`: increment `fix_round` for the finding.
6. Move to `re-preflight`.
7. Round escalation: use `implementer` for rounds 1-3; if a finding fails `reviewer-fixes` three times, escalate to `implementer-strong` for round 4; if it still fails, route to `blocked`.

## Outputs
- Updated `rounds_per_finding` in `review-metrics.json`: increment `fix_round` for the finding being fixed
- If `implementer` was used:
  - `review-log-implementer-brief.md`
  - `review-log-implementer-report.md`
  - Commit containing the fix
- If inline was used:
  - The updated file(s)
  - Updated `scan_findings`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --json --metrics <scratch_dir>/review-metrics.json
