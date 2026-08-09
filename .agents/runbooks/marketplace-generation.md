# Marketplace Generation Runbook

Use this reference when working with marketplace generation, validation, and regeneration in the agent-asset-marketplace repo. This runbook covers the canonical tooling, when to regenerate, and what validation to run.

## Before You Begin: Read the Standards

- **[`.agents/doctrine/custody-and-marketplace-doctrine.md`](../../.agents/doctrine/custody-and-marketplace-doctrine.md)** — source custody rules, provenance modes, plugin curation rules
- **[`.devin/rules/tools.md`](../../.devin/rules/tools.md)** — marketplace generation and validation tooling

## Canonical Tooling

### Local Rebuild (Write Mode)
```bash
tools/run marketplace --apply
```

In a shared or git-worktree checkout, also pass `--allow-shared-checkout` to approve writes.

This is the canonical local rebuild and validation entrypoint. It:
- Regenerates the marketplace manifest
- Refreshes installed skills
- Runs all validation checks
- Regenerates the repo index and index mesh

Use this when you have made changes to plugin skill files, bundle manifests, plugin manifests, provenance records, or adapter files.

### What `tools/run` does

`tools/run` is the canonical **local full reconciliation** command. It writes derived marketplace surfaces and then validates them. Think of it as the single "refresh marketplace" call.

#### Editable inputs (do not edit the derived surfaces by hand)

- `codex-marketplace/plugin-roots.json` — discovered active plugin roots
- `codex-marketplace/plugins/<plugin>/skills/<skill>/` — canonical skill source trees
- `codex-marketplace/plugins/<plugin>/SOURCE.md` — per-pack source custody and provenance

#### Execution flow

The `marketplace` target runs the generator/validator stack in order:

1. `inventory` — refreshes `codex-marketplace/plugin-roots.json` and validates plugin roots.
2. `installed-skills` — refreshes `.agents/skills/` for installed plugins.
3. `repo-index` — writes the root `INDEX.json` registry and each zone's per-directory `INDEX.json` sidecar.
4. `mesh` — regenerates repo-wide `INDEX.md` navigation mesh.
5. `validate` — structural validation of plugin trees, manifests, and bundle manifests.
6. `marketplace` — final aggregate validation.

#### Key outputs

- Marketplace manifests: `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`
- Plugin roots: `codex-marketplace/plugins/<pack>/`
- Bundle manifests: `codex-marketplace/plugins/<pack>/references/bundle-manifest.json`
- Root index: `INDEX.json`; zone sidecars: `codex-marketplace/INDEX.json`, `.agents/plugins/INDEX.json`, `.agents/plans/INDEX.json`, `.agents/specs/INDEX.json`, `tools/INDEX.json`, `codex-marketplace/plugins/INDEX.json`
- Index mesh: `INDEX.md` files throughout the repo
- Installed skills: `.agents/skills/<skill>/`

#### When it fails

- A missing `README.md`/`SOURCE.md`/`LICENSE` in a plugin root usually means a hand-maintained pack doc was deleted during a merge.
- A `validate_marketplace` failure usually means a bundle manifest or plugin manifest is out of sync with the registry.
- A `validate_repo_index` failure usually means the repo index is stale.

Run the same command again after fixing the underlying source; do not hand-edit derived outputs.

### CI Check (Read-Only Mode)
```bash
tools/run ci --check
```

This is the canonical non-mutating CI gate. It:
- Checks if marketplace regeneration is needed
- Validates current marketplace state
- Checks installed skills freshness
- Performs git diff checks

Use this in CI to verify the committed state is current.

### Skills Installation
```bash
tools/run installed-skills --apply
```

In a shared or git-worktree checkout, also pass `--allow-shared-checkout`.

Refreshes installed skills from marketplace plugins. Use this when:
- Skills have been modified in source
- Plugin configuration has changed
- You need to refresh without a full marketplace rebuild

Check mode:
```bash
tools/run installed-skills --check
```

### Index Mesh Generation
```bash
tools/run mesh --apply
```

In a shared or git-worktree checkout, also pass `--allow-shared-checkout`.

Regenerates the repo-wide INDEX.md mesh. Use this when:
- Files have been added or removed
- Directories have been added or removed
- You need to update navigation

Check mode:
```bash
tools/run mesh --check
```

## When to Regenerate

You must run the full marketplace regeneration (`tools/run marketplace --apply`) after any change to:

- Canonical plugin skills under `codex-marketplace/plugins/<plugin>/skills/`
- Per-pack `SOURCE.md` provenance records under `codex-marketplace/plugins/<plugin>/SOURCE.md`
- Bundle manifests in plugin `references/`
- Plugin manifests under `codex-marketplace/plugins/<plugin>/.codex-plugin/`

Partial regeneration is a fallback-only repair path and should not be used as a normal completion route.

## Validation Standards

After regeneration, verify:

1. **All validation checks pass** — `tools/run marketplace --apply` runs validation automatically
2. **No git diff errors** — whitespace and formatting checks pass
3. **Installed skills are current** — `tools/run installed-skills --check` passes
4. **Index mesh is current** — `tools/run mesh --check` passes

## Deterministic Pack Rule

If a plugin pack lacks a manifest-driven generator/validator path, add one to `tools/` and wire it into the standard `tools/run` entrypoints. Do not hand-edit marketplace manifests, bundle manifests, or installed skill surfaces.

## Editable Custody Inputs

The editable custody inputs for marketplace generation are:
- Canonical skill trees under `codex-marketplace/plugins/<plugin>/skills/`
- Per-pack provenance records under `codex-marketplace/plugins/<plugin>/SOURCE.md`
- Plugin metadata under `codex-marketplace/plugins/<plugin>/.codex-plugin/`

Generated surfaces (manifests, bundle manifests, repo index, index mesh, installed skills) must stay derived from these inputs.

## Source-of-Truth Split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks.

Linear remains the control plane for issue state, worker state, review posture, and closeout decisions. Do not treat a Linear note, worker report, or chat summary as repo truth until the repository state or an explicit follow-up issue preserves the consequence.

Generated artifacts are downstream outputs unless the repo explicitly says otherwise.
