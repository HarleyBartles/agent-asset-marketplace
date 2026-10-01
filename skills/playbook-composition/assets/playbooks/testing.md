# Testing concern

Use this guidance whenever a change can affect observable behavior, regardless of which lifecycle stage is active.

Choose evidence that could reveal the defect the change might introduce. Prefer a focused behavior test for the changed contract, then run the repository's required broader gate. Include failure paths and boundaries when they matter. Avoid tests that only restate implementation details or prove that a file changed. Keep tests deterministic and runnable in the environments the repository supports. If a check is unavailable or skipped, say so plainly; do not present a narrower result as a full pass.

Testing work is complete when the evidence matches the risk and the reported result names the actual commands and outcome.
