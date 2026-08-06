# Validate projection contracts and licensing provenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tighten the marketplace validators so projected skills and bundles must carry explicit provenance, authorship, and agent-config metadata instead of relying on implicit repository convention.

**Architecture:** Keep the current marketplace layout and generated surfaces intact, but move the enforcement into reusable validator helpers that check skill frontmatter, `agents/openai.yaml`, and bundle-manifest `repo_index` metadata against the current projection contract. Favor narrow schema checks that match the repo's existing projection patterns so the validators catch drift without requiring a marketplace rewrite.

**Tech Stack:** Python 3, JSON, YAML, pytest/unittest, existing marketplace generation and validation scripts.

---

### Task 1: Harden skill and agent metadata validation

**Files:**
- Modify: `tools/skill_zip_artifacts.py`
- Modify: `tools/skill_overlay_materializer.py`
- Modify: `.agents/docs/contracts/openai-agent-yaml.md`
- Modify: `tests/test_skill_overlay_materializer.py`
- Modify: `tests/test_validate_marketplace.py`

- [x] **Step 1: Extend `validate_skill_markdown_frontmatter` so projected `SKILL.md` files must keep structured metadata instead of only `name` and `description`.**

```python
metadata = parsed_frontmatter.get("metadata")
if not isinstance(metadata, dict):
    raise ValueError(f"{skill_md} frontmatter metadata must be a mapping")
```

- [x] **Step 2: Add focused checks for the projection metadata keys already used in this repo, including `source_category`, `upstream_name`, `upstream_version`, `adaptation_overlay`, `projection_plugin`, `source-id`, `source-path`, `provenance-name`, `origin`, `content_mode`, `source_author`, `source_license`, and `adapted_author` when those fields are present.**

```python
if metadata.get("content_mode") == "adapted":
    for field in ("source_path", "source_author", "source_license", "adapted_author"):
        if not isinstance(metadata.get(field), str) or not metadata.get(field).strip():
            raise ValueError(f"{skill_md} metadata {field} must be a nonblank string for adapted projections")
```

- [x] **Step 3: Expand `validate_openai_agent_yaml` so `agents/openai.yaml` must support the richer Codex metadata pattern used in the repo, including `version`, `metadata`, optional `interface`, optional `policy`, and optional tool `dependencies`.**

```python
interface = parsed.get("interface")
if interface is not None and not isinstance(interface, dict):
    raise ValueError(f"{agent_yaml_path} interface must be a mapping when present")
policy = parsed.get("policy")
if policy is not None and not isinstance(policy, dict):
    raise ValueError(f"{agent_yaml_path} policy must be a mapping when present")
```

- [x] **Step 4: Update the OpenAI agent contract doc to describe the validated fields and the repo's two observed patterns: light projection metadata and richer Codex UI/policy metadata.**

### Task 2: Enforce bundle provenance and repo-index contract shape

**Files:**
- Modify: `tools/validate_marketplace.py`
- Modify: `tests/test_validate_marketplace.py`
- Modify: `tools/generate_repo_index.py` if the validator exposes a missing `repo_index` field that the generator currently tolerates

- [x] **Step 1: Add a reusable helper that validates bundle-manifest `repo_index` metadata for projected packs.**

```python
def _validate_repo_index_metadata(repo_index: dict, *, plugin_root: str) -> None:
    if not isinstance(repo_index.get("source_ledger", []), list):
        raise ValueError(f"{plugin_root} repo_index source_ledger must be a list")
```

- [x] **Step 2: Require explicit provenance fields on bundle entries so verbatim projections retain source author/license/source and adapted projections also declare repo adaptation authorship.**

```python
if content_mode == "verbatim":
    for field in ("source_author", "source_license", "source_path"):
        if not isinstance(entry.get(field), str) or not entry.get(field).strip():
            raise ValueError(f"{bundle_name} entry {canonical_name} must declare {field}")
```

- [x] **Step 3: No-op for the no-clobber / `everything-codex-code` guard.** The repo does not contain a live `everything-codex-code` projection surface, so there is nothing to guard in this branch; evidence: `rg -n "everything-codex-code|no-clobber|protected-root|clobber" tools docs tests codex-marketplace sources -g '!**/node_modules/**'` returned only the plan and implementation-record references.

```python
if plugin_root.name == "everything-codex-code":
    # Mirror only eligible code-facing skills; never the full raw ECC snapshot.
    ...
```

- [x] **Step 4: Add or update regression tests that prove the validator accepts the current Superpowers+/ECC projections and rejects missing provenance or malformed `repo_index` metadata.**

### Task 3: Regenerate evidence, update the implementation record, and close out publication

**Files:**
- Modify: `docs/superpowers/records/2026-06-19-mark-258-validate-projection-contracts-and-licensing-provenance.md`
- Modify: `repo-index/repo-index.json` if regeneration changes it
- Modify: `generated/skill-zips/registry.json` only through the normal generator path if it changes

- [x] **Step 1: Mark the completed plan steps with `[x]` and record any remaining ambiguity directly in the plan or implementation record.**

- [x] **Step 2: Run the repo validation ladder required by the issue.**

```powershell
py -3 tools/update_skill_artifacts.py --all
py -3 tools/generate_marketplace.py
py -3 tools/generate_repo_index.py
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
git diff --check
```

- [x] **Step 3: Update the MARK-258 implementation record, commit, push the branch, and open a draft PR on `harleydbartles/mark-258-validate-projection-contracts-and-licensing-provenance`.**

### Non-goals

- Do not broaden into a marketplace reshuffle.
- Do not hand-edit generated zips or registries outside the normal tooling path.
- Do not invent a new projection surface for `everything-codex-code` if the repo does not already contain one; record that as a blocker instead.
