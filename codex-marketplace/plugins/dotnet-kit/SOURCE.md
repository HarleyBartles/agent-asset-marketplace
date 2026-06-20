# Source

This plugin projects the MARK-166 approved subset of
`codewithmukesh/dotnet-claude-kit` into a Codex marketplace pack.

## Upstream basis

- Repo: `codewithmukesh/dotnet-claude-kit`
- URL: <https://github.com/codewithmukesh/dotnet-claude-kit.git>
- Pinned commit: `9a9a91107596b3ac3ad1d0ad5ec5eef189e74515`
- License: `MIT`
- Retained snapshot root: `sources/third_party/dotnet-claude-kit/upstream/`

## First-party custody

- Selection/provenance ledger: `sources/first_party/skills/dotnet-kit/decisions.json`
- Human-readable ledger: `sources/first_party/skills/dotnet-kit/decisions.md`
- Intake record: `sources/first_party/skills/dotnet-kit/intake.json`

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/dotnet-kit/`
- Skill root: `codex-marketplace/plugins/dotnet-kit/skills/`
- Generated install units: `generated/skill-zips/dotnet-kit/<skill-name>/skill.zip`

## Boundary

Only the six approved technical skills are projected. `tdd` and `verify` stay
out of this child. Provider-specific execution assumptions are removed before
packaging.

## Authorship

The plugin shell is authored by Harley Bartles. The projected skill roots retain
their upstream source author, source license, and source path in the bundle
manifest and source map so verbatim content stays attributable.
