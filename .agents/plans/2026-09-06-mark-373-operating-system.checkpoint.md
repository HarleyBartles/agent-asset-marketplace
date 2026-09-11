plan: .agents/plans/2026-09-06-mark-373-operating-system.md
branch: codex/mark-373-operating-system
implementation_head: this checkpoint's containing commit
last_completed_task: skill-language contract Task 4
next_task: human review
next_step: review Draft PR #311; do not promote Ready without human instruction
checkpoint_state: MARK-373 implementation, contracts/routing repair, and skill-language migration are complete
working_tree_status: clean at the containing commit

current_evidence:
  - focused repo-standards and workflow-contract suites: 91 passed
  - the containing commit passed the complete tracked pre-commit apply/check gate
  - PR #311 remains OPEN and Draft against main
  - repository-level contracts have one home at .agents/contracts/
  - structural tests now enforce using-superpowers-plus as the sole active composition router
  - active canonical, generated, local, contract, and live-plan prose uses skill identifiers without slash invocation sugar
  - vendored skill descriptions, structured routing metadata, and OpenAI wrappers follow distinct field-language contracts
  - deterministic grammar defects hard-fail; workflow-like discovery clauses remain explicit human-review candidates
  - the pressure tree retains reusable prompts/configuration and current checked controls only

evidence_boundaries:
  - no behavioral model baseline is claimed
  - no paid model or Quorum evaluation was run for the skill-language sub-slice
  - review-preflight warnings inherited from origin/main are not attributed to MARK-373

resume_reads:
  - .agents/plans/2026-09-06-mark-373-operating-system.md: Global Constraints, Task 8
  - tests/pressure/workflow-contracts/README.md
  - AGENTS.md
