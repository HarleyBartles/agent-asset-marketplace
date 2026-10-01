# Tracked Hook and CI Standard

**Standard ID:** `tracked-validation-hook`

## Pledge

The repository maintains a tracked pre-commit hook and hosted CI that run one complete validation gate with equivalent checks and failure criteria. Agents do not skip the hook. Windows local execution and Linux hosted execution prove the same repository requirements before paid CI is needed and before changes merge.

## Required implementation

- Run the complete required gate in both the Windows hook and Linux hosted CI, including tests, integration tests, lint, generation checks, and other merge-blocking validation.
- Provide required infrastructure and prerequisites on both platforms. Missing requirements fail clearly rather than silently omitting checks.
- Have the hook assess the candidate tree that will be committed. Include hook-side normalization or generation in that candidate and validate it. Preserve unrelated unstaged work. Gates must not rely on stale ignored build/configuration artifacts; refresh ignored derived inputs from the candidate or isolate the gate.
- Have hosted CI assess the committed counterpart. Keep check coverage and failure criteria equivalent while allowing platform-specific adapters where needed. Derive ignored generated/setup inputs from the checked-out commit before using them as evidence.
- Normalize declared line endings and final newlines, including generated and formatted text, so platform changes do not create churn.
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

- `assets/hooks/pre-commit`: candidate-safe Bash hook with fail-closed repository-owned apply/check seams. Copy and adapt it, or implement another tracked hook. Preserve its executable bit when Git launches the tracked file directly.
- `assets/normalization/normalize_text.py`: standard-library Python normalizer for explicitly selected UTF-8 paths, with `--check` and `--apply`. Repositories choose scope and policy. `gitattributes.example` is optional.
- `assets/workflows/github-actions-hosted-gate.yml`: one GitHub Actions example that checks out the proposed commit and calls the tracked hook in hosted mode. Its prerequisite step fails until adapted. It does not require an AOM runtime checkout.
- `assets/targets/repository_gate.py`: optional check-only command-bus target sample. Manually copy and register/adapt it only if command-bus is also adopted. It forwards a repository-owned complete read-only check command and defines no shared module ABI, configuration contract, or installation behavior.

None is required by the pledge. A repository can implement the invariants in its existing tools or adopt any subset of these examples. Copied material is adapted, maintained, and certified by the repository. Presence of any starter is not evidence of compliance. Do not add a fixed command JSON, source submodule, or the retired shared-checkout mutation-intent flag as an obligation.
