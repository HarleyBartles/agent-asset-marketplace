# node-closeout

## Purpose

Apply the repository's planning-artifact custody policy during PR closeout.

## Inputs

- PR body and linked issues
- Plan and specification paths named in the PR body or repository-declared planning guidance
- Related roadmaps and other artifacts that establish scope
- Repository standards subscription and readable certification
- Branch working tree and base

## Recipe

1. Identify the planning artifacts in scope from the PR, linked issues, and repository-declared planning locations. Follow links that clarify each artifact's scope.
2. Resolve the repository's immutable subscription revision and read its definition and readable certification. The standard ID alone does not establish which obligations are in force. If the repo has not adopted it or a human has not requested it, follow local policy. If adopted, route to `completing-planning-artifacts` and follow the pinned version; do not silently upgrade an older pin.
3. For each artifact, classify its whole scope as complete, active or mixed, explicitly abandoned, or uncertain. Use checkboxes, markers, state labels, and PR metadata as clues, then compare them with implementation, tests, delivery records, linked issues, and future obligations.
4. Promote enduring decisions before removing any artifact. Preserve active scope, including parent roadmaps with future work. A completed child plan may be retired independently if its own work is complete.
5. When the pinned definition requires two-slice custody, keep governing artifacts in the completing PR through merge. In a successor slice, retire only artifacts eligible under the pinned definition and certification, present in its current `main` base, in the first substantive commit of that slice. Keep branch-only artifacts through their completing PR. Follow local policy when the standard is not adopted.
6. Remove stale links or generated indexes in the same retirement change. Run the consumer's declared validation and regeneration commands when a retirement is required.
7. Verify the final tracked state and the PR's canonical CI gate before reporting closeout.

## Outputs

- Artifact-by-artifact custody decisions with evidence and the applicable repository policy
- Eligible successor-slice artifacts retired in the correct commit, or completing-slice artifacts retained through merge
- Durable decisions promoted and stale links updated where removal occurred

## Next check

py -3 <runtime-skill-path-for-iterative-review>/scripts/next_node.py --metrics \<scratch_dir>/review-metrics.json
