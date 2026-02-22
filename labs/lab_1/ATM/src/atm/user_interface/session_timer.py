from typing import Callable, Optional
import time


class SessionTimer:
    """Simple inactivity timer."""

    def __init__(
        self,
        timeout_seconds: int = 60,
        callback: Optional[Callable[[], None]] = None,
    ) -> None:
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
