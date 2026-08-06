# MARK-301: Re-project ECC Skills Into Domain Packs From Fresh Source Inspection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reproject a deterministic ECC skill set from third-party source custody into installable Codex plugins, with every selected skill root internally sane, every shipped reference resolved inside the skill itself, and every selected skill mapped to a real topical pack instead of a generic workflow pack.

**Architecture:** ECC source stays in `sources/third_party/ecc/upstream` as third-party custody. Projection happens only into Codex plugin roots under `codex-marketplace/plugins/`, with path reshaping and metadata normalization handled by `adapters/codex/...`. The active selection is split across topical packs that match the skill merits: agentic workflow mechanics, agent evaluation/feedback, research, engineering delivery, repo hygiene, and security. `everything-codex-code` is the single ECC mega-pack that contains every selected third-party ECC skill for reference. No ECC projection is allowed into `superpowers-ecc`, `superpowers-plus`, or `codex-cortex`. The old `ecc-workflow-pack` label is retired for this issue.

**Source basis:** The retained mirror at `sources/third_party/ecc/upstream` is the implementation basis for this issue, pinned to upstream commit `71d22d0a77b7e0684f4e51cba03749b788993cdb`. That snapshot must be proven by custody files before any implementation proceeds.

**Tech Stack:** Markdown plans, retained third-party source custody, Codex marketplace plugin manifests, `adapters/codex`, mega-pack generator/validator tooling, repo index generation, skill-zip generation, PowerShell, Git.

## Global Constraints

- Do not create or restore `superpowers-ecc`.
- Do not reintroduce `ecc-superpowers` as a live wrapper or source surface.
- Do not project ECC into `superpowers-plus`.
- Do not project any ECC skill into `codex-cortex`.
- Do not create any first-party ECC skill source tree.
- Keep all ECC source custody in `sources/third_party/ecc/upstream`.
- Use `adapters/codex/...` for skill-root reshaping, metadata normalization, and internal path fixes.
- Every selected ECC skill must remain internally sane: relative links in the shipped skill root must resolve inside that root.
- Treat any existing adapter tree as potentially stale until it is compared against custody; do not inherit a deletion or relocation just because an adapter already says so.
- Treat any `superpowers-ecc` or `ecc-superpowers` provenance as historical evidence only; do not resurrect either name as an active projection surface.
- The active projection topology is domain packs, not one generic workflow pack.
- `everything-codex-code` is the required ECC mega-pack and must include every selected ECC third-party skill in this issue.
- `agents/openai.yaml` insertions must earn their keep: emit them only when the adapter can populate skill-specific metadata and a skill-specific description, not as generic stubs.
- The canonical shipped skill-root families are `references/`, `scripts/`, `assets/`, and `agents/openai.yaml`, with `examples/` normalized into `references/examples/` and `templates/` normalized into `references/templates/` by default.
- Use `assets/templates/` only when a template is genuinely asset-like or binary-ish and should not live as reference prose.
- No selected skill may ship loose files at the root besides `SKILL.md`; any other loose file must be normalized into one of the canonical root families.
- Keep the work to one branch and one PR.
- Do not hand-edit generated zips, generated registry files, source maps, provenance maps, marketplace manifests, repo indexes, or generated proof surfaces when tooling owns them.
- Use `py -3` for generator and validator commands.
- Implementation starts only after this plan is shared and approved.

---

## Selected Skill Set

The selected set is fixed after plan approval. Task 1 may only confirm it from custody or block with evidence; it may not reshuffle the selection during implementation.

### Agentic workflow mechanics

| Skill | Primary home | Roll-up | Shape | Normalization note |
| --- | --- | --- | --- | --- |
| `agent-harness-construction` | `agentic-workflows` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `autonomous-agent-harness` | `agentic-workflows` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `continuous-agent-loop` | `agentic-workflows` | `everything-codex-code` | single-file skill root | remains complementary to `using-superpowers`, not a router |
| `dynamic-workflow-mode` | `agentic-workflows` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `dmux-workflows` | `agentic-workflows` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `agentic-os` | `agentic-workflows` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |

### Agent evaluation and feedback

| Skill | Primary home | Roll-up | Shape | Normalization note |
| --- | --- | --- | --- | --- |
| `agent-self-evaluation` | `agentic-evaluation` | `everything-codex-code` | multi-file skill root | `examples/` -> `references/examples/`; `templates/` -> `references/templates/`; `scripts/` stays `scripts/` |
| `agent-eval` | `agentic-evaluation` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `agent-architecture-audit` | `agentic-evaluation` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |

### Research, engineering, repo hygiene, and security

