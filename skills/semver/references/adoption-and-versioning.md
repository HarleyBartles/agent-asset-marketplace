# SemVer Adoption and Versioning

## Confirm adoption and scope

Read `.agents/contracts/operating-standards.json` and its certification before applying SemVer as a repository obligation. A missing subscription means non-adoption unless the human requests assessment or adoption. Identify the versioned product and its public interface. Do not infer adoption from tags, package metadata, matching copies, or an installed skill.

For explicit adoption, inspect the current pin and preserve it while implementing an upgrade. Document the compatibility policy that applies to current versions. A repository below `1.0.0` is not required to declare or promise the future stable API as an adoption prerequisite. Identify the one authored product version and every generated product-version destination. Document the build that propagates it and the check that detects missing or stale outputs. Record the v2 pin and honest certification; leave certification incomplete until the semantic and mechanical obligations are implemented.

SemVer does not imply a branch workflow. A trunk-based repository can adopt SemVer without `develop` or merge-triggered development versions. Read the Gitflow standard only if Gitflow is independently adopted or explicitly requested for assessment.

## Choose a product version

Classify a proposed change against the declared public API and the policy for the product's current stability level. For a stable public API, an incompatible change advances MAJOR, a compatible API addition or deprecation advances MINOR, and a compatible bug fix advances PATCH. During `0.y.z`, SemVer makes no API stability promise; record the repository's current compatibility and version-selection policy without inventing a future stable guarantee. Follow SemVer 2.0.0 syntax and precedence, including resetting lower components when higher components increment and its prerelease precedence rules.

During `0.y.z` development, SemVer does not promise API stability and permits changes. The repository records its current policy for compatibility and version selection without inventing a future stable promise. When preparing the first `1.0.0` release, define and publish the public compatibility contract that will apply to that stable release; do not prescribe a calendar date as evidence of readiness.

## Maintain one product identity

Edit the single authoritative product version, then invoke the repository's explicit build/propagation command. Inspect the changed generated destinations. Run version identity validation to ensure every required copy is derived and matches. If validation finds a mismatch, report or repair it through the build step; check mode must not rewrite maintained outputs.

Keep independent version authorities separate. A database schema may need migration steps and its own compatibility version. A dependency retains its publisher's version. A product made of separately released components may declare one source per component.

## Prepare and identify a release

Verify the proposed version against the public compatibility decision. Build the exact proposed source and check propagated package, runtime, manifest, and artifact identities. A release tag may use a prefix such as `v`; document that spelling separately from the SemVer product value. Ensure the immutable release points at the verified source and do not move a published tag to identify changed contents.

When both Gitflow and SemVer are adopted, follow the joint `dev.N`, `rc.N`, stable promotion, and reconciliation cadence in the [SemVer standard](standard.md#joint-gitflow-and-semver-checkpoint-cadence) and branch routes in the [Gitflow guide](../../gitflow/references/adoption-and-workflow.md). A merge-back to an unchanged stable baseline remains stable until development diverges; a hotfix merged into an existing future development line advances that line's checkpoint.

## References

The [SemVer standard](standard.md) defines AOM obligations. Source attribution and derivation boundaries are in [the authority record](../assets/authority/CITATIONS.md). See [repository adoption and certification](../../repo-standards/references/adoption-and-certification.md) for the explicit subscription workflow.
