# Receiving Code Review Deeper-Smell Design

> **Status:** Approved for implementation on 2026-09-21. Deferred to a fresh PR after draft PR #328.

## Problem

The current `receiving-code-review` skill stops after it verifies feedback, evaluates the suggestion, implements the reported correction, and tests that correction. That is sufficient for literal review satisfaction, but it does not prompt the receiver to inspect whether a correct finding exposes a repeatable failure mechanism in the repository. A competent agent can therefore repair one manifest entry, unsafe call site, or duplicated check while leaving the condition that will produce the same class of defect again.

## Goal

Make code-review reception include one bounded deeper-smell inspection after a finding is verified as correct, and prove that new behaviour with a blinded RED/GREEN exercise in a fresh local Git repository.

## Success criteria

- A receiving agent still verifies feedback before acting and still fixes the reported instance correctly.
- When repository evidence exposes a repeatable mechanism, the agent inspects it and chooses the smallest justified response: in-scope prevention or an evidence-backed follow-up when prevention is consequential.
- The new guidance does not turn isolated mistakes into speculative redesign.
- A blinded baseline run demonstrates the current failure: correct local repair and verification followed by an unjustified stop at the specimen.
- A blinded treatment run on an identical fixture demonstrates transfer to a defect class other than manifest drift.

## Design decisions

### 1. Add a structural deeper-smell step

The response pattern in the canonical `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/SKILL.md` will add an explicit inspection between technical evaluation and response:

```text
READ -> UNDERSTAND -> VERIFY -> EVALUATE -> INSPECT -> RESPOND -> IMPLEMENT -> VERIFY
```

`INSPECT` asks whether the verified finding reveals a deeper smell. The governing test is:

> Could another competent implementer, using the repository's current interfaces, workflow, and guidance, plausibly make the same class of mistake?

The skill will define three branches:

1. **No credible deeper smell:** correct and verify the reported instance.
2. **Credible, small, in-scope prevention:** correct the instance, add the smallest durable prevention, and prove the prevention addresses the defect class rather than only the reported specimen.
3. **Credible but consequential or out of scope:** make the independently safe local correction, report the evidenced mechanism, and propose a concrete follow-up instead of silently expanding authority.

The smell must be a causal mechanism supported by repository evidence, not an imagined future risk. Representative indicators include duplicated truth, unenforced invariants, incomplete multi-surface operations, unsafe interfaces, unclear ownership, and missing boundary or postcondition checks. Preferred prevention removes the opportunity, mechanically detects the class, or makes the correct action the easy action. Prose reminders are the fallback when the rule genuinely requires judgment.

The skill's common-mistakes table will name the existing failure directly: fixing only the reviewed specimen without checking for an evidenced repeatable mechanism. One compact example will use manifest drift to explain the concept, but the behavioural proof will use a different defect class.

### 2. Define the clean RED before authoring the guidance

The clean RED is not a generally poor review response. It is competent literal review satisfaction:

1. The feedback is correct and understood.
2. The agent verifies it against the repository.
3. The agent makes a technically sound local correction.
4. The agent adds or runs focused verification for that correction.
5. The repository contains reasonably discoverable evidence of a repeatable mechanism behind the defect.
6. The agent stops without investigating or naming that mechanism.

A run is not a valid RED if the agent misunderstands the reviewer, applies an incorrect patch, omits ordinary verification, cannot reasonably discover the mechanism, or notices the smell but lawfully declines a consequential redesign. If the unmodified skill already produces the desired deeper-smell behaviour, the fixture has not established RED and must not be used to justify the change.

### 3. Use a different defect class for transfer

The pressure fixture will model a small Python command-line package with several command wrappers. Existing wrappers independently infer subprocess success from output or error text rather than the process return code. The PR under review adds another wrapper by following that existing pattern. A reviewer correctly reports that the new wrapper can claim success when its subprocess exits non-zero without diagnostic text.

The literal correction is intentionally straightforward: check the return code in the reviewed wrapper and add a focused regression test. The deeper smell is that subprocess-success semantics are duplicated across sibling wrappers. The smallest durable prevention is a shared checked-execution boundary with one class-level regression test and migration of the small wrapper family to that boundary. The fixture will contain no unrelated subprocess concerns such as retries, timeouts, telemetry, or a general execution framework.

This scenario proves transfer because the skill may use manifest drift as an explanatory example while the examination requires recognition of duplicated process-result semantics.

### 4. Ship and materialize an ordinary local PR fixture

