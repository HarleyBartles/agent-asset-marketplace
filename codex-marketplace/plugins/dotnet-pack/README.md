# Dotnet Pack

This plugin bundle projects the first-party .NET ecosystem skill into an installable Codex marketplace pack.

## Bundle contents

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary
- `dotnet` carries the first-party .NET ecosystem guidance.
- Provider-specific assumptions from the upstream snapshot are stripped or rewritten in the installable pack.

## Install shape

The installable skill zips are generated under `generated/skill-zips/<skill-name>.zip`.
