# MARK-300: Retire linear-issue-compactor Into Worker Issue-Shaping Doctrine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `linear-issue-compactor` as an active first-party skill, move its compact Linear issue-shaping pattern into `worker-dispatch-linear` as a reference-backed default for worker issues, and update the surrounding Linear-shaping skills and house-skills ledgers so the retired path no longer appears as a live route.

**Architecture:** `worker-dispatch-linear` becomes the owning source for compact worker issue shape: the issue body stays a short control surface, dense material moves into attached docs, and a dedicated Preflight document carries only investigation seams and understanding questions. `linear-superpowers` keeps the smallest-applicable Linear issue-shaping role, but it stops routing to `linear-issue-compactor`; `boring-loop` routes dense issue bodies to `linear-superpowers` instead of the retired skill. House Skills source custody and its generated projections stay aligned through the existing generator/validator path, with `linear-issue-compactor` removed from active root inventory and any historical mentions preserved only in provenance or archive-ledger surfaces.

**Tech Stack:** Markdown plans, first-party skill source custody, Linear document/issue shaping, Codex marketplace projections, repo generator/validator tooling, PowerShell, Git.

## Global Constraints

- Do not implement source changes until this plan is approved.
- Keep the issue implementation-ready; do not introduce a new `worker-preflight-ready` or planning-only state.
- Preserve the MARK worker convention: worker-ready issues remain `Todo` + Harley + `WORKER` label + shaped DOD/validation, with no running evidence.
- Treat `linear-issue-compactor` as retired from active routing/projection. Any surviving mentions must be historical/provenance only or have a hard recorded reason.
- Use repo tooling for generated surfaces. Do not hand-edit generated manifests, projections, source maps, provenance maps, repo index entries, or `skill.zip` artifacts.
- Use `py -3` for generator and validator commands.
- Keep the work to one branch and one PR unless validation reveals a real split condition.
- If the implementation ends up requiring a version bump for `worker-dispatch-linear`, update the source-id and the version-history/changelog together.
- Before any repo inspection or planning, start from fresh `origin/main`, create or reuse a dedicated worktree for MARK-300, and record the worktree path plus the starting `origin/main` SHA in the preflight evidence. All repo inspection, plan writing, implementation, validation, and PR publication must happen from that worktree. Do not write source changes in the main checkout or in an unrelated existing worktree.

## Worktree Preflight Evidence

- Dedicated worktree path: `C:\WORK\codex-lanes\codex-b\worktrees\mark-300`
- Worktree branch: `codex/mark-300-retire-linear-issue-compactor`
- Starting `origin/main` SHA: `d65d7973b9d6862e6361e22001116f34684ee515`
- Worktree base: fresh `origin/main`
- Scope rule: repo inspection, planning, implementation, validation, and PR publication must stay inside this worktree
- Exclusion rule: do not write source changes in the main checkout or in an unrelated existing worktree

## Preflight Answers

### Where `linear-issue-compactor` currently lives

- Defined in source custody at `sources/first_party/skills/linear-issue-compactor/` with `SKILL.md`, `agents/openai.yaml`, `references/partition-patterns.md`, and `assets/icon.svg`.
- Projected into the live House Skills bundle at `codex-marketplace/plugins/house-skills/skills/linear-issue-compactor/`.
- Indexed in the House Skills source map and bundle manifest at `codex-marketplace/plugins/house-skills/references/source-map.md` and `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`.
- Zipped in the generated House Skills export at `generated/skill-zips/house-skills/linear-issue-compactor/skill.zip`, with the matching registry row in `generated/skill-zips/registry.json`.
- Referenced by live shaping docs in `sources/first_party/skills/house-skills/SKILL.md`, `sources/first_party/skills/house-skills/decisions.md`, `sources/first_party/skills/house-skills/decisions.json`, `sources/first_party/skills/house-skills/intake.json`, `sources/first_party/skills/linear-superpowers/SKILL.md`, `sources/first_party/skills/boring-loop/SKILL.md`, and the historical note in `provenance/house-skills.md`.

### Active versus historical surfaces

