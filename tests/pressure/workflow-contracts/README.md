# MARK-373 workflow pressure campaign

The committed campaign definition and prompts are the reproducible input. Raw
Codex traces under `runs/` are local-only and ignored. Trials run from one
immutable evaluation head in fresh detached worktrees, with `read-only` or
`workspace-write` sandboxes only. External publication and connector writes
are never part of the baseline; publication scenarios stop at a local intent
boundary.

Scores are post-hoc Luna executor adjudications. They hash the exact local raw
files reviewed without publishing the event streams.
