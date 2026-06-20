# DREAD Risk Assessment

DREAD is a risk assessment framework for quantifying threat severity.

## Criteria

Score each criterion from `0` to `10` and average the result.

- Damage potential: how much damage if exploited?
- Reproducibility: how easy is the attack to repeat?
- Exploitability: how much skill and tooling are required?
- Affected users: how many people or systems are impacted?
- Discoverability: how easy is the weakness to find?

## Interpretation

- `0.0` to `3.0`: low risk
- `3.1` to `5.0`: medium risk
- `5.1` to `7.0`: high risk
- `7.1` to `10.0`: critical risk

## Worksheet

```markdown
## Threat: [Threat Name]
### DREAD Scoring
- D: [0-10] damage potential
- R: [0-10] reproducibility
- E: [0-10] exploitability
- A: [0-10] affected users
- D: [0-10] discoverability
### Risk
- Score: ([D] + [R] + [E] + [A] + [D]) / 5
- Level: [Low/Medium/High/Critical]
```

