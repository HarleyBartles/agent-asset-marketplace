# Fresh-context pressure results

The checked-in campaign now records controller-orchestrated evidence from
fresh Codex subagent contexts. The evidence is not a CLI-run campaign and does
not claim more repetitions than the controller supplied.

## Coverage

- Six independent scenario contexts: three no-guidance controls and three
  guided variants.
- Five independent micro-test contexts, exactly matching the five responses
  supplied by the controller. No five-fold repetition claim is made, and the
  sixth fixture micro-test is not claimed as executed.
- Every recorded context has `fresh_codex_subagent_context: true`, its source
  rollout filename, and a raw response excerpt in `campaign.json`; omitted
  middle text is marked with `...`.

## Observed contract behavior

The raw responses consistently show:

- Git-derived checkout and worktree resolution instead of filesystem guessing;
- stop/refusal for mutation from a shared checkout without the explicit
  override and current human approval;
- unconditional submodule rejection, including when
  `--allow-shared-checkout` is suggested;
- mandatory `repo-worker-base` plus matching baseline, local guide, and
  downstream Superpowers lane composition;
- publication-proof gating: local tests or a local commit do not qualify for
  GREEN without a pushed head, PR-visible evidence, and required remote checks.

The full structured records, context classifications, judgments, and raw
excerpts are in `campaign.json`. The fixture remains reproducible: its prompts
and expected behavior are unchanged, while `runtime_results` now contains only
observed controller evidence.
