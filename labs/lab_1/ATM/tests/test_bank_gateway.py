from decimal import Decimal

import pytest

from atm.bank_communication.bank_gateway import BankGateway


class TestBankGateway:
    def test_get_balance(self):
        gw = BankGateway()
        bal = gw.get_balance("1234567890123456")
        assert bal is not None
        assert bal == Decimal("10000")

    def test_get_balance_blocked_returns_none(self):
        gw = BankGateway()
        assert gw.get_balance("9999999999999999") is None

    def test_withdraw(self):
        gw = BankGateway()
        assert gw.withdraw("1234567890123456", Decimal("100")) is True
        assert gw.get_balance("1234567890123456") == Decimal("9900")

    def test_deposit(self):
        gw = BankGateway()
        assert gw.deposit("1234567890123456", Decimal("500")) is True
        assert gw.get_balance("1234567890123456") == Decimal("10500")

    def test_validate_pin(self):
        gw = BankGateway()
        assert gw.validate_pin("1234567890123456", "0000") is True
        assert gw.validate_pin("1234567890123456", "wrong") is False

    def test_is_card_blocked(self):
        gw = BankGateway()
        assert gw.is_card_blocked("9999999999999999") is True
        assert gw.is_card_blocked("1234567890123456") is False

    def test_get_account(self):
        gw = BankGateway()
        acc = gw.get_account("1234567890123456")
        assert acc is not None
        assert acc.expiry_date is not None

    def test_transfer(self):
        gw = BankGateway()
        assert gw.transfer(
            "1234567890123456", "1111111111111111", Decimal("200")
        ) is True
        assert gw.get_balance("1234567890123456") == Decimal("9800")
        assert gw.get_balance("1111111111111111") == Decimal("5200")
