# Tracked Hook and CI Standard

**Standard ID:** `tracked-validation-hook`

## Pledge

The repository maintains a tracked pre-commit hook and hosted CI that run one complete validation gate with equivalent checks and failure criteria. Agents do not skip the hook. Windows local execution and Linux hosted execution prove the same repository requirements before paid CI is needed and before changes merge.

## Required implementation

- Run the complete required gate in both the Windows hook and Linux hosted CI, including tests, integration tests, lint, generation checks, and other merge-blocking validation.
- Provide required infrastructure and prerequisites on both platforms. Missing requirements fail clearly rather than silently omitting checks.
- Have the hook assess the exact candidate tree that will be committed in a disposable checkout and private index. Load gate configuration and adapters from that candidate, never from unstaged edits. Preserve all author checkout state. Checks may create disposable ignored build and test outputs in the isolated checkout, but must not alter maintained candidate files or its index. Gates must not rely on stale ignored inputs from the author checkout.
- Have hosted CI assess the committed counterpart. Keep check coverage and failure criteria equivalent while allowing platform-specific adapters where needed. Derive ignored generated/setup inputs from the checked-out commit before using them as evidence.
- Put normalization, formatting, generation, and other maintained-file repairs in explicit command-bus apply targets when a bus is adopted. The hook rejects a candidate that needs repair; it never repairs or stages it. A passing gate may create disposable ignored build/test outputs, but must leave maintained candidate files and its private index unchanged.
- Order checks from cheapest to most expensive and stop at the first failing check. Name the failed check and command, preserve its status and output, and print the exact focused repair and recheck commands when available. Expensive test/build setup starts only after preceding checks pass.
- Prohibit hook skipping by agents. The repository owns its hook, candidate materialization, canonical gate, and drift controls.
- If command bus is adopted, the bus owns its CLI contract. A hook may call a conforming bus target through an agent-integrated implementation.
- AOM adoption requires root `AGENTS.md` routing to subscription and certification.

## Conditional obligations

When CI exists and the repository adopts another standard that requires a checker in CI, include it in the complete gate. A bus implementation is optional and does not alter this standard's parity promise.

## Self-certification

Identify the tracked hook and hosted workflow, demonstrate equivalent checks and prerequisites on Windows and Linux, and explain how the staged candidate, unrelated working changes, and ignored generated inputs are handled. Describe how agents learn and follow the no-skip rule and how parity is maintained.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM ships optional, independently selectable examples in the `tracked-repo-hooks` skill package:

- `assets/hooks/pre-commit`: candidate-preserving Bash hook with a fail-closed repository-owned check seam. Copy and adapt it, or implement another tracked hook. Preserve its executable bit when Git launches the tracked file directly.
- `assets/normalization/normalize_text.py`: standard-library Python normalizer for explicitly selected UTF-8 paths, with `--check` and `--apply`. Repositories choose scope and policy. `gitattributes.example` is optional.
- `assets/workflows/github-actions-hosted-gate.yml`: one GitHub Actions example that checks out the proposed commit and calls the tracked hook in hosted mode. Its prerequisite step fails until adapted. It does not require an AOM runtime checkout.
- `assets/targets/repository_gate.py`: optional check-only command-bus target sample. Manually copy and register/adapt it only if command-bus is also adopted. It forwards a repository-owned complete candidate-preserving check command and defines no shared module ABI, configuration contract, or installation behavior.

None is required by the pledge. A repository can implement the invariants in its existing tools or adopt any subset of these examples. Copied material is adapted, maintained, and certified by the repository. Presence of any starter is not evidence of compliance. Do not add a fixed command JSON, source submodule, or the retired shared-checkout mutation-intent flag as an obligation.
