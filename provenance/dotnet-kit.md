# .NET Kit Provenance

## Summary

The .NET Kit plugin projects the MARK-166 approved subset of `codewithmukesh/dotnet-claude-kit` into a Codex marketplace pack, adapting technical .NET guidance for Codex-native workflows.

## Upstream Basis

- **Upstream repository**: `codewithmukesh/dotnet-claude-kit`
- **URL**: <https://github.com/codewithmukesh/dotnet-claude-kit.git>
- **Pinned commit**: `9a9a91107596b3ac3ad1d0ad5ec5eef189e74515`
- **License**: MIT
- **Retained snapshot root**: `sources/third_party/dotnet-claude-kit/upstream/`
- **Marketplace package**: `codex-marketplace/plugins/dotnet-kit/`

## First-Party Custody

- **Selection/provenance ledger**: `sources/first_party/skills/dotnet-kit/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/dotnet-kit/decisions.md`
- **Intake record**: `sources/first_party/skills/dotnet-kit/intake.json`

## Approved Skills (MARK-166 Subset)

The first Codex-native subset focuses on technical .NET guidance that transfers cleanly after adaptation:

| Skill | Status | Reason |
|---|---|---|
| `modern-csharp` | Included | Baseline C# 14 guidance with minimal provider coupling |
| `vertical-slice` | Included | Feature-folder and handler guidance that maps cleanly to Codex workflows |
| `clean-architecture` | Included | Boundary and dependency guidance remains useful after provider-neutral rewrites |
| `ddd` | Included | Tactical domain modeling is portable once Claude-specific workflow text is removed |
| `ef-core` | Included | Durable persistence guidance directly useful in .NET repos |
| `testing` | Included | High-value test guidance that transfers cleanly to Codex-native repo work |

## Deferred Skills

- `tdd` - Workflow orchestrator with strong Claude command and validation-pipeline assumptions
- `verify` - Workflow orchestrator with strong Claude command and validation-pipeline assumptions

Reason: Both are better handled after the first Codex-native technical pack exists and the command/validation contract is defined for this marketplace.

## Marketplace Adaptation

- **Status**: `adapted`
- **Plugin name**: `dotnet-kit`
- **Display name**: ".NET Kit"
- **Marketplace category**: `Productivity`
- **Content mode**: `adapted` from upstream with provider-specific assumptions removed
- **Adaptation notes**:
  - Stripped `CLAUDE.md`-specific setup language
  - Removed slash-command assumptions
  - Removed hook and plugin-install instructions
  - Removed MCP runtime assumptions specific to Claude Code
  - Rewrote references to imply marketplace installation rather than upstream repo

## Pack Shape

- **Codex plugin root**: `codex-marketplace/plugins/dotnet-kit/`
- **Skill root**: `codex-marketplace/plugins/dotnet-kit/skills/`
- **Generated install units**: `generated/skill-zips/<skill-name>.zip`

## Rights and Attribution

- **Upstream source**: codewithmukesh/dotnet-claude-kit
- **License**: MIT
- **Redistribution rights**: Per MIT license terms
- **Modifications**: MARK-166 adaptation for Codex-native workflows with provider-specific assumptions removed

## Boundary

Only the six approved technical skills are projected. `tdd` and `verify` stay out of this pack. Provider-specific execution assumptions are removed before packaging.

## Notes

This is the standardized provenance file for the dotnet-kit plugin. The original detailed intake record is preserved at `provenance/dotnet-claude-kit.md` for historical reference.
