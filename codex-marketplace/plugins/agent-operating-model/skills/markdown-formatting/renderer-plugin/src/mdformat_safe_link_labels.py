"""mdformat extension that avoids needless escapes in plain link labels."""

from __future__ import annotations

from collections.abc import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render


def _preserve_plain_link_label_underscores(rendered: str, node: RenderTreeNode, _context: RenderContext) -> str:
    """Remove escapes only from labels whose parsed children are plain text."""
    if not node.children or any(child.type != "text" for child in node.children):
        return rendered

    closing = _link_label_closing_bracket(rendered)
    if closing is None:
        return rendered
    label = rendered[1:closing].replace(r"\_", "_")
    return f"[{label}]{rendered[closing + 1 :]}"


def _link_label_closing_bracket(rendered: str) -> int | None:
    if not rendered.startswith("["):
        return None
    depth = 0
    escaped = False
    for index, character in enumerate(rendered):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
        elif character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                return index
    return None


def update_mdit(_mdit: MarkdownIt) -> None:
    """The extension changes renderer output only, not parser semantics."""


RENDERERS: Mapping[str, Render] = {}
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "link": _preserve_plain_link_label_underscores,
}
