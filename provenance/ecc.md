# ECC Provenance

## Source anchor

- Upstream repository: `affaan-m/ECC`
- Default branch: `main`
- Resolved commit: `ceca28852e5b31edbbf66ebccc8fd163dd14208e`
- License: see retained upstream snapshot

## Custody surface

- Retained snapshot root: `sources/third_party/ecc/upstream/skills/`
- Retained machine manifest: `sources/third_party/ecc/upstream/manifest.json`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/security-pack/`
- Generated install units:
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

## Boundary

The historical ECC projection contributed security review, security scan, safe-operation,
config validation, bounty-hunter, framework-specific security, and
risk-review guidance to `security-pack`. MARK-295 removed the active ECC projections from all plugins, but retained ECC custody stays available for deliberate follow-on reprojection work. MARK-301 is the place to reintroduce any fresh ECC-derived projections after source inspection, manifest updates, provenance updates, and validator updates. Compliance-only or unrelated implementation skills stay out of this projection slice.
