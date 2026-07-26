# Update Superpowers+ to upstream v6.2.0

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the retained `obra/superpowers` upstream snapshot from `v6.1.0` to `v6.2.1`, keep `superpowers-plus` source-custody and provenance records accurate, and reconcile the `adapters/codex/superpowers-plus/` overlays so the Codex projection still applies the same repo-local adaptations on top of the new upstream source.

**Architecture:** Use the deterministic source-update path (`tools/update_superpowers_source.py`) and the projection rebuild path (`tools/rebuild_marketplace.py`). The `update_superpowers_source.py` script currently edits the generated `bundle-manifest.json` but not the source-of-truth `custody-pack-registry.json`, so the first task is to fix that. Then update overlay metadata/version pins, manually reconcile the overlays that `heal_overlays.py` cannot auto-heal, run the rebuild, and validate.

**Tech Stack:** Python 3, YAML, git, `py -3 tools/update_superpowers_source.py`, `py -3 tools/heal_overlays.py`, `py -3 tools/rebuild_marketplace.py`, `py -3 tools/check_marketplace.py`.

---

## Global constraints

- `codex-marketplace/custody-pack-registry.json` is the source of truth for pack manifests. `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json` is generated from it; do not hand-edit it as a final source of truth.
- `sources/third_party/**` is immutable retained custody. Do not edit upstream content; express all marketplace-specific behavior through `adapters/codex/superpowers-plus/**` overlays.
- Preserve the existing adaptation intent: add Codex marketplace frontmatter, repoint `docs/superpowers/` to `.agents/superpowers/`, repoint `.superpowers/` to `.agents/superpowers/`, and keep bundled `new-worktree`/`remove-worktree`/SDD helpers.
- Generated surfaces (`codex-marketplace/plugins/superpowers-plus/skills/`, `.agents/skills/`, `generated/skill-zips/`, source/provenance maps) must be regenerated, not hand-edited.

---

## Task 1: Fix `tools/update_superpowers_source.py` to update the source-of-truth registry

`tools/update_superpowers_source.py` is the canonical helper for bumping the retained `obra/superpowers` snapshot. Its `_update_custody_registry()` currently looks for `registry["mappings"]`; the actual registry uses `registry["packs"]`, and the `superpowers-plus` pack carries the per-skill `entries` and `source_ledger` that `generate_pack_manifests.py` reads. Fixing this keeps `rebuild_marketplace.py` from silently reverting the bundle manifest back to `v6.1.0`.

**Files:**
- Modify: `tools/update_superpowers_source.py`

### Step 1: Replace `_update_custody_registry` with a pack-aware update

Change the function to locate the `superpowers-plus` pack in `registry["packs"]`, update `source_ledger`, and update every `entries` item whose `source_family` is `superpowers`:

```python
def _update_custody_registry(
    *,
    old_root: str,
    old_version: str,
    new_root: str,
    new_version: str,
) -> None:
    registry = json.loads(SUPERPOWERS_CUSTODY_REGISTRY_PATH.read_text(encoding="utf-8"))
    changed = False
    for pack in registry.get("packs", []):
        if not isinstance(pack, dict):
            continue
        if pack.get("bundle_name") != "superpowers-plus":
            continue

        source_ledger = pack.get("source_ledger", [])
        for i, ledger_path in enumerate(source_ledger):
            if not isinstance(ledger_path, str):
                continue
            updated = ledger_path.replace(old_root, new_root).replace(old_version, new_version)
            if updated != ledger_path:
                source_ledger[i] = updated
                changed = True

        for entry in pack.get("entries", []):
            if not isinstance(entry, dict):
                continue
            if entry.get("source_family") != "superpowers":
                continue
            for field in (
                "canonical_source_path",
                "source_path",
                "provenance_note",
                "adaptation_note",
            ):
                value = entry.get(field)
                if isinstance(value, str):
                    updated = value.replace(old_root, new_root).replace(old_version, new_version)
                    if updated != value:
                        entry[field] = updated
                        changed = True
            if entry.get("source_repo") != UPSTREAM_REPO:
                entry["source_repo"] = UPSTREAM_REPO
                changed = True

        break  # superpowers-plus is unique

    if changed:
        SUPERPOWERS_CUSTODY_REGISTRY_PATH.write_text(
            json.dumps(registry, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
```

