# Planning Pack Source Map

This bundle projects 5 planning-related skills from the retained
`NickCrew/Claude-Cortex` custody root into the `planning-pack` marketplace
projection.

The retained upstream skills keep their original bodies and are projected
into `planning-pack` with pack-relative references.

Retained custody evidence:

### From NickCrew/Claude-Cortex

- `sources/third_party/claude-cortex/upstream/README.md`
- `sources/third_party/claude-cortex/upstream/LICENSE`
- `sources/third_party/claude-cortex/upstream/skills/requirements-discovery/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/requirements-discovery/references/elicitation-techniques.md`
- `sources/third_party/claude-cortex/upstream/skills/mermaid-diagramming/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/mermaid-diagramming/references/diagram-types.md`
- `sources/third_party/claude-cortex/upstream/skills/development-estimation/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/development-estimation/references/estimate.md`
- `sources/third_party/claude-cortex/upstream/skills/release-prep/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/release-prep/references/prepare-release.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/assets/template.html`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/assets/styles/blueprint/mermaid-dark.json`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/assets/styles/blueprint/mermaid-light.json`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/assets/styles/blueprint/style.css`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/assets/styles/corporate/mermaid-dark.json`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/assets/styles/corporate/mermaid-light.json`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/assets/styles/corporate/style.css`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/citation-protocol.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/docs-reconciliation.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/mermaid-conventions.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/mode-configuration-provenance.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/mode-environment-matrix.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/mode-promotion-path.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/mode-recovery-rollback.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/report-template.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/subagent-dispatch.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/synthesis-readme.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/references/verification-protocol.md`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/scripts/compile-html.sh`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/scripts/compile-pdf.sh`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/scripts/render.sh`
- `sources/third_party/claude-cortex/upstream/skills/release-analysis/scripts/verify-citations.sh`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| requirements-discovery | `sources/third_party/claude-cortex/upstream/skills/requirements-discovery/SKILL.md` | `codex-marketplace/plugins/planning-pack/skills/requirements-discovery/SKILL.md` | Verbatim projection of requirements gathering and shaping guidance. |
| mermaid-diagramming | `sources/third_party/claude-cortex/upstream/skills/mermaid-diagramming/SKILL.md` | `codex-marketplace/plugins/planning-pack/skills/mermaid-diagramming/SKILL.md` | Verbatim projection of diagramming guidance for planning and architecture. |
| development-estimation | `sources/third_party/claude-cortex/upstream/skills/development-estimation/SKILL.md` | `codex-marketplace/plugins/planning-pack/skills/development-estimation/SKILL.md` | Verbatim projection of development effort estimation techniques. |
| release-prep | `sources/third_party/claude-cortex/upstream/skills/release-prep/SKILL.md` | `codex-marketplace/plugins/planning-pack/skills/release-prep/SKILL.md` | Verbatim projection of release preparation workflows and checklists. |
| release-analysis | `sources/third_party/claude-cortex/upstream/skills/release-analysis/SKILL.md` | `codex-marketplace/plugins/planning-pack/skills/release-analysis/SKILL.md` | Verbatim projection of release analysis, comparison, and reporting guidance. |

The pack root is an installable Codex plugin projection. It does not replace
the retained `claude-cortex` custody snapshot.