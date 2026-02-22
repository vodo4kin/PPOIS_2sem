from decimal import Decimal

import pytest

from atm.bank_communication.account_data import AccountData
from atm.bank_communication.mock_bank_repo import MockBankRepository


class TestMockBankRepository:
    def test_seed_created_when_empty(self, temp_data_dir):
        repo = MockBankRepository()
        accounts = repo.get_all_accounts()
        assert len(accounts) >= 5
        assert "1234567890123456" in accounts
        assert "9999999999999999" in accounts
        assert "1000000000000001" in accounts
        assert "1000000000000002" in accounts

    def test_get_account(self):
        repo = MockBankRepository()
        acc = repo.get_account("1234567890123456")
        assert acc is not None
        assert acc.card_number == "1234567890123456"
        assert acc.is_blocked is False
        assert acc.expiry_date is not None

    def test_get_account_blocked(self):
        repo = MockBankRepository()
        acc = repo.get_account("9999999999999999")
        assert acc is not None
        assert acc.is_blocked is True

    def test_validate_pin(self):
        repo = MockBankRepository()
        assert repo.validate_pin("1234567890123456", "0000") is True
        assert repo.validate_pin("1234567890123456", "9999") is False

    def test_update_balance(self):
        repo = MockBankRepository()
        assert repo.update_balance("1234567890123456", Decimal("5000")) is True
        assert repo.get_account("1234567890123456").balance == Decimal("5000")

    def test_block_card(self):
        repo = MockBankRepository()
        assert repo.block_card("1234567890123456") is True
        assert repo.get_account("1234567890123456").is_blocked is True

    def test_change_pin(self):
        repo = MockBankRepository()
        assert repo.change_pin("1234567890123456", "5555") is True
        assert repo.validate_pin("1234567890123456", "5555") is True

    def test_transfer(self):
        repo = MockBankRepository()
        assert repo.transfer(
            "1234567890123456", "1111111111111111", Decimal("100")
        ) is True
        assert repo.get_account("1234567890123456").balance == Decimal("9900")
        assert repo.get_account("1111111111111111").balance == Decimal("5100")

    def test_persistence(self, temp_data_dir):
        repo1 = MockBankRepository()
        repo1.update_balance("1234567890123456", Decimal("111"))
        repo2 = MockBankRepository()
        assert repo2.get_account("1234567890123456").balance == Decimal("111")

    def test_load_skips_invalid_card_number(self, temp_data_dir):
        import json
        path = temp_data_dir / "bank_accounts.json"
        path.write_text(
            json.dumps({
                "1234": {
                    "card_number": "1234",
                    "pin_hash": "h",
                    "balance": "0",
                    "is_blocked": False,
                    "owner_name": None,
                },
                "1234567890123456": {
                    "card_number": "1234567890123456",
                    "pin_hash": "hashed_pin_0000",
                    "balance": "100",
                    "is_blocked": False,
                    "owner_name": "Ok",
                    "expiry_date": "12/28",
                },
            }, indent=2),
            encoding="utf-8",
        )
        repo = MockBankRepository()
        assert repo.get_account("1234") is None
        assert repo.get_account("1234567890123456") is not None
        assert repo.get_account("1234567890123456").balance == Decimal("100")
