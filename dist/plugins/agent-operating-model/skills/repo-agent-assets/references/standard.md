# Repository Plugin Subscriptions Standard

**Standard ID:** `repo-plugin-subscriptions`

## Pledge

The repository declares the plugins agents need through native harness configuration backed by Git dependencies, so a fresh clone can resolve the intended repository plugins subject to access and host prerequisites.

## Required implementation

- Declare repository plugin dependencies in `.agents/plugins/` using the native formats for the repository's supported harnesses.
- Identify each dependency's source repository and plugin path where required. A Git branch such as `main` may be used for capabilities the repository intentionally refreshes; an immutable revision is also valid.
- Bind the declaration through each supported harness's native repo-level mechanism. Keep Codex and Devin configuration idiomatic to those clients while expressing the same intended plugin dependency.
- Reserve `.agents/skills/` for skills authored and owned by the repository. Do not copy installed plugin skills there.
- Do not require a `repo.local_skills` inventory. Repository-authored skills are the only content in `.agents/skills/`.
- Distinguish a valid declaration from successful installation, authentication, trust, and runtime availability.
- AOM adoption requires root `AGENTS.md` routing to subscription and certification.

## Conditional obligations

Apply bindings for the harnesses the repository supports. A repository with no repository plugins may still adopt this standard if its pledge describes the dependencies it does use; it need not fabricate a dependency.

Updating plugin payloads does not update any AOM standard subscription. Standard requirements remain pinned independently by their source commit.

## Self-certification

Identify the dependency declarations, supported harness bindings, and how a fresh clone's plugin availability is checked or established. Explain authentication or host prerequisites that affect availability. Confirm `.agents/skills/` contains only repository-authored skills.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM supplies adoption guidance and may provide editable native configuration examples or checks. Repositories own their declarations and harness bindings. No marketplace source submodule, copied plugin payload, universal installer, or separate local skill inventory is required.