- Active now: the source tree for `linear-issue-compactor`, the House Skills projection, the generated House Skills zip, and the live House Skills ledgers that still name it as a current root.
- Active adjacent projections that will also move when the shared source text changes: `sources/first_party/skills/boring-loop/` projects into both `codex-marketplace/plugins/house-skills/` and `codex-marketplace/plugins/repo-worker-base/`; `sources/first_party/skills/linear-superpowers/` projects into both `codex-marketplace/plugins/house-skills/` and `codex-marketplace/plugins/superpowers-plus/`.
- Historical only after the change: any retained mention of the retired compactor should live in `provenance/house-skills.md` or another archive/provenance surface, not in the live root list or active routing text.
- The current `sources/first_party/skills/house-skills/decisions.md`, `decisions.json`, and `intake.json` are generator inputs today, not passive archive copies, so they must be updated in lockstep with the source and projection removal.

### Expected generated outputs

- `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- `codex-marketplace/plugins/house-skills/references/source-map.md`
- `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- `codex-marketplace/plugins/house-skills/README.md`
- `codex-marketplace/plugins/house-skills/SOURCE.md`
- `codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/linear-issue-compactor/**` should disappear from active projection output
- `generated/skill-zips/registry.json`
- `generated/skill-zips/house-skills/linear-issue-compactor/skill.zip` should disappear
- `generated/skill-zips/house-skills/worker-dispatch-linear/skill.zip` may change if the new compact-shape reference is surfaced in the shipped skill payload
- `generated/skill-zips/house-skills/linear-superpowers/skill.zip`, `generated/skill-zips/house-skills/boring-loop/skill.zip`, `generated/skill-zips/superpowers-plus/linear-superpowers/skill.zip`, and `generated/skill-zips/repo-worker-base/boring-loop/skill.zip` may change if the route-text edits alter the shipped payloads for those projections
- `repo-index/repo-index.json`
- `.agents/plugins/marketplace.json`
- `codex-marketplace/manifest.json`

### Why this is one PR

- The change is one custody-to-projection refactor with one retired source tree, one new reference file, two route-text edits, and one shared house-skills ledger cleanup.
- All affected outputs are derived from the same repository source-of-truth surfaces, so splitting them would create an invalid in-between state where the retired skill is removed from some places but still advertised in others.
- The validation set already checks the whole chain together, so a single PR keeps the removal atomic, reviewable, and easy to falsify.
- I do not see a separate protected surface, repo boundary, or prerequisite seam that forces a second PR.

## File Map

- `sources/first_party/skills/worker-dispatch-linear/SKILL.md`: own the new compact issue-shape doctrine and, if versioned, bump the active source id.
- `sources/first_party/skills/worker-dispatch-linear/references/compact-issue-shape.md`: new reference file for compact worker issue body, dense-doc buckets, and Preflight document rules.
- `sources/first_party/skills/worker-dispatch-linear/CHANGELOG.md`: record the doctrine move and any version bump.
- `sources/first_party/skills/worker-dispatch-linear/references/version-history.md`: record the active version if the source-id changes.
- `sources/first_party/skills/linear-superpowers/SKILL.md`: remove `linear-issue-compactor` routing and route compact worker issues through `worker-dispatch-linear` instead.
- `sources/first_party/skills/boring-loop/SKILL.md`: replace the dense-issue-body route to the retired compactor with the new Linear-shaping path.
- `sources/first_party/skills/house-skills/SKILL.md`: remove `linear-issue-compactor` from the live current-root list and update the active-root count.
- `sources/first_party/skills/house-skills/decisions.md`: drop the active compactor entry from the live ledger or mark it retired in-place if the generator requires a historical row.
- `sources/first_party/skills/house-skills/decisions.json`: keep the JSON ledger aligned with `decisions.md`.
- `sources/first_party/skills/house-skills/intake.json`: keep the structured intake mirror aligned with the live ledger.
- `provenance/house-skills.md`: preserve the retired compactor note as historical/provenance evidence if a record is still needed.
- `sources/first_party/skills/linear-issue-compactor/**`: delete the retired active skill source tree.
- Derived surfaces to regenerate: `codex-marketplace/plugins/house-skills/**`, `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`, `repo-index/repo-index.json`, `generated/skill-zips/registry.json`, and the `generated/skill-zips/house-skills/**` payload.

