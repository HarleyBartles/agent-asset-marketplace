# Consumer runner migration after index mesh retirement

This guide moves a consumer from ambient plugin copies and installed-skill runner paths to an explicit standards composition. It keeps the repository's outer `tools/run.py ci --apply` and `tools/run.py ci --check` commands and tracked staged-snapshot hook as the local and hosted entrypoints.

The example contract below is a portable fixture for the runner boundary. Preserve each consumer's own command bus and standard IDs when applying the migration.

```json consumer-runner-contract
{
  "outer_commands": {
    "check": ["tools/run.py", "ci", "--check"],
    "apply": ["tools/run.py", "ci", "--apply"]
  },
  "standards_dispatcher": ".agents/standards/_runtime/repo_standards.py",
  "refresh_script": ".agents/plugins/marketplace-source/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py",
  "refresh_options": ["--no-roll-marketplace-source"]
}
```

## Migration sequence

### 1. Record the starting state

Commit or otherwise preserve the current consumer state. Record the marketplace-source gitlink revision, the current standards contract, plugin subscriptions, runner command map, tracked hook, hosted workflow, and generated index files. Confirm the check/apply outer commands and hosted staged-snapshot behavior before changing their internals.

Do not update the marketplace-source pin and remove mesh calls in separate unvalidated steps. The pinned revision after Plan 1 has no mesh generator, validator, skill, or generated index files.

### 2. Preview and deploy only selected standards

From the consumer's pinned marketplace-source checkout, review the legacy selection and deployment previews:

```powershell
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/migrate_operating_standards.py --check
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/deploy_operating_standards.py --prepare-migration --check
```

Review the proposed standards against the consumer's actual policy. The migration preview derives the selection from the legacy operating-model surface exceptions. Edit the proposed composition deliberately if the repository wants a smaller set or no marketplace standards. Marketplace plugin subscriptions do not select standards.

After approving the composition, deploy its selected, pinned resources before activating the new contract:

```powershell
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/deploy_operating_standards.py --prepare-migration --apply --yes
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/migrate_operating_standards.py --apply
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/deploy_operating_standards.py --check
```

Run the consumer's current canonical check while it still uses its existing runner. Resolve deployment or validation errors before changing the runner. Deployment writes only the selected standard implementations, the generic dispatcher needed for those selections, and their provenance. An empty marketplace selection does not require marketplace runtime files.

### 3. Point selected-standard checks at deployed inputs

Update the consumer's internal standards command to invoke the deployed dispatcher at `.agents/standards/_runtime/repo_standards.py`. The dispatcher reads `.agents/contracts/operating-standards.json` and runs only declared standards and dependencies. Keep repository-owned standards in their own declared implementation roots.

The hosted workflow must run the same canonical `ci --check` command through the tracked hook with its existing staged-snapshot marker. Its clean checkout needs the composition, deployed selected resources, and pinned marketplace-source gitlink. It must not need Codex, ambient plugin installation, `.agents/skills/`, or `.agents/plugins/marketplace.json`.

Run the consumer's full check and hosted-hook parity fixture before removing any plugin subscription. Check that the hook still applies only generated surfaces owned by the consumer and checks the exact staged snapshot.

### 4. Move skill refresh to the pinned marketplace source

Change the refresh implementation path from:

```text
.agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py
```

to:

```text
.agents/plugins/marketplace-source/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py
```

Pass `--no-roll-marketplace-source` in deterministic CI so the runner consumes the committed gitlink instead of trying to advance it. Preserve explicit mutation safeguards for local apply. A shared checkout must pass `--allow-shared-checkout` together with `--apply`; a linked worktree follows the utility's normal apply path. Do not invoke a copied Repo Worker Pack refresh script.

Run both existing outer commands after the path change:

```powershell
py -3 tools/run.py ci --check
py -3 tools/run.py ci --apply
```

Then verify skill refresh changes only the consumer's installed skill projection and its skill provenance. The operating-standards composition, deployed checkers, and standards provenance must remain unchanged.

### 5. Remove index-mesh calls and artifacts

Remove the consumer's mesh generation and validation targets and every runner, hook, or workflow call to them. Delete tracked generated `INDEX.md` and `INDEX.json` files owned by the retired mesh. Remove mesh-specific checks and documentation. There is no replacement mesh command or generated index surface.

Run the full consumer check, then search tracked files and runner targets for mesh calls and generated index artifacts. A migration is incomplete if any hook or hosted workflow still invokes a retired mesh command.

### 6. Remove ambient subscriptions that are no longer needed

Only after steps 2 through 5 pass, remove subscriptions and copied skill/plugin material that existed solely to supply refresh, mesh, or standards implementation files. Keep genuinely useful ambient plugins available to agents if desired. Their presence or absence does not change the repository's declared standards.

Run the canonical check and tracked hook with ambient skill projections and marketplace plugin configuration absent in the hosted fixture. Confirm the outer command contract remains `ci --apply` and `ci --check`.

## Recovery

If a preview or deployment fails, stop before activating the new contract or changing the runner. The legacy declaration and runner remain authoritative at that point.

If runner or hook validation fails after activation, restore the saved consumer commit, including its prior marketplace-source gitlink, standards files, runner, and plugin configuration, then rerun its prior validation. This rollback restores the complete previous state, including the matching old marketplace-source revision. Do not restore retired mesh calls against a marketplace-source revision that no longer provides them. Once the consumer advances to the post-retirement pin, either complete mesh-call removal or revert the whole migration to the recorded prior pin.

## Completion evidence

A migration is ready when the consumer's check and apply commands and tracked hook pass; hosted validation passes without ambient projections; only declared standards run from pinned deployed resources; refresh runs from the pinned marketplace-source checkout; no mesh calls or generated index artifacts remain; and standards provenance is unchanged by skill refresh.
