# Language Patterns Pack Source Map

This bundle projects the MARK-212 TypeScript slice and the MARK-213 Python language/runtime slice from the retained Claude-Cortex custody plugin, and the MARK-246 ECC language/framework skills slice from retained ECC custody, into a marketplace surface. The retained Claude-Cortex upstream skills use plugin-root-relative reference paths; the projected pack normalizes those references to skill-root-relative paths and adds canonical `agents/openai.yaml` metadata in the installable shape. ECC skills are projected verbatim from retained ECC source custody with MIT license attribution to upstream author affaan-m/ECC.

Retained custody evidence:

### Claude-Cortex

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

### ECC

- `sources/third_party/ecc/upstream/manifest.json`
- `sources/third_party/ecc/upstream/skills/bun-runtime/SKILL.md`
- `sources/third_party/ecc/upstream/skills/cpp-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/csharp-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/dart-flutter-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/django-celery/SKILL.md`
- `sources/third_party/ecc/upstream/skills/django-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/django-tdd/SKILL.md`
- `sources/third_party/ecc/upstream/skills/fastapi-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/flutter-dart-code-review/SKILL.md`
- `sources/third_party/ecc/upstream/skills/fsharp-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/golang-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/kotlin-coroutines-flows/SKILL.md`
- `sources/third_party/ecc/upstream/skills/kotlin-ktor-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/kotlin-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/laravel-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/laravel-plugin-discovery/SKILL.md`
- `sources/third_party/ecc/upstream/skills/laravel-tdd/SKILL.md`
- `sources/third_party/ecc/upstream/skills/nestjs-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/perl-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/python-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/pytorch-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/quarkus-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/quarkus-tdd/SKILL.md`
- `sources/third_party/ecc/upstream/skills/rust-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/springboot-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/springboot-tdd/SKILL.md`
- `sources/third_party/ecc/upstream/skills/swift-protocol-di-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/tinystruct-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/tdd-workflow/SKILL.md`

First-party custody:

### Claude-Cortex

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

### ECC

- `docs/superpowers/plans/mark-241-skill-categorization.json`
- `provenance/ecc.md`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| typescript-advanced-patterns | `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/SKILL.md` | Adapted projection that normalizes plugin-root-relative reference paths to skill-root-relative references. |
| python-testing-patterns | `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/python-testing-patterns/SKILL.md` | Adapted projection that normalizes plugin-root-relative reference paths to skill-root-relative references. |
| async-python-patterns | `sources/third_party/codex-cortex/upstream/skills/async-python-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/async-python-patterns/SKILL.md` | Direct projection of the retained async runtime guidance. |
| python-performance-optimization | `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/python-performance-optimization/SKILL.md` | Adapted projection that normalizes plugin-root-relative reference paths to skill-root-relative references. |
| bun-runtime | `sources/third_party/ecc/upstream/skills/bun-runtime/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/bun-runtime/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| cpp-testing | `sources/third_party/ecc/upstream/skills/cpp-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/cpp-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| csharp-testing | `sources/third_party/ecc/upstream/skills/csharp-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/csharp-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| dart-flutter-patterns | `sources/third_party/ecc/upstream/skills/dart-flutter-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/dart-flutter-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| django-celery | `sources/third_party/ecc/upstream/skills/django-celery/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/django-celery/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| django-patterns | `sources/third_party/ecc/upstream/skills/django-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/django-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| django-tdd | `sources/third_party/ecc/upstream/skills/django-tdd/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/django-tdd/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| fastapi-patterns | `sources/third_party/ecc/upstream/skills/fastapi-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/fastapi-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| flutter-dart-code-review | `sources/third_party/ecc/upstream/skills/flutter-dart-code-review/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/flutter-dart-code-review/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| fsharp-testing | `sources/third_party/ecc/upstream/skills/fsharp-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/fsharp-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| golang-testing | `sources/third_party/ecc/upstream/skills/golang-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/golang-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| kotlin-coroutines-flows | `sources/third_party/ecc/upstream/skills/kotlin-coroutines-flows/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/kotlin-coroutines-flows/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| kotlin-ktor-patterns | `sources/third_party/ecc/upstream/skills/kotlin-ktor-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/kotlin-ktor-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| kotlin-testing | `sources/third_party/ecc/upstream/skills/kotlin-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/kotlin-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| laravel-patterns | `sources/third_party/ecc/upstream/skills/laravel-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/laravel-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| laravel-plugin-discovery | `sources/third_party/ecc/upstream/skills/laravel-plugin-discovery/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/laravel-plugin-discovery/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| laravel-tdd | `sources/third_party/ecc/upstream/skills/laravel-tdd/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/laravel-tdd/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| nestjs-patterns | `sources/third_party/ecc/upstream/skills/nestjs-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/nestjs-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| perl-testing | `sources/third_party/ecc/upstream/skills/perl-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/perl-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| python-testing | `sources/third_party/ecc/upstream/skills/python-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/python-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| pytorch-patterns | `sources/third_party/ecc/upstream/skills/pytorch-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/pytorch-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| quarkus-patterns | `sources/third_party/ecc/upstream/skills/quarkus-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/quarkus-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| quarkus-tdd | `sources/third_party/ecc/upstream/skills/quarkus-tdd/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/quarkus-tdd/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| rust-testing | `sources/third_party/ecc/upstream/skills/rust-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/rust-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| springboot-patterns | `sources/third_party/ecc/upstream/skills/springboot-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/springboot-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| springboot-tdd | `sources/third_party/ecc/upstream/skills/springboot-tdd/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/springboot-tdd/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| swift-protocol-di-testing | `sources/third_party/ecc/upstream/skills/swift-protocol-di-testing/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/swift-protocol-di-testing/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| tinystruct-patterns | `sources/third_party/ecc/upstream/skills/tinystruct-patterns/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/tinystruct-patterns/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |
| tdd-workflow | `sources/third_party/ecc/upstream/skills/tdd-workflow/SKILL.md` | `codex-marketplace/plugins/language-patterns-pack/skills/tdd-workflow/SKILL.md` | Verbatim projection from ECC custody with MIT license attribution to affaan-m/ECC. |

The pack root is an installable Codex plugin projection. It does not replace the `codex-cortex` or `ecc` custody plugins or the first-party import ledgers.