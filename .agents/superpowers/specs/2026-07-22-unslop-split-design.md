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
- Do not change `codex-marketplace/plugin-roots.json`; the `unslop-plus` plugin root stays active.
- Do not implement the design in this spec.

## Source custody

### `sources/first_party/skills/unslop-engine/`

First-party engine skill. The `SKILL.md` body is a clean-room operational rewrite for Codex/GPT use, citing `mshumer/unslop` as the upstream authority.

- `SKILL.md`
  - `name: unslop-engine`
  - `description`: "Use when you need to empirically detect repetitive AI output patterns in a domain and generate a reusable anti-slop profile."
  - `license: MIT`
  - `metadata`:
    - `source-id`: `unslop-engine`
    - `source-path`: `sources/first_party/skills/unslop-engine`
    - `provenance-name`: `Unslop Engine first-party skill`
    - `source-category`: `first_party`
    - `status`: `active`
    - `owner`: `Harley Bartles`
    - `use_when`: `["Use when generating a domain-specific anti-slop profile from samples or observed defaults."]`
    - `do_not_use_when`: `["Do not use when applying an existing anti-slop profile to a task."]`
    - `related_skills`: `["unslop-profiles"]`
  - Body (under 500 words): identify domain/text-or-visual, run `py -3 <skill>/scripts/unslop.py --domain "..." [--type visual --count N]`, review `unslop-output/analysis.md` and `unslop-output/skill.md`, return the generated profile and the dominant repeated patterns.
- `scripts/unslop.py` moved from `sources/first_party/skills/unslop-plus/scripts/unslop.py`.
- `scripts/validate_unslop_output.py` moved from `sources/first_party/skills/unslop-plus/scripts/validate_unslop_output.py`.
- `scripts/validate_package.py` moved from `sources/first_party/skills/unslop-plus/scripts/validate_package.py` and updated to check the `unslop-engine` source root, removing the obsolete upstream `unslop` plugin-name check and any references to missing files such as `references/output-contract.md`.
- `LICENSE.upstream` moved from `sources/first_party/skills/unslop-plus/LICENSE.upstream`.
- `references/upstream-provenance.md` moved from `sources/first_party/skills/unslop-plus/references/upstream-provenance.md`; update any internal references from `unslop-plus` to `unslop-engine`.
- `assets/authority/authority.yaml` and `assets/authority/CITATIONS.md` in the `skills-with-citation` lane per `source-grounded-authoring.md`. `authority.yaml` cites `mshumer/unslop` at commit `edcb62386d129c65e4395f0cfcc9168eb1ba2148` (README SHA-256 `5c5e317d341aa63d73f73ca0b50309ca712acaebf660c6057b4ee376736643bd`) and records `SKILL.md` and `references/upstream-provenance.md` as `first_party_synthesis`. `source-map.yaml` matches `authority.yaml`.
- `agents/openai.yaml`:
  ```yaml
  interface:
    display_name: Unslop Engine
    short_description: Use when generating a reusable anti-slop profile from observed defaults.
    default_prompt: Use $unslop-engine to analyze a domain for repetitive AI defaults and generate a reusable anti-slop profile.
  policy:
    allow_implicit_invocation: false
  ```

### `sources/first_party/skills/unslop-profiles/`

First-party read-when router skill with no external authority assets.

- `SKILL.md`
  - `name: unslop-profiles`
  - `description`: "Use when applying anti-slop guidance to writing, documentation, implementation plans, code review, worker returns, debugging, React work, UI design, API design, architecture, testing, security review, or repository cleanup."
  - `license: MIT`
  - `metadata`:
    - `source-id`: `unslop-profiles`
    - `source-path`: `sources/first_party/skills/unslop-profiles`
    - `provenance-name`: `Unslop Profiles first-party skill`
    - `source-category`: `first_party`
    - `status`: `active`
    - `owner`: `Harley Bartles`
    - `use_when`: one bullet per profile trigger (writing, technical-writing, implementation-plans, code-review, worker-returns, debugging, frontend-react, frontend-ui, api-design, architecture, testing, security-review, cleanup-custody).
    - `do_not_use_when`: `["Do not use when generating a new domain-specific profile."]`
    - `related_skills`: `["unslop-engine"]`
  - Body (under 500 words): a routing table mapping each trigger to the exact `profiles/<name>.md` file. First line: "Do not apply a profile from memory. Read the listed file for the current task, then apply its avoid/prefer rules."
- `profiles/` directory containing the thirteen existing profile files moved from `sources/first_party/skills/unslop-plus/profiles/` (filenames unchanged).
- `agents/openai.yaml`:
  ```yaml
  interface:
    display_name: Unslop Profiles
    short_description: Use when applying the right anti-slop profile to a software development workflow.
    default_prompt: Use $unslop-profiles to apply the right anti-slop profile for the current task.
  policy:
    allow_implicit_invocation: true
  ```

### `sources/first_party/skills/unslop-plus/`

Retired. After `unslop.py`, the profiles, provenance files, `LICENSE.upstream`, and `agents/openai.yaml` are migrated to the two new skill roots, delete this directory.

## Pack and registry changes

### `codex-marketplace/custody-pack-registry.json`

