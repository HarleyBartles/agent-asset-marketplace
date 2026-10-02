---
name: agents-routing
description: Use when creating, reviewing, or certifying repository AGENTS.md routers and their scoped guidance routes.
metadata:
  source-id: agents-routing
  source-path: skills/agents-routing/SKILL.md
  provenance-name: AGENTS Routing first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - the human asks to adopt or assess the root-agent-router standard in a repository.
    - the repository subscribes to root-agent-router and an AGENTS.md route, scope, or budget is changing.
  do_not_use_when:
    - the task edits unrelated guidance and no AGENTS.md routing obligation applies.
    - the repository has no subscription and no explicit adoption or assessment request for root-agent-router.
license: MIT
---

# AGENTS Routing

Use the [AGENTS routing standard](references/standard.md) when a repository explicitly adopts or asks to assess `root-agent-router`. First inspect its pinned subscription and certification. Ambient availability of this skill does not adopt the standard.

AOM offers an editable [checker starter](assets/check_agents_md.py). Copy and adapt it into a repository-owned location; the plugin copy is not the repository's implementation. It scans root and nested `AGENTS.md` files, including untracked files visible in the worktree; defaults warn above 55 lines and fail above 100. Adapt thresholds and exclusions to repository policy. The checker imposes no router-count limit and cannot judge safe scope, concise routing, or whether the repository's budget fits. A repository adopting this standard must maintain its own checker and run it in CI when CI exists. The repository owns deployment, any hook integration, and semantic review.
