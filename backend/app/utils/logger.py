"""
AutoSecAI — Structured Logger
==============================
Provides a pre-configured logger with coloured console output
and optional file output.

Usage:
    from app.utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Server started")
    logger.warning("Token missing")
"""

import logging
import os
import sys

# Log file lives at  backend/logs/autosecai.log
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LOG_DIR = os.path.join(_BASE_DIR, "logs")
_LOG_FILE = os.path.join(_LOG_DIR, "autosecai.log")

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ANSI colour codes for Windows / Unix terminals
_COLOURS = {
    "DEBUG": "\033[36m",     # cyan
    "INFO": "\033[32m",      # green
    "WARNING": "\033[33m",   # yellow
    "ERROR": "\033[31m",     # red
    "CRITICAL": "\033[1;31m",  # bold red
}
_RESET = "\033[0m"


class _ColouredFormatter(logging.Formatter):
    """Adds ANSI colour codes around the level name for console output."""

    def format(self, record: logging.LogRecord) -> str:
        colour = _COLOURS.get(record.levelname, "")
        record.levelname = f"{colour}{record.levelname}{_RESET}"
        return super().format(record)


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Return a logger named *name* with console + file handlers.

    Calling this multiple times with the same name returns the same logger
    (standard library behaviour).
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured — avoid duplicate handlers
        return logger

    logger.setLevel(level)

    # ── Console handler (coloured) ─────────────────────────────────────
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(_ColouredFormatter(_FORMAT, datefmt=_DATE_FORMAT))
    logger.addHandler(console)

    # ── File handler (plain text) ──────────────────────────────────────
    os.makedirs(_LOG_DIR, exist_ok=True)
    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATE_FORMAT))
    logger.addHandler(file_handler)

    return logger
