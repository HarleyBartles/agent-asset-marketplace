# Language Patterns Pack Source Map

This bundle projects the MARK-212 `typescript-advanced-patterns` slice from the
retained Claude-Cortex custody plugin into a marketplace surface. The retained
upstream skill uses plugin-root-relative reference paths; the projected pack
normalizes those references to skill-root-relative paths and adds canonical
`agents/openai.yaml` metadata in the installable shape.

Retained custody evidence:

- `sources/third_party/codex-cortex/upstream/README.md`
- `sources/third_party/codex-cortex/upstream/LICENSE`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/advanced-generics.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/branded-types.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/builder-pattern.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/common-pitfalls.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/conditional-types.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/decorators.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/discriminated-unions.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/mapped-types.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/performance-best-practices.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/template-literal-types.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/testing-types.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/type-guards.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/type-inference.md`
- `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/references/utility-types.md`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Projected pack skill:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| typescript-advanced-patterns | `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/SKILL.md` | Adapted projection that normalizes plugin-root-relative reference paths to skill-root-relative references. |

The pack root is an installable Codex plugin projection. It does not replace
the `codex-cortex` custody plugin or the first-party import ledger.
