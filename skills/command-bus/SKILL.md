---
name: command-bus
description: Use when creating, reviewing, or changing a repository command bus and its named targets.
metadata:
  source-id: command-bus
  source-path: skills/command-bus/SKILL.md
  provenance-name: Command Bus first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Command Bus

For explicit adoption or assessment, inspect the repository's pinned subscription and certification through `repo-standards`, then follow the [command bus definition](references/standard.md). Ambient availability does not adopt the standard.

A command bus is a repository-owned CLI under `tools/` that presents named targets. The repository chooses its implementation language and owns the bus and its targets. Python is a practical portable choice, not a requirement. The optional AOM bus implementation can bootstrap the repository bus; adoption does not automatically install it or register targets. Other standards may offer optional modules for deployment into a repository that has adopted a bus.

Each target supports `--help` and the `--check` and `--apply` modes that make sense for that target. The CLI itself supports `--help`. `--check` reports state without mutation. A mutating target may support `--dry-run` when it can report the planned state. Define one consistent no-mode behavior for the bus and every target; do not let targets silently choose different defaults. Preserve target output and exit status, and reject unsupported or conflicting modes clearly.

The optional [Python starter](assets/tools/run.py) and its [sample target](assets/tools/targets/check_status.py) can bootstrap a repository bus. The other sample targets demonstrate apply and dry-run behavior. Copy and adapt selected files under the repository's `tools/` directory as an explicit agent task. The starter's `TARGETS` mapping is only that implementation's local registry; a conforming repository can use any language, filename, target model, or CLI integration that meets the standard.

Multi-target orchestration and ordering are optional repository choices, not universal requirements. Use the repository's own policy for target discovery, dependency ordering, and failure behavior. If the repository has an older v1 pin, follow that definition until an explicit upgrade.
