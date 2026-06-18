# Frontend Pack

Marketplace wrapper for the retained `game-studio` source snapshot projected into an available-source frontend seed.

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
- The exact issue-named candidates `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, and `webapp-testing` were searched for in durable repo and retained source surfaces and are not present in this checkout.
- Because those source files do not exist here, the pack is a source-backed frontend seed rather than a direct projection of the requested five candidates.
- The game-studio slice is the only retained frontend implementation source available in this checkout, so the current pack intentionally projects that source instead of inventing missing candidates.
- The missing five remain blocked by source custody, not merely deferred.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/frontend-pack/web-game-foundations/skill.zip`
- `generated/skill-zips/frontend-pack/game-ui-frontend/skill.zip`
- `generated/skill-zips/frontend-pack/react-three-fiber-game/skill.zip`
- `generated/skill-zips/frontend-pack/game-playtest/skill.zip`

and can be installed directly from those artifacts.
