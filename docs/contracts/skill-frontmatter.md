# Skill Frontmatter Contract

This contract applies to installable `SKILL.md` surfaces in the Codex
marketplace bundle, including first-party Superpowers+ skills.

## Canonical Shape

```yaml
---
name: using-superpowers-plus
description: Use when starting workflow-sensitive work that may need a Superpowers workflow skill.
metadata:
  source-id: using-superpowers-plus
  source-path: codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md
  provenance-name: Using Superpowers Plus first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
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
- `metadata` is required for all skills bundled via a bundle-manifest entry, and must be a mapping.
- `metadata` is optional for non-bundled source custody surfaces, but if present it must be a mapping.
- Duplicate keys are rejected.
- Frontmatter should not contain execution instructions.
- Descriptions should say when to use the skill, not just what it is.
- Bundled skills are expected to keep provenance, license, and marketplace bundle
  identity in structured `metadata` fields instead of scattering those facts
  across loose top-level YAML keys.

## Notes

- `metadata` is the canonical place for provenance and adaptation notes.
- Devin-specific dispatch keys (`agent`, `triggers`, `argument-hint`) are
  allowed at the top level for skills that dispatch to a custom subagent.
  They are preserved verbatim by the first-party skill normalizer.
- `metadata.content_mode`, when present, must be one of `verbatim`,
  `normalised`, or `adapted`. `verbatim` means the skill body is copied
  unchanged from upstream. `normalised` means minimal compliance adaptation
  (codex-safe shape, openai-spec compliance, rich metadata, repointing
  moved-file links) with the skill body otherwise unchanged and ownership
  staying with the upstream author. `adapted` means substantive editorial
  adaptation beyond normalisation.
- This contract is narrow: it covers the Superpowers adaptation seam and the
  installable skill marketplace bundle shape, not every historical source snapshot.
