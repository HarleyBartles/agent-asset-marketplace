# AGENTS.md

Scope: `.worktrees/`

This directory is repo-resident scratch space for isolated issue worktrees.
Keep the container itself in the repository so fresh checkouts create the
folder, but treat every nested worktree payload as disposable local state.

Rules:

- Keep `.worktrees/` present in fresh checkouts.
- Ignore every nested worktree directory and file under `.worktrees/` except
  this `AGENTS.md`.
- Use `.worktrees/` only for isolated branch checkouts and temporary local
  issue lanes.
- Do not store canonical source, generated outputs, or long-lived repo assets
  here.