The skill will ship the complete lightweight fixture source tree at `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/`. The tree will contain the materializer, review comment, rubric, feature patch, and a deliberately small fixture repository. It will contain no dependency trees, build output, binaries, caches, or captured run artifacts.

`materialize.py` will default to a read-only check and require an explicit apply mode, empty destination, and skill-source path before it writes. It will copy the fixture unchanged into a neutral project, initialize Git, commit the complete base state on `main`, install the selected `receiving-code-review` behavioural surface, create a feature branch, apply and commit the feature patch, and leave a clean PR-head working tree. The installed copy excludes the skill's `tests/` tree so the fixture recipe, hidden rubric, and expected result cannot leak into the blinded worker context. `git diff main...HEAD` will show only the implementation under review.

The materializer must be deterministic apart from irrelevant Git timestamps, fail closed on a non-empty destination, avoid remote configuration, and expose no network or external connector surface. Generated repositories and run output live under the repository's resolved off-repo scratch root and are removed after the campaign.

The subagent receives a fresh context, the fixture repository as its working directory, an instruction to read the installed `receiving-code-review` skill, and one blocking inline-review comment naming the changed file and line. It is not shown the fixture recipe, rubric, RED/GREEN terminology, prior conversation, or expected deeper smell.

### 5. Compare the existing and candidate skills on the same recipe

The RED repository is materialized from the current skill before the behavioural addition. Its subagent patch, test output, searches, and final report are kept only as transient scratch evidence for the current change. The run record names the fixture-recipe digest, baseline-skill digest, base commit, PR-head commit, model/profile selection, and rubric version without retaining a full transcript.

After RED is confirmed, the minimal skill addition is authored. GREEN uses a newly materialized repository from the same fixture tree and feature patch, with only the installed skill content changed to the candidate version. Model, reasoning, prompt, tools, repository shape, review comment, and scoring rubric stay equal.

GREEN requires observable evidence that the agent:

- fixes and verifies the reported wrapper defect;
- inspects sibling uses of the same success-detection pattern;
- names duplicated process-result semantics as the repeatable mechanism;
- implements only the shared checked-execution prevention;
- adds proof at the shared invariant boundary; and
- avoids unrelated subprocess redesign.

Mentioning a possible systemic issue without inspecting it is not GREEN. Redesigning the command framework is also not GREEN. One bounded paired pressure proof is sufficient unless it exposes a concrete wording or fixture failure; any such failure returns the change to refinement and re-proof.

Stable prompts, fixture inputs, and the rubric remain tracked. Full model transcripts, score directories, copied model metadata, and generated Git repositories do not become repository evidence.

## Source and generated surfaces

Authored changes belong in the canonical `receiving-code-review` skill tree. The installed `.agents/skills/receiving-code-review/` copy, marketplace manifests, indexes, and mesh surfaces remain generated outputs. No installed projection is edited by hand.

## Failure handling

- If the fixture cannot produce the defined competent-local-fix RED, stop. Do not weaken the rubric or claim the new guidance is necessary from that run.
- If GREEN fixes only the specimen, refine the minimal skill wording against the observed omission and rerun the paired proof.
- If GREEN overreaches, tighten the evidence and authority branches rather than accepting deeper-smell recognition alone.
- If RED and GREEN differ in anything besides the skill content, discard the comparison and rematerialize both sides.

## Validation

Validation will include deterministic tests of the fixture materializer's branch, commit, diff, cleanliness, refusal of non-empty destinations, and weight limits; a clean RED recorded before editing the skill; one bounded clean GREEN after the minimal skill edit; focused prose-contract tests for the evidence and authority branches; normal marketplace and installed-skill regeneration; the repository's staged hooked commit gate; and self-review before Ready status.

## Non-goals

- Mandatory root-cause analysis for every review comment.
- Turning typos or unique mistakes into architecture work.
- Giving review feedback authority to expand implementation scope silently.
- Building a general-purpose evaluation service or permanent GitHub fixture repository.
- Loading test recipes or rubrics during ordinary skill invocation.
- Retaining full model transcripts or generated fixture repositories in Git.

## Planning handoff

The existing implementation plan remains the execution artifact for this work. Its already-completed test-custody tasks are historical prerequisites supplied by draft PR #328; the fresh deeper-smell PR begins at the fixture and observed-RED work. Execution must establish a competent RED before changing the skill, make the minimal behavioural addition, prove GREEN on a newly materialized equivalent repository, regenerate projections, and pass the repository gate.
