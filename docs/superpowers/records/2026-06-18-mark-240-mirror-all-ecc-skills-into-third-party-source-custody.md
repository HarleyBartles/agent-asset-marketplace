# MARK-240 Mirror All ECC Skills Into Third-Party Source Custody

Issue: MARK-240
Branch: `harleydbartles/mark-240-drain-selected-ecc-skills-into-third-party-source-custody`

## Outcome

Mirrored the full upstream ECC skill tree into third-party source custody at
`sources/third_party/ecc/upstream/skills/` from pinned commit
`ceca28852e5b31edbbf66ebccc8fd163dd14208e`.

The mirror covers all `271` upstream skill directories with `0` skips.

## Changed surfaces

- Added the full third-party skill mirror under
  `sources/third_party/ecc/upstream/skills/`.
- Added the machine-readable custody manifest at
  `sources/third_party/ecc/upstream/manifest.json`.
- Updated `sources/third_party/ecc/upstream/source-custody.md` with the full
  mirror note and manifest pointer.
- Updated `sources/third_party/README.md` to describe the full ECC source
  custody root.
- Added the lightweight plans-folder guidance file at
  `docs/superpowers/plans/AGENTS.md` and wired it into `repo-index/repo-index.json`.
- Added the MARK-240 implementation plan at
  `docs/superpowers/plans/2026-06-18-mark-240-mirror-all-ecc-skills-into-third-party-source-custody.md`.

## Generated artifacts

- No marketplace projection artifacts were created.
- No wrappers were created.
- No generated zips were created.
- The manifest was generated from the committed MARK-238 custody record and the
  pinned upstream ECC checkout.

## Verbatim proof

- Pinned upstream checkout: `.tmp/ecc-upstream` at
  `ceca28852e5b31edbbf66ebccc8fd163dd14208e`.
- Verification method: byte-for-byte recursive comparison of every file in each
  mirrored skill directory against the pinned upstream checkout.
- Result: `verbatim=ok` for all `271` skill directories.

## Validation

- `py -3 tools/validate_marketplace.py` - passed.
- `py -3 tools/validate_repo_index.py` - passed.
- `git diff --check` - passed with only line-ending warnings from Git.

## Notes

- The temporary upstream checkout under `.tmp/ecc-upstream` was removed after
  verification.
- The branch remains unpublished until the required commit, push, and draft PR
  steps are completed.
