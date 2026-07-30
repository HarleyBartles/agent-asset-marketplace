---
name: review-branch-diff
description: Use when the current branch is complete and a whole-branch diff review
  against main is needed.
metadata:
  source-id: review-branch-diff
  source-path: sources/first_party/skills/review-branch-diff/SKILL.md
  provenance-name: Review Branch Diff first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when the current branch is complete and a whole-branch diff review against
    main is needed.
  use_when:
  - Use when a feature branch is complete and a whole-branch diff review is needed.
  - Use when the user asks to review the current branch diff against main.
  do_not_use_when:
  - Do not use when the current branch has no commits ahead of main.
  - Do not use when only a single file or small diff needs review; use a file-level
    reviewer instead.
  related_skills:
  - subagent-driven-development
  - finishing-a-development-branch
  - requesting-code-review
license: MIT
agent: branch-reviewer
triggers:
- user
- model
---

# Review Branch Diff

Review the current branch diff against `main` (or `origin/main`) for correctness, style, consistency, and risk.

1. Determine the base ref. Run `git rev-parse --verify main` and, if that fails, `git rev-parse --verify origin/main`. Use the first one that succeeds as `<base>`.
2. Run `git diff --no-color <base>...HEAD` to obtain the full diff.
3. If the diff is too large to review at once, run `git diff --stat <base>...HEAD`, then review changed files in batches using `git diff --no-color <base>...HEAD -- <path>`.
4. Identify correctness, style, consistency, and risk issues. Cite specific files and line numbers.
5. Do not modify files and do not run commands other than the git commands above.

**Fallback:** If the global `branch-reviewer` subagent profile is not available, an agent can install `assets/branch-reviewer/AGENT.md` from this skill as `~/.config/devin/agents/branch-reviewer/AGENT.md` before invoking this skill.
