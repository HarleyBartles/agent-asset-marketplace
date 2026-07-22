# Projection

This bundle projects first-party source custody into the Codex marketplace.

<!-- BEGIN GENERATED: projection-contract -->
- Active manifest entries (7):
  - `clean-architecture`
  - `cqrs`
  - `database-design-patterns`
  - `ddd`
  - `event-driven-systems`
  - `event-sourcing`
  - `hexagonal-architecture`
<!-- END GENERATED: projection-contract -->

## Layer Model

This repository uses three distinct layers for the Architecture Pack bundle:

- Source custody keeps the retained source snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md

## Boundary
- The pack covers software architecture patterns, domain-driven design, CQRS, event sourcing, clean architecture, and hexagonal architecture.
- Keep unrelated topical slices in their dedicated packs.