---

### Task 1: Lock the live edit surface and confirm the retirement target

**Files:**
- Inspect: `sources/first_party/skills/linear-issue-compactor/SKILL.md`
- Inspect: `sources/first_party/skills/linear-issue-compactor/agents/openai.yaml`
- Inspect: `sources/first_party/skills/linear-issue-compactor/references/partition-patterns.md`
- Inspect: `sources/first_party/skills/worker-dispatch-linear/SKILL.md`
- Inspect: `sources/first_party/skills/worker-dispatch-linear/agents/openai.yaml`
- Inspect: `sources/first_party/skills/worker-dispatch-linear/references/issue-readiness.md`
- Inspect: `sources/first_party/skills/worker-dispatch-linear/references/external-worker-handoff.md`
- Inspect: `sources/first_party/skills/worker-dispatch-linear/references/devin-campaign-shape.md`
- Inspect: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Inspect: `sources/first_party/skills/boring-loop/SKILL.md`
- Inspect: `sources/first_party/skills/house-skills/SKILL.md`
- Inspect: `sources/first_party/skills/house-skills/decisions.md`
- Inspect: `sources/first_party/skills/house-skills/decisions.json`
- Inspect: `sources/first_party/skills/house-skills/intake.json`
- Inspect: `provenance/house-skills.md`
- Inspect: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Inspect: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Inspect: `generated/skill-zips/registry.json`

- [x] **Step 1: Confirm the dedicated worktree gate before any repo inspection**

Use the worktree evidence above as the required starting condition.

Expected result:

- the implementation starts from fresh `origin/main`
- all repo work for MARK-300 stays inside the dedicated worktree
- the path and starting SHA are recorded before any further repo inspection or planning

- [x] **Step 2: Re-run the exact retirement search and record the live references**

Run:

```powershell
rg -n --hidden --glob '!generated/**' --glob '!.git/**' "linear-issue-compactor|/linear-issue-compactor" .
rg -n -C 2 "linear-issue-compactor|linear-superpowers|worker-dispatch-linear|boring-loop" sources/first_party/skills/house-skills/SKILL.md sources/first_party/skills/house-skills/decisions.md sources/first_party/skills/house-skills/intake.json provenance/house-skills.md
```

Expected result:

- active references are limited to the source-custody and historical/provenance surfaces that are intentionally being updated
- the plan has a concrete list of live files to edit and derived files to regenerate

- [x] **Step 3: Confirm whether `worker-dispatch-linear` needs a version bump**

Check the current active version in `sources/first_party/skills/worker-dispatch-linear/SKILL.md` and the matching `references/version-history.md` entry.

If the doctrine move changes the active source id, update the source-id, changelog, and version history together in the next task.

Expected result:

- the implementation does not guess at versioning
- the source-id, changelog, and version history stay internally consistent

---

### Task 2: Move compact Linear worker-shape doctrine into `worker-dispatch-linear`

**Files:**
- Modify: `sources/first_party/skills/worker-dispatch-linear/SKILL.md`
- Create: `sources/first_party/skills/worker-dispatch-linear/references/compact-issue-shape.md`
- Modify: `sources/first_party/skills/worker-dispatch-linear/CHANGELOG.md`
- Modify: `sources/first_party/skills/worker-dispatch-linear/references/version-history.md` if the source-id changes
- Modify: `sources/first_party/skills/worker-dispatch-linear/agents/openai.yaml` if the default prompt should surface the new reference
- Modify: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Modify: `sources/first_party/skills/boring-loop/SKILL.md`

- [x] **Step 1: Add the new compact issue-shape reference under `worker-dispatch-linear`**

Create `sources/first_party/skills/worker-dispatch-linear/references/compact-issue-shape.md` with these sections:

