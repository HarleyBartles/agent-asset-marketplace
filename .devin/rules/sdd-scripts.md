---
description: "Subagent script selection"
trigger: glob
globs: "**/scripts/**"
---

Use the no-extension bash scripts by default when the environment has bash.
If bash is unavailable, use the sibling `*.ps1` script with the same basename.
For task-review diffs, pass the plan file to `review-package` so the output lands in `../_agent-scratch/<branch>/<plan_name>/`.
