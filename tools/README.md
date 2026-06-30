# tools

Small helper scripts belong here.

Agent-facing policy for this directory lives in [AGENTS.md](AGENTS.md).

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` from the local plugin bundle and source ledger, and `--check` compares both files without writing.
- `update_skill_artifacts.py` is the canonical generator orchestrator for targeted skill updates, pack updates, and explicit full regeneration. Full regeneration runs the marketplace manifest, repo index, pack-manifest, mega-pack, projection, proof-map, and skill-zip generators in one deterministic pass. Targeted updates still refresh the mega-pack manifests before projection and zips so first-party removals and additions prune cleanly, but they are fallback repair paths rather than the preferred completion route.
- `package_skill_zips.py` remains the thin lower-level wrapper over `skill_zip_artifacts.py`.
- `validate_skill_zips.py` checks the canonical skill.zip surface and fails on stale, missing, malformed, or unregistered artifacts.
- `validate_generated_drift.py` rejects generated zips or registry entries that changed without the matching source, overlay, or packaging-tooling change, unless full regeneration was explicitly declared.
- `export_skill_zips.py` copies requested canonical artifacts into a manual GPT upload batch, writing `<out>/<skill-name>/skill.zip` plus `export-manifest.json`.
- `generate_repo_index.py` regenerates `repo-index/repo-index.json` and `--check` compares the rendered file without writing.
- `generate_pack_manifests.py` regenerates the selected pack bundle-manifest surfaces and `--check` compares them without writing.
- `materialize_projection.py` regenerates and validates projection-lane plugin skill trees and `--check` compares the materialized trees without writing.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, local path references, projection materialization, and selected pack bundle-manifest freshness for the protected marketplace shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces, but it is not the freshness proof for `repo-index/repo-index.json`.

Codex plugin first; generated GPT-safe skill zips second.

Current scope note: `generated/skill-zips/` is the GPT-ready export surface for
skill zips. It packages marketplace source plus any repo-owned GPT overlay
declared in `gpt-overlays/`.
`py -3 tools/rebuild_marketplace.py` is the canonical full reconciliation and validation entrypoint. It runs the full generator stack and the matching validators before a worker should return green.

Common worker update command:

```bash
py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>
```

Use `--pack` when the whole pack is wanted, `--all` or `--full-regeneration` for a repair-oriented explicit full refresh, and `--check` to validate the current generated surface without rewriting it. Prefer the wrapper above for normal completion.

The export helper still exists for manual GPT upload batches:

```bash
py -3 tools/export_skill_zips.py --skills <pack>/<skill>,<pack>/<skill> --out worker-output/<issue>/<name> --clean-output
```

Keep tooling minimal and focused on validation or lightweight asset handling.
