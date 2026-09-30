# Command Bus Standard

**Standard ID:** `command-bus`

## Pledge

The repository implements a command bus CLI under `tools/` that exposes named targets through a consistent, truthful interface. AOM offers an optional Python starter; the repository chooses the implementation language and target set.

## Required implementation

- Provide top-level `--help`, target discovery, and `<target> --help`. Help explains purpose, supported modes, prerequisites, side effects, and target-specific arguments without running target work.
- Targets support the meaningful subset of `--check`, `--apply`, and optional `--dry-run`. Check assesses without correcting maintained repository files. Apply performs the documented changes. Dry-run previews mutation when meaningful; proposed changes alone do not make a dry-run fail. Disposable test/build outputs are compatible with check mode.
- Require an explicit mode or help request for a selected target. Without one, show usage and exit nonzero. A bare bus invocation may show top-level help.
- Reject unknown targets, conflicting modes, and unsupported modes before work starts. Never silently succeed without an operation.
- Forward target-specific arguments faithfully. Preserve target output and exact exit status. Required failures or skipped work cannot be reported as success.
- Keep dispatch semantics consistent when no mode is supplied: selected targets fail with usage rather than applying different defaults.
- Integrate targets through an agent task. The bus does not automatically install or discover AOM artifacts.
- AOM adoption requires root `AGENTS.md` routing to subscription and certification.

## Conditional obligations

An adopted hook/CI standard may integrate a bus target if the repository chooses to use a bus. The hook/CI standard remains responsible for complete gate parity. A bus can exist without hook/CI adoption.

No shared module ABI is required. Targets may be implemented in the repository's chosen language and connected by its own integration.

## Self-certification

Describe the CLI, target ownership and inventory, supported modes, help behavior, forwarding and exit semantics, and the measures that keep them consistent. Evidence covers representative successful, failing, and unsupported invocations.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM provides an optional Python bus bootstrap. Repositories may deploy and modify it or implement a bus in another language if it meets this interface. Optional standard targets, including hook/CI modules, must be integrated by an agent and conform to this contract. `tools/` is the convention; `scripts/` remains a common home for standalone script work.
