# Wild Bunch Project Pack Provenance

## Summary

The Wild Bunch Project Pack packages Wild Bunch first-party skills together with curated support skills from retained `game-studio`, `dotnet-claude-kit`, `ecc`, and `claude-cortex` custody as a self-contained Codex plugin.

## Source Basis

- **License posture**: Mixed first-party and third-party custody
- **First-party custody**: `sources/first_party/skills/`
- **Third-party custody**: `sources/third_party/game-studio/upstream/skills/`
- **Third-party custody**: `sources/third_party/dotnet-claude-kit/upstream/skills/`
- **Third-party custody**: `sources/third_party/ecc/upstream/skills/`
- **Third-party custody**: `sources/third_party/claude-cortex/upstream/skills/`
- **Marketplace package**: `codex-marketplace/plugins/wild-bunch-project-pack/`

## Source Roots

### First-Party Wild Bunch and Control-Plane Skills

- `sources/first_party/skills/wild-bunch-browser-game/SKILL.md`
- `sources/first_party/skills/wild-bunch-domain-modeling/SKILL.md`
- `sources/first_party/skills/wild-bunch-dotnet-architecture/SKILL.md`
- `sources/first_party/skills/wild-bunch-project-doctrine/SKILL.md`
- `sources/first_party/skills/wild-bunch-worker-verification/SKILL.md`
- `sources/first_party/skills/repo-worker-base/SKILL.md`
- `sources/first_party/skills/boring-loop/SKILL.md`
- `sources/first_party/skills/connector-safety/SKILL.md`
- `sources/first_party/skills/using-github/SKILL.md`
- `sources/first_party/skills/crew/SKILL.md`

### Third-Party Game-Studio Skills

- `sources/third_party/game-studio/upstream/skills/game-studio/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-playtest/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-ui-frontend/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/phaser-2d-game/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/react-three-fiber-game/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/sprite-pipeline/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/three-webgl-game/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/web-3d-asset-pipeline/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md`

### Third-Party Dotnet-Kit Skills

- `sources/third_party/dotnet-claude-kit/upstream/skills/clean-architecture/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/ddd/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/ef-core/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/modern-csharp/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/testing/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/vertical-slice/SKILL.md`

### Third-Party Claude-Cortex Skills

- `sources/third_party/claude-cortex/upstream/skills/api-design-patterns/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/event-driven-architecture/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/interaction-design/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/openapi-specification/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/owasp-top-10/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/secure-coding-practices/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/security-testing-patterns/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/ux-review/SKILL.md`

### Third-Party ECC Skills

- `sources/third_party/ecc/upstream/skills/accessibility/SKILL.md`
- `sources/third_party/ecc/upstream/skills/architecture-decision-records/SKILL.md`
- `sources/third_party/ecc/upstream/skills/backend-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/browser-qa/SKILL.md`
- `sources/third_party/ecc/upstream/skills/design-system/SKILL.md`
- `sources/third_party/ecc/upstream/skills/docker-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/e2e-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/hexagonal-architecture/SKILL.md`
- `sources/third_party/ecc/upstream/skills/make-interfaces-feel-better/SKILL.md`
- `sources/third_party/ecc/upstream/skills/react-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/react-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/security-review/SKILL.md`
- `sources/third_party/ecc/upstream/skills/webapp-testing/SKILL.md`

### Hooks

- `hooks/` - Pack-local Codex hooks (advisory only, not part of GPT skill exports)

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `wild-bunch-project-pack`
- **Display name**: `Wild Bunch Project Pack`
- **Marketplace category**: `Productivity`
- **Content modes**: `verbatim`, `normalised`, and `adapted` as declared in the bundle manifest
- **Adaptation notes**:
  - The pack is self-contained at install time and does not depend on another plugin bundle
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

The active projection inventory lives in `references/bundle-manifest.json` and `references/source-map.md`. Pack-local Codex hooks live under `hooks/` and are advisory only; they do not become part of GPT skill exports. The bundle manifest and provenance map are maintained in `references/`.
