# Superpowers+ Becomes First-Party Authored

> Spec for converting the `superpowers-plus` Codex plugin from a mixed third-party/adapted overlay bundle into a first-party authored skill bundle. The upstream `obra/superpowers` v6.2.0 snapshot remains in `sources/third_party/` as reference and provenance.

## Problem

`codex-marketplace/plugins/superpowers-plus/` is currently a mixed bundle. It contains first-party helpers, third-party `verbatim` skills, and 14 third-party `adapted` skills that are materially rewritten by `adapters/codex/superpowers-plus/<skill>/overlay.yaml`. The overlays add Codex frontmatter, swap `run_subagent` templates, repoint path conventions (e.g. `.superpowers/` → `.agents/superpowers/`), add PowerShell siblings, and rewrite skill bodies. This has stopped being "overlay" work and is effectively first-party authorship with extra indirection.

The current posture also contradicts the custody doctrine: `sources/third_party/` is meant to stay immutable, but the projected skills in `codex-marketplace/plugins/superpowers-plus/` are the real editable artifacts because the overlays are so heavy. That makes source custody unclear and generation/validation more complex than the actual content requires.

## Goals

1. Convert every `superpowers-plus` skill that is currently `third_party` `adapted` into a first-party authored skill under `sources/first_party/skills/`.
2. Keep the upstream `obra/superpowers` v6.2.0 snapshot in `sources/third_party/superpowers/obra-superpowers/v6.2.0/` as immutable reference and provenance.
3. Migrate all adapter-held assets (scripts, references, `agents/openai.yaml`, etc.) into the matching first-party skill source trees.
4. Update `codex-marketplace/custody-pack-registry.json` so `superpowers-plus` entries point at first-party source with `content_mode: "verbatim"`.
5. Rename the `using-superpowers` skill to `using-superpowers-plus` in first-party source; keep all other skill names stable.
6. Retire the `adapters/codex/superpowers-plus/` overlay tree.
7. Remove the third-party overlay materializer and validation paths once no bundle entries use `adaptation_overlay_path`.
8. Regenerate all marketplace, plugin, and index surfaces with `tools/run marketplace --apply` and pass `tools/run ci --check`.

## Constraints

- `sources/third_party/superpowers/` remains immutable. Do not edit it.
- First-party source becomes the editable custody for `superpowers-plus` skills.
- Do not hand-edit generated plugin skill trees, bundle manifests, source maps, or provenance maps; edit the registry and source, then regenerate.
- All first-party skills must pass the marketplace shape validators and `normalize_first_party_skill_sources.py`.
- `using-superpowers` becomes `using-superpowers-plus`; downstream references in first-party skills (e.g. `inspecting-the-environment`) must be updated.
- The `superpowers-plus` plugin root and marketplace identity stay the same; only the source custody and provenance mode change.
- License posture stays honest: first-party skills are MIT, and each skill's provenance metadata names the upstream `obra/superpowers` v6.2.0 MIT source it derives from.

## Proposed Approaches

### Option A: Freeze overlay output as first-party source (recommended)

- Take the current projected `codex-marketplace/plugins/superpowers-plus/skills/<name>/` content (which is already the desired end state) and promote it to `sources/first_party/skills/<name>/`.
- Convert frontmatter to the canonical first-party shape.
- Move adapter scripts/references into the first-party skill roots.
- Update the registry to `first_party` `verbatim` and regenerate.
- **Pros:** fastest, lowest-risk, preserves the current behavior exactly, and cleanly retires the overlays.
- **Cons:** carries the current text exactly as-is, including any awkwardness from the overlay process, but that can be iteratively improved once it is editable source.

### Option B: Rewrite from scratch against the upstream

- For each skill, re-read `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/<name>/` and write a fresh first-party version.
- **Pros:** cleanest break from overlay artifacts.
- **Cons:** large editorial effort, risk of losing the current Devin Desktop/Codex-specific adaptations, and unnecessary because the projected content is already the desired artifact.

### Option C: Keep one foot in both lanes

