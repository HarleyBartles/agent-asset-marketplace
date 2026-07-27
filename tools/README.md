# tools

Small helper scripts belong here.

Agent-facing policy for this directory lives in [AGENTS.md](AGENTS.md).

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` from the local plugin bundle and source ledger, and `--check` compares both files without writing.
- `update_skill_artifacts.py` is the canonical generator orchestrator for targeted skill updates, pack updates, and explicit full regeneration. Full regeneration runs the marketplace manifest, repo index, pack-manifest, mega-pack, projection, proof-map, first-party-catalog, and flat skill-zip generators in one deterministic pass.
- `project_skills.py` stages overlays, materializes plugin skill trees under `codex-marketplace/plugins/<pack>/skills/`, and writes flat deterministic `generated/skill-zips/<skill>.zip` archives. `--check` validates projected trees and zip shape without writing.
- `validate_skill_zips.py` checks the canonical flat `skill.zip` surface and fails on stale, missing, or malformed artifacts.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, local path references, projection materialization, and selected pack bundle-manifest freshness for the protected marketplace shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces, but it is not the freshness proof for `repo-index/repo-index.json`.
- `generate_repo_index.py` regenerates `repo-index/repo-index.json` and `--check` compares the rendered file without writing.
- `generate_pack_manifests.py` regenerates the selected pack bundle-manifest surfaces and `--check` compares them without writing.
- `rebuild_marketplace.py` is the canonical local full reconciliation and validation entrypoint. It runs the full generator stack and the matching validators before a worker should return green.
- `scripts/ci-preflight.sh --check` is the canonical CI gate. It runs the non-mutating checks and fails if the committed tree would need regeneration.

Codex plugin first; generated GPT-safe skill zips second.

Current scope note: `generated/skill-zips/` is the flat GPT-ready export surface
for skill zips. It is a deterministic copy of the staged Codex projection.
`py -3 tools/rebuild_marketplace.py` is the canonical local full reconciliation
and validation entrypoint. `bash scripts/ci-preflight.sh --check` is the canonical
CI gate.

Common worker update command:

```bash
py -3 tools/update_skill_artifacts.py --all
```

Use `--check` to validate the current generated surface without rewriting it.
The `--skill` and `--pack` flags remain as backwards-compatible aliases that
run the full pipeline.

Keep tooling minimal and focused on validation or lightweight asset handling.
