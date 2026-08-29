"""
AutoSecAI — Timing Decorator
=============================
Logs the wall-clock execution time of any function.

Usage:
    from app.utils.timing import timed

    @timed
    def my_slow_function():
        ...
"""

import functools
import time

from app.utils.logger import get_logger

_logger = get_logger("autosecai.timing")


def timed(func):
    """
    Decorator that logs the execution time of *func*.

    Works with both sync and async functions (sync only for now).
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            _logger.info("%s completed in %.2f s", func.__qualname__, elapsed)
        return result

    return wrapper
