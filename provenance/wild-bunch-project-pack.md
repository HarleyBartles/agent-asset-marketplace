# Wild Bunch Project Pack Provenance

## Summary

The Wild Bunch Project Pack packages hydrated Wild Bunch first-party skills together with selected browser-game helper skills from the OpenAI game-studio upstream as a self-contained Codex plugin.

## Source Basis

- **License posture**: Mixed first-party and third-party custody
- **First-party custody**: `sources/first_party/skills/`
- **Third-party custody**: `sources/third_party/game-studio/upstream/skills/`
- **Marketplace package**: `codex-marketplace/plugins/wild-bunch-project-pack/`

## Source Roots

### First-Party Wild Bunch Skills (5 skills)

- `sources/first_party/skills/wild-bunch-browser-game/SKILL.md`
- `sources/first_party/skills/wild-bunch-domain-modeling/SKILL.md`
- `sources/first_party/skills/wild-bunch-dotnet-architecture/SKILL.md`
- `sources/first_party/skills/wild-bunch-project-doctrine/SKILL.md`
- `sources/first_party/skills/wild-bunch-worker-verification/SKILL.md`

### Third-Party Browser-Game Skills (5 skills)

- `sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/phaser-2d-game/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-ui-frontend/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-playtest/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/sprite-pipeline/SKILL.md`

### Hooks

- `hooks/` - Pack-local Codex hooks (advisory only, not part of GPT skill exports)

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `wild-bunch-project-pack`
- **Display name**: `Wild Bunch Project Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: 
  - `verbatim` for first-party Wild Bunch skills
  - `imported` for third-party game-studio skills
- **Adaptation notes**:
  - The pack is self-contained at install time and does not depend on another plugin bundle
  - `agent-browser` was reviewed and intentionally excluded because the repo does not retain an approved projection copy for it
  - Icon paths normalized to `./assets/icon.svg` for validator compatibility

## Rights and Attribution

### First-Party Content

- **License**: First-party Harley-owned source
- **Ownership**: Harley Bartles
- **Rights**: Full first-party rights for Wild Bunch skills

### Third-Party Content

- **Upstream repo**: `openai/plugins`
- **Upstream URL**: <https://github.com/openai/plugins.git>
- **Pinned commit**: `c33199897758cab145bb7fdab1ca8fb1cbd9de50`
- **License**: MIT
- **Redistribution rights**: Per MIT license terms
- **Attribution**: OpenAI plugins repository

## Notes

The active projection inventory lives in `codex-marketplace/plugins/wild-bunch-project-pack/skills/`. Pack-local Codex hooks live under `hooks/` and are advisory only; they do not become part of GPT skill exports. The bundle manifest and provenance map are maintained in `references/`.