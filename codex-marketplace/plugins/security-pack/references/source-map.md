# Security Pack Source Map

This bundle projects the MARK-207 `secure-coding-practices`,
`owasp-top-10`, and `security-testing-patterns` slices plus the MARK-210
`threat-modeling-techniques` slice from the retained Codex Cortex custody
plugin into a marketplace surface.

Retained custody evidence:

- `sources/third_party/codex-cortex/upstream/README.md`
- `sources/third_party/codex-cortex/upstream/LICENSE`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/references/authentication.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/references/cryptography.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/references/dependencies.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/references/error-handling.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/references/input-validation.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/references/output-encoding.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/references/secure-defaults.md`
- `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/validation/rubric.yaml`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/authentication-failures.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/broken-access-control.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/cryptographic-failures.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/injection.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/insecure-design.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/integrity-failures.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/logging-monitoring.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/prevention-strategies.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/security-misconfiguration.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/ssrf.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/vulnerable-components.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/references/assessment-workflow.md`
- `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/validation/rubric.yaml`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/references/api-security.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/references/automation-pipeline.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/references/dast.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/references/fuzzing.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/references/penetration-testing.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/references/sca.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/references/sast.md`
- `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/validation/rubric.yaml`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/attack-trees.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/data-flow-diagrams.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/dread-scoring.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/mitigation-strategies.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-spoofing.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-tampering.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-repudiation.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-disclosure.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-dos.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-elevation.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/tools-and-process.md`
- `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/validation/rubric.yaml`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| secure-coding-practices | `sources/third_party/codex-cortex/upstream/skills/secure-coding-practices/SKILL.md` | `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/SKILL.md` | Adapted from the retained Codex Cortex custody plugin into the installable Security Pack. |
| owasp-top-10 | `sources/third_party/codex-cortex/upstream/skills/owasp-top-10/SKILL.md` | `codex-marketplace/plugins/security-pack/skills/owasp-top-10/SKILL.md` | Adapted from the retained Codex Cortex custody plugin into the installable Security Pack. |
| security-testing-patterns | `sources/third_party/codex-cortex/upstream/skills/security-testing-patterns/SKILL.md` | `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/SKILL.md` | Adapted from the retained Codex Cortex custody plugin into the installable Security Pack. |
| threat-modeling-techniques | `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/SKILL.md` | `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/SKILL.md` | Adapted from the retained Codex Cortex custody plugin into the installable Security Pack. |

The pack root is an installable Codex plugin projection. It does not replace
the `codex-cortex` custody plugin or the first-party import ledger.

