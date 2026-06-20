# Source

This Codex marketplace plugin is the repo-canonical copy of the locally created
Repo Worker Base asset.

## Local source

- Local source path: `C:\Users\Harls\plugins\repo-worker-base`
- Source files:
  - `.codex-plugin/plugin.json`
  - `skills/repo-worker-base/SKILL.md`
  - `skills/repo-worker-base/agents/openai.yaml`

## Projected skills

### First-party core skills

- `boring-loop` projected from `sources/first_party/core/boring-loop`
- `connector-safety` projected from `sources/first_party/core/connector-safety`
- `github-operations` projected from `sources/first_party/core/github-operations`

### ECC repo/operator skills

The following 43 skills are projected from ECC (affaan-m/ECC) third-party custody under `sources/third_party/ecc/upstream/skills/`:

- `agent-introspection-debugging` projected from `sources/third_party/ecc/upstream/skills/agent-introspection-debugging`
- `agent-sort` projected from `sources/third_party/ecc/upstream/skills/agent-sort`
- `android-clean-architecture` projected from `sources/third_party/ecc/upstream/skills/android-clean-architecture`
- `api-connector-builder` projected from `sources/third_party/ecc/upstream/skills/api-connector-builder`
- `claude-devfleet` projected from `sources/third_party/ecc/upstream/skills/claude-devfleet`
- `click-path-audit` projected from `sources/third_party/ecc/upstream/skills/click-path-audit`
- `code-tour` projected from `sources/third_party/ecc/upstream/skills/code-tour`
- `codebase-onboarding` projected from `sources/third_party/ecc/upstream/skills/codebase-onboarding`
- `competitive-report-structure` projected from `sources/third_party/ecc/upstream/skills/competitive-report-structure`
- `config-gc` projected from `sources/third_party/ecc/upstream/skills/config-gc`
- `cost-tracking` projected from `sources/third_party/ecc/upstream/skills/cost-tracking`
- `cpp-coding-standards` projected from `sources/third_party/ecc/upstream/skills/cpp-coding-standards`
- `data-scraper-agent` projected from `sources/third_party/ecc/upstream/skills/data-scraper-agent`
- `deep-research` projected from `sources/third_party/ecc/upstream/skills/deep-research`
- `django-verification` projected from `sources/third_party/ecc/upstream/skills/django-verification`
- `ecc-guide` projected from `sources/third_party/ecc/upstream/skills/ecc-guide`
- `ecc-tools-cost-audit` projected from `sources/third_party/ecc/upstream/skills/ecc-tools-cost-audit`
- `flox-environments` projected from `sources/third_party/ecc/upstream/skills/flox-environments`
- `git-workflow` projected from `sources/third_party/ecc/upstream/skills/git-workflow`
- `github-ops` projected from `sources/third_party/ecc/upstream/skills/github-ops`
- `google-workspace-ops` projected from `sources/third_party/ecc/upstream/skills/google-workspace-ops`
- `hermes-imports` projected from `sources/third_party/ecc/upstream/skills/hermes-imports`
- `inherit-legacy-style` projected from `sources/third_party/ecc/upstream/skills/inherit-legacy-style`
- `knowledge-ops` projected from `sources/third_party/ecc/upstream/skills/knowledge-ops`
- `kotlin-exposed-patterns` projected from `sources/third_party/ecc/upstream/skills/kotlin-exposed-patterns`
- `laravel-verification` projected from `sources/third_party/ecc/upstream/skills/laravel-verification`
- `market-research` projected from `sources/third_party/ecc/upstream/skills/market-research`
- `parallel-execution-optimizer` projected from `sources/third_party/ecc/upstream/skills/parallel-execution-optimizer`
- `production-audit` projected from `sources/third_party/ecc/upstream/skills/production-audit`
- `project-flow-ops` projected from `sources/third_party/ecc/upstream/skills/project-flow-ops`
- `quarkus-verification` projected from `sources/third_party/ecc/upstream/skills/quarkus-verification`
- `react-performance` projected from `sources/third_party/ecc/upstream/skills/react-performance`
- `repo-scan` projected from `sources/third_party/ecc/upstream/skills/repo-scan`
- `rules-distill` projected from `sources/third_party/ecc/upstream/skills/rules-distill`
- `security-bounty-hunter` projected from `sources/third_party/ecc/upstream/skills/security-bounty-hunter`
- `security-scan` projected from `sources/third_party/ecc/upstream/skills/security-scan`
- `skill-comply` projected from `sources/third_party/ecc/upstream/skills/skill-comply`
- `skill-scout` projected from `sources/third_party/ecc/upstream/skills/skill-scout`
- `skill-stocktake` projected from `sources/third_party/ecc/upstream/skills/skill-stocktake`
- `springboot-verification` projected from `sources/third_party/ecc/upstream/skills/springboot-verification`
- `terminal-ops` projected from `sources/third_party/ecc/upstream/skills/terminal-ops`
- `unified-notifications-ops` projected from `sources/third_party/ecc/upstream/skills/unified-notifications-ops`
- `workspace-surface-audit` projected from `sources/third_party/ecc/upstream/skills/workspace-surface-audit`

