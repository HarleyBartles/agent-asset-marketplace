---
description: "Pull-request workflow and publication proof"
trigger: glob
globs:
  - "gh pr*"
  - "tools/run.py ci*"
  - ".agents/runbooks/pr.md"
---
## Scope

This rule fires when creating, updating, or publishing a pull request.

For the canonical doctrine, read root `AGENTS.md` `## Publication proof for repo work` and `## Draft PR policy`.

For the step-by-step runbook, read `.agents/runbooks/pr.md`.
