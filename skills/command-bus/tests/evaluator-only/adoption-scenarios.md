# Command Bus Adoption Scenarios

Use the following prompts in fresh contexts with the `command-bus` skill available. Evaluate decisions against the pinned standard definition and approved AOM design, not exact response wording. The agent should inspect repository evidence before proposing edits and must not claim implementation or certification from file presence alone.

## Python starter selected

You are working in a small Python repository with a root `AGENTS.md`, an existing `tools/` directory, and no command-bus subscription. The maintainer asks to adopt AOM's command-bus standard and says the Python starter may help. Add only one `status --check` target that preserves maintained files while allowing disposable outputs. The repository has no hook or CI subscription. Describe the changes needed, inspect whether existing files should be edited or preserved, and state when it is honest to record certification.

Expected decisions: inspect and read the pinned standard; treat the starter as optional and repository-owned after adaptation; create/adapt only the CLI and selected target; add the command-bus subscription and route root `AGENTS.md` to subscription/certification without replacing authored guidance; certify after the implemented target satisfies mode/help/forwarding/status behavior and drift controls are stated. Do not add hook, workflow, normalizer, or unrelated targets.

## Repository-authored implementation selected

You are working in a C# repository with no Python runtime requirement. Its maintainers want to implement their own bus and adopt only the command-bus standard. They ask whether `tools/run.py`, AOM's local `TARGETS` mapping, and Python sample targets are required. Explain the implementation choices, the mandatory interface behavior, adoption records, and evidence needed for self-certification.

Expected decisions: Python and `run.py` are optional starters; no AOM registry format or module ABI is required. The repository may implement a C# CLI under its own `tools/` convention and must demonstrate target discovery/help, supported explicit modes, no-mode failure, unsupported-mode rejection, exact target argument/output/status behavior, preserved maintained files in check mode, and continuing drift controls. Root `AGENTS.md` routes the subscription and certification. Do not copy starter assets unless they help.

## Bus without hook/CI

You are working in a repository that wants a command bus but has no adopted hook/CI standard. The bus has targets for test, docs, and release. The maintainer asks whether subscribing to command bus means a tracked pre-commit hook, a hosted workflow, or automatic registration for future AOM target modules.

Expected decisions: command bus is independently selectable and requires the conforming CLI only. It does not imply hook/CI, a release target inventory, or automatic registration. Other selected standards may later offer optional target assets, but an agent explicitly integrates each one into the repository-owned bus. Certify the chosen bus and its target inventory without claiming any neighboring standard.
