from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from atm.transaction.transaction_factory import TransactionFactory
from atm.transaction.transfer import TransferTransaction
from atm.transaction.payment import PaymentTransaction


class TestTransactionFactory:
    def test_create_balance(self):
        atm = MagicMock()
        t = TransactionFactory.create("balance", atm)
        assert t.__class__.__name__ == "BalanceInquiryTransaction"

    def test_create_withdraw(self):
        atm = MagicMock()
        t = TransactionFactory.create("withdraw", atm, {"amount": 100})
        assert t.__class__.__name__ == "WithdrawalTransaction"
        assert t.amount == Decimal(100)

    def test_create_transfer(self):
        atm = MagicMock()
        t = TransactionFactory.create(
            "transfer", atm, {"amount": 50, "to_card": "1111111111111111"}
        )
        assert isinstance(t, TransferTransaction)
        assert t.amount == Decimal(50)
        assert t.to_card_number == "1111111111111111"

    def test_create_payment(self):
        atm = MagicMock()
        t = TransactionFactory.create(
            "payment", atm, {"amount": 25, "service_name": "Electricity"}
        )
        assert isinstance(t, PaymentTransaction)
        assert t.amount == Decimal(25)
        assert t.service_name == "Electricity"

    def test_create_unknown_raises(self):
        atm = MagicMock()
        with pytest.raises(ValueError, match="Unknown"):
            TransactionFactory.create("unknown", atm)
