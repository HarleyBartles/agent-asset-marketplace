# Game Studio Source Map

This bundle projects the retained OpenAI game-studio plugin snapshot as a
market-facing Codex plugin.

The plugin shell is Harley-authored. Verbatim skill projections retain upstream
authorship and MIT licensing in the bundle manifest and the projected skill
frontmatter.

| Skill | Content mode | Source origin | Upstream author | Upstream license | Source path | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| game-playtest | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/game-playtest/SKILL.md` | Game playtesting and feedback workflows. Adapted with upstream authorship metadata frontmatter. |
| game-studio | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/game-studio/SKILL.md` | Core game studio planning and coordination. Adapted with upstream authorship metadata frontmatter. |
| game-ui-frontend | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/game-ui-frontend/SKILL.md` | Game UI and frontend development. Adapted with upstream authorship metadata frontmatter. |
| phaser-2d-game | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/phaser-2d-game/SKILL.md` | Phaser 2D game development workflows. Adapted with upstream authorship metadata frontmatter. |
| react-three-fiber-game | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/react-three-fiber-game/SKILL.md` | React Three Fiber 3D game development. Adapted with upstream authorship metadata frontmatter. |
| sprite-pipeline | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/sprite-pipeline/SKILL.md` | Sprite asset pipeline workflows. Adapted with upstream authorship metadata frontmatter. |
| three-webgl-game | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/three-webgl-game/SKILL.md` | Three.js WebGL game development. Adapted with upstream authorship metadata frontmatter. |
| web-3d-asset-pipeline | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/web-3d-asset-pipeline/SKILL.md` | 3D asset pipeline for web games. Adapted with upstream authorship metadata frontmatter. |
| web-game-foundations | adapted | OpenAI plugins | OpenAI | MIT | `sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md` | Web game foundations and setup. Adapted with upstream authorship metadata frontmatter. |

Retained OpenAI plugins custody:

- `sources/third_party/game-studio/upstream/`
- `sources/third_party/game-studio/upstream/.codex-plugin/plugin.json`
- `sources/third_party/game-studio/upstream/assets/`
- `sources/third_party/game-studio/upstream/skills/game-playtest/`
- `sources/third_party/game-studio/upstream/skills/game-studio/`
- `sources/third_party/game-studio/upstream/skills/game-ui-frontend/`
- `sources/third_party/game-studio/upstream/skills/phaser-2d-game/`
- `sources/third_party/game-studio/upstream/skills/react-three-fiber-game/`
- `sources/third_party/game-studio/upstream/skills/sprite-pipeline/`
- `sources/third_party/game-studio/upstream/skills/three-webgl-game/`
- `sources/third_party/game-studio/upstream/skills/web-3d-asset-pipeline/`
- `sources/third_party/game-studio/upstream/skills/web-game-foundations/`

The pack root is an installable Codex plugin projection. It does not replace
the retained OpenAI plugins source custody tree.
