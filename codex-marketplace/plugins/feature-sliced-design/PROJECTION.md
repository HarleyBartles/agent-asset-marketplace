# Projection

This root is the Codex-facing marketplace projection of the upstream
Feature-Sliced Design skill.

## Layer Model

This repository uses two distinct layers for this plugin:

- Source custody keeps the retained third-party snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only
  by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected skill is materialized from
  `sources/third_party/feature-sliced/upstream/skills/feature-sliced-design/`.

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the
  third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can
  be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install
  surfaces, not hand-edited sources.

## Projection contract

- `feature-sliced-design` is the third-party standalone plugin projection of the
  upstream FSD skill.
- Content is vendored verbatim from the pinned upstream commit.
- First-party selection decisions are recorded in the issue references (MARK-290).

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/feature-sliced-design/SKILL.md`
- `skills/feature-sliced-design/references/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream GitHub workflows, issue templates, and repository metadata remain in
  `sources/third_party/feature-sliced/upstream/` as support provenance.
