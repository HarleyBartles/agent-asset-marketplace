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

The `branch-reviewer` subagent profile contains the full review procedure; this skill dispatches it.

1. If the global `branch-reviewer` subagent profile is not available, install `assets/branch-reviewer/AGENT.md` from this skill as `~/.config/devin/agents/branch-reviewer/AGENT.md`.
2. Dispatch the subagent:

```
run_subagent profile: branch-reviewer
  title: "Review branch diff"
```

3. Report the findings returned by the subagent.
