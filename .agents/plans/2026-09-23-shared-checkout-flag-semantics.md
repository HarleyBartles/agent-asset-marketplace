# Shared Checkout Flag Semantics Plan

> **For agentic workers:** Use `executing-plans` inline. Keep the RED/GREEN proof focused on checkout identity.

**Goal:** Make `--allow-shared-checkout` mean explicit intent to mutate the shared checkout, while linked worktrees need only `--apply`.

**State:** in-progress

**Execution Strategy:** Inline implementation in the canonical worktree; focused tests, generated projections, tracked hook, draft PR.

## Constraints

- Edit canonical plugin skills first, then regenerate installed projections. The consumer-authored `tools/shared_checkout.py` must match its repo-shape seed.
- A noninteractive or interactive `--apply` in the shared checkout requires `--allow-shared-checkout`, regardless of branch name. A linked worktree does not require or imply that flag.
- `--check` remains read-only and rejects a stray `--allow-shared-checkout` as it does today.
- Keep the `runtime-agents` exception distinct: it deliberately writes to the main checkout even when invoked from a worktree.

## Task 1: RED

Add focused tests that show shared checkout on a non-main branch and an interactive shared checkout currently bypass the flag. Show that a linked worktree is allowed without it. Run them and record intended failures.

## Task 2: GREEN

1. Fix the shared checkout guard in the canonical repo-shape seed and consumer copy. Remove the branch and prompt bypasses, preserving the warning when the flag is supplied.
2. Fix canonical `refreshing-installed-skills` and `generating-agent-mesh` instructions and the affected CLI help text. Remove unnecessary flag forwarding in the `new_worktree.py` fallback path. Keep command-bus worktree calls unchanged.
3. Run focused tests and inspect the diff for unintended mutation-authority changes.

## Task 3: Validate and publish

Regenerate marketplace, installed skills, index, and mesh. Run the focused tests and tracked pre-commit gate. Mark this plan `completed-awaiting-retirement`, retain it through the PR, push the branch, open a draft PR into `main`, and verify its head.

## Review focus

- Shared checkout requires the explicit flag on every branch and in every input mode.
- Linked worktrees do not need the flag.
- Skill prose, CLI help, worktree fallback, and executable guard agree.
