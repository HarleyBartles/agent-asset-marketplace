---
name: requesting-code-review
description: Use when a change is ready for another review pass before merge or release.
---

# Requesting Code Review

Ask a reviewer to check the change with enough context to evaluate the work,
the requirements, and the verification you already ran. Keep the request tight
and specific so the reviewer can focus on correctness, missing tests, and edge
cases.

## Quick Pattern

1. Summarize what changed.
2. State what the change is supposed to do.
3. Include the verification you already ran.
4. Ask for the specific risks you want checked.
5. Fix the findings before you move on.

## Guardrails

- Review before merge, not after a surprise lands.
- Do not bury the important context in a long history dump.
- Treat actionable findings as real work, not noise.