### Step 2: Pass old and new roots into the call

In `_prepare()`, change the call from `_update_custody_registry(target_root.relative_to(ROOT).as_posix())` to:

```python
_update_custody_registry(
    old_root=old_root,
    old_version=old_version,
    new_root=target_root.relative_to(ROOT).as_posix(),
    new_version=tag,
)
```

### Step 3: Keep `_update_bundle_manifest()` aligned

Optionally expand `_update_bundle_manifest` to also rewrite `adaptation_note` and `source_repo` for every third-party entry, so the generated bundle manifest is internally consistent before `rebuild_marketplace.py` regenerates it from the registry.

---

## Task 2: Prepare the new upstream source snapshot

**Files:**
- Create: `sources/third_party/superpowers/obra-superpowers/v6.2.0/**`
- Delete: `sources/third_party/superpowers/obra-superpowers/v6.1.0/**`
- Modify: `codex-marketplace/custody-pack-registry.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Modify: `provenance/superpowers-plus.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json` (intermediate, regenerated later)

### Step 1: Run the source-custody prepare step

```powershell
py -3 tools/update_superpowers_source.py --tag v6.2.0 --prepare
```

Expected output includes:
- Resolved tag object and commit SHA for `v6.2.0`.
- `sources/third_party/superpowers/obra-superpowers/v6.2.0/` populated.
- Adapter-drift warning pointing at `using-superpowers/overlay.yaml` and `agents/openai.yaml`.

### Step 2: Verify the registry was updated

```powershell
Select-String 'v6\.2\.0' codex-marketplace/custody-pack-registry.json | Select-Object -First 10
```

Expected: `canonical_source_path` and `source_path` entries for every superpowers-plus skill now point at `.../obra-superpowers/v6.2.0/...`.

### Step 3: Verify provenance and source docs

```powershell
Select-String 'v6\.2\.0' provenance/superpowers-plus.md, codex-marketplace/plugins/superpowers-plus/SOURCE.md
```

Expected: release tag, commit, and source-ledger paths reflect `v6.2.0`.

---

## Task 3: Update overlay metadata and version pins

Every `adapters/codex/superpowers-plus/*/overlay.yaml` and `adapters/codex/superpowers-plus/using-superpowers/agents/openai.yaml` still claims `upstream_version: v6.1.0` and `source_path: .../obra-superpowers/v6.1.1/...`. If left unchanged, the projected frontmatter will lie about its source and fail marketplace provenance validation.

**Files:**
- Modify: `adapters/codex/superpowers-plus/*/overlay.yaml` (14 overlays)
- Modify: `adapters/codex/superpowers-plus/using-superpowers/agents/openai.yaml`

### Step 1: Bulk-replace `v6.1.0` references in superpowers-plus adapters

Run from the repo root:

```powershell
Get-ChildItem -Recurse -File adapters/codex/superpowers-plus | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $new = $content -replace 'v6\.1\.0', 'v6.2.0'
    if ($new -ne $content) {
        Set-Content -Path $_.FullName -Value $new -NoNewline
        Write-Host "updated $($_.FullName)"
    }
}
```

Verify:

```powershell
grep -R 'v6\.1\.0' adapters/codex/superpowers-plus
```

Expected: no matches.

### Step 2: Verify `openai.yaml` still has all required fields

```powershell
py -3 tools/skill_overlay_materializer.py --check-openai adapters/codex/superpowers-plus/using-superpowers/agents/openai.yaml
```

If that flag does not exist, validate by inspection: the file must contain `upstream_version: v6.2.1` and a nonblank `source-path` pointing at the new `SKILL.md`.

---

## Task 4: Heal the overlays that drifted against v6.2.0

`py -3 tools/heal_overlays.py --check` against the prepared `v6.2.0` snapshot showed the following overlays cannot be auto-healed because `v6.2.1` changed or removed the source text the overlays target:

| Overlay | Problem | Required action |
|---|---|---|
| `finishing-a-development-branch` | Upstream description shortened; `SKILL.md` 1-4 `expected_lines` no longer match. | Update `expected_lines` to the new v6.2.0 frontmatter and keep the `replace_lines` metadata block with the new `source_path`/`upstream_version`. |
| `subagent-driven-development` | Upstream now plan-scopes SDD and already passes `PLAN_FILE` to `review-package`; five old `expected_lines` blocks about `BASE HEAD` no longer exist, and `.superpowers/sdd/progress.md` became `.superpowers/sdd/<plan-basename>/progress.md`. | Remove or rework line-edits that added `PLAN_FILE` (upstream now covers them). Keep path edits that repoint `docs/superpowers/plans/` to `.agents/superpowers/plans/` and `.superpowers/sdd/` to `.agents/superpowers/sdd/` (preserving the `<plan-basename>` segment). |
| `using-git-worktrees` | Upstream restructured guard sections into a rationalization table; at least one `insert_after` anchor is gone. | Re-anchor or replace the relevant insert against a surviving line in the v6.2.0 `SKILL.md`. |

The following overlays only have line-number shifts and can be auto-healed after the version-pin update:

- `brainstorming`
- `executing-plans`
- `writing-plans`

**Files:**
- Modify: `adapters/codex/superpowers-plus/finishing-a-development-branch/overlay.yaml`
- Modify: `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`
- Modify: `adapters/codex/superpowers-plus/using-git-worktrees/overlay.yaml`

### Step 1: Reconcile `finishing-a-development-branch`

Open `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/finishing-a-development-branch/SKILL.md` and the overlay. Update the first edit so `expected_lines` matches the new frontmatter exactly:

```yaml
- path: SKILL.md
  op: replace
  start_line: 1
  end_line: 4
  expected_lines:
  - '---'
  - 'name: finishing-a-development-branch'
  - 'description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work'
  - '---'
  replace_lines:
  - '---'
  - 'name: finishing-a-development-branch'
  - 'description: "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work"'
  - 'metadata:'
  - '  source_category: "third_party"'
  - '  upstream_name: "finishing-a-development-branch"'
  - '  upstream_version: "v6.2.0"'
  - '  adaptation_overlay: "adapters/codex/superpowers-plus/finishing-a-development-branch"'
  - '  projection_plugin: "superpowers-plus"'
  - '  source_author: "obra"'
  - '  source_license: "MIT"'
  - '  source_repo: "https://github.com/obra/superpowers"'
  - '  source_path: "sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/finishing-a-development-branch/SKILL.md"'
  - '  content_mode: "adapted"'
  - '  adapted_author: "Harley Bartles"'
  - '  adaptation_note: "Added marketplace frontmatter metadata block and skill-routing triggers to the upstream skill without modifying the instruction body."'
  ...
