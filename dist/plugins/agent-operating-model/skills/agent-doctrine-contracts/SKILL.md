---
name: agent-doctrine-contracts
description: Use when adopting or assessing agent-facing doctrine and contracts, their repository locations, quality, or routes.
metadata:
  source-id: agent-doctrine-contracts
  source-path: skills/agent-doctrine-contracts/SKILL.md
  provenance-name: Agent Doctrine and Contracts first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Agent Doctrine and Contracts

Use the [agent doctrine and contracts standard](references/standard.md) when a repository explicitly adopts or asks to assess `agent-doctrine-contracts`. It governs agent-facing operating knowledge, not product schemas merely named contracts.

AOM offers an editable [checker starter](assets/check_agent_docs.py). Copy and adapt it into a repository-owned location; the plugin copy is not the repository's implementation. It checks that `.agents/doctrine/` and `.agents/contracts/` exist, parses JSON syntax without imposing a schema, and checks local Markdown links in those stores and in explicitly selected `--route-root` sources. Other Markdown files can contribute inbound-link evidence for advisory candidate reporting, but their unrelated broken links do not fail this check. Use `--exclude` for repository-specific boundaries. The starter cannot identify agent documents misplaced elsewhere, establish semantic reachability, or see harness scope, skill metadata, plugin/tool registries, and other non-Markdown routes. Adapt it and add the semantic review your repository needs. A repository adopting this standard must maintain its own checker and run it in CI when CI exists; it owns any hook integration and continuing certification.
