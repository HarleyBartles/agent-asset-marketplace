# Standard selection evaluator notes

- Case A: useful release-stage guidance, honest certification, and effective root routing are required. No playbook, doctrine store, ambient plugin, fixed heading set, or starter inventory is required.
- Case B: the existing subscription remains governed by its pinned commit. Ambient refresh creates no upgrade obligation, latest-version alarm, or warning.
- Case C: inline review guidance in root `REVIEW.md` is valid. Review books, fan-out, and another guidance store are not required.
- Case D: subscribe to Gitflow only; implement branch roles, routes, promotion, and reconciliation. No application version, SemVer, `dev.N`, or `rc.N` is implied.
- Case E: SemVer permits trunk-based development and does not require `develop` or `dev.N`. Matching hand-maintained copies do not meet AOM's single-source requirement; one authored product version must propagate through a build to all product identities. Keep schema and dependency versions independent.
- Case F: apply the complete transition table in the SemVer standard. Each ordinary development merge advances one unique `dev.N`; commits inside an unmerged PR do not. Hotfix or release reconciliation into continuing development advances its existing line, including `0.3.0-dev.4` to `dev.5`, while reconciliation that leaves integration at a stable baseline keeps that stable identity until the next development merge starts the selected next line at `dev.1`. Cutting `rc.1` leaves integration unchanged; a changed and requalified candidate becomes `rc.2`; verified stable promotion uses the core version without prerelease. Do not require branch-triggered cadence from either standard alone.

Reject answers that treat a catalog entry, installed plugin, optional starter, or available tool as adoption by itself.
