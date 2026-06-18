# Security Pack

This plugin bundle projects the MARK-207 `secure-coding-practices`,
`owasp-top-10`, and `security-testing-patterns` slices plus the MARK-210
`threat-modeling-techniques` slice from the retained Codex Cortex custody
plugin into an installable Codex marketplace pack.

## Bundle contents

- `secure-coding-practices`
- `owasp-top-10`
- `security-testing-patterns`
- `threat-modeling-techniques`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `secure-coding-practices` owns defensive application coding, input
  validation, output encoding, secrets handling, and secure defaults.
- `owasp-top-10` owns OWASP Top 10 application risk review and remediation
  guidance.
- `security-testing-patterns` owns security testing strategy, SAST/DAST/SCA,
  penetration testing, and validation automation.
- `threat-modeling-techniques` owns design-time threat modeling, abuse-case
  thinking, trust boundaries, and risk framing.
- The bundle stays out of generic compliance theatre, infra security, repo
  governance, and audit-prep-only material unless another issue explicitly
  composes them in.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zip is generated under:

- `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
- `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`

