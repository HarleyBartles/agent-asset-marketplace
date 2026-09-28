# Non-repo locations policy

This policy binds this repo's canonical off-repo locations. Canonical layout, sanitization, and cleanup rules live in `repo-standards` `references/scratch-workspace-policy.md` and `repo-worker-base` `references/worktree-and-branch-policy.md`; `subagent-workspace` resolves paths inside the layout.

## Locations

- Isolated branch worktrees: `../_agent-worktrees/<repo-name>/<branch-name>/`
- Scratch (temporary scripts, commit-message files, inspection scripts, debug output): `../_agent-scratch/<repo-name>/<branch>/<plan-basename>/`
- Completed-artifact convenience copies: `../_agent-scratch/<repo-name>/completed/<artifact-type>/`

Do not store canonical source, generated outputs, or long-lived repo assets in either location.

## Subagent profile runtime staging

Portable subagent profiles shipped with the `selecting-a-subagent` skill are installed to the Devin Desktop user-global agents directory:

```
py -3 .agents/skills/selecting-a-subagent/scripts/install_profiles.py --apply
```

The runtime searches the user-global directory first, so portable profiles do not need `runtime-agents` staging and should not be placed in `.agents/agents/`.

Use `runtime-agents` only for repo-local `.agents/agents/*.md` profiles (e.g. `reviewer-marketplace.md`). The Devin runtime resolves profiles against the `.agents/agents/` directory of the main checkout (the IDE's `cwd`), not a linked worktree. When working in a feature branch that adds or changes repo-local profiles, stage them into the main checkout uncommitted so the runtime can see them:

```
py -3 tools/run.py runtime-agents --apply --allow-shared-checkout
```

These are local runtime staging copies only. Do not commit them to `main`. Restart the IDE after applying so the runtime picks up the new profiles.
