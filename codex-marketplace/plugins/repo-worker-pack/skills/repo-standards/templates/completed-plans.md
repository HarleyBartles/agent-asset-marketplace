## Scope

Completed-plan custody and retained completed specifications.

## Purpose

Completed implementation plans are not retained in the tracked repository.
They are copied to the protected off-repo cold store at
`<main-checkout>/../_agent-scratch/<repo-name>/archive/completed-plans/`, with
a deterministic hash manifest, before removal from Git. Git history is the
immutable receipt; the cold store is convenience retrieval only.

## Rule

Do not use a completed plan as:
- a source of canonical command sequences,
- a template for current implementation,
- or an authoritative example of repo conventions.

They may contain outdated tooling, stale links, or superseded patterns.

For current conventions, use:
- `.agents/doctrine/*.md`
- `.agents/runbooks/*.md`
- active plans and specs in `.agents/plans/` and `.agents/specs/`
- the `repo-standards` and `handoff-gates` skills

Before plan removal, promote any enduring decision into an ADR or current
doctrine/runbook. A consumer may retain completed specs when it has explicitly
decided they are durable architecture records; completed specs are not an
automatic substitute for ADRs.
