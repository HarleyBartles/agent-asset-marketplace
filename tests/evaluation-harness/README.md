# Evaluation harness tests

This suite tests the shared pressure-campaign runner and scanner under `tools/`. Run it when changing those tools:

```powershell
py -3 -m pytest tests/evaluation-harness -q
```

Each skill owns its pressure cases under `skills/<skill-id>/tests/pressure/`. The builder carries those cases into plugins that include the skill. Run pressure evaluations explicitly in an isolated context; record current findings in the handoff. Generated responses, scores, transcripts, and run metadata belong in ignored `runs/` or external scratch, not in Git.

The commit and PR gate does not run this suite or launch model evaluations.
