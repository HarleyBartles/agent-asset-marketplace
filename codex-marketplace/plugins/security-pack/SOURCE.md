# Source

This plugin projects the MARK-207 `secure-coding-practices`,
`owasp-top-10`, and `security-testing-patterns` slices plus the MARK-210
`threat-modeling-techniques` slice from the retained Codex Cortex custody
plugin into a Codex marketplace pack.

## Source custody

- Retained upstream root: `sources/third_party/codex-cortex/upstream/`
- Retained skill roots:
  `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/`
  `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/`
  `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/`
- Retained skill root:
  `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/`
- First-party ledgers:
  - `sources/first_party/skills/codex-cortex/intake.json`
  - `sources/first_party/skills/codex-cortex/decisions.json`
  - `sources/first_party/skills/codex-cortex/decisions.md`
- Provenance note: `provenance/codex-cortex.md`

## Projection surfaces

- Codex Cortex projection:
  `codex-marketplace/plugins/codex-cortex/skills/secure-coding-practices/`
  `codex-marketplace/plugins/codex-cortex/skills/owasp-top-10/`
  `codex-marketplace/plugins/codex-cortex/skills/security-testing-patterns/`
  `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/`
- Security Pack projection:
  `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/`
  `codex-marketplace/plugins/security-pack/skills/owasp-top-10/`
  `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/`
  `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/`
- Security Pack source map: `codex-marketplace/plugins/security-pack/references/source-map.md`
- Generated install unit:
  `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
  `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
  `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
  `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`

## Boundary

`secure-coding-practices` stays focused on defensive application coding
patterns, `owasp-top-10` stays focused on application-risk taxonomy and
remediation, `security-testing-patterns` stays focused on validation and
testing strategy, and `threat-modeling-techniques` stays focused on
pre-implementation risk framing, attack surfaces, abuse cases, and security
design choices. Generic compliance theatre, infra security, repo governance,
and audit-prep-only material stay out of scope.

