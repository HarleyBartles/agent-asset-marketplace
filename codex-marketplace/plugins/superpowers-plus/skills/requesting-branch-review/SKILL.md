---
name: requesting-branch-review
description: Use when an agent should dispatch a whole-branch diff review for a
  specific branch and worktree against main.
metadata:
  source-id: requesting-branch-review
  source-path: sources/first_party/skills/requesting-branch-review/SKILL.md
  provenance-name: Requesting Branch Review first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when an agent should dispatch a whole-branch diff review for a specific
    branch and worktree against main.
  use_when:
  - Use when an agent should dispatch a whole-branch diff review for a specific branch.
  - Use when the user asks to review a branch diff against main and the branch or worktree is not the current one.
  - Use when the main agent can gather the target branch and worktree and then launch the branch-reviewer subagent.
  do_not_use_when:
  - Do not use when the target branch has no commits ahead of <base>.
  - Do not use when only a single file or small diff needs review; use a file-level reviewer instead.
  related_skills:
  - selecting-a-subagent
  - subagent-driven-development
  - finishing-a-development-branch
  - requesting-code-review
license: MIT
triggers:
- user
- model
---

# Requesting Branch Review

Use the `branch-reviewer` subagent to review a branch diff for a specific branch and worktree.

1. Determine the target branch and worktree:
   - If the user provided them, use those values.
   - Otherwise, default to the current git branch and current working directory.
   - If any value is ambiguous or missing, ask the user before proceeding.
2. Verify the branch exists: if you are not already in `<worktree>`, run `cd "<worktree>"`. Then run `git rev-parse --verify <branch>` (or `git rev-parse --verify refs/heads/<branch>`). If it does not exist, stop and report.
3. Verify the worktree exists: check that `<worktree>` is a directory and contains a `.git` directory or file. If it does not exist, stop and report.
4. Determine the base ref: if you are not already in `<worktree>`, run `cd "<worktree>"`. In the worktree, run `git rev-parse --verify main` and, if that fails, `git rev-parse --verify origin/main`. Use the first one that succeeds as `<base>`.
5. Choose the `branch-reviewer` subagent profile, preferring a branch-local one over the bundled generic profile:
   1. Search the worktree for a branch-local `branch-reviewer` profile. Repo-local profiles may be prefixed with the repository's canonical skill local prefix (e.g. `rooms-branch-reviewer.md`, `mark-branch-reviewer.md`) or be the unprefixed `branch-reviewer.md`. Search these directories in this order:
      - `<worktree>/.devin/agents/`
      - `<worktree>/.agents/agents/`
   2. In each directory, list files matching `*branch-reviewer.md`. Prefer a prefixed file (`<prefix>-branch-reviewer.md`) over the unprefixed `branch-reviewer.md`; if the repo's local prefix is known, prefer that prefix. The first matching file found is the branch-local profile.
   3. If you find a branch-local profile:
      - Ensure the global agents directory exists: `mkdir -p ~/.config/devin/agents` (macOS/Linux) or `New-Item -ItemType Directory -Path "$env:APPDATA\devin\agents" -Force` (Windows).
      - If the global `branch-reviewer.md` does not exist, or is byte-identical to the branch-local one, copy the branch-local profile to `~/.config/devin/agents/branch-reviewer.md` (macOS/Linux) or `%APPDATA%\devin\agents\branch-reviewer.md` (Windows).
      - If the global `branch-reviewer.md` exists and differs from the branch-local one, warn that the global profile will be overwritten and ask the user to confirm before copying. Do not overwrite a user-customized global profile silently.
   4. If no branch-local profile exists:
      - Ensure the global agents directory exists as above.
      - If the global `branch-reviewer.md` does not exist, or differs from the bundled generic `assets/branch-reviewer.md`, install or update it at the same global path.
6. Dispatch the subagent:

```
run_subagent profile: branch-reviewer
  title: "Review <branch> vs <base>"
  task: "Review the diff of branch <branch> against <base> in the worktree at <worktree> for correctness, style, consistency, and risk. If the subagent is not already in that worktree, run `cd <worktree>` before running any git commands. Use `git diff --no-color <base>...<branch>` to obtain the diff. Cite specific files and line numbers. Do not modify files."
```

7. Report the findings returned by the subagent.
