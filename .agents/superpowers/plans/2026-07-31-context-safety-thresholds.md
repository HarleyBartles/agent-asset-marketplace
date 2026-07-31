# context-safety Threshold Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `sources/first_party/skills/context-safety/` so the skill only fires for truly large writes (2,000 lines / 1 MB), removes the session-accumulation trigger, and refreshes all skill-facing text.

**Architecture:** Edit the canonical first-party source (`SKILL.md` + `agents/openai.yaml`), then run the first-party source normalizer and the `marketplace` regeneration target to update all derived surfaces, and finish with the full `ci` gate.

**Tech Stack:** Markdown, YAML, `tools/normalize_first_party_skill_sources.py`, `tools/run.ps1` on Windows, git.

## Global Constraints

- Source of truth: `sources/first_party/skills/context-safety/SKILL.md` and `sources/first_party/skills/context-safety/agents/openai.yaml`.
- Do not hand-edit generated projection files under `.agents/skills/context-safety/`; regenerate from source.
- Keep canonical identity fields stable (`name`, `source-id`, `source-path`, `provenance-name`, `source-category`, `status`, `owner`).
- Follow `docs/skill-standards-policy.md`: descriptions and `use_when` describe triggers, not workflow.
- All generated surfaces stay in sync with canonical source.
- All commands assume the worktree root as the working directory, except where a command explicitly references an absolute path.

---

### Task 1: Update `SKILL.md` frontmatter

**Files:**
- Modify: `sources/first_party/skills/context-safety/SKILL.md` (frontmatter only)
- Test: `python -c` in-line checks

**Interfaces:**
- Consumes: the spec's proposed final frontmatter
- Produces: a `SKILL.md` frontmatter that no longer mentions 200-line chunking

- [x] **Step 1: Write the failing test**

Run:
```powershell
python -c "import pathlib; text = pathlib.Path('sources/first_party/skills/context-safety/SKILL.md').read_text(); assert '200-line chunking' not in text, 'description still references 200-line chunking'; assert 'very large' in text, 'description does not mention very large'; print('frontmatter clean')"
```
Expected: FAIL

- [x] **Step 2: Update the frontmatter fields**

Replace the top-level `description` and these three `metadata` fields in `sources/first_party/skills/context-safety/SKILL.md`, leaving the canonical identity fields and `license` unchanged:

```yaml
description: Use when a text write is expected to exceed the safe threshold for the
  remaining session context, when a document is very large or context-heavy, or when
  a normal editor write path would be brittle.
scope: very large text write safety, bounded composition, compaction boundaries, and atomic replacement.
use_when:
  - Use when a text write is expected to exceed 2,000 lines or 1 MB of UTF-8 text.
  - Use when inline composition would risk consuming the remaining session context.
  - Use when safe staging and atomic replacement are required for a large text write.
  - Use when `/compact` should happen only after durable state has been preserved.
do_not_use_when:
  - Do not use when the change is small and can be written directly.
  - Do not use when the task is unrelated to large or context-heavy text writes.
```

The `description` key is at the top level of the YAML frontmatter; `scope`, `use_when`, and `do_not_use_when` belong under `metadata:`.

- [x] **Step 3: Run the test to verify it passes**

Same command as Step 1. Expected: PASS.

- [x] **Step 4: Normalize the source**

Run:
```powershell
py -3 tools/normalize_first_party_skill_sources.py
```
Expected: clean exit (it may rewrite the file with canonical field ordering/whitespace; if so, review the diff).

- [x] **Step 5: Commit**

```powershell
git add sources/first_party/skills/context-safety/SKILL.md
git commit -m "Update context-safety frontmatter for 2k/1MB thresholds"
```

**Mark this task's steps `[x]`**

In `.agents/superpowers/plans/2026-07-31-context-safety-thresholds.md`, replace `[ ]` with `[x]` for every step in this task, then report the task as complete.

---

### Task 2: Update `SKILL.md` body thresholds and remove session-context trigger

**Files:**
- Modify: `sources/first_party/skills/context-safety/SKILL.md` (body)
- Test: `python -c` in-line checks

**Interfaces:**
- Consumes: the new frontmatter (Task 1)
- Produces: a `SKILL.md` body that uses the new thresholds and only size-based triggers

- [x] **Step 1: Write the failing test**

Run:
```powershell
python -c "import pathlib; text = pathlib.Path('sources/first_party/skills/context-safety/SKILL.md').read_text(); assert 'target 2,000 lines per chunk' in text, 'missing 2,000 target'; assert 'more than 1 MB' in text, 'missing 1 MB threshold'; assert 'the session has already accumulated significant subagent output' not in text, 'session trigger not removed'; print('body thresholds updated')"
```
Expected: FAIL

- [x] **Step 2: Update the threshold text**

Make the following in-place edits in `SKILL.md`:

