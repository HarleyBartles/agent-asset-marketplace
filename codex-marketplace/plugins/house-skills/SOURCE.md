# Source

This plugin is the reviewed first-party House Skills plugin root.

## Source basis

- Source ledger: `sources/first_party/skills/house-skills/decisions.md`
- Structured archive ledger: `sources/first_party/skills/house-skills/decisions.json`
- Intake ledger: `sources/first_party/skills/house-skills/intake.json`
- Provenance note: `provenance/house-skills.md`
- Current skill roots: `codex-marketplace/plugins/house-skills/skills/`
- Wild Bunch first-party hydration: `codex-marketplace/plugins/house-skills/skills/wild-bunch-*/`

## Source surfaces copied

- `.codex-plugin/plugin.json`
- `assets`
- `skills`

## Marketplace adaptation

- Status: `current`
- Plugin name: `house-skills`
- Display name: `House Skills`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- Kept each current skill root unversioned and installable under `skills/<skill-name>/`
- Folded the still-needed support files from historical version packages into the unversioned skill roots
- Preserved the version history in each skill's changelog and support files

## Notes

The active source inventory now lives in `codex-marketplace/plugins/house-skills/skills/`.

`connector-safety` and `github-operations` are now projected from
`sources/first_party/skills/connector-safety/` and
`sources/first_party/skills/github-operations/` respectively. House Skills
keeps the installable projections, not the canonical first-party source
authority, for those two skills.
