---
name: asset-market
description: Source-facing Asset Marketplace skill and pack acquisition with fidelity control. Use when Harley asks to get, pull, fetch, install, update, compare, or prepare the latest GPT skill or bundled skill pack from the asset marketplace repo, especially phrases like "using asset-market", "from the repo", or "latest marketplace version". Owns connector-backed repo source resolution, exact source reconstruction, pack-to-per-skill install-unit expansion, and source/projection ambiguity. Does not validate, package, present installable zips, or mutate the repo.
---

# Asset Market

## Owned decision

Resolve the canonical marketplace source for a requested GPT skill or bundled skill pack, then stage exact, fidelity-preserving skill source trees for downstream installation work.

This skill owns source acquisition, source-fidelity blocking, and pack-to-per-skill install-unit expansion. It does not author improvements, validate skill quality, package archives, present install cards, install skills, or mutate the marketplace repo.

## Source contract

Treat the asset marketplace repo as the source of truth only after it has been inspected through an available repo connector. Do not infer current repo paths, manifest state, latest skill contents, pack inventory, or projection mappings from memory, chat, Linear, prior package links, or installed local skills.

When connector access to the marketplace repo is unavailable, stop with `blocked_source_unavailable`. Do not reconstruct the skill or pack from memory unless Harley explicitly asks for new skill authoring rather than the marketplace version.

## Route classification

Classify the request before source inspection:

- `single_skill`: Harley asks for one named skill, such as `asset-market`, `adventures-bootstrap`, or `wild-bunch-domain-modeling`.
- `pack`: Harley asks for a bundled skill pack or plugin, such as `adventures-pack`, `wild-bunch-project-pack`, `install the Adventures project pack`, or `install all skills from a pack`.
- `comparison`: Harley asks to compare repo source, installed skill state, package contents, or projections without installation.
- `blocked_or_ambiguous`: the request could refer to multiple skills or packs and repo inspection cannot disambiguate.

For GPT installation, a pack is not itself the install unit. A pack is a repo source catalog that expands into a queue of single-skill install units.

## Single-skill workflow

1. Parse the requested skill name and route shape.
2. Inspect the marketplace repo through the connector and locate the canonical skill source, manifest entry, and any projection/source-map surfaces that govern the skill.
3. Stage the skill source exactly as found: preserve `SKILL.md`, `agents/openai.yaml`, scripts, references, assets, executable bits when available, and relative paths.
4. Partition evidence:
   - `repo_inspected`: files and manifests actually fetched.
   - `inferred`: path or ownership conclusions derived from inspected files.
   - `unavailable`: expected files or manifests the connector could not fetch.
5. If any required file is missing, ambiguous, stale, duplicated, or only inferred, stop before installation handoff and report the blocker.
6. Hand the staged source path and evidence packet to the appropriate downstream workflow when the user requested installation or packaging.

## Pack workflow

Use the pack workflow when Harley requests a project pack, plugin bundle, or all skills from a pack for GPT installation.

1. Inspect the pack root through the connector. Required pack evidence is:
   - `.codex-plugin/plugin.json` when present;
   - `SOURCE.md` when present;
   - `references/bundle-manifest.json` or an equivalent manifest that lists component skill names and local skill paths;
   - `references/source-map.md` or equivalent projection/source mapping when the manifest references canonical projections.
2. Confirm the pack root points to a normal skill directory, usually through `"skills": "./skills/"` in `.codex-plugin/plugin.json`, or through explicit component paths in the bundle manifest.
3. Expand the pack into install units. Each install unit must name one `target_skill` and one concrete skill folder under the inspected pack, usually `codex-marketplace/plugins/<pack>/skills/<skill-name>`.
4. Do not stage or hand off the pack root itself as a GPT-installable skill unless the user explicitly asks to install the pack-router skill and the pack contains a normal `skills/<pack-name>/SKILL.md` unit.
5. For each requested install unit, inspect the actual `SKILL.md` and any required sibling files before emitting a per-skill `asset_market_source_packet`.
6. For an `all skills from pack` request, return an `asset_market_pack_packet` first, then process install units as a one-at-a-time queue through the current install/projection lane. Do not claim the pack is installed because the queue was enumerated.

## Downstream transfer

Use this handoff only after the staged source is complete and source fidelity is green:

```yaml
asset_market_source_packet:
  target_skill: <skill-name>
  repo: <owner/name or connector identity>
  source_basis: repo_inspected
  staged_source_path: <path to exact staged skill folder>
  inspected_repo_paths:
    - <path>
  manifest_paths:
    - <path or []>
  unavailable_paths: []
  fidelity_status: green
  next_required_step: downstream-workflow
```

For pack enumeration, use this object before any per-skill downstream handoff:

```yaml
asset_market_pack_packet:
  target_pack: <pack-name>
  repo: <owner/name or connector identity>
  source_basis: repo_inspected
  pack_root: <repo path to pack root>
  plugin_manifest_path: <path or null>
  manifest_paths:
    - <bundle/source-map path>
  install_units:
    - target_skill: <skill-name>
      source_path: <repo path to one skill folder>
      role: <project | dependency | pack-router | unknown>
      projection_status: <projected | canonical | unknown>
  unavailable_paths: []
  fidelity_status: green
  next_required_step: downstream-workflow_per_unit
```

If fidelity is not green, do not call the package path. Return:

```yaml
asset_market_source_packet:
  target_skill: <skill-name or null>
  source_basis: blocked
  staged_source_path: null
  unavailable_paths:
    - <path or connector gap>
  fidelity_status: blocked_source_gap | blocked_ambiguous_source | blocked_duplicate_source | blocked_unavailable_connector | blocked_pack_manifest_gap | blocked_pack_install_units_ambiguous
  next_required_step: resolve_source_gap
```

For blocked pack requests, use the same blocked fields in `asset_market_pack_packet` and do not invent an install-unit list.

## Adjacent-skill boundaries

Use the current install/projection lane after source acquisition when the user wants an installable package or install handoff. For a pack, hand off one green `asset_market_source_packet` per install unit; do not ask a pack-level workflow to install the whole plugin or pack as one unit.

Use `skill-creator` only when Harley asks to create or modify skill content rather than reproduce the marketplace source exactly.

Use repo/GitHub proof or worker dispatch skills only when the task is to change or verify the marketplace repo itself. This skill is read-only with respect to repo state.

## Anti-drift rules

Do not silently fix descriptions, rewrite bodies, drop references, omit scripts, flatten assets, normalize names, or remove compatibility files while pulling a marketplace skill. A marketplace-source install must reproduce the repo skill, not create a cleaner local approximation.

Do not treat packaged zips, installed GPT skills, Linear descriptions, chat summaries, or pack-level prose as canonical source for a marketplace pull. They can be comparison inputs only after repo source has been inspected.

For projected skills that appear in multiple plugins, do not choose a projection from memory. Use the inspected pack manifest, source map, or explicit user route to decide whether to stage the house-skill projection, the project-pack projection, or another declared projection.

## Stop rule

Once the single-skill source packet, pack packet, or blocked source packet is produced, stop. Do not validate, package, or present a `skill.zip` from this skill.
