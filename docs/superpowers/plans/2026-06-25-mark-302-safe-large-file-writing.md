# MARK-302 safe-large-file-writing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an installable first-party `safe-large-file-writing` skill that keeps Devin/Desktop agents off the interactive editor OOM path for large text writes.

**Architecture:** Put the authoritative skill body in first-party source custody under `sources/first_party/skills/safe-large-file-writing/`. Project that source into the first-party `house-skills` marketplace surface and its generated `skill.zip` / registry outputs by updating the source-ledger entries and regenerating the bundle manifest, source map, provenance, and zip surfaces through the repo generators. Keep the content compact and operational: detect likely large writes first, route to script/CLI/temp-file/atomic-replace flows, validate size and line count before swap, and keep Windows/Python examples in the skill itself.

**Tech Stack:** Markdown skill source, YAML agent metadata, JSON ledgers/manifests, Python generator/validation scripts, generated `skill.zip` artifacts, PowerShell/Python execution examples.

## Global Constraints

- Use the fresh `origin/main` base and keep the isolated `.worktrees/` checkout as the only edit surface.
- Do not add repo-local instruction files as the primary solution; the durable fix is a first-party marketplace skill.
- Keep the skill compact and practical; this is a behavior guardrail, not a long-form essay.
- Keep any single large text write under 500 lines per manual edit.
- The first-party source is authoritative; generated marketplace/projection/zip surfaces are downstream outputs.
- Preflight note: `py -3 tools/validate_marketplace.py` currently fails in this worktree on a pre-existing missing `adventures-pack` asset at `codex-marketplace/plugins/adventures-pack/skills/adventures-asset-sheet-compiler/assets/templates/template_asset_sheet_3hero_6alt_v4.png`; do not widen MARK-302 to fix that unrelated surface unless future validation requires it.

---

### Task 1: Author the first-party source skill

**Files:**
- Create: `sources/first_party/skills/safe-large-file-writing/SKILL.md`
- Create: `sources/first_party/skills/safe-large-file-writing/agents/openai.yaml`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `sources/first_party/skills/house-skills/decisions.md`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `provenance/house-skills.md`

**Interfaces:**
- Consumes: `/using-superpowers`, `/writing-skills`, `/inspecting-the-environment`, `/connector-safety`
- Produces: a first-party source skill with metadata that triggers on large writes and recommends temp-file/atomic-replace workflows.

- [ ] **Step 1: Write the skill body**

Add `SKILL.md` with explicit trigger language for creating, replacing, appending, regenerating, or substantially editing large text files. Keep the core behavior narrow:

```markdown
## Core behavior

- Estimate whether a write will exceed the safe threshold before editing.
- Avoid whole-file editor replacement for large text files.
- Avoid sending 300+ lines as one editor edit.
- Use a script, CLI write, shell redirection, or chunked append path instead.
- Write to a temporary file first.
- Validate byte size and line count before replacement.
- Atomically replace the target only after validation.
- Prefer localized patches for large existing source files.
- Avoid opening generated large files in the editor unless review is required.
- Stop retrying editor writes after memory pressure and switch to the safe write path.
```

- [ ] **Step 2: Include Windows-friendly safe-write examples**

Show a Python temp-file pattern the worker can copy without guessing:

```python
from pathlib import Path

target = Path("output.md")
tmp = target.with_suffix(target.suffix + ".tmp")
payload = "# content\n"

tmp.write_text(payload, encoding="utf-8", newline="\n")
if len(payload.splitlines()) > 300 or tmp.stat().st_size > 256_000:
    raise RuntimeError("switch to a safer chunked write path")
tmp.replace(target)
```

Add a short PowerShell example only if it keeps the skill usable on Windows without turning the skill into a shell cookbook.

- [ ] **Step 3: Add the installable metadata file**

Create `agents/openai.yaml` with the display name, a short description that points at safe large-file writes, and a default prompt that tells the agent to choose script/CLI/temp-file workflows instead of interactive editor replacement when the write is large.

- [ ] **Step 4: Register the source in the house-skills ledgers**

Append the new source root to the house-skills decision/intake/provenance records so validation can see the canonical source path as first-party Harley-owned source custody for large-file write safety.

### Task 2: Project the skill and regenerate the marketplace outputs

