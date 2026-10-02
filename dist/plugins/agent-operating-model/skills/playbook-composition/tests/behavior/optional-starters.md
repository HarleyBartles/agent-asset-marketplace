# Optional playbook starter behavior cases

Use these cases to assess adoption decisions and category boundaries, not exact wording or heading structure.

## Case A: playbook standard alone

A repository has recurring testing and security concerns but no runbooks or doctrine/contracts store. It adopts only `playbook-composition` and asks which AOM files it must install.

## Case B: review concern across stages

A repository has a code-review runbook that describes requesting, conducting, resolving, and closing a review. Implementation and planning work also need review principles. AOM offers a code-review playbook.

## Case C: compose selected stages and concerns

A repository adopts both standards and selects design and implementation runbooks plus testing and security playbooks. Not every task needs security review.

## Expected decisions

- Case A can carry the necessary concern guidance in its selected playbooks, link only real available references, and route them through whatever agent-facing entrypoint it owns. No runbook or doctrine/contracts standard is implied. All AOM examples are optional.
- Case B keeps the lifecycle of review in the runbook and uses the playbook for reusable review judgment across stages. Neither document is a substitute for the other's category.
- Case C routes only applicable concerns from each selected stage or task. Testing may be useful broadly while security is conditional; no all-to-all routing or fixed minimum inventory follows from adoption.
- Structural checker success never establishes semantic usefulness, correct category, or effective runtime routing.
