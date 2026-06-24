# Source

This bundle packages the Wild Bunch first-party skills together with curated support skills from retained `game-studio`, `dotnet-claude-kit`, `ecc`, and `claude-cortex` custody as a self-contained Codex plugin.

## Canonical basis

- First-party Wild Bunch and control-plane source custody: `sources/first_party/skills/`
- Third-party browser-game source custody: `sources/third_party/game-studio/upstream/skills/`
- Third-party .NET source custody: `sources/third_party/dotnet-claude-kit/upstream/skills/`
- Third-party ECC source custody: `sources/third_party/ecc/upstream/skills/`
- Third-party Claude-Cortex source custody: `sources/third_party/claude-cortex/upstream/skills/`
- License posture: mixed first-party and third-party custody

## Source roots copied

- `references/bundle-manifest.json`
- `references/source-map.md`
- `references/provenance-map.json`
- `hooks/`

## Marketplace adaptation

- Status: `projected`
- Plugin name: `wild-bunch-project-pack`
- Display name: `Wild Bunch Project Pack`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- The pack is self-contained at install time and does not depend on another plugin bundle.
- `agent-browser` was reviewed and intentionally excluded because the repo does not retain an approved projection copy for it.

## Notes

The active projection inventory lives in `references/bundle-manifest.json` and `references/source-map.md`.
Pack-local Codex hooks live under `hooks/` and are advisory only; they do not become part of GPT skill exports.
