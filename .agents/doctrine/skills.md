## Scope

`.agents/skills/`

This scope contains agent skills installed from marketplace plugins.

## Purpose

This directory contains two custody lanes:

- marketplace-derived skills copied from plugins with `INSTALLED_BY_DEFAULT` policy; and
- tracked repository-local skills declared by exact name in `repo.local_skills` in `.agents/plugins/marketplace.json`.

Marketplace-derived skills are generated output. Registered local skills are authored local custody and are not part of marketplace provenance. Prefixes are optional naming choices, not custody requirements.

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

The installer validates and preserves every valid skill named in `repo.local_skills`. It rejects name collisions with marketplace content and does not remove registered local skill directories as orphans.

## Source of Truth

For marketplace-derived skills, canonical source is under `skills/<skill-id>/` in this repository; the installed plugin copy under `dist/plugins/<plugin>/skills/` is generated and should not be edited directly. Ambient plugins are available to agents through the runtime and are not installed in `.agents/skills/` here.

For repository-local skills declared in `repo.local_skills`, the source of truth is the tracked local directory under `.agents/skills/`. Those skills are local custody and may be edited directly; they are not regenerated from marketplace content or included in marketplace provenance.

## Regeneration

When marketplace plugins are updated, rebuild the packages and then refresh this repository's subscribed installed skills:

```bash
tools/run marketplace --apply
tools/run refresh-skills --apply
```

The refresh updates only plugins listed as installed by default in `.agents/plugins/marketplace.json`.

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
