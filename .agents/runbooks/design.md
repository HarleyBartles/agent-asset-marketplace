# Design Runbook

Use this reference when turning an idea into a repo-ready design spec for the agent-asset-marketplace repo. This guide only adds repo-specific design and handoff rules. The general brainstorming workflow comes from `brainstorming`.

## Before You Begin: Read the Standards

A design that ignores the repo's standards will produce specs that do not hand off cleanly. Read these before you start:

- **[`../.agents/doctrine/mesh-policy.md`](../.agents/doctrine/mesh-policy.md)** - how AGENTS.md, README, and INDEX.md surfaces are supposed to work
- **[`AGENTS.md`](../../AGENTS.md)** - repository source-of-truth and publication rules
- **[`.agents/doctrine/custody-and-marketplace-doctrine.md`](../../.agents/doctrine/custody-and-marketplace-doctrine.md)** - source custody rules, provenance modes, plugin curation rules

## Design Spec Expectations

Write architectural design specs to
`.agents/specs/YYYY-MM-DD-<topic>-design.md` and commit them; the `specs/`
surface is repo-resident and indexed.

- Write the spec to `.agents/specs/YYYY-MM-DD-<topic>-design.md`.
  Do not create design specs under `.agents/docs/design/` or another tracked
  docs directory.
- Keep the design spec in the `specs/` surface while the design is being
  developed and reviewed; it is tracked, not ignored.
- Use the repo's existing vocabulary and file locations. The spec should not invent a new terminology layer when the repo already has one
- Include only the additional repo-specific facts the planner will need, not the full text of the brainstorming workflow
- Verify marketplace file paths, skill names, custody, and contract details
  against the live repository before recording them.

## Cross-repo consumer check

When the design produces a vendored asset, skill, or prompt that will be consumed by other repos (especially sister or consumer repos installed from this marketplace), confirm the spec does not hardcode this repo's paths, commands, or conventions. Use consumer-canonical examples and avoid targets or file layouts that do not exist in the consumer's environment.

## Workflow ownership

`brainstorming` owns design method, spec self-review, readiness, approval, and
the subsequent planning handoff. This runbook adds only the repository paths,
custody, marketplace source checks, and cross-repo consumer constraint above.
