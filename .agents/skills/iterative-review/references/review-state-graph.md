# Iterative review state graph

This is the canonical control-flow graph for the `iterative-review` skill. The
orchestrator follows the graph from `setup` to `ready` or `blocked`, recording
state at every `metrics-track`.

Canonical node recipes live in `references/node-*.md` files (one per node in this
directory, named `node-<node>.md`), and the orchestrator uses `next_node.py` to
discover the current node. See `node-next-node.md` for the validation recipe.

## Mermaid graph

```mermaid
flowchart TD
    setup --> normalize-inputs --> preflight
    preflight -->|red| fast-fix --> preflight
    preflight -->|green| scope-honesty --> orchestrator-self-review
    orchestrator-self-review --> lens-dispatch
    lens-dispatch --> normalize-inputs --> lens-triage

    lens-triage -->|blocking / important| metrics-track
    lens-triage -->|trivial / deferred| final-strong
    lens-triage -->|contested / load-bearing| blocked
    lens-triage -->|clean| final-strong

    metrics-track --> finding-fix
    finding-fix --> re-preflight
    finding-fix -->|round cap exceeded| blocked
    re-preflight -->|red| fast-fix --> re-preflight
    re-preflight -->|green| reviewer-fixes

    reviewer-fixes -->|original fixed, no regressions| resolved-ledger
    reviewer-fixes -->|original not fixed| finding-fix
    reviewer-fixes -->|new issue, same lens/blast radius| metrics-track
    reviewer-fixes -->|non-trivial or cross-cutting| regression-scan

    regression-scan -->|clean| resolved-ledger
    regression-scan -->|new confirmed| metrics-track

    resolved-ledger -->|more open findings| finding-fix
    resolved-ledger -->|all findings resolved| final-strong
    final-strong -->|clean| closeout
    final-strong -->|findings| metrics-track
    final-strong -->|contested / load-bearing| blocked
    closeout --> ready
```

## Nodes

| Node | Actor | Recipe | Purpose |
|---|---|---|---|
| `setup` | orchestrator | [node-setup.md](node-setup.md) | Prepare the workspace, diff, PR context, and `scan_findings`. |
| `normalize-inputs` | orchestrator | [node-normalize-inputs.md](node-normalize-inputs.md) | Run `normalize_review_inputs.py --apply` on the scratch directory so every downstream file is plain UTF-8. |
| `preflight` | consumer CI preflight | [node-preflight.md](node-preflight.md) | Run deterministic pattern checks on the branch before any subagent. |
| `fast-fix` | orchestrator or implementer | [node-fast-fix.md](node-fast-fix.md) | Fix a deterministic preflight finding; trivial items the orchestrator can fix, mechanical items an `implementer`. |
| `scope-honesty` | orchestrator | [node-scope-honesty.md](node-scope-honesty.md) | Compare the diff to the plan, spec, PR body, and linked issues. Fix drift. |
| `orchestrator-self-review` | orchestrator | [node-orchestrator-self-review.md](node-orchestrator-self-review.md) | Orchestrator-only; no subagent dispatch. Apply each relevant `reviewer-*.md` profile's `## Checklist` to the diff, fix predictable items, and record uncertain items in `review-log-orchestrator-self-review.md`. |
| `lens-dispatch` | parallel subagents | [node-lens-dispatch.md](node-lens-dispatch.md) | Run the relevant lens reviewers with the prediction log as input. This node is mandatory; do not route around it because the orchestrator-self-review was clean. |
| `lens-triage` | orchestrator | [node-lens-triage.md](node-lens-triage.md) | Decide the fate of each lens finding: `blocking/important` findings enter the fast fix loop, `trivial/deferred` findings are left for `final-strong`, and `contested/load-bearing` findings are `blocked`. If no findings, proceed to `final-strong`. |
| `metrics-track` | orchestrator | [node-metrics-track.md](node-metrics-track.md) | Record the finding, the node that discovered it, the round number, the node where it resolves, and the `regression_class`. This node does not block. |
| `finding-fix` | `implementer` subagent | [node-finding-fix.md](node-finding-fix.md) | Resolve one finding with the lens's checklist and a concrete brief, then commit. |
| `re-preflight` | `tools/run.py ci --check` | [node-re-preflight.md](node-re-preflight.md) | Re-run the deterministic checks on the post-fix range. |
| `reviewer-fixes` | `reviewer-fixes` subagent | [node-reviewer-fixes.md](node-reviewer-fixes.md) | Cheap lens-aware re-review of the fix blast radius. Verifies the original finding and applies the originating lens's `## Checklist` to the changed files only. |
| `regression-scan` | `reviewer-strong` on the touched area | [node-regression-scan.md](node-regression-scan.md) | For non-trivial or cross-cutting fixes, confirm and classify any new issue the fix introduced. |
| `resolved-ledger` | orchestrator | [node-resolved-ledger.md](node-resolved-ledger.md) | Bookkeeping node that records resolutions via `record_resolution.py` into `resolutions.jsonl` and `compile_metrics.py` generates `review-metrics.json`. When the queue is empty, runs `resolved_ledger.py --apply` to produce `review-log-resolved-ledger.md` before `final-strong`. |
| `final-strong` | `reviewer-strong` | [node-final-strong.md](node-final-strong.md) | One whole-branch pass after all queued findings are resolved. Requires `review-log-resolved-ledger.md` and a clean `review-metrics.json`; `reviewer-strong` refuses if either is missing or shows unresolved `important`/`blocking` findings or regressions. Confirms no remaining gaps, contradictions, or design issues. |
| `closeout` | orchestrator | [node-closeout.md](node-closeout.md) | After `reviewer-strong: clean`, archive completed plans/specs/roadmaps per `.agents/runbooks/completing-plans.md` if the PR closes them. |
| `ready` | orchestrator | [node-ready.md](node-ready.md) | Final `ci --check`; flip the PR from draft to ready; wait for remote CI to pass. |
| `blocked` | orchestrator | [node-blocked.md](node-blocked.md) | Human escalation for contested or load-bearing findings the orchestrator cannot resolve. |