| Skill | Primary home | Roll-up | Shape | Normalization note |
| --- | --- | --- | --- | --- |
| `research-ops` | `research-pack` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `ai-first-engineering` | `engineering-pack` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `deployment-patterns` | `engineering-pack` | `everything-codex-code` | single-file skill root | no shipped companions expected beyond `agents/openai.yaml` if justified |
| `search-first` | `repo-worker-base` | `everything-codex-code` | single-file skill root | stays complementary to repo hygiene and evidence-first editing |
| `safety-guard` | `security-pack` | `everything-codex-code` | single-file skill root | stays in the security pack as a destructive-action guard |
| `security-review` | `security-pack` | `everything-codex-code` | multi-file skill root | `cloud-infrastructure-security.md` must be normalized into `references/` rather than left loose at the root |

### Explicitly excluded for this issue

- `superpowers-ecc`, because it stays retired.
- `ecc-workflow-pack`, because the issue now uses topical domain packs instead of a generic workflow pack.
- `codex-cortex`, because user scope says ECC must not project there.
- `continuous-learning` v1 and `continuous-learning-v2`, because the upstream shape makes it a separate adaptation project and the user explicitly removed it from this pass.
- `claude-devfleet`, `rules-distill`, `skill-stocktake`, `skill-comply`, `team-agent-orchestration`, `team-builder`, `messages-ops`, `recursive-decision-ledger`, `token-budget-advisor`, `prediction-market-oracle-research`, and `ml-adoption-playbook`, because they were explicitly ruled out or do not earn their keep for the selected set.

---

### Task 1: Prove the pinned custody snapshot before any projection work

**Files:**
- Inspect: `sources/third_party/ecc/upstream/source-custody.md`
- Inspect: `sources/third_party/ecc/upstream/manifest.json`
- Inspect: `sources/third_party/ecc/upstream/LICENSE`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-self-evaluation/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-self-evaluation/examples/high-score-example.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-self-evaluation/examples/low-score-example.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-self-evaluation/references/evaluation-criteria.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-self-evaluation/references/hook-integration.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-self-evaluation/scripts/evaluate.py`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-self-evaluation/templates/evaluation-report.md`
- Inspect: `sources/third_party/ecc/upstream/skills/security-review/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/security-review/cloud-infrastructure-security.md`
- Inspect: `sources/third_party/ecc/upstream/skills/search-first/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/safety-guard/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agentic-os/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-harness-construction/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/autonomous-agent-harness/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/continuous-agent-loop/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/dmux-workflows/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/dynamic-workflow-mode/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-eval/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/agent-architecture-audit/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/research-ops/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/ai-first-engineering/SKILL.md`
- Inspect: `sources/third_party/ecc/upstream/skills/deployment-patterns/SKILL.md`
- Inspect: `provenance/ecc.md`
- Inspect: `provenance/security-pack.md`
- Inspect: `provenance/repo-worker-base.md`
- Inspect: `docs/custody-and-projection-doctrine.md`
- Inspect: `.agents/docs/contracts/openai-agent-yaml.md`
- Inspect: `.agents/docs/contracts/skill-frontmatter.md`

- [ ] **Step 1: Verify the custody snapshot is the exact pinned upstream state**

Confirm that `source-custody.md`, `manifest.json`, and the retained source tree jointly prove the pinned snapshot `71d22d0a77b7e0684f4e51cba03749b788993cdb`.

If those three custody surfaces do not agree, block implementation and report the mismatch. Do not proceed by assuming custody is current.

Expected result:

- the plan is tied to a proven custody snapshot before projection starts
- no implementation step is allowed to compensate for stale or inconsistent custody
- the worker must report the exact custody evidence used, or the exact blocker if custody does not line up

- [ ] **Step 2: Freeze the selected set and its topical homes**

Confirm the selected set above against custody and record, for each selected skill:

- retained source path
- primary topical home
- roll-up home
- file-shape class: single-file or multi-file
- whether any relative link in the root needs repointing
- whether any missing companion file needs to be recovered into custody first
- whether the skill should get a generated `agents/openai.yaml` or remain `SKILL.md`-only in the projected root

This step may confirm the matrix or block with evidence. It may not expand, contract, or reshuffle the selected set.

Expected result:

- the matrix contains the selected workflow, evaluation, research, engineering, repo, and security skills listed above
- no selected skill routes through `superpowers-ecc` or `superpowers-plus`
- no selected skill routes through `codex-cortex`
- every selected skill has a deterministic home
- every emitted `agents/openai.yaml` is backed by skill-specific metadata and description text, not a generic placeholder

- [ ] **Step 3: Verify internal link resolution and custody completeness**

