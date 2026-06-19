# Security Pack

This plugin bundle projects retained Codex Cortex security foundations and
retained ECC security-oriented skills into an installable Codex marketplace
pack.

## Bundle contents

- Codex Cortex security foundations:
  - `secure-coding-practices`
  - `owasp-top-10`
  - `security-testing-patterns`
  - `threat-modeling-techniques`
- ECC security-oriented skills:
  - `defi-amm-security`
  - `django-security`
  - `laravel-security`
  - `llm-trading-agent-security`
  - `network-config-validation`
  - `perl-security`
  - `prediction-market-risk-review`
  - `quarkus-security`
  - `safety-guard`
  - `security-bounty-hunter`
  - `security-review`
  - `security-scan`
  - `springboot-security`
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
- `defi-amm-security` owns DeFi AMM security review and attack-surface
  analysis.
- `django-security` owns Django-specific security review and hardening.
- `laravel-security` owns Laravel-specific security review and hardening.
- `llm-trading-agent-security` owns LLM trading agent security review and
  guardrails.
- `network-config-validation` owns network configuration validation and
  security checks.
- `perl-security` owns Perl-specific security review and hardening.
- `prediction-market-risk-review` owns prediction-market security and risk
  review.
- `quarkus-security` owns Quarkus security review and hardening.
- `safety-guard` owns safe-operation guidance for avoiding destructive
  actions.
- `security-bounty-hunter` owns security bounty hunting and exploit-oriented
  review workflows.
- `security-review` owns general security review and cloud infrastructure
  security checks. It stays distinct from `secure-coding-practices` and
  `owasp-top-10` so code-level hardening, taxonomy, and infrastructure review
  remain composable rather than collapsed.
- `security-scan` owns configuration scanning and AgentShield-based security
  hygiene checks.
- `springboot-security` owns Spring Boot security review and hardening.
- The bundle stays out of generic compliance theatre, repo governance, and
  unrelated implementation domains unless another issue explicitly composes
  them in.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zip is generated under:

- `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
- `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`
- `generated/skill-zips/security-pack/defi-amm-security/skill.zip`
- `generated/skill-zips/security-pack/django-security/skill.zip`
- `generated/skill-zips/security-pack/laravel-security/skill.zip`
- `generated/skill-zips/security-pack/llm-trading-agent-security/skill.zip`
- `generated/skill-zips/security-pack/network-config-validation/skill.zip`
- `generated/skill-zips/security-pack/perl-security/skill.zip`
- `generated/skill-zips/security-pack/prediction-market-risk-review/skill.zip`
- `generated/skill-zips/security-pack/quarkus-security/skill.zip`
- `generated/skill-zips/security-pack/safety-guard/skill.zip`
- `generated/skill-zips/security-pack/security-bounty-hunter/skill.zip`
- `generated/skill-zips/security-pack/security-review/skill.zip`
- `generated/skill-zips/security-pack/security-scan/skill.zip`
- `generated/skill-zips/security-pack/springboot-security/skill.zip`
