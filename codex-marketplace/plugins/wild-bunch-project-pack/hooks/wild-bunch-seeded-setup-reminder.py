from __future__ import annotations

import json
import os


REMINDER = (
    "Wild Bunch reminder: when a task touches seed, world setup, difficulty, "
    "entropy, inventory profile, rope, ammo, random rolls, shuffles, luck, "
    "travel, encounters, or gameplay decision loops, consult the installed "
    "`wild-bunch-project-doctrine` reference at "
    "`skills/wild-bunch-project-doctrine/references/"
    "difficulty-entropy-seeded-world-setup.md` before planning or review."
)


def main() -> None:
    payload: dict[str, object]
    if os.environ.get("CURSOR_PLUGIN_ROOT"):
        payload = {"additional_context": REMINDER}
    elif os.environ.get("CLAUDE_PLUGIN_ROOT") and not os.environ.get("COPILOT_CLI"):
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": REMINDER,
            }
        }
    else:
        payload = {"additionalContext": REMINDER}

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
