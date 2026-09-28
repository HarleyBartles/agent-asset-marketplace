# mdformat-safe-link-labels

This source package provides the `safe-link-labels` mdformat extension used by the `markdown-formatting` skill. Its build writes a wheel to `dist/wheels/`.

## Build the wheel

Run `py -3 src/packages/mdformat-safe-link-labels/build_wheel.py` from the repository root. The script builds from a temporary copy so source stays free of setuptools output. When changing the package version, update the skill requirement and expected distribution version together.
