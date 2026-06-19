# Source

This plugin projects retained Codex Cortex security foundations and retained
ECC security-oriented skills into a Codex marketplace pack.

## Source custody

- Retained Codex Cortex upstream root: `sources/third_party/codex-cortex/upstream/`
- Retained Codex Cortex skill roots:
  `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/`
  `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/`
  `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/`
  `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/`
- Retained ECC upstream root: `sources/third_party/ecc/upstream/`
- Retained ECC skill roots:
  `sources/third_party/ecc/upstream/skills/defi-amm-security/`
  `sources/third_party/ecc/upstream/skills/django-security/`
  `sources/third_party/ecc/upstream/skills/laravel-security/`
  `sources/third_party/ecc/upstream/skills/llm-trading-agent-security/`
  `sources/third_party/ecc/upstream/skills/network-config-validation/`
  `sources/third_party/ecc/upstream/skills/perl-security/`
  `sources/third_party/ecc/upstream/skills/prediction-market-risk-review/`
  `sources/third_party/ecc/upstream/skills/quarkus-security/`
  `sources/third_party/ecc/upstream/skills/safety-guard/`
  `sources/third_party/ecc/upstream/skills/security-bounty-hunter/`
  `sources/third_party/ecc/upstream/skills/security-review/`
  `sources/third_party/ecc/upstream/skills/security-scan/`
  `sources/third_party/ecc/upstream/skills/springboot-security/`
- First-party ledgers:
  - `sources/first_party/skills/codex-cortex/intake.json`
  - `sources/first_party/skills/codex-cortex/decisions.json`
  - `sources/first_party/skills/codex-cortex/decisions.md`
- Provenance notes:
  - `provenance/codex-cortex.md`
  - `provenance/ecc.md`

## Projection surfaces

- Codex Cortex projection:
  `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/`
  `codex-marketplace/plugins/security-pack/skills/owasp-top-10/`
  `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/`
  `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/`
- ECC projection:
  `codex-marketplace/plugins/security-pack/skills/defi-amm-security/`
  `codex-marketplace/plugins/security-pack/skills/django-security/`
  `codex-marketplace/plugins/security-pack/skills/laravel-security/`
  `codex-marketplace/plugins/security-pack/skills/llm-trading-agent-security/`
  `codex-marketplace/plugins/security-pack/skills/network-config-validation/`
  `codex-marketplace/plugins/security-pack/skills/perl-security/`
  `codex-marketplace/plugins/security-pack/skills/prediction-market-risk-review/`
  `codex-marketplace/plugins/security-pack/skills/quarkus-security/`
  `codex-marketplace/plugins/security-pack/skills/safety-guard/`
  `codex-marketplace/plugins/security-pack/skills/security-bounty-hunter/`
  `codex-marketplace/plugins/security-pack/skills/security-review/`
  `codex-marketplace/plugins/security-pack/skills/security-scan/`
  `codex-marketplace/plugins/security-pack/skills/springboot-security/`
- Security Pack source map: `codex-marketplace/plugins/security-pack/references/source-map.md`
- Generated install units:
  `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
  `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
  `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
  `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`
  `generated/skill-zips/security-pack/defi-amm-security/skill.zip`
  `generated/skill-zips/security-pack/django-security/skill.zip`
  `generated/skill-zips/security-pack/laravel-security/skill.zip`
  `generated/skill-zips/security-pack/llm-trading-agent-security/skill.zip`
  `generated/skill-zips/security-pack/network-config-validation/skill.zip`
  `generated/skill-zips/security-pack/perl-security/skill.zip`
  `generated/skill-zips/security-pack/prediction-market-risk-review/skill.zip`
  `generated/skill-zips/security-pack/quarkus-security/skill.zip`
  `generated/skill-zips/security-pack/safety-guard/skill.zip`
  `generated/skill-zips/security-pack/security-bounty-hunter/skill.zip`
  `generated/skill-zips/security-pack/security-review/skill.zip`
  `generated/skill-zips/security-pack/security-scan/skill.zip`
  `generated/skill-zips/security-pack/springboot-security/skill.zip`

## Boundary

The combined bundle keeps the source families distinct while letting them
compose:

- `secure-coding-practices` stays focused on defensive application coding,
  input validation, output encoding, secrets handling, and secure defaults.
- `owasp-top-10` stays focused on application-risk taxonomy and remediation.
- `security-testing-patterns` stays focused on validation, security testing
  strategy, and automation.
- `threat-modeling-techniques` stays focused on pre-implementation risk
  framing, abuse cases, and trust boundaries.
- `defi-amm-security`, `django-security`, `laravel-security`,
  `llm-trading-agent-security`, `network-config-validation`, `perl-security`,
  `prediction-market-risk-review`, `quarkus-security`, `safety-guard`,
  `security-bounty-hunter`, `security-review`, `security-scan`, and
  `springboot-security` stay focused on their respective ECC-adapted review,
  safety, and hardening concerns.
- `security-review` stays distinct from `secure-coding-practices` and
  `owasp-top-10`: the pack uses it for general review and cloud infrastructure
  security, with the support doc projected at
  `skills/security-review/references/cloud-infrastructure-security.md`.
- The bundle stays out of generic compliance theatre, repo governance, and
  unrelated implementation domains unless another issue explicitly composes
  them in.
