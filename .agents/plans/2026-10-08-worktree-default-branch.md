# Worktree default branch

Status: completed-awaiting-retirement.

Goal: Create new worktrees from the latest tip of origin's advertised default branch, including Gitflow repositories whose default is develop, while preserving explicit --base-ref overrides and the existing HEAD fallback when origin is unavailable.

Execution strategy: Implement inline in the canonical isolated worktree. Keep helper behavior, bundled documentation, and generated plugin copies aligned.

- [x] Prove remote-default selection and fresh-tip behavior with real Git repositories whose local origin/HEAD is absent or stale and whose main branch has different content.
- [x] Resolve origin's advertised HEAD, fetch that branch explicitly, and preserve explicit base refs and unavailable-origin fallback.
- [x] Use a fully qualified remote-tracking ref to avoid local-ref ambiguity and document fetching during preview.
- [x] Run focused helper tests, regenerate marketplace outputs, and obtain independent review.
- [x] Retire the predecessor SemVer plan whose whole scope shipped in the current base, following repository artifact custody.
- [x] Prepare fully reviewed source and the completed plan for the repository's hooked commit and Draft PR publication route.

Publication follows the repository PR runbook: commit through the tracked hook, push the task branch, open a Draft PR, and verify its head identity. Keep this plan through the completing PR.
