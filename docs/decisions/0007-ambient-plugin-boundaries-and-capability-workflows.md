# ADR 0007: Ambient plugin boundaries and capability-based workflows

**Status:** Accepted

## Context

Agent Operating Model, Superpowers+, Repo Worker Pack, MCP Usage Pack, and Unslop+ are available to agents as ambient plugins. A consumer repository must not need a copy of those packs or adopt their standards simply because the agent can use them. A portable workflow still needs a reliable way to find a suitable skill, and an absent required capability must not be silently skipped.

## Decision

Keep each ambient product's role distinct:

- Superpowers+ composes workflow skills.
- Repo Worker Pack provides general agent capabilities for repository work.
- MCP Usage Pack guides use of MCP tools exposed in the current runtime.
- Unslop+ provides writing-quality and profile capabilities that can be used optionally.
- Agent Operating Model catalogs independently deployable repository standards and their implementation resources.

Portable runbooks and playbooks declare the capability they need and whether it is required. At runtime, the agent inspects available skills and chooses a suitable provider. A repository may name one of its genuinely repository-owned skills exactly. If no suitable provider exists for a required capability, the agent stops before the dependent action and reports what is unavailable. Optional capabilities may be skipped with the omission reported.

Repository paths and standards belong to the consumer's own declarations or to a marketplace standard it explicitly adopts. Runtime plugin availability and skill projections do not establish a consumer subscription or standard selection. A bundled ambient helper is resolved from the loaded skill's runtime path; consumer canonical runners use their checked-in, pinned implementation path.

Hosted validation checks the authored runbook/playbook contract, repository-owned skill custody, and composition graph. It does not claim that ambient plugins or skills are installed in the hosted environment.

## Consequences

Ambient packs can evolve without consumer copy-refresh cycles. Portable workflow contracts must distinguish abstract capabilities from repository-owned exact skills and preserve a clear failure for unavailable required capabilities. Consumer standards remain independently selectable and hosted checkers remain consumer-controlled.

## Current authority

The ambient pack sources and product definitions own plugin roles. The Agent Operating Model catalog owns selectable standards. `repo-composition` defines runbook/playbook capability semantics, and each subscribing repository owns its implementation and self-certification. Focused standards own their optional starter assets; no central scaffolder owns the adopted repository surfaces. These are the current authorities; dated audit records are task evidence and do not supersede them.
