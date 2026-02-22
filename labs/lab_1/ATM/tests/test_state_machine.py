from unittest.mock import MagicMock

from atm.session_manager.state import State
from atm.session_manager.atm_state_machine import (
    ATMStateMachine,
    NoCardState,
    CardInsertedState,
    EnteringPINState,
    AuthenticatedState,
    WithdrawalState,
    SessionEndingState,
)
from atm.atm import ATM


class TestATMStateMachine:
    def test_initial_state_is_no_card(self):
        atm = ATM()
        assert atm.state_machine.current_state.__class__.__name__ == "NoCardState"

    def test_change_state(self):
        atm = ATM()
        fsm = atm.state_machine
        new_state = CardInsertedState(fsm)
        fsm.change_state(new_state)
        assert fsm.current_state.__class__.__name__ == "CardInsertedState"
