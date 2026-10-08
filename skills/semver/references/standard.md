# SemVer Standard

**Standard ID:** `semver`

## Pledge

The repository communicates product compatibility through a declared public interface and semantically meaningful versions. Every independently versioned product has one authored version source; its build propagates and verifies all product identity copies before release.

## Required implementation

- Declare the product's current public API and compatibility policy precisely enough to classify changes under its current stability level. During `0.y.z`, that policy may explicitly allow breaking changes and does not promise API stability. Version changes communicate the current policy; a `MAJOR.MINOR.PATCH` shaped string by itself is not SemVer adoption.
- Follow SemVer 2.0.0 syntax and precedence for the product version: normal versions contain three nonnegative integer components without leading zeroes; prerelease identifiers follow the core version and have lower precedence than the corresponding stable release; build metadata does not change precedence. Apply the specification's major, minor, and patch meanings once the public API is stable; during `0.y.z`, state the repository's version-selection policy without claiming API stability.
- State the repository's current initial-development (`0.y.z`) compatibility and version policy. An adopter before `1.0.0` is not required to declare or promise the future stable API in advance. Define and publish the stable compatibility contract when preparing the first `1.0.0` release; do not claim readiness solely because time elapsed or a version string exists.
- For each independently versioned product, choose exactly one authored product-version source. A build step propagates it to every required package, lockfile root, manifest, runtime identity, archive, and artifact. Treat the other product-version values as derived outputs; do not hand-maintain multiple copies and hope they agree.
- Make the explicit build produce or repair derived identity outputs. Make check/validation reject missing, stale, malformed, conflicting, or unexpectedly independently authored product-version copies. Checks must not silently rewrite maintained files. Bind each released version to its verified immutable source and matching artifact identity; never change released contents under an existing identity.
- Keep independent version domains independent. Dependencies, data schemas, message or payload contracts, and separately released products have their own compatibility authorities where applicable; they are not duplicate copies of this product's version.
- Explain how compatibility decisions, version ownership, build propagation, release identity validation, and drift controls are maintained. Mechanical equality alone cannot certify semantic bump correctness or prove there is one authored source.

## Conditional obligations

- When the repository also adopts `gitflow`, each ordinary development merge into the integration branch establishes a unique `MAJOR.MINOR.PATCH-dev.N` checkpoint, and changed, qualified release candidates use `MAJOR.MINOR.PATCH-rc.N`. A release or hotfix reconciliation that leaves integration at the stable baseline keeps the stable version; reconciliation into continuing next-release work advances that line's checkpoint. Gitflow branch routing remains owned by the Gitflow standard.
- SemVer alone does not require Gitflow, `develop`, branch-triggered checkpoint numbers, an RC naming convention, a particular tagging convention, a hosted release, or a particular artifact format. A repository declares how it publishes each release.
- If the product has no published or otherwise declared public interface or compatibility expectation, determine whether SemVer has a useful subject before adopting it. Do not invent a public contract just to make the versioning label look complete.

## Joint Gitflow and SemVer checkpoint cadence

This section applies only when both `gitflow` and `semver` are subscribed.

- Assign one distinct `MAJOR.MINOR.PATCH-dev.N` identity to each ordinary integration merge, including documentation and tooling changes. Commits within an unmerged PR share one proposed checkpoint; the merge, not each commit, establishes the landmark. Begin a newly selected release line at positive `dev.1` and advance N monotonically for each subsequent integration merge on that line.
- Select the next release core from the current compatibility policy and intended release scope. Do not assume every post-release change increments only PATCH. If the intended release core changes, start its development checkpoint sequence at `dev.1`.
- Revalidate proposed checkpoint identity against the current integration head before merge. If another merge made it stale or duplicated, refresh the branch and assign the next unique identity. Preserve a repository's explicit merge strategy; a squash of one PR remains one integration landmark.
- A development checkpoint identifies a merged source/build state; it does not itself declare a stable release or require a tag or hosted publication.
- A qualified release candidate uses the selected core and `rc.1`. Advance to the next `rc.N` only when candidate source changes and is rebuilt and requalified. A verification rerun of identical source does not create a new candidate identity.
- Promote a verified candidate to the stable core version without the prerelease suffix. Build again from the exact stable release source and verify its derived identities. Stable source and artifact identity must agree.
- On release or hotfix reconciliation, set integration to the stable release version when it is left at that released baseline. Do not assign `-dev.1` merely because the merge-back occurred. The first subsequent integration merge that diverges from stable starts the next intended release at `dev.1`.
- If integration already contains continuing next-release work when an older release or hotfix returns, preserve that intended line and advance its N for the reconciliation change. For example, reconciling `0.2.1` into `0.3.0-dev.4` yields `0.3.0-dev.5`. Do not reset integration to the older stable identity or discard the future work.

## Self-certification

Identify each independently versioned product, its current compatibility policy (which may explicitly allow breaking changes during `0.y.z`), its single authored version source, the build that propagates the value, and the checks that reject stale or conflicting outputs. A future `1.0.0` contract is not required for pre-1.0 adoption; document the stable contract when preparing that release. Explain who decides bump meaning and how releases bind to verified source and artifacts. Where Gitflow is also adopted, describe checkpoint allocation, release candidates, stable promotion, and the two reconciliation states. Identify mechanical evidence and judgment-based limits separately; do not certify through equal strings or generated-file presence alone.

## Subscription and continuing certification

Record `semver`, its source repository, full immutable definition commit, definition path, and repository-owned certification reference in `.agents/contracts/operating-standards.json`. Certification ordinarily lives in `.agents/contracts/standards-certification.md`. A subscription does not introduce a versioning script, CI gate, or build convention automatically; the repository owns its implementation. Maintain certification as products, compatibility policies, version destinations, and release flows change. Existing pins remain authoritative until an explicit upgrade.

## Optional AOM assets

AOM may supply version parsing, comparison, or propagation examples as optional accelerators. Adopters choose, adapt, replace, or omit them. No programming language, filename, command bus, build system, release host, CI provider, tag spelling, artifact format, or shared runtime is required by this pledge.
