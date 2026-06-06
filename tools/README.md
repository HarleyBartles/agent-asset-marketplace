# tools

Small helper scripts belong here.

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` from the local plugin bundle and source ledger.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, and local path references.

Keep tooling minimal and focused on validation or lightweight asset handling.
