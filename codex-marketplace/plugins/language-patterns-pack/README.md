# Language Patterns Pack

This plugin bundle projects the MARK-212 TypeScript slice and the MARK-213 Python language/runtime slice from the retained Claude-Cortex custody plugin into an installable Codex marketplace pack.

## Bundle contents

- `typescript-advanced-patterns`
- `python-testing-patterns`
- `async-python-patterns`
- `python-performance-optimization`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `typescript-advanced-patterns` carries TypeScript language and runtime guidance.
- `python-testing-patterns` carries Python testing idioms, fixtures, mocking, parametrization, property-based testing, and async test patterns.
- `async-python-patterns` carries Python async and concurrency guidance.
- `python-performance-optimization` carries Python profiling, algorithmic optimization, memory optimization, and acceleration guidance.
- The bundle does not own frontend, architecture, database, security, repo governance, CI, or generic engineering doctrine.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-testing-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/async-python-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-performance-optimization/skill.zip`

and can be installed directly from those artifacts.