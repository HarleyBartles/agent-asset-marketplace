# Design Runbook

Use this reference when turning an idea into a repo-ready design spec for the agent-asset-marketplace repo. This guide only adds repo-specific design and handoff rules. The general brainstorming workflow comes from `/brainstorming`.

## Before You Begin: Read the Standards

A design that ignores the repo's standards will produce specs that do not hand off cleanly. Read these before you start:

- **[`../docs/mesh-policy.md`](../docs/mesh-policy.md)** - how AGENTS.md, README, and INDEX.md surfaces are supposed to work
- **[`AGENTS.md`](../../AGENTS.md)** - repository source-of-truth and publication rules
- **[`docs/custody-and-marketplace-doctrine.md`](../../docs/custody-and-marketplace-doctrine.md)** - source custody rules, provenance modes, plugin curation rules

## Design Spec Expectations

The design spec is the working record of the decision, not the implementation
plan. Write the spec to `.agents/specs/YYYY-MM-DD-<topic>-design.md`
and commit it; the `specs/` surface is repo-resident and indexed.

- Write the spec to `.agents/specs/YYYY-MM-DD-<topic>-design.md`.
  Do not create design specs under `.agents/docs/design/` or another tracked
  docs directory.
- Keep the design spec in the `specs/` surface while the design is being
  developed and reviewed; it is tracked, not ignored.
- Keep it concrete enough that a planning agent can turn it into a task plan without inventing missing decisions
- Include the real names, counts, file targets, and contract rules that define the work
- Separate goals, scope, non-goals, contract, and validation
- Call out any tradeoffs or intentionally deferred decisions explicitly
- Keep the spec focused on the requested slice. If the idea is too large for one spec, split it before writing
- Use the repo's existing vocabulary and file locations. The spec should not invent a new terminology layer when the repo already has one
- Include only the additional repo-specific facts the planner will need, not the full text of the brainstorming workflow

## Spec Self-Review

After writing the spec, review it against these checks before handing it off:

1. **Placeholder scan** - remove any `TBD`, `TODO`, or vague shorthand
2. **Internal consistency** - make sure the goals, scope, contracts, and validation all agree
3. **Scope check** - confirm the spec is narrow enough for one implementation plan
4. **Ambiguity check** - if a requirement could be interpreted two ways, make it explicit now
5. **Source sanity** - verify the file paths, skill names, and contract details against the live repo
6. **Repo-only content check** - remove any generic brainstorming instructions that are already covered by `/brainstorming`

If the spec fails any of those checks, fix it before proceeding.

## Cross-repo consumer check

When the design produces a vendored asset, skill, or prompt that will be consumed by other repos (especially sister or consumer repos installed from this marketplace), confirm the spec does not hardcode this repo's paths, commands, or conventions. Use consumer-canonical examples and avoid targets or file layouts that do not exist in the consumer's environment.

## Handoff to Planning

Before handing the spec to a planning agent, assess whether it is already strong enough to avoid avoidable in-flight invention.

Once the design is approved, write the implementation plan under the tracked
`.agents/plans/` surface. The plan is the task-ready handoff
artifact; the committed design spec remains visible for provenance.

- Rate the spec's handoff confidence honestly on a 0-10 scale
- If the confidence is below `9/10`, do not hand it off yet
- Tighten the design, verify source facts, or close obvious gaps until the score reaches the floor or the remaining gap is clearly user-owned
- If a gap materially changes scope, sequence, or file targets, surface it in the design instead of burying it for the planner
- The planner should receive a spec that is both honest and as de-risked as the current source allows
- If the spec is missing repository-specific contract details, keep editing it rather than hoping the planner will infer them

When the spec is ready, hand it off with the key contract points the planner will need:

- exact skill or plugin names
- counts or cardinalities
- path and naming rules
- validation expectations (marketplace regeneration, CI checks)
- any explicit non-goals or out-of-scope items
- any repo-specific handoff gate or confidence floor that differs from the generic brainstorming workflow

## What a Design Spec Is Not

- A design spec is not an implementation plan
- A design spec is not a commit log
- A design spec is not permission to broaden the work beyond the asked slice
- A design spec is not ready until it can hand off cleanly to planning without forcing the planner to invent the contract
