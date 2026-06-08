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

- Base and control plane: all reviewed imports from MARK-19, MARK-20, MARK-21, and MARK-30 in the base/control-plane lane.
- Adventures v1.1: all reviewed imports from MARK-65 in the Adventures lane.
- Rooms: all reviewed imports from MARK-23 and MARK-30 in the Rooms lane.

Component map:

| Lane | Canonical name | Component version | Installed source skill id | Source path | Import status |
| --- | --- | --- | --- | --- | --- |
| Base and control plane | don-logan-boundary | v1 | `don-logan-boundary-v1` | `gpt-skills/house-skills/don-logan-boundary/v1/don-logan-boundary-v1/SKILL.md` | imported |
| Base and control plane | gpt-base-doctrine | v1 | `gpt-base-doctrine-v1` | `gpt-skills/house-skills/gpt-base-doctrine/v1/gpt-base-doctrine-v1/SKILL.md` | imported |
| Base and control plane | work-mode-router | v1 | `work-mode-router-v1` | `gpt-skills/house-skills/work-mode-router/v1/work-mode-router-v1/SKILL.md` | imported |
| Base and control plane | worker-dispatch-linear | v1 | `worker-dispatch-linear-v1` | `gpt-skills/house-skills/worker-dispatch-linear/v1/worker-dispatch-linear-v1/SKILL.md` | imported |
| Base and control plane | linear | v1 | `linear-v1` | `gpt-skills/house-skills/linear/v1/linear-v1/SKILL.md` | imported |
| Base and control plane | tps-reporting | v1 | `tps-reporting-v1` | `gpt-skills/house-skills/tps-reporting/v1/tps-reporting-v1/SKILL.md` | imported |
| Base and control plane | tps-ingress | v1 | `tps-ingress-v1` | `gpt-skills/house-skills/tps-ingress/v1/tps-ingress-v1/SKILL.md` | imported |
| Base and control plane | session-buster | v0.1 | `session-buster-v0.1` | `gpt-skills/house-skills/session-buster/v0.1/session-buster-v0.1/SKILL.md` | imported |
| Base and control plane | session-buster-ingress | v0.1 | `session-buster-ingress-v0.1` | `gpt-skills/house-skills/session-buster-ingress/v0.1/session-buster-ingress-v0.1/SKILL.md` | imported |
| Base and control plane | crew | v1 | `crew-v1` | `gpt-skills/house-skills/crew/v1/crew-v1/SKILL.md` | imported |
| Base and control plane | buster-framework | v1 | `buster-framework-v1` | `gpt-skills/house-skills/buster-framework/v1/buster-framework-v1/SKILL.md` | imported |
| Base and control plane | ambiguity-buster | v1 | `ambiguity-buster-v1` | `gpt-skills/house-skills/ambiguity-buster/v1/ambiguity-buster-v1/SKILL.md` | imported |
| Base and control plane | boring-buster | v1 | `boring-buster-v1` | `gpt-skills/house-skills/boring-buster/v1/boring-buster-v1/SKILL.md` | imported |
| Base and control plane | invariant-buster | v1 | `invariant-buster-v1` | `gpt-skills/house-skills/invariant-buster/v1/invariant-buster-v1/SKILL.md` | imported |
| Base and control plane | analogy-buster | v1 | `analogy-buster-v1` | `gpt-skills/house-skills/analogy-buster/v1/analogy-buster-v1/SKILL.md` | imported |
| Base and control plane | canon-buster | v1 | `canon-buster-v1` | `gpt-skills/house-skills/canon-buster/v1/canon-buster-v1/SKILL.md` | imported |
| Base and control plane | cleanup-custody | v0.1 | `cleanup-custody-v0.1` | `gpt-skills/house-skills/cleanup-custody/v0.1/cleanup-custody-v0.1/SKILL.md` | imported |
| Base and control plane | skill-validator | v1 | `skill-validator-v1` | `gpt-skills/house-skills/skill-validator/v1/skill-validator-v1/SKILL.md` | imported |
| Base and control plane | skill-packager | v1 | `skill-packager-v1` | `gpt-skills/house-skills/skill-packager/v1/skill-packager-v1/SKILL.md` | imported |
| Base and control plane | skill-buster | v0.1 | `skill-buster-v0.1` | `gpt-skills/house-skills/skill-buster/v0.1/skill-buster-v0.1/SKILL.md` | imported |
| Rooms | rooms-image-sidecars | v0.1 | `rooms-image-sidecars-v0.1` | `gpt-skills/house-skills/rooms-image-sidecars/v0.1/rooms-image-sidecars-v0.1/SKILL.md` | imported |
| Base and control plane | crew-buster | v1 | `crew-buster-v1` | `gpt-skills/house-skills/crew-buster/v1/crew-buster-v1/SKILL.md` | imported |
| Adventures v1.1 | adventures-project-doctrine | v1.1 | `adventures-project-doctrine-v1.1` | `gpt-skills/house-skills/adventures-project-doctrine/v1.1/adventures-project-doctrine-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-bootstrap | v1.1 | `adventures-bootstrap-v1.1` | `gpt-skills/house-skills/adventures-bootstrap/v1.1/adventures-bootstrap-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-github-operations | v1.1 | `adventures-github-operations-v1.1` | `gpt-skills/house-skills/adventures-github-operations/v1.1/adventures-github-operations-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-visual-preproduction | v1.1 | `adventures-visual-preproduction-v1.1` | `gpt-skills/house-skills/adventures-visual-preproduction/v1.1/adventures-visual-preproduction-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-storyboard-preflight | v1.1 | `adventures-storyboard-preflight-v1.1` | `gpt-skills/house-skills/adventures-storyboard-preflight/v1.1/adventures-storyboard-preflight-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-visual-bible-creator | v1.1 | `adventures-visual-bible-creator-v1.1` | `gpt-skills/house-skills/adventures-visual-bible-creator/v1.1/adventures-visual-bible-creator-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-visual-bible-interpreter | v1.1 | `adventures-visual-bible-interpreter-v1.1` | `gpt-skills/house-skills/adventures-visual-bible-interpreter/v1.1/adventures-visual-bible-interpreter-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-image-qa | v1.1 | `adventures-image-qa-v1.1` | `gpt-skills/house-skills/adventures-image-qa/v1.1/adventures-image-qa-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-asset-sheet-compiler | v1.1 | `adventures-asset-sheet-compiler-v1.1` | `gpt-skills/house-skills/adventures-asset-sheet-compiler/v1.1/adventures-asset-sheet-compiler-v1.1/SKILL.md` | imported |
| Adventures v1.1 | adventures-frame-buster | v1.1 | `adventures-frame-buster-v1.1` | `gpt-skills/house-skills/adventures-frame-buster/v1.1/adventures-frame-buster-v1.1/SKILL.md` | imported |
| Rooms | rooms-project-doctrine | v1 | `rooms-project-doctrine-v1` | `gpt-skills/house-skills/rooms-project-doctrine/v1/rooms-project-doctrine-v1/SKILL.md` | imported |
| Rooms | rooms-bootstrap | v1 | `rooms-bootstrap-v1` | `gpt-skills/house-skills/rooms-bootstrap/v1/rooms-bootstrap-v1/SKILL.md` | imported |
| Rooms | rooms-source-partitioning | v1 | `rooms-source-partitioning-v1` | `gpt-skills/house-skills/rooms-source-partitioning/v1/rooms-source-partitioning-v1/SKILL.md` | imported |
| Rooms | rooms-ambiguity-buster | v1 | `rooms-ambiguity-buster-v1` | `gpt-skills/house-skills/rooms-ambiguity-buster/v1/rooms-ambiguity-buster-v1/SKILL.md` | imported |
| Rooms | rooms-analogy-buster | v1 | `rooms-analogy-buster-v1` | `gpt-skills/house-skills/rooms-analogy-buster/v1/rooms-analogy-buster-v1/SKILL.md` | imported |
| Rooms | rooms-zoom-outs-buster | v1 | `rooms-zoom-outs-buster-v1` | `gpt-skills/house-skills/rooms-zoom-outs-buster/v1/rooms-zoom-outs-buster-v1/SKILL.md` | imported |
| Rooms | rooms-character-investigation | v1 | `rooms-character-investigation-v1` | `gpt-skills/house-skills/rooms-character-investigation/v1/rooms-character-investigation-v1/SKILL.md` | imported |
| Rooms | rooms-sheet-creator | v1 | `rooms-sheet-creator-v1` | `gpt-skills/house-skills/rooms-sheet-creator/v1/rooms-sheet-creator-v1/SKILL.md` | imported |

The bundle version is separate from the component versions. The component versions stay encoded in the reviewed source skill names and source records.
