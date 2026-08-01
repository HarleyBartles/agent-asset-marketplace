
## Scope

`.agents/skills/`

This scope contains agent skills installed from marketplace plugins.

## Purpose

This directory contains two custody lanes:

- marketplace-derived skills copied from plugins with `INSTALLED_BY_DEFAULT` policy; and
- tracked repository-local skills under the reserved `mark-*` prefix.

Marketplace-derived skills are generated output. `mark-*` skills are authored local custody and are not part of marketplace provenance.

## Installation

Skills are installed and refreshed using the deterministic tooling:

```bash
tools/run installed-skills --apply
```

This tool:
- Reads `.agents/plugins/marketplace.json` to identify plugins with `INSTALLED_BY_DEFAULT` policy
- Copies skill directories from the plugin's `skills/` directory to `.agents/skills/`
- Removes orphan skills that no longer belong to any installed plugin
- Supports `--check` mode to report what would change without making changes

The installer validates and preserves every valid `mark-*` directory. It never copies marketplace content over a `mark-*` name and never removes a `mark-*` directory as an orphan.

## Source of Truth

For marketplace-derived skills, the source of truth is the marketplace plugin under `codex-marketplace/plugins/<pack-name>/skills/`. Those installed skills are generated output and should not be edited directly.

For repository-local `mark-*` skills, the source of truth is the tracked local directory under `.agents/skills/`. Those skills are local custody and may be edited directly; they are not regenerated from marketplace content or included in marketplace provenance.

## Regeneration

When marketplace plugins are updated, run the full marketplace rebuild to refresh installed skills:

```bash
tools/run marketplace --apply
```

This will regenerate marketplace projections and refresh installed skills automatically.

## Manual Refresh

To refresh skills without a full marketplace rebuild:

```bash
tools/run installed-skills --apply
```

## Check Mode

To check if skills need refresh without making changes:

```bash
tools/run installed-skills --check
```
