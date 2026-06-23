# Projection

This root is the Codex-facing marketplace projection of the selected ECC
mega-pack slice.

## Layer Model

This repository uses three distinct layers for the Everything Codex Code
bundle:

- Source custody keeps the retained third-party snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any
  Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and
  is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md

## Boundary

- Keep the mega pack as a reference projection of the selected ECC slice.
- Keep the topical packs as the user-facing homes for actual work.
