# Frontend Pack

Marketplace wrapper for the retained `claude-cortex` frontend application source
slice.

## Bundle contents

- `react-performance-optimization`
- `accessibility-audit`
- `ux-review`
- `interaction-design`
- `webapp-testing`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `react-performance-optimization` carries React render, memoization, code splitting, virtualization, and profiling guidance.
- `accessibility-audit` carries WCAG 2.2 AA triage and keyboard, labels, contrast, and motion checks.
- `ux-review` carries heuristic UX review, accessibility review, and interaction analysis for frontend flows and components.
- `interaction-design` carries user flow, state transition, micro-interaction, and feedback pattern guidance.
- `webapp-testing` carries Playwright-based browser automation and local web application testing guidance.
- The pack is sourced from retained `NickCrew/Claude-Cortex` frontend skills under the retained `claude-cortex` custody root, not from `game-studio`.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/frontend-pack/react-performance-optimization/skill.zip`
- `generated/skill-zips/frontend-pack/accessibility-audit/skill.zip`
- `generated/skill-zips/frontend-pack/ux-review/skill.zip`
- `generated/skill-zips/frontend-pack/interaction-design/skill.zip`
- `generated/skill-zips/frontend-pack/webapp-testing/skill.zip`

and can be installed directly from those artifacts.
