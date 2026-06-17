# Dotnet Kit

This plugin bundle projects the MARK-166 approved .NET technical skills from a
selective retained snapshot of `codewithmukesh/dotnet-claude-kit`.

## Bundle contents

- `modern-csharp`
- `vertical-slice`
- `clean-architecture`
- `ddd`
- `ef-core`
- `testing`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `tdd` and `verify` are deferred from this child.
- Claude hooks, slash commands, MCP/runtime assumptions, and plugin-install
  assumptions are stripped or rewritten in the installable pack.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zips are generated under `generated/skill-zips/dotnet-kit/`
and each skill can be installed directly from its `skill.zip` artifact.
