# Writing-style pressure evidence

## Method and boundary

Run date: 2026-08-25. Two agents ran sequentially in fresh contexts with the
new canonical `writing-style` guidance available. Each run could read only its
named scenario and the bounded skill files listed below. Neither agent edited
the repository.

These are instruction-following pressure checks, not statistical evidence of
reader preference, prose quality, human authorship, or detector accuracy. Task
1's unchanged RED baseline already passed both scenario rubrics. These GREEN
runs therefore document current route behavior and contract coverage; they do
not demonstrate a causal improvement from `writing-style`.

### Execution configuration

Both runs used Codex MultiAgentV2. Shared role: `reviewer`; named `.md` profile:
not applicable in Codex MultiAgentV2; model: `gpt-5.6-terra`; reasoning: high;
context: fresh (`fork_turns=none`). Model, reasoning, and `fork_turns` are the
complete exposed dispatch dimensions for these runs. The route follows
[`codex-multi-agent-v2-profile.md`](../../../codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/references/codex-multi-agent-v2-profile.md).

## Results

### `preserve-deliberate-device.md`

- **Agent task:** `/root/task_4_implementer/green_style_device`.
- **Route/model/profile:** Shared role: `reviewer`; named profile: not
  applicable; model: `gpt-5.6-terra`; reasoning: high; context: fresh
  (`fork_turns=none`).
- **Exact scenario path:**
  `tests/pressure/writing/prompts/preserve-deliberate-device.md`.
- **Skill files available:** `writing-style/SKILL.md`,
  `references/profile-contract.md`, and
  `references/profiles/fatigue/ai-prose-fatigue/profile.md`.
- **Fixture provenance:** Repository-authored public pressure fixture introduced
  in Task 1 and attributed only to a generic founder. The prompt does not state
  whether the note is wholly synthetic or adapted; no real identity or source
  corpus was supplied to this run. This unresolved provenance is a limitation,
  not permission to reuse the copy outside the test.
- **Response:**

  > We built this for the nights when the answer matters — when the team is waiting, the client is waiting, and you are waiting. We wanted one place to see the evidence, one place to make the call, one place to move.
  >
  > I reject a blanket “model-like pattern” removal rule. The em dash, waiting refrain, and final triad each carry the note’s urgency and progression; there is no concrete reader-cost reason to remove them.

- **Rubric judgment:** Pass (3/3). The response retained the em dash, waiting
  refrain, and final triad; explicitly rejected blanket removal; and added no
  error, choppiness, or random variation.
- **Observed limitation:** One run cannot establish that every legitimate
  device or audience context will be preserved.

### `voice-without-private-corpus.md`

- **Agent task:** `/root/task_4_implementer/green_style_voice`.
- **Route/model/profile:** Shared role: `reviewer`; named profile: not
  applicable; model: `gpt-5.6-terra`; reasoning: high; context: fresh
  (`fork_turns=none`).
- **Exact scenario path:**
  `tests/pressure/writing/prompts/voice-without-private-corpus.md`.
- **Skill files available:** `writing-style/SKILL.md`,
  `references/voice-card.md`, and
  `references/profiles/voice/voice-card.schema.json`.
- **Fixture provenance:** The prompt explicitly declares the paragraph synthetic
  public test copy, not a real person's text, private sample, or retained corpus.
- **Response:**

  ```json
  {
    "schema_version": 1,
    "profile_id": "current-task-brief-voice",
    "version": "1.0.0",
    "scope": {
      "task_boundary": "current_task",
      "genres": ["brief guidance"],
      "audiences": ["brief authors"]
    },
    "derivation": {
      "basis": "current_task_text",
      "authorization": "current_task_user",
      "sample_count": 1,
      "derived_at": "2026-08-25",
      "source_retained": false,
      "retention_boundary": "no_source_storage"
    },
    "tendencies": {
      "sentence_range": {
        "typical_min_words": 8,
        "typical_max_words": 14
      },
      "directness": "high",
      "vocabulary_register": ["plain", "domain-specific"],
      "tolerated_fragments": false,
      "rhetorical_devices": ["parallelism"],
      "formatting_norms": ["compact prose guidance"]
    },
    "choices": {
      "prefer": [
        "state the claim before its supporting evidence",
        "make uncertainty explicit",
        "retain room for qualification or complication"
      ],
      "avoid": [
        "unsupported certainty",
        "evidence-free assertions"
      ]
    },
    "limitations": [
      "Derived from one synthetic current-task sample only.",
      "Applies only to this task's brief-guidance context.",
      "Does not support identity, personality, authorship, or broader style claims."
    ]
  }
  ```

  > Retention note: The supplied text is used only for this task. It is not retained as a private corpus, sentence bank, or source for personal-trait inference.

- **Rubric judgment:** Pass (3/3). The response recorded bounded observable
  tendencies, declared task-only/no-source retention, and neither copied the
  supplied passage nor invented a person-level fact.
- **Observed limitation:** A single synthetic paragraph exercises schema shape
  and privacy boundaries, not robust voice inference across genres.

## Overall judgment

Both fresh-context runs passed their unchanged rubrics. Combined with the
all-pass/inconclusive Task 1 baseline, the evidence supports only a present
instruction-following result. It does not support a GREEN delta, causal
improvement claim, universal fatigue rule, or author-identification claim.
