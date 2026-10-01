# Tracked Hook and CI Adoption Scenarios

Use these prompts in fresh contexts with the `tracked-repo-hooks` skill available. Evaluate decisions against the pinned standard, not exact response wording. The agent should inspect repository evidence before proposing changes and must not claim implementation or certification from starter presence alone.

## Adopt without command bus

You are working in a repository that wants to adopt the tracked hook and CI standard. It has no command bus, and its maintainers are considering AOM's hook, normalizer, and GitHub Actions examples. Describe what is required, what can be selected or omitted, and what needs to be true before self-certification.

Expected decisions: explain the complete Windows pre-commit/Linux hosted gate, equivalent checks and prerequisites, staged candidate handling, declared text normalization, and agent no-skip rule. Treat each AOM artifact as optional. The repository may use its existing tooling or copy/adapt selected assets. Do not add command-bus adoption or require every sample. Certify only after both platforms and drift controls are evidenced and root `AGENTS.md` routes subscription/certification.

## Adopt with a command bus

You are working in a repository that separately adopts command-bus and tracked hook/CI. The maintainers want to use AOM's sample `repository_gate.py` target. Explain what it does, how it enters the repo, and what the hook/CI standard still requires.

Expected decisions: make manual copy/adaptation and explicit registration into the repository-owned bus an agent task. The sample wraps a repository-owned read-only complete-check command and preserves its output and status. It creates no module ABI or shared target registry. The repository can omit or replace it. Hook/CI still owns the complete gate and Windows/Linux parity; command-bus adoption is not implied by tracked hook/CI.

## Existing implementation already conforms

You are working in a repository with a tracked Windows pre-commit hook and Linux hosted CI that appear to run the same complete gate. Its text normalization policy, staged-candidate behavior, and agent no-skip guidance are also documented. The maintainer asks to subscribe to the standard but does not want a rewrite or copied AOM scaffold. Describe the assessment and adoption path.

Expected decisions: inspect the actual hook, workflow, candidate handling, required prerequisites, equivalent gate coverage, no-skip routing, normalization policy, and drift controls. Preserve conforming repository-owned implementation and add no AOM artifacts unless a specific gap makes one useful. Record subscription and route it from root `AGENTS.md`; self-certify after evidence verifies current behavior and drift-prevention measures. Do not demand a command bus or template inventory.
