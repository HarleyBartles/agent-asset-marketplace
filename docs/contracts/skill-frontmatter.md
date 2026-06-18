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
  adaptation_overlay: adaptation-overlays/superpowers/using-superpowers
  projection_plugin: superpowers
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
- `metadata` is optional, but if present it must be a mapping.
- Duplicate keys are rejected.
- Frontmatter should not contain execution instructions.
- Descriptions should say when to use the skill, not just what it is.

## Notes

- `metadata` is the canonical place for provenance and adaptation notes.
- This contract is narrow: it covers the Superpowers adaptation seam and the
  installable skill projection shape, not every historical source snapshot.
