# tools

Small helper scripts belong here.

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` from the local plugin bundle and source ledger.
- `package_skill_zips.py` writes the canonical repo-resident `generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip` artifacts plus `generated/skill-zips/registry.json`.
- `validate_skill_zips.py` checks the canonical skill.zip surface and fails on stale, missing, malformed, or unregistered artifacts.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, and local path references for the protected four-root shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces.

Keep tooling minimal and focused on validation or lightweight asset handling.