For each selected skill root, verify that every relative link resolves inside that root:

- markdown links in `SKILL.md`
- links in companion docs under `examples/`, `references/`, or adjacent shipped files
- script/documentation pointers that assume files outside the root

If any link target is missing from custody, recover it from the external ECC repo into the skill root's custody mirror first, then re-point the shipped skill to that internal copy.

If an existing adapter deletes a file that is present in custody, treat that adapter as stale and regenerate the projection from custody instead of copying the deletion forward.

Expected result:

- `agent-self-evaluation` uses `references/examples/` and `references/templates/`
- `security-review` keeps its companion document under `references/`
- the remaining selected skills stay internally self-contained

- [ ] **Step 4: Lock the issue scope to the selected set only**

Record the final selection in the plan body itself so later implementation does not drift.

The active selection is:

- `agentic-workflows`
  - `agent-harness-construction`
  - `autonomous-agent-harness`
  - `continuous-agent-loop`
  - `dynamic-workflow-mode`
  - `dmux-workflows`
  - `agentic-os`
- `agentic-evaluation`
  - `agent-self-evaluation`
  - `agent-eval`
  - `agent-architecture-audit`
- `research-pack`
  - `research-ops`
- `engineering-pack`
  - `ai-first-engineering`
  - `deployment-patterns`
- `repo-worker-base`
  - `search-first`
- `security-pack`
  - `safety-guard`
  - `security-review`
- `everything-codex-code`
  - every selected skill above

This step is the scope lock for the rest of the PR.

---

### Task 2: Create the topical pack shells and define the ECC mega-pack

**Files:**
- Modify: `codex-marketplace/custody-mega-pack-registry.json`
- Modify: `codex-marketplace/plugin-roots.json`
- Create: `codex-marketplace/plugins/everything-codex-code/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/everything-codex-code/README.md`
- Create: `codex-marketplace/plugins/everything-codex-code/SOURCE.md`
- Create: `codex-marketplace/plugins/everything-codex-code/PROJECTION.md`
- Create: `codex-marketplace/plugins/everything-codex-code/LICENSE`
- Create: `codex-marketplace/plugins/everything-codex-code/assets/icon.svg`
- Create: `codex-marketplace/plugins/agentic-workflows/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/agentic-workflows/README.md`
- Create: `codex-marketplace/plugins/agentic-workflows/SOURCE.md`
- Create: `codex-marketplace/plugins/agentic-workflows/PROJECTION.md`
- Create: `codex-marketplace/plugins/agentic-workflows/assets/icon.svg`
- Create: `codex-marketplace/plugins/agentic-evaluation/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/research-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/engineering-pack/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/PROJECTION.md`
- Modify: `codex-marketplace/plugins/security-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/security-pack/PROJECTION.md`

- [ ] **Step 1: Add the ECC custody-to-mega-pack mapping back into the registry**

Restore the ECC family mapping so the generator treats `everything-codex-code` as the mega-pack for `sources/third_party/ecc/upstream`, while the new topical packs become the installable homes for the selected skills.

Expected result:

- `source_family` becomes `ecc`
- `mega_pack` becomes `everything-codex-code`
- `mega_pack_root` becomes `codex-marketplace/plugins/everything-codex-code`
- the topical pack roots become `agentic-workflows`, `agentic-evaluation`, `research-pack`, `engineering-pack`, `repo-worker-base`, and `security-pack`

- [ ] **Step 2: Create the topical pack roots and their shell files only**

Materialize the new topical pack roots as shell/source surfaces, not as generated proof surfaces.

Expected shape:

- create or update only the shell files and source/adapters needed to define the new pack roots
- do not hand-create generated bundle manifests, source maps, provenance maps, marketplace manifests, repo indexes, or generated zip registries
- `everything-codex-code` is a roll-up pack, not a separate source of truth

- [ ] **Step 3: Keep the existing topical packs that still own selected ECC skills**

Update only the existing packs that remain selected homes:

- `codex-marketplace/plugins/repo-worker-base`
- `codex-marketplace/plugins/security-pack`

Expected result:

- `search-first` stays in `repo-worker-base`
- `safety-guard` and `security-review` stay in `security-pack`
- no selected ECC skill is routed into `superpowers-plus`

- [ ] **Step 4: Refresh the marketplace registries through tooling, not hand edits**

The worker may update source/plugin shell files, but the following surfaces must be regenerated by tooling rather than edited directly:

- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `repo-index/repo-index.json`
- `generated/skill-zips/registry.json`
- generated pack `bundle-manifest.json`, `source-map.md`, and `provenance-map.json` files

The task outcome is a tooling refresh, not manual registry surgery.