- compact issue body as a TOC/control surface;
- attached docs as the home for dense scope, implementation detail, validation, and evidence;
- one constant Preflight document for non-trivial worker implementation issues;
- Preflight content limited to investigation seams and questions that prove understanding;
- anti-patterns: do not turn Preflight into readiness state, do not bury all detail in Preflight, do not keep a separate compactor trigger for normal issue shaping.

Expected result:

- worker issue shape is owned by `worker-dispatch-linear`
- the reference is explicit enough that later edits do not need to infer the pattern from old compactor wording

- [x] **Step 2: Update `worker-dispatch-linear` to own the compact worker issue contract**

Edit `sources/first_party/skills/worker-dispatch-linear/SKILL.md` so it:

- describes the compact issue body / dense-doc / Preflight model directly;
- keeps worker issues implementation-ready, not planning-only;
- keeps the no-execution-lane rule intact;
- points the reader to the new reference file for the worker issue-shape pattern;
- bumps the active version if the source-id changes.

If the source-id is bumped, update `sources/first_party/skills/worker-dispatch-linear/CHANGELOG.md` and `references/version-history.md` in the same change.

Expected result:

- `worker-dispatch-linear` becomes the durable source for compact Linear worker issue shaping
- the skill still reads as a control-plane skill, not an execution lane

- [x] **Step 3: Remove compactor routing from `linear-superpowers`**

Edit `sources/first_party/skills/linear-superpowers/SKILL.md` so it no longer tells GPT to invoke `linear-issue-compactor`.

Replace that route with one of these explicit behaviors:

- apply compact issue shaping directly when the issue is a normal Linear packet;
- route worker issues to `worker-dispatch-linear` when the packet is a worker-ready repo task;
- keep `connector-safety` as the blocked-write recovery path.

Expected result:

- `linear-superpowers` stays the smallest-applicable Linear issue-shaping skill
- the retired compactor is no longer part of the active route text

- [x] **Step 4: Replace the dense-body fallback in `boring-loop`**

Edit `sources/first_party/skills/boring-loop/SKILL.md` so the dense-issue-body route points to the live shaping path instead of `linear-issue-compactor`.

Keep the false-green guard intact:

- the target must be named;
- the source of truth must be current;
- the mutation surface must be bounded;
- the proof route must be known;
- the result must be falsifiable from durable evidence.

Expected result:

- `boring-loop` still routes to the smallest safe next move
- the retired compactor is not treated as a live routing option

---

### Task 3: Retire the active compactor root from house-skills ledgers and archive it as history

**Files:**
- Modify: `sources/first_party/skills/house-skills/SKILL.md`
- Modify: `sources/first_party/skills/house-skills/decisions.md`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `provenance/house-skills.md`
- Delete: `sources/first_party/skills/linear-issue-compactor/**`
- Derived outputs to regenerate: `codex-marketplace/plugins/house-skills/**`, `generated/skill-zips/house-skills/**`, `generated/skill-zips/registry.json`, `repo-index/repo-index.json`, `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`

- [x] **Step 1: Remove `linear-issue-compactor` from the live house-skills current-root list**

Update `sources/first_party/skills/house-skills/SKILL.md` so the current-root list and active-root count no longer present `linear-issue-compactor` as a live control-plane skill.

Expected result:

- the live control-plane list reflects the retired root count
- the file no longer describes the retired skill as a current control-plane root

- [x] **Step 2: Keep the house-skills ledgers internally aligned**

Update `sources/first_party/skills/house-skills/decisions.md`, `decisions.json`, and `intake.json` together so the active ledger no longer treats `linear-issue-compactor` as a current imported root.

If a historical record is still required, preserve it in `provenance/house-skills.md` instead of leaving it as an active ledger entry.

Expected result:

- the source-ledger inputs and the narrative source doc agree
- the retired root is historical only, not active inventory

- [x] **Step 3: Delete the active source tree for `linear-issue-compactor`**

Remove the active source folder under `sources/first_party/skills/linear-issue-compactor/`.

Do not hand-edit the derived `codex-marketplace/plugins/house-skills/skills/linear-issue-compactor/` projection. Let the generators remove it when the source-ledger inputs no longer select it.

