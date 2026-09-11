plan: .agents/plans/2026-09-06-mark-373-operating-system.md
branch: codex/mark-373-operating-system
implementation_head: this checkpoint's containing commit
last_completed_task: local contracts, provenance, and all-runbook boundary audit
next_task: human review
next_step: review Draft PR #311; do not promote Ready without human instruction
checkpoint_state: MARK-373 implementation and approved follow-up slices are complete
working_tree_status: this checkpoint's containing commit is the published closeout record

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
  - focused installer, repo-standards, workflow-contract, and writing-profile suites: 181 passed
  - repo.local_skills is exact-name registration; runtime rejects legacy prefix keys and scaffold migration fails closed on unresolved prefixes
  - repo-resident unslop contract lives at .agents/contracts/unslop/repository.md
  - all runbooks were audited: generic method is routed to skills; repo paths, commands, custody, exceptions, and evidence stay local
  - Superpowers+ records its upstream v6.3.0 pin without claiming a retained upstream snapshot

evidence_boundaries:
  - no behavioral model baseline is claimed
  - no paid model or Quorum evaluation was run for the skill-language sub-slice
  - semantic language review is deterministic and source-based; it is not a behavioral model-evaluation claim
  - unconstrained `pytest` collection is not a MARK-373 gate: it enters standalone eval fixtures without their fixture packages, and two Bash-wrapper tests cannot translate Windows paths in this runtime
  - review-preflight warnings inherited from origin/main are not attributed to MARK-373

resume_reads:
  - .agents/plans/2026-09-06-mark-373-operating-system.md: Global Constraints, Task 8
  - tests/pressure/workflow-contracts/README.md
  - AGENTS.md
