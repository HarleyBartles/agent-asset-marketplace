# Frontend Pack Source Map

This bundle projects the retained `NickCrew/Claude-Cortex` frontend
application skills from the retained `claude-cortex` custody root into a
marketplace surface. The retained upstream skills keep their original bodies
and are projected into `frontend-pack` with pack-relative references.

The plugin shell is authored by Harley Bartles. The projected skill roots retain
their upstream source author, source license, and source path in the bundle
manifest and source map so verbatim content stays attributable.

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

| Skill | Content mode | Source origin | Upstream author | Upstream license | Source path | Pack path | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| react-performance-optimization | adapted | Claude-Cortex | NickCrew | MIT | `sources/third_party/claude-cortex/upstream/skills/react-performance-optimization/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/react-performance-optimization/SKILL.md` | Adapted projection with upstream authorship metadata frontmatter for MARK-244 provenance compliance. Skill content body remains verbatim from upstream. |
| accessibility-audit | adapted | Claude-Cortex | NickCrew | MIT | `sources/third_party/claude-cortex/upstream/skills/accessibility-audit/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/accessibility-audit/SKILL.md` | Adapted projection with upstream authorship metadata frontmatter for MARK-244 provenance compliance. Skill content body remains verbatim from upstream. |
| ux-review | adapted | Claude-Cortex | NickCrew | MIT | `sources/third_party/claude-cortex/upstream/skills/ux-review/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/ux-review/SKILL.md` | Adapted projection with upstream authorship metadata frontmatter for MARK-244 provenance compliance. Skill content body remains verbatim from upstream. |
| interaction-design | adapted | Claude-Cortex | NickCrew | MIT | `sources/third_party/claude-cortex/upstream/skills/interaction-design/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/interaction-design/SKILL.md` | Adapted projection with upstream authorship metadata frontmatter for MARK-244 provenance compliance. Skill content body remains verbatim from upstream. |
| webapp-testing | adapted | Claude-Cortex | NickCrew | MIT | `sources/third_party/claude-cortex/upstream/skills/webapp-testing/SKILL.md` | `codex-marketplace/plugins/frontend-pack/skills/webapp-testing/SKILL.md` | Adapted projection with upstream authorship metadata frontmatter for MARK-244 provenance compliance. Skill content body remains verbatim from upstream. |

The pack root is an installable Codex plugin projection. It does not replace
the retained `claude-cortex` custody snapshot.
