# MARK-37 Activity Log

## Start Posture

- Date: 2026-06-06
- Branch start: `main`
- Starting main SHA: `f4795af126ce43e1bf772cf39ee5822be2863b34`
- Sync status: `git fetch origin` completed; local `main` already matched `origin/main`
- Surfaces read:
  - MARK-37 issue prompt
  - MARK-33 parent issue prompt
  - MARK-31 Adoption / Custody Note prompt

## Completion Notes

- Branch: `mark-37-marketplace-registry-gates`
- Registry source decision: `sources/house-skills/decisions.md` is the human registry source; `sources/house-skills/decisions.json` is the structured mirror consumed by tooling.
- Generator/check changes: `tools/generate_marketplace.py` now regenerates `.agents/plugins/marketplace.json`; `tools/validate_marketplace.py` now checks the registry export, plugin manifest, bundle manifest, source ledger, icon/path links, and bundle projection consistency.
- Documentation updates: `README.md`, `plugins/house-skills/README.md`, `plugins/house-skills/skills/house-skills/SKILL.md`, `plugins/house-skills/skills/house-skills/references/source-map.md`, `provenance/house-skills.md`, and `tools/README.md`.
- Validation passed:
  - `python -m json.tool .agents/plugins/marketplace.json`
  - `python -m json.tool plugins/house-skills/.codex-plugin/plugin.json`
  - `python -m json.tool plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
  - `python tools/validate_marketplace.py`
  - `git diff --check HEAD~1 HEAD`
  - `python -B -c "import ast, pathlib; ..."` for `tools/marketplace_utils.py`, `tools/generate_marketplace.py`, and `tools/validate_marketplace.py`
- Notes:
  - The bundle projection is intentionally scoped to the MARK-30 House Skills slice already represented in the bundle manifest.
  - `git diff --check` only reported line-ending warnings; no whitespace errors.
