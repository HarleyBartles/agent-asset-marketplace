# Unslop Profile: repository

## Task trigger and scope

Use this profile when planning, implementing, reviewing, or preparing a pull request for repository changes in this Marketplace. Apply only the failure cues below that are relevant to the current work.

## Recurring failure pattern

Agents can mistake remembered, reported, generated, or convenient state for current repository or publication truth; make claims beyond the evidence available; or broaden a change beyond its approved scope. These failures make repository work hard to verify and can cause unsafe lifecycle decisions.

## Recognition cues

- A claim about a file, test, PR, issue, merge, generated projection, or published state is supported only by memory, a summary, an unverified report, or stale output.
- Distinct evidence owners are collapsed, such as treating a Linear plan as GitHub implementation proof or a generated projection as canonical source.
- A proposed cleanup, refactor, publication, or completion claim has no named source seam, validation result, or owning-system evidence.
- The change adds adjacent work that is not required by the approved issue or plan.

## Corrective behavior

- Inspect the owning source and state the evidence that supports each material claim. Use current tracked files for repository facts, Linear for issue facts, and GitHub for PR facts.
- Keep planning intent, implementation, generated output, and publication evidence distinct. Use the smallest surface that can prove the claim.
- Narrow changes to approved scope. For lifecycle actions, obtain evidence from the owning surface and preserve active work.
- Report what was verified and what remains unverified. Do not label a result complete when the evidence does not support it.

## False-positive and override boundaries

Memory, worker reports, generated artifacts, and PR text can be useful pointers; the cue is resolved by checking their owning source, not by ignoring them categorically. A lightweight change does not need elaborate evidence rituals: use evidence proportionate to the claim and consequence. Follow a clear user instruction about scope, and raise conflicts with binding doctrine rather than treating this profile as authority.

## Applicable workflow paths

- [Planning](../runbooks/planning.md)
- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
- [Pull request publication](../runbooks/pr.md)

## Doctrine and skill references

- [Marketplace worker doctrine](../doctrine/marketplace-worker-doctrine.md)
- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)
- [Completed artifact custody](../doctrine/completed-artifacts.md)
- [Unslop profile application skill](../../skills/unslop-profiles/SKILL.md)

## Application example

If a worker report says a PR was merged, first inspect the live GitHub PR and verify its merge state before retiring its plan. Keep the report as a useful pointer, and base the lifecycle decision on GitHub evidence.
