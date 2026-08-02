# AGENTS.md Migration Audit

Plan: `.agents/plans/2026-08-01-devin-rules-mesh-migration.md`

## Classification table

| Path | Classification | Reasoning | Target surface |
|------|----------------|-----------|---------------|
| `AGENTS.md` | `keep-thin` | Contains global repo doctrine, publication rules, source-of-truth split - genuinely always-on for whole repo | Keep as `AGENTS.md` (thin to ~30-50 lines) |
| `.agents/AGENTS.md` | `keep-thin` | Very short (32 lines), scoped law for `.agents/` directory - safe to load always-on | Keep as `.agents/AGENTS.md` (already under 20 lines) |
| `.agents/docs/AGENTS.md` | `keep-thin` | Very short (20 lines), scoped law for `.agents/docs/` - safe to load always-on | Keep as `.agents/docs/AGENTS.md` (already under 20 lines) |
| `.agents/docs/superpowers/AGENTS.md` | `delete` | Historical directory marker, not operative law | Delete |
| `.agents/guides/AGENTS.md` | `keep-thin` | Very short (23 lines), guide-stage routing - safe to load always-on | Keep as `.agents/guides/AGENTS.md` (already under 20 lines) |
| `.agents/plans/AGENTS.md` | `devin-rule` | Plan workflow guidance, scoped to `.agents/plans/` | `.devin/rules/plans.md` with `trigger: glob`, `globs: ".agents/plans/**"` |
| `.agents/plugins/AGENTS.md` | `keep-thin` | Very short (12 lines), plugin posture - safe to load always-on | Keep as `.agents/plugins/AGENTS.md` (already under 20 lines) |
| `.agents/skills/AGENTS.md` | `devin-rule` | Skill installation and source-of-truth rules (71 lines), scoped to `.agents/skills/` | `.devin/rules/skills.md` with `trigger: glob`, `globs: ".agents/skills/**"` |
| `.agents/skills/repo-standards/templates/AGENTS.md` | `regenerate-source` | Template file with placeholders, copied when skills are installed | Remove from template source in the deleted first-party skill tree `repo-standards/templates/` |
| `.agents/skills/subagent-driven-development/scripts/AGENTS.md` | `devin-rule` | Script usage guidance, scoped to scripts directory | `.devin/rules/sdd-scripts.md` with `trigger: glob`, `globs: "**/scripts/**"` |
| `adapters/AGENTS.md` | `devin-rule` | Adapter surface law, scoped to `adapters/` | `.devin/rules/adapters.md` with `trigger: glob`, `globs: "adapters/**"` |
| `codex-marketplace/AGENTS.md` | `devin-rule` | Marketplace source/projection law (99 lines), scoped to `codex-marketplace/` | `.devin/rules/codex-marketplace.md` with `trigger: glob`, `globs: "codex-marketplace/**"` |
| `codex-marketplace/plugins/AGENTS.md` | `devin-rule` | Plugin projection law (89 lines), scoped to `codex-marketplace/plugins/` | `.devin/rules/codex-plugins.md` with `trigger: glob`, `globs: "codex-marketplace/plugins/**"` |
| `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/AGENTS.md` | `regenerate-source` | Projected copy from the deleted first-party skill tree `repo-standards/templates/AGENTS.md` | Fix source template, then regenerate marketplace |
| `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/scripts/AGENTS.md` | `regenerate-source` | Projected copy from the deleted first-party skill tree `subagent-driven-development/scripts/AGENTS.md` | Fix source, then regenerate marketplace |
| `docs/AGENTS.md` | `devin-rule` | Docs-owned guidance, scoped to `docs/` | `.devin/rules/docs.md` with `trigger: glob`, `globs: "docs/**"` |
| `docs/contracts/AGENTS.md` | `devin-rule` | Contract-doc routing, scoped to `docs/contracts/` | `.devin/rules/docs-contracts.md` with `trigger: glob`, `globs: "docs/contracts/**"` |
| `provenance/AGENTS.md` | `devin-rule` | Provenance evidence law, scoped to `provenance/` | `.devin/rules/provenance.md` with `trigger: glob`, `globs: "provenance/**"` |
| the deleted source tree `AGENTS.md` | `devin-rule` | Source custody law, scoped to the deleted source tree | `.devin/rules/sources.md` with `trigger: glob`, `globs: "the deleted source tree `**"` |
| the deleted first-party skill tree `AGENTS.md` | `devin-rule` | First-party skill format guidance (68 lines), scoped to the deleted first-party skill tree | `.devin/rules/first-party-skills.md` with `trigger: glob`, `globs: "the deleted first-party skill tree `**"` |
| the deleted first-party skill tree `repo-standards/templates/AGENTS.md` | `regenerate-source` | Template file with placeholders | Remove template file entirely |
| the deleted first-party skill tree `subagent-driven-development/scripts/AGENTS.md` | `devin-rule` | Script usage guidance, scoped to scripts directory | Merge with `.devin/rules/sdd-scripts.md` |
| the deleted third-party source tree `AGENTS.md` | `devin-rule` | Third-party custody law (62 lines), scoped to the deleted third-party source tree | `.devin/rules/third-party.md` with `trigger: glob`, `globs: "the deleted third-party source tree `**"` |
| the deleted third-party source tree `superpowers/obra-superpowers/v6.2.0/AGENTS.md` | `keep` | Vendored upstream file (points to `CLAUDE.md`) | Keep as vendored upstream file; do not modify (immutable third-party custody). If it causes rule overload, remove or rename in a future upstream sync, not here. |
| `tools/AGENTS.md` | `devin-rule` | Tooling law (165 lines), scoped to `tools/` | `.devin/rules/tools.md` with `trigger: glob`, `globs: "tools/**"` |

## Summary

| Classification | Count |
|----------------|-------|
| `keep-thin` | 5 |
| `keep` | 1 |
| `devin-rule` | 13 |
| `delete` | 1 |
| `regenerate-source` | 4 |

**Total files:** 24

### Key findings

1. **5 files** are already short enough to keep as `AGENTS.md` (under 20-32 lines each): root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/docs/AGENTS.md`, `.agents/guides/AGENTS.md`, and `.agents/plugins/AGENTS.md`. These are genuinely always-on routing surfaces.
2. **1 file** is an immutable upstream vendored file in the deleted third-party source tree `superpowers/obra-superpowers/v6.2.0/AGENTS.md`. It must not be edited directly. If the overload is unacceptable, the solution is a future upstream sync or an adapter overlay, not a local rename.
3. **13 files** contain scoped law that should be migrated to `.devin/rules/*.md` with appropriate `trigger: glob` patterns.
4. **1 file** should be deleted: `.agents/docs/superpowers/AGENTS.md` is a historical marker with no operative law.
5. **4 files** are generated or template files that should be fixed at the source; the projected copies under `codex-marketplace/plugins/` will be removed by a full marketplace regeneration once the source templates are gone.