- Convert only the most heavily adapted skills (e.g. `subagent-driven-development`, `using-superpowers`) and leave the rest as third-party `adapted`.
- **Pros:** smaller diff.
- **Cons:** keeps the overlay machinery alive and leaves the boundary muddy; does not solve the stated problem.

**Recommendation:** Option A.

## Design Details

### First-party skill inventory

The following first-party source roots are created under `sources/first_party/skills/`, each seeded from the current projected `codex-marketplace/plugins/superpowers-plus/skills/<name>/` content:

| Current projected skill | First-party source root | Notes |
| --- | --- | --- |
| `brainstorming` | `sources/first_party/skills/brainstorming` | Repointed Superpowers path references and spec-readiness handoff gate are now source content. |
| `dispatching-parallel-agents` | `sources/first_party/skills/dispatching-parallel-agents` | Marketplace metadata and skill-routing triggers are now source content. |
| `executing-plans` | `sources/first_party/skills/executing-plans` | Handoff-gates composition and completion-readiness step are now source content. |
| `finishing-a-development-branch` | `sources/first_party/skills/finishing-a-development-branch` | Marketplace frontmatter and triggers are now source content. |
| `receiving-code-review` | `sources/first_party/skills/receiving-code-review` | Marketplace frontmatter and triggers are now source content. |
| `requesting-code-review` | `sources/first_party/skills/requesting-code-review` | Plan path repointed to `.agents/superpowers/plans/` is now source content. |
| `subagent-driven-development` | `sources/first_party/skills/subagent-driven-development` | Bash and PowerShell helpers, `sdd` plan-scoped output, Devin Desktop profiles, and `requesting-branch-review` final review are now source content. |
| `systematic-debugging` | `sources/first_party/skills/systematic-debugging` | Bash and PowerShell helpers are now source content. |
| `test-driven-development` | `sources/first_party/skills/test-driven-development` | Marketplace frontmatter and triggers are now source content. |
| `using-git-worktrees` | `sources/first_party/skills/using-git-worktrees` | Worktree scripts are now source content. |
| `using-superpowers` | `sources/first_party/skills/using-superpowers-plus` | Renamed to `using-superpowers-plus` to make the first-party derivation explicit. |
| `verification-before-completion` | `sources/first_party/skills/verification-before-completion` | Marketplace frontmatter and triggers are now source content. |
| `writing-plans` | `sources/first_party/skills/writing-plans` | Plan path repointed to `.agents/superpowers/plans/` is now source content. |
| `writing-skills` | `sources/first_party/skills/writing-skills` | Marketplace frontmatter and triggers are now source content. |

The existing first-party skills already projected into `superpowers-plus` (`inspecting-the-environment`, `requesting-branch-review`, `handoff-gates`, `selecting-a-subagent`, `working-with-epics`) are left untouched except for any references to `@using-superpowers` that must become `@using-superpowers-plus`.

### `using-superpowers` → `using-superpowers-plus`

- First-party source root: `sources/first_party/skills/using-superpowers-plus`.
- Skill name: `using-superpowers-plus`.
- `agents/openai.yaml`: `skill_name: using-superpowers-plus`.
- All first-party skills that start with `@using-superpowers` are updated to `@using-superpowers-plus`.
- The `superpowers-plus` bundle still contains a `using-superpowers-plus` skill that is the workflow-selection entrypoint for that pack.

### First-party `SKILL.md` frontmatter

Each first-party `SKILL.md` must use the canonical first-party shape:

```yaml
---
name: <skill-name>
description: <trigger description>
metadata:
  source-id: <skill-name>
  source-path: sources/first_party/skills/<skill-name>/SKILL.md
  provenance-name: <Skill Name> first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: <trigger description>
  use_when:
    - ...
  do_not_use_when:
    - ...
  related_skills:
    - ...
license: MIT
---
```

`normalize_first_party_skill_sources.py` rebuilds this frontmatter from the canonical fields. Do not introduce a non-whitelisted `provenance` metadata block unless the normalizer is also updated to preserve it.

### Provenance in the skill body

Place the upstream attribution and license notice in the `SKILL.md` body, not in the YAML frontmatter. A brief, consistent block at the top of each derived skill:

```markdown
## Provenance

This skill is a first-party authored derivation of `obra/superpowers` v6.2.0, released under the MIT License. The original upstream snapshot is retained in `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/<original-skill-name>/` for reference.
```

The structured provenance (upstream author, license, repo, version, and derivation note) is recorded in `codex-marketplace/custody-pack-registry.json` under each entry's `provenance_note` and is surfaced in the generated `provenance-map.json` and `source-map.md`.

### First-party `agents/openai.yaml`

```yaml
version: 1
metadata:
  skill_name: <skill-name>
  source_category: first_party

interface:
  display_name: <Skill Name>
  short_description: <use when phrasing>
  default_prompt: Use /<skill-name> to <use when phrasing>.

policy:
  products:
    - codex
  allow_implicit_invocation: true
```

### Adapter asset migration

Each `adapters/codex/superpowers-plus/<skill>/` directory contains the following that must move into the matching first-party skill root:

- `overlay.yaml` → delete (no longer needed).
- `scripts/*` → move to `sources/first_party/skills/<skill>/scripts/`.
- `assets/*` → move to `sources/first_party/skills/<skill>/assets/`.
- `references/*` → move to `sources/first_party/skills/<skill>/references/`.
- `agents/openai.yaml` → replace with a generated first-party `agents/openai.yaml`.
- `subagent-driven-development/scripts/` contains `review-package`, `review-package.ps1`, `sdd-workspace`, `sdd-workspace.ps1`, `task-brief`, `task-brief.ps1` — all move into the first-party `subagent-driven-development` source.
- `using-git-worktrees/scripts/` contains `new-worktree.ps1`, `new-worktree.sh`, `new_worktree.py`, `remove-worktree.ps1`, `remove-worktree.sh`, `remove_worktree.py` — all move into the first-party `using-git-worktrees` source.
- `brainstorming/scripts/` contains `start-server.sh`, `stop-server.sh` and `start-server.ps1`, `stop-server.ps1` — move into first-party `brainstorming` source.
- `script-shell-selection.md` → move to a first-party `brainstorming/references/` or delete if it only served the overlay.

After migration, the entire `adapters/codex/superpowers-plus/` tree is removed.

### Registry changes

In `codex-marketplace/custody-pack-registry.json`, under the `superpowers-plus` pack, every third-party `adapted` entry becomes first-party `verbatim`:

```json
{
  "canonical_name": "brainstorming",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/brainstorming",
  "local_path": "skills/brainstorming",
  "provenance_note": "First-party skill derived from the obra/superpowers v6.2.0 MIT upstream snapshot retained in third-party source custody.",
  "copy_expectation": "byte_identical"
}
```

- Remove `import_status`, `adaptation_overlay_path`, `adapted_author`, `adaptation_note`, `source_path`, `source_author`, `source_license`, `source_repo`, and `source_family` from these entries.
- For `using-superpowers-plus`, `canonical_name` and `canonical_source_path` become `using-superpowers-plus` and `sources/first_party/skills/using-superpowers-plus`, while `local_path` stays `skills/using-superpowers-plus`.
- Update the pack `notes` to: "Superpowers+ is a first-party authored skill bundle. The upstream `obra/superpowers` v6.2.0 MIT snapshot is retained under `sources/third_party/superpowers/` as reference."
- Update `source_ledger` to list the first-party source roots instead of the upstream `package.json`, `README.md`, `LICENSE`, `AGENTS.md`. The upstream license and notice must still be referenced in `provenance/superpowers-plus.md`.

### Provenance surface update

- Update `provenance/superpowers-plus.md` to state that `superpowers-plus` is now a first-party authored bundle and that `sources/third_party/superpowers/` is the retained upstream reference.
- Update `provenance/first-party-skills.md` by regenerating after the new first-party skills are created.

### Tooling changes

After `superpowers-plus` is first-party and `feature-sliced-design` is confirmed `verbatim` (it currently has no overlay), the overlay machinery has no users:

