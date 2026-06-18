# Frontend Pack

Marketplace wrapper for the retained `game-studio` source snapshot projected into a frontend-focused pack.

## Bundle contents

- `web-game-foundations`
- `game-ui-frontend`
- `react-three-fiber-game`
- `game-playtest`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `web-game-foundations` carries browser-game architectural guidance for simulation/render boundaries, input mapping, and shared UI structure.
- `game-ui-frontend` carries DOM HUD, menu, overlay, and responsive layout guidance.
- `react-three-fiber-game` carries React-hosted 3D UI and shared-state guidance.
- `game-playtest` carries browser-game QA and playtest guidance.
- The pack does not include the exact issue-named candidates `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, or `webapp-testing` because those names are not present in the retained source snapshot in this checkout.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/frontend-pack/web-game-foundations/skill.zip`
- `generated/skill-zips/frontend-pack/game-ui-frontend/skill.zip`
- `generated/skill-zips/frontend-pack/react-three-fiber-game/skill.zip`
- `generated/skill-zips/frontend-pack/game-playtest/skill.zip`

and can be installed directly from those artifacts.
