from typing import Optional
from .session_type import SessionType
import datetime


class Session:
    """Represents current ATM session."""

    def __init__(self) -> None:
        self.session_type: Optional[SessionType] = None
        self.user_id: Optional[str] = None
        self.start_time: Optional[datetime.datetime] = None
        self.is_active: bool = False

    def start(self, session_type: SessionType, user_id: str) -> None:
        """Start new session."""
        if self.is_active:
            raise RuntimeError("Session already active")
        self.session_type = session_type
        self.user_id = user_id
        self.start_time = datetime.datetime.now()
        self.is_active = True

    def end(self) -> None:
        """End current session."""
        if not self.is_active:
            raise RuntimeError("No active session")
        self.session_type = None
        self.user_id = None
        self.start_time = None
        self.is_active = False

    def __str__(self) -> str:
        if not self.is_active:
            return "No active session"
        if self.session_type is None:
            raise AssertionError("Session type is missing")
        return f"Session({self.session_type.name}, user={self.user_id}, started={self.start_time})"
