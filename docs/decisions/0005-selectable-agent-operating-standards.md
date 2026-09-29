# ADR 0005: Selectable Agent Operating Model standards

**Status:** Accepted

## Context

Agent Operating Model is available to agents as an ambient plugin. Treating its installation as a consumer's commitment to every repository standard couples agent capability with repository policy and makes hosted validation depend on an agent runtime.

## Decision

Agent Operating Model publishes a catalog of individually identifiable standards and the resources needed to deploy them. Each consumer declares the marketplace standards it adopts and its repository-owned standards in its own versioned composition. An empty marketplace-standard selection is valid. Plugin subscriptions and installed skill projections do not select or require standards.

The consumer's runner validates the complete composition, dispatches only selected checks and scaffolds, and honors explicit dependencies. A consumer deploys selected marketplace checker inputs from a pinned marketplace revision. Local hooks and hosted CI run those consumer-controlled inputs without requiring Codex or ambient plugin projections.

## Consequences

Standards need stable IDs, clear ownership, dependency declarations, and an executable resource contract. Adoption and updates are explicit consumer changes. The marketplace migration path must preserve existing runner behavior until deployed checkers and the new composition pass validation. Skill refresh does not change the composition, deployed checker bytes, or their provenance.

## Current authority

The Agent Operating Model `operating-standards-catalog.json`, `operating-standards.schema.json`, `repository-shape-standard.md`, and `ci-validation-pipeline.md` define the catalog, consumer declaration, selected dispatch, deployment, and hosted validation behavior.
