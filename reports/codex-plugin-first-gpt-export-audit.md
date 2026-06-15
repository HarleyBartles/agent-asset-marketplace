# Codex Plugin-First GPT Export Audit

Issue: `MARK-146`

## Audit Method

Live repo state was inspected from fresh `main` on branch `harleydbartles/mark-146-audit-asset-marketplace-source-and-gpt-export-posture`.

Commands and data sources used:

- `git fetch origin`
- `git pull --ff-only origin main`
- `git status --short --branch`
- `git rev-parse HEAD`
- `mcp__codex_apps__linear._search` for `MARK-146`
- `mcp__codex_apps__linear._fetch` for `issue:MARK-146`
- `Get-Content` on:
  - `AGENTS.md`
  - `README.md`
  - `codex-marketplace/README.md`
  - `codex-marketplace/AGENTS.md`
  - `codex-marketplace/manifest.json`
  - `codex-marketplace/plugin-roots.json`
  - `gpt-overlays/AGENTS.md`
  - `gpt-overlays/README.md`
  - `gpt-overlays/manifest.json`
  - `sources/first_party/skills/house-skills/decisions.md`
  - `sources/first_party/skills/house-skills/intake.json`
  - pack-level `SOURCE.md`, `README.md`, `PROJECTION.md`, `LICENSE`, and bundle manifests
  - `tools/validate_marketplace.py`
  - `tools/validate_repo_index.py`
  - `tools/validate_generated_drift.py`
- `py -3` inspection scripts for:
  - `generated/skill-zips/registry.json`
  - `gpt-overlays/manifest.json`
  - representative generated zip payloads
  - archive-wide forbidden-surface scanning

Sampling policy:

- Fully enumerated: `codex-marketplace/manifest.json`, `codex-marketplace/plugin-roots.json`, `gpt-overlays/manifest.json`, `generated/skill-zips/registry.json`, and all 102 generated `skill.zip` archives.
- Sampled: representative archive payload contents for direct and overlay classes.
- No source route was unavailable.

## Current Posture Summary

The repo still behaves as `Codex plugin first; generated GPT-safe skill zips second.`

Evidence:

- Active marketplace roots are fixed to 6 plugin packs in `codex-marketplace/plugin-roots.json`.
- The marketplace manifest and `.agents/plugins/marketplace.json` are aligned on those 6 roots.
- The generated export registry contains 102 published skill archives and 3 intentionally excluded exports.
- Export modes are currently `95 direct`, `7 overlay`, and `3 excluded`.
- The generated archive scan found `0` forbidden plugin-harness leaks across all 102 `skill.zip` files.

## Asset Inventory

| Asset pack | Canonical source custody | Codex plugin exposure | GPT export mode | Overlay / exclusion state | Provenance truth | Repair need |
| --- | --- | --- | --- | --- | --- | --- |
| `house-skills` | First-party Harley-owned source in `sources/first_party/skills/house-skills/` plus the projected plugin root. | Exposed through `codex-marketplace/plugins/house-skills/` and the marketplace registry. | `direct` for 52 exported skills. | No GPT overlay required; no exclusions in the pack. | `decisions.md`, `decisions.json`, `intake.json`, and `provenance/house-skills.md` agree on the source split and projection shape. | None. |
| `adventures-pack` | First-party House Skills projection rooted in `codex-marketplace/plugins/house-skills/skills/` with provenance in `sources/first_party/skills/house-skills/*`. | Exposed through `codex-marketplace/plugins/adventures-pack/`. | `direct` for 18 exported skills. | No GPT overlay required; no exclusions in the pack. | `SOURCE.md`, `references/source-map.md`, and `references/bundle-manifest.json` describe the copied skills and dependency lanes consistently. | None. |
| `unslop` | Third-party retained upstream snapshot from `mshumer/unslop` in `sources/third_party/unslop/upstream/`. | Exposed through `codex-marketplace/plugins/unslop/`. | `direct` for 1 exported skill. | No GPT overlay required; no exclusions in the pack. | `SOURCE.md`, `bundle-manifest.json`, and `provenance/MARK-99-unslop.md` match the retained upstream package boundary. | None. |
| `game-studio` | Third-party retained upstream snapshot from `openai/plugins` in `sources/third_party/game-studio/upstream/`. | Exposed through `codex-marketplace/plugins/game-studio/`. | `direct` for 9 exported skills. | No GPT overlay required; no exclusions in the pack. | `SOURCE.md` and `references/bundle-manifest.json` describe the imported snapshot and normalized projection correctly. | None. |
| `wild-bunch-project-pack` | Mixed first-party House Skills source plus retained third-party browser-game helper source. | Exposed through `codex-marketplace/plugins/wild-bunch-project-pack/`. | `direct` for 10 exported skills. | Pack-local `hooks/` stay in source custody and are intentionally excluded from GPT zips. | `SOURCE.md`, `references/bundle-manifest.json`, and `references/provenance-map.json` keep the mixed-custody story consistent. | None. |
| `superpowers` | Third-party retained upstream `obra/superpowers` `v5.1.0` plus the first-party `linear-superpowers` projection. | Exposed through `codex-marketplace/plugins/superpowers/`. | Mix of `direct`, `overlay`, and `excluded` exports. | `7` overlay-backed skills, `5` direct skills, `3` excluded skills. Source-only harness surfaces stay in third-party custody. | `SOURCE.md`, `PROJECTION.md`, `references/bundle-manifest.json`, and `references/provenance-map.json` describe the source/projection split truthfully. | None. |

