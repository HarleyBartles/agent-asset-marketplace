# Codex Cortex Provenance

## Source anchor

- Upstream repository: `NickCrew/Claude-Cortex`
- Default branch: `main`
- Resolved commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: MIT

## Custody surface

- Retained snapshot root: `sources/third_party/codex-cortex/upstream/`
- First-party import ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- First-party intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/codex-cortex/`
- Installable plugin projection: `codex-marketplace/plugins/architecture-pack/`
- Installable plugin projection: `codex-marketplace/plugins/api-contracts-pack/`
- Installable plugin projection: `codex-marketplace/plugins/language-patterns-pack/`
- Installable plugin projection: `codex-marketplace/plugins/security-pack/`
- Generated install unit: `generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/event-driven-architecture/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/database-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/api-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/openapi-specification/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/secure-coding-practices/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/owasp-top-10/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/security-testing-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/threat-modeling-techniques/skill.zip`
- Generated install unit: `generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip`
- Generated install unit: `generated/skill-zips/architecture-pack/event-driven-architecture/skill.zip`
- Generated install unit: `generated/skill-zips/architecture-pack/database-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/api-contracts-pack/openapi-specification/skill.zip`
- Retained source snapshot root: `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/`
- Generated install unit: `generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`
- Installable plugin projection: `codex-marketplace/plugins/language-patterns-pack/`
- Generated install unit: `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- Generated install unit: `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
- Generated install unit: `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`

## Boundary

The retained custody surface seeds `cqrs-event-sourcing`,
`event-driven-architecture`, `database-design-patterns`, `api-design-patterns`,
`openapi-specification`, `secure-coding-practices`, `owasp-top-10`,
`security-testing-patterns`, the MARK-212 `typescript-advanced-patterns`
guidance projected through `language-patterns-pack`, and `threat-modeling-techniques`.
Generic compliance theatre, infra security, repo governance, and audit-prep-only
material stay out of scope unless a later issue explicitly composes them in.
