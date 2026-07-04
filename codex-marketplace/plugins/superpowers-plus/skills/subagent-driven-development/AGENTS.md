Use this adapter surface to change projected Superpowers behavior without editing `sources/third_party/**`.

Prefer `overlay.yaml` line edits for projected text changes. Use `schema_version: 2` with explicit `edits` when a targeted line replacement can express the change. Do not replace whole files in the adapter when a bounded line edit is enough.

Keep third-party source custody immutable. If the projected plugin needs different wording, commands, or paths, declare the adapter delta here and regenerate the marketplace projection instead of editing the upstream snapshot.

For runtime script behavior, keep sibling Bash and PowerShell implementations together under `skills/subagent-driven-development/scripts/`. For review-package and task-brief behavior, the adapter should drive the projected outputs, including `sdd/<plan_name>/` placement.
