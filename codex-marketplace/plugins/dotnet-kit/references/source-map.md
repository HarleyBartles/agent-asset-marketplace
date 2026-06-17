# Dotnet Kit Source Map

This bundle projects the MARK-166 approved `.NET` technical skills from a
selective retained snapshot of `codewithmukesh/dotnet-claude-kit`.

Retained upstream evidence:

- `sources/third_party/dotnet-claude-kit/upstream/README.md`
- `sources/third_party/dotnet-claude-kit/upstream/LICENSE`
- `sources/third_party/dotnet-claude-kit/upstream/CLAUDE.md`
- `sources/third_party/dotnet-claude-kit/upstream/.mcp.json`
- `sources/third_party/dotnet-claude-kit/upstream/.claude-plugin/plugin.json`
- `sources/third_party/dotnet-claude-kit/upstream/.claude-plugin/marketplace.json`
- `sources/third_party/dotnet-claude-kit/upstream/skills/modern-csharp/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/vertical-slice/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/clean-architecture/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/ddd/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/ef-core/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/testing/SKILL.md`

First-party custody:

- `sources/first_party/skills/dotnet-kit/decisions.md`
- `sources/first_party/skills/dotnet-kit/decisions.json`
- `sources/first_party/skills/dotnet-kit/intake.json`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| modern-csharp | `sources/third_party/dotnet-claude-kit/upstream/skills/modern-csharp/SKILL.md` | `codex-marketplace/plugins/dotnet-kit/skills/modern-csharp/SKILL.md` | Modern C# guidance kept, provider-specific load assumptions removed. |
| vertical-slice | `sources/third_party/dotnet-claude-kit/upstream/skills/vertical-slice/SKILL.md` | `codex-marketplace/plugins/dotnet-kit/skills/vertical-slice/SKILL.md` | Architecture guidance kept, dotnet-claude-kit framing removed. |
| clean-architecture | `sources/third_party/dotnet-claude-kit/upstream/skills/clean-architecture/SKILL.md` | `codex-marketplace/plugins/dotnet-kit/skills/clean-architecture/SKILL.md` | Architecture guidance kept, advisor-specific framing removed. |
| ddd | `sources/third_party/dotnet-claude-kit/upstream/skills/ddd/SKILL.md` | `codex-marketplace/plugins/dotnet-kit/skills/ddd/SKILL.md` | Tactical DDD guidance kept, provider-specific triggers normalized. |
| ef-core | `sources/third_party/dotnet-claude-kit/upstream/skills/ef-core/SKILL.md` | `codex-marketplace/plugins/dotnet-kit/skills/ef-core/SKILL.md` | EF Core guidance kept, provider-specific load assumptions removed. |
| testing | `sources/third_party/dotnet-claude-kit/upstream/skills/testing/SKILL.md` | `codex-marketplace/plugins/dotnet-kit/skills/testing/SKILL.md` | Testing guidance kept, provider-specific load assumptions removed. |

Deferred in this child:

- `tdd`
- `verify`

The pack root is a documentation and registry surface. The six skills are the
installable units.
