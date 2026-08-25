# Frozen writing-style A/B campaign

This subtree freezes one adversarial worker stimulus, its separate hidden judge
rubric, and the machine-readable campaign contract. Task 4 designs and freezes
the experiment but does not run either arm.

Before any output is generated, verify the SHA-256 pins for the stimulus,
hidden rubric, the complete treatment-readable writing-style and
writing-with-clarity route, and the evaluator goldens. Abort the campaign
without running a trial if any pin differs. Version 1.4.0 records the fourth
pre-output review correction; no worker output existed and no arm had run
before the prospective refreeze.

Task 5 must first build and validate the deterministic profile evaluator using
only the profile goldens. After engine GREEN, it may run the frozen campaign:
three fresh no-skill workers and three fresh workers with `writing-style`
explicitly available and invoked, all using the identical declared Codex V2
route. Workers may never read `hidden-rubric.md`, the manifest's scoring
thresholds, another worker's output, or an existing result.

The campaign can support a causal interpretation only if its predeclared
baseline RED and treatment GREEN thresholds both hold without degrading the
secondary preservation, clarity, factuality, and voice metrics. Otherwise its
verdict is inconclusive or non-discriminating. No skill, profile, engine,
evaluator, stimulus, rubric, or threshold may change after outputs are revealed
to make the campaign pass.
