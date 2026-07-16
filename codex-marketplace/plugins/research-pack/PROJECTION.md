# Projection

This root is the Codex-facing marketplace projection of the selected ECC
research slice.

## Layer Model

This repository uses three distinct layers for the Research Pack bundle:

- Source custody keeps the retained third-party snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any
  Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and
  is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md

## Boundary

- Keep evidence-first research tools in this pack.
- Keep workflow dispatch, evaluation, engineering, and security slices in their
  topical homes.