## Source files

### First-party core skills

- `skills/repo-worker-base/SKILL.md`
- `skills/repo-worker-base/agents/openai.yaml`
- `skills/boring-loop/SKILL.md`
- `skills/boring-loop/agents/openai.yaml`
- `skills/connector-safety/SKILL.md`
- `skills/connector-safety/agents/openai.yaml`
- `skills/github-operations/SKILL.md`
- `skills/github-operations/agents/openai.yaml`
- `skills/github-operations/assets/icon.svg`
- `skills/github-operations/references/source-route-posture.md`
- `skills/github-operations/references/pr-review-writes.md`

### ECC repo/operator skills

All ECC skills are copied verbatim from `sources/third_party/ecc/upstream/skills/<skill>/` to `skills/<skill>/`:

- `skills/agent-introspection-debugging/SKILL.md`
- `skills/agent-sort/SKILL.md`
- `skills/android-clean-architecture/SKILL.md`
- `skills/api-connector-builder/SKILL.md`
- `skills/claude-devfleet/SKILL.md`
- `skills/click-path-audit/SKILL.md`
- `skills/code-tour/SKILL.md`
- `skills/codebase-onboarding/SKILL.md`
- `skills/competitive-report-structure/SKILL.md`
- `skills/config-gc/SKILL.md`
- `skills/cost-tracking/SKILL.md`
- `skills/cpp-coding-standards/SKILL.md`
- `skills/data-scraper-agent/SKILL.md`
- `skills/deep-research/SKILL.md`
- `skills/django-verification/SKILL.md`
- `skills/ecc-guide/SKILL.md`
- `skills/ecc-tools-cost-audit/SKILL.md`
- `skills/flox-environments/SKILL.md`
- `skills/git-workflow/SKILL.md`
- `skills/github-ops/SKILL.md`
- `skills/google-workspace-ops/SKILL.md`
- `skills/hermes-imports/SKILL.md`
- `skills/inherit-legacy-style/SKILL.md`
- `skills/knowledge-ops/SKILL.md`
- `skills/kotlin-exposed-patterns/SKILL.md`
- `skills/laravel-verification/SKILL.md`
- `skills/market-research/SKILL.md`
- `skills/parallel-execution-optimizer/SKILL.md`
- `skills/production-audit/SKILL.md`
- `skills/project-flow-ops/SKILL.md`
- `skills/quarkus-verification/SKILL.md`
- `skills/react-performance/SKILL.md`
- `skills/repo-scan/SKILL.md`
- `skills/rules-distill/SKILL.md`
- `skills/security-bounty-hunter/SKILL.md`
- `skills/security-scan/SKILL.md`
- `skills/skill-comply/SKILL.md`
- `skills/skill-scout/SKILL.md`
- `skills/skill-stocktake/SKILL.md`
- `skills/springboot-verification/SKILL.md`
- `skills/terminal-ops/SKILL.md`
- `skills/unified-notifications-ops/SKILL.md`
- `skills/workspace-surface-audit/SKILL.md`

### References

- `references/source-map.md`

## Scope

This asset is intentionally thin:

- fresh-main discipline before repo edits;
- branch-from-current-main workflow;
- validation and publication evidence;
- honest status reporting for repo-backed work;
- generic connector safety and GitHub proof helpers needed by workers;
- ECC repo/operator skills for repository and operational workflows.

It does not include project-specific doctrine for any particular repo.
The `boring-loop` skill is a projected first-party coordination skill for
keeping work small, honest, and routed to the right specialist.
The `connector-safety` and `github-operations` skills are projected as the
generic safety/proof helper surfaces that no longer need House Skills as the
install surface. Their canonical source roots live under
`sources/first_party/core/<skill>/`.

The 43 ECC repo/operator skills are projected verbatim from third-party custody
under `sources/third_party/ecc/upstream/skills/` to provide repository and
operational workflow capabilities. These skills are sourced from the ECC
(affaan-m/ECC) upstream repository under MIT license.
