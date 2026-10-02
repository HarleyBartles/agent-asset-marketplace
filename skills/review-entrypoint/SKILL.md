---
name: review-entrypoint
description: Use when creating, assessing, or maintaining a repository's root REVIEW.md code review guidance.
metadata:
  source-id: review-entrypoint
  source-path: skills/review-entrypoint/SKILL.md
  provenance-name: Review Entrypoint first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - the human asks to adopt or assess the review-entrypoint standard.
    - the repository root REVIEW.md code review guidance is being created, reviewed, or maintained.
  do_not_use_when:
    - the task is a code review of proposed changes rather than review-guidance maintenance.
    - the repository has no subscription and no explicit adoption or assessment request for this standard.
license: MIT
---

# Review Entrypoint

Use the [review entrypoint standard](references/standard.md) when a repository explicitly adopts or asks to assess `review-entrypoint`. Existing inline root guidance can satisfy it; inspect the repository's pinned certification before changing it.

AOM offers an optional inline-capable [root REVIEW.md example](assets/REVIEW.md.example). Adapt or replace it with review guidance grounded in the repository. The standard requires only a maintained, useful root entrypoint; another review document, a book inventory, or fan-out is not required.
