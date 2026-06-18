# Frontend Pack Source Map

This bundle projects the retained `NickCrew/Claude-Cortex` frontend application
skills into a marketplace surface. The retained upstream skills keep their
original bodies and are projected into `frontend-pack` with pack-relative
references.

Retained custody evidence:

- `sources/third_party/claude-cortex/upstream/README.md`
- `sources/third_party/claude-cortex/upstream/LICENSE`
- `sources/third_party/claude-cortex/upstream/skills/react-performance-optimization/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/react-performance-optimization/validation/rubric.yaml`
- `sources/third_party/claude-cortex/upstream/skills/accessibility-audit/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/ux-review/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/interaction-design/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/interaction-design/references/state-patterns.md`
- `sources/third_party/claude-cortex/upstream/skills/webapp-testing/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/webapp-testing/LICENSE.txt`
- `sources/third_party/claude-cortex/upstream/skills/webapp-testing/scripts/with_server.py`
- `sources/third_party/claude-cortex/upstream/skills/webapp-testing/examples/static_html_automation.py`
- `sources/third_party/claude-cortex/upstream/skills/webapp-testing/examples/element_discovery.py`
- `sources/third_party/claude-cortex/upstream/skills/webapp-testing/examples/console_logging.py`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| react-performance-optimization | `sources/third_party/claude-cortex/upstream/skills/react-performance-optimization/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/react-performance-optimization/SKILL.md` | Verbatim projection of React performance guidance. |
| accessibility-audit | `sources/third_party/claude-cortex/upstream/skills/accessibility-audit/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/accessibility-audit/SKILL.md` | Verbatim projection of WCAG 2.2 AA triage guidance. |
| ux-review | `sources/third_party/claude-cortex/upstream/skills/ux-review/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/ux-review/SKILL.md` | Verbatim projection of the UX review workflow. |
| interaction-design | `sources/third_party/claude-cortex/upstream/skills/interaction-design/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/interaction-design/SKILL.md` | Verbatim projection of the interaction design guidance and state-pattern reference. |
| webapp-testing | `sources/third_party/claude-cortex/upstream/skills/webapp-testing/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/SKILL.md` | Verbatim projection of the Playwright-based testing toolkit, scripts, and examples. |

The pack root is an installable Codex plugin projection. It does not replace
the retained `claude-cortex` custody snapshot.
