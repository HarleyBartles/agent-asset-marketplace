# Boring Contract

Use this reference for formal `boring-buster` runs.

## Terminal states

`GREEN`: the target is boring for the selected lane. Requires full gates plus golden-gate falsification. Never shortcut to GREEN.

`RED`: the target is proven not becoming boring today. Include what would make it amber later.

`AMBER_UNRESOLVED`: the target remains unresolved because GREEN and RED cannot be proven. Neutral, not blame.

`BLOCKED`: assessment or shaping cannot proceed lawfully because source, authority, tooling, or required user steer is unavailable.

## Preflight outcomes

Allowed preflight verdicts: `GREENABLE_TODAY`, `RED_SHORTCUT`, `BLOCKED`, `NEEDS_USER_STEER`. Preflight may shortcut to RED or BLOCKED. It may never shortcut to GREEN.

## Boring-enough lanes

`right_now`: current actor can implement now without hidden missing decisions, source gaps, or validation/closeout surprises.

`linear_worker_next`: a Linear issue is ready for a future worker only if the golden gate proves the work is repo-executable, environment/setup expectations are adequate, return evidence can be read from Linear/GitHub, and `writing-plans` has confirmed the implementation-plan shape.

`gpt_native_skillwork`: the work belongs in the ChatGPT skill stack unless a versioned repo source target is proven.

`next_actor`: later actor can implement from durable context alone without reconstructing this conversation.

`proposal`: idea is shaped enough as a proposal and identifies the durable artifact or authority needed before implementation.

`legacy_plan_b`: old-style non-Linear worker packet is appropriate only after Linear/default worker flow is unavailable, unsuitable, or explicitly rejected.

## Required gates for GREEN

All applicable gates must be green or explicitly not applicable:

- target fit;
- ambiguity;
- invariant;
- architecture/seam;
- validation ladder;
- closeout proof;
- route suitability;
- interest extraction;
- durable pickup when lane requires it;
- writing-plans implementation-shape gate for Linear worker coding issues;
- golden-gate falsifier.

## Writing-plans implementation-shape gate

For a Linear issue intended to be worker-send-ready for repo or code execution, GREEN requires a `writing-plans` pass unless the issue is explicitly discovery/planning-only.

The issue must give the next engineer:

- one observable implementation goal;
- likely changed files or exact source seams;
- small executable steps or a clearly selected implementation route;
- validation commands or acceptable validation evidence;
- protected non-goals;
- expected return evidence;
- no placeholders or hidden replanning requirement.

If this cannot be stated without guessing, return `AMBER_UNRESOLVED` or repair the issue before GREEN.

## Active gate repair

When a gate's non-green condition has a deterministic, lawful, authorized, local repair inside the selected lane, do that repair or recommend the exact repair and rerun the relevant gate.

Receipt repair may move AMBER to GREEN only when durable context is the only blocker, the correct durable home is known, current authority covers writing there, and rerun gates plus golden-gate pass.

## Golden-gate falsifier

After local gates appear green, ask how the GREEN can be disproven:

- Does one gate rely on another unresolved assumption?
- Does the chosen worker route actually access the editable target?
- Does worker readiness depend on plugin/environment/setup state not proven or not required in the issue?
- Does validation prove local correctness but not issue-goal conformance?
- Does closeout proof depend on worker intent rather than observable state?
- Does GREEN depend on session-only knowledge for a later pickup lane?
- Is durable issue ceremony being required for right-now work that will complete in-session?
- Is a proposal being treated as implementation-authorized?
- Is GPT-native installed-skill work being routed to a repo worker without repo source?
- Is a Linear worker coding issue marked ready without a `writing-plans` implementation-shape pass?

If any material falsifier succeeds, repair and rerun or return RED, AMBER_UNRESOLVED, or BLOCKED.

## Formal output fields

Use prose, a small table, or JSON unless YAML is explicitly requested. Include:

- target;
- lane;
- result;
- terminal state;
- decisive gate;
- terminal reason;
- next move;
- preserved context;
- route summary when implementation is involved.
