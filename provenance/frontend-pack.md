# Frontend Pack Provenance

## Source anchor

- Upstream repository: `openai/plugins`
- Upstream commit: `c33199897758cab145bb7fdab1ca8fb1cbd9de50`
- License: MIT

## Custody surface

- Retained snapshot root: `sources/third_party/game-studio/upstream/`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/frontend-pack/`
- Generated install unit: `generated/skill-zips/frontend-pack/web-game-foundations/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/game-ui-frontend/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/react-three-fiber-game/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/game-playtest/skill.zip`

## Boundary

The retained custody surface seeds browser-game frontend guidance for `web-game-foundations`, `game-ui-frontend`, `react-three-fiber-game`, and `game-playtest`. The exact issue-named candidates `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, and `webapp-testing` were searched for in live repo source and are not present in this checkout, so they remain blocked by missing source custody rather than being projected from invented placeholders.

This makes `frontend-pack` an available-source frontend seed for MARK-214, not a direct projection of the requested five candidates. If those exact skills later appear in durable source custody, they should be projected from that source or split into a separate follow-up issue rather than retrofitted into this pack.
