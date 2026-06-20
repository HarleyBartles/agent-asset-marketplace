# Codex Cortex Provenance

## Source anchor

- Upstream repository: `NickCrew/Claude-Cortex`
- Default branch: `main`
- Resolved commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: MIT

## Custody surface

- Retained snapshot root: `sources/third_party/claude-cortex/upstream/`
- First-party import ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- First-party intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/codex-cortex/`
- Installable plugin projection: `codex-marketplace/plugins/architecture-pack/`
- Installable plugin projection: `codex-marketplace/plugins/api-contracts-pack/`
- Installable plugin projection: `codex-marketplace/plugins/language-patterns-pack/`
- Installable plugin projection: `codex-marketplace/plugins/security-pack/`
- Installable plugin projection: `codex-marketplace/plugins/frontend-pack/`
- Generated install unit: `generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/event-driven-architecture/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/database-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/api-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/openapi-specification/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/secure-coding-practices/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/owasp-top-10/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/security-testing-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/codex-cortex/threat-modeling-techniques/skill.zip`
- Generated install unit: `generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip`
- Generated install unit: `generated/skill-zips/architecture-pack/event-driven-architecture/skill.zip`
- Generated install unit: `generated/skill-zips/architecture-pack/database-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/api-contracts-pack/openapi-specification/skill.zip`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/typescript-advanced-patterns/`
- Generated install unit: `generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`
- Installable plugin projection: `codex-marketplace/plugins/language-patterns-pack/`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/python-testing-patterns/`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/async-python-patterns/`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/python-performance-optimization/`
- Generated install unit: `generated/skill-zips/language-patterns-pack/python-testing-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/language-patterns-pack/async-python-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/language-patterns-pack/python-performance-optimization/skill.zip`
- Generated install unit: `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- Generated install unit: `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
- Generated install unit: `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- Generated install unit: `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/react-performance-optimization/`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/accessibility-audit/`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/ux-review/`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/interaction-design/`
- Retained source snapshot root: `sources/third_party/claude-cortex/upstream/skills/webapp-testing/`
- Generated install unit: `generated/skill-zips/frontend-pack/react-performance-optimization/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/accessibility-audit/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/ux-review/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/interaction-design/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/webapp-testing/skill.zip`

## Boundary

The retained custody surface seeds `cqrs-event-sourcing`, `event-driven-architecture`, `database-design-patterns`, `api-design-patterns`, `openapi-specification`, and the MARK-212 `typescript-advanced-patterns` guidance that is projected through `language-patterns-pack`. MARK-213 adds the Python language/runtime slice through `python-testing-patterns`, `async-python-patterns`, and `python-performance-optimization`. MARK-214 adds the frontend first-wave slice through `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, and `webapp-testing`. The retained `python-testing-patterns` validation rubric stays in source custody only.

## MARK-279 full upstream inventory

The retained Claude-Cortex custody surface at `sources/third_party/claude-cortex/upstream/` holds exactly 18 skill directories, pinned at upstream commit `7892d00e7cb6adf00144a535103b930c772fb2c0` (MIT license). No other Claude-Cortex skills are retained in source custody.

## MARK-279 accepted/projected list by plugin

All 18 retained upstream skills are projected into canonical marketplace plugins. No new projections were added in this PR; all 18 were already projected by prior issues (MARK-172, MARK-200, MARK-201, MARK-204, MARK-205, MARK-207, MARK-210, MARK-212, MARK-213, MARK-214).

| Skill | Projected into |
| --- | --- |
| `accessibility-audit` | `frontend-pack` |
| `api-design-patterns` | `codex-cortex`, `api-contracts-pack` |
| `async-python-patterns` | `language-patterns-pack` |
| `cqrs-event-sourcing` | `codex-cortex`, `architecture-pack` |
| `database-design-patterns` | `codex-cortex`, `architecture-pack` |
| `event-driven-architecture` | `codex-cortex`, `architecture-pack` |
| `interaction-design` | `frontend-pack` |
| `openapi-specification` | `codex-cortex`, `api-contracts-pack` |
| `owasp-top-10` | `security-pack`, `codex-cortex` |
| `python-performance-optimization` | `language-patterns-pack` |
| `python-testing-patterns` | `language-patterns-pack` |
| `react-performance-optimization` | `frontend-pack` |
| `secure-coding-practices` | `security-pack`, `codex-cortex` |
| `security-testing-patterns` | `security-pack`, `codex-cortex` |
| `threat-modeling-techniques` | `security-pack`, `codex-cortex` |
| `typescript-advanced-patterns` | `language-patterns-pack` |
| `ux-review` | `frontend-pack` |
| `webapp-testing` | `frontend-pack` |

