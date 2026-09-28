# Model routing with Jev

Use `jev_route_model` only after the task owner authorizes a child and `selecting-a-subagent` has identified the live dispatch contract. The model route is advisory; reasoning effort and context mode remain separate choices.

1. Read the live child model IDs and supported reasoning values. Exclude models or route combinations the runtime cannot invoke. Apply hard policy before the call. In Codex V2, Astra is exceptional: include it only when a concrete, described integration need demonstrates why Sol is inadequate, and never use Astra above `low` reasoning. Do not let Jev decide whether to relax that rule.
2. If fewer than two eligible models remain, choose under `selecting-a-subagent` without a Jev call. If the task is underdefined, clarify or shape it before routing.
3. Send `task` as a compact task description and `candidates` as objects with exact live `id` and accurate `description`. Include binding `constraints`; put `priorities` in the intended order when the task establishes them. Set `stakes` by the consequence of choosing an inadequate model, not by task size. Describe cost, latency, context, and tool support only when the runtime or another reliable source actually supplies those facts. Do not infer entitlement from a model name.
4. Accept only a returned candidate ID from the supplied set. Recheck live availability, policy, reasoning, and context restrictions immediately before dispatch. A supplied model can still conflict with `selecting-a-subagent`'s least escalated adequate rule; when task evidence establishes that conflict, follow the local rule and record why Jev's recommendation was overridden. If the response includes an `escalate` signal, treat it as a prompt to consider the owning workflow's appropriate independent check or human review; it does not authorize a stronger model or add an automatic review requirement. If the result is uncertain, malformed, unavailable, or conflicts with policy, use the existing deterministic/manual route and record why.

For `spawn_agent` with `fork_turns`, `"all"` inherits the parent model and reasoning and cannot enforce a different model. Choose a bounded brief with `"none"` or a positive turn count when an override is needed. Record the selected model, reasoning, context mode, and whether Jev advised the model choice. A Jev response does not imply the child was launched.

Example request shape (replace descriptions with supported facts for the current runtime):

```json
{
  "task": "Focused review of a small, well-scoped code correction",
  "candidates": [
    {"id": "gpt-6-luna", "description": "Exposed model for bounded focused work"},
    {"id": "gpt-6-sol", "description": "Exposed model for normal implementation and review"}
  ],
  "constraints": ["Choose the least escalated adequate route"]
}
```
