# Source

This bundle packages the hydrated Wild Bunch first-party skills together with the selected browser-game helper skills as a self-contained Codex plugin.

The plugin shell is authored by Harley Bartles. The projected skill roots retain their upstream source author, source license, and source path in the bundle manifest and source map so verbatim content stays attributable.

## Canonical basis

- First-party Wild Bunch source custody: `sources/first_party/skills/`
- Third-party browser-game source custody: `sources/third_party/game-studio/upstream/skills/`
- License posture: mixed first-party and third-party custody

## Source roots copied

- `skills/wild-bunch-browser-game/SKILL.md`
- `skills/wild-bunch-domain-modeling/SKILL.md`
- `skills/wild-bunch-dotnet-architecture/SKILL.md`
- `skills/wild-bunch-project-doctrine/SKILL.md`
- `skills/wild-bunch-worker-verification/SKILL.md`
- `skills/web-game-foundations/SKILL.md`
- `skills/phaser-2d-game/SKILL.md`
- `skills/game-ui-frontend/SKILL.md`
- `skills/game-playtest/SKILL.md`
- `skills/sprite-pipeline/SKILL.md`
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

The active projection inventory now lives in `codex-marketplace/plugins/wild-bunch-project-pack/skills/`.
Pack-local Codex hooks live under `hooks/` and are advisory only; they do not become part of GPT skill exports.
