# node-closeout

## Purpose

Remove completed planning artifacts before flipping the PR to ready.

## Inputs

- PR body, linked issues
- Plan and spec paths named in the PR body or repository-declared planning guidance
- Any related roadmaps or research files
- Branch working tree

## Recipe

1. Identify the plan and spec named in the PR body, linked issues, or the repository's declared planning locations.
2. Confirm the plan's work is complete and promote enduring decisions into ADRs or current doctrine.
3. Remove the completed plan, spec, roadmap, checkpoint, and related planning artifacts from Git. An optional copy may go to the consumer's central completed-artifact scratch store; it is disposable and not evidence.
4. Run the consumer's declared validation and marketplace regeneration helpers when applicable.
5. Run the consumer's canonical CI check; do not proceed if it fails.
6. Commit the completed-artifact removal normally.

## Outputs

- Completed planning artifacts absent from the tracked tree
- Durable decisions retained only in their current authority surfaces

## Next check

py -3 <runtime-skill-path-for-iterative-review>/scripts/next_node.py --metrics \<scratch_dir>/review-metrics.json
