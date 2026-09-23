# GPT-6 Subagent Routing and Canonical Worktree Creation Plan

> **For agentic workers:** Use `executing-plans` inline. Keep RED/GREEN checks cheap and observable.

**Goal:** Route Codex subagents through the live GPT-6 family, require review dispatches to consult the selector, and make the bundled worktree script the required creation path.

**State:** completed-awaiting-retirement

**Execution Strategy:** Inline implementation in this worktree, followed by focused validation, the tracked hook, and a draft PR.

## Scope and constraints

- Edit canonical `codex-marketplace/plugins/superpowers-plus/skills/` source; regenerate marketplace and installed projections. Do not hand-edit generated copies.
- Restrict model changes to Codex MultiAgentV2. Leave Devin Desktop, generic, and Codex V1 routing unchanged.
- `requesting-code-review` describes the review need and consults `selecting-a-subagent` before every dispatch it owns. It does not prescribe `reviewer-strong`, `general-purpose`, or any model.
- GPT-6 Sol and Luna are normal Codex V2 routes. Astra is exceptional for highly complex integration beyond Sol and never above `low`. GPT-5.6 has no active V2 default route.
- The worktree skill requires its bundled `new_worktree.py` for creation; remove the generic native-tool escape hatch. Keep existing-worktree detection and verification.
- Tests belong under each changed skill's `tests/`; no task-size model matrix or synthetic performance claim.

## Task 1: Cheap RED evidence

1. Add focused maintainer checks for three observable contracts: review skill defers dispatch route to selector; V2 profile supplies a GPT-6 route from live inventory and rejects Astra above low; worktree skill requires the bundled script instead of an arbitrary native creator.
2. Run them against current canonical text and record the intended failures. They check decision instructions and route invariants, not model capability.

## Task 2: Minimal GREEN edits

1. Update `requesting-code-review/SKILL.md` and its template only where needed to remove profile and `general-purpose` dispatch instructions, adding selector consultation before each dispatch.
2. Update `selecting-a-subagent/references/codex-multi-agent-v2-profile.md` for GPT-6 and the Astra low ceiling. Reconcile only Codex-specific stale shared-policy language if it contradicts V2.
3. Update `using-git-worktrees/SKILL.md` to require `scripts/new_worktree.py --check` then `--apply` for creation. State that an arbitrary native creator may violate the consumer location policy.
4. Run focused GREEN checks. Review the diff for unintended Devin, generic, or V1 changes.

## Task 3: Generate, validate, publish

1. Run `py -3 tools/run.py marketplace --apply`, `installed-skills --apply`, `repo-index --apply`, and `mesh --apply` as needed. Run focused tests again.
2. Self-review and run the tracked pre-commit hook on the staged tree. Mark this plan `completed-awaiting-retirement` once agent-owned work is done, retaining it through the PR, then commit.
3. Push `codex/gpt6-subagent-routing`, open a draft PR into `main`, attach it to this task, and verify the remote head and PR state.

## Review focus

- No review skill dispatch path bypasses the selector.
- Codex V2 routes choose only exposed GPT-6 models; Astra is at most low and exceptional.
- Devin Desktop, generic, and Codex V1 routes remain unchanged.
- Worktree creation follows the canonical sibling root through the bundled script.
