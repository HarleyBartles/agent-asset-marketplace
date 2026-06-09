# Browser Game Stack Notes

- Use the `game-studio` plugin as the primary browser-game reference pack.
- Default to Phaser, TypeScript, and Vite with a DOM HUD.
- Keep the renderer authoritative only for presentation.
- Keep the simulation authoritative for game truth.
- Use `web-game-foundations`, `phaser-2d-game`, `game-ui-frontend`, and
  `game-playtest` as the supporting local patterns.
- Use `agent-browser` from the Vercel plugin for dev-server verification and
  screenshot-based QA when it is installed.
