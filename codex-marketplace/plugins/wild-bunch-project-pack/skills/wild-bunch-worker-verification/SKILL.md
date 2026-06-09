---
name: wild-bunch-worker-verification
description: Verify Wild Bunch work against the issue goal, validation, and publication contract before claiming completion.
---

# Wild Bunch Worker Verification

## Overview

Use this skill when finishing or reviewing Wild Bunch work. Passing tests are
not the same thing as issue-goal conformance.

## Rules

- Compare changed source against the Linear and GitHub issue goal.
- Falsify likely misses instead of assuming the tests are enough.
- Include validation commands run and the result.
- Include branch, commit SHA, PR URL or number, and touched files summary.
- If browser or UI work is included, attach screenshot evidence or explain why
  it was unavailable.
- Do not claim landed or mainline state unless it is verified after merge.

## References

- [Verification checklist](references/verification-checklist.md)