## Generated GPT Export Coverage

| Pack | Coverage | Observed export classes | Leakage / safety check |
| --- | --- | --- | --- |
| `house-skills` | 52 artifacts, all `direct`. | Direct exports only. | No forbidden harness surfaces appeared in any generated archive. |
| `adventures-pack` | 18 artifacts, all `direct`. | Direct exports only. | Skill-local `agents/openai.yaml` appears where defined by source, but no plugin harness metadata leaked into the zip payloads. |
| `unslop` | 1 artifact, `direct`. | Direct export only. | No plugin-only surfaces appeared in the generated zip payload. |
| `game-studio` | 9 artifacts, all `direct`. | Direct exports only. | No plugin-only surfaces appeared in the generated zip payloads. |
| `wild-bunch-project-pack` | 10 artifacts, all `direct`. | Direct exports only. | Pack `hooks/` remain source-only and do not appear in generated zips. |
| `superpowers` | 15 skill classes: `7 overlay`, `5 direct`, `3 excluded`. | Overlay-backed: `brainstorming`, `executing-plans`, `finishing-a-development-branch`, `requesting-code-review`, `using-superpowers`, `writing-plans`, `writing-skills`. Direct: `linear-superpowers`, `receiving-code-review`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`. Excluded: `dispatching-parallel-agents`, `subagent-driven-development`, `using-git-worktrees`. | The overlay manifest and archive contents agree; source-only harness metadata stayed out of the generated payloads. |

## Repair Routing

| Surface | Finding | Route |
| --- | --- | --- |
| All inspected marketplace packs | No repair required. The current source/projection split matches the declared posture. | None. |
| Generated `skill.zip` corpus | No forbidden plugin-harness surfaces were found in any of the 102 archives. | None. |
| `superpowers` overlay classes | Overlay-backed exports are already declared and present. | None. |
| Excluded export classes | The 3 excluded exports are intentionally withheld from raw GPT export. | None. |

## Non-Findings

- No `hooks/`, `.codex-plugin/`, `.agents/`, `package.json`, `README.md`, `SOURCE.md`, `PROJECTION.md`, `LICENSE`, or `marketplace.json` paths leaked into any generated `skill.zip`.
- `codex-marketplace/manifest.json` and `.agents/plugins/marketplace.json` matched.
- `generated/skill-zips/registry.json` matched the overlay manifest classification.
- The repo index and marketplace validators were aligned with the live tree.
- No follow-up issue was required for a repair finding.

## Validation Evidence

Validation commands run and passed:

- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_generated_drift.py --full-regeneration`
- `git diff --check HEAD~1 HEAD`

Archive-scan evidence:

- A `py -3` scan over all 102 generated `skill.zip` files found `0` forbidden plugin-harness surface matches.
