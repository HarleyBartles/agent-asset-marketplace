# Gitflow Adoption and Workflow

## Confirm adoption and fit

Read `.agents/contracts/operating-standards.json` and its certification before applying Gitflow as a repository obligation. A missing subscription means non-adoption unless the human asks for assessment or adoption. Check whether deliberate stabilization or concurrent supported release lines justify the added branch coordination. A continuously delivered product with no need for parallel release lines may choose a simpler workflow.

For an explicit adoption, read the exact requested definition and existing pin, then agree the local mapping for stable, integration, release, and hotfix branches. Record the immutable v2 pin and honest certification. Implement the route in the repository's own guidance and enforcement points; do not create remote branches or change hosting rules as an implied consequence of writing the subscription.

## Route work

| Work | Start from | Target | Purpose |
|---|---|---|---|
| Ordinary feature | Current integration branch | Integration branch | Integrate reviewed work |
| Release stabilization | Integration branch | Stable branch | Verify and promote a bounded release |
| Urgent production fix | Released stable state | Stable branch | Correct production without importing unrelated future work |
| Release or hotfix reconciliation | Promoted release/fix | Integration and affected active release lines | Carry fixes forward while preserving ongoing work |

Use the repository's declared branch names and feature prefixes. Refresh from remote refs before choosing a base. Check source and target commits, PR target, merge strategy, and the current hosted rules before publishing or relying on enforcement.

## Reconcile version and source state

After promotion, compare integration with the verified released source and the intended next-release work. If integration is left at the stable baseline, its identity is the stable version. The first later development merge starts the next intended release's `dev.1` only when both Gitflow and SemVer are adopted.

If integration already contains the next release's development identity, preserve that line while incorporating a fix. For example, when `0.3.0-dev.4` exists and a `0.2.1` hotfix returns to integration, advance the integration checkpoint to `0.3.0-dev.5`; do not reset it to `0.2.1`. Refresh competing PRs from the new integration head and allocate a unique checkpoint to each resulting merge. Rebuild derived version identities and run the route's applicable validation before claiming the merge-back is ready.

## Joint release cadence

When both standards are adopted, use `MAJOR.MINOR.PATCH-dev.N` as a SemVer prerelease identity for each merged development landmark and `MAJOR.MINOR.PATCH-rc.N` for each changed, qualified release candidate. The SemVer standard owns syntax, precedence, and version-source/build requirements. This guide owns when branch transitions create or reset those identities. SemVer adoption alone does not require Gitflow, `develop`, or this merge-triggered cadence.

## References

The [Gitflow standard](standard.md) owns AOM obligations. Source attribution and derivation boundaries are in [the authority record](../assets/authority/CITATIONS.md). See [repository adoption and certification](../../repo-standards/references/adoption-and-certification.md) for the explicit subscription workflow.
