# Non-repo locations policy

This policy covers canonical locations outside the repo tree that agents use
for isolated work and scratch artifacts.

## Worktrees

Isolated branch worktrees live in `../_agent-worktrees/<repo-name>/<date>-<branch-name>/`,
a sibling of the repo folder. Worktree payloads live entirely outside the repo
tree.

Rules:

- Use worktrees only for isolated branch checkouts and temporary local issue
  lanes.
- Do not store canonical source, generated outputs, or long-lived repo assets
  in worktrees.

## Scratch files

Scratch files (temporary scripts, commit message temp files, inspection
scripts, debug output) go in `../_agents-scratch/<branch-name>/`, not in the
repo tree. The scratch directory is a sibling of the repo folder.

Rules:

- Create a subfolder named after the worktree branch the scratch belongs to.
- Scratch contents are not durable. Do not put anything in scratch that needs
  to survive beyond the work it supports.
- Do not commit scratch files into the repo.
- Do not leave scratch files in the repo working tree. If a scratch file ends
  up in the repo tree, remove it before committing.
