# mdformat-safe-link-labels

This marketplace package provides the `safe-link-labels` mdformat extension used by the `markdown-formatting` skill. Keep it separate from skill source: consumers install the wheel through their pinned `marketplace-source` submodule.

## Build the wheel

Run:

```text
python build_wheel.py
```

The build script copies the package source to a temporary directory and writes the resulting wheel under `wheels/`. This keeps setuptools metadata and build output out of the marketplace checkout. When changing the package version, update the skill's requirements path and expected distribution version in `format_markdown.py` in the same change.
