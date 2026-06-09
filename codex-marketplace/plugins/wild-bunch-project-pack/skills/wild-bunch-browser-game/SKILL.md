---
name: wild-bunch-browser-game
description: Bridge Wild Bunch to the browser-game marketplace stack, QA flow, and agent-browser verification.
---

# Wild Bunch Browser Game

## Overview

Use this skill when the task touches browser delivery, HUD design, or playtest
verification. The default browser-game route stays Phaser, TypeScript, and Vite
with a DOM HUD unless the issue explicitly chooses another stack.

## Rules

- Use the existing `game-studio` plugin as the browser-game reference pack.
- Default to Phaser/TypeScript/Vite plus DOM HUD unless the issue says
  otherwise.
- Browser rendering adapts authoritative game state and emits player commands;
  it must not become game truth.
- Use `web-game-foundations` for simulation, render, UI, and save boundaries.
- Use `phaser-2d-game` for the 2D implementation shape.
- Use `game-ui-frontend` for HUD, menu, and overlay direction.
- Use `game-playtest` plus screenshots for browser QA.
- Use `agent-browser` from the Vercel plugin where installed for dev-server
  verification and screenshot-based QA.

## References

- [Browser-game stack notes](references/browser-game-stack.md)
