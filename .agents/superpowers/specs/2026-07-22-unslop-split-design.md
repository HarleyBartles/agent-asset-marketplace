# Split `unslop-plus` into `unslop-engine` and `unslop-profiles`

## Problem

The current `sources/first_party/skills/unslop-plus/SKILL.md` lists the thirteen anti-slop profiles but does **not** tell an agent to read the actual `profiles/<name>.md` files. The body says "Read the profile's purpose..." without a path, so the profile content is never loaded. The description also enumerates all profiles, which is a workflow summary, not a trigger list, and violates the repo's skill-discovery rule that descriptions should state *when* to use the skill.

In addition, the skill conflates two jobs:
- running the Unslop engine to generate new domain-specific profiles, and
- routing an agent to an existing profile and applying it.

## Goals

- Retire `unslop-plus` as a **skill**; keep `unslop-plus` as a **plugin** name.
- Create `sources/first_party/skills/unslop-engine/`, a first-party re-implementation of the engine skill.
- Create `sources/first_party/skills/unslop-profiles/`, a first-party read-when router skill.
- Put both skills in the `unslop-plus` plugin and in `house-skills`.
- Put `unslop-profiles` in `repo-worker-pack` so it is installed by default.
- Keep `sources/third_party/unslop/upstream/` untouched for provenance; do not project the upstream `skills/unslop/` skill.
- Update `codex-marketplace/custody-pack-registry.json` and generated marketplace surfaces to reflect the new shape.

## Non-goals

- Do not rewrite the `unslop.py` algorithm; move the existing adapted script.
- Do not change the text of the thirteen profile files.
- Do not add new profiles.
- Do not edit `sources/third_party/unslop/upstream/`.
- Do not implement the design in this spec.

## Source custody

### `sources/first_party/skills/unslop-engine/`

First-party engine skill. It is a clean-room operational rewrite for Codex/GPT use, citing `mshumer/unslop` as the upstream authority.

- `SKILL.md`
  - `name: unslop-engine`
  - `description`: "Use when you need to empirically detect repetitive AI output patterns in a domain and generate a reusable anti-slop profile."
  - `metadata.use_when`: `[Use when generating a domain-specific anti-slop profile from samples or observed defaults.]`
  - `metadata.do_not_use_when`: `[Do not use when applying an existing anti-slop profile to a task; use $unslop-profiles instead.]`
  - Body: identify domain/type, run `py -3 <skill>/scripts/unslop.py --domain "..."`, review `unslop-output/analysis.md` and `unslop-output/skill.md`, return the generated profile and main repeated patterns.
- `scripts/unslop.py` moved from `sources/first_party/skills/unslop-plus/scripts/unslop.py`.
- `scripts/validate_unslop_output.py` and `scripts/validate_package.py` moved if still useful.
- `LICENSE.upstream` moved from `sources/first_party/skills/unslop-plus/LICENSE.upstream`.
- `references/upstream-provenance.md` moved from `sources/first_party/skills/unslop-plus/references/upstream-provenance.md`.
- `assets/authority/authority.yaml` and `assets/authority/CITATIONS.md` per `source-grounded-authoring.md`, citing `mshumer/unslop` and the adaptation.
- `agents/openai.yaml` with `default_prompt: "Use $unslop-engine to analyze a domain for repetitive AI defaults and generate a reusable anti-slop profile."` and `allow_implicit_invocation: false`.

### `sources/first_party/skills/unslop-profiles/`

First-party read-when router skill.

- `SKILL.md`
  - `name: unslop-profiles`
  - `description`: "Use when applying anti-slop guidance to writing, documentation, implementation plans, code review, worker returns, debugging, React work, UI design, API design, architecture, testing, security review, or repository cleanup."
  - `metadata.use_when`: one bullet per profile trigger (writing, technical-writing, implementation-plans, code-review, worker-returns, debugging, frontend-react, frontend-ui, api-design, architecture, testing, security-review, cleanup-custody).
  - `metadata.do_not_use_when`: `[Do not use when generating a new domain-specific profile; use $unslop-engine instead.]`
  - Body: a routing table mapping each trigger to the exact `profiles/<name>.md` file, with the instruction "Read the file, then apply its avoid/prefer rules. Do not summarize the profile from memory."