Expected result:

- the new topical packs are present in the active inventory after regeneration
- no stale `superpowers-ecc` inventory remains
- the repo index and marketplace manifests agree with the new root set

---

### Task 3: Normalize the selected skill roots through adapters and repoint internal paths

**Files:**
- Modify or create: `adapters/codex/agentic-workflows/<skill>/overlay.yaml`
- Modify or create: `adapters/codex/agentic-workflows/<skill>/SKILL.md` only if the selected skill needs repo-specific reshaping
- Modify or create: `adapters/codex/agentic-evaluation/<skill>/overlay.yaml`
- Modify or create: `adapters/codex/research-pack/research-ops/overlay.yaml`
- Modify or create: `adapters/codex/engineering-pack/<skill>/overlay.yaml`
- Modify or create: `adapters/codex/repo-worker-base/search-first/overlay.yaml`
- Modify or create: `adapters/codex/security-pack/<skill>/overlay.yaml`
- Modify: `codex-marketplace/plugins/agentic-workflows/skills/<selected-skill>/...`
- Modify: `codex-marketplace/plugins/agentic-evaluation/skills/<selected-skill>/...`
- Modify: `codex-marketplace/plugins/research-pack/skills/research-ops/...`
- Modify: `codex-marketplace/plugins/engineering-pack/skills/<selected-skill>/...`
- Modify: `codex-marketplace/plugins/repo-worker-base/skills/search-first/...`
- Modify: `codex-marketplace/plugins/security-pack/skills/<selected-skill>/...`
- Modify: `provenance/ecc.md`
- Modify: `provenance/security-pack.md`
- Modify: `provenance/repo-worker-base.md`

- [ ] **Step 1: Apply adapter-only shape changes where the skill root needs local reshaping**

If a selected ECC skill needs any of the following:

- path normalization
- reference relocation
- companion-file copying
- metadata enrichment
- installability fixes
- stale adapter deletions that contradict custody
- normalization of loose root files into canonical OpenAI skill folders

then record that change in `adapters/codex/<target-pack>/<skill>/` rather than in third-party custody.

Expected result:

- third-party custody stays intact
- the projected plugin root becomes installable and self-contained
- the adapter explains the shape change honestly
- the worker can report exactly which skills emitted `agents/openai.yaml`, which stayed `SKILL.md`-only, and why

- [ ] **Step 2: Normalize companion files into canonical skill folders**

Apply the normalization rules consistently:

- `examples/` becomes `references/examples/`
- `templates/` becomes `references/templates/` when the template is textual or explanatory
- `templates/` becomes `assets/templates/` only when the content is asset-like and should be treated as a shipped asset
- loose root docs become `references/<name>.md`
- loose root JSON or configuration data becomes `references/<name>.json` unless the adapter proves a different canonical home is better

Expected result:

- `agent-self-evaluation` uses `references/examples/` and `references/templates/`
- `security-review` keeps its companion document under `references/`

- [ ] **Step 3: Gate `agents/openai.yaml` emission on skill-specific metadata**

If an adapter can produce a rich, skill-specific `agents/openai.yaml`, emit it with nonblank metadata and a description that actually identifies the skill's use case.

If it cannot, do not inject a generic stub.

Expected result:

- `agents/openai.yaml` exists only where it adds real value
- the file parses as YAML and satisfies the current contract in `.agents/docs/contracts/openai-agent-yaml.md`
- metadata fields such as `skill_name`, `plugin`, `source_category`, `upstream_name`, `upstream_version`, `projection_plugin`, and `content_mode` are all populated with nonblank values where present

- [ ] **Step 4: Refresh pack-level provenance notes for the new selected set**

Rewrite the provenance notes so they describe the newly selected ECC projections and nothing else.

Requirements:

- remove any mention of `superpowers-ecc`
- remove any mention of first-party ECC source or ledgers
- keep only the retained third-party ECC snapshot plus the current projection decision
- record the selected topical packs and the `everything-codex-code` roll-up explicitly

---

### Task 4: Update the generator, validator, and tests so the ECC shape is enforced by construction

**Files:**
- Modify: `tools/generate_mega_packs.py`
- Modify: `tools/generate_repo_index.py`
- Modify: `tools/validate_marketplace.py`
- Modify: `tools/validate_repo_index.py` only if the repo-index shape needs a new ECC guard
- Modify: `tools/materialize_projection.py` only if mega-pack materialization needs an ECC-specific path
- Modify: `tools/update_skill_artifacts.py` if the new pack topology needs a pack-aware refresh path
- Modify: `tests/test_validate_marketplace.py`
- Create or modify: a targeted regression test for skill-root link integrity and companion-file completeness

