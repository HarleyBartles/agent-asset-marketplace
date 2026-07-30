# Remove `rooms-project-pack` and `rooms-*` first-party skills

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Retire the `rooms-project-pack` Codex plugin and remove all first-party `rooms-*` skills from this repo, because those skills now live as local repo skills in the Rooms project and should no longer be vendored by the marketplace.

**Architecture:** Edit the editable custody registry, delete first-party source roots, clean hand-maintained provenance/intake references, then run the canonical marketplace regeneration and CI gate so every derived surface (plugin roots, manifests, bundle manifests, source maps, zips, catalog, repo index, mesh) is rebuilt from source rather than hand-edited.

**Tech Stack:** JSON, Python generators, `tools/run`, PowerShell.

## Global Constraints

- Source of truth for pack membership is `codex-marketplace/custody-pack-registry.json`; never hand-edit derived bundle manifests, source maps, provenance maps, projected skill trees, or zip artifacts.
- Source of truth for first-party skill presence is `sources/first_party/skills/<skill-name>/`; generated surfaces are derived from it.
- Destructive deletes must be staged with `git rm` (or tracked and committed as deleted) so git records the change.
- Full regeneration is `tools/run marketplace --apply`; full validation is `tools/run ci --check`.
- Do not edit historical plans under `.agents/superpowers/plans/` or specs unless the task itself is plan/spec authorship.

---

## Task 1: Verify the source and generated footprint before removal

**Files:**
- Read: `codex-marketplace/custody-pack-registry.json` (find the `rooms-project-pack` pack node, lines ~1099-1203)
- Read: `sources/first_party/skills/house-skills/intake.json`
- Read: `provenance/house-skills.md`
- Read: `provenance/rooms-project-pack.md`
- Read: `codex-marketplace/plugins/README.md`
- Read: `docs/custody-and-projection-doctrine.md` (around line 72)

**Interfaces:**
- Consumes: User instruction that `rooms-project-pack` and all `rooms-*` first-party skills are to be removed.
- Produces: Confirmed inventory of source files that must change.

- [x] **Step 1: List the tracked `rooms-*` first-party skills**

Run:
```powershell
Get-ChildItem -Directory 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance\sources\first_party\skills\rooms-*'
```

Expected output: five directories:
- `rooms-character-investigation`
- `rooms-image-sidecars`
- `rooms-project-doctrine`
- `rooms-risk-gates`
- `rooms-sheet-creator`

- [x] **Step 2: Confirm the `rooms-project-pack` pack node in the custody registry**

Run:
```powershell
py -3 -c "
import json, pathlib
p = pathlib.Path('Z:/_agent-worktrees/agent-asset-marketplace/fix/refreshing-installed-skills-provenance/codex-marketplace/custody-pack-registry.json')
data = json.loads(p.read_text(encoding='utf-8'))
for pack in data['packs']:
    if pack.get('bundle_name') == 'rooms-project-pack':
        print(pack)
"
```

Expected: A `projection-lane` pack node with plugin root `codex-marketplace/plugins/rooms-project-pack` and six entries, five `rooms-*` skills plus `database-design-patterns`.

- [x] **Step 3: List all hand-maintained files that reference the pack or `rooms-*` source paths**

Run:
```powershell
Set-Location 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance'
git grep -l 'rooms-project-pack' -- 'codex-marketplace/custody-pack-registry.json' 'provenance/' 'docs/' 'codex-marketplace/plugins/README.md'
git grep -l 'sources/first_party/skills/rooms-' -- 'provenance/' 'sources/first_party/skills/house-skills/'
```

Expected matches:
- `codex-marketplace/custody-pack-registry.json`
- `provenance/rooms-project-pack.md`
- `provenance/house-skills.md`
- `sources/first_party/skills/house-skills/intake.json`
- `docs/custody-and-projection-doctrine.md` (example text)
- `codex-marketplace/plugins/README.md` (active root list)

---

