# Skill Frontmatter Contract

This contract applies to installable `SKILL.md` surfaces in the Codex
marketplace projection, including Superpowers adaptations.

## Canonical Shape

```yaml
---
name: using-superpowers
description: Use when starting workflow-sensitive work that may need a Superpowers workflow skill.
metadata:
  source_category: third_party
  upstream_name: using-superpowers
  upstream_version: v5.1.0
  adaptation_overlay: adapters/codex/superpowers-plus/using-superpowers
  projection_plugin: superpowers
  license: "MIT"
---
```

## Rules

- The first line must be a standalone `---`.
- The closing delimiter must be a standalone `---`.
- The file must be UTF-8 without a BOM.
- The frontmatter must parse with `yaml.safe_load`.
- The frontmatter must be a top-level mapping.
- `name` is required and must be a nonblank string.
- `description` is required and must be a nonblank string.
- `metadata` is required for all skills projected via a bundle-manifest entry, and must be a mapping.
- `metadata` is optional for non-projected source custody surfaces, but if present it must be a mapping.
- Duplicate keys are rejected.
- Frontmatter should not contain execution instructions.
- Descriptions should say when to use the skill, not just what it is.
- Projected skills are expected to keep provenance, license, and projection
  identity in structured `metadata` fields instead of scattering those facts
  across loose top-level YAML keys.

## Notes

- `metadata` is the canonical place for provenance and adaptation notes.
- `metadata.content_mode`, when present, must be one of `verbatim`,
  `normalised`, or `adapted`. `verbatim` means the skill body is copied
  unchanged from upstream. `normalised` means minimal compliance adaptation
  (codex-safe shape, openai-spec compliance, rich metadata, repointing
  moved-file links) with the skill body otherwise unchanged and ownership
  staying with the upstream author. `adapted` means substantive editorial
  adaptation beyond normalisation.
- This contract is narrow: it covers the Superpowers adaptation seam and the
  installable skill projection shape, not every historical source snapshot.
