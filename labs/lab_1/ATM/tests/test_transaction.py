from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from atm.transaction.transaction import Transaction
from atm.transaction.withdrawal import WithdrawalTransaction
from atm.transaction.balance_inquiry import BalanceInquiryTransaction


class ConcreteTransaction(Transaction):
    def execute(self) -> bool:
        self.success = True
        return True


class TestTransaction:
    def test_get_result_message_success(self):
        atm = MagicMock()
        t = ConcreteTransaction(atm, amount=None)
        t.success = True
        assert "successful" in t.get_result_message()

    def test_get_result_message_failed(self):
        atm = MagicMock()
        t = ConcreteTransaction(atm, amount=None)
        t.success = False
        t.error_message = "No funds"
        assert "No funds" in t.get_result_message()


class TestWithdrawalTransaction:
    def test_execute_no_card(self):
        atm = MagicMock()
        atm.card_reader.get_current_card.return_value = None
        t = WithdrawalTransaction(atm, Decimal("100"))
        assert t.execute() is False
        assert "No card" in (t.error_message or "")

    def test_execute_success(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.bank_gateway.withdraw.return_value = True
        t = WithdrawalTransaction(atm, Decimal("200"))
        assert t.execute() is True
        atm.cash_dispenser.dispense.assert_called_once_with(200)

    def test_execute_insufficient_funds(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.bank_gateway.withdraw.return_value = False
        t = WithdrawalTransaction(atm, Decimal("100"))
        assert t.execute() is False


class TestBalanceInquiryTransaction:
    def test_execute_success(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.bank_gateway.get_balance.return_value = Decimal("5000")
        from atm.transaction.balance_inquiry import BalanceInquiryTransaction
        t = BalanceInquiryTransaction(atm)
        assert t.execute() is True
        assert t.success is True
