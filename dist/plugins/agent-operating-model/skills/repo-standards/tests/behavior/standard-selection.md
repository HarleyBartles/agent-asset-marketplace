# Standard selection behavior cases

Use these cases to assess whether guidance preserves independent standard selection. Evaluate the decisions, not exact wording.

## Case A: one lifecycle guide

A tiny repository wants a release-stage runbook only. It has no playbooks, doctrine store, or ambient workflow plugin. Explain adoption requirements.

## Case B: ambient refresh

Installed AOM changed today. This repository's certification pins an older commit. Assess whether an upgrade is mandatory or produces a warning.

## Case C: inline review guidance

A repository has a root `REVIEW.md` with its review guide inline. Assess whether it must create review books or another guidance store.

## Case D: Gitflow without product versioning

A repository explicitly wants release stabilization and concurrent release lines, but does not publish a SemVer-versioned product. It requests Gitflow only. Decide what branch obligations apply and whether the subscription requires a product version, `dev.N`, or SemVer.

## Case E: SemVer without an integration branch

A command-line product publishes a documented public API and adopts SemVer while keeping trunk-based development. It has four manually maintained product version copies that currently agree and an independently versioned schema and dependency. Decide which obligations apply and whether Gitflow cadence or copied version values establish compliance.

## Case F: both standards and version transitions

A repository adopts both standards. Integration is `0.3.0-dev.4` when a verified `0.2.1` hotfix returns. State the identity after reconciliation, the next integration merge's identity, and the result when release reconciliation instead leaves integration at stable `0.2.0` with no continuing development.
