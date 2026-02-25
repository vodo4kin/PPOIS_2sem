"""Current ATM session (type, user, start time)."""

import datetime
from typing import Optional

from .session_type import SessionType


class Session:
    """Represents current ATM session."""

    def __init__(self) -> None:
        """Create inactive session."""
        self.session_type: Optional[SessionType] = None
        self.user_id: Optional[str] = None
        self.start_time: Optional[datetime.datetime] = None
        self.is_active: bool = False

    def start(self, session_type: SessionType, user_id: str) -> None:
        """Start session with given type and user id."""
        if self.is_active:
            raise RuntimeError("Session already active")
        self.session_type = session_type
        self.user_id = user_id
        self.start_time = datetime.datetime.now()
        self.is_active = True

    def end(self) -> None:
        """End session and clear state."""
        if not self.is_active:
            return
        self.session_type = None
        self.user_id = None
        self.start_time = None
        self.is_active = False

    def __str__(self) -> str:
        """Human-readable session description."""
        if not self.is_active:
            return "No active session"
        if self.session_type is None:
            raise RuntimeError(
                "Session is active, but session_type is None — invariant violation"
            )
        return f"Session({self.session_type.name}, user={self.user_id}, started={self.start_time})"
