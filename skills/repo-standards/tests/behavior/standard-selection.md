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

A repository adopts both standards. It has stable `0.2.0`, then starts the selected `0.3.0` line. Explain that the first ordinary integration merge is `0.3.0-dev.1`, later merges advance one checkpoint each, and extra commits inside an unmerged PR do not advance the checkpoint. A verified `0.2.1` hotfix returning to `0.3.0-dev.4` makes integration `0.3.0-dev.5`; the next development merge is `dev.6`. Reconciling released `0.2.0` into that continuing line also advances it to `0.3.0-dev.5`, while reconciling a release or hotfix into an integration tree left at the stable baseline keeps the stable identity until the next development merge starts the newly selected line at `dev.1`. Cutting a release candidate at `0.3.0-rc.1` does not advance integration; changing and requalifying the candidate makes it `0.3.0-rc.2`, and stable promotion uses `0.3.0` after verification.
