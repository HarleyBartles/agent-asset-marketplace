# MARK-86 Adventures Installed Skill Reconciliation

This note reconciles the clean repo-backed Adventures v1.1 projection against
the installed-style Adventures skill names surfaced in the current doctrine and
routing surfaces.

## Repo-backed active basis

The clean Adventures bundle stays anchored to the v1.1 projection in
`codex-marketplace/plugins/adventures-pack/`.

Active repo-backed Adventures skills:

- `adventures-project-doctrine-v1.1`
- `adventures-bootstrap-v1.1`
- `adventures-github-operations-v1.1`
- `adventures-visual-preproduction-v1.1`
- `adventures-storyboard-preflight-v1.1`
- `adventures-visual-bible-creator-v1.1`
- `adventures-visual-bible-interpreter-v1.1`
- `adventures-image-qa-v1.1`
- `adventures-asset-sheet-compiler-v1.1`
- `adventures-frame-buster-v1.1`

Shared dependency skills projected with the pack:

- `don-logan-boundary-v1`
- `gpt-base-doctrine-v1`
- `worker-dispatch-linear-v1`
- `connector-safety-v1`
- `linear-v1`
- `tps-reporting-v1`
- `tps-ingress-v1`

## Installed-style residue observed in repo-held doctrine

The following names are visible in repo-held routing or reference surfaces, but
they are not part of the clean active v1.1 bundle above:

| Name | Repo-backed match | Decision | Follow-up slice |
| --- | --- | --- | --- |
| `adventures-reporting-hygiene` | no clean v1.1 projection match | keep as installed-only residue until a dedicated repo-backed surface exists | either collapse into the current reporting/proof lanes or mint a separate reporting-hygiene source issue |
| `adventures-github-issue-management` | no clean v1.1 projection match | keep as installed-only residue until a dedicated repo-backed surface exists | either map it into `adventures-github-operations-v1.1` or spin a separate issue-management slice |
| `adventures-visual-intent-gate` | no clean v1.1 projection match | keep as a locked gate alias, not a bundle component | capture in a follow-up if it remains an installed skill rather than a routing-only name |
| `adventures-image-preflight` | no clean v1.1 projection match | keep as a readiness alias, not a bundle component | add a dedicated source slice if the installed surface still exists |
| `adventures-project-doctrine-v1` | historical alias of the clean project doctrine line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-bootstrap-v1` | historical alias of the clean bootstrap line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-github-operations-v1` | historical alias of the clean GitHub operations line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-visual-preproduction-v1` | historical alias of the clean visual-preproduction line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-storyboard-preflight-v1` | historical alias of the clean storyboard-preflight line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-visual-bible-creator-v1` | historical alias of the clean visual-bible creator line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-visual-bible-interpreter-v1` | historical alias of the clean visual-bible interpreter line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-image-qa-v1` | historical alias of the clean image QA line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-asset-sheet-compiler-v1` | historical alias of the clean asset-sheet compiler line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |
| `adventures-frame-buster-v1` | historical alias of the clean frame-buster line | do not project as active inventory | keep only as provenance/history while the `v1.1` source remains active |

## Installed-to-repo decision summary

- Keep the clean repo-backed Adventures v1.1 projection as the only active
  bundle inventory.
- Treat the installed-style names above as either historical aliases or
  capability/routing names until a separate issue vends a repo-backed source
  surface for them.
- Do not widen the clean bundle just to absorb residue. Future work should land
  as explicit follow-up slices for reporting hygiene, issue management, image
  readiness, or the locked gate surfaces only if those skills remain installed
  and need repo custody.

## Follow-up slices

1. Confirm whether `adventures-reporting-hygiene` and
   `adventures-github-issue-management` still exist in the installed GPT skill
   set, then decide whether each should be folded into
   `adventures-github-operations-v1.1` or vendored as a separate repo-backed
   source slice.
2. Confirm whether `adventures-visual-intent-gate` and `adventures-image-preflight`
   are live installed skills or routing-only names, then give each a durable
   home if they still need one.
3. If any `*-v1` alias remains installed, migrate that installed surface to the
   matching `*-v1.1` repo-backed source and leave the old alias historical only.

## Evidence basis

- `codex-marketplace/plugins/adventures-pack/README.md`
- `codex-marketplace/plugins/adventures-pack/references/bundle-manifest.json`
- `codex-marketplace/plugins/adventures-pack/references/source-map.md`
- `sources/house-skills/decisions.md`
- `sources/house-skills/decisions.json`
- `provenance/house-skills.md`
- `gpt-skills/house-skills/adventures-project-doctrine/v1/adventures-project-doctrine-v1/references/adventures-skill-routing.md`
