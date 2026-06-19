# Wild Bunch Project Pack Source Map

This bundle packages the hydrated Wild Bunch first-party skills together with selected browser-game helper skills as a self-contained Codex plugin.

The plugin shell is authored by Harley Bartles. The projected skill roots retain their upstream source author, source license, and source path in the bundle manifest and source map so verbatim content stays attributable.

| Skill | Content mode | Source origin | Upstream author | Upstream license | Source path | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| wild-bunch-project-doctrine | verbatim | first_party | Harley Bartles | MIT | `sources/first_party/skills/wild-bunch-project-doctrine/SKILL.md` | Hydrated from authoritative zip, projected unchanged. |
| wild-bunch-domain-modeling | verbatim | first_party | Harley Bartles | MIT | `sources/first_party/skills/wild-bunch-domain-modeling/SKILL.md` | Hydrated from authoritative zip, projected unchanged. |
| wild-bunch-dotnet-architecture | verbatim | first_party | Harley Bartles | MIT | `sources/first_party/skills/wild-bunch-dotnet-architecture/SKILL.md` | Hydrated from authoritative zip, projected unchanged. |
| wild-bunch-browser-game | verbatim | first_party | Harley Bartles | MIT | `sources/first_party/skills/wild-bunch-browser-game/SKILL.md` | Hydrated from authoritative zip, projected unchanged. |
| wild-bunch-worker-verification | verbatim | first_party | Harley Bartles | MIT | `sources/first_party/skills/wild-bunch-worker-verification/SKILL.md` | Hydrated from authoritative zip, projected unchanged. |
| web-game-foundations | verbatim | game-studio | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md` | Copied verbatim from retained game-studio snapshot. |
| phaser-2d-game | verbatim | game-studio | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/phaser-2d-game/SKILL.md` | Copied verbatim from retained game-studio snapshot. |
| game-ui-frontend | verbatim | game-studio | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/game-ui-frontend/SKILL.md` | Copied verbatim from retained game-studio snapshot. |
| game-playtest | verbatim | game-studio | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/game-playtest/SKILL.md` | Copied verbatim from retained game-studio snapshot. |
| sprite-pipeline | verbatim | game-studio | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/sprite-pipeline/SKILL.md` | Copied verbatim from retained game-studio snapshot. |

Retained first-party custody:

- `sources/first_party/skills/wild-bunch-browser-game/`
- `sources/first_party/skills/wild-bunch-domain-modeling/`
- `sources/first_party/skills/wild-bunch-dotnet-architecture/`
- `sources/first_party/skills/wild-bunch-project-doctrine/`
- `sources/first_party/skills/wild-bunch-worker-verification/`

Retained third-party game-studio custody:

- `sources/third_party/game-studio/upstream/`
- `sources/third_party/game-studio/upstream/.codex-plugin/plugin.json`
- `sources/third_party/game-studio/upstream/skills/web-game-foundations/`
- `sources/third_party/game-studio/upstream/skills/phaser-2d-game/`
- `sources/third_party/game-studio/upstream/skills/game-ui-frontend/`
- `sources/third_party/game-studio/upstream/skills/game-playtest/`
- `sources/third_party/game-studio/upstream/skills/sprite-pipeline/`

The pack root is an installable Codex plugin projection. It does not replace the retained source custody trees.
