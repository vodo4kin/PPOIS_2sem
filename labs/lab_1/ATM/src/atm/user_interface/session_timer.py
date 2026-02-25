"""Inactivity timer and timeout-aware input for the ATM."""

from __future__ import annotations

import sys
import time
from typing import Callable, Optional

try:
    from select import select
    _SELECT_AVAILABLE = True
except ImportError:
    _SELECT_AVAILABLE = False


def read_line_with_timeout(  # pragma: no cover - interactive/timeout path
    prompt: str,
    timer: SessionTimer,
) -> Optional[str]:
    """Read a line from stdin; return None on inactivity timeout (calls timer callback)."""
    if prompt:
        print(prompt, end="", flush=True)
    if not _SELECT_AVAILABLE:
        try:
            line = input().strip()
            timer.reset()
            return line
        except EOFError:
            return None
    while True:
        try:
            rlist, _, _ = select([sys.stdin], [], [], 1.0)
        except (ValueError, OSError):
            try:
                line = input().strip()
                timer.reset()
                return line
            except EOFError:
                return None
        if rlist:
            line = sys.stdin.readline()
            if line is not None:
                timer.reset()
                return line.strip()
        if time.time() - timer.last_activity > timer.timeout:
            if timer.callback is not None:
                timer.callback()
            return None


class SessionTimer:
    """Simple inactivity timer."""

    def __init__(
        self,
        timeout_seconds: int = 60,
        callback: Optional[Callable[[], None]] = None,
    ) -> None:
        """Set timeout in seconds and optional callback on timeout."""
        self.timeout = timeout_seconds
        self.callback: Optional[Callable[[], None]] = callback
        self.last_activity = time.time()

    def reset(self) -> None:
        """Reset the inactivity timer."""
        self.last_activity = time.time()

    def check_timeout(self) -> bool:
        """Check if timeout has occurred and call callback if set."""
        if time.time() - self.last_activity > self.timeout:
            if self.callback is not None:
                self.callback()
            return True
        return False
