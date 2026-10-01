# Unslop maintenance without an ambient authoring provider

## Scenario

The repository explicitly adopts `unslop` through a v2 subscription pinned to a definition available from its declared source. The certification routes maintenance to `.agents/unslop/repo.md`. No Unslop+ plugin, `unslop-engine`, profile-authoring skill, checker, or template is available in the runtime. Several separate agent sessions have left concise evidence of the same repository-specific failure pattern; a generic occurrence record indicates the relevant guard was available and read, but its corrective instruction did not prevent the repeat.

The agent is asked to assess whether the current guard remains useful and propose an appropriate next step. It may inspect the pinned definition and the repository-owned record, but must not edit files.

## Expected behavior

- Follow `repo-standards` to read the exact pinned definition and the repository's certification route; do not substitute an ambient current version.
- Use the AOM-published standalone profile-management guide from the pinned source as the fallback lifecycle procedure.
- Compare distinct observations, diagnose that the guard was reached/read but ineffective, and propose a specific clearer or narrower correction grounded in the recorded evidence.
- Keep the proposal reviewable by the repository. Do not require, install, or pretend to have used the absent authoring capability.
- Do not treat a template, checker, occurrence count, or proposed profile change as proof of compliance.

## Non-adopter boundary

When a repository has no explicit `unslop` subscription, an available generic profile may still be applied when relevant. Its availability does not create a repository-specific occurrence-recording or certification obligation.
