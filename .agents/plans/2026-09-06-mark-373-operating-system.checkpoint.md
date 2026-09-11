plan: .agents/plans/2026-09-06-mark-373-operating-system.md
branch: codex/mark-373-operating-system
implementation_head: 194d32c8b44a7f855ccb72d2277d1ddf941597a3
last_completed_task: contracts-and-routing Task 5
next_task: contracts-and-routing Task 6
next_step: repair routing review findings, normalize active skill references, regenerate, validate, and push Draft PR #311
checkpoint_state: MARK-373 implementation is under final routing-contract repair
working_tree_status: dirty during the approved Task 6 implementation pass

current_evidence:
  - focused repo-standards and workflow-contract suites: 85 passed
  - the containing commit passed the complete tracked pre-commit apply/check gate
  - PR #311 remains OPEN and Draft against main
  - repository-level contracts have one home at .agents/contracts/
  - structural tests now enforce using-superpowers-plus as the sole active composition router
  - active canonical, generated, local, contract, and live-plan prose uses skill identifiers without slash invocation sugar
  - the pressure tree retains reusable prompts/configuration and current checked controls only

evidence_boundaries:
  - no behavioral model baseline is claimed
  - review-preflight warnings inherited from origin/main are not attributed to MARK-373

resume_reads:
  - .agents/plans/2026-09-06-mark-373-operating-system.md: Global Constraints, Task 8
  - tests/pressure/workflow-contracts/README.md
  - AGENTS.md
