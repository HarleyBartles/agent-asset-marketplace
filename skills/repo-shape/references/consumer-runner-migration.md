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

Commit or otherwise preserve the current consumer state. Record the marketplace-source gitlink revision, current standards contract, plugin subscriptions, runner command map, tracked hook, hosted workflow, and generated index files. Confirm the check/apply outer commands and hosted staged-snapshot behavior before changing internals.

Keep the ambient plugin subscriptions and installed projections during preparation. The old runner still calls the installed refresh and mesh scripts, and the old pinned repo-shape checker may still enforce its bootstrap plugin prerequisites. Do not remove those inputs yet.

### 2. Pin the compatibility source and prepare selected standards

Advance the marketplace-source gitlink to the published source SHA containing the no-op ambient plugin prerequisite check, deployable standards catalog, pinned checker resources, capability-based runbook contract, and retired mesh source. Do not run skill refresh from the old runner after this pin changes.

From the pinned checkout, preview the legacy selection and deployment:

```powershell
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/migrate_operating_standards.py --check
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/deploy_operating_standards.py --prepare-migration --check
```

Review the proposed standards against the repository's actual policy. The migration preview derives a proposal from legacy operating-model surface exceptions. Edit the composition deliberately so it contains only standards the repository adopts, including an empty marketplace selection when appropriate. Plugin subscriptions do not select standards.

Prepare the selected resources and migrate the contract by invoking the scripts in the pinned checkout:

```powershell
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/deploy_operating_standards.py --prepare-migration --apply --yes
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/migrate_operating_standards.py --apply
py -3 .agents/plugins/marketplace-source/skills/repo-shape/scripts/deploy_operating_standards.py --check
```

Migrate runbooks and playbooks to `Required capabilities`, `Optional capabilities`, `Required repository-owned skills`, and `Optional repository-owned skills`. Describe ambient needs as capabilities and select suitable providers from skills exposed at runtime. Put exact names only for genuine local skills declared in `repo.local_skills`. A missing required capability must stop dependent work and be reported; an unavailable optional capability may be reported and skipped. Legacy `Required skills` remains a temporary compatibility form, not evidence that an ambient provider exists.

Do not run the complete old `tools/run.py ci` after advancing the pin and before the runner cutover. It still calls the old projection-based refresh and mesh scripts.

### 3. Cut over the runner and mesh calls together

In one consumer change, keep the outer `tools/run.py ci --apply` and `tools/run.py ci --check` commands but update all internal calls:

- Run selected standards through `.agents/standards/_runtime/repo_standards.py`.
- Run refresh from `.agents/plugins/marketplace-source/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` with `--no-roll-marketplace-source`.
- Remove mesh generation and validation targets and every runner, hook, or workflow call to them.
- Remove any tool-specific mesh validator and tracked generated `INDEX.md` and `INDEX.json` artifacts.
- Preserve unrelated local checks, consumer-owned standards, and the staged-snapshot hook contract.

Do not invoke refresh while the old runner still calls mesh scripts. Stage the source pin, standard composition and deployed resources, runner, hooks, and mesh removal as a coherent cutover. Run `tools/run.py ci --apply` and `tools/run.py ci --check` only after that complete runner change is present. The refresh can then update projections without removing a script that the active runner still needs. Verify standard provenance does not change during skill refresh.

Hosted CI must run the same consumer-owned command and deployed selected checkers from the pinned source. It must not need Codex, ambient plugin installations, or copied ambient skill projections. Keep `.agents/plugins/marketplace.json` when the refresh utility needs it to declare the plugin list and genuine `repo.local_skills`; the plugin list may be empty, and its contents do not prove that any ambient runtime capability is available.

### 4. Remove copied ambient subscriptions only after cutover passes

After the updated tracked hook and hosted validation pass, remove subscriptions and copied skill/plugin material whose only purpose was to supply ambient workflow, standards, refresh, or mesh implementation. Preserve unrelated plugins and genuine repository-owned skills. Refresh installed projections with the new runner and rerun the canonical check and tracked hook with the ambient plugin list empty. Keep only the standards explicitly declared in the operating-standards composition.

A subscription or skill projection is not a standard adoption declaration. Removing the five ambient plugin subscriptions does not remove a standard that the repository explicitly selected and deployed.

## Recovery

If a preview or deployment fails, stop before activating the new contract or changing the runner. The legacy declaration and runner remain authoritative at that point.

If runner or hook validation fails after activation, restore the saved consumer commit, including its prior marketplace-source gitlink, standards files, runner, and plugin configuration, then rerun its prior validation. This rollback restores the complete previous state, including the matching old marketplace-source revision. Do not restore retired mesh calls against a marketplace-source revision that no longer provides them. Once the consumer advances to the post-retirement pin, either complete mesh-call removal or revert the whole migration to the recorded prior pin.

## Completion evidence

A migration is ready when the consumer's check and apply commands and tracked hook pass; hosted validation passes without ambient projections; only declared standards run from pinned deployed resources; refresh runs from the pinned marketplace-source checkout; no mesh calls or generated index artifacts remain; and standards provenance is unchanged by skill refresh.
