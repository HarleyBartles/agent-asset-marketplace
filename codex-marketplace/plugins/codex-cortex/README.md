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

- `generated/skill-zips/cqrs-event-sourcing.zip`
- `generated/skill-zips/event-driven-architecture.zip`
- `generated/skill-zips/api-design-patterns.zip`
- `generated/skill-zips/openapi-specification.zip`
- `generated/skill-zips/secure-coding-practices.zip`
- `generated/skill-zips/owasp-top-10.zip`
- `generated/skill-zips/security-testing-patterns.zip`
- `generated/skill-zips/threat-modeling-techniques.zip`