- `profiles/` directory containing the thirteen existing profile files moved from `sources/first_party/skills/unslop-plus/profiles/`.
- `agents/openai.yaml` with `default_prompt: "Use $unslop-profiles to apply the right anti-slop profile for the current task."` and `allow_implicit_invocation: true`.

### `sources/first_party/skills/unslop-plus/`

Retired. After `unslop.py`, the profiles, provenance files, and `agents/openai.yaml` are migrated to the two new skill roots, remove this directory.

## Pack and registry changes

### `codex-marketplace/custody-pack-registry.json`

1. Remove or retire the top-level `unslop` mega-pack mapping (`is_mega_pack: true`, `mega_pack: unslop-plus`). Mega-packs are being deprecated as a concept for this work.
2. Add a new projection-lane pack node:
   - `bundle_name: "unslop-plus"`
   - `plugin_root: "codex-marketplace/plugins/unslop-plus"`
   - `bundle_type: "projection-lane"`
   - `is_mega_pack: false`
   - `category: "Productivity"`
   - `entries`:
     - `unslop-engine`: `source_category: first_party`, `content_mode: verbatim`, `source_family: first_party`, `canonical_source_path: sources/first_party/skills/unslop-engine`
     - `unslop-profiles`: `source_category: first_party`, `content_mode: verbatim`, `source_family: first_party`, `canonical_source_path: sources/first_party/skills/unslop-profiles`
   - `generated_doc_surfaces`: `["README.md", "SOURCE.md"]` after adding the generated-marker pairs to those files.
3. In `repo-worker-pack` entries, replace the existing `unslop-plus` entry with `unslop-profiles` (`source_category: first_party`, `content_mode: verbatim`, `source_family: first_party`). `unslop-engine` does **not** need to be in `repo-worker-pack`.

### `codex-marketplace/plugins/unslop-plus/`

- `.codex-plugin/plugin.json`: update `description`, `longDescription`, and `defaultPrompt` to reference `$unslop-engine` and `$unslop-profiles`.
- `README.md` and `SOURCE.md`: add generated documentation marker pairs so `generate_pack_manifests.py` can maintain them, then regenerate.
- `references/bundle-manifest.json`, `references/source-map.md`, and `references/provenance-map.json`: regenerated by `tools/rebuild_marketplace.py`.
- `skills/unslop-engine/` and `skills/unslop-profiles/`: regenerated projections.

### Other generated surfaces

- `codex-marketplace/plugins/house-skills/` regenerated from `sources/first_party/skills/`; it will include both new skills.
- `codex-marketplace/plugins/repo-worker-pack/` regenerated to include `unslop-profiles`.
- `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` regenerated by `generate_marketplace.py`.
- `generated/skill-zips/unslop-engine.zip` and `generated/skill-zips/unslop-profiles.zip` regenerated by `project_skills.py`.
- `repo-index/repo-index.json` regenerated by `generate_repo_index.py`.
- `docs/custody-and-projection-doctrine.md`: remove `unslop-plus` from the mega-pack list since it is now a projection-lane pack.

## Validation

- `py -3 tools/rebuild_marketplace.py`
- `py -3 tools/check_marketplace.py`
- `py -3 tools/validate_marketplace.py --skip-freshness-checks`
- Manual checks:
  - `codex-marketplace/plugins/unslop-plus/skills/` contains `unslop-engine/` and `unslop-profiles/`.
  - `codex-marketplace/plugins/repo-worker-pack/skills/` contains `unslop-profiles/` but not `unslop-engine/`.
  - `codex-marketplace/plugins/house-skills/skills/` contains both.
  - `unslop-profiles/SKILL.md` explicitly tells the agent to read `profiles/<name>.md` for each trigger.
- Verify `unslop-plus` skill no longer exists in `sources/first_party/skills/` or any projection.

## Handoff notes

Confidence: **9/10**. The file targets, custody split, and registry mechanics are clear. The only remaining detail is whether to add generated documentation markers to `unslop-plus/README.md` and `SOURCE.md` or leave them hand-maintained; the recommended approach is to add markers and include them in `generated_doc_surfaces`.