## MARK-279 rejected candidates with hard reasons

Every Claude-Cortex candidate not in the 18-skill retained custody is rejected with a hard reason. No useful work is deferred.

| Candidate | Hard reason | Source gap / Existing authority |
| --- | --- | --- |
| `doc-claim-validator` | Not in retained custody; duplicate existing authority | Not snapshotted into `sources/third_party/claude-cortex/upstream/`. Duplicates durable-source doctrine in repo-root `AGENTS.md`. |
| `doc-maintenance` | Not in retained custody; duplicate existing authority | Not snapshotted. Duplicates `house-skills:cleanup-custody`. |
| `repo-cleanup` | Not in retained custody; duplicate existing authority | Not snapshotted. Duplicates `house-skills:cleanup-custody`. |
| `quality-audit` | Not in retained custody; duplicate existing authority | Not snapshotted. Duplicates `unslop-superpowers` and `tools/validate_marketplace.py`. |
| `codanna-codebase-intelligence` | Not in retained custody; violates durable-source doctrine | Not snapshotted. Memory-first/tooling-dependent; conflicts with repo-root `AGENTS.md` durable-source rule. |
| `knowledge-stack` | Not in retained custody; violates durable-source doctrine | Not snapshotted. Memory-first; conflicts with repo-root `AGENTS.md` durable-source rule. |
| `requirements-discovery` | Not in retained custody; duplicate existing authority | Not snapshotted. Duplicates `superpowers-plus:linear-superpowers` and `superpowers-plus:writing-plans`. |
| `mermaid-diagramming` | Not in retained custody | Not snapshotted into `sources/third_party/claude-cortex/upstream/`. |
| `github-actions-workflows` | Not in retained custody | Not snapshotted into `sources/third_party/claude-cortex/upstream/`. |
| product strategy | Not in retained custody | Not snapshotted. |
| market research | Not in retained custody | Not snapshotted. |
| competitor analysis | Not in retained custody | Not snapshotted. |
| UX research/writing | Not in retained custody | Not snapshotted. |
| dashboard design | Not in retained custody | Not snapshotted. |
| frontend design | Not in retained custody | Not snapshotted. |
| user journeys | Not in retained custody | Not snapshotted. |
| documentation/tutorial/research methods | Not in retained custody | Not snapshotted. |
| synthesis | Not in retained custody | Not snapshotted. |
| constructive dissent | Not in retained custody | Not snapshotted. |
| Socratic questioning | Not in retained custody | Not snapshotted. |
| multi-LLM consultation | Not in retained custody | Not snapshotted. |
| blog post | Not in retained custody | Not snapshotted. |
| copywriter | Not in retained custody | Not snapshotted. |
| storyteller | Not in retained custody | Not snapshotted. |
| idea lab | Not in retained custody | Not snapshotted. |
| visual modes | Not in retained custody | Not snapshotted. |
| concept forge | Not in retained custody | Not snapshotted. |
| mashup | Not in retained custody | Not snapshotted. |
| color palette | Not in retained custody | Not snapshotted. |
| canvas design | Not in retained custody | Not snapshotted. |
| microservices | Not in retained custody | Not snapshotted. |
| legacy modernization | Not in retained custody | Not snapshotted. |
| build optimization | Not in retained custody | Not snapshotted. |
| Kubernetes/Helm/Terraform/GitOps | Not in retained custody | Not snapshotted. |
| performance specialists | Not in retained custody | Not snapshotted. |

## MARK-279 child coverage map

