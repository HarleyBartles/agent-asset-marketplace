---
name: mermaid-diagramming
description: Use when selecting, writing, or reviewing Mermaid diagrams for technical documentation.
metadata:
  source-id: mermaid-diagramming
  source-path: codex-marketplace/plugins/planning-pack/skills/mermaid-diagramming/SKILL.md
  provenance-name: Mermaid Diagramming first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when selecting, writing, or reviewing Mermaid diagrams for technical documentation.
  use_when:
  - Use when selecting a diagram type for a process, interaction, data model, or state machine.
  - Use when writing or reviewing Mermaid syntax in documentation.
  do_not_use_when:
  - Do not use when the audience needs interactive or pixel-perfect visuals that Mermaid cannot provide.
  related_skills:
  - clean-architecture
  - api-design
  - writing-with-clarity
license: MIT
---

# Mermaid Diagramming

## Overview

Express technical diagrams as plain text inside docs, ADRs, and READMEs so they stay versioned and easy to update.

## When to Use

- Selecting a diagram type for a process, interaction, data model, or state machine.
- Writing or reviewing Mermaid syntax in documentation.
- Do not use when the audience needs interactive or pixel-perfect visuals that Mermaid cannot provide.

## Core Pattern

1. Choose the diagram type by what you want to show:
   - `flowchart` for processes and decisions.
   - `sequenceDiagram` for actor interactions over time.
   - `erDiagram` for data relationships.
   - `classDiagram` for object structure and inheritance.
   - `stateDiagram-v2` for state transitions.
   - `gantt` for schedules.
   - `journey`, `mindmap`, or `timeline` for UX flows, idea maps, or chronology.
2. Declare the diagram with the type keyword and keep one concept per diagram.
3. Use descriptive node IDs and quoted labels for special characters; prefer `LR` or `TB` direction.
4. Group related nodes with `subgraph` and label edges with `-->|"reason"|`.
5. Provide a basic and a styled version, plus a note about the target renderer such as GitHub, Mermaid Live Editor, or VS Code.

## Common Mistakes

- Overloading a single diagram with 15+ nodes → split into focused views.
- Relying on color alone to convey meaning → add labels and shapes.
- Committing diagrams without rendering them on the target platform → verify before committing.

Load `references/operational-guidance.md` for detailed diagram selection and syntax guidance.
