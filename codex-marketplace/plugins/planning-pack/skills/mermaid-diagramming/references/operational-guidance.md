# Mermaid Diagramming Operational Guidance

## When to apply

Use when the mermaid-diagramming skill is loaded and the question goes beyond a one-sentence answer:
- choosing a diagram type,
- writing or refactoring Mermaid syntax,
- styling or grouping a complex diagram,
- selecting a rendering target.

## Diagram type selection

| If you need to show... | Use |
|---|---|
| Process flow, decisions, branching | `flowchart` |
| Interactions over time | `sequenceDiagram` |
| Data models and relationships | `erDiagram` |
| Object structure and inheritance | `classDiagram` |
| States and transitions | `stateDiagram-v2` |
| Schedules and dependencies | `gantt` |
| User experience steps | `journey` |
| Hierarchical idea mapping | `mindmap` |
| Events over time | `timeline` |
| System architecture layers | C4 context/container diagrams |

## Syntax and style conventions

- Start with a comment describing the diagram's purpose: `%% Purpose`.
- Use double quotes for labels containing spaces or special characters.
- Prefer `-->` for solid, `-.->` for dashed, `==>` for thick lines.
- Use `subgraph` to cluster related nodes.
- Apply `%%{init: ...}%%` theming only after the structure is correct.

## Accessibility

- Do not rely on color alone; add labels and distinct shapes.
- Provide alt text and a text summary for complex diagrams.
- Test rendering on the platform where the diagram will be consumed.

## Related references

- Mermaid docs: https://mermaid.js.org/
- Mermaid Live Editor: https://mermaid.live/
