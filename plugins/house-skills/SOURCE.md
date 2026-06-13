# Source

This plugin packages the reviewed first-party House Skills source catalog as a market-facing Codex plugin.

## Source basis

- Source ledger: `sources/house-skills/decisions.md`
- Structured mirror: `sources/house-skills/decisions.json`
- Intake ledger: `sources/house-skills/intake.json`
- Provenance note: `provenance/house-skills.md`
- Active source roots: `gpt-skills/house-skills/`

## Source surfaces copied

- `.codex-plugin/plugin.json`
- `assets`
- `skills`

## Marketplace adaptation

- Status: `projected`
- Plugin name: `house-skills`
- Display name: `House Skills`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- Mirrored each active first-party House Skills root into `skills/<skill-name>/`
- Preserved nested historical and reference-only skill substance within each copied root
- Kept the bundle wrapper skill as the control plane for the projection

## Notes

The active source inventory remains authoritative in `gpt-skills/house-skills/` and the source ledger. This plugin root is the installable marketplace surface that mirrors those active roots in place.
