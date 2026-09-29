# Vendor profile deployment

## Ownership

`repo-standards/scripts/deploy_vendor_profiles.py` owns the one-shot deployment of `dist/plugins/*/assets/profiles/*.md` into `.agents/agents/`.

Vendor profile deployment is independent of plugin skill discovery and is run by the repository standards workflow.

## How it works

1. Read `.agents/plugins/marketplace.json`.
2. For every plugin with `policy.installation == "INSTALLED_BY_DEFAULT"`, find `assets/profiles/*.md`.
3. Compare those expected files with the current contents of `.agents/agents/`.
4. In `--apply` mode: copy any missing profiles and remove any orphan profiles not contributed by an installed plugin. In `--check` mode: only report what would change.

## Safe invocation

```bash
py -3 dist/plugins/agent-operating-model/skills/repo-shape/scripts/deploy_vendor_profiles.py --check
py -3 dist/plugins/agent-operating-model/skills/repo-shape/scripts/deploy_vendor_profiles.py --apply
```

The Marketplace build workflow calls this script automatically; do not run it directly unless you are testing or debugging.

## Local overrides

Repo-local agent profiles in `.devin/agents/` are user-managed. This script never reads, writes, or removes files in that directory.
