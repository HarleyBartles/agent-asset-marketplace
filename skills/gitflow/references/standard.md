# Gitflow Standard

**Standard ID:** `gitflow`

## Pledge

The repository declares and follows a branch model that separates integration from the stable release line, routes ordinary changes through integration, and promotes reviewed release or urgent fix work without losing fixes or future work during reconciliation.

## Applicability

Gitflow is an optional branching pattern for products that need deliberate release stabilization or concurrent supported release lines. Assess fit before adoption. Continuous delivery with no parallel release lines may be served by a simpler branch workflow; do not impose Gitflow because its skill or plugin is available.

## Required implementation

- Declare the repository's stable release branch and integration branch by name. The conventional names in this standard are `main` and `develop`; a repository can map the same roles to its own branch names and document the mapping.
- Route ordinary feature work from current integration state back into integration. Do not send ordinary feature work directly to the stable release line. Repository-specific branch prefixes are permitted.
- Start a release branch from integration. Limit it to release identity, notes, packaging, and stabilization work. Promote the reviewed release to the stable line and reconcile release changes into integration.
- Start a hotfix branch from the released stable state. Verify and promote the fix to the stable line, identify the immutable released source, then reconcile the fix into integration and each active release line that needs it.
- Declare merge strategy for feature, release, hotfix, and reconciliation routes. Preserve release and hotfix ancestry where needed to show what was promoted and returned; a repository may permit squash merges for ordinary feature work.
- Reconcile against the current source and intended version state. A release or hotfix merge-back that leaves integration at the released baseline uses the stable product version. It does not invent a development prerelease. If ongoing next-release development already exists, preserve that intended line and incorporate the fix without discarding development work or reusing a checkpoint identity.
- Declare how branch routing, merge results, and current hosting policies are verified. Do not claim branch protection, required checks, review rules, or successful reconciliation from branch names or local documentation alone.

## Conditional obligations

- When the repository also adopts `semver`, apply the joint development-checkpoint and release-candidate cadence defined by that standard. Gitflow alone does not require an application version, SemVer syntax, `dev.N`, or `rc.N`.
- Where an active release branch exists, reconcile fixes that affect its candidate or supported release into that branch under its declared validation policy.
- If CI or repository protection exists, declare how it enforces or reports branch-routing requirements. The standard does not prescribe a host, checker, merge queue, or protection configuration.

## Self-certification

Identify the stable and integration branch names, branch and PR routes, release and hotfix scopes, merge methods, and reconciliation practice. Explain how agents check current remote refs and hosting rules, how fixes reach every affected line, and how drift is discovered. Separate mechanically checked facts from semantic judgments about release scope and continuing development. If implementation is partial, certify only the routes that work and describe the remaining gap.

## Subscription and continuing certification

Record `gitflow`, its source repository, full immutable definition commit, definition path, and repository-owned certification reference in `.agents/contracts/operating-standards.json`. Certification ordinarily lives in `.agents/contracts/standards-certification.md`. The subscription creates no standard implementation automatically. Maintain the certification when branch policy or release routes change. Existing pins remain authoritative until an explicit upgrade.

## Optional AOM assets

AOM may provide workflow guidance or checker examples separately. A repository may use, adapt, replace, or omit them. No specific runbook, playbook, branch naming prefix, CI provider, script, subscription scaffold, or remote branch configuration is required by this pledge.
