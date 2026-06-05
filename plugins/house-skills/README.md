# House Skills Plugin Skeleton

Issue: MARK-13

`house-skills` is the first repo-backed, first-party House Skills Codex plugin
bundle skeleton for Harley's custom skills.

The bundle is installable as an early private marketplace placeholder so Codex
can discover the House Skills projection shape, provenance, and validation
route. MARK-16 imports canonical source records under `gpt-skills/house-skills/`,
but this plugin bundle does not yet project imported House Skill source text.

## Bundle Shape

```text
plugins/house-skills/
  .codex-plugin/plugin.json
  skills/
  hooks/
  assets/
  README.md
```

## Import Boundary

This plugin currently carries only skeleton README files, metadata, and source
pointers. Later projection slices should add reviewed `SKILL.md` content under
`skills/` only after the corresponding canonical source exists under
`gpt-skills/house-skills/` and the asset/provenance records are updated.

## Canonical Source Pointers

MARK-16 imports canonical source records for `linear-v1` and
`worker-dispatch-linear-v1` under `gpt-skills/house-skills/`. This plugin
projection remains metadata-only in that slice; it does not mirror those
`SKILL.md` files into `plugins/house-skills/skills/`.
