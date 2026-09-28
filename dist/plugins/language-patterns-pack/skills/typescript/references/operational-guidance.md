# TypeScript operational guidance

This reference distils TypeScript guidance from the TypeScript-Website `v2` documentation for day-to-day type design and project configuration.

## Type system basics

Use `string`, `number`, `boolean`, `bigint`, `symbol`, and `undefined`/`null` for primitives. Express arrays as `T[]` or `Array<T>`, tuples with fixed lengths and element types, and object shapes with object type literals. Prefer union types (`A | B`) for "either/or" values and intersection types (`A & B`) for combining shapes. Use literal types to narrow allowed constants.

## Interfaces and type aliases

Use `interface` for object shapes that may be merged or extended; use `type` aliases for unions, tuples, mapped types, and conditional types. Declare read-only properties with `readonly`, optional properties with `?`, and index signatures for dictionary-like objects.

## Generics and advanced types

Write generic functions and types when the same logic applies across multiple types. Use constraints (`T extends U`) to ensure a generic has the operations the implementation needs. Leverage mapped types to transform object shapes and conditional types to choose types based on a condition. Keep generic names short but meaningful (`T`, `K`, `V` when conventional).

## Type inference, narrowing, and type guards

Prefer `let`/`const` declarations without explicit annotations where TypeScript can infer the type. Use `typeof`, `instanceof`, `in`, and user-defined type predicates (`x is T`) to narrow unions. Avoid `any`; prefer `unknown` and assertion functions for unsafe boundaries.

## Declaration files and module resolution

Write `.d.ts` files to type external JavaScript or publish library types. Use `declare` for global variables and modules. Align `tsconfig.json` module resolution (`node`, `node16`, `nodenext`, `bundler`) with the runtime and build tooling. Keep `esModuleInterop` and `strict` on for new projects.

## TSConfig options and strictness

Enable `strict`, `noImplicitAny`, `strictNullChecks`, and `noImplicitReturns` to catch common errors. Use `skipLibCheck` selectively to speed builds when library types are trusted. Document intentional `any` with a comment and a plan to replace it.

## Module resolution and project references

Organize code into packages or `references` for composite projects. Use `baseUrl` and `paths` only when they simplify imports; prefer explicit relative or package imports. Keep `outDir` and `rootDir` aligned to avoid accidental output leakage.
