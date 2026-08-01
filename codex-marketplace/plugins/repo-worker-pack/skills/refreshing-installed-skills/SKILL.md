---
name: refreshing-installed-skills
description: Use when a worktree is initialized or .agents/skills/ is stale from the plugin source.
metadata:
  source-id: refreshing-installed-skills
  source-path: sources/first_party/skills/refreshing-installed-skills/SKILL.md
  provenance-name: Refreshing Installed Skills first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Install or refresh .agents/skills/ from the plugin source.
  use_when:
  - Use when creating a new worktree.
  - Use after updating the marketplace-source submodule.
  - Use when .agents/skills/ appears stale.
  do_not_use_when:
  - Do not use when only the INDEX.md mesh is stale without any skill changes; use generating-agent-mesh instead.
  related_skills:
  - generating-agent-mesh
  - using-git-worktrees
license: MIT
---

# Refreshing Installed Skills

Install or refresh `.agents/skills/` from the plugin source.

## When to Use

- After creating a new worktree.
- After updating the `marketplace-source` submodule in a consumer repo.
- When `.agents/skills/` appears stale.

## Usage

```bash
py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply
py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --check
```

This skill runs the bundled `refresh_installed_skills.py` core, which installs/refreshes `.agents/skills/` from the plugins declared in `.agents/plugins/marketplace.json`, and rolls the optional `marketplace-source` submodule to `origin/main`. It defaults to `--check` mode; pass `--apply` to write files. When running from a linked worktree, add `--apply --allow-shared-checkout`.

## Plugin source types

Each plugin entry in `.agents/plugins/marketplace.json` declares its source with `source.source`:

- `local`: `source.path` is relative to the consumer repo root.
- `github`: `source.path` is relative to the `marketplace-source` submodule root (`.agents/plugins/marketplace-source`).

Both `local` and `github` sources are normalized and must resolve to a directory under their respective roots.

## Local skill validation extension

After the bundled core validates that local skill directories match their frontmatter names and do not collide with reserved marketplace prefixes, it calls a repo-supplied extension script if one exists:

- `scripts/validate_local_skills_extra.sh` — bash script; receives `--check` followed by the skills root and any local skill prefixes.
- `scripts/validate_local_skills_extra.ps1` — PowerShell script; must declare `param([switch]$Check, [Parameter(ValueFromRemainingArguments=$true)][string[]]$Remaining)`.

Example invocation:

```text
scripts/validate_local_skills_extra.sh .agents/skills wild-bunch-
```

In `--check` mode the script must report errors and exit non-zero if invalid. In write mode it may also auto-fix or just validate. The skill fails with a clear error if the hook exits non-zero.

## Provenance

`.agents/skills/.provenance.json` records the marketplace-source version that was installed. When the `marketplace-source` submodule is present, `manifestSha` tracks the submodule HEAD; otherwise it falls back to a SHA-256 content hash of the effective marketplace configuration (`.agents/plugins/marketplace.json`). `syncedPlugins` lists every plugin configured as `INSTALLED_BY_DEFAULT`, in order, regardless of whether its skills needed copying on this run.

It also records:

- `localSkills`: the names of any skills installed from the consumer repo's local skill source (declared by `repo.local_skill_prefixes`).
- `localPlugins`: the names of any plugins whose skills were installed from a `local` source.
- `marketplace`: the source repository and source path used for the marketplace.
- `marketplaceFile`: the path to `.agents/plugins/marketplace.json`.
- `syncedSkills`: the count of skills copied from marketplace plugins.
- `vendorProfiles`: an array of vendor subagent profiles installed from pack `assets/profiles/*.md`. Each entry records `plugin` (the pack name), `sourcePath` (the pack `assets/profiles` directory), and `profiles` (the list of installed `.md` profile file names).
- `syncedAt`: the timestamp of the last refresh.

## Vendor subagent profiles

For each installed plugin, the core also looks for `assets/profiles/*.md` inside the plugin root and copies those profiles into the consumer's agent search path:

- `.agents/agents/<profile>.md` — always written when profiles are present.
- `.devin/agents/<profile>.md` — also written when `.devin/agents/` already exists, so the Devin Desktop search path documented in `selecting-a-subagent` finds them.

Orphan vendor profiles (files in those directories that no installed plugin contributes) are removed on refresh, mirroring the orphan-skill cleanup. The `vendorProfiles` provenance array records which plugin installed which profiles, alongside the existing `localSkills` and `syncedPlugins` fields.

Provenance is now rewritten when the installed plugin list, the local skill inventory, or the marketplace metadata changes, even if no marketplace skill files were copied. Because of this, `--check` may report a stale provenance file and `--apply` will update it without unnecessary skill copying.
