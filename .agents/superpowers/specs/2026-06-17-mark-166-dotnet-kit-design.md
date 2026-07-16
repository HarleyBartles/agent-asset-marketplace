# MARK-166 dotnet-kit Design Receipt

**Goal:** Repack the MARK-165 approved `dotnet-claude-kit` subset into a Codex/GPT-compatible `.NET` pack with selective retained upstream custody, first-party provenance, and installable marketplace artifacts.

**Approved boundary:** retain only the upstream material needed to verify and adapt the six selected technical skills, plus license/provenance files needed to prove source custody. Do not snapshot the full upstream repository.

## Design

The work will split into three durable surfaces:

1. `sources/third_party/dotnet-claude-kit/upstream/` for the selective upstream snapshot and provider-specific evidence.
2. `sources/first_party/skills/dotnet-kit/` for the first-party selection/provenance ledger.
3. `codex-marketplace/plugins/dotnet-kit/` for the market-facing Codex pack.

The pack will project only the approved technical skills:

- `modern-csharp`
- `vertical-slice`
- `clean-architecture`
- `ddd`
- `ef-core`
- `testing`

The child issue boundary stays intact:

- `tdd` and `verify` remain out of scope.
- Claude-specific hooks, slash commands, MCP/runtime assumptions, plugin-install assumptions, and `CLAUDE.md`-specific behavior are removed or rewritten.
- The pack will not become a GPT handoff issue; direct install notes will point at any generated `skill.zip` artifacts instead.

## Source Custody Shape

The retained upstream snapshot will keep the selected upstream skill files and the minimum root files needed to prove and inspect the provider-specific assumptions that must be stripped:

- upstream license and repository identity files
- upstream `CLAUDE.md`
- upstream MCP/plugin metadata used only as evidence of what was removed or neutralized
- the six selected upstream skill sources

The first-party ledger will record:

- the approved subset
- the retained upstream commit
- the exact inclusion/exclusion boundary
- the adaptation rationale for each selected skill

## Pack Shape

The `dotnet-kit` plugin root will follow the existing marketplace bundle pattern:

- `.codex-plugin/plugin.json`
- `README.md`
- `SOURCE.md`
- `LICENSE`
- `assets/icon.svg`
- `references/bundle-manifest.json`
- `references/source-map.md`
- `skills/<skill-name>/SKILL.md` for the six adapted skills

The bundle manifest and source map will treat the pack as a third-party projection over the selective upstream snapshot plus the first-party ledger. The pack root itself is documentation and registry surface, not part of the six-skill boundary.

## Validation

Validation will use the repo’s current marketplace and artifact pipeline:

- `py -3 tools/update_skill_artifacts.py --pack dotnet-kit`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/update_skill_artifacts.py --check`
- `git diff --check`

The generated `skill.zip` artifacts, registry, and marketplace manifests must prove that only the six selected skills were projected and that `tdd`/`verify` were not imported.
