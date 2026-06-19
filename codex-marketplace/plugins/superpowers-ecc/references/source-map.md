# Superpowers ECC Source Map

This bundle harmonizes retained ECC workflow skills into a dedicated
Superpowers-style marketplace surface.

Harmonization notes:

- `agent-harness-construction` stays at the agent tool/observation design layer.
- `ai-first-engineering` stays at the AI-heavy engineering operating model layer.
- `deployment-patterns` stays at the deployment and release-readiness layer.
- `dmux-workflows` stays at the multi-agent orchestration layer.
- `messages-ops` stays at the evidence-first messaging layer.
- `ml-adoption-playbook` stays at the AI/ML adoption framing layer.
- `prediction-market-oracle-research` stays at the prediction-market research layer.
- `recursive-decision-ledger` stays at the recursive decision and evidence-trail layer.
- `research-ops` stays at the current-state research layer.
- `safety-guard` stays at the destructive-operation guardrail layer.
- `search-first` stays at the research-before-coding layer.
- `team-agent-orchestration` stays at the squad orchestration layer.
- `team-builder` stays at the team composition layer.
- `token-budget-advisor` stays at the token-budget guidance layer.
- `superpowers-plus` only owns the thin `ecc-superpowers` routing wrapper.
- Detailed file-level projections and source-file inventories are captured in
  `references/bundle-manifest.json`.

Retained ECC custody:

- `sources/third_party/ecc/upstream/skills/agent-harness-construction/`
- `sources/third_party/ecc/upstream/skills/ai-first-engineering/`
- `sources/third_party/ecc/upstream/skills/deployment-patterns/`
- `sources/third_party/ecc/upstream/skills/dmux-workflows/`
- `sources/third_party/ecc/upstream/skills/messages-ops/`
- `sources/third_party/ecc/upstream/skills/ml-adoption-playbook/`
- `sources/third_party/ecc/upstream/skills/prediction-market-oracle-research/`
- `sources/third_party/ecc/upstream/skills/recursive-decision-ledger/`
- `sources/third_party/ecc/upstream/skills/research-ops/`
- `sources/third_party/ecc/upstream/skills/safety-guard/`
- `sources/third_party/ecc/upstream/skills/search-first/`
- `sources/third_party/ecc/upstream/skills/team-agent-orchestration/`
- `sources/third_party/ecc/upstream/skills/team-builder/`
- `sources/third_party/ecc/upstream/skills/token-budget-advisor/`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| agent-harness-construction | `sources/third_party/ecc/upstream/skills/agent-harness-construction/` | `codex-marketplace/plugins/superpowers-ecc/skills/agent-harness-construction/` | Dedicated agent tool/action/observation design slice. |
| ai-first-engineering | `sources/third_party/ecc/upstream/skills/ai-first-engineering/` | `codex-marketplace/plugins/superpowers-ecc/skills/ai-first-engineering/` | Dedicated AI-heavy engineering operating-model slice. |
| deployment-patterns | `sources/third_party/ecc/upstream/skills/deployment-patterns/` | `codex-marketplace/plugins/superpowers-ecc/skills/deployment-patterns/` | Dedicated deployment and release-readiness slice. |
| dmux-workflows | `sources/third_party/ecc/upstream/skills/dmux-workflows/` | `codex-marketplace/plugins/superpowers-ecc/skills/dmux-workflows/` | Dedicated multi-agent orchestration slice. |
| messages-ops | `sources/third_party/ecc/upstream/skills/messages-ops/` | `codex-marketplace/plugins/superpowers-ecc/skills/messages-ops/` | Dedicated evidence-first messaging slice. |
| ml-adoption-playbook | `sources/third_party/ecc/upstream/skills/ml-adoption-playbook/` | `codex-marketplace/plugins/superpowers-ecc/skills/ml-adoption-playbook/` | Dedicated AI/ML adoption framing slice. |
| prediction-market-oracle-research | `sources/third_party/ecc/upstream/skills/prediction-market-oracle-research/` | `codex-marketplace/plugins/superpowers-ecc/skills/prediction-market-oracle-research/` | Dedicated prediction-market research slice. |
| recursive-decision-ledger | `sources/third_party/ecc/upstream/skills/recursive-decision-ledger/` | `codex-marketplace/plugins/superpowers-ecc/skills/recursive-decision-ledger/` | Dedicated recursive decision and evidence-trail slice. |
| research-ops | `sources/third_party/ecc/upstream/skills/research-ops/` | `codex-marketplace/plugins/superpowers-ecc/skills/research-ops/` | Dedicated current-state research slice. |
| safety-guard | `sources/third_party/ecc/upstream/skills/safety-guard/` | `codex-marketplace/plugins/superpowers-ecc/skills/safety-guard/` | Dedicated destructive-operation guardrail slice. |
| search-first | `sources/third_party/ecc/upstream/skills/search-first/` | `codex-marketplace/plugins/superpowers-ecc/skills/search-first/` | Dedicated research-before-coding slice. |
| team-agent-orchestration | `sources/third_party/ecc/upstream/skills/team-agent-orchestration/` | `codex-marketplace/plugins/superpowers-ecc/skills/team-agent-orchestration/` | Dedicated squad orchestration slice. |
| team-builder | `sources/third_party/ecc/upstream/skills/team-builder/` | `codex-marketplace/plugins/superpowers-ecc/skills/team-builder/` | Dedicated team composition slice. |
| token-budget-advisor | `sources/third_party/ecc/upstream/skills/token-budget-advisor/` | `codex-marketplace/plugins/superpowers-ecc/skills/token-budget-advisor/` | Dedicated token-budget guidance slice. |

The pack root is an installable Codex plugin projection. It does not replace
the retained ECC source custody tree or the thin Superpowers+ wrapper.
