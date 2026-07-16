"""Icon system for Terminal UI - Unicode icons with guaranteed compatibility."""

from __future__ import annotations


class Icons:
    """Unicode icons for terminal UI - guaranteed compatibility."""

    # Status indicators
    SUCCESS = "✓"
    READY = "○"
    RUNNING = "⏳"
    ERROR = "✗"
    WARNING = "⚠"
    INFO = "ℹ"
    BLOCKED = "🚫"
    METRICS = "📊"

    # Navigation
    SELECTED = "▶"
    UNSELECTED = " "
    ARROW_RIGHT = "→"
    ARROW_LEFT = "←"
    ARROW_DOWN = "↓"
    ARROW_UP = "↑"
    CLOCK = "🕒"

    # File types
    FILE = "📄"
    FOLDER = "📁"
    CODE = "💻"
    TEST = "🧪"
    DOC = "📝"
    DOCUMENT = "📄"

    # Actions
    PLAY = "▶"
    PAUSE = "⏸"
    STOP = "⏹"
    REFRESH = "↻"
    SYNC = "🔄"
    SEARCH = "🔍"
    FILTER = "⚑"

    # Progress
    COMPLETE = "█"
    INCOMPLETE = "░"
    BULLET = "•"
    HEART = "❤"

    # Connectors (for trees/hierarchies)
    BRANCH = "├─"
    LAST_BRANCH = "└─"
    PIPE = "│"
    SPACE = "  "


class StatusIcon:
    """Smart status icon with color - works with both Rich and Textual markup."""

    @staticmethod
    def active() -> str:
        """Active status with green checkmark."""
        return f"[green]{Icons.SUCCESS}[/green] Active"

    @staticmethod
    def inactive() -> str:
        """Inactive/ready status with dimmed circle."""
        return f"[dim]{Icons.READY}[/dim] Ready"

    @staticmethod
    def running() -> str:
        """Running status with yellow hourglass."""
        return f"[yellow]{Icons.RUNNING}[/yellow] Running"

    @staticmethod
    def error() -> str:
        """Error status with red X."""
        return f"[red]{Icons.ERROR}[/red] Failed"

    @staticmethod
    def warning() -> str:
        """Warning status with yellow warning sign."""
        return f"[yellow]{Icons.WARNING}[/yellow] Warning"

    @staticmethod
    def pending() -> str:
        """Pending status with dimmed circle."""
        return f"[dim]{Icons.READY}[/dim] Pending"
