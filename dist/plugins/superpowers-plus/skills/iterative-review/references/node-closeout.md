# node-closeout

## Purpose

Apply the repository's planning-artifact custody policy during PR closeout.

## Inputs

- PR body and linked issues
- Plan and specification paths named in the PR body or repository-declared planning guidance
- Related roadmaps and other artifacts that establish scope
- Repository standards subscription and readable certification, when available
- Branch working tree and base

## Recipe

1. Identify the planning artifacts in scope from the PR, linked issues, and repository-declared planning locations. Follow links that clarify each artifact's scope.
2. Read the repository's applicable custody policy. Apply `completed-artifact-custody` only when the repository adopted it or a human requested it; otherwise follow local policy.
3. For each artifact, classify its whole scope as complete, active or mixed, explicitly abandoned, or uncertain. Use checkboxes, markers, state labels, and PR metadata as clues, then compare them with implementation, tests, delivery records, linked issues, and future obligations.
4. Promote enduring decisions before removing any artifact. Preserve active scope, including parent roadmaps with future work. A completed child plan may be retired independently if its own work is complete.
5. When the current PR completes the work and the repository adopted the two-slice standard, keep its governing artifacts in the PR through merge. If this is a successor slice, retire only eligible artifacts present in its current `main` base, in the first substantive commit of that slice. Keep branch-only artifacts through their completing PR. Follow local policy when the standard is not adopted.
6. Remove stale links or generated indexes in the same retirement change. Run the consumer's declared validation and regeneration commands when a retirement is required.
7. Verify the final tracked state and the PR's canonical CI gate before reporting closeout.

## Outputs

- Artifact-by-artifact custody decisions with evidence and the applicable repository policy
- Eligible successor-slice artifacts retired in the correct commit, or completing-slice artifacts retained through merge
- Durable decisions promoted and stale links updated where removal occurred

## Next check

py -3 <runtime-skill-path-for-iterative-review>/scripts/next_node.py --metrics \<scratch_dir>/review-metrics.json
