# Marketplace Generation Guide

Use this reference when working with marketplace generation, validation, and regeneration in the agent-asset-marketplace repo. This guide covers the canonical tooling, when to regenerate, and what validation to run.

## Before You Begin: Read the Standards

- **[`docs/custody-and-projection-doctrine.md`](../../docs/custody-and-projection-doctrine.md)** — source custody rules, provenance modes, plugin curation rules
- **[`tools/AGENTS.md`](../../tools/AGENTS.md)** — marketplace generation and validation tooling

## Canonical Tooling

### Local Rebuild (Write Mode)
```bash
py -3 tools/rebuild_marketplace.py
```

This is the canonical local rebuild and validation entrypoint. It:
- Regenerates all marketplace projections
- Refreshes installed skills
- Runs all validation checks
- Performs git diff checks on changed files

Use this when you have made changes to source custody, adapter files, projection plugin shapes, bundle manifests, source maps, provenance maps, or generated zips.

### CI Check (Read-Only Mode)
```bash
py -3 tools/check_marketplace.py
```

This is the canonical non-mutating CI gate. It:
- Checks if marketplace regeneration is needed
- Validates current marketplace state
- Checks installed skills freshness
- Performs git diff checks

Use this in CI to verify the committed state is current.

### Skills Installation
```bash
py -3 tools/install_agent_skills.py
```

Refreshes installed skills from marketplace plugins. Use this when:
- Skills have been modified in source
- Plugin configuration has changed
- You need to refresh without a full marketplace rebuild

Check mode:
```bash
py -3 tools/install_agent_skills.py --check
```

### Index Mesh Generation
```bash
py -3 tools/generate_index_mesh.py
```

Regenerates the repo-wide INDEX.md mesh. Use this when:
- Files have been added or removed
- Directories have been added or removed
- You need to update navigation

Check mode:
```bash
py -3 tools/generate_index_mesh.py --check
```

## When to Regenerate

You must run the full marketplace regeneration (`rebuild_marketplace.py`) after any change to:

- Source custody under `sources/first_party/` or `sources/third_party/`
- Codex adapter/overlay files under `adapters/codex/`
- Projection plugin shapes under `codex-marketplace/plugins/`
- Bundle manifests in plugin references
- Source maps or provenance maps
- Generated skill zips

Partial regeneration is a fallback-only repair path and should not be used as a normal completion route.

## Validation Standards

After regeneration, verify:

1. **All validation checks pass** — rebuild_marketplace.py runs validation automatically
2. **No git diff errors** — whitespace and formatting checks pass
3. **Installed skills are current** — install_agent_skills.py --check passes
4. **Index mesh is current** — generate_index_mesh.py --check passes

## Deterministic Pack Rule

If a skillset pack or projection lane lacks a manifest-driven generator/validator path, add one to `tools/` and wire it into the standard update/check entrypoints. Do not hand-edit projected skill trees, source maps, provenance maps, or zip artifacts.

## Editable Custody Inputs

The editable custody inputs for marketplace generation are:
- Source trees under `sources/`
- Codex overlay/adapter trees under `adapters/codex/`
- Pack registry under `codex-marketplace/custody-pack-registry.json`

Generated surfaces (manifests, projection trees, source maps, provenance maps, zip artifacts) must stay derived from these inputs.

## Source-of-Truth Split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks.

Linear remains the control plane for issue state, worker state, review posture, and closeout decisions. Do not treat a Linear note, worker report, or chat summary as repo truth until the repository state or an explicit follow-up issue preserves the consequence.

Generated artifacts are downstream outputs unless the repo explicitly says otherwise.
