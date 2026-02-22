# Пока заглушка
from typing import Any
from .state import State


class ATMStateMachine:
    """Finite state machine for ATM behavior."""

    def __init__(self, initial_state: State) -> None:
        self.current_state: State = initial_state
        self.current_state.on_enter()

    def change_state(self, new_state: State) -> None:
        """Transition to new state."""
        self.current_state.on_exit()
        self.current_state = new_state
        self.current_state.on_enter()

    def handle(self) -> None:
        """Execute current state's logic."""
        self.current_state.handle()
