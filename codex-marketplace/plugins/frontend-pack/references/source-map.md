# Frontend Pack Source Map

This bundle projects the retained `game-studio` browser frontend and QA guidance into a marketplace surface. The retained upstream skills keep their original bodies and are projected into `frontend-pack` with pack-relative references.

Retained custody evidence:

- `sources/third_party/game-studio/upstream/README.md` is not present as a root file in this snapshot; the retained source lives under the upstream skill and reference tree.
- `sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-ui-frontend/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/react-three-fiber-game/SKILL.md`
- `sources/third_party/game-studio/upstream/skills/game-playtest/SKILL.md`
- `sources/third_party/game-studio/upstream/references/engine-selection.md`
- `sources/third_party/game-studio/upstream/references/phaser-architecture.md`
- `sources/third_party/game-studio/upstream/references/three-webgl-architecture.md`
- `sources/third_party/game-studio/upstream/references/threejs-stack.md`
- `sources/third_party/game-studio/upstream/references/react-three-fiber-stack.md`
- `sources/third_party/game-studio/upstream/references/web-3d-asset-pipeline.md`
- `sources/third_party/game-studio/upstream/references/frontend-prompts.md`
- `sources/third_party/game-studio/upstream/references/three-hud-layout-patterns.md`
- `sources/third_party/game-studio/upstream/references/playtest-checklist.md`
- `sources/third_party/game-studio/upstream/references/react-three-fiber-starter.md`
- `sources/third_party/game-studio/upstream/references/gltf-loading-starter.md`
- `sources/third_party/game-studio/upstream/references/rapier-integration-starter.md`
- `sources/third_party/game-studio/upstream/references/webgl-debugging-and-performance.md`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| web-game-foundations | `sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/web-game-foundations/SKILL.md` | Verbatim projection of the shared browser-game architecture guidance that the UI and QA skills reference. |
| game-ui-frontend | `sources/third_party/game-studio/upstream/skills/game-ui-frontend/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/game-ui-frontend/SKILL.md` | Verbatim projection of the retained frontend UI guidance. |
| react-three-fiber-game | `sources/third_party/game-studio/upstream/skills/react-three-fiber-game/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/react-three-fiber-game/SKILL.md` | Verbatim projection of the retained React-hosted 3D guidance. |
| game-playtest | `sources/third_party/game-studio/upstream/skills/game-playtest/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/game-playtest/SKILL.md` | Verbatim projection of the retained browser QA and playtest guidance. |

Deferred issue-named candidates:

- `react-performance-optimization`
- `accessibility-audit`
- `ux-review`
- `interaction-design`
- `webapp-testing`

Those exact names are not present in the retained source snapshot in this checkout, so they are deferred until a real source file is available.

The pack root is an installable Codex plugin projection. It does not replace the retained `game-studio` custody snapshot or the issue-level defer record.
