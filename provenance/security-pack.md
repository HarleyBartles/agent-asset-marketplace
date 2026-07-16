# Security Pack Provenance

## Summary

The Security Pack historically projected retained NickCrew/Claude-Cortex security foundations and retained ECC security-oriented skills into a Codex marketplace pack. MARK-295 removed the active ECC slice.

## Source Custody

### Retained NickCrew/Claude-Cortex Upstream

- **Upstream root**: `sources/third_party/claude-cortex/upstream/`
- **Retained skill roots**:
  - `sources/third_party/claude-cortex/upstream/skills/secure-coding-practices/`
  - `sources/third_party/claude-cortex/upstream/skills/owasp-top-10/`
  - `sources/third_party/claude-cortex/upstream/skills/security-testing-patterns/`
  - `sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques/`

### Historical ECC Upstream

- **Upstream root**: `sources/third_party/ecc/upstream/`
- **Retained skill roots**:
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

### NickCrew/Claude-Cortex Projection

- `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/`
- `codex-marketplace/plugins/security-pack/skills/owasp-top-10/`
- `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/`
- `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/`

### Historical ECC Projection

- `codex-marketplace/plugins/security-pack/skills/defi-amm-security/`
- `codex-marketplace/plugins/security-pack/skills/django-security/`
- `codex-marketplace/plugins/security-pack/skills/laravel-security/`
- `codex-marketplace/plugins/security-pack/skills/llm-trading-agent-security/`
- `codex-marketplace/plugins/security-pack/skills/network-config-validation/`
- `codex-marketplace/plugins/security-pack/skills/perl-security/`
- `codex-marketplace/plugins/security-pack/skills/prediction-market-risk-review/`
- `codex-marketplace/plugins/security-pack/skills/quarkus-security/`
- `codex-marketplace/plugins/security-pack/skills/safety-guard/`
- `codex-marketplace/plugins/security-pack/skills/security-bounty-hunter/`
- `codex-marketplace/plugins/security-pack/skills/security-review/`
- `codex-marketplace/plugins/security-pack/skills/security-scan/`
- `codex-marketplace/plugins/security-pack/skills/springboot-security/`

- **Security Pack source map**: `codex-marketplace/plugins/security-pack/references/source-map.md`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `security-pack`
- **Display name**: `Security Pack`
- **Marketplace category**: `Productivity`
- **Content mode**:
  - `normalised` from NickCrew/Claude-Cortex custody (path normalization, frontmatter enrichment, MARK-262 metadata)
  - `normalised` from ECC custody (frontmatter enrichment, MARK-262 metadata)
- **Adaptation note**: The ECC slice was removed in MARK-295; the remaining NickCrew/Claude-Cortex security foundations stay in place

## Rights and Attribution

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

- `secure-coding-practices` stays focused on defensive application coding, input validation, output encoding, secrets handling, and secure defaults.
- `owasp-top-10` stays focused on application-risk taxonomy and remediation.
- `security-testing-patterns` stays focused on validation, security testing strategy, and automation.
- `threat-modeling-techniques` stays focused on pre-implementation risk framing, abuse cases, and trust boundaries.
- ECC skills were removed from the active bundle in MARK-295; follow-up reprojection can reconsider the slice after fresh source inspection.
- `security-review` stays distinct from `secure-coding-practices` and `owasp-top-10`: the pack uses it for general review and cloud infrastructure security, with the support doc projected at `skills/security-review/references/cloud-infrastructure-security.md`.
- The bundle stays out of generic compliance theatre, repo governance, and unrelated implementation domains unless another issue explicitly composes them in.
