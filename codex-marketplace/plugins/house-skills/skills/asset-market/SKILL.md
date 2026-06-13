---
name: asset-market
description: Fetch exact marketplace skill source for installation handoff. Use when Harley wants the latest marketplace version, a source packet, a clean comparison, or source-fidelity checks before skill packaging. Owns source acquisition and fidelity blocking only; it does not author skill content, validate skill quality, package archives, or present installable links.
---

# Asset Market

## Owned decision

Resolve the canonical marketplace source for a requested GPT skill and stage an exact, fidelity-preserving source tree for downstream installation work.

This skill owns source acquisition and source-fidelity blocking. It does not author improvements, validate skill quality, package archives, present install cards, install skills, or mutate the marketplace repo.

## Source contract

Treat the asset marketplace repo as the source of truth only after it has been inspected through an available repo connector. Do not infer current repo paths, manifest state, or latest skill contents from memory, chat, Linear, prior package links, or installed local skills.

When connector access to the marketplace repo is unavailable, stop with `blocked_source_unavailable`. Do not reconstruct the skill from memory unless Harley explicitly asks for a new skill rather than the marketplace version.

## Quick workflow

1. Parse the requested skill name and route shape.
2. Inspect the marketplace repo through the connector and locate the canonical skill source, manifest entry, and any projection/source-map surfaces that govern the skill.
3. Stage the skill source exactly as found: preserve `SKILL.md`, `agents/openai.yaml`, scripts, references, assets, executable bits when available, and relative paths.
4. Partition evidence:
   - `repo_inspected`: files and manifests actually fetched.
   - `inferred`: path or ownership conclusions derived from inspected files.
   - `unavailable`: expected files or manifests the connector could not fetch.
5. If any required file is missing, ambiguous, stale, duplicated, or only inferred, stop before installation handoff and report the blocker.
6. Hand the staged source path and evidence packet to `skill-installer` when the user requested installation or packaging.

## Handoff to skill-installer

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
  next_required_step: skill-installer
```

If fidelity is not green, do not call the package path. Return:

```yaml
asset_market_source_packet:
  target_skill: <skill-name>
  source_basis: blocked
  staged_source_path: null
  unavailable_paths:
    - <path or connector gap>
  fidelity_status: blocked_source_gap | blocked_ambiguous_source | blocked_duplicate_source | blocked_unavailable_connector
  next_required_step: resolve_source_gap
```

## Adjacent-skill boundaries

Use `skill-installer` after source acquisition when the user wants an installable package or install handoff.

Use `skill-creator` only when Harley asks to create or modify skill content rather than reproduce the marketplace source exactly.

Use repo/GitHub proof or worker dispatch skills only when the task is to change or verify the marketplace repo itself. This skill is read-only with respect to repo state.

## Anti-drift rules

Do not silently fix descriptions, rewrite bodies, drop references, omit scripts, flatten assets, normalize names, or remove compatibility files while pulling a marketplace skill. A marketplace-source install must reproduce the repo skill, not create a cleaner local approximation.

Do not treat packaged zips, installed GPT skills, Linear descriptions, or chat summaries as canonical source for a marketplace pull. They can be comparison inputs only after repo source has been inspected.

## Stop rule

Once the source packet is produced or blocked, stop. Do not validate, package, or present a `skill.zip` from this skill.