1. **Remove** the top-level `unslop` mega-pack mapping (`source_family: unslop`, `mega_pack: unslop-plus`, `is_mega_pack: true`). Mega-packs are being deprecated for this work.
2. **Add a new projection-lane pack node** for `unslop-plus`:
   ```json
   {
     "bundle_name": "unslop-plus",
     "plugin_root": "codex-marketplace/plugins/unslop-plus",
     "bundle_version": "1.0.0",
     "bundle_type": "projection-lane",
     "category": "Productivity",
     "is_mega_pack": false,
     "notes": [
       "Unslop+ is a first-party projection-lane bundle containing the unslop engine skill and the anti-slop profile router skill.",
       "The bundle replaces the previous unslop mega-pack and keeps the engine separate from the profile router."
     ],
     "source_ledger": [
       "sources/first_party/skills/unslop-engine",
       "sources/first_party/skills/unslop-profiles"
     ],
     "provenance_refs": [
       "provenance/unslop.md",
       "codex-marketplace/plugins/unslop-plus/references/source-map.md"
     ],
     "generated_doc_surfaces": [
       "README.md",
       "SOURCE.md"
     ],
     "entries": [
       {
         "canonical_name": "unslop-engine",
         "source_category": "first_party",
         "content_mode": "verbatim",
         "source_family": "first_party",
         "canonical_source_path": "sources/first_party/skills/unslop-engine",
         "local_path": "skills/unslop-engine",
         "provenance_note": "Projected verbatim from the first-party unslop-engine skill.",
         "copy_expectation": "byte_identical"
       },
       {
         "canonical_name": "unslop-profiles",
         "source_category": "first_party",
         "content_mode": "verbatim",
         "source_family": "first_party",
         "canonical_source_path": "sources/first_party/skills/unslop-profiles",
         "local_path": "skills/unslop-profiles",
         "provenance_note": "Projected verbatim from the first-party unslop-profiles skill.",
         "copy_expectation": "byte_identical"
       }
     ]
   }
   ```
3. **Update `repo-worker-pack`**:
   - Replace the `unslop-plus` entry with `unslop-profiles` (same field values as the `unslop-plus` pack node `unslop-profiles` entry above, with `local_path: skills/unslop-profiles`).
   - Remove `sources/first_party/skills/unslop-plus` from `source_ledger` and add `sources/first_party/skills/unslop-profiles`.

### `codex-marketplace/plugins/unslop-plus/`

- `.codex-plugin/plugin.json`:
  - `description`: update to reference the engine and profile router.
  - `interface.shortDescription`: "Anti-slop engine and profile router for software development workflows."
  - `interface.longDescription`: update to mention `$unslop-engine` for generating profiles and `$unslop-profiles` for applying existing profiles.
  - `interface.defaultPrompt`: `["Use $unslop-profiles to apply the right anti-slop profile for the current workflow, or $unslop-engine to generate a new domain-specific profile."]`
  - `keywords`: add `unslop-engine` and `unslop-profiles` if appropriate.
- `README.md`: keep the existing prose, and add generated documentation markers around the bundle contents list:
  ```markdown
  ## What's Included
  <!-- BEGIN GENERATED: bundle-contents -->
  <!-- END GENERATED: bundle-contents -->
  ```
- `SOURCE.md`: keep the existing provenance prose, and add generated documentation markers around the inventory:
  ```markdown
  ## Source custody
  <!-- BEGIN GENERATED: pack-inventory -->
  <!-- END GENERATED: pack-inventory -->
  ```
- `references/bundle-manifest.json`, `references/source-map.md`, and `references/provenance-map.json`: regenerated by `tools/rebuild_marketplace.py`.
- `skills/unslop-engine/` and `skills/unslop-profiles/`: regenerated projections.

### Other generated surfaces

- `codex-marketplace/plugins/house-skills/` regenerated from `sources/first_party/skills/`; it will include both new skills and no longer include `unslop-plus`.
- `codex-marketplace/plugins/repo-worker-pack/` regenerated to include `unslop-profiles` and not `unslop-plus`.
- `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` regenerated by `generate_marketplace.py`.
- `generated/skill-zips/unslop-engine.zip` and `generated/skill-zips/unslop-profiles.zip` regenerated; delete stale `generated/skill-zips/unslop-plus.zip`.
- `repo-index/repo-index.json` regenerated by `generate_repo_index.py`.
- `docs/custody-and-projection-doctrine.md`: change "Six maintained mega-packs" to "Five maintained mega-packs" and remove the `unslop-plus` bullet.
- `provenance/unslop.md`: update plugin path references from `codex-marketplace/plugins/unslop/` to `codex-marketplace/plugins/unslop-plus/` and source references to the new `unslop-engine`/`unslop-profiles` roots.

## Validation

- `py -3 tools/rebuild_marketplace.py`
- `py -3 tools/check_marketplace.py`
- `py -3 tools/validate_marketplace.py --skip-freshness-checks`
- `py -3 tools/install_agent_skills.py --check` to confirm default-installed skills reflect `unslop-profiles`.
- Manual checks:
  - `codex-marketplace/plugins/unslop-plus/skills/` contains `unslop-engine/` and `unslop-profiles/`.
  - `codex-marketplace/plugins/repo-worker-pack/skills/` contains `unslop-profiles/` but not `unslop-engine/`.
  - `codex-marketplace/plugins/house-skills/skills/` contains both.
  - `unslop-profiles/SKILL.md` explicitly tells the agent to read `profiles/<name>.md` for each trigger.
  - No `unslop-plus.zip` remains in `generated/skill-zips/`.
  - No `sources/first_party/skills/unslop-plus/` directory remains.

## Handoff notes

Confidence: **9/10**. The custody split, registry node contract, plugin metadata, generated-document markers, and validation steps are now explicit. The only remaining runtime detail is the exact wording of `validate_package.py` updates, which can be finalized during implementation.
