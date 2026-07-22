# Projection

This bundle projects first-party and retained third-party source custody into the Codex marketplace.

<!-- BEGIN GENERATED: projection-contract -->
- Active manifest entries (6):
  - `feature-sliced-design`
  - `frontend-ux`
  - `playwright-testing`
  - `react`
  - `wcag`
  - `web-styling`
<!-- END GENERATED: projection-contract -->

## Layer Model

This repository uses three distinct layers for the Frontend Pack bundle:

- Source custody keeps the retained source snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md

## Boundary
- The pack covers frontend application development, including React, accessibility, UX, testing, and Feature-Sliced Design.
- Keep unrelated topical slices in their dedicated packs.