- Remove `adapters/codex/superpowers-plus/`.
- Remove or narrow `adapters/AGENTS.md` if `adapters/` is no longer in use.
- Remove `tools/skill_overlay_materializer.py` and the overlay application code in `tools/project_skills.py`.
- Remove overlay validation in `tools/validate_marketplace.py`.
- Remove `tools/heal_overlays.py` and its `heal` target if it has no remaining use.
- Remove the `adaptation_overlay_path` field support from `tools/generate_pack_manifests.py` and `tools/project_skills.py`.
- Remove the `content_mode: "adapted"` and `normalised` code paths if they are no longer used by any pack.

These tooling changes can be a follow-up PR or the same PR if the generator/validator tests still pass; the spec treats them as the final phase.

## Files to Touch

### Create

- `sources/first_party/skills/brainstorming/` and `SKILL.md`, `agents/openai.yaml`, plus any migrated scripts/references.
- `sources/first_party/skills/dispatching-parallel-agents/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/executing-plans/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/finishing-a-development-branch/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/receiving-code-review/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/requesting-code-review/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/subagent-driven-development/` and `SKILL.md`, `agents/openai.yaml`, plus migrated `scripts/`.
- `sources/first_party/skills/systematic-debugging/` and `SKILL.md`, `agents/openai.yaml`, plus `scripts/find-polluter.ps1`.
- `sources/first_party/skills/test-driven-development/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/using-git-worktrees/` and `SKILL.md`, `agents/openai.yaml`, plus migrated `scripts/`.
- `sources/first_party/skills/using-superpowers-plus/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/verification-before-completion/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/writing-plans/` and `SKILL.md`, `agents/openai.yaml`.
- `sources/first_party/skills/writing-skills/` and `SKILL.md`, `agents/openai.yaml`.

### Modify

- `codex-marketplace/custody-pack-registry.json` — redeclare `superpowers-plus` entries as first-party `verbatim`.
- `provenance/superpowers-plus.md` — update the projection contract and provenance statement.
- `sources/first_party/skills/inspecting-the-environment/SKILL.md` — update `@using-superpowers` to `@using-superpowers-plus`.
- Any other first-party skills that name `@using-superpowers` in their body.

### Remove

- `adapters/codex/superpowers-plus/` tree.
- Overlay machinery in `tools/project_skills.py`, `tools/validate_marketplace.py`, `tools/generate_pack_manifests.py`, and `tools/skill_overlay_materializer.py` (when safe to do so).

### Regenerate (do not hand-edit)

- `codex-marketplace/plugins/superpowers-plus/skills/` and all children.
- `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`.
- `codex-marketplace/plugins/superpowers-plus/references/source-map.md`.
- `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`.
- `codex-marketplace/plugins/superpowers-plus/README.md`, `SOURCE.md`, `PROJECTION.md`.
- `provenance/first-party-skills.md`.
- `codex-marketplace/manifest.json` and `.agents/plugins/marketplace.json` if the bundle surface changes.
- `repo-index/repo-index.json` if new paths are added.

## Verification

1. `py -3 tools/generate_first_party_skill_catalog.py --check` (or `--apply` then `--check`) to validate the first-party skill set.
2. `py -3 tools/run.py marketplace --apply` to regenerate all derived surfaces.
3. `py -3 tools/run.py ci --check` to prove no drift remains.
4. `py -3 tools/validate_marketplace.py --check` to confirm the bundle manifest, source map, and provenance map are current.
5. `py -3 tools/project_skills.py --check` to confirm the projected `superpowers-plus` skill trees are byte-identical to the first-party source.
6. Inspect `codex-marketplace/plugins/superpowers-plus/references/source-map.md` to confirm every entry is `first_party` `verbatim`.
7. Confirm `adapters/codex/superpowers-plus/` is gone and no bundle entry carries `adaptation_overlay_path`.

## Out of scope

- Converting `feature-sliced-design` to first-party is a separate, future exercise. This spec leaves it as the only third-party `verbatim` pack and does not touch its source or registry entries.
- Editorial improvement of the skill bodies beyond what is required to make them valid first-party source. Once the skills are first-party, iterative improvements can happen in normal skill work.
- Renaming any skill other than `using-superpowers` → `using-superpowers-plus`.
