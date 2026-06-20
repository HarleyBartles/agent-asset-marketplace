---
name: threat-modeling-techniques
description: Threat modeling methodologies using STRIDE, attack trees, and risk assessment for proactive security analysis.
keywords:
  - STRIDE
  - attack surface
  - attack tree
  - risk assessment
  - security architecture
  - security design
  - threat analysis
  - threat landscape
  - threat modeling
  - vulnerability analysis
file_patterns:
  - "**/*secret*.py"
  - "**/*secret*.ts"
  - "**/auth/**"
  - "**/security/**"
confidence: 0.82
metadata:
  source_author: NickCrew
  source_license: MIT
  source_repo: https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques/SKILL.md
  content_mode: normalised
---

# Threat Modeling Techniques

Use this retained custody slice to frame attack surfaces, abuse cases, trust
boundaries, and design-time security controls before implementation hardens the
architecture.

## When to Use This Skill

- designing new systems or features with security requirements;
- conducting security architecture reviews;
- identifying attack vectors and threat scenarios;
- assessing security risks before implementation;
- creating security requirements and controls;
- evaluating third-party integrations for security impact;
- planning security testing strategies;
- documenting security design decisions; or
- training teams on proactive security thinking.

## Quick Reference

| Topic | Load reference |
| --- | --- |
| STRIDE: Spoofing Identity | `references/stride-spoofing.md` |
| STRIDE: Tampering with Data | `references/stride-tampering.md` |
| STRIDE: Repudiation | `references/stride-repudiation.md` |
| STRIDE: Information Disclosure | `references/stride-disclosure.md` |
| STRIDE: Denial of Service | `references/stride-dos.md` |
| STRIDE: Elevation of Privilege | `references/stride-elevation.md` |
| Attack Trees | `references/attack-trees.md` |
| Data Flow Diagrams | `references/data-flow-diagrams.md` |
| DREAD Risk Scoring | `references/dread-scoring.md` |
| Mitigation Strategies | `references/mitigation-strategies.md` |
| Tools and Process | `references/tools-and-process.md` |
| Validation rubric | `validation/rubric.yaml` |

## Core Process

1. define the system and the scope of analysis;
2. identify threats with STRIDE and attack trees;
3. assess impact and likelihood with DREAD or a project-specific rubric;
4. design mitigations that reduce or eliminate the threat; and
5. validate the controls with security review and testing.

## STRIDE

STRIDE is the fast way to pressure-test a design:

- Spoofing: identity or session impersonation;
- Tampering: malicious modification of data;
- Repudiation: denial without sufficient evidence;
- Information disclosure: unauthorized data exposure;
- Denial of service: resource exhaustion or unavailability; and
- Elevation of privilege: unauthorized capability gain.

Apply STRIDE to every process, data flow, data store, and trust boundary.

## Attack Trees

Use attack trees when one threat goal can be reached by multiple paths.
Model the attacker goal at the root, use `OR` branches for alternative paths,
and use `AND` branches for required steps.

## DREAD

DREAD is a simple way to score a threat when you need a shared severity view.
Score damage, reproducibility, exploitability, affected users, and
discoverability, then use the average to rank the work.

## Mitigation Planning

Prefer the smallest effective control:

- eliminate the attack surface when the feature is not necessary;
- reduce the likelihood or impact with controls and constraints;
- transfer the risk to a stronger external service when that is justified;
- accept the risk only with explicit approval and monitoring.

## Practical Workflow

### 1. Scope Definition

- identify in-scope components;
- define trust boundaries;
- list assets that need protection; and
- note any compliance or business constraints that affect the design.

### 2. Architecture Decomposition

- draw data flow diagrams;
- map external dependencies;
- identify authentication and authorization points; and
- document data storage locations.

### 3. Threat Identification

- apply STRIDE to each diagram element;
- create attack trees for high-value assets;
- capture abuse cases with developers, architects, and security reviewers; and
- use tooling only to accelerate the human analysis.

### 4. Risk Assessment

- score the threats;
- rank the highest-risk paths;
- separate quick wins from longer-term work; and
- record the assumptions behind each score.

### 5. Mitigation and Validation

- design controls that are testable;
- assign owners for the changes;
- verify the controls in code review and security testing; and
- keep the threat model current when the design changes.

## Common Mistakes

- doing threat modeling after the implementation has hardened;
- focusing only on external attackers;
- creating static models that never get updated;
- over-complicating the diagrams;
- ignoring low-likelihood, high-impact threats; and
- failing to follow through on mitigations.

## Resources

- `references/attack-trees.md`
- `references/data-flow-diagrams.md`
- `references/dread-scoring.md`
- `references/mitigation-strategies.md`
- `references/tools-and-process.md`
- `validation/rubric.yaml`

