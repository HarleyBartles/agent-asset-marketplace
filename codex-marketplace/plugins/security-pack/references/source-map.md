# Security Pack Source Map

This bundle projects the MARK-210 `threat-modeling-techniques` slice from the
retained Codex Cortex custody plugin into a marketplace surface.

Retained custody evidence:

- `sources/third_party/codex-cortex/upstream/README.md`
- `sources/third_party/codex-cortex/upstream/LICENSE`
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

Projected pack skill:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| threat-modeling-techniques | `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/SKILL.md` | `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/SKILL.md` | Adapted from the retained Codex Cortex custody plugin into the installable Security Pack. |

The pack root is an installable Codex plugin projection. It does not replace
the `codex-cortex` custody plugin or the first-party import ledger.