1. Replace the top-level tag:
   - Old: `target 200 lines per chunk. absolute red limit max 400 lines per chunk.`
   - New: `target 2,000 lines per chunk. absolute red limit max 4,000 lines per chunk.`

2. Replace `Pre-composition context pressure` section with a section that only uses the current write size:

```markdown
## Pre-composition context pressure

Before composing a large document, decide whether the composition itself will exceed the safe threshold.

Treat a write as context-risky when either of these is true:

- the output is likely to exceed about 2,000 lines;
- the output is likely to exceed about 1 MB of UTF-8 text.

When context-risky:

1. Do not compose the whole document as one inline string in the main session.
2. Prefer a clean-context worker/subagent write with only the required inputs.
3. Or generate the document in bounded sections with sequential append calls, keeping each section near the 2,000-line target and well below the 4,000-line ceiling.
4. Still apply the existing chunked/temp-file write mechanics inside the chosen path.

If the output is expected to land around 1,500 lines or more, split it into smaller chunks before starting so the chunks stay under the target and comfortably below the limit.
```

3. Replace `Large-write threshold` bullets:
   - Old: `more than 200 lines;` and `more than 256 KB of UTF-8 text.`
   - New: `more than 2,000 lines;` and `more than 1 MB of UTF-8 text.`

4. Update the rest of the body to replace `400` hard-ceiling, `300` early-split, and `256 KB` references with `4,000`, `1,500`, and `1 MB` respectively.

- [x] **Step 3: Run the test to verify it passes**

Same command as Step 1. Expected: PASS.

- [x] **Step 4: Commit**

```powershell
git add sources/first_party/skills/context-safety/SKILL.md
git commit -m "Raise context-safety body thresholds to 2k/1MB and drop session trigger"
```

**Mark this task's steps `[x]`**

In `.agents/superpowers/plans/2026-07-31-context-safety-thresholds.md`, replace `[ ]` with `[x]` for every step in this task, then report the task as complete.

---

### Task 3: Update the Python pattern in `SKILL.md`

**Files:**
- Modify: `sources/first_party/skills/context-safety/SKILL.md` (Python code block)
- Test: `python -c` in-line checks

**Interfaces:**
- Consumes: the new body thresholds (Task 2)
- Produces: a `SKILL.md` Python example that reflects the new constants

- [x] **Step 1: Write the failing test**

Run:
```powershell
python -c "import pathlib; text = pathlib.Path('sources/first_party/skills/context-safety/SKILL.md').read_text(); assert 'TARGET_LINES = 2000' in text, 'missing TARGET_LINES 2000'; assert 'HARD_LIMIT = 4000' in text, 'missing HARD_LIMIT 4000'; assert 'LARGE_BYTES = 1_000_000' in text, 'missing LARGE_BYTES 1_000_000'; assert 'def iter_line_chunks(lines: list[str], chunk_lines: int = 200)' not in text, 'old iter_line_chunks default still present'; print('python pattern updated')"
```
Expected: FAIL

- [x] **Step 2: Replace the Python pattern**

Replace the existing `## Python pattern` block with:

```python
TARGET_LINES = 2000
HARD_LIMIT = 4000
LARGE_BYTES = 1_000_000


def iter_line_chunks(lines: list[str], chunk_lines: int = TARGET_LINES):
    for start in range(0, len(lines), chunk_lines):
        yield lines[start:start + chunk_lines]


def write_large_text(target: Path, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    byte_size = len(text.encode("utf-8"))
    ends_with_newline = text.endswith("\n")
    chunk_lines = 1500 if len(lines) >= 3000 else TARGET_LINES if len(lines) > TARGET_LINES else len(lines)
    is_large = len(lines) > TARGET_LINES or byte_size > LARGE_BYTES

    tmp = target.with_suffix(target.suffix + ".tmp")

    if is_large:
        with tmp.open("w", encoding="utf-8", newline="\n") as handle:
            for chunk_index, chunk in enumerate(iter_line_chunks(lines, chunk_lines=chunk_lines)):
                if len(chunk) > HARD_LIMIT:
                    raise RuntimeError("chunk exceeds the absolute hard limit")
                handle.write("\n".join(chunk))
                is_last_chunk = chunk_index == ((len(lines) - 1) // chunk_lines)
                if not is_last_chunk or ends_with_newline:
                    handle.write("\n")
    else:
        with tmp.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)

    with tmp.open("r", encoding="utf-8", newline="\n") as handle:
        completed = handle.read()
    if completed != text:
        raise RuntimeError("temp file validation failed")
    if len(completed.splitlines()) != len(lines):
        raise RuntimeError("line count validation failed")
    if tmp.stat().st_size != byte_size:
        raise RuntimeError("byte size validation failed")

    tmp.replace(target)
```

- [x] **Step 3: Run the test to verify it passes**

Same command as Step 1. Expected: PASS.

- [x] **Step 4: Commit**

```powershell
git add sources/first_party/skills/context-safety/SKILL.md
git commit -m "Update context-safety Python pattern for 2k/1MB thresholds"
```

