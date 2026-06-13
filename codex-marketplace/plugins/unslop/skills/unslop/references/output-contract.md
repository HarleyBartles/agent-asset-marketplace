# Output Contract

Full runs write an `unslop-output/` directory unless `--output` selects another path.

```text
unslop-output/
  manifest.json
  prompts.json
  samples/
  analysis.md
  skill.md
  validation.md
  before-after/
```

`manifest.json` records the domain, run type, tool version, upstream provenance, provider/orchestration mode, sample counts, validation status, and optional visual evidence status.

`analysis.md` must contain counted, domain-specific repeated patterns. `skill.md` is a draft profile for review; it should mostly say what to avoid and should not be treated as install-ready until `validate_unslop_output.py` passes and a human or agent reviews the findings.

Prompt-generation runs use the `unslop-prompts-only/v1` contract and only guarantee `manifest.json` and `prompts.json`. They do not claim `analysis.md`, `skill.md`, `validation.md`, or `before-after/`.
