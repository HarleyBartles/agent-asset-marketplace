# OpenAI Agent YAML Contract

This contract documents the `agents/openai.yaml` surfaces used by the current
Codex marketplace projections.

## Canonical Shape

Two repository patterns are currently in use:

```yaml
version: 1
metadata:
  skill_name: using-superpowers
  plugin: superpowers
  source_category: third_party
  upstream_name: using-superpowers
  upstream_version: v5.1.0
  adaptation_overlay: adapters/codex/superpowers-plus/using-superpowers
  projection_plugin: superpowers-plus
```

```yaml
version: 1
metadata:
  source-id: ecc-superpowers
  source-path: sources/first_party/skills/ecc-superpowers/SKILL.md
  provenance-name: MARK-244 ECC Superpowers compositional routing skill
  origin: first_party
  source_author: Harley Bartles
  source_license: MIT
  source_repo: https://github.com/HarleyBartles/agent-asset-marketplace
  content_mode: adapted
  adapted_author: Harley Bartles
interface:
  display_name: ECC Superpowers
  short_description: Route ECC workflow-shaped work to the dedicated superpowers-ecc pack.
policy:
  allow_implicit_invocation: true
```

## Rules

- The file must be UTF-8 without a BOM.
- The file must parse with `yaml.safe_load`.
- The top level must be a mapping.
- `version: 1` is required.
- `metadata` is required and must be a mapping.
- All skills projected via a bundle-manifest entry must include `metadata`; source-custody snapshots can omit it.
- When present, provenance keys such as `skill_name`, `plugin`,
  `source_category`, `upstream_name`, `upstream_version`, `adaptation_overlay`,
  `projection_plugin`, `source-id`, `source-path`, `provenance-name`, `origin`,
  `content_mode`, `source_author`, `source_license`, `source_repo`, and
  `adapted_author` must be nonblank strings.
- `interface`, when present, must be a mapping with nonblank `display_name`
  and `short_description`.
- `policy`, when present, must be a mapping, and `allow_implicit_invocation`
  must be boolean when present.
- `dependencies`, when present, must be a mapping, and `dependencies.tools`
  must be a list of mappings with nonblank `type` and `value`.
- `content_mode`, when present under `metadata`, must be one of `verbatim`,
  `normalised`, or `adapted`. `verbatim` means the skill body is copied
  unchanged from upstream. `normalised` means minimal compliance adaptation
  (codex-safe shape, openai-spec compliance, rich metadata, repointing
  moved-file links) with the skill body otherwise unchanged and ownership
  staying with the upstream author. `adapted` means substantive editorial
  adaptation beyond normalisation.

## Notes

- Keep this file boring and additive. It is a contract for the repo's current
  Codex skill projections, not a general agent-manifest standard.
