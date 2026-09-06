plan: .agents/plans/2026-09-06-mark-373-operating-system.md
branch: codex/mark-373-operating-system
head_at_capture: 2fb546735b8f9f45ec2f1fb4fb00f86a1f2a8d96
last_completed_task: 6
next_task: 7
next_step: resolve the harness-blocked read-only smoke, then rerun the fixed campaign from a fresh immutable evidence head
checkpoint_state: clean
checkpoint_publication: committed checkpoint record; live HEAD may include this record's publication commit
working_tree_status: clean
working_diff_sha: none
last_green_evidence:
  - branch refresh => fast-forwarded to 672becb21de42e0545f89ea95e1667ca95163ca1 [PR #311 remains Draft]
  - git -C <temp-clone> cat-file -e <v6.3>^{commit} => passed [b36e0829c6d0140e93cfef2ca599b1b07d4a7797]
  - git -C <temp-clone> cat-file -e <v6.2>^{commit} => passed [3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9]
  - git diff --check => passed
  - py -3 tools/run.py marketplace --check => passed
  - py -3 -m pytest tests/test_workflow_contracts.py::TestEvaluationCampaign -q => 6 passed
  - py -3 tools/workflow_pressure_scan.py ... => 104 candidate hits recorded in [pressure-scan.json]; classifications in [pressure-scan.md]
  - py -3 -m pytest tests/test_workflow_contracts.py -q => initial RED preserved in [red-baseline.md]
  - py -3 -m pytest tests/test_workflow_contracts.py::TestAuthorityBootstrapPortability -q => 4 passed
  - py -3 tools/workflow_pressure_scan.py ... => refreshed candidate scan after Task 3 source repair
  - py -3 -m pytest tests/test_workflow_contracts.py::TestValidationTddPublication -q => 4 passed
  - py -3 -m pytest tests/test_workflow_contracts.py::TestPlanningDelegationReview -q => 5 passed
  - py -3 -m pytest tests/test_validate_agent_mesh.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q => 29 passed
  - py -3 tools/run.py mesh --check => passed
  - py -3 -m pytest tests/test_workflow_contracts.py::TestRepositoryCallersAndPressure -q => 3 passed
  - py -3 -m pytest tests/test_workflow_contracts.py -q => 22 passed
  - py -3 tools/validate_tool_cli.py --check => 22 tools pass, 0 warnings, 0 failures
  - normal hooked commit => cc7341e47 (ci check passed; 95 files changed)
  - campaign preflight at evaluation_head cc7341e47 => preflight-ready, codex-cli 0.153.4
  - campaign trials before harness repair => 45/52 complete; Luna/Terra/Sol 13 each, Astra 6; failure was UTF-8 output decoded through Windows cp1252 and is not a model-unavailable result
  - py -3 -m pytest tests/test_workflow_contracts.py::TestEvaluationCampaign -q => 6 passed after capture repair
  - py -3 tools/run_workflow_pressure_campaign.py --check => passed after capture repair
  - normal hooked harness repair commit => 82132d817 (ci check passed)
  - repaired campaign resume at evaluation_head 82132d817 => seven Astra trials completed; 52/52 valid trial records across both immutable heads
  - campaign-meta.json => preflight-ready, fixed four-family matrix, 52 completed trials, explicit unobservable API reasoning mode
  - committed score schema => 52 records, raw hashes, trial/judge provenance, criterion evidence, 14 pass and 38 harness-capability failure verdicts
  - py -3 -m pytest tests/test_workflow_contracts.py::TestEvaluationCampaign -q => 7 passed
  - PR #311 verification => OPEN, Draft, base main, head branch codex/mark-373-operating-system
  - py -3 tools/run.py marketplace --apply => passed; generated outputs current with no unrelated generated diff
  - final focused pytest set => 52 passed
  - py -3 tools/run.py mesh --check => passed
  - py -3 tools/run.py review-preflight --check => four pre-existing warnings also present on origin/main; no new warning introduced by MARK-373
  - normal hooked pressure-campaign commit => b858e06de76aecaa6a55e4b12a8669d5b27055ce (all hook CI targets passed)
  - committed verification => clean status, git diff --check passed, mesh passed; review-preflight retained the four documented origin/main warnings
  - git push origin codex/mark-373-operating-system => published b858e06de76aecaa6a55e4b12a8669d5b27055ce
  - PR #311 verification => OPEN, Draft, base main, full head b858e06de76aecaa6a55e4b12a8669d5b27055ce; Draft workflow check skipped as expected
  - MARK-373 review repair commit => 6b030b94ca2c234a6dd1e9b7a3df06fa0b8ebac3 (source contracts, runner preflight, scan dispositions, focused tests)
  - real Luna preflight at 6b030b94ca2c234a6dd1e9b7a3df06fa0b8ebac3 => harness-blocked; codex-cli 0.153.4 smoke exited 0 without SMOKE_OK; no behavioral trials started
  - campaign invocation at 6b030b94ca2c234a6dd1e9b7a3df06fa0b8ebac3 => stopped after preflight and wrote ignored raw meta
  - py -3 -m pytest tests/test_workflow_contracts.py::TestRepositoryCallersAndPressure tests/test_workflow_contracts.py::TestEvaluationCampaign -q => 12 passed
  - normal hooked diagnostic-status commit => 2fb546735b8f9f45ec2f1fb4fb00f86a1f2a8d96
evidence_head: 6b030b94ca2c234a6dd1e9b7a3df06fa0b8ebac3
unresolved_blockers: revised campaign remains harness-blocked until the real read-only smoke produces SMOKE_OK; temporary upstream clone cleanup was rejected by environment destructive-command policy; review-preflight retains four pre-existing origin/main warnings; Ready promotion remains a human-owned decision for the coordinated cross-repository campaign
resume_reads:
  - .agents/plans/2026-09-06-mark-373-operating-system.md: Luna Execution Contract, Global Constraints, Task 7
  - .agents/docs/mark-373-superpowers-v6.3-rebase.md
  - tests/pressure/workflow-contracts/README.md
  - codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md
  - AGENTS.md
