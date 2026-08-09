# Repo Index

The repo index is the machine-readable navigation surface for the repository. It lives in two layers:

- **Root `INDEX.json`** at the repository root is a thin registry. It lists the repository's zones and points each zone at its own sidecar.
- **Per-zone `INDEX.json` sidecars** live next to the things they describe (e.g. `codex-marketplace/INDEX.json`, `tools/INDEX.json`). Each sidecar carries zone-specific metadata such as `surface_kind`, `nearest_scoped_agents_md`, `key_validation_scripts`, and any data that the `INDEX.md` mesh does not already express.

The index exists so agents can traverse the repository without depending on chat memory, embeddings, or a separate discovery runtime. It records the main repo zones, the nearest scoped `AGENTS.md` file where one exists, and the validation or generation hooks that matter for a path.

## How to use it

- Start with the root `INDEX.json` when you need a compact map of the repo zones.
- Read a zone's `INDEX.json` sidecar when you need zone-local metadata, validation scripts, or structured inventory such as `marketplace_plugins`.
- Use the `zones` entries to find the nearest guidance file and the right validation or generation hook for a path.
- Treat the index as navigation metadata only. It helps you find repo truth; it does not replace manifests, ledgers, per-pack `SOURCE.md` provenance, or the files on disk themselves.

## Validation

Keep the index current with the repo's canonical commands:

- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/generate_repo_index.py --apply`
- `py -3 tools/generate_marketplace.py --apply`
- `py -3 tools/generate_marketplace.py --check`
- `py -3 tools/generate_repo_index.py --check`
- `py -3 tools/run.py mesh --apply`
- `py -3 tools/run.py ci --check`

If the root `INDEX.json` or a zone sidecar is stale, the check commands above fail with a clear error. Regenerate the index with `py -3 tools/generate_repo_index.py --apply` and the `INDEX.md` mesh with `py -3 tools/run.py mesh --apply` when zones or their metadata change.
