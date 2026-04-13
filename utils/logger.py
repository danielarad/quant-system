"""
utils/logger.py
---------------
Lightweight logging utility.

Replaces raw print() calls with structured, level-aware log messages.
Design rationale: keep it simple for now (no external deps), but use
a consistent interface so it can later be swapped for Python's logging
module or a structured logger (structlog, loguru) without touching callers.

Usage:
    from utils.logger import log
    log("info", "MetaAgent", "Routing to Quant Agent")
    log("error", "DataLoader", "API timeout")
"""

from datetime import datetime, timezone


# Log level display config — controls output format
_LEVELS = {
    "info":    "[INFO ]",
    "warning": "[WARN ]",
    "error":   "[ERROR]",
    "debug":   "[DEBUG]",
}


def log(level: str, source: str, message: str) -> None:
    """
    Print a formatted log message to stdout.

    Args:
        level:   One of 'info', 'warning', 'error', 'debug'.
        source:  The module or agent name producing the log (e.g. 'MetaAgent').
        message: Human-readable description of the event.

    Example output:
        [2025-01-15 14:23:01 UTC] [INFO ] [DataLoader] Fetched BTC price: $83,412.50
    """
    level_tag = _LEVELS.get(level.lower(), "[LOG  ]")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {level_tag} [{source}] {message}")


def log_separator(label: str = "") -> None:
    """
    Print a visual separator line — useful for grouping agent output.

    Args:
        label: Optional label displayed at the center of the separator.
    """
    if label:
        padding = (50 - len(label) - 2) // 2
        print(f"{'─' * padding} {label} {'─' * padding}")
    else:
        print("─" * 54)
