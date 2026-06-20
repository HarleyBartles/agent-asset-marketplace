# Security Pack Source Map

This bundle harmonizes retained Codex Cortex security foundations with retained
ECC security-oriented skills into a marketplace surface.

Harmonization notes:

- `secure-coding-practices` stays at the code-hardening layer.
- `owasp-top-10` stays at the application-risk taxonomy layer.
- `security-testing-patterns` stays at the validation and testing layer.
- `threat-modeling-techniques` stays at the design-time risk-framing layer.
- `security-review` stays distinct from `secure-coding-practices` and
  `owasp-top-10`; it owns general review and cloud infrastructure security, and
  its support doc is projected at
  `codex-marketplace/plugins/security-pack/skills/security-review/references/cloud-infrastructure-security.md`.
- Detailed file-level projections and source-file inventories are captured in
  `references/bundle-manifest.json`.

Retained Codex Cortex custody:

- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/`

Retained ECC custody:

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
- `sources/third_party/ecc/upstream/skills/security-review/cloud-infrastructure-security.md`
- `sources/third_party/ecc/upstream/skills/security-scan/`
- `sources/third_party/ecc/upstream/skills/springboot-security/`

Projected pack skills:

## Codex Cortex projection

| Skill | Source path | Pack path | Content mode | Source origin | Upstream author | Upstream license | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| secure-coding-practices | `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/` | `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/` | verbatim | Codex Cortex | NickCrew | MIT | Retained code-hardening foundation, kept distinct from infrastructure review. |
| owasp-top-10 | `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/` | `codex-marketplace/plugins/security-pack/skills/owasp-top-10/` | verbatim | Codex Cortex | NickCrew | MIT | Retained OWASP taxonomy and remediation layer. |
| security-testing-patterns | `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/` | `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/` | verbatim | Codex Cortex | NickCrew | MIT | Retained security validation and testing layer. |
| threat-modeling-techniques | `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/` | `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/` | verbatim | Codex Cortex | NickCrew | MIT | Retained design-time risk-framing layer. |

## ECC projection

| Skill | Source path | Pack path | Content mode | Source origin | Upstream author | Upstream license | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| defi-amm-security | `sources/third_party/ecc/upstream/skills/defi-amm-security/` | `codex-marketplace/plugins/security-pack/skills/defi-amm-security/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the DeFi AMM review slice. |
| django-security | `sources/third_party/ecc/upstream/skills/django-security/` | `codex-marketplace/plugins/security-pack/skills/django-security/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the Django hardening slice. |
| laravel-security | `sources/third_party/ecc/upstream/skills/laravel-security/` | `codex-marketplace/plugins/security-pack/skills/laravel-security/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the Laravel hardening slice. |
| llm-trading-agent-security | `sources/third_party/ecc/upstream/skills/llm-trading-agent-security/` | `codex-marketplace/plugins/security-pack/skills/llm-trading-agent-security/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the LLM trading-agent guardrails slice. |
| network-config-validation | `sources/third_party/ecc/upstream/skills/network-config-validation/` | `codex-marketplace/plugins/security-pack/skills/network-config-validation/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the network config validation slice. |
| perl-security | `sources/third_party/ecc/upstream/skills/perl-security/` | `codex-marketplace/plugins/security-pack/skills/perl-security/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the Perl hardening slice. |
| prediction-market-risk-review | `sources/third_party/ecc/upstream/skills/prediction-market-risk-review/` | `codex-marketplace/plugins/security-pack/skills/prediction-market-risk-review/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the prediction-market risk slice. |
| quarkus-security | `sources/third_party/ecc/upstream/skills/quarkus-security/` | `codex-marketplace/plugins/security-pack/skills/quarkus-security/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the Quarkus hardening slice. |
| safety-guard | `sources/third_party/ecc/upstream/skills/safety-guard/` | `codex-marketplace/plugins/security-pack/skills/safety-guard/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the safe-operation overlay. |
| security-bounty-hunter | `sources/third_party/ecc/upstream/skills/security-bounty-hunter/` | `codex-marketplace/plugins/security-pack/skills/security-bounty-hunter/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the exploit-oriented review slice. |
| security-review | `sources/third_party/ecc/upstream/skills/security-review/` | `codex-marketplace/plugins/security-pack/skills/security-review/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the general security review slice. |
| security-review support doc | `sources/third_party/ecc/upstream/skills/security-review/cloud-infrastructure-security.md` | `codex-marketplace/plugins/security-pack/skills/security-review/references/cloud-infrastructure-security.md` | verbatim | ECC | Affaan Mustafa | MIT | Projected through the skill-local `references/` adapter path. |
| security-scan | `sources/third_party/ecc/upstream/skills/security-scan/` | `codex-marketplace/plugins/security-pack/skills/security-scan/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the configuration scanning slice. |
| springboot-security | `sources/third_party/ecc/upstream/skills/springboot-security/` | `codex-marketplace/plugins/security-pack/skills/springboot-security/` | verbatim | ECC | Affaan Mustafa | MIT | Copied verbatim into the combined Security Pack as the Spring Boot hardening slice. |

The pack root is an installable Codex plugin projection. It does not replace
either retained custody tree.
