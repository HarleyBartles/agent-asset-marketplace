---
name: unslop
description: Generate a domain-specific anti-slop profile from local GPT/Codex samples, validate that the analysis is concrete, and record optional visual evidence status without external source fetching or provider-specific CLI dependencies.
metadata:
  content_mode: adapted
  source_author: Harley Bartles
  source_license: MIT
  source_repo: https://github.com/HarleyBartles/agent-asset-marketplace
  source_path: sources/first_party/skills/unslop/SKILL.md
  adapted_author: Harley Bartles
---

# Unslop

Use this skill when a user wants a reusable profile that identifies repetitive AI defaults for a domain and turns those findings into instructions for what to avoid.

## Workflow

1. Decide the domain and whether the run is `text` or `visual`.
2. Create or collect representative samples for the same domain.
   - For GPT-only use, ask the model to produce samples and save each response as a `.txt` or `.md` file.
   - For Codex use, save sample files in a working directory or pass short samples with repeated `--sample` flags.
3. Run the bundled script from the skill package:

```bash
python3 scripts/unslop.py --domain "<domain>" --samples-dir ./samples --output ./unslop-output
```

For a visual run, pass HTML samples and request optional visual evidence:

```bash
python3 scripts/unslop.py --domain "<domain>" --type visual --samples-dir ./samples --output ./unslop-output
```

4. Validate the generated profile:

```bash
python3 scripts/validate_unslop_output.py ./unslop-output
```

5. Review `unslop-output/analysis.md`, then treat `unslop-output/skill.md` as a draft profile until it is checked for domain fit.

## Sample Collection

Text mode does not need Playwright. If no samples are ready yet, generate prompts first:

```bash
python3 scripts/unslop.py --domain "<domain>" --count 12 --prompts-only --output ./unslop-output
```

Use `unslop-output/prompts.json` as the task list, save model responses into a sample directory, then rerun with `--samples-dir`.

For quick smoke validation of the package itself, use:

```bash
python3 scripts/unslop.py --domain "release note writing" --fixture-samples --output ./unslop-output
```

If you only need prompts, add `--prompts-only`; that mode writes `prompts.json` plus a manifest with the `unslop-prompts-only/v1` contract instead of the full analysis bundle.
When reusing an existing output directory, add `--force-cleanup` so the script can clear it safely.

## Output Review

- `analysis.md` must include counts, concrete repeated patterns, and language tied to the requested domain.
- `skill.md` should mostly prohibit observed defaults. It should not merely prescribe a new generic house style.
- `manifest.json` must record run parameters, sample counts, tool version, upstream provenance, provider/orchestration mode, validation status, and optional visual evidence status.
- Prompts-only runs are intentionally non-validated and only guarantee `manifest.json` and `prompts.json`.
- `validation.md` should state whether visual evidence ran or was skipped.

## Visual Dependency Handling

Visual mode first checks for the Python Playwright package and a Chromium-compatible executable. If either is missing, the run still produces text/domain outputs and records visual evidence as skipped. Do not vendor browser binaries into the skill package.

## Deliverable

Return the generated `skill.md`, the main repeated patterns found, the `manifest.json` path, validation results, and whether visual evidence ran or was skipped.
