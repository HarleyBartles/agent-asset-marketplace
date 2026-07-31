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
   1. Search the worktree for a branch-local `branch-reviewer` profile in this order:
      - `<worktree>/.devin/agents/branch-reviewer/AGENT.md`
      - `<worktree>/.agents/agents/branch-reviewer/AGENT.md`
   2. If you find a branch-local profile, install or overwrite the global `branch-reviewer` profile by copying it to `~/.config/devin/agents/branch-reviewer/AGENT.md` (macOS/Linux) or `%APPDATA%\devin\agents\branch-reviewer\AGENT.md` (Windows).
   3. If no branch-local profile exists, ensure the bundled generic `assets/branch-reviewer/AGENT.md` is installed or updated at the same global path.
6. Dispatch the subagent:

```
run_subagent profile: branch-reviewer
  title: "Review <branch> vs <base>"
  task: "Review the diff of branch <branch> against <base> in the worktree at <worktree> for correctness, style, consistency, and risk. If the subagent is not already in that worktree, run `cd <worktree>` before running any git commands. Use `git diff --no-color <base>...<branch>` to obtain the diff. Cite specific files and line numbers. Do not modify files."
```

7. Report the findings returned by the subagent.
