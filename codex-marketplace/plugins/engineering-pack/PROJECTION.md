# Projection

This root is the Codex-facing marketplace projection of the selected ECC
engineering slice.

## Layer Model

This repository uses three distinct layers for the Engineering Pack bundle:

- Source custody keeps the retained third-party snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any
  Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and
  is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md

## Boundary

- Keep implementation and deployment support in this pack.
- Keep workflow dispatch, evaluation, research, and security slices in their
  topical homes.
