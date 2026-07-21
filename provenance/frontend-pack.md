# Frontend Pack Provenance

## Summary

The Frontend Pack projects first-party frontend skills alongside retained `feature-sliced` and `NickCrew/Claude-Cortex` custody into a Codex marketplace pack.

## Source Custody

### First-Party Custody

- `sources/first_party/skills/react/`
- `sources/first_party/skills/wcag/`
- `sources/first_party/skills/web-styling/`

### Retained Upstream

- `feature-sliced` upstream: `sources/third_party/feature-sliced/upstream/skills/feature-sliced-design/`
- `NickCrew/Claude-Cortex` upstream:
  - `sources/third_party/claude-cortex/upstream/skills/interaction-design/`
  - `sources/third_party/claude-cortex/upstream/skills/ux-review/`
  - `sources/third_party/claude-cortex/upstream/skills/webapp-testing/`

## Projection Surfaces

- `codex-marketplace/plugins/frontend-pack/skills/react/`
- `codex-marketplace/plugins/frontend-pack/skills/wcag/`
- `codex-marketplace/plugins/frontend-pack/skills/web-styling/`
- `codex-marketplace/plugins/frontend-pack/skills/feature-sliced-design/`
- `codex-marketplace/plugins/frontend-pack/skills/interaction-design/`
- `codex-marketplace/plugins/frontend-pack/skills/ux-review/`
- `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/`

## Generated Install Units

- `generated/skill-zips/react.zip`
- `generated/skill-zips/wcag.zip`
- `generated/skill-zips/web-styling.zip`
- `generated/skill-zips/feature-sliced-design.zip`
- `generated/skill-zips/interaction-design.zip`
- `generated/skill-zips/ux-review.zip`
- `generated/skill-zips/webapp-testing.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `frontend-pack`
- **Display name**: `Frontend Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `verbatim` for first-party and retained upstream skills

## Rights and Attribution

- First-party skills are MIT-licensed by Harley Bartles.
- `feature-sliced-design` is used under the upstream MIT license.
- `interaction-design`, `ux-review`, and `webapp-testing` are used under NickCrew/Claude-Cortex MIT terms.

## Boundary

The pack covers React component and performance patterns, web accessibility conformance, CSS approach decisions, feature-sliced design, and supporting interaction/UX/testing guidance. It does not include framework-specific server frameworks, provider-specific tooling, or unrelated implementation domains.
