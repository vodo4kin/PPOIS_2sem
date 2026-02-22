from pathlib import Path

import pytest

from atm.config import Config


class TestConfig:
    def test_data_dir_is_path(self):
        assert isinstance(Config.DATA_DIR, Path)

    def test_atm_state_file_under_data_dir(self):
        assert Config.ATM_STATE_FILE == Config.DATA_DIR / "atm_state.json"

    def test_bank_accounts_file_under_data_dir(self):
        assert Config.BANK_ACCOUNTS_FILE == Config.DATA_DIR / "bank_accounts.json"

    def test_ensure_data_dir_creates_dir(self, temp_data_dir):
        Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        assert Config.DATA_DIR.exists()

    def test_constants(self):
        assert Config.MAX_PIN_ATTEMPTS == 3
        assert Config.PIN_LENGTH == 4
        assert Config.MIN_WITHDRAW_AMOUNT == 100
        assert Config.SESSION_TIMEOUT_SECONDS >= 1
        assert Config.DEFAULT_CURRENCY == "BYN"
        assert 100 in Config.ATM_CASH_DENOMINATIONS
