# Frontend Pack Source Map

This bundle projects frontend skills from two upstream sources:
1. The retained `NickCrew/Claude-Cortex` frontend application skills from the retained `claude-cortex` custody root
2. The retained `affaan-m/ECC` frontend skills from the retained `ecc` custody root

The retained upstream skills keep their original bodies and are projected into `frontend-pack` with pack-relative references.

Retained custody evidence:

### From NickCrew/Claude-Cortex

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

### From affaan-m/ECC

- `sources/third_party/ecc/upstream/skills/accessibility/SKILL.md`
- `sources/third_party/ecc/upstream/skills/angular-developer/SKILL.md`
- `sources/third_party/ecc/upstream/skills/browser-qa/SKILL.md`
- `sources/third_party/ecc/upstream/skills/design-system/SKILL.md`
- `sources/third_party/ecc/upstream/skills/e2e-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/make-interfaces-feel-better/SKILL.md`
- `sources/third_party/ecc/upstream/skills/react-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/react-testing/SKILL.md`
- `sources/third_party/ecc/upstream/skills/swiftui-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/vue-patterns/SKILL.md`
- `sources/third_party/ecc/upstream/skills/windows-desktop-e2e/SKILL.md`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| react-performance-optimization | `sources/third_party/claude-cortex/upstream/skills/react-performance-optimization/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/react-performance-optimization/SKILL.md` | Verbatim projection of React performance guidance. |
| accessibility-audit | `sources/third_party/claude-cortex/upstream/skills/accessibility-audit/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/accessibility-audit/SKILL.md` | Verbatim projection of WCAG 2.2 AA triage guidance. |
| ux-review | `sources/third_party/claude-cortex/upstream/skills/ux-review/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/ux-review/SKILL.md` | Verbatim projection of the UX review workflow. |
| interaction-design | `sources/third_party/claude-cortex/upstream/skills/interaction-design/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/interaction-design/SKILL.md` | Verbatim projection of the interaction design guidance and state-pattern reference. |
| webapp-testing | `sources/third_party/claude-cortex/upstream/skills/webapp-testing/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/SKILL.md` | Verbatim projection of the Playwright-based testing toolkit, scripts, and examples. |
| accessibility | `sources/third_party/ecc/upstream/skills/accessibility/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/accessibility/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| angular-developer | `sources/third_party/ecc/upstream/skills/angular-developer/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/angular-developer/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| browser-qa | `sources/third_party/ecc/upstream/skills/browser-qa/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/browser-qa/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| design-system | `sources/third_party/ecc/upstream/skills/design-system/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/design-system/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| e2e-testing | `sources/third_party/ecc/upstream/skills/e2e-testing/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/e2e-testing/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| make-interfaces-feel-better | `sources/third_party/ecc/upstream/skills/make-interfaces-feel-better/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/make-interfaces-feel-better/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| react-patterns | `sources/third_party/ecc/upstream/skills/react-patterns/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/react-patterns/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| react-testing | `sources/third_party/ecc/upstream/skills/react-testing/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/react-testing/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| swiftui-patterns | `sources/third_party/ecc/upstream/skills/swiftui-patterns/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/swiftui-patterns/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| vue-patterns | `sources/third_party/ecc/upstream/skills/vue-patterns/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/vue-patterns/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |
| windows-desktop-e2e | `sources/third_party/ecc/upstream/skills/windows-desktop-e2e/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/windows-desktop-e2e/SKILL.md` | Verbatim projection from ECC custody as part of MARK-245. |

The pack root is an installable Codex plugin projection. It does not replace
the retained `claude-cortex` or `ecc` custody snapshots.
