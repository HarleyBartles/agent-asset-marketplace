# Codex Cortex

This plugin bundle retains the MARK-172 `cqrs-event-sourcing` seed, the MARK-200
`event-driven-architecture` import, the MARK-204 `api-design-patterns` import,
the MARK-205 `openapi-specification` import, the MARK-207
`secure-coding-practices`, `owasp-top-10`, and `security-testing-patterns`
imports, and the MARK-210 `threat-modeling-techniques` import from
Claude-Cortex.

## Bundle contents

- `cqrs-event-sourcing`
- `event-driven-architecture`
- `api-design-patterns`
- `openapi-specification`
- `secure-coding-practices`
- `owasp-top-10`
- `security-testing-patterns`
- `threat-modeling-techniques`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the retained source skills are projected.
- Later Claude-Cortex candidates beyond MARK-210 stay out of scope.
- The bundle is a custody surface, not the installable marketplace projection.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip`
- `generated/skill-zips/codex-cortex/event-driven-architecture/skill.zip`
- `generated/skill-zips/codex-cortex/api-design-patterns/skill.zip`
- `generated/skill-zips/codex-cortex/openapi-specification/skill.zip`
- `generated/skill-zips/codex-cortex/secure-coding-practices/skill.zip`
- `generated/skill-zips/codex-cortex/owasp-top-10/skill.zip`
- `generated/skill-zips/codex-cortex/security-testing-patterns/skill.zip`
- `generated/skill-zips/codex-cortex/threat-modeling-techniques/skill.zip`