| Child | Title | Classification | Evidence |
| --- | --- | --- | --- |
| MARK-189 | Seed security-pack from first-wave security candidates | already satisfied | `security-pack` projects `secure-coding-practices`, `owasp-top-10`, `security-testing-patterns`, `threat-modeling-techniques`. Linear status: Done. |
| MARK-190 | Seed language-patterns-pack from language and runtime skills | already satisfied | `language-patterns-pack` projects `typescript-advanced-patterns`, `python-testing-patterns`, `async-python-patterns`, `python-performance-optimization`. Linear status: Done. |
| MARK-191 | Seed frontend-pack with React and frontend application skills | already satisfied | `frontend-pack` projects `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, `webapp-testing`. Linear status: Done. |
| MARK-192 | Seed cross-repo truth and governance pack | rejected | `doc-claim-validator`, `doc-maintenance`, `repo-cleanup`, `quality-audit` not in retained custody; duplicate `house-skills:cleanup-custody`, `unslop-superpowers`, and `tools/validate_marketplace.py`. Linear status: Duplicate. |
| MARK-193 | Seed source-intelligence-pack from codebase and knowledge candidates | rejected | `codanna-codebase-intelligence` and `knowledge-stack` not in retained custody; violate durable-source doctrine (memory-first). Linear status: Duplicate. |
| MARK-194 | Seed planning-pack from requirements and diagramming candidates | rejected | `requirements-discovery` not in retained custody; duplicates `superpowers-plus:linear-superpowers` and `superpowers-plus:writing-plans`. `mermaid-diagramming` not in retained custody. Linear status: Duplicate. |
| MARK-195 | Seed ci-pack from GitHub Actions workflow guidance | rejected | `github-actions-workflows` not in retained custody. Linear status: Duplicate. |
| MARK-196 | Inventory product, research, UX, and creative Claude-Cortex candidates | rejected | All product/research/UX/creative candidates not in retained custody. Linear status: Duplicate. |
| MARK-197 | Maintain deferred Claude-Cortex specialist parking lot | rejected | All specialist candidates (microservices, legacy modernization, build optimization, Kubernetes/Helm/Terraform/GitOps, performance) not in retained custody. Linear status: Duplicate. |
| MARK-218 | Compare cleanup and quality governance overlaps | already satisfied | Comparison completed; cleanup/quality-audit candidates rejected as duplicates. Linear status: Done. |
| MARK-219 | Project doc claim and maintenance guidance into repo-truth pack | rejected | `doc-claim-validator` and `doc-maintenance` not in retained custody; duplicate `house-skills:cleanup-custody` and durable-source doctrine. Linear status: Duplicate. |
| MARK-221 | Inventory source-intelligence compatibility and source custody fit | rejected | `codanna-codebase-intelligence` and `knowledge-stack` not in retained custody; violate durable-source doctrine. Linear status: Duplicate. |
| MARK-222 | Prove codanna-codebase-intelligence compatibility | rejected | `codanna-codebase-intelligence` not in retained custody; violates durable-source doctrine. Linear status: Duplicate. |
| MARK-223 | Evaluate knowledge-stack durable-source posture | rejected | `knowledge-stack` not in retained custody; violates durable-source doctrine. Linear status: Duplicate. |
| MARK-224 | Compare requirements-discovery against issue shaping stack | rejected | `requirements-discovery` not in retained custody; duplicates `superpowers-plus:linear-superpowers` and `superpowers-plus:writing-plans`. Linear status: Duplicate. |
| MARK-225 | Evaluate mermaid-diagramming planning value | rejected | `mermaid-diagramming` not in retained custody. Linear status: Duplicate. |

## MARK-279 retained existing skills

No existing first-party or third-party plugin content was removed or replaced. All 18 Claude-Cortex skills retain their existing projections across `codex-cortex`, `architecture-pack`, `api-contracts-pack`, `language-patterns-pack`, `security-pack`, and `frontend-pack`. This PR corrects provenance path drift, updates the retained snapshot README to reflect the full 18-skill inventory, and records the consolidated child coverage map proving the full drain.
