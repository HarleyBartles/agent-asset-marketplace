# Worktree default branch

Status: active.

Goal: Create new worktrees from the latest tip of origin's advertised default branch, including Gitflow repositories whose default is develop, while preserving explicit --base-ref overrides and the existing HEAD fallback when origin is unavailable.

Execution strategy: Implement inline in the canonical isolated worktree. Keep helper behavior, bundled documentation, and generated plugin copies aligned.

- [ ] Prove remote-default selection and fresh-tip behavior with real Git repositories whose local origin/HEAD is absent or stale and whose main branch has different content.
- [ ] Resolve origin's advertised HEAD, fetch that branch explicitly, and preserve explicit base refs and unavailable-origin fallback.
- [ ] Run focused helper tests, regenerate marketplace outputs, and obtain independent review.
- [ ] Complete the plan, commit through the tracked hook, and publish a Draft PR with verified head identity.
