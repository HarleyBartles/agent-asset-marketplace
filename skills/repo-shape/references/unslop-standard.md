# Unslop Standard

## Purpose and authority

The Unslop standard is an optional Operating Model standard for consumer-owned operational profiles. It defines where a repository declares its profile roots and how its workflows route agents to applicable profiles. Adopting it does not require installation of Unslop+ or any other ambient plugin.

An operational profile helps an agent recognize and correct a recurring failure pattern. It is not repository policy, a checklist of historic mistakes, or a general ban on words and styles. Doctrine remains the source of binding rules. A profile may link to doctrine and skills but must not restate their binding requirements as profile rules.

The standard checks adoption configuration, profile structure, safe roots, local references, and workflow routing. These deterministic checks do not determine whether real work followed a profile. Real-work assessment remains profile-guided review unless a separate deterministic check explicitly owns that decision.

## Adoption contract

An adopting repository declares the standard in `.agents/contracts/operating-standards.json` and keeps its Unslop-specific settings in `.agents/contracts/unslop.json`:

```json
{
  "version": 1,
  "profile_roots": [".agents/unslop"]
}
```

`profile_roots` is a non-empty list of unique repository-relative directories. The default is `.agents/unslop`; repositories may add other safe roots. Roots may be absent or empty before any local profile is authored. `repo-standards --apply` creates only the missing default contract. It does not create a profile or overwrite a consumer-authored contract.

The Unslop catalog entry uses explicit legacy migration. Presence of a similarly named directory, a repo-shape surface, or an ambient plugin does not adopt the standard. Existing repositories select it deliberately in their operating-standards composition.

## Profile documents

Each profile is a Markdown file beneath one declared root. Its first heading identifies it with a stable kebab-case id:

```markdown
# Unslop Profile: evidence-first-plans
```

It has these non-empty sections:

- `Task trigger and scope`
- `Recurring failure pattern`
- `Recognition cues`
- `Corrective behavior`
- `False-positive and override boundaries`
- `Applicable workflow paths`
- `Doctrine and skill references`
- `Application example`

The workflow and reference sections contain Markdown links. Workflow links resolve to tracked repository files. Each routed workflow has an `Unslop profile routing` section that invokes `$unslop-profiles` at the relevant stage. Local links must resolve inside the repository. External authority links may remain external.

The standard validates these structural and routing obligations. It does not grade whether a pattern is useful, whether a cue is frequent enough, or whether an agent's correction was proportionate. Consumers keep profile wording operational, concrete, scoped, and subordinate to doctrine.

## Workflow use

An applicable runbook or playbook names `$unslop-profiles` in its `Unslop profile routing` section. The profile names the workflow paths in which its trigger may apply. Workflow routing is conditional: unrelated work does not acquire a global profile obligation.

At runtime, Unslop+ discovers profiles exposed by the declared consumer roots when that standard is adopted and may also use an applicable generic starter profile. Consumer profiles remain repository-owned operational guidance. When no profile fits, the agent skips profile application. Profile cues are evidence for judgment, not mechanical keyword bans; clarity, meaning, evidence, doctrine, user intent, and the profile's false-positive boundaries govern corrections.

## Profile lifecycle

Create a profile when recurring evidence reveals a durable opportunity to prevent a costly failure. Revise it when the failure pattern or effective intervention changes. Retire it when it has no reader or its guidance has been absorbed elsewhere. One mistake does not automatically modify a profile. The consumer reviews and decides proposed creation, revision, or retirement.

The Unslop engine can analyze samples and validate generated output packages. Those checks do not prove that an agent followed a profile. Profile adherence remains a review judgment unless a named deterministic check provides evidence for that specific claim.
