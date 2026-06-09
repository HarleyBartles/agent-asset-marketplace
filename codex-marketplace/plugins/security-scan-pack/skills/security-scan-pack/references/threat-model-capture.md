# Threat Model Capture

Capture this before the scan is treated as complete.

## Minimum questions

- What path, repo, image, or SBOM is in scope?
- What is the expected exposure model?
- What data would be damaging to leak or mutate?
- Which paths are intentionally excluded?
- Which tool outputs are authoritative for this run?

## Minimum fields

- `scope`
- `assets`
- `trust_boundaries`
- `entry_points`
- `attacker_goals`
- `assumptions`
- `excluded_paths`
- `authoritative_outputs`

## Analysis rules

- Prefer concrete attacker goals over generic checklists.
- Separate reachable attack paths from merely present code patterns.
- Mark assumptions clearly when the environment or runtime model is unknown.
- If the threat model cannot be completed, record the blocker in the report.
