# Feature-Sliced Design Source Custody Record

> Issue: MARK-290
> Scope: third-party source custody for upstream Feature-Sliced Design skill
> Upstream repo: `https://github.com/feature-sliced/skills`
> Upstream commit: `653e7f3187eac51311652bf787a72bcf56325eea`
> Upstream license: `MIT` (declared in README.md)
> Total skills vendored: `1` (`feature-sliced-design`)

## Summary

This record captures verbatim source custody for the `feature-sliced-design`
skill from the upstream `feature-sliced/skills` repository. The skill teaches
AI coding agents Feature-Sliced Design (FSD) v2.1 architectural methodology
for frontend projects.

## Skill inventory

| Skill | Description |
| --- | --- |
| `feature-sliced-design` | Official FSD v2.1 skill for structuring frontend projects with layers, slices, and segments |

## Source structure

```
sources/third_party/feature-sliced/upstream/
├── source-custody.md       (this file)
├── LICENSE
├── manifest.json
└── skills/
    └── feature-sliced-design/
        ├── SKILL.md
        └── references/
            ├── asset-handling.md
            ├── cross-import-patterns.md
            ├── excessive-entities.md
            ├── framework-integration.md
            ├── layer-structure.md
            ├── migration-guide.md
            └── practical-examples.md
```

## Notes

- The upstream repo declares MIT license in its README but does not include a
  standalone LICENSE file. A LICENSE file has been generated from the MIT
  declaration for custody compliance.
- All skill content is copied verbatim from the upstream snapshot.
- The upstream repo uses `master` as its default branch.
