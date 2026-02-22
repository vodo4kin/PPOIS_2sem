from abc import ABC, abstractmethod
from typing import Any


class State(ABC):
    """Base class for all ATM states."""

    def __init__(self, context: Any) -> None:
        self.context = context

    @abstractmethod
    def handle(self) -> None:
        """Handle the current state logic."""
        pass

    def on_enter(self) -> None:
        """Called when entering this state."""
        pass

    def on_exit(self) -> None:
        """Called when exiting this state."""
        pass
