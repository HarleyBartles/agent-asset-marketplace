# tools

Small helper scripts belong here.

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` from the local plugin bundle and source ledger.
- `update_skill_artifacts.py` is the worker-facing entrypoint for targeted skill updates, pack updates, and explicit full regeneration.
- `package_skill_zips.py` remains the thin lower-level wrapper over `skill_zip_artifacts.py`.
- `validate_skill_zips.py` checks the canonical skill.zip surface and fails on stale, missing, malformed, or unregistered artifacts.
- `validate_generated_drift.py` rejects generated zips or registry entries that changed without the matching source change, unless full regeneration was explicitly declared.
- `export_skill_zips.py` copies requested canonical artifacts into a manual GPT upload batch, writing `<out>/<skill-name>/skill.zip` plus `export-manifest.json`.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, and local path references for the protected marketplace shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces.

Common worker update command:

```bash
py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>
```

Use `--pack` when the whole pack is wanted, `--all` or `--full-regeneration` for an explicit full refresh, and `--check` to validate the current generated surface without rewriting it.

The export helper still exists for manual GPT upload batches:

```bash
py -3 tools/export_skill_zips.py --skills <pack>/<skill>,<pack>/<skill> --out worker-output/<issue>/<name> --clean-output
```

Keep tooling minimal and focused on validation or lightweight asset handling.