```

Verify:

```powershell
py -3 tools/heal_overlays.py --overlay adapters/codex/superpowers-plus/finishing-a-development-branch/overlay.yaml --check
```

Expected: no `ERROR` lines.

### Step 2: Reconcile `subagent-driven-development`

Open `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/subagent-driven-development/SKILL.md` and the overlay. Remove every `replace` edit whose sole purpose was to insert `PLAN_FILE` into `scripts/review-package BASE HEAD`, because `v6.2.0` already reads `scripts/review-package PLAN_FILE BASE HEAD`.

Keep and update any edits that change path prefixes:
- `docs/superpowers/plans/feature-plan.md` -> `.agents/superpowers/plans/feature-plan.md`
- `.superpowers/sdd/progress.md` -> `.agents/superpowers/sdd/<plan-basename>/progress.md` (preserve the directory segment upstream added)

For each remaining edit, set `expected_lines` to the exact text in `v6.2.0` and run:

```powershell
py -3 tools/heal_overlays.py --overlay adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml --check
```

Expected: only line-number/whitespace healing reports, no `content NOT FOUND` errors.

### Step 3: Reconcile `using-git-worktrees`

Open `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/using-git-worktrees/SKILL.md` and the overlay. Locate each `insert_after` anchor in the new source; if an anchor is gone, replace it with a surviving line near the same logical location, or convert the insert into a `replace` of a short block that still exists.

Verify per overlay:

```powershell
py -3 tools/heal_overlays.py --overlay adapters/codex/superpowers-plus/using-git-worktrees/overlay.yaml --check
```

Expected: no `ERROR` lines.

### Step 4: Auto-heal the remaining overlays

After all manual reconciliation:

```powershell
py -3 tools/heal_overlays.py
```

This updates `start_line`/`end_line` and `expected_lines` whitespace for `brainstorming`, `executing-plans`, `writing-plans`, and any other shifted-but-otherwise-unchanged blocks. Re-run `--check` until it returns `0`:

```powershell
py -3 tools/heal_overlays.py --check
```

Expected:

```
OK all overlays healthy
```

---

## Task 5: Regenerate projections and derived surfaces

**Files:**
- Modify (generated): `codex-marketplace/plugins/superpowers-plus/skills/**`
- Modify (generated): `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Modify (generated): `codex-marketplace/plugins/superpowers-plus/references/source-map.md`
- Modify (generated): `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- Modify (generated): `generated/skill-zips/**`
- Modify (generated): `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`, `repo-index/repo-index.json`
- Modify (generated): `.agents/skills/**`

### Step 1: Run the canonical rebuild

```powershell
py -3 tools/rebuild_marketplace.py
```

If `update_superpowers_source.py` still insists on adapter staleness, run `rebuild_marketplace.py` directly; it calls `heal_overlays.py` in write mode as the first phase.

### Step 2: Verify the bundle manifest was regenerated from the registry

```powershell
grep 'v6\.2\.0' codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json | Select-Object -First 5
```

Expected: every `canonical_source_path` and `source_path` now contains `v6.2.0`.

---

## Task 6: Validate

### Step 1: Run the CI gate

```powershell
py -3 tools/check_marketplace.py
```

Expected:

```
Marketplace validation passed.
Repo index validation passed.
```

### Step 2: Verify git status and diff

```powershell
git status --short
git diff --check
```

Expected: `git diff --check` reports no whitespace errors, and the only untracked files are the new upstream tree and any generated artifacts.

### Step 3: Sanity-check projected skill frontmatter

```powershell
grep 'upstream_version' codex-marketplace/plugins/superpowers-plus/skills/*/SKILL.md | Select-Object -First 10
```

Expected: all `upstream_version` values are `v6.2.0`.

---

## Task 7: Commit, push, and open a PR

Follow `repo-worker-base` / `finishing-a-development-branch` publication proof. The PR branch is the worktree used for the upgrade.

### Step 1: Stage and commit

```powershell
git add -A
git commit -m "feat: update retained superpowers upstream to v6.2.0 and heal codex overlays"
```

### Step 2: Push and open PR to `main`

```powershell
git push -u origin scope-superpowers-v6-2-0
gh pr create --base main --title "Update superpowers-plus to upstream v6.2.0" --body-file pr-body.md
```

The PR body should include:
- Upstream tag and commit (`v6.2.0`, `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`).
- The overlays that required manual reconciliation (`finishing-a-development-branch`, `subagent-driven-development`, `using-git-worktrees`).
- Verification output from `py -3 tools/check_marketplace.py`.
- The `update_superpowers_source.py` registry fix.

---

## Risks and open decisions

- **Registry source-of-truth bug:** If `tools/update_superpowers_source.py` is not fixed first, `rebuild_marketplace.py` will regenerate `bundle-manifest.json` from `custody-pack-registry.json` and silently revert the version pins to `v6.1.0`.
- **Manual overlay work is concentrated in three files:** `subagent-driven-development`, `using-git-worktrees`, and `finishing-a-development-branch`. The rest are either line-number shifts or only need version-pin replacement.
- **Plan-scoped SDD paths:** `v6.2.0` introduces `.superpowers/sdd/<plan-basename>/`. The overlay must repoint this to `.agents/superpowers/sdd/<plan-basename>/` while preserving the directory segment; do not collapse it back to a flat path.
- **New upstream files:** `v6.2.0` adds `skills/using-superpowers/references/gemini-tools.md` and `skills/subagent-driven-development/re-review-prompt.md`. They will be copied into the projection automatically. No overlay action is required unless you want `using-superpowers/SKILL.md` to list `gemini-tools.md` in the harness list.
- **`testing-anti-patterns.md` removed, `writing-good-tests.md` added:** `test-driven-development` projection tree will reflect this automatically.
- **Intermediate `bundle-manifest.json` edits:** Because `bundle-manifest.json` is generated, the script's direct edit is only a convenience for `heal_overlays.py`. The registry fix is the durable change.
