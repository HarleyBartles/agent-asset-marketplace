# Codex Cortex Provenance

## Source anchor

- Upstream repository: `NickCrew/Claude-Cortex`
- Default branch: `main`
- Resolved commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: MIT

## Custody surface

- Full upstream mirror root: `sources/third_party/claude-cortex/upstream/`
- First-party import ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- First-party intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Full upstream custody inventory

The full Claude-Cortex upstream is mirrored into source custody at
`sources/third_party/claude-cortex/upstream/` at pinned commit
`7892d00e7cb6adf00144a535103b930c772fb2c0` (MIT license).

The mirror includes all 149 skill directories plus the full upstream tree
(agents, rules, hooks, Python CLI, tests, docs, schemas, configuration).

### All 149 upstream skill directories in custody

`.system`, `accessibility-audit`, `agent-loops`, `ai-tells-review`,
`ai-tells-scan`, `api-design-patterns`, `api-gateway-patterns`,
`architectural-analysis`, `async-python-patterns`, `atlas-crew-tasks`,
`atomic-commits`, `backlog-md`, `blog-post`, `brand-library-architect`,
`build-optimization`, `business-analyst`, `canvas-design`, `chart-builder`,
`codanna-codebase-intelligence`, `code-explanation`, `code-quality-workflow`,
`codex-code-review`, `collaboration`, `color-palette`, `community`,
`competitor-analyst`, `compliance-audit`, `condition-based-waiting`,
`constructive-dissent`, `copywriter`, `cortex-skills-loop`,
`cqrs-event-sourcing`, `dashboard-designer`, `database-design-patterns`,
`dataset-curator`, `decision-maker`, `defense-in-depth`, `design-critiquer`,
`design-journey-review`, `design-system-architecture`, `development-estimation`,
`dev-workflows`, `dispatching-parallel-agents`, `doc-architecture-review`,
`doc-claim-validator`, `doc-completeness-audit`, `doc-health-audit`,
`doc-maintenance`, `doc-quality-review`, `documentation-production`,
`document-skills`, `email-drafter`, `eval-designer`, `evaluator-optimizer`,
`event-driven-architecture`, `fact-checker`, `feature-implementation`,
`finishing-a-development-branch`, `frontend-design`, `github-actions-workflows`,
`git-ops`, `gitops-workflows`, `helm-chart-patterns`, `html-seo-review`,
`implementation-workflow`, `incident-response`, `interaction-design`,
`internal-comms`, `justfile-author`, `knowledge-stack`, `knowledge-synthesis`,
`kubernetes-deployment-patterns`, `kubernetes-security-policies`,
`legacy-modernization`, `mapping-suite`, `market-researcher`,
`mermaid-diagramming`, `microservices-patterns`, `model-comparator`,
`multi-llm-consult`, `multi-perspective-analysis`, `multi-specialist-review`,
`openapi-specification`, `owasp-top-10`, `playwright`, `product-manager`,
`product-strategy`, `prompt-engineering`, `proofreader`,
`python-performance-optimization`, `python-testing-patterns`, `quality-audit`,
`react-performance-optimization`, `reasoning-controls`, `receiving-code-review`,
`reference-documentation`, `regex-master`, `release-analysis`, `release-prep`,
`repo-cleanup`, `requesting-code-review`, `requirements-discovery`,
`research-methodology`, `root-cause-tracing`, `secure-coding-practices`,
`security-testing-patterns`, `session-management`, `sharing-skills`,
`skill-creator`, `socratic-questioning`, `storyteller`,
`subagent-driven-development`, `super-saiyan`, `systematic-debugging`,
`system-design`, `task-orchestration`, `template-skill`,
`template-skill-enhanced`, `terms-of-service`, `terraform-best-practices`,
`test-driven-development`, `test-generation`, `testing-anti-patterns`,
`testing-skills-with-subagents`, `test-review`, `threat-modeling-techniques`,
`token-efficiency`, `tool-selection`, `tutorial-design`,
`typescript-advanced-patterns`, `ui-design-aesthetics`, `user-journey-mapping`,
`using-git-worktrees`, `using-superpowers`, `ux-interaction-review`,
`ux-researcher`, `ux-review`, `ux-writer`, `verification-before-completion`,
`vibe-security`, `visual-modes`, `webapp-testing`, `web-researcher`,
`wiring-audit`, `workflow-bug-fix`, `workflow-feature`,
`workflow-performance`, `workflow-security-audit`, `writing-skills`.

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/codex-cortex/`
- Installable plugin projection: `codex-marketplace/plugins/architecture-pack/`
- Installable plugin projection: `codex-marketplace/plugins/api-contracts-pack/`
- Installable plugin projection: `codex-marketplace/plugins/language-patterns-pack/`
- Installable plugin projection: `codex-marketplace/plugins/security-pack/`
- Installable plugin projection: `codex-marketplace/plugins/frontend-pack/`
- Installable plugin projection: `codex-marketplace/plugins/planning-pack/`

## Projected today / already projected

23 of 149 upstream skills are projected into canonical marketplace plugins.

### Already projected (prior issues MARK-172 through MARK-214)

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

### Projected today (MARK-279)

| Skill | Projected into |
| --- | --- |
| `requirements-discovery` | `planning-pack` |
| `mermaid-diagramming` | `planning-pack` |
| `development-estimation` | `planning-pack` |
| `release-prep` | `planning-pack` |
| `release-analysis` | `planning-pack` |

## Retained in source custody / not yet projected

126 of 149 upstream skills are retained in source custody but not yet projected
into marketplace plugins. They are available for future projection when a
follow-up issue scopes them.

`.system`, `agent-loops`, `ai-tells-review`, `ai-tells-scan`,
`api-gateway-patterns`, `architectural-analysis`, `atlas-crew-tasks`,
`atomic-commits`, `backlog-md`, `blog-post`, `brand-library-architect`,
`build-optimization`, `business-analyst`, `canvas-design`, `chart-builder`,
`code-explanation`, `code-quality-workflow`, `codex-code-review`,
`collaboration`, `color-palette`, `community`, `competitor-analyst`,
`compliance-audit`, `condition-based-waiting`, `constructive-dissent`,
`copywriter`, `cortex-skills-loop`, `dashboard-designer`, `dataset-curator`,
`decision-maker`, `defense-in-depth`, `design-critiquer`,
`design-journey-review`, `design-system-architecture`, `dev-workflows`,
`dispatching-parallel-agents`, `doc-architecture-review`, `doc-claim-validator`,
`doc-completeness-audit`, `doc-health-audit`, `doc-maintenance`,
`doc-quality-review`, `documentation-production`, `document-skills`,
`email-drafter`, `eval-designer`, `evaluator-optimizer`, `fact-checker`,
`feature-implementation`, `finishing-a-development-branch`, `frontend-design`,
`github-actions-workflows`, `git-ops`, `gitops-workflows`,
`helm-chart-patterns`, `html-seo-review`, `implementation-workflow`,
`incident-response`, `internal-comms`, `justfile-author`, `knowledge-stack`,
`knowledge-synthesis`, `kubernetes-deployment-patterns`,
`kubernetes-security-policies`, `legacy-modernization`, `mapping-suite`,
`market-researcher`, `microservices-patterns`, `model-comparator`,
`multi-llm-consult`, `multi-perspective-analysis`, `multi-specialist-review`,
`playwright`, `product-manager`, `product-strategy`, `prompt-engineering`,
`proofreader`, `quality-audit`, `reasoning-controls`, `receiving-code-review`,
`reference-documentation`, `regex-master`, `repo-cleanup`,
`requesting-code-review`, `research-methodology`, `root-cause-tracing`,
`session-management`, `sharing-skills`, `skill-creator`, `socratic-questioning`,
`storyteller`, `subagent-driven-development`, `super-saiyan`,
`systematic-debugging`, `system-design`, `task-orchestration`, `template-skill`,
`template-skill-enhanced`, `terms-of-service`, `terraform-best-practices`,
`test-driven-development`, `test-generation`, `testing-anti-patterns`,
`testing-skills-with-subagents`, `test-review`, `token-efficiency`,
`tool-selection`, `tutorial-design`, `ui-design-aesthetics`,
`user-journey-mapping`, `using-git-worktrees`, `using-superpowers`,
`ux-interaction-review`, `ux-researcher`, `ux-writer`,
`verification-before-completion`, `vibe-security`, `visual-modes`,
`web-researcher`, `wiring-audit`, `workflow-bug-fix`, `workflow-feature`,
`workflow-performance`, `workflow-security-audit`, `writing-skills`.

## Rejected with hard reasons

| Candidate | Hard reason |
| --- | --- |
| `codanna-codebase-intelligence` | Violates durable-source doctrine: memory-first/tooling-dependent approach conflicts with repo-root `AGENTS.md` durable-source rule. Source is in custody but projection would introduce a plugin that depends on external memory/tooling not available in the marketplace install surface. |
| `knowledge-stack` | Violates durable-source doctrine: memory-first approach conflicts with repo-root `AGENTS.md` durable-source rule. Source is in custody but projection would introduce a plugin that depends on external memory/tooling not available in the marketplace install surface. |

## MARK-279 child coverage map

| Child | Title | Classification | Evidence |
| --- | --- | --- | --- |
| MARK-189 | Seed security-pack from first-wave security candidates | already satisfied | `security-pack` projects `secure-coding-practices`, `owasp-top-10`, `security-testing-patterns`, `threat-modeling-techniques`. Linear status: Done. |
| MARK-190 | Seed language-patterns-pack from language and runtime skills | already satisfied | `language-patterns-pack` projects `typescript-advanced-patterns`, `python-testing-patterns`, `async-python-patterns`, `python-performance-optimization`. Linear status: Done. |
| MARK-191 | Seed frontend-pack with React and frontend application skills | already satisfied | `frontend-pack` projects `react-performance-optimization`, `accessibility-audit`, `ux-review`, `interaction-design`, `webapp-testing`. Linear status: Done. |
| MARK-192 | Seed cross-repo truth and governance pack | retained / not yet projected | `doc-claim-validator`, `doc-maintenance`, `repo-cleanup`, `quality-audit` are in custody but not yet projected. No existing pack covers this domain. Available for future projection. |
| MARK-193 | Seed source-intelligence-pack from codebase and knowledge candidates | rejected | `codanna-codebase-intelligence` and `knowledge-stack` violate durable-source doctrine (memory-first). Source is in custody but projection is rejected. |
| MARK-194 | Seed planning-pack from requirements and diagramming candidates | implemented in this PR | `planning-pack` projects `requirements-discovery`, `mermaid-diagramming`, `development-estimation`, `release-prep`, `release-analysis`. |
| MARK-195 | Seed ci-pack from GitHub Actions workflow guidance | retained / not yet projected | `github-actions-workflows` is in custody but not yet projected. No existing pack covers CI workflow guidance. Available for future projection. |
| MARK-196 | Inventory product, research, UX, and creative Claude-Cortex candidates | retained / not yet projected | All product/research/UX/creative candidates (`product-manager`, `product-strategy`, `market-researcher`, `competitor-analyst`, `ux-researcher`, `ux-writer`, `blog-post`, `copywriter`, `storyteller`, `visual-modes`, `canvas-design`, `color-palette`, `chart-builder`, `dashboard-designer`, etc.) are in custody but not yet projected. Available for future projection. |
| MARK-197 | Maintain deferred Claude-Cortex specialist parking lot | retained / not yet projected | All specialist candidates (`microservices-patterns`, `legacy-modernization`, `build-optimization`, `kubernetes-deployment-patterns`, `helm-chart-patterns`, `terraform-best-practices`, `gitops-workflows`, `workflow-performance`, etc.) are in custody but not yet projected. Available for future projection. |
| MARK-218 | Compare cleanup and quality governance overlaps | retained / not yet projected | `quality-audit`, `repo-cleanup`, `doc-health-audit` are in custody. Overlap with `house-skills:cleanup-custody` exists but does not block projection. Available for future projection. |
| MARK-219 | Project doc claim and maintenance guidance into repo-truth pack | retained / not yet projected | `doc-claim-validator` and `doc-maintenance` are in custody but not yet projected. Available for future projection. |
| MARK-221 | Inventory source-intelligence compatibility and source custody fit | rejected | See MARK-193. `codanna-codebase-intelligence` and `knowledge-stack` violate durable-source doctrine. |
| MARK-222 | Prove codanna-codebase-intelligence compatibility | rejected | See MARK-193. `codanna-codebase-intelligence` violates durable-source doctrine. |
| MARK-223 | Evaluate knowledge-stack durable-source posture | rejected | See MARK-193. `knowledge-stack` violates durable-source doctrine. |
| MARK-224 | Compare requirements-discovery against issue shaping stack | implemented in this PR | `requirements-discovery` projected into `planning-pack`. Overlap with `superpowers-plus:linear-superpowers` noted but does not block projection; the skills serve different contexts. |
| MARK-225 | Evaluate mermaid-diagramming planning value | implemented in this PR | `mermaid-diagramming` projected into `planning-pack`. |

## MARK-279 retained existing skills

No existing first-party or third-party plugin content was removed or replaced. All 18 previously-projected Claude-Cortex skills retain their existing projections across `codex-cortex`, `architecture-pack`, `api-contracts-pack`, `language-patterns-pack`, `security-pack`, and `frontend-pack`. Projected plugin copies were synced to match the full upstream mirror source where the upstream content differed from the previous selective snapshot.

## MARK-279 generated artifact explanation

- `codex-marketplace/manifest.json` and `.agents/plugins/marketplace.json` regenerated by `tools/generate_marketplace.py` to include the new `planning-pack` plugin root.
- `repo-index/repo-index.json` regenerated by `tools/generate_repo_index.py` to include the `planning-pack` entry.
- `generated/skill-zips/registry.json` regenerated by `tools/update_skill_artifacts.py --all` to include 5 new planning-pack skill zip entries.
- `generated/skill-zips/planning-pack/` skill zip artifacts produced by the packaging tool for the 5 projected planning-pack skills.
