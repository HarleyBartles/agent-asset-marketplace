# Safe Markdown Link Labels Implementation Plan

**State:** completed-awaiting-retirement

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task by task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Make generated index links with safe literal underscores pass generation and Markdown formatting checks without changing their labels or targets.

**Architecture:** Keep the portable formatter as the owner of normalization. Replace or extend its pinned renderer through a supported, distributable mechanism that preserves literal underscores only where the parsed Markdown meaning is unchanged. Exercise the canonical index producer against that formatter, including its explicit `--check-files` boundary.

**Tech Stack:** Python, mdformat, markdown-it-py, pytest, marketplace skill projections.

**Spec:** The Rooms-Mostly agent letter and the approved direction in this task; the existing portable contract is `codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/SKILL.md`.

**Execution Strategy:** `executing-plans`, because renderer selection, the formatter contract, and generator integration depend on one sequential design decision.

## Global Constraints

- Edit canonical skill source under `codex-marketplace/plugins/`; regenerate `.agents/skills/` through the repository commands.
- Preserve GFM, frontmatter, validation, LF output, and the existing file selection and exclusion contract.
- Keep `--check-files` checking every requested producer output, including untracked files.
- Do not add a Rooms filename rule, blanket underscore unescaping, generator emitted escapes, or an exclusion for generated indexes.
- Use a focused RED/GREEN behavior test and meaningful producer integration. Avoid tests that merely compare mirrored implementation strings.
- Publish implementation through a Draft PR to `main`; the tracked pre-commit hook owns the full staged gate.

## Review Focus

- A double underscore inside a filename label remains literal and links to the intended file.
- Underscores that can create emphasis remain protected and render with the same structure.
- Already escaped labels keep their rendered meaning; safe plain-text escapes may normalize to literal underscores. Code spans and non-label Markdown keep their intended output.
- A second generator run and formatter check both accept the same source bytes.

______________________________________________________________________

### Task 1: Establish the formatter behavior and implementation seam

**Files:**

- Modify: `codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/tests/test_format_markdown.py`
- Modify: `tests/test_markdown_format.py` only if the repository-level command needs direct coverage
- Create or modify: a focused renderer integration module under the canonical `markdown-formatting` skill, if needed
- Modify: the canonical skill's `requirements.txt`, `SKILL.md`, and any formatter config template only if the selected mechanism requires it

**Interfaces:**

- Consumes: `format_markdown.py` CLI and its pinned mdformat toolchain.

- Produces: one reproducible formatter command that accepts safe literal link-label underscores and preserves parsed meaning.

- [x] Add a real fixture containing `- [absynth_lover__seegreenfairies](absynth_lover__seegreenfairies.md)` and a target file. Assert the CLI `--check-files` accepts the literal source, `--apply` leaves it literal, and a second check succeeds. Assert the current pin fails before implementation.

- [x] Add a contrasting fixture where unescaped underscores alter emphasis parsing. Compare parsed token structure and link destination before and after formatting; require semantic preservation rather than a regex-only assertion.

- [x] Inspect mdformat's documented renderer/plugin extension API and the installed `escape_underscore_emphasis` call site. Select a supported extension or maintained pinned formatter build; do not monkeypatch private installed package files at runtime. Record the chosen seam and version or package provenance in the skill documentation.

- [x] Implement the smallest formatter-level change and rerun the focused tests. Confirm the ordinary prose, list, GFM, and frontmatter behavior already covered by the skill tests still passes.

### Task 2: Prove producer and formatter convergence

**Files:**

- Modify: `tests/test_generate_index_mesh.py`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/generating-agent-mesh/scripts/generate_index_mesh.py` only if a genuine producer defect appears; retain literal labels

**Interfaces:**

- Consumes: Task 1's formatter invocation through `--check-files`.

- Produces: a generated index whose source is accepted unchanged by generation and formatting checks.

- [x] In a temporary consumer repository, track a file named `absynth_lover__seegreenfairies.md`, enable the formatting contract, install the canonical skills and pinned requirements, and run the real index generator. Assert the generated link label and target are literal and correct.

- [x] Run generator `--check`, formatter `--check-files` on the index, formatter repository `--check`, and generator `--check` again. Compare index bytes before and after; all commands must pass without source churn.

- [x] Confirm the generator still reports a deliberately malformed or stale index; the integration must not bypass either check.

### Task 3: Regenerate, validate, and publish

**Files:**

- Regenerate: `.agents/skills/markdown-formatting/` and relevant marketplace/mesh outputs through their owning commands
- Update: this plan's checkboxes and completion state at the end of implementation

**Interfaces:**

- Consumes: Tasks 1 and 2.

- Produces: a reviewable Draft PR with the canonical source, generated projection, focused evidence, and hook proof.

- [x] Run the focused skill and generator tests, then `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py mesh --apply`; inspect the diff for unrelated generated changes.

- [x] Stage the intended tree and commit normally so the tracked pre-commit hook runs its staged apply/check gate. Do not run a redundant canonical check immediately before or after that commit.

- [x] Review the committed diff and obtain a fresh code review. Correct findings and repeat review on the latest commit.

- [ ] Use `completing-planning-artifacts` to promote any enduring decision, mark this plan `completed-awaiting-retirement`, and commit it. Push the branch, open a Draft PR to `main`, and verify its head and checks in GitHub.
