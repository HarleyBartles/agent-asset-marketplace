# Custody and Marketplace Doctrine

This document defines source custody, product composition, and generated package boundaries.

## Source custody

- `skills/<skill-id>/` is the canonical source for each installable skill. Source identity and provenance do not depend on which plugin includes it.
- `shared/` owns reusable references, templates, and assets. Definitions name each resource and its destination inside a packaged skill.
- `src/plugin-definitions/<plugin>/plugin.json` owns Codex plugin metadata. `contents.json` declares skill membership, shared resources, and per-inclusion provenance.
- All marketplace skills are first-party maintained source, including adaptations of open-source material. Record attribution, upstream revision or URL, adaptation, and license obligations accurately. Do not create a separate third-party source pool or describe an adaptation as unmodified upstream source.
- `dist/plugins/` contains generated, self-contained installable plugin packages. Never edit shipped output to change source behavior.
- `src/marketplace/` owns reusable definition validation and build implementation. `tools/` owns command entry points and repository tooling.
- Skill tests remain beside source under `skills/<skill-id>/tests/` and ship with the skill except evaluator-only material and run results. Build tests live in `tests/build/`; installed product contracts live in `tests/shipping/`. Repository tests live in `tests/repository/`.
- `.agents/skills/` is reserved for skills authored and owned by the repository; no separate inventory declaration is required. This repository records selected AOM standard pins in `.agents/contracts/operating-standards.json` and its self-certifications in `.agents/contracts/standards-certification.md`. Each pin identifies the source repository, immutable commit, and definition path; subscribing does not require a deployed `.agents/standards/` copy.

## Composition and build

One skill may appear in multiple plugin definitions. Distinct source IDs may share an installed skill name when their authored behavior differs. A shared resource is copied into each declared skill at its package-relative destination; installed plugins resolve no path outside their own package.

Run `py -3 tools/run.py marketplace --apply` to build packages and regenerate the marketplace catalog. Run `py -3 tools/run.py marketplace --check` to detect missing, stale, or unexpected package output without writing. The build is deterministic and preserves independent sources under `src/packages/`.

`dist/` is the committed generated output root for assets distributed by this repository. It is not an editable source tree.

## Provenance and license

First-party describes current source custody and responsibility. It does not erase an upstream basis. Keep attribution and required notices with the canonical source and ensure every plugin that ships that material includes the required notice. Preserve upstream names, URLs or commit pins, license terms, and meaningful adaptation notes. Avoid claims of verbatim upstream copying when repository authors have adapted the work.

## Authoring workflow

1. Create or update canonical source under `skills/<skill-id>/` and shared materials under `shared/`.
2. Declare product membership and resource destinations in the relevant `src/plugin-definitions/<plugin>/contents.json` files.
3. Run the focused skill tests, build tests, or package tests owned by the changed behavior.
4. Run `py -3 tools/run.py marketplace --apply` to build and regenerate marketplace metadata.
5. Run focused checks. The tracked hook runs the three repository-owned suites once on the final commit.

## Product metadata

`src/plugin-definitions/` and `dist/plugin-roots.json` describe installable products and inventory. The generated `dist/plugins/<plugin>/` tree is the published package surface. `references/bundle-manifest.json`, package summaries, marketplace manifests, and indexes are generated compatibility or discovery outputs; they are not composition authorities.
