# Source

This plugin is the MARK-172, MARK-200, MARK-201, MARK-204, MARK-205,
MARK-207, MARK-210, and MARK-242 Codex Cortex custody surface for the retained
Claude-Cortex `cqrs-event-sourcing` seed, `event-driven-architecture` import,
`database-design-patterns` import, `api-design-patterns` import,
`openapi-specification` import, `secure-coding-practices`, `owasp-top-10`, and
`security-testing-patterns` imports, `threat-modeling-techniques` import, and
the ECC agent/eval workflow skills projected under MARK-242.

## Upstream basis

- Repo: `NickCrew/Claude-Cortex`
- URL: <https://github.com/NickCrew/Claude-Cortex.git>
- Pinned commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: `MIT`
- Retained snapshot root: `sources/third_party/claude-cortex/upstream/`

## First-party custody

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`

## ECC agent/eval skills (MARK-242)

ECC (affaan-m/ECC) agent/eval workflow skills projected into this plugin under
MARK-242.

- Upstream repo: `affaan-m/ECC`
- URL: <https://github.com/affaan-m/ECC.git>
- Pinned commit: `ceca28852e5b31edbbf66ebccc8fd163dd14208e`
- License: `MIT`
- Retained snapshot root: `sources/third_party/ecc/upstream/skills/`
- Categorization: `docs/superpowers/plans/mark-241-skill-categorization.json`

Projected ECC skills (29 total):

- agent-architecture-audit
- agent-eval
- agent-self-evaluation
- agentic-engineering
- agentic-os
- ai-regression-testing
- autonomous-agent-harness
- autonomous-loops
- benchmark
- benchmark-methodology
- benchmark-optimization-loop
- context-budget
- continuous-agent-loop
- dynamic-workflow-mode
- eval-harness
- gan-style-harness
- gateguard
- iterative-retrieval
- orch-add-feature
- orch-build-mvp
- orch-change-feature
- orch-fix-defect
- orch-pipeline
- orch-refine-code
- plan-orchestrate
- prompt-optimizer
- ralphinho-rfc-pipeline
- santa-method
- verification-loop

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/codex-cortex/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/api-design-patterns/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/secure-coding-practices/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/owasp-top-10/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/security-testing-patterns/`
- Skill root:
  `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/agent-architecture-audit/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/agent-eval/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/agent-self-evaluation/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/agentic-engineering/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/agentic-os/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/ai-regression-testing/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/autonomous-agent-harness/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/autonomous-loops/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/benchmark/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/benchmark-methodology/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/benchmark-optimization-loop/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/context-budget/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/continuous-agent-loop/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/dynamic-workflow-mode/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/eval-harness/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/gan-style-harness/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/gateguard/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/iterative-retrieval/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/orch-add-feature/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/orch-build-mvp/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/orch-change-feature/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/orch-fix-defect/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/orch-pipeline/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/orch-refine-code/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/plan-orchestrate/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/prompt-optimizer/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/ralphinho-rfc-pipeline/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/santa-method/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/verification-loop/`
- Generated install units: `generated/skill-zips/codex-cortex/<skill-name>/skill.zip`

## Boundary

Only the retained source skills are kept here. Later Claude-Cortex candidates
stay out of scope for MARK-172, MARK-200, MARK-201, MARK-204, MARK-205,
MARK-207, and MARK-210. ECC skills beyond the 29 agent/eval workflow skills
projected under MARK-242 stay out of scope.
