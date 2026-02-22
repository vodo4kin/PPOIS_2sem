from decimal import Decimal
from unittest.mock import MagicMock

from atm.transaction.deposit import DepositTransaction
from atm.transaction.pin_change import PinChangeTransaction
from atm.transaction.transfer import TransferTransaction
from atm.transaction.payment import PaymentTransaction


class TestDepositTransaction:
    def test_execute_cancelled(self):
        atm = MagicMock()
        atm.keypad.read_input.return_value = ""
        t = DepositTransaction(atm)
        assert t.execute() is False
        assert "cancelled" in (t.error_message or "").lower()

    def test_execute_success(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.keypad.read_input.return_value = "100:2 50:4"
        atm.cash_acceptor.accept.return_value = 400
        atm.bank_gateway.deposit.return_value = True
        t = DepositTransaction(atm)
        assert t.execute() is True
        atm.bank_gateway.deposit.assert_called_once()
        call_args = atm.bank_gateway.deposit.call_args
        assert call_args[0][1] == Decimal(400)


class TestPinChangeTransaction:
    def test_execute_no_card(self):
        atm = MagicMock()
        atm.card_reader.get_current_card.return_value = None
        t = PinChangeTransaction(atm)
        assert t.execute() is False
        assert "No card" in (t.error_message or "")


class TestTransferTransaction:
    def test_execute_success(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.bank_gateway.transfer.return_value = True
        t = TransferTransaction(atm, Decimal("100"), "1111111111111111")
        assert t.execute() is True

    def test_execute_no_card(self):
        atm = MagicMock()
        atm.card_reader.get_current_card.return_value = None
        t = TransferTransaction(atm, Decimal("100"), "1111111111111111")
        assert t.execute() is False
        assert "No card" in (t.error_message or "")

    def test_execute_invalid_amount(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        t = TransferTransaction(atm, Decimal("-1"), "1111111111111111")
        assert t.execute() is False
        t2 = TransferTransaction(atm, Decimal("0"), "1111111111111111")
        assert t2.execute() is False

    def test_execute_transfer_fails(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.bank_gateway.transfer.return_value = False
        t = TransferTransaction(atm, Decimal("100"), "1111111111111111")
        assert t.execute() is False

    def test_execute_invalid_to_card(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        t = TransferTransaction(atm, Decimal("100"), "1234")
        assert t.execute() is False
        assert "16 digits" in (t.error_message or "")


class TestPaymentTransaction:
    def test_execute_success(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.bank_gateway.withdraw.return_value = True
        t = PaymentTransaction(atm, Decimal("50"), "Utilities")
        assert t.execute() is True

    def test_execute_no_card(self):
        atm = MagicMock()
        atm.card_reader.get_current_card.return_value = None
        t = PaymentTransaction(atm, Decimal("50"), "Utilities")
        assert t.execute() is False
        assert "No card" in (t.error_message or "")

    def test_execute_invalid_amount(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        t = PaymentTransaction(atm, Decimal("-1"), "Utilities")
        assert t.execute() is False

    def test_execute_insufficient_funds(self):
        atm = MagicMock()
        card = MagicMock()
        card.number = "1234567890123456"
        atm.card_reader.get_current_card.return_value = card
        atm.bank_gateway.withdraw.return_value = False
        t = PaymentTransaction(atm, Decimal("50"), "Utilities")
        assert t.execute() is False
        assert "Insufficient" in (t.error_message or "") or "failed" in (t.error_message or "").lower()
