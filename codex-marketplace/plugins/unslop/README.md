# Unslop

Asset Marketplace-owned package for generating domain-specific anti-slop profiles from local samples.

- Upstream basis: `mshumer/unslop`
- Upstream commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- Declared upstream license: `MIT`
- Runtime shape: bundled Python scripts, no source-fetch step, no Anthropic CLI dependency

Text mode runs with Python standard library only. Visual mode first checks for the Playwright Python package and a Chromium-compatible executable; if either is unavailable, the run continues and records visual evidence as skipped in `manifest.json` and `validation.md`.

Codex installs this package through `.codex-plugin/plugin.json`. GPT skill installs use `skills/unslop/` directly.
