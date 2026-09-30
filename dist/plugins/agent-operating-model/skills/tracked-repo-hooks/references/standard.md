# Tracked Hook and CI Standard

**Standard ID:** `tracked-validation-hook`

## Pledge

The repository maintains a tracked pre-commit hook and hosted CI that run one complete validation gate with equivalent checks and failure criteria. Agents do not skip the hook. Windows local execution and Linux hosted execution prove the same repository requirements before paid CI is needed and before changes merge.

## Required implementation

- Run the complete required gate in both the Windows hook and Linux hosted CI, including tests, integration tests, lint, generation checks, and other merge-blocking validation.
- Provide required infrastructure and prerequisites on both platforms. Missing requirements fail clearly rather than silently omitting checks.
- Have the hook assess the candidate tree that will be committed. Include hook-side normalization or generation in that candidate and validate it. Preserve unrelated unstaged work.
- Have hosted CI assess the committed counterpart. Keep check coverage and failure criteria equivalent while allowing platform-specific adapters where needed.
- Normalize declared line endings and final newlines, including generated and formatted text, so platform changes do not create churn.
- Prohibit hook skipping by agents. The repository owns its hook, candidate materialization, canonical gate, and drift controls.
- If command bus is adopted, the bus owns its CLI contract. A hook may call a conforming bus target through an agent-integrated implementation.
- AOM adoption requires root `AGENTS.md` routing to subscription and certification.

## Conditional obligations

When CI exists and the repository adopts another standard that requires a checker in CI, include it in the complete gate. A bus implementation is optional and does not alter this standard's parity promise.

## Self-certification

Identify the tracked hook and hosted workflow, demonstrate equivalent checks and prerequisites on Windows and Linux, and explain how the staged candidate and unrelated working changes are handled. Describe how agents learn and follow the no-skip rule and how parity is maintained.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM may offer a hook starter, normalization support, and a bus target implementation. Each is optional and becomes repository-owned when adopted. No fixed command JSON or source submodule is required. Do not add the retired shared-checkout mutation-intent flag as an obligation.