**Files:**
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/SKILL.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/agents/openai.yaml`
- Regenerated: `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip`
- Regenerated: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the source skill from Task 1 and the current `house-skills` bundle manifest.
- Produces: installable `house-skills` projections and the corresponding generated skill zip / registry entries.

- [ ] **Step 1: Materialize the House Skills projection**

Run:

```bash
py -3 tools/update_skill_artifacts.py --skill house-skills/safe-large-file-writing
```

Expected: the `house-skills` projection surface and `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip` are refreshed from source custody, not hand-copied.

- [ ] **Step 2: Review the generated surfaces**

Confirm the regenerated `house-skills` bundle manifest, source map, and zip registry show only the new `safe-large-file-writing` entries plus the mechanical projection outputs. Do not broaden the diff into unrelated bundle churn.

### Task 3: Publish the plan branch and wait for approval

**Files:**
- No new files; the plan branch is already published as a draft PR and now serves as the approval gate.

**Interfaces:**
- Consumes: the plan document and the draft PR on this branch.
- Produces: an approved execution gate for the implementation tasks below.

- [ ] **Step 1: Keep the plan-only PR open**

Do not start implementation until approval lands. The existing draft PR is the publication surface for this plan-only handoff.

- [ ] **Step 2: Record the pre-implementation baseline**

Note the known unrelated `adventures-pack` asset gap if it is still present. That blocker stays outside MARK-302 unless a later validation step proves it must be resolved first.

### Task 4: Implement the skill and finish the branch

**Files:**
- Create: `sources/first_party/skills/safe-large-file-writing/SKILL.md`
- Create: `sources/first_party/skills/safe-large-file-writing/agents/openai.yaml`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `sources/first_party/skills/house-skills/decisions.md`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `provenance/house-skills.md`
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/SKILL.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/agents/openai.yaml`
- Regenerated: `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip`
- Regenerated: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the approved plan, the source skill edits from Task 1, and the `house-skills` projection surfaces.
- Produces: an installable first-party skill in `house-skills`, generated zip/registry updates, and implementation evidence for MARK-302 closeout.

- [ ] **Step 1: Write the safe branching pattern into the skill**

Use a branching-first pattern that estimates size before writing and only chooses a simple temp-file path for small payloads:

```python
from pathlib import Path

def iter_text_chunks(text: str, chunk_size: int = 8_192):
    for start in range(0, len(text), chunk_size):
        yield text[start:start + chunk_size]

def write_large_text(target: Path, text: str) -> None:
    lines = text.splitlines()
    byte_size = len(text.encode("utf-8"))
    is_large = len(lines) > 300 or byte_size > 256_000

    tmp = target.with_suffix(target.suffix + ".tmp")

    if is_large:
        with tmp.open("w", encoding="utf-8", newline="\n") as handle:
            for chunk in iter_text_chunks(text, chunk_size=8_192):
                handle.write(chunk)
    else:
        tmp.write_text(text, encoding="utf-8", newline="\n")

    completed = tmp.read_text(encoding="utf-8")
    if completed != text:
        raise RuntimeError("temp file validation failed")
    if len(completed.splitlines()) != len(lines) or tmp.stat().st_size != byte_size:
        raise RuntimeError("validated size mismatch")

    tmp.replace(target)
```

Keep the helper small and explicit. The point is to branch before the write path, not to build a general-purpose file writer.

- [ ] **Step 2: Regenerate the `house-skills` projection**

Run:

```bash
py -3 tools/update_skill_artifacts.py --skill house-skills/safe-large-file-writing
```

Expected: the `house-skills` source-backed projection and `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip` are regenerated from the edited source.

- [ ] **Step 3: Run the full implementation validation ladder**

Run:

```bash
py -3 tools/materialize_projection.py --check
py -3 tools/update_skill_artifacts.py --check
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/validate_marketplace.py
git diff --check
```

Treat the checks as follows:

- `materialize_projection.py --check` proves the projection matches the source and manifest shape.
- `update_skill_artifacts.py --check` proves the generated skill zip registry is consistent for the updated skill surface.
- `generate_marketplace.py --check` and `generate_repo_index.py --check` prove the marketplace and repo index surfaces are current.
- `validate_marketplace.py` proves the repository-wide marketplace invariants.
- `git diff --check` catches whitespace and patch-shape issues.
- If `validate_marketplace.py` still fails on the pre-existing `adventures-pack` asset gap, record that as a baseline blocker and keep MARK-302 scoped to the skill work.

- [ ] **Step 4: Commit the implementation**

Commit the implemented skill source, the `house-skills` projection updates, and the generated skill zip / registry outputs in a focused MARK-302 commit.

- [ ] **Step 5: Push the updated branch and update the PR**

Push the updated branch and update the existing PR so it now carries the implementation diff and validation evidence. Do not open a second PR.

### Coverage Check

- Source skill and metadata: Task 1
- Marketplace projections and generated zips: Task 2 and Task 4
- Approval gate: Task 3
- Validation and publication proof: Task 4 and Task 5
- Known unrelated baseline blocker: pre-existing `adventures-pack` validation failure noted above
