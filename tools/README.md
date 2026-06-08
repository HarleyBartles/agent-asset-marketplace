# tools

Small helper scripts belong here.

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` from the local plugin bundle and source ledger.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, and local path references.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces.

Keep tooling minimal and focused on validation or lightweight asset handling.
