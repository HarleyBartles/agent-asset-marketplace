# tools

Small helper scripts belong here.

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` from the local plugin bundle and source ledger.
- `package_skill_zips.py` writes the canonical repo-resident `generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip` artifacts plus `generated/skill-zips/registry.json`.
- `validate_skill_zips.py` checks the canonical skill.zip surface and fails on stale, missing, malformed, or unregistered artifacts.
- `export_skill_zips.py` copies requested canonical artifacts into a manual GPT upload batch, writing `<out>/<skill-name>/skill.zip` plus `export-manifest.json`.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, and local path references for the protected marketplace shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces.

Common worker export command:

```bash
py -3 tools/export_skill_zips.py --skills <pack>/<skill>,<pack>/<skill> --out worker-output/<issue>/<name> --clean-output
```

Use `--pack` when the whole pack is wanted, `--skills` for a small requested subset, and `--from-file` when the worker receives a newline-delimited request list.

Keep tooling minimal and focused on validation or lightweight asset handling.
