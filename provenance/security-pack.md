# Security Pack Provenance

## Summary

The Security Pack projects first-party security skills alongside retained `NickCrew/Claude-Cortex` and `ECC` security-oriented skills into a Codex marketplace pack. MARK-295 removed the active ECC slice; MARK-343 and MARK-351 added first-party `owasp-top-ten` and `web-identity`.

## Source Custody

### First-Party Custody

- `sources/first_party/skills/owasp-top-ten/`
- `sources/first_party/skills/web-identity/`

### Retained NickCrew/Claude-Cortex Upstream

- **Upstream root**: `sources/third_party/claude-cortex/upstream/`
- **Retained skill roots**:
  - `sources/third_party/claude-cortex/upstream/skills/secure-coding-practices/`
  - `sources/third_party/claude-cortex/upstream/skills/security-testing-patterns/`
  - `sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques/`

### Historical ECC Upstream

- **Upstream root**: `sources/third_party/ecc/upstream/`
- **Retained skill roots** (historical, not active in this pack):
  - `sources/third_party/ecc/upstream/skills/defi-amm-security/`
  - `sources/third_party/ecc/upstream/skills/django-security/`
  - `sources/third_party/ecc/upstream/skills/laravel-security/`
  - `sources/third_party/ecc/upstream/skills/llm-trading-agent-security/`
  - `sources/third_party/ecc/upstream/skills/network-config-validation/`
  - `sources/third_party/ecc/upstream/skills/perl-security/`
  - `sources/third_party/ecc/upstream/skills/prediction-market-risk-review/`
  - `sources/third_party/ecc/upstream/skills/quarkus-security/`
  - `sources/third_party/ecc/upstream/skills/safety-guard/`
  - `sources/third_party/ecc/upstream/skills/security-bounty-hunter/`
  - `sources/third_party/ecc/upstream/skills/security-review/`
  - `sources/third_party/ecc/upstream/skills/security-scan/`
  - `sources/third_party/ecc/upstream/skills/springboot-security/`

### First-Party Ledgers

- **Selection/provenance ledger**: `sources/first_party/skills/codex-cortex/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/codex-cortex/decisions.md`
- **Intake record**: `sources/first_party/skills/codex-cortex/intake.json`
- **Provenance notes**:
  - `provenance/codex-cortex.md`
  - `provenance/ecc.md`

## Projection Surfaces

### First-Party Projection

- `codex-marketplace/plugins/security-pack/skills/owasp-top-ten/`
- `codex-marketplace/plugins/security-pack/skills/web-identity/`

### NickCrew/Claude-Cortex Projection

- `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/`
- `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/`
- `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/`

### ECC Projection

- `codex-marketplace/plugins/security-pack/skills/safety-guard/`
- `codex-marketplace/plugins/security-pack/skills/security-review/`

- **Security Pack source map**: `codex-marketplace/plugins/security-pack/references/source-map.md`

## Generated Install Units

- `generated/skill-zips/security-pack/owasp-top-ten/skill.zip`
- `generated/skill-zips/security-pack/web-identity/skill.zip`
- `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`
- `generated/skill-zips/security-pack/safety-guard/skill.zip`
- `generated/skill-zips/security-pack/security-review/skill.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `security-pack`
- **Display name**: `Security Pack`
- **Marketplace category**: `Productivity`
- **Content mode**:
  - `verbatim` for first-party skills
  - `normalised` from NickCrew/Claude-Cortex custody (path normalization, frontmatter enrichment, MARK-262 metadata)
  - `normalised` from ECC custody (frontmatter enrichment, MARK-262 metadata)
- **Adaptation note**: The first-party `owasp-top-ten` replaces the retired Claude-Cortex `owasp-top-10` projection. `web-identity` is a new citation-backed first-party skill.

## Rights and Attribution

### First-Party Content

- **Author**: Harley Bartles
- **License**: MIT

### NickCrew/Claude-Cortex Content

- **Upstream source**: NickCrew/Claude-Cortex
- **License**: MIT
- **Redistribution rights**: Per upstream license terms with first-party selection provenance

### Historical ECC Content

- **Upstream source**: ECC (Enterprise Contract Copilot)
- **License**: Per ECC license terms
- **Redistribution rights**: Per upstream license terms with first-party selection provenance
- **Provenance note**: `provenance/ecc.md`

## Boundary

The combined bundle keeps the source families distinct while letting them compose:

- `owasp-top-ten` stays focused on application-risk taxonomy and remediation.
- `web-identity` stays focused on OAuth 2.0 / OIDC flow selection, token validation, and identity-provider integration.
- `secure-coding-practices` stays focused on defensive application coding, input validation, output encoding, secrets handling, and secure defaults.
- `security-testing-patterns` stays focused on validation, security testing strategy, and automation.
- `threat-modeling-techniques` stays focused on pre-implementation risk framing, abuse cases, and trust boundaries.
- `safety-guard` is the retained ECC safety guard complement.
- `security-review` stays distinct from `secure-coding-practices` and `owasp-top-ten`: the pack uses it for general review and cloud infrastructure security, with the support doc projected at `skills/security-review/references/cloud-infrastructure-security.md`.
- The bundle stays out of generic compliance theatre, repo governance, and unrelated implementation domains unless another issue explicitly composes them in.
