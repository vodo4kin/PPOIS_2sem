from unittest.mock import MagicMock, patch

import pytest

from atm.atm import ATM


class TestATMIntegration:
    def test_atm_creates_and_has_state_machine(self):
        atm = ATM()
        assert atm.state_machine is not None
        assert atm.state_machine.current_state.__class__.__name__ == "NoCardState"

    def test_atm_has_incassator_and_technician_components(self):
        atm = ATM()
        assert atm.cash_replenisher is not None
        assert atm.cash_collector is not None
        assert atm.reboot_controller is not None
        assert atm.retained_card_collector is not None

    def test_run_exit_choice(self):
        atm = ATM()
        with patch.object(atm.display, "ask_input", side_effect=["4"]):
            atm.run()
        atm.logger.close()
