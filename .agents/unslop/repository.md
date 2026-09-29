# Unslop Profile: repository

## Task trigger and scope

Use this profile when planning, implementing, reviewing, or preparing a pull request for repository changes in this Marketplace. Apply only the failure cues below that are relevant to the current work.

## Recurring failure pattern

Agents can mistake remembered, reported, generated, or convenient state for current repository or publication truth; make claims beyond the evidence available; or broaden a change beyond its approved scope. These failures make repository work hard to verify and can cause unsafe lifecycle decisions.

## Recognition cues

- A plan, review note, worker return, or PR summary calls an action complete but offers no direct evidence from the changed output or published state.
- A proposed correction is based on a generated projection or remembered behavior without checking the source or current result.
- The diff adds adjacent work whose connection to the approved task is not apparent.

## Corrective behavior

- Open the specific changed file, test output, generated result, or published record behind the claim. Confirm that it shows the stated outcome.
- Compare the correction to the approved task and actual diff. If its connection is unclear, remove the adjacent change or explain why it is required.
- When direct evidence is unavailable, label the claim unverified and leave dependent completion or lifecycle decisions open.

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
