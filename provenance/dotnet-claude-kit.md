# dotnet-claude-kit Provenance and Codex .NET subset proposal

## Source anchor

- Upstream repository: `https://github.com/codewithmukesh/dotnet-claude-kit`
- Default branch: `main`
- Resolved commit: `9a9a91107596b3ac3ad1d0ad5ec5eef189e74515`
- License: MIT

## Intake scope

This note is a source intake and selection record for a future Codex-native .NET skill/plugin pack. It does not repack any upstream skill, template, agent, hook, or workflow surface in this child issue.

The upstream repository contains a broad Claude Code companion surface:

- `CLAUDE.md`
- `.claude-plugin/`
- `.codex/`
- `.cursor/`
- `.opencode/`
- `gemini-extension.json`
- `hooks/`
- `.mcp.json`
- `mcp-configs/`
- slash-command workflows in `skills/`

Those surfaces are provider-specific or workflow-specific and should be treated as source evidence, not copied as-is into the first Codex subset.

## Proposed first Codex subset

Keep the first Codex-native slice focused on technical .NET guidance that transfers cleanly after adaptation:

| Skill | Keep for MARK-166 | Why it belongs |
|---|---|---|
| `modern-csharp` | Yes | Baseline C# 14 guidance with minimal provider coupling. |
| `vertical-slice` | Yes | Feature-folder and handler guidance that maps cleanly to Codex workflows. |
| `clean-architecture` | Yes | Boundary and dependency guidance remains useful after provider-neutral rewrites. |
| `ddd` | Yes | Tactical domain modeling is portable once Claude-specific workflow text is removed. |
| `ef-core` | Yes | Durable persistence guidance directly useful in .NET repos. |
| `testing` | Yes | High-value test guidance that transfers cleanly to Codex-native repo work. |

## Deferred from the first slice

- `tdd`
- `verify`

Reason: both are workflow orchestrators with strong Claude command and validation-pipeline assumptions. They are better handled after the first Codex-native technical pack exists and the command/validation contract is defined for this marketplace.

## Adaptation notes

For the kept skills, MARK-166 should strip or rewrite:

- `CLAUDE.md`-specific setup language
- slash-command assumptions
- hook and plugin-install instructions
- MCP runtime assumptions that are specific to Claude Code
- any references that imply the upstream repo is the install target rather than the source reference

## Proposed next child issue shape

MARK-166 should repack the first Codex subset into a new marketplace plugin root, likely under:

- `codex-marketplace/plugins/dotnet-kit/`

with matching source custody under:

- `sources/first_party/skills/dotnet-kit/`

and a source/provenance map that ties each imported skill back to the upstream commit above and this note.

## Compatibility guardrail

Do not present upstream material as original work. Keep this note, the future source map, and the future marketplace projection explicit about what was retained, what was adapted, and what remained upstream-only.
