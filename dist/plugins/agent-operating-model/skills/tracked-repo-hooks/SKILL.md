---
name: tracked-repo-hooks
description: Use when changing or assessing a repository's tracked pre-commit hook and hosted-CI parity under its adopted standard.
metadata:
  source-id: tracked-repo-hooks
  source-path: skills/tracked-repo-hooks/SKILL.md
  provenance-name: Tracked Repo Hooks first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Tracked Repo Hooks

For explicit adoption or assessment, inspect the repository's pinned subscription and certification through `repo-standards`, then follow the [tracked hook and CI definition](references/standard.md). Ambient availability does not adopt the standard.

The pledge is one complete gate on Windows before commit and Linux in hosted CI. The checks are the same in both places: tests, lint, build, and other configured CI gates do not move exclusively to paid hosted CI or exclusively to a developer hook. The tracked hook must be maintained, hook skipping is prohibited for agents, and hosted CI runs the equivalent gate against the proposed commit.

Preserve repository content across platforms. Validate the exact candidate commit state in an isolated checkout and report failures clearly. Checks may create disposable ignored build/test outputs, but must not change maintained files or the candidate index. Put normalization, formatting, generation, and other repairs in explicit command-bus apply targets when a bus is adopted. The hook only rejects or passes; order checks cheapest-first, stop at the first failure, and print its exact repair and recheck command.

An adoption is repository-owned implementation and self-certification, not deployment of a mandatory AOM scaffold. Route the subscription and readable certification from root `AGENTS.md`. Certification names the hook, hosted workflow, complete gate, Windows/Linux prerequisites and evidence, candidate/unstaged-work handling, normalization policy, agent no-skip rule, and the measures that prevent parity drift. Every agent changing an affected surface maintains that certification. Certify only after the complete gate and its drift controls are in place.

Choose only the starter assets that help, or use none:

- [Candidate-preserving Bash hook](assets/hooks/pre-commit) is a fail-closed seed. Adapt its repository-owned check function and install it as the tracked hook. It expects Git Bash on Windows and Bash on Linux. When Git launches the tracked file directly as a hook, preserve its executable bit on platforms that require it.
- [Python text normalizer](assets/normalization/normalize_text.py) operates only on explicitly selected UTF-8 text paths. Adapt its selected paths and line-ending/final-newline policy. The [`.gitattributes` example](assets/normalization/gitattributes.example) is optional policy material, not a required global file.
- [GitHub Actions hosted-gate example](assets/workflows/github-actions-hosted-gate.yml) checks out the proposed commit and invokes the same hook in hosted mode. Its prerequisite step intentionally fails until adapted. Other CI providers may implement the same pledge directly.
- [Optional bus target](assets/targets/repository_gate.py) can be copied and manually registered only when the repository separately adopts command-bus. It forwards one repository-owned candidate-preserving complete-check command; it is not an installer, bus ABI, or command registry.

Assets become repository-owned when copied. Presence does not prove conformance. The hook, normalizer, workflow, and bus target can each be replaced independently if the repo's own approach meets its pinned requirements. V1 consumers continue to follow their pinned definition until an explicit upgrade.

The gate runs in a disposable checkout so author-side ignored files are neither imported nor removed. Checks may leave disposable ignored outputs inside that checkout; maintained candidate changes and private-index changes reject the gate. Hosted CI checks the same candidate and required checks, with its own explicit prerequisite setup.
