# House Skills Source Map

This bundle projects the reviewed House Skills inventory into one repo-local marketplace surface.

Authoritative source references:

- `sources/house-skills/decisions.json`
- `sources/house-skills/decisions.md`
- `sources/house-skills/intake.json`
- `provenance/house-skills.md`

Registry edit flow:

- edit the human registry in `sources/house-skills/decisions.md`;
- keep `sources/house-skills/decisions.json` as the structured mirror;
- regenerate `.agents/plugins/marketplace.json` with `tools/generate_marketplace.py`;
- validate the registry with `tools/validate_marketplace.py`.

Bundle references:

- `.agents/plugins/marketplace.json`
- `plugins/house-skills/.codex-plugin/plugin.json`
- `plugins/house-skills/skills/house-skills/references/bundle-manifest.json`

Lane summary:

- Base and control plane: all reviewed imports from MARK-30 plus the shared connector-safety v1.1 import from WILL-276 in the base/control-plane lane.
- Adventures: all reviewed imports from MARK-30 in the Adventures lane.
- Rooms: all reviewed imports from MARK-30 in the Rooms lane, plus the MARK-23 `rooms-image-sidecars` import.

Component map:

| Lane | Canonical name | Component version | Installed source skill id | Source path | Import status |
| --- | --- | --- | --- | --- | --- |
| Base and control plane | don-logan-boundary | v1 | `don-logan-boundary-v1` | `gpt-skills/house-skills/don-logan-boundary/SKILL.md` | imported |
| Base and control plane | gpt-base-doctrine | v1.1 | `gpt-base-doctrine-v1.1` | `gpt-skills/house-skills/gpt-base-doctrine/SKILL.md` | imported |
| Base and control plane | work-mode-router | v1 | `work-mode-router-v1` | `gpt-skills/house-skills/work-mode-router/SKILL.md` | imported |
| Base and control plane | worker-dispatch-linear | v1 | `worker-dispatch-linear-v1` | `gpt-skills/house-skills/worker-dispatch-linear/SKILL.md` | imported |
| Base and control plane | linear | v1.1 | `linear-v1.1` | `gpt-skills/house-skills/linear/SKILL.md` | imported |
| Base and control plane | tps-reporting | v1 | `tps-reporting-v1` | `gpt-skills/house-skills/tps-reporting/SKILL.md` | imported |
| Base and control plane | tps-ingress | v1 | `tps-ingress-v1` | `gpt-skills/house-skills/tps-ingress/SKILL.md` | imported |
| Base and control plane | session-buster | v0.2 | `session-buster-v0.2` | `gpt-skills/house-skills/session-buster/SKILL.md` | imported |
| Base and control plane | session-buster-ingress | v0.2 | `session-buster-ingress-v0.2` | `gpt-skills/house-skills/session-buster-ingress/SKILL.md` | imported |
| Base and control plane | crew | v1 | `crew-v1` | `gpt-skills/house-skills/crew/SKILL.md` | imported |
| Base and control plane | crew-buster | v1 | `crew-buster-v1` | `gpt-skills/house-skills/crew-buster/SKILL.md` | imported |
| Base and control plane | connector-safety | v1.1 | `connector-safety-v1.1` | `gpt-skills/house-skills/connector-safety/SKILL.md` | imported |
| Adventures | adventures-bootstrap | v1.1 | `adventures-bootstrap-v1.1` | `gpt-skills/house-skills/adventures-bootstrap/SKILL.md` | imported |
| Adventures | adventures-github-operations | v1.1 | `adventures-github-operations-v1.1` | `gpt-skills/house-skills/adventures-github-operations/SKILL.md` | imported |
| Adventures | adventures-visual-preproduction | v1.1 | `adventures-visual-preproduction-v1.1` | `gpt-skills/house-skills/adventures-visual-preproduction/SKILL.md` | imported |
| Adventures | adventures-storyboard-preflight | v1.1 | `adventures-storyboard-preflight-v1.1` | `gpt-skills/house-skills/adventures-storyboard-preflight/SKILL.md` | imported |
| Adventures | adventures-visual-bible-creator | v1.1 | `adventures-visual-bible-creator-v1.1` | `gpt-skills/house-skills/adventures-visual-bible-creator/SKILL.md` | imported |
| Adventures | adventures-visual-bible-interpreter | v1.1 | `adventures-visual-bible-interpreter-v1.1` | `gpt-skills/house-skills/adventures-visual-bible-interpreter/SKILL.md` | imported |
| Adventures | adventures-image-qa | v1.1 | `adventures-image-qa-v1.1` | `gpt-skills/house-skills/adventures-image-qa/SKILL.md` | imported |
| Adventures | adventures-asset-sheet-compiler | v1.1 | `adventures-asset-sheet-compiler-v1.1` | `gpt-skills/house-skills/adventures-asset-sheet-compiler/SKILL.md` | imported |
| Adventures | adventures-frame-buster | v1.1 | `adventures-frame-buster-v1.1` | `gpt-skills/house-skills/adventures-frame-buster/SKILL.md` | imported |
| Rooms | rooms-project-doctrine | v1 | `rooms-project-doctrine-v1` | `gpt-skills/house-skills/rooms-project-doctrine/SKILL.md` | imported |
| Rooms | rooms-image-sidecars | v0.1 | `rooms-image-sidecars-v0.1` | `gpt-skills/house-skills/rooms-image-sidecars/SKILL.md` | imported |
| Rooms | rooms-bootstrap | v1 | `rooms-bootstrap-v1` | `gpt-skills/house-skills/rooms-bootstrap/SKILL.md` | imported |
| Rooms | rooms-source-partitioning | v1 | `rooms-source-partitioning-v1` | `gpt-skills/house-skills/rooms-source-partitioning/SKILL.md` | imported |
| Rooms | rooms-ambiguity-buster | v1 | `rooms-ambiguity-buster-v1` | `gpt-skills/house-skills/rooms-ambiguity-buster/SKILL.md` | imported |
| Rooms | rooms-analogy-buster | v1 | `rooms-analogy-buster-v1` | `gpt-skills/house-skills/rooms-analogy-buster/SKILL.md` | imported |
| Rooms | rooms-zoom-outs-buster | v1 | `rooms-zoom-outs-buster-v1` | `gpt-skills/house-skills/rooms-zoom-outs-buster/SKILL.md` | imported |
| Rooms | rooms-character-investigation | v1 | `rooms-character-investigation-v1` | `gpt-skills/house-skills/rooms-character-investigation/SKILL.md` | imported |
| Rooms | rooms-sheet-creator | v1 | `rooms-sheet-creator-v1` | `gpt-skills/house-skills/rooms-sheet-creator/SKILL.md` | imported |

The bundle version is separate from the component versions. The component versions stay recorded in the source ledger and SKILL.md frontmatter metadata.