- [ ] **Step 1: Replace the stale `superpowers-ecc` generator and validator branches with the new topical packs**

Update the generator and validator code so the ECC family is owned by the new topical packs and the mega-pack, not by any Superpowers surface.

Expected result:

- `tools/generate_repo_index.py` exposes the new pack entries instead of a `superpowers-ecc` entry
- `tools/validate_marketplace.py` no longer treats `superpowers-ecc` as the ECC target
- validation fails if ECC reappears in `superpowers-plus` or `codex-cortex`

- [ ] **Step 2: Teach the validation path to enforce the inclusion rule**

Add a guard that requires every selected ECC projection to appear in `everything-codex-code`.

The guard must also ensure:

- ECC projections do not appear in `superpowers-plus`
- ECC projections do not appear in `codex-cortex`
- the mega-pack stays synchronized with the topical ECC selections
- the selected ECC set remains the same across topical plugins and the mega-pack

- [ ] **Step 3: Add regression coverage for skill-root integrity**

Extend the test suite so it proves:

- each selected ECC skill root has no unresolved relative links
- shipped companion files remain inside the same skill root
- any generated `agents/openai.yaml` has nonblank required metadata and a skill-specific description
- `agent-self-evaluation` ships `examples/`, `references/`, `scripts/`, and `templates/` only through canonical folders
- `security-review` ships `cloud-infrastructure-security.md` under `references/`
- the selected ECC roll-up is generated by code, not by manual manifest edits

Expected result:

- future drift in the registry, generator, or skill-root file shapes is caught by tests

---

### Task 5: Regenerate the derived outputs, validate the repo, and publish one PR

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/<selected-pack>/<selected-skill>/skill.zip`
- Modify: `codex-marketplace/manifest.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `repo-index/repo-index.json`
- Modify: any generated `codex-marketplace/plugins/everything-codex-code/**` and topical plugin proof files produced by tooling

- [ ] **Step 1: Regenerate the mega-pack and plugin projections from the selected matrix**

Run the generation path using the actual selected set from Task 1.

Expected command family:

```powershell
py -3 tools/generate_mega_packs.py
py -3 tools/update_skill_artifacts.py --skill
```

Run `py -3 tools/update_skill_artifacts.py --skill` once per selected pack/skill pair from Task 1. Use `--all` only if the selected set requires a full refresh and the resulting churn is intentionally reviewed.

- [ ] **Step 2: Verify the generated outputs are current and coherent**

Run:

```powershell
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/materialize_projection.py --check
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
git diff --check
```

Expected result:

- the new ECC mega-pack is present and current
- the selected topical ECC plugins are current
- no `superpowers-ecc` surface reappears
- no ECC content leaks into `superpowers-plus` or `codex-cortex`
- all generated proof surfaces match the chosen selection matrix
- the worker can provide explicit readback/grep evidence for the absence of live `superpowers-ecc`, `ecc-superpowers`, `superpowers-plus` ECC projection, and `codex-cortex` ECC projection
- the worker can report which selected skills emitted `agents/openai.yaml`, which remained `SKILL.md`-only, and why

- [ ] **Step 3: Publish the plan and the implementation in one branch/one PR**

After the plan is approved and the implementation is complete:

- stage the plan file alongside the code changes
- commit the branch
- push one PR

The final PR must include the plan file and the implementation diff together so the plan is visible next to the work it governed.

---

## Self-Review

### Spec coverage

1. Fresh ECC source inspection and deterministic selection matrix - Task 1
2. No `superpowers-ecc`, no ECC in `superpowers-plus`, and no ECC in `codex-cortex` - Global Constraints, Tasks 2 to 4
3. No first-party ECC source tree - Global Constraints, Task 1, Task 3
4. `everything-codex-code` mega-pack roll-up - Task 2 and Task 4
5. Adapter-only shape changes - Task 3
6. Generator, validator, and repo-index updates - Task 4
7. Derived output regeneration and validation - Task 5
8. One PR publication path - Task 5

### Placeholder scan

- No TBDs, TODOs, or unspecified paths are left for the implementation stage.
- The only conditional paths depend on custody proof from Task 1.
- The plan does not assume a `superpowers-ecc` fallback, a first-party ECC ledger, or a live `codex-cortex` projection.

### Type consistency

- `everything-codex-code` is the only ECC mega-pack in scope.
- `agentic-workflows`, `agentic-evaluation`, `research-pack`, `engineering-pack`, `repo-worker-base`, and `security-pack` are the topical homes for the selected ECC skills.
- `adapters/codex/...` is the only place this plan allows shape changes for selected ECC skills.
