# Projection

This bundle projects first-party source custody into the Codex marketplace.

<!-- BEGIN GENERATED: projection-contract -->
- Active manifest entries (3):
  - `python`
  - `python-frameworks`
  - `typescript`
<!-- END GENERATED: projection-contract -->

## Layer Model

This repository uses three distinct layers for the Language Patterns Pack bundle:

- Source custody keeps the retained source snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md

## Boundary
- The pack covers Python and TypeScript language, testing, async, performance, and framework guidance.
- Keep unrelated topical slices in their dedicated packs.
