---
name: rooms-ambiguity-buster
description: Use when preserve rooms ambiguity for identity, motive, authorship, archive
  gaps, narration, and disappearance.
metadata:
  source-id: rooms-ambiguity-buster
  source-path: sources/first_party/skills/rooms-ambiguity-buster/SKILL.md
  provenance-name: Rooms Ambiguity Buster first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when preserve rooms ambiguity for identity, motive, authorship, archive
    gaps, narration, and disappearance.
  use_when:
  - Use when preserve rooms ambiguity for identity, motive, authorship, archive gaps,
    narration, and disappearance.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
  projection_targets:
  - codex-marketplace/plugins/house-skills/skills/rooms-ambiguity-buster
license: MIT
---
# Rooms Ambiguity Buster

Use this Skill when the work risks resolving uncertainty without evidence.

## Source-route discipline

When ambiguity depends on repo evidence, choose the source route explicitly.

- Use bound `file_search` GitHub for broad discovery across archive, canon, manuscript, issue, or repo surfaces when
  the relevant evidence surface is not already known.
- Use the live GitHub API connector route, such as `api_tool` when exposed, for exact known files, issue threads,
  comments, commits, refs, and PR details.
- If `file_search` is unbound and broad discovery is needed before a safe ambiguity judgment, ask Harley to bind the
  GitHub `file_search` connector to the relevant repo set.
- If exact known surfaces are enough, inspect them through the live API route rather than blocking on `file_search`.

Search-only absence is not evidence that ambiguity is resolved. If source access is unavailable or partial, preserve the
uncertainty.

## Preserve

- who experienced;
- who witnessed;
- who reconstructed;
- who narrated;
- who benefited;
- who exposed;
- who protected;
- who disappeared;
- who paid the emotional cost.

## Rules

`We do not know` is valid. Do not collapse ambiguous identity, motive, authorship, archive gaps, room history, narrator
knowledge, or manuscript uncertainty. Do not say `most likely` without provenance.

When evidence is partial, say what is known, what is unknown, what source route was checked, and what would be needed to
resolve it.
