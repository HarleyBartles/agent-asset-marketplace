# OpenAI Agent YAML Contract

This contract documents the small metadata file used by the MARK-237
Superpowers adaptation overlay seam.

## Canonical Shape

```yaml
version: 1
metadata:
  skill_name: using-superpowers
  plugin: superpowers
  source_category: third_party
  upstream_version: v5.1.0
  adaptation_overlay: adaptation-overlays/superpowers/using-superpowers
```

## Rules

- The file must be UTF-8 without a BOM.
- The file must parse with `yaml.safe_load`.
- The top level must be a mapping.
- `version: 1` is required for the overlay metadata contract used in MARK-237.
- `metadata` is required and must be a mapping.
- `metadata.skill_name`, `metadata.plugin`, `metadata.source_category`,
  `metadata.upstream_version`, and `metadata.adaptation_overlay` are the
  expected provenance keys.
- Additional fields may exist if downstream tooling already expects them, but
  this contract does not require a larger schema.

## Notes

- Existing repo examples may also carry richer `interface`, `policy`, or
  `license` blocks inside `agents/openai.yaml`; this contract does not remove
  those patterns.
- Keep this file boring and additive. It is a provenance stub, not a full
  agent manifest standard.
