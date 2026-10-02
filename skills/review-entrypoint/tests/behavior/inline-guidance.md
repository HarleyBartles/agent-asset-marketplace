# Inline review entrypoint behavior case

A repository adopts `review-entrypoint`, has no review playbook or review-stage runbook, and asks whether it must create either before maintaining root `REVIEW.md`.

Expected: the repository may put useful review invariants directly in `REVIEW.md`. It may route to existing review guidance if that is useful. It does not need deeper REVIEW files, a book inventory, fan-out, or another adopted standard.
