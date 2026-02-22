from decimal import Decimal

import pytest

from atm.bank_communication.account_data import AccountData


class TestAccountData:
    def test_create_valid(self):
        acc = AccountData("1234567890123456", "hash", Decimal("100"), False)
        assert acc.card_number == "1234567890123456"
        assert acc.balance == Decimal("100")
        assert acc.is_blocked is False

    def test_expiry_optional(self):
        acc = AccountData(
            "1234567890123456", "h", Decimal("0"), False, False, None, "12/28"
        )
        assert acc.expiry_date == "12/28"

    def test_empty_card_number_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            AccountData("", "h", Decimal("0"), False)

    def test_short_card_number_raises(self):
        with pytest.raises(ValueError, match="16 digits"):
            AccountData("1234", "h", Decimal("0"), False)

    def test_negative_balance_raises(self):
        with pytest.raises(ValueError, match="negative"):
            AccountData(
                "1234567890123456", "h", Decimal("-1"), False
            )

    def test_owner_name_optional(self):
        acc = AccountData(
            "1234567890123456", "h", Decimal("0"), False, False, "John"
        )
        assert acc.owner_name == "John"
