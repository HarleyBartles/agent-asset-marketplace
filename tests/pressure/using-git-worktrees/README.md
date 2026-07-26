# using-git-worktrees pressure test

This pressure test evaluates whether the `using-git-worktrees` skill steers
agents away from force-deleting a locked worktree directory when a human
partner applies time/authority pressure.

## Files

- `prompts/red.md` — prompt for the agent reading the skill **without**
  the new warnings.
- `prompts/green.md` — prompt for the agent reading the skill **with**
  the new warnings.
- `results.md` — recorded RED/GREEN subagent responses and judgment.

## Status

One-shot controller-orchestrated run completed. Results show the skill's
locked-directory stop message and `## Red Flags` section prevent the agent
from falling back to `rm -rf` / `rmdir /s /q` / `Remove-Item -Recurse -Force`.