## Task 2: Remove the `rooms-project-pack` bundle node from the custody registry

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json` (delete the entire pack node for `bundle_name: "rooms-project-pack"`)

**Interfaces:**
- Consumes: Footprint from Task 1.
- Produces: A custody registry that no longer declares `rooms-project-pack` or any `rooms-*` entries.

- [x] **Step 1: Delete the pack node**

Using the editor, remove the JSON object that starts at:
```json
    {
      "bundle_name": "rooms-project-pack",
      "plugin_root": "codex-marketplace/plugins/rooms-project-pack",
```
and ends at the matching `},` just before the next pack object (or at the end of the array). Keep the surrounding array commas valid JSON.

- [x] **Step 2: Validate the registry is still well-formed JSON**

Run:
```powershell
py -3 -c "import json; json.load(open('Z:/_agent-worktrees/agent-asset-marketplace/fix/refreshing-installed-skills-provenance/codex-marketplace/custody-pack-registry.json', encoding='utf-8'))"
```

Expected: No exception.

---

## Task 3: Delete the first-party `rooms-*` skill source directories

**Files:**
- Delete: `sources/first_party/skills/rooms-character-investigation`
- Delete: `sources/first_party/skills/rooms-image-sidecars`
- Delete: `sources/first_party/skills/rooms-project-doctrine`
- Delete: `sources/first_party/skills/rooms-risk-gates`
- Delete: `sources/first_party/skills/rooms-sheet-creator`

**Interfaces:**
- Consumes: Task 2 (pack node removed).
- Produces: First-party source tree with no `rooms-*` skills.

- [x] **Step 1: Stage deletions with git**

Run from the worktree root:
```powershell
Set-Location 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance'
git rm -rf 'sources/first_party/skills/rooms-character-investigation' 'sources/first_party/skills/rooms-image-sidecars' 'sources/first_party/skills/rooms-project-doctrine' 'sources/first_party/skills/rooms-risk-gates' 'sources/first_party/skills/rooms-sheet-creator'
```

Expected: git reports five deleted directories.

- [x] **Step 2: Confirm the source tree is gone**

Run:
```powershell
Get-ChildItem -Directory 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance\sources\first_party\skills\rooms-*'
```

Expected: `Get-ChildItem: Cannot find path ... because it does not exist.`

---

## Task 4: Remove `rooms-*` entries from `house-skills` intake ledger

**Files:**
- Modify: `sources/first_party/skills/house-skills/intake.json`

**Interfaces:**
- Consumes: Task 3 (source paths removed).
- Produces: `intake.json` that no longer imports active `rooms-*` skills.

- [x] **Step 1: Remove the active `rooms-*` import objects**

Using the editor, delete every object in the `imports` array whose `public_name` or `source_id` starts with `rooms-` and whose `source_path` is under `sources/first_party/skills/rooms-*`. Retired historical objects whose source is already gone may be removed or moved to a dedicated retired section; the critical thing is that no `imports` entry points to a removed `rooms-*` source path.

The objects to remove are the five live entries:
- `rooms-image-sidecars`
- `rooms-project-doctrine`
- `rooms-character-investigation`
- `rooms-sheet-creator`
- `rooms-risk-gates`

- [x] **Step 2: Validate JSON**

Run:
```powershell
py -3 -c "import json; json.load(open('Z:/_agent-worktrees/agent-asset-marketplace/fix/refreshing-installed-skills-provenance/sources/first_party/skills/house-skills/intake.json', encoding='utf-8'))"
```

Expected: No exception.

- [x] **Step 3: Confirm no `rooms-*` imports remain**

Run:
```powershell
git diff -- 'sources/first_party/skills/house-skills/intake.json'
```

Expected: The diff shows only deleted `rooms-*` objects and no new references.

---

## Task 5: Delete the `provenance/rooms-project-pack.md` note

**Files:**
- Delete: `provenance/rooms-project-pack.md`

**Interfaces:**
- Consumes: Task 2 (pack removed from registry).
- Produces: No stale pack-level provenance note.

- [x] **Step 1: Delete the file through git**

Run:
```powershell
Set-Location 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance'
git rm 'provenance/rooms-project-pack.md'
```

Expected: git reports the file deleted.

---

## Task 6: Update `provenance/house-skills.md` for retired Rooms skills

**Files:**
- Modify: `provenance/house-skills.md`

**Interfaces:**
- Consumes: Tasks 3 and 4 (skills and intake removed).
- Produces: House Skills provenance note with no active `rooms-*` references and accurate historical notes.

- [x] **Step 1: Remove the `### Rooms` active imports subsection**

Delete this block in `provenance/house-skills.md`:
```markdown
### Rooms

- `rooms-project-doctrine-v1` - `sources/first_party/skills/rooms-project-doctrine/v1/rooms-project-doctrine-v1/SKILL.md`
- `rooms-risk-gates` - `sources/first_party/skills/rooms-risk-gates/SKILL.md`
- `rooms-character-investigation-v1` - `sources/first_party/skills/rooms-character-investigation/v1/rooms-character-investigation-v1/SKILL.md`
- `rooms-sheet-creator-v1` - `sources/first_party/skills/rooms-sheet-creator/v1/rooms-sheet-creator-v1/SKILL.md`
```

