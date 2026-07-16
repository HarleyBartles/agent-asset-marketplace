---
name: wild-bunch-worker-verification
description: Use when Wild Bunch-specific setup, difficulty, entropy, or seeded-world
  claims need falsification on top of generic worker verification. Use when reviewing
  or finishing Wild Bunch work that depends on project doctrine, or when a generic
  worker-verification pass needs Wild Bunch-specific context.
metadata:
  source-id: wild-bunch-worker-verification
  source-path: sources/first_party/skills/wild-bunch-worker-verification/SKILL.md
  provenance-name: Wild Bunch Worker Verification first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when Wild Bunch-specific setup, difficulty, entropy, or seeded-world
    claims need falsification on top of generic worker verification. Use when reviewing
    or finishing Wild Bunch work that depends on project doctrine, or when a generic
    worker-verification pass needs Wild Bunch-specific context.
  use_when:
  - Use when Wild Bunch-specific setup, difficulty, entropy, or seeded-world claims
    need falsification on top of generic worker verification. Use when reviewing or
    finishing Wild Bunch work that depends on project doctrine, or when a generic worker-verification
    pass needs Wild Bunch-specific context.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---

# Wild Bunch Worker Verification

Use this skill when finishing or reviewing Wild Bunch work that needs project-specific falsification beyond the generic `worker-verification` skill. Passing tests are not the same thing as issue-goal conformance.

## Workflow

1. Identify the issue, PR, branch, commit, changed files, validation evidence, and claimed completion state.
2. Compare the changed source against the current Wild Bunch issue goal and the live repo state.
3. If the task touches world setup, seed identity, difficulty, entropy, or random selection, read `wild-bunch-project-doctrine` before deciding the falsification pass.
4. Falsify likely misses before accepting any Wild Bunch-specific return.
5. Use generic `worker-verification` for branch, PR, commit, validation, and mainline proof.
6. For browser or UI work, require screenshot evidence or state why it is unavailable.
7. Do not claim landed or mainline state unless it is verified after merge.
8. If a PR changes variable gameplay outcomes or initial setup, verify difficulty, entropy, and seeded setup handling or an explicit deferral.

## Rules

- Worker reports, chat summaries, and issue comments are not source proof.
- Passing validation is necessary evidence, not issue-goal conformance by itself.
- A PR existing is not landed state.
- A merge claim is not mainline proof until main is checked after merge.
- Preserve uncertainty when a required source, issue, PR, or validation route is unavailable.
