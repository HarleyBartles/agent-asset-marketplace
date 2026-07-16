---
name: worker-verification
description: Use when verifying worker returns, PRs, commits, validation notes, and
  closure claims against issue goals, changed source, publication evidence, and verified
  mainline state before completion is accepted. Use when reviewing or finishing repo work,
  checking issue conformance, deciding Green/Amber/Red status, or preventing tests, reports,
  or worker summaries from being treated as proof.
metadata:
  source-id: worker-verification
  source-path: sources/first_party/skills/worker-verification/SKILL.md
  provenance-name: Worker Verification first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when verifying worker returns, PRs, commits, validation notes, and closure
    claims against issue goals, changed source, publication evidence, and verified mainline
    state before completion is accepted. Use when reviewing or finishing repo work, checking
    issue conformance, deciding Green/Amber/Red status, or preventing tests, reports, or
    worker summaries from being treated as proof.
  use_when:
  - Use when verifying worker returns, PRs, commits, validation notes, and closure claims
    against issue goals, changed source, publication evidence, and verified mainline state
    before completion is accepted. Use when reviewing or finishing repo work, checking issue
    conformance, deciding Green/Amber/Red status, or preventing tests, reports, or worker
    summaries from being treated as proof.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---

# Worker Verification

Use this skill when finishing or reviewing repo work. Passing tests are not the same thing as issue-goal conformance.

## Workflow

1. Identify the issue, PR, branch, commit, changed files, validation evidence, and claimed completion state.
2. Compare the changed source against the current issue goal.
3. Falsify likely misses before accepting the return.
4. Report validation commands run and their results.
5. Include branch, commit SHA, PR URL or number, and a concise touched-files summary.
6. For browser or UI work, require screenshot evidence or state why it is unavailable.
7. Do not claim landed or mainline state unless it is verified after merge.
8. If a task changes initial setup, seeded behavior, or entropy-sensitive behavior, verify those claims or note the explicit deferral.
9. When the task is Wild Bunch-specific, consult `wild-bunch-project-doctrine` for setup, difficulty, entropy, and seeded-world verification.

## Review gates

- For plan PR review, verify the Linear route-state block, repo-resident plan path, plan PR, scope split conditions, and validation expectations before any implementation claim.
- For execution PR review, verify the source diff against the current issue goal, the checked-off plan file, validation evidence, publication proof, and any touched-files summary.
- Keep plan PR review and execution PR review separate unless the issue explicitly combines them.

## Rules

- Worker reports, chat summaries, and issue comments are claims, not source proof.
- Passing validation is necessary evidence, not issue-goal conformance by itself.
- A PR existing is not landed state.
- A merge claim is not mainline proof until main is checked after merge.
- Preserve uncertainty when a required source, issue, PR, or validation route is unavailable.
