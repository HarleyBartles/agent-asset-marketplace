# Make plugin onboarding generation metadata-driven Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let ordinary plugin onboarding generation pull repo-index data from plugin metadata instead of hand-coded generator branches, starting with the Superpowers/ECC path required by MARK-244 and MARK-259.

**Architecture:** Keep protected marketplace ordering and validation intact, but move the per-plugin repo-index details into bundle-manifest metadata where the generator can read them directly. Use a narrow metadata contract so the generator can synthesize entries from the plugin root inventory plus bundle-manifest hints, while still falling back to the existing registry copy path for unchanged roots.

**Tech Stack:** Python 3, JSON manifests, marketplace generators, repo-index validation, PowerShell shell commands.

---

### Task 1: Add metadata-driven repo-index hints to the Superpowers bundle manifests

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json`

- [x] **Step 1: Add a `repo_index` metadata object to each bundle manifest with the repo-index-only fields the generator should consume.**

```json
{
  "repo_index": {
    "source_ledger": ["..."],
    "provenance_refs": ["..."],
    "agents_md": null,
    "registry_alignment": {
      "status": "aligned",
      "note": null
    }
  }
}
```

- [x] **Step 2: Keep the existing bundle manifest validation fields and notes unchanged so the current marketplace projection still validates.**

- [x] **Step 3: Review the updated JSON for ordering, trailing commas, and path consistency against the current repo-index entry shape.**

### Task 2: Generalize repo-index synthesis to read metadata instead of hard-coding ordinary pack branches

**Files:**
- Modify: `tools/generate_repo_index.py`
- Modify: `repo-index/repo-index.json`

- [x] **Step 1: Add a helper that loads a plugin's bundle manifest, reads the optional `repo_index` metadata block, and merges it with the plugin-root fields from `codex-marketplace/plugin-roots.json`.**

```python
def _metadata_driven_plugin_entry(plugin: dict[str, Any]) -> dict[str, Any] | None:
    bundle_manifest = _load_bundle_manifest(plugin["plugin_root"])
    repo_index = bundle_manifest.get("repo_index")
    if not isinstance(repo_index, dict):
        return None
    return {
        "name": plugin["name"],
        "plugin_root": plugin["plugin_root"],
        "plugin_manifest": plugin["manifest_path"],
        "source_md": bundle_manifest.get("source_md") or f"{plugin['plugin_root']}/SOURCE.md",
        "source_ledger": repo_index.get("source_ledger", []),
        "license_path": f"{plugin['plugin_root']}/LICENSE",
        "bundle_manifest": f"{plugin['plugin_root']}/references/bundle-manifest.json",
        "skills_path": f"{plugin['plugin_root']}/skills",
        "provenance_refs": repo_index.get("provenance_refs", []),
        "agents_md": repo_index.get("agents_md"),
        "registry_path": plugin["registry_path"],
        "registry_alignment": repo_index.get("registry_alignment", {"status": "aligned", "note": None}),
    }
```

- [x] **Step 2: Remove the dedicated `superpowers-plus` and `superpowers-ecc` branches from the generator and let the new metadata-driven helper synthesize those entries.**

- [x] **Step 3: Keep the existing fallback path for protected roots that do not yet expose `repo_index` metadata, so the generator remains stable for unchanged marketplace entries.**

- [x] **Step 4: Regenerate `repo-index/repo-index.json` from the updated generator and confirm the output order still matches the protected marketplace registry.**

### Task 3: Validate the metadata-driven path and publish the branch

**Files:**
- Modify: `docs/superpowers/plans/2026-06-19-mark-260-make-plugin-onboarding-generation-metadata-driven.md`

- [x] **Step 1: Mark completed plan steps as `[x]` and record any intentionally deferred follow-up in the plan text itself.**

- [x] **Step 2: Run the repo validation ladder: `py -3 tools/generate_marketplace.py`, `py -3 tools/generate_repo_index.py`, `py -3 tools/update_skill_artifacts.py --all`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_skill_zips.py`, and `git diff --check`.**

- [ ] **Step 3: Commit, push, and open a draft PR on `harleydbartles/mark-260-make-plugin-onboarding-generation-metadata-driven` with the changed files and validation evidence attached.**

### Non-goals

- Do not weaken protected plugin-root validation.
- Do not rewrite the whole marketplace generation stack.
- Do not hand-edit generated registries or skill zips outside the normal tooling path.
