# Language Patterns Pack Source Map

This bundle projects the MARK-212 TypeScript slice and the MARK-213 Python language/runtime slice from the retained Claude-Cortex custody plugin into a marketplace surface. The retained upstream skills use plugin-root-relative reference paths; the projected pack normalizes those references to skill-root-relative paths and adds canonical `agents/openai.yaml` metadata in the installable shape.

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
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/pytest-fundamentals.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/fixtures.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/parametrized-tests.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/mocking.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/async-testing.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/property-based-testing.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/monkeypatch.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/test-organization.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/coverage.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/integration-testing.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/references/best-practices.md`
- `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/validation/rubric.yaml` (retained source-only)
- `sources/third_party/codex-cortex/upstream/skills/async-python-patterns/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/references/acceleration.md`
- `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/references/algorithms.md`
- `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/references/memory.md`
- `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/references/profiling.md`
- `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/references/string-io.md`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| typescript-advanced-patterns | `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/SKILL.md` | Adapted projection that normalizes plugin-root-relative reference paths to skill-root-relative references. |
| python-testing-patterns | `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/python-testing-patterns/SKILL.md` | Adapted projection that normalizes plugin-root-relative reference paths to skill-root-relative references. |
| async-python-patterns | `sources/third_party/codex-cortex/upstream/skills/async-python-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/async-python-patterns/SKILL.md` | Direct projection of the retained async runtime guidance. |
| python-performance-optimization | `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/python-performance-optimization/SKILL.md` | Adapted projection that normalizes plugin-root-relative reference paths to skill-root-relative references. |

The pack root is an installable Codex plugin projection. It does not replace the `codex-cortex` custody plugin or the first-party import ledger.