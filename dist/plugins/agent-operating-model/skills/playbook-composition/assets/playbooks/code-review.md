# Code review concern

Use these principles whenever reviewing a change, whether review is a dedicated lifecycle stage or a check within another stage.

Assess the change against the requested behavior and its owning design. Prioritize defects that can break user-visible behavior, data integrity, security, or maintainability. Trace important paths through their callers and failure cases. Check whether tests establish behavior rather than mirror implementation, and whether claims in the change summary match the evidence. Keep findings specific, explain the consequence, and distinguish a defect from a preference or question.

This playbook describes review concerns and judgment. A code-review runbook, if present, owns the sequence from review request through disposition; this playbook can be routed from that stage and from other stages that need review.
