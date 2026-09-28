# Test suites

The suite directory names identify what is being tested:

| Suite                 | Owns                                                      | When it runs              |
| --------------------- | --------------------------------------------------------- | ------------------------- |
| `build/`              | Plugin definition and assembly code in `src/marketplace/` | Commit and PR gate        |
| `repository/`         | This repository's own command and validation tools        | Commit and PR gate        |
| `shipping/`           | Built plugins as installable packages                     | Commit and PR gate        |
| `evaluation-harness/` | Shared pressure-campaign runner and scanner               | When that harness changes |

Skill code, instruction behavior, and pressure cases belong to the skill under `skills/<skill-id>/tests/`. Run the changed skill's tests explicitly. The builder copies ship-ready tests with that skill and excludes `tests/evaluator-only/`, caches, and run results.

The `ci` target invokes the three commit-gated suites separately. Default pytest discovery covers those three suites only; it does not collect every test file in the repository.
