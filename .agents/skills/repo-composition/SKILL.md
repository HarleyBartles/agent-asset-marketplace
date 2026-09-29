---
name: repo-composition
description: Use when creating, changing, or validating repository runbooks, playbooks, their policy mapping, or declared composition edges.
metadata:
  source-id: repo-composition
  source-path: skills/repo-composition/SKILL.md
  provenance-name: Repo Composition first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Repo Composition

Lifecycle stages are runbooks. Topical workflows are playbooks available whenever their concern applies. Runbook routing is optional; declared runbook/playbook edges resolve and agree on both sides. Playbooks may compose other playbooks through their `Composition` section, but composition targets must resolve and the resulting graph must remain acyclic.

Use `Required capabilities` and `Optional capabilities` to describe what the workflow needs, without naming ambient provider skills. At runtime, inspect the skills actually exposed, choose a suitable provider for each capability, and follow its instructions. If a required capability has no suitable provider, stop before dependent work and report the unmet capability. Report and skip an unavailable optional capability when the rest of the workflow can proceed.

Use `Required repository-owned skills` and `Optional repository-owned skills` only for exact skill names with repository custody declared in `repo.local_skills`. Marketplace subscriptions and installed skill projections do not prove local ownership or runtime capability availability. Hosted validation checks document structure, path mappings, graph integrity, and declared local-skill custody only; it cannot prove that an ambient provider is available to an agent.

Use the paths declared in the repository's runbook/playbook policy. Conventional `.agents/runbooks/` and `.agents/playbooks/` homes are defaults of explicitly adopted standards, not portable ambient assumptions.

The portable contract and scaffolds currently live with `repo-shape` while the coordinator consumes them. This skill owns their semantics and is the trigger for future changes to those assets.
