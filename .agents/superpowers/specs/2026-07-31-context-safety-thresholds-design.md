# Context Safety Threshold Update

## Problem

The `context-safety` skill was introduced to protect against large inline text writes that could exhaust the remaining session context and cause OOMs. Since the recent Devin Desktop update, that OOM failure mode is now extremely rare. The current 200-line target / 400-line hard ceiling / 256 KB byte trigger fires too often for ordinary writes, causing unnecessary chunking and subagent dispatch.

## Goals

1. Keep the `context-safety` skill active for genuinely large writes.
2. Raise the line and byte thresholds so it fires only when a write is actually context-risky.
3. Remove the session-accumulation trigger; fire on the current write size only.
4. Refresh the skill's description, trigger metadata, and `agents/openai.yaml` so no surface still advertises the old 200-line limit.

## Constraints

- Source of truth: `sources/first_party/skills/context-safety/SKILL.md` and `sources/first_party/skills/context-safety/agents/openai.yaml`.
- Do not hand-edit generated projection files under `.agents/skills/context-safety/`; regenerate from source.
- Keep canonical identity fields stable (`name`, `source-id`, `source-path`, `provenance-name`, `source-category`, `status`, `owner`).
- Follow the skill-standards policy: descriptions and `use_when` describe triggers, not workflow.

## Changes

### `SKILL.md` body

- Update the top-line threshold tag to: "target 2,000 lines per chunk. absolute red limit max 4,000 lines per chunk."
- In `Pre-composition context pressure`, remove the trigger based on accumulated session context. The skill now fires when the current write itself exceeds the threshold.
- In `Large-write threshold`, update the size gates:
  - more than 2,000 lines;
  - more than 1 MB of UTF-8 text.
- Keep the hard-ceiling rule: split any chunk that would exceed 4,000 lines.
- Update the early-split cue and any 300-line references to a value that gives room under the new target, e.g., 1,500 lines.
- Update the Python pattern to use new constants `TARGET_LINES = 2000`, `HARD_LIMIT = 4000`, and `LARGE_BYTES = 1_000_000`, and adjust the helper logic accordingly.
- Update the `Decision test` and any remaining 200/400/256 KB cross-references.

### `SKILL.md` frontmatter

- `description`: remove the "200-line chunking" workflow summary. Focus on the symptom: "Use when very large or context-heavy text writes need bounded composition, deliberate compaction boundaries, and atomic replacement. Use when a write may exceed the safe threshold or when inline composition risks exhausting context."
- `scope`: "very large text write safety, bounded composition, compaction boundaries, and atomic replacement."
- `use_when`: rephrase triggers to mention "very large" writes, the 2,000-line cue, and the 1 MB byte cue.
- `do_not_use_when`: keep the exclusion for small, direct writes.

### `agents/openai.yaml`

- `interface.short_description`: align with the new `description`.
- `interface.default_prompt`: replace 200/400/256 KB references with 2,000/4,000/1 MB.

## Proposed final frontmatter

### `SKILL.md` frontmatter

- `description`: `Use when a text write is expected to exceed the safe threshold for the remaining session context, when a document is very large or context-heavy, or when a normal editor write path would be brittle.`
- `scope`: `very large text write safety, bounded composition, compaction boundaries, and atomic replacement.`
- `use_when`:
  - `Use when a text write is expected to exceed 2,000 lines or 1 MB of UTF-8 text.`
  - `Use when inline composition would risk consuming the remaining session context.`
  - `Use when safe staging and atomic replacement are required for a large text write.`
  - `Use when /compact should happen only after durable state has been preserved.`
- `do_not_use_when`:
  - `Do not use when the change is small and can be written directly.`
  - `Do not use when the task is unrelated to large or context-heavy text writes.`

### `agents/openai.yaml`

```yaml
interface:
  short_description: Use when a text write is expected to exceed the safe threshold, when a document is very large or context-heavy, or when a normal editor write path would be brittle.
  default_prompt: Use /context-safety when a text write is expected to exceed the safe threshold, when inline composition itself would risk consuming the remaining context, or when tool-call boundaries should be used as checkpoints. Estimate line count and byte size before writing, treat 2,000 lines per chunk as the target and 4,000 lines per chunk as the absolute red limit, split writes expected to land around 1,500 lines or more into smaller chunks before composing, preserve durable state before /compact, use a clean-context worker/subagent or bounded append path for risky writes, validate the completed temp file, and atomically replace the target only after validation.
```

## Verification

1. Run `python tools/normalize_first_party_skill_sources.py` to normalize the first-party source.
2. Run `.\tools\run.ps1 marketplace --apply` to regenerate projections and the installed skill.
3. Run `.\tools\run.ps1 ci --check` on the committed/staged tree as the final green proof.
4. If pre-commit hooks run `ci --check`, let them execute; otherwise commit and run the CI check manually.

## Out of scope

- No new metadata fields are added, so the `normalize_first_party_skill_sources.py` whitelist does not need updating.
- The skill is not retired or renamed.