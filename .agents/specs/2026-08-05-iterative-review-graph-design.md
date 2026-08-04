# Spec: Iterative review as a graph

## Problem

The current `iterative-review` skill is a numbered list of rounds. It does not encode:

- Why we move from one step to the next.
- What to do when a fix introduces a new issue in a different concern area.
- Which lens should re-review which fix.
- Where a finding was actually caught.

As a result, a critical finding can surface late (Round 3 or later), either because an earlier round missed it or because a sloppy fix created it. The orchestrator has no explicit structure to route the work back to the right place.

## Goals

1. **Fast catch:** Deterministic `tools/review_preflight.py` catches pattern classes before any subagent is dispatched.
2. **Early catch:** The orchestrator's `orchestrator-predict` step applies the lens profiles as a checklist before lens dispatch, fixing predictable issues immediately.
3. **No sloppy fixes:** Every fix passes through `re-preflight` and a conditional `regression-scan` so a fix that creates a new issue is caught before `reviewer-strong` final review.
4. **Transparent loop:** The graph is the canonical control flow; every finding records the node that discovered it and the node that resolved it.
5. **Evidence of improvement:** `review-metrics.json` reports findings by node, rounds per finding, and regressions, so we can tune the process.

## Design

### Review state graph

The graph is a directed control-flow graph. Each node is a step; each edge is a condition. The orchestrator follows the graph and logs state.

**Nodes**

| Node | Actor | Purpose |
|---|---|---|
| `setup` | orchestrator | Prepare workspace, diff, PR context, `scan_findings`. |
| `preflight` | `tools/run.py ci --check` | Deterministic pattern checks. |
| `fast-fix` | orchestrator | Fix a preflight finding. |
| `scope-honesty` | orchestrator | Compare diff to plan/spec/PR. Fix drift. |
| `orchestrator-predict` | orchestrator | Apply each relevant `reviewer-*.md` checklist to the diff; record uncertain items. |
| `lens-dispatch` | parallel subagents | Run `reviewer-security`, `reviewer-skills`, `reviewer-marketplace`, etc. with the prediction log as input. |
| `strong-review` | `reviewer-strong` | Whole-branch pass combining lens logs; find gaps, contradictions, design issues. |
| `metrics-track` | orchestrator | Record where a finding was discovered, the round number, and later where it resolved. No hard budget cap. |
| `finding-fix` | orchestrator + implementer subagent | Resolve one finding; commit. |
| `re-preflight` | `tools/run.py ci --check` on the post-fix range | Ensure the fix did not introduce deterministic issues. |
| `targeted-re-review` | `reviewer-fast` or full lens | Confirm the original finding is resolved. |
| `regression-scan` | `reviewer-strong` on the touched area | Check for new issues caused by the fix. Conditional on non-trivial fixes. |
| `ready` | orchestrator | Final `ci --check` and wait for consumer remote CI; mark PR ready. |
| `blocked` | orchestrator | Human escalation when the orchestrator cannot resolve a contested or load-bearing finding. |

**Conditional edges**

- `orchestrator-predict` always routes to `lens-dispatch`. A clean prediction is not a substitute for lens review.
- `strong-review` routes to `metrics-track` when findings exist; to `ready` when clean.
- `re-preflight` routes back to `fast-fix` on red, forward to `targeted-re-review` on green.
- `targeted-re-review` routes to `regression-scan` for non-trivial fixes (multi-file, generated surfaces, security/tooling boundary) or `strong-review` for trivial fixes.
- `regression-scan` routes back to `metrics-track` if a new issue appears; to `strong-review` if clean.
- `strong-review` after a re-review can route to `ready` (clean), `metrics-track` (new/remaining findings), or `blocked` (contested load-bearing finding).

### `review-state-graph.md` reference

A new reference file in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md` contains:

- A Mermaid graph.
- The node table above.
- An edge table with exact conditions.
- A `review-metrics.json` schema.
- A `review-log-orchestrator-prediction.md` template.

`iterative-review/SKILL.md` becomes a walkthrough of the graph, not a numbered round list.

### Implementer self-review

`implementing.md` and `subagent-driven-development/SKILL.md` are updated so the implementer must read the relevant `reviewer-*.md` profile(s) before marking a task complete. The goal is to make `lens-dispatch` mechanical verification, not discovery.

### Lens profile checklists

Each `reviewer-*.md` profile receives an explicit `## Checklist` section that the orchestrator can use during `orchestrator-predict` and that the lens subagent can use mechanically.

### Metrics

Every finding in `review-metrics.json` records:

- `finding_id`
- `lens`
- `discovered_at_node`
- `discovered_at_round`
- `resolved_at_node`
- `resolved_at_round`
- `regression_of` (if a fix caused it)
- `severity`

Aggregates are reported at the end of a run.

### No hard budget cap

The graph allows as many rounds as a particular PR needs. `metrics-track` records the counts. If the same pattern of many rounds repeats across PRs, the metrics reveal which node to improve rather than blocking a single PR.

## Files to change

- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md` (rewrite around the graph)
- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md` (new)
- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json` (new)
- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-log-orchestrator-prediction.md` (new)
- `.agents/runbooks/pr.md` (use the graph)
- `.agents/runbooks/implementing.md` (implementer self-review)
- `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md` (implementer self-review)
- `.agents/agents/reviewer-skills.md` and source profile (checklist + regression input)
- `.agents/agents/reviewer-security.md` and source profile (checklist + regression input)
- `.agents/agents/reviewer-marketplace.md` (checklist + regression input)
- `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-strong.md` (checklist + regression input)
- `AGENTS.md` or runbook reference to the metrics file

## Acceptance

- `py -3 tools/run.py ci --check` passes.
- `iterative-review/SKILL.md` no longer contains a numbered round list.
- `review-state-graph.md` contains a Mermaid graph and edge table.
- `reviewer-*.md` profiles contain a `## Checklist` section.
- A sample `review-metrics.json` schema is present in references.