## Edges

| From | To | Condition |
|---|---|---|
| `setup` | `normalize-inputs` | Always. |
| `normalize-inputs` | `preflight` | Always. |
| `preflight` | `fast-fix` | Any deterministic finding from `review-preflight`. |
| `fast-fix` | `preflight` | Always; re-run preflight after the fix. |
| `preflight` | `scope-honesty` | `ci --check` passes. |
| `scope-honesty` | `orchestrator-self-review` | Drift corrected or no drift. |
| `orchestrator-self-review` | `lens-dispatch` | Always; the orchestrator's prediction is not a substitute for lens review. The only exception is a PR with zero changed files. |
| `lens-dispatch` | `normalize-inputs` | All lens logs are available. |
| `normalize-inputs` | `lens-triage` | UTF-8 backstop has run on the scratch directory. |
| `lens-triage` | `metrics-track` | `blocking/important` findings that need a fix before `final-strong`. |
| `lens-triage` | `final-strong` | No findings, `trivial/deferred` findings only, or no `blocking/important` findings left. |
| `lens-triage` | `blocked` | A finding is `contested`, `tool-blocked`, or `load-bearing` and the orchestrator cannot resolve it. |
| `metrics-track` | `finding-fix` | Always; choose the next finding to fix. |
| `finding-fix` | `re-preflight` | Fix is committed. |
| `finding-fix` | `blocked` | Round cap exceeded: `implementer-strong` on round 4 still fails. |
| `re-preflight` | `fast-fix` | A new deterministic issue appears. |
| `fast-fix` | `re-preflight` | Always; re-run preflight after the fix. |
| `re-preflight` | `reviewer-fixes` | `ci --check` passes. |
| `reviewer-fixes` | `resolved-ledger` | The original finding is fixed and `reviewer-fixes` is clean. |
| `reviewer-fixes` | `finding-fix` | The original finding is not fixed. |
| `reviewer-fixes` | `metrics-track` | `reviewer-fixes` finds a new same-lens/blast-radius issue. |
| `reviewer-fixes` | `regression-scan` | The fix is non-trivial (multi-file, generated surfaces, security/tooling boundary, or changes a public interface). |
| `regression-scan` | `resolved-ledger` | `reviewer-strong` on the touched area is clean. |
| `regression-scan` | `metrics-track` | `reviewer-strong` on the touched area confirms a new issue. |
| `resolved-ledger` | `finding-fix` | More findings remain in the queue. |
| `resolved-ledger` | `final-strong` | All findings are resolved. |
| `final-strong` | `closeout` | `reviewer-strong` reports `reviewer-strong: clean`. |
| `final-strong` | `metrics-track` | `reviewer-strong` reports findings. |
| `final-strong` | `blocked` | A finding is contested or load-bearing. |
| `closeout` | `ready` | Archives (if any) are committed and the local tree passes `ci --check`. |

## Round counting

A "round" is one complete traversal through `lens-dispatch` or `final-strong` that produces findings. `orchestrator-self-review`, `lens-triage`, `reviewer-fixes`, and `resolved-ledger` are not rounds because they are cheap or bookkeeping nodes. The first `lens-dispatch` is round 1. The first `final-strong` is round 2. A `regression-scan` or `final-strong` that confirms a new issue starts a new round at `metrics-track`.

## `review-metrics.json` schema

```json
{
  "pr": {
    "branch": "feat/example",
    "base": "main",
    "head_sha": "..."
  },
  "findings_by_node": {
    "preflight": 0,
    "orchestrator-self-review": 0,
    "lens-security": 0,
    "lens-skills": 0,
    "lens-marketplace": 0,
    "lens-plans": 0,
    "lens-mesh": 0,
    "lens-scripts": 0,
    "strong-review": 0,
    "regression-scan": 0
  },
  "rounds_per_finding": [
    {
      "finding_id": "F1",
      "lens": "reviewer-skills",
      "discovered_at_node": "lens-dispatch",
      "discovered_at_round": 1,
      "resolved_at_node": "resolved-ledger",
      "resolved_at_round": 2,
      "severity": "important"
    }
  ],
  "regressions": [
    {
      "fix_for": "F1",
      "new_finding": "F2",
      "discovered_at_node": "regression-scan",
      "discovered_at_round": 2,
      "lens": "reviewer-security",
      "regression_class": "outside-blast-radius",
      "severity": "blocking"
    }
  ],
  "total_rounds": 2,
  "total_reviewer_subagent_dispatches": 4,
  "devin_auto_review_invocations": 1
}
```

## `review-log-orchestrator-self-review.md` template

Use the skeleton at `references/review-log-orchestrator-self-review-template.md`.
The orchestrator fills it into `review-log-orchestrator-self-review.md` in the
off-repo scratch. Use the filled log to record what the orchestrator could
predict and fix, and what it left for the lens reviewers.
