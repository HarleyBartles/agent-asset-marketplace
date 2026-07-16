# AGENTS.md

Scope: `.agents/skills/`

This scope contains agent skills installed from marketplace plugins.

## Purpose

This directory is the deterministic installation surface for skills from marketplace plugins that have `INSTALLED_BY_DEFAULT` policy in `.agents/plugins/marketplace.json`.

## Installation

Skills are installed and refreshed using the deterministic tooling:

```bash
py -3 tools/install_agent_skills.py
```

This tool:
- Reads `.agents/plugins/marketplace.json` to identify plugins with `INSTALLED_BY_DEFAULT` policy
- Copies skill directories from the plugin's `skills/` directory to `.agents/skills/`
- Removes orphan skills that no longer belong to any installed plugin
- Supports `--check` mode to report what would change without making changes

## Source of Truth

The source of truth for skill content is the marketplace plugin under `codex-marketplace/plugins/<pack-name>/skills/`. This `.agents/skills/` directory is a derived installation surface and should not be edited directly.

## Regeneration

When marketplace plugins are updated, run the full marketplace rebuild to refresh installed skills:

```bash
py -3 tools/rebuild_marketplace.py
```

This will regenerate marketplace projections and refresh installed skills automatically.

## Manual Refresh

To refresh skills without a full marketplace rebuild:

```bash
py -3 tools/install_agent_skills.py
```

## Check Mode

To check if skills need refresh without making changes:

```bash
py -3 tools/install_agent_skills.py --check
```