- [x] **Step 2: Remove the active `## rooms-*` skill sections**

Delete the following `## rooms-*` sections entirely:
- `## rooms-image-sidecars` (lines ~60-66)
- `## rooms-canon-buster` (lines ~68-75)
- `## rooms-bootstrap` (lines ~169-175)

- [x] **Step 3: Update the `risk-gates` notes**

Find the `risk-gates` entry. Replace text like:

```markdown
- Notes: Imported as the consolidated risk-gates skill that retires and replaces the six MARK-19 core generic buster source records (buster-framework, ambiguity-buster, boring-buster, invariant-buster, analogy-buster, canon-buster) plus the Rooms gate overlays (rooms-ambiguity-buster, rooms-analogy-buster, rooms-canon-buster, rooms-zoom-outs-buster), crew/crew-buster, boring-loop, and session-buster/session-buster-ingress. Generic gate references live under `references/gates/`; Rooms-specific gate profiles live in `rooms-risk-gates/references/`.
```

with:

```markdown
- Notes: Imported as the consolidated risk-gates skill that retires and replaces the six MARK-19 core generic buster source records (buster-framework, ambiguity-buster, boring-buster, invariant-buster, analogy-buster, canon-buster), crew/crew-buster, boring-loop, and session-buster/session-buster-ingress. Generic gate references live under `references/gates/`. Rooms-specific gate profiles were retired and moved to the Rooms project as local repo skills on 2026-07-30; this marketplace no longer vendors `rooms-risk-gates`.
```

- [x] **Step 4: Update the projection scope paragraph**

In the `## Projection scope` paragraph (around lines 211-215), remove references to `rooms-risk-gates` and `Rooms`. Example replacement:

```markdown
- Projection scope: reviewed active House Skills only, grouped into base/control plane and Wild Bunch, plus the shared `connector-safety` component in the base/control-plane lane, the `using-github` GitHub surface router skill, and the `risk-gates` consolidated pre-action risk gate router. The Adventures project pack, Don Logan boundary, and Rooms skills are retired and excluded from this projection.
```

- [x] **Step 5: Confirm no stale `rooms-*` source paths remain**

Run:
```powershell
git diff -- 'provenance/house-skills.md'
```

Expected: The diff shows the removed `### Rooms` section, removed `## rooms-*` sections, and updated `risk-gates` / projection scope notes. No `sources/first_party/skills/rooms-*` paths remain.

---

## Task 7: Update hand-maintained root documentation

**Files:**
- Modify: `codex-marketplace/plugins/README.md`
- Modify: `docs/custody-and-projection-doctrine.md`

**Interfaces:**
- Consumes: Task 2 (pack removed from registry).
- Produces: No prose claiming `rooms-project-pack` is an active root or example.

- [x] **Step 1: Remove `rooms-project-pack` from the active root list**