**Mark this task's steps `[x]`**

In `.agents/superpowers/plans/2026-07-31-context-safety-thresholds.md`, replace `[ ]` with `[x]` for every step in this task, then report the task as complete.

---

### Task 4: Update `agents/openai.yaml`

**Files:**
- Modify: `sources/first_party/skills/context-safety/agents/openai.yaml`
- Test: `python -c` in-line checks

**Interfaces:**
- Consumes: the new `SKILL.md` frontmatter (Task 1)
- Produces: the Codex-facing wrapper aligned with the new thresholds

- [x] **Step 1: Write the failing test**

Run:
```powershell
python -c "import pathlib; text = pathlib.Path('sources/first_party/skills/context-safety/agents/openai.yaml').read_text(); assert '2,000 lines per chunk' in text, 'missing 2,000 lines in openai.yaml'; assert '4,000 lines per chunk' in text, 'missing 4,000 lines in openai.yaml'; assert '1 MB' in text, 'missing 1 MB in openai.yaml'; assert '200-line chunking' not in text, 'old 200-line phrase still in openai.yaml'; print('openai.yaml updated')"
```
Expected: FAIL

- [x] **Step 2: Replace the file contents**

Write the full new `sources/first_party/skills/context-safety/agents/openai.yaml`:

```yaml
version: 1
metadata:
  skill_name: context-safety
  source_category: first_party

interface:
  display_name: Context Safety
  short_description: Use when a text write is expected to exceed the safe threshold, when a document is very large or context-heavy, or when a normal editor write path would be brittle.
  default_prompt: Use /context-safety when a text write is expected to exceed the safe threshold, when inline composition itself would risk consuming the remaining context, or when tool-call boundaries should be used as checkpoints. Estimate line count and byte size before writing, treat 2,000 lines per chunk as the target and 4,000 lines per chunk as the absolute red limit, split writes expected to land around 1,500 lines or more into smaller chunks before composing, preserve durable state before `/compact`, use a clean-context worker/subagent or bounded append path for risky writes, validate the completed temp file, and atomically replace the target only after validation.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
dependencies:
  tools: []
```

- [x] **Step 3: Run the test to verify it passes**

Same command as Step 1. Expected: PASS.

- [x] **Step 4: Commit**

```powershell
git add sources/first_party/skills/context-safety/agents/openai.yaml
git commit -m "Align context-safety openai.yaml with 2k/1MB thresholds"
```

**Mark this task's steps `[x]`**

In `.agents/superpowers/plans/2026-07-31-context-safety-thresholds.md`, replace `[ ]` with `[x]` for every step in this task, then report the task as complete.

---

### Task 5: Regenerate derived surfaces and run the full CI gate

**Files:**
- Generate: all derived marketplace, plugin, and installed-skill surfaces
- Test: `tools/run` CI gate

**Interfaces:**
- Consumes: the updated first-party source (Tasks 1-4)
- Produces: a passing `ci --check` and an in-sync repo

- [ ] **Step 1: Normalize first-party source**

Run:
```powershell
py -3 tools/normalize_first_party_skill_sources.py
```
Expected: clean exit. Review the diff; if it made changes, commit them as a fixup to the same task before proceeding.

- [ ] **Step 2: Regenerate all derived surfaces**

Run:
```powershell
.\tools\run.ps1 marketplace --apply
```
Expected: passes all targets and writes updated projections.

- [ ] **Step 3: Inspect and stage generated changes**

Run:
```powershell
git status --short
```
Expected: only generated surfaces related to `context-safety` and `repo-worker-pack` are modified, plus any index/mesh files. If unrelated files are dirty, stop and investigate before committing.

- [ ] **Step 4: Commit the regenerated surfaces (pre-commit hook will run `ci --check`)**

```powershell
git add .
git commit -m "Regenerate projections and mesh for context-safety threshold update"
```
Expected: the pre-commit hook runs `.	ools
un.ps1 ci --check` and the commit succeeds. If the hook is not present or is bypassed, run `.	ools
un.ps1 ci --check` immediately after the commit.

- [ ] **Step 5: Run the CI gate manually if the pre-commit hook did not run it**

Run:
```powershell
.\tools\run.ps1 ci --check
```
Expected: `all requested targets passed.`

**Mark this task's steps `[x]`**

In `.agents/superpowers/plans/2026-07-31-context-safety-thresholds.md`, replace `[ ]` with `[x]` for every step in Task 5, then report the task as complete.

---

## Self-review for the plan

1. **Spec coverage:** Every requirement in the spec (thresholds, trigger scope, frontmatter, openai.yaml, Python pattern, validation) maps to a task.
2. **Placeholder scan:** No `TBD`, `TODO`, or `implement later` remain. Each step has the exact text or command to run.
3. **Type consistency:** N/A — this is a documentation/skill source change; the only types are string constants.