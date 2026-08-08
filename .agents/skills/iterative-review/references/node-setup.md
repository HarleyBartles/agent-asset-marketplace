# node-setup

## Purpose
Collect and normalize the off-repo review inputs for the draft PR.

## Inputs
- `<base>` and `<branch>` (or `<head_sha>`)
- `<pr_number>`
- Off-repo `<scratch_dir>` path from `sdd-workspace`
- Lens profiles and consumer preflight command

## Recipe
1. Determine `<base>` and `<branch>` for the draft PR.
2. Run `.agents/skills/subagent-workspace/scripts/sdd-workspace` (Bash) or `.agents/skills/subagent-workspace/scripts/sdd-workspace.ps1` (PowerShell) to resolve the off-repo workspace.
3. Create an `iterative-review-<pr_number>` subdirectory inside the scratch workspace.
4. Materialize inputs in that directory:
   - `<diff_path>` via `.agents/skills/subagent-workspace/scripts/review-package - <base> <branch> "$workspace/iterative-review-<pr_number>/review-<base7>..<head7>.diff"`
   - `<pr_description>` as a UTF-8 file
   - Optional `<issue_context>` as a UTF-8 file
   - `<scan_findings>` from the consumer's canonical preflight
5. Validate every input file is valid UTF-8 (no BOM).
6. Ensure `review-metrics.json` exists in `<scratch_dir>`. Do not overwrite it if `next_node.py` has already populated `current_node` and `previous_node`.

## Outputs
- `review-<base7>..<head7>.diff`
- `pr_description`
- Optional `issue_context`
- `scan_findings`
- Raw review input files
- `review-metrics.json` (ensure it exists; preserve any `current_node`/`previous_node` already written by `next_node.py`)

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