Expected result:

- the retired skill no longer has an active first-party source tree
- the generated projection is forced to follow source custody instead of stale projection files

---

### Task 4: Regenerate the marketplace, validate the retirement, and publish one PR

**Files:**
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Modify: `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md`
- Modify: `codex-marketplace/plugins/house-skills/README.md`
- Modify: `codex-marketplace/plugins/house-skills/SOURCE.md`
- Modify or delete: `codex-marketplace/plugins/house-skills/skills/linear-issue-compactor/**`
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/house-skills/worker-dispatch-linear/skill.zip` if the new reference changes the zip payload
- Modify: `generated/skill-zips/house-skills/linear-superpowers/skill.zip` if the route text change changes the zip payload
- Modify: `generated/skill-zips/house-skills/boring-loop/skill.zip` if the route text change changes the zip payload
- Modify: `repo-index/repo-index.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/manifest.json`

- [x] **Step 1: Refresh the derived artifacts through repo tooling**

Run:

```powershell
py -3 tools/update_skill_artifacts.py --all
py -3 tools/generate_marketplace.py
py -3 tools/generate_repo_index.py
py -3 tools/generate_provenance_maps.py
py -3 tools/generate_source_maps.py
```

Expected result:

- the live house-skills projection matches the updated source custody
- the retired skill disappears from active projection surfaces
- the new `worker-dispatch-linear` reference is carried into the generated skill payload

- [x] **Step 2: Validate the repo and confirm the retirement is not still active**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/materialize_projection.py --check
py -3 tools/validate_skill_zips.py
git diff --check
rg -n --hidden --glob '!generated/**' --glob '!.git/**' "linear-issue-compactor|/linear-issue-compactor" .
```

Expected result:

- `linear-issue-compactor` remains only in historical/provenance contexts or disappears entirely
- no active projection still exposes the retired skill as an installable or routed root
- generated artifacts and the repo index are current

- [x] **Step 3: Publish one branch and one PR after validation passes**

Create the branch from the fresh `origin/main`, commit the plan and implementation together, push once, and open one PR.

Return evidence must include:

- branch name;
- starting `origin/main` SHA;
- final head SHA;
- PR URL;
- changed files;
- exact validation commands and results;
- generated-artifact explanation;
- GREEN/AMBER/RED/BLOCKED judgment.

Expected result:

- the plan, source changes, and validation are all visible in one reviewable publication surface
- the retired-skill removal is provable from GitHub-visible state, not just local output

## Self-Review

### Spec coverage

1. Retire and remove `linear-issue-compactor` as an active skill - Task 3, Task 4
2. Move compact issue-shaping doctrine into `worker-dispatch-linear` - Task 2
3. Remove compactor routing from `linear-superpowers` and `boring-loop` - Task 2
4. Keep worker issues implementation-ready, not planning-only - Global Constraints, Task 2
5. Keep historical/provenance mentions only where justified - Global Constraints, Task 3
6. Regenerate marketplace manifests, source maps, provenance maps, repo index, and zips through tooling - Task 4
7. Verify no active projection still exposes the retired skill - Task 4
8. Return branch, SHAs, PR URL, changed files, and validation output - Task 4

### Placeholder scan

- No TBDs or undefined file paths remain in the plan.
- The only conditional item is the `worker-dispatch-linear` version bump, and it is explicitly tied to the observed source-id change.

### Type consistency

- `compact-issue-shape.md` is the new reference file path used by both the source edit and the later regeneration step.
- `worker-dispatch-linear` is the owning skill for the compact worker issue doctrine.
- `linear-superpowers` is the issue-shaping router, not the retired compactor.
- `boring-loop` remains the false-green coordinator and points at the live shaping path.

## Completion

- Implementation, regeneration, and validation completed in the dedicated MARK-300 worktree.
- The retired `linear-issue-compactor` source tree and its generated projection were removed from active custody and export surfaces.
- The plan is published in the PR alongside the implementation diff so the review surface includes the completed contract and the final evidence chain.
