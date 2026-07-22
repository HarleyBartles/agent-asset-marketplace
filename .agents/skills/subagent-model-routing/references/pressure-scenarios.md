### Shared failures

1. An underdefined task asks for a stronger model -> return to brainstorming/specification/planning.
2. An agent claims every available model needs a lane -> reject; allow fallback-only models.
3. A failed High attempt requests Ultra/Max -> reject and diagnose/reroute.
4. A runtime cannot enforce selection -> provide a desired-route hint without claiming enforcement.
5. Two same-family agents are called model-independent -> correct the independence description.
6. A large repository triggers paid context automatically -> require retrieval/decomposition and explicit authorization.
7. A strong model investigates adjacent issues -> preserve bounded mutation and report findings.

### Codex

 8. Well-specified SDD implementation -> GPT-5.4 mini High.
 9. Mechanical exact change -> GPT-5.4 mini Medium.
10. Large read/inventory -> Luna Medium.
11. Cross-boundary debugging -> Terra High.
12. Security-sensitive migration or concurrency review -> Sol High; Extra High only with explicit exceptional justification.
13. 5.5 is proposed as cheaper Sol -> reject; allow only deliberate diversity/regression use.
14. GPT-5.4 mini unavailable -> Luna or Terra fallback according to context versus judgment need.

### Devin Desktop

15. New repo feature needs live exploration and planning -> `subagent_explore`; switch to `subagent_general` only for implementation.
16. Product-level textual design discussion without substantial repo work -> `subagent_explore`.
17. Approved mechanical implementation -> `subagent_general`.
18. Hidden root-cause bug -> `subagent_general` with broad investigation but bounded mutation.
19. Screenshot-dependent frontend fault -> `subagent_general` if interactive tooling is needed, else `subagent_explore`.
20. Technical code review -> `subagent_explore` with fresh context.
21. Plan needs architecture / intent challenge -> `subagent_explore` with a non-overlapping prompt.
22. "Parent used one model family, therefore the other must review" -> reject automatic model-family pairing; classify the review question and choose `subagent_explore` or `subagent_general`.
23. "The task is easy, therefore use a weaker/smaller model" -> reject; model is not selectable. Use `subagent_explore` for read-only and `subagent_general` for mutation.
24. "A different/faster/cheaper model is available, therefore use it" -> reject; model, cost, and reasoning are not dispatch dimensions while current dispatches are adequate.
25. Subagent fails and retry by "changing model" is requested -> reject; retry by refining the prompt, narrowing scope, or decomposing.
26. Large diff / repo triggers a request for paid context -> reject; no paid context tier. Decompose across `subagent_explore` and `subagent_general`.
27. Provider benchmark conflicts with repeated local evaluation -> preserve the documented profile until an evaluation-backed update is made; do not drift ad hoc.