Edit `codex-marketplace/plugins/README.md` line 8. Remove `, `rooms-project-pack`' from the comma-separated list while preserving the surrounding sentence.

- [x] **Step 2: Update the topical pack example in the doctrine doc**

In `docs/custody-and-projection-doctrine.md` around line 72, replace:

```markdown
A topical projection-lane pack (such as `repo-worker-pack` or `rooms-project-pack`) is additional exposure, not a replacement home;
```

with:

```markdown
A topical projection-lane pack (such as `repo-worker-pack` or `architecture-pack`) is additional exposure, not a replacement home;
```

- [x] **Step 3: Verify the remaining references are intentional history only**

Run:
```powershell
git diff -- 'codex-marketplace/plugins/README.md' 'docs/custody-and-projection-doctrine.md'
```

Expected: Only the two deletions/edits above.

---

## Task 8: Regenerate all derived marketplace surfaces

**Files:**
- Generated (do not hand-edit): `codex-marketplace/plugin-roots.json`, `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`, `codex-marketplace/plugins/*/references/bundle-manifest.json`, `codex-marketplace/plugins/*/references/source-map.md`, `codex-marketplace/plugins/*/references/provenance-map.json`, `codex-marketplace/plugins/*/skills/*`, `codex-marketplace/plugins/rooms-project-pack/` (pruned), `generated/skill-zips/*.zip`, `provenance/first-party-skills.md`, `provenance/INDEX.md`, `repo-index/repo-index.json`, and `INDEX.md` files.

**Interfaces:**
- Consumes: Tasks 2-7 (editable source updated).
- Produces: A fully regenerated and consistent marketplace state.

- [x] **Step 1: Run the canonical full marketplace regeneration**

Run:
```powershell
Set-Location 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance'
py -3 tools/run.py marketplace --apply
```

Or on Windows PowerShell:
```powershell
.\tools\run.ps1 marketplace --apply
```

Expected: The command completes without errors. You should see lines like:
- `Pruned stale projected plugin root codex-marketplace/plugins/rooms-project-pack`
- `Pruned stale generated zip generated/skill-zips/rooms-*.zip`
- Plugin and manifest files are regenerated.

- [x] **Step 2: Verify no `rooms-project-pack` or `rooms-*` generated artifacts remain**

Run:
```powershell
Test-Path 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance\codex-marketplace\plugins\rooms-project-pack'
Get-ChildItem 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance\generated\skill-zips\rooms-*.zip'
git status --short
```

Expected: `False` for the plugin root; no `rooms-*.zip` files; `git status` shows expected changes and no unexpected generated artifacts left behind.

---

## Task 9: Run the CI gate

**Files:**
- All repo surfaces.

**Interfaces:**
- Consumes: Task 8 (regeneration complete).
- Produces: A green `ci --check` result proving the marketplace, repo-standards, and lint gates pass.

- [x] **Step 1: Run CI check**

Run:
```powershell
Set-Location 'Z:\_agent-worktrees\agent-asset-marketplace\fix\refreshing-installed-skills-provenance'
py -3 tools/run.py ci --check
```

Or on Windows PowerShell:
```powershell
.\tools\run.ps1 ci --check
```

Expected: Output ends with `OK ...` and exit code `0`.

- [x] **Step 2: If the gate fails, fix the root cause and re-run**

Common failures and fixes:
- `first-party orphan skills detected`: a `rooms-*` directory was not fully removed or a manifest still references it.
- `bundle manifest entry inventory does not match the live plugin root`: a `rooms-*` skill is still in `house-skills` projection but source is gone; re-run `tools/run marketplace --apply`.
- `validate_marketplace: inventory` or `plugin root mismatch`: `codex-marketplace/plugins/rooms-project-pack/` was not pruned; re-run `tools/run marketplace --apply`.
- `provenance paths mismatch`: `provenance/house-skills.md` still references a removed source path; edit and re-run.

---

## Task 10: Commit the rooms removal

**Files:**
- All modified/deleted files from Tasks 2-8.

**Interfaces:**
- Consumes: Task 9 (CI green).
- Produces: A clean commit in the worktree branch.

- [x] **Step 1: Review the diff**

Run:
```powershell
git diff --stat
```

- [x] **Step 2: Stage and commit**

Run:
```powershell
git add -A
git commit -m "$(cat <<'EOF'
marketplace: retire rooms-project-pack and remove rooms-* first-party skills

The Rooms skills now live as local repo skills in the Rooms project, so
stop vendoring them from agent-asset-marketplace.

- Remove the rooms-project-pack bundle node from custody-pack-registry.json
- Delete first-party sources for rooms-character-investigation,
  rooms-image-sidecars, rooms-project-doctrine, rooms-risk-gates, and
  rooms-sheet-creator
- Remove rooms-* entries from house-skills intake.json
- Delete the rooms-project-pack provenance note
- Update provenance/house-skills.md to retire Rooms references
- Drop rooms-project-pack from plugin root README and doctrine example
- Regenerate all marketplace, catalog, and repo-index surfaces

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
EOF
)"
```

---

## Self-Review

**1. Spec coverage:**
- Remove `rooms-project-pack` as a plugin: Task 2 (registry), Task 5 (provenance note), Task 7 (README list), Task 8 (regeneration pruning).
- Remove all `rooms-*` prefix skills from first-party source: Task 3 (source directories).
- Keep the same PR as the provenance work: Task 10 commits on top of the existing `fix/refreshing-installed-skills-provenance` branch; publication proof is shared with the original PR.

**2. Placeholder scan:**
- No `TBD`/`TODO`/fill-in steps. Every task has concrete commands and file paths.

**3. Type consistency:**
- JSON files are edited as JSON. JSON validation commands are provided.
- `git rm` is used for tracked deletions. `git add -A` captures generated changes from the canonical tooling.

## Execution Handoff

Plan complete and saved to `.agents/superpowers/plans/2026-07-30-remove-rooms-project-pack.md`.

Two execution options:

**1. Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** - Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints.

Before choosing, use `superpowers:handoff-gates` plan-readiness lane.
