# Superpowers Source Refresh Runbook

Use this runbook to update the retained upstream Superpowers source to the
latest release, update the adapter, regenerate the marketplace surfaces, and
validate the result.

## Preconditions

- The repo is on a fresh `main` branch or a branch created from fresh `main`.
- The upstream release tag and commit are known.
- The adapter overlay exists and may need a manual edit before regen.

## Procedure

1. Run the deterministic updater:

   ```powershell
   py -3 tools/update_superpowers_source.py --tag <latest-tag> --prepare
   ```

2. If the updater reports adapter drift, edit the adapter surfaces first:
   - `adapters/codex/superpowers-plus/using-superpowers/overlay.yaml`
   - `adapters/codex/superpowers-plus/using-superpowers/agents/openai.yaml`

3. Re-run the deterministic updater with regeneration:

   ```powershell
   py -3 tools/update_superpowers_source.py --tag <latest-tag> --regen
   ```

4. Validate the output:

   ```powershell
   py -3 tools/validate_marketplace.py
   py -3 tools/validate_repo_index.py
   git diff --check
   ```

5. Commit, push, and open a PR only after validation passes.

## Failure handling

- If the adapter goes stale, update it before regeneration.
- If the retained source snapshot cannot be moved cleanly to one latest version,
  stop and open a follow-up issue.
- If validation fails, fix the script or source, not the generated output.

## Related doctrine

- `.agents/docs/playbook-runbook-doctrine.md`
- `.agents/playbooks/superpowers-refresh-playbook.md`
